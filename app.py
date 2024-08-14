import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog
from rna_app import Ui_rna_app
import pandas as pd


class MainWindow(QtWidgets.QWidget, Ui_rna_app):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.load_btn.clicked.connect(self.load_data)
        self.counts = None

        self.load_metada_btn.clicked.connect(self.load_metadata)
        self.save_metadata_btn.clicked.connect(self.save_metadata)

    def load_data(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open File", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.selected_lbl.setText("Selected file: " + file_path.split("/")[-1])
            self.counts = pd.read_csv(file_path, index_col=0)

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
