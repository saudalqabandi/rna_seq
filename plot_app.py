import sys
import os
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QTimer
from plot_app_ui import Ui_plotter
from pydeseq2.ds import DeseqStats
import pandas as pd
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from gtf import get_annotations
from custom_inference import CustomInference
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure


class MainWindow(QtWidgets.QWidget, Ui_plotter):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.data_load_btn.clicked.connect(self.load_data)
        self.dds = None
        self.stats = None
        self.gtf = get_annotations()
        self.canvas = Canvas(self.plot_frame)

        self.update_btn.clicked.connect(self.update_plot)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.update_plot)
        self.updated_item = None

        self.save_btn.clicked.connect(self.save_plot)

        self.plot_combo.currentIndexChanged.connect(self.plot)

    def plot(self):
        self.canvas.axes.clear()

        if hasattr(self.canvas, "colorbar") and self.canvas.colorbar is not None:
            try:
                self.canvas.colorbar.remove()
            except AttributeError:
                print("No colorbar to remove")
            self.canvas.colorbar = None

        self.canvas.draw()
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
            self.canvas.data = df
            self.canvas.volcano_plot()
            self.canvas.draw()

        if self.plot_combo.currentText() == "Heatmap":
            sigs = self.stats[self.stats["padj"] < 0.05]
            if sigs.empty:
                self.canvas.no_sig_genes()
                self.canvas.draw()
                return
            self.dds.layers["log1p"] = np.log1p(self.dds.layers["normed_counts"])

            dds_sigs = self.dds[:, sigs.index]

            graph_data = pd.DataFrame(
                dds_sigs.layers["log1p"].T,
                index=dds_sigs.var_names,
                columns=dds_sigs.obs_names,
            )

            graph_data.index = graph_data.index.map(self.gtf)
            self.canvas.title = self.title_input.text()
            self.canvas.data = graph_data
            self.canvas.heatmap_plot()
            self.canvas.draw()

    def load_data(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open File", "", "Pickle Files (*.pkl)"
        )
        file_name = file_path.split("/")[-1].replace(".pkl", "")

        with open(file_path, "rb") as f:
            dds = pickle.load(f)

        if file_name + ".csv" in os.listdir(os.path.dirname(file_path)):
            self.stats = pd.read_csv(file_path.replace(".pkl", ".csv"), index_col=0)
        else:
            stats = DeseqStats(dds, inference=CustomInference(backend="threading"))
            stats.summary()
            self.data_load_lbl.setText("Running Wald Test")
            self.stats = stats.results_df

        self.dds = dds
        self.data_load_lbl.setText(f"Loaded: {file_name}")
        self.stats["symbol"] = self.stats.index.map(lambda x: self.gtf[x])

    def map_colour(self, df):
        log2FoldChange, nlog10 = df

        if abs(log2FoldChange) > 7 and nlog10 >= 3:
            return "Highly Significant"
        elif abs(log2FoldChange) > 1 and nlog10 >= 1.3:
            return "Significant"
        else:
            return "Not Significant"

    def update_plot(self):
        if self.title_input.text():
            self.canvas.axes.set_title(self.title_input.text())

        if self.xmin_input.text():
            self.canvas.axes.set_xlim(float(self.xmin_input.text()), None)

        if self.xmax_input.text():
            self.canvas.axes.set_xlim(None, float(self.xmax_input.text()))

        if self.ymin_input.text():
            self.canvas.axes.set_ylim(float(self.ymin_input.text()), None)

        if self.ymax_input.text():
            self.canvas.axes.set_ylim(None, float(self.ymax_input.text()))

        self.canvas.draw()

    def save_plot(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(
            self,
            "Save File",
            self.title_input.text().replace(" ", "_"),
            "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;PDF Files (*.pdf)",
        )

        if file_path:
            self.canvas.fig.savefig(file_path)
            self.canvas.data.to_csv(file_path.rsplit(".", 1)[0] + ".csv")


class Canvas(FigureCanvas):
    def __init__(self, parent):
        self.dpi = 100
        rect = tuple(parent.geometry().getRect())[-2:]
        self.figsize = self.pxToInch(rect)
        self.fig, self.axes = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        self.data = None
        self.colorbar = None
        super().__init__(self.fig)
        self.setParent(parent)

        self.texts = []

    def volcano_plot(self):
        self.axes.clear()
        ax = sns.scatterplot(
            data=self.data,
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

        for spine in ax.spines.values():
            spine.set_visible(True)

        ax.set_title(self.title)
        self.fig.tight_layout()

        self.mpl_connect("button_press_event", self.on_click)

    def heatmap_plot(self):
        self.axes.clear()
        ax = sns.heatmap(data=self.data, ax=self.axes,cbar_kws={'label': 'log1p(normed_counts)'})
        self.colorbar = ax.collections[0].colorbar
        self.colorbar.set_label("log1p(normed_counts)")
        ax.set_xlim(0, self.data.shape[1])
        ax.set_ylim(0, self.data.shape[0])

        self.fig.tight_layout(rect=[0, 0, 1, 0.95])

    def no_sig_genes(self):
        self.axes.text(
            0.5,
            0.5,
            "No significant genes found",
            fontsize=12,
            ha="center",
            va="center",
        )

    def pxToInch(self, size):
        return tuple([x / self.dpi for x in size])

    def on_click(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            if event.button == 1:  # Left click
                closest_point = self.get_closest_point(x, y)
                if closest_point is not None:
                    self.add_label(closest_point)
                    self.draw()
            elif event.button == 3:  # Right click
                self.remove_nearest_label(x, y)
                self.draw()

    def get_closest_point(self, x, y):
        data_x = self.data["log2FoldChange"]
        data_y = self.data["nlog10"]
        distances = np.sqrt((data_x - x) ** 2 + (data_y - y) ** 2)
        min_index = np.argmin(distances)

        RADIUS = 0.5
        if distances[min_index] <= RADIUS:
            return data_x[min_index], data_y[min_index]
        else:
            return None

    def add_label(self, point):
        x, y = point
        index = self.data[
            (self.data["log2FoldChange"] == x) & (self.data["nlog10"] == y)
        ].index
        gene_symbol = self.data.loc[index, "symbol"].values[0]
        text = self.axes.text(
            x + 0.02, y + 0.02, gene_symbol, fontsize=9, ha="left", va="bottom"
        )
        self.texts.append(text)
        return text

    def remove_nearest_label(self, x, y):
        if not self.texts:
            return

        distances = []
        for text in self.texts:
            text_x, text_y = text.get_position()
            distance = np.sqrt((text_x - x) ** 2 + (text_y - y) ** 2)
            distances.append(distance)

        min_distance = min(distances)
        if min_distance <= 0.5:  # RADIUS
            min_index = distances.index(min_distance)
            self.texts[min_index].remove()
            del self.texts[min_index]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
