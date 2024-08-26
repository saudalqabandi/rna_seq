import sys
from PySide6 import QtWidgets
from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import QFileDialog
from rna_app_ui import Ui_rna_app
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
import time
import pickle
from plot_app import Ui_plotter


class MainWindow(QtWidgets.QWidget, Ui_rna_app):
    update_status_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.load_btn.clicked.connect(self.load_data)
        self.counts = None
        self.file_name = None

        self.load_metada_btn.clicked.connect(self.load_metadata)
        self.save_metadata_btn.clicked.connect(self.save_metadata)

        self.tabWidget.tabBarClicked.connect(self.on_tab_clicked)

        self.condition1_combo.currentIndexChanged.connect(self.check_conditions)
        self.condition2_combo.currentIndexChanged.connect(self.check_conditions)
        self.condition1 = None
        self.condition2 = None

        self.de_btn.clicked.connect(self.run_de)

        self.dds = None
        self.stats = None

        self.update_status_signal.connect(self.update_status)

    def load_data(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open File", "", "CSV Files (*.csv)"
        )
        self.file_name = file_path.split("/")[-1].replace(".csv", "")

        if file_path:
            self.selected_lbl.setText("Selected file: " + file_path.split("/")[-1])
            self.counts = pd.read_csv(file_path, index_col=0)
            self.counts.fillna(0, inplace=True)
            self.counts = self.counts[self.counts.sum(axis=1) > 0]
            self.counts = self.counts.astype(int)

            for column in self.counts.columns:
                row_count = self.metadata_tbl.rowCount()
                self.metadata_tbl.insertRow(row_count)
                self.metadata_tbl.setItem(
                    row_count, 0, QtWidgets.QTableWidgetItem(column)
                )

    def load_metadata(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open File", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.metadata = pd.read_csv(file_path)

            self.metadata_tbl.setRowCount(0)
            for _, row in self.metadata.iterrows():
                row_count = self.metadata_tbl.rowCount()
                self.metadata_tbl.insertRow(row_count)
                self.metadata_tbl.setItem(
                    row_count, 0, QtWidgets.QTableWidgetItem(row["Sample"])
                )
                self.metadata_tbl.setItem(
                    row_count, 1, QtWidgets.QTableWidgetItem(row["Condition"])
                )

    def save_metadata(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(
            self, "Save File", f"{self.file_name}_metadata", "CSV Files (*.csv)"
        )

        if self.metadata_tbl.rowCount() > 0:
            self.metadata = pd.DataFrame()
            for row in range(self.metadata_tbl.rowCount()):
                for column in range(self.metadata_tbl.columnCount()):
                    item = self.metadata_tbl.item(row, column)
                    if item is not None:
                        self.metadata.loc[row, column] = item.text()
            self.metadata.columns = ["Sample", "Condition"]

        if file_path:
            self.metadata.to_csv(file_path, index=False)

    def on_tab_clicked(self, index):
        if index == 1:
            conditions = self.metadata["Condition"].unique()

            self.condition1_combo.clear()
            self.condition2_combo.clear()

            self.condition1_combo.addItems(conditions)
            self.condition2_combo.addItems(conditions)

    def check_conditions(self):
        self.condition1 = self.condition1_combo.currentText()
        self.condition2 = self.condition2_combo.currentText()

        if self.condition1 == "" or self.condition2 == "":
            self.batch_err_lbl.setText("Select conditions")
            self.de_btn.setDisabled(True)

        if self.condition1 == self.condition2:
            self.batch_err_lbl.setText("Conditions must be different")
            self.de_btn.setDisabled(True)
        else:
            self.batch_err_lbl.setText("")
            self.de_btn.setDisabled(False)

    def run_de(self):
        self.de_status_lbl.setText("Starting DE analysis")
        self.de_status_lbl.update()
        self.condition1_combo.setDisabled(True)
        self.condition2_combo.setDisabled(True)

        current_index = self.tabWidget.currentIndex()
        for i in range(self.tabWidget.count()):
            if i != current_index:
                self.tabWidget.setTabEnabled(i, False)

        self.thread = QThread()
        self.thread.run = self.differential_expression_analysis

        self.thread.finished.connect(self.on_analysis_complete)
        self.thread.start()

    def differential_expression_analysis(self):
        self.update_status_signal.emit("Running DE analysis")

        metadata = self.metadata[
            (self.metadata["Condition"] == self.condition1)
            | (self.metadata["Condition"] == self.condition2)
        ]
        metadata = self.metadata.set_index("Sample")

        batch = self.counts.T
        batch = batch.loc[metadata.index]

        start_time = time.time()
        dds = DeseqDataSet(
            counts=batch, metadata=metadata, design_factors=["Condition"]
        )
        dds.deseq2(fit_type="mean")
        stats = DeseqStats(
            dds, contrast=["Condition", self.condition1, self.condition2]
        )
        stats.summary()

        self.dds = dds
        self.stats = stats

        end_time = time.time()
        execution_time = end_time - start_time

        self.update_status_signal.emit(
            f"DE analysis completed in {execution_time:.2f} seconds"
        )

    @Slot(str)
    def update_status(self, message):
        self.de_status_lbl.setText(message)
        self.de_status_lbl.update()

    def on_analysis_complete(self):
        for i in range(self.tabWidget.count()):
            self.tabWidget.setTabEnabled(i, True)

        self.condition1_combo.setDisabled(False)
        self.condition2_combo.setDisabled(False)

        self.thread.wait()
        self.thread.deleteLater()

        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(
            self,
            "Save File",
            f"{self.file_name}_{self.condition1.lower()}_{self.condition2.lower()}",
            "Pickle Files (*.pkl)",
        )

        if file_path:
            with open(file_path, "wb") as f:
                pickle.dump(self.dds, f)

            if self.de_save_csv.isChecked():
                file_path = file_path.replace(".pkl", ".csv")
                self.stats.results_df.to_csv(file_path)

    def load_de(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open File", "", "Pickle Files (*.pkl)"
        )

        with open(file_path, "rb") as f:
            dds = pickle.load(f)

        try:
            self.stats = pd.read_csv(file_path.replace(".pkl", ".csv"))
        except FileNotFoundError:
            stats = DeseqStats(
                dds, contrast=["Condition", self.condition1, self.condition2]
            )
            stats.summary()
            self.stats = stats.results_df()

        self.dds = dds


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
