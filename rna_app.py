# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rna_app.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_rna_app(object):
    def setupUi(self, rna_app):
        if not rna_app.objectName():
            rna_app.setObjectName(u"rna_app")
        rna_app.resize(606, 322)
        self.horizontalLayout = QHBoxLayout(rna_app)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(rna_app)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setDocumentMode(True)
        self.data_tab = QWidget()
        self.data_tab.setObjectName(u"data_tab")
        self.horizontalLayout_4 = QHBoxLayout(self.data_tab)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.data_frame = QFrame(self.data_tab)
        self.data_frame.setObjectName(u"data_frame")
        self.data_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.data_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.data_frame_lbl = QLabel(self.data_frame)
        self.data_frame_lbl.setObjectName(u"data_frame_lbl")
        self.data_frame_lbl.setGeometry(QRect(10, 10, 231, 16))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.data_frame_lbl.setFont(font)
        self.load_btn = QPushButton(self.data_frame)
        self.load_btn.setObjectName(u"load_btn")
        self.load_btn.setGeometry(QRect(10, 50, 231, 41))
        self.selected_lbl = QLabel(self.data_frame)
        self.selected_lbl.setObjectName(u"selected_lbl")
        self.selected_lbl.setGeometry(QRect(10, 100, 231, 16))

        self.horizontalLayout_4.addWidget(self.data_frame)

        self.metadata_frame = QFrame(self.data_tab)
        self.metadata_frame.setObjectName(u"metadata_frame")
        self.metadata_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.metadata_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.metadata_lbl = QLabel(self.metadata_frame)
        self.metadata_lbl.setObjectName(u"metadata_lbl")
        self.metadata_lbl.setGeometry(QRect(10, 10, 231, 16))
        self.metadata_lbl.setFont(font)
        self.layoutWidget_2 = QWidget(self.metadata_frame)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 200, 251, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.load_metada_btn = QPushButton(self.layoutWidget_2)
        self.load_metada_btn.setObjectName(u"load_metada_btn")

        self.horizontalLayout_3.addWidget(self.load_metada_btn)

        self.save_metadata_btn = QPushButton(self.layoutWidget_2)
        self.save_metadata_btn.setObjectName(u"save_metadata_btn")

        self.horizontalLayout_3.addWidget(self.save_metadata_btn)

        self.metadata_tbl = QTableWidget(self.metadata_frame)
        if (self.metadata_tbl.columnCount() < 2):
            self.metadata_tbl.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.metadata_tbl.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.metadata_tbl.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.metadata_tbl.setObjectName(u"metadata_tbl")
        self.metadata_tbl.setGeometry(QRect(10, 40, 251, 151))

        self.horizontalLayout_4.addWidget(self.metadata_frame)

        self.tabWidget.addTab(self.data_tab, "")
        self.de_tab = QWidget()
        self.de_tab.setObjectName(u"de_tab")
        self.de_frame = QFrame(self.de_tab)
        self.de_frame.setObjectName(u"de_frame")
        self.de_frame.setGeometry(QRect(280, 10, 272, 244))
        self.de_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.de_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.de_frame_lbl = QLabel(self.de_frame)
        self.de_frame_lbl.setObjectName(u"de_frame_lbl")
        self.de_frame_lbl.setGeometry(QRect(10, 10, 231, 16))
        self.de_frame_lbl.setFont(font)
        self.de_btn = QPushButton(self.de_frame)
        self.de_btn.setObjectName(u"de_btn")
        self.de_btn.setGeometry(QRect(10, 80, 231, 41))
        self.de_status_llbl = QLabel(self.de_frame)
        self.de_status_llbl.setObjectName(u"de_status_llbl")
        self.de_status_llbl.setGeometry(QRect(10, 130, 231, 16))
        self.de_save_csv = QCheckBox(self.de_frame)
        self.de_save_csv.setObjectName(u"de_save_csv")
        self.de_save_csv.setGeometry(QRect(10, 50, 79, 20))
        self.batch_frame = QFrame(self.de_tab)
        self.batch_frame.setObjectName(u"batch_frame")
        self.batch_frame.setGeometry(QRect(0, 10, 272, 244))
        self.batch_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.batch_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.batch_frame_lbl = QLabel(self.batch_frame)
        self.batch_frame_lbl.setObjectName(u"batch_frame_lbl")
        self.batch_frame_lbl.setGeometry(QRect(10, 10, 231, 16))
        self.batch_frame_lbl.setFont(font)
        self.condition1_combo = QComboBox(self.batch_frame)
        self.condition1_combo.setObjectName(u"condition1_combo")
        self.condition1_combo.setGeometry(QRect(20, 60, 221, 22))
        self.condition1_lbl = QLabel(self.batch_frame)
        self.condition1_lbl.setObjectName(u"condition1_lbl")
        self.condition1_lbl.setGeometry(QRect(20, 40, 121, 16))
        self.condition2_lbl = QLabel(self.batch_frame)
        self.condition2_lbl.setObjectName(u"condition2_lbl")
        self.condition2_lbl.setGeometry(QRect(20, 100, 121, 16))
        self.condition2_combo = QComboBox(self.batch_frame)
        self.condition2_combo.setObjectName(u"condition2_combo")
        self.condition2_combo.setGeometry(QRect(20, 120, 221, 22))
        self.batch_err_lbl = QLabel(self.batch_frame)
        self.batch_err_lbl.setObjectName(u"batch_err_lbl")
        self.batch_err_lbl.setGeometry(QRect(20, 160, 221, 16))
        self.tabWidget.addTab(self.de_tab, "")
        self.plt_tab = QWidget()
        self.plt_tab.setObjectName(u"plt_tab")
        self.plt_frame = QFrame(self.plt_tab)
        self.plt_frame.setObjectName(u"plt_frame")
        self.plt_frame.setGeometry(QRect(0, 0, 271, 244))
        self.plt_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.plt_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.plt_frame_lbl = QLabel(self.plt_frame)
        self.plt_frame_lbl.setObjectName(u"plt_frame_lbl")
        self.plt_frame_lbl.setGeometry(QRect(10, 10, 231, 16))
        self.plt_frame_lbl.setFont(font)
        self.plt_load_lbl = QLabel(self.plt_frame)
        self.plt_load_lbl.setObjectName(u"plt_load_lbl")
        self.plt_load_lbl.setGeometry(QRect(10, 80, 231, 16))
        self.plt_load_btn = QPushButton(self.plt_frame)
        self.plt_load_btn.setObjectName(u"plt_load_btn")
        self.plt_load_btn.setGeometry(QRect(10, 30, 231, 41))
        self.tabWidget.addTab(self.plt_tab, "")

        self.horizontalLayout.addWidget(self.tabWidget)


        self.retranslateUi(rna_app)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(rna_app)
    # setupUi

    def retranslateUi(self, rna_app):
        rna_app.setWindowTitle(QCoreApplication.translate("rna_app", u"RNA-Seq", None))
        self.data_frame_lbl.setText(QCoreApplication.translate("rna_app", u"Load counts file", None))
        self.load_btn.setText(QCoreApplication.translate("rna_app", u"Load Data", None))
        self.selected_lbl.setText(QCoreApplication.translate("rna_app", u"Selected file:", None))
        self.metadata_lbl.setText(QCoreApplication.translate("rna_app", u"Metadata", None))
        self.load_metada_btn.setText(QCoreApplication.translate("rna_app", u"Load", None))
        self.save_metadata_btn.setText(QCoreApplication.translate("rna_app", u"Save", None))
        ___qtablewidgetitem = self.metadata_tbl.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("rna_app", u"Sample", None));
        ___qtablewidgetitem1 = self.metadata_tbl.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("rna_app", u"Condition", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.data_tab), QCoreApplication.translate("rna_app", u"Data", None))
        self.de_frame_lbl.setText(QCoreApplication.translate("rna_app", u"Differential Expression", None))
        self.de_btn.setText(QCoreApplication.translate("rna_app", u"Run DE", None))
        self.de_status_llbl.setText("")
        self.de_save_csv.setText(QCoreApplication.translate("rna_app", u"Save CSV", None))
        self.batch_frame_lbl.setText(QCoreApplication.translate("rna_app", u"Batch", None))
        self.condition1_lbl.setText(QCoreApplication.translate("rna_app", u"Condition 1:", None))
        self.condition2_lbl.setText(QCoreApplication.translate("rna_app", u"Condition 2:", None))
        self.batch_err_lbl.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.de_tab), QCoreApplication.translate("rna_app", u"DE", None))
        self.plt_frame_lbl.setText(QCoreApplication.translate("rna_app", u"Plot", None))
        self.plt_load_lbl.setText("")
        self.plt_load_btn.setText(QCoreApplication.translate("rna_app", u"Load DE", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plt_tab), QCoreApplication.translate("rna_app", u"Plot", None))
    # retranslateUi

