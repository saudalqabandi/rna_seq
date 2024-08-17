import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QTimer
from plot_app import Ui_plotter
from pydeseq2.ds import DeseqStats
import pandas as pd
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure


class MainWindow(QtWidgets.QWidget, Ui_plotter):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.data_load_btn.clicked.connect(self.load_data)
        self.dds = None
        self.stats = None
        self.gtf = self.get_annotations()

        self.canvas = Canvas(self.plot_frame)
        self.plot()

        self.title_input.textChanged.connect(self.start_timer)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.update_plot)

    def start_timer(self):
        self.timer.start(500)

    def plot(self):
        if self.stats is None:
            return

        if self.plot_combo.currentText() == "Volcano":
            df = self.stats
            df["symbol"] = df.index.map(lambda x: self.gtf[x])
            df["nlog10"] = -np.log10(df["padj"])
            df["colour"] = df[["log2FoldChange", "nlog10"]].apply(
                self.map_colour, axis=1
            )
            self.canvas.title = self.title_input.text()
            self.canvas.volcano_plot(data=df)

    def load_data(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open File", "", "Pickle Files (*.pkl)"
        )

        with open(file_path, "rb") as f:
            dds = pickle.load(f)

        try:
            self.stats = pd.read_csv(file_path.replace(".pkl", ".csv"), index_col=0)
        except FileNotFoundError:
            stats = DeseqStats(
                dds, contrast=["Condition", self.condition1, self.condition2]
            )
            stats.summary()
            self.stats = stats.results_df()
        self.dds = dds

        file_name = file_path.split("/")[-1].replace(".pkl", "")
        self.data_load_lbl.setText(f"Loaded: {file_name}")

        self.canvas.title = file_name + " Volcano Plot"
        self.plot()

    def map_colour(self, df):
        log2FoldChange, nlog10 = df

        if abs(log2FoldChange) > 7 and nlog10 >= 3:
            return "Highly Significant"
        elif abs(log2FoldChange) > 1 and nlog10 >= 1.3:
            return "Significant"
        else:
            return "Not Significant"

    def get_annotations(self):
        with open("gtf/gtf_gene_dict.json", "r") as f:
            gtf = json.load(f)
        return gtf

    def update_plot(self):
        self.canvas.axes.set_title(self.title_input.text())
        self.canvas.draw()


class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.axes = plt.subplots(figsize=(7, 3), dpi=100)
        super().__init__(fig)
        self.setParent(parent)

    def volcano_plot(self, data):
        ax = sns.scatterplot(
            data=data,
            x="log2FoldChange",
            y="nlog10",
            hue="colour",
            hue_order=["Not Significant", "Significant", "Highly Significant"],
            palette=["grey", "firebrick", "rebeccapurple"],
            ax=self.axes,
        )

        ax.axhline(1.3, zorder=0, c="k", lw=2, ls="--")
        ax.axvline(-1, zorder=0, c="k", lw=2, ls="--")
        ax.axvline(1, zorder=0, c="k", lw=2, ls="--")

        ax.set_title(self.title)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
