import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog
from rna_app import Ui_rna_app
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
import time


class MainWindow(QtWidgets.QWidget, Ui_rna_app):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.load_btn.clicked.connect(self.load_data)
        self.counts = None

        self.load_metada_btn.clicked.connect(self.load_metadata)
        self.save_metadata_btn.clicked.connect(self.save_metadata)

        self.tabWidget.tabBarClicked.connect(self.on_tab_clicked)

        self.condition1_combo.currentIndexChanged.connect(self.check_conditions)
        self.condition2_combo.currentIndexChanged.connect(self.check_conditions)
        self.condition1 = None
        self.condition2 = None

        self.de_btn.clicked.connect(self.run_de)

    def load_data(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open File", "", "CSV Files (*.csv)"
        )
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
            self.selected_lbl.setText("Selected file: " + file_path.split("/")[-1])
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
            self, "Save File", "", "CSV Files (*.csv)"
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
        if index == 2:
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
        self.de_status_llbl.setText("Running DE analysis")
        self.de_status_llbl.repaint()

        metadata = self.metadata[
            (self.metadata["Condition"] == self.condition1)
            | (self.metadata["Condition"] == self.condition2)
        ]
        metadata = self.metadata.set_index("Sample")

        batch = self.counts.T
        batch = batch.loc[metadata.index]

        print(self.condition1, self.condition2)

        start_time = time.time()
        dds = DeseqDataSet(
            counts=batch, metadata=metadata, design_factors=["Condition"]
        )
        dds.deseq2()
        stats = DeseqStats(
            dds, contrast=["Condition", self.condition1, self.condition2]
        )

        end_time = time.time()
        execution_time = end_time - start_time

        self.de_status_llbl.setText(
            f"DE analysis completed in {execution_time:.2f} seconds"
        )
        print(stats.summary())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
