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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QTabWidget,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_rna_app(object):
    def setupUi(self, rna_app):
        if not rna_app.objectName():
            rna_app.setObjectName(u"rna_app")
        rna_app.resize(585, 304)
        self.horizontalLayout = QHBoxLayout(rna_app)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(rna_app)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setDocumentMode(True)
        self.data_tab = QWidget()
        self.data_tab.setObjectName(u"data_tab")
        self.data_frame = QFrame(self.data_tab)
        self.data_frame.setObjectName(u"data_frame")
        self.data_frame.setGeometry(QRect(9, 9, 272, 244))
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
        self.tabWidget.addTab(self.data_tab, "")
        self.metadata_tab = QWidget()
        self.metadata_tab.setObjectName(u"metadata_tab")
        self.metadata_frame = QFrame(self.metadata_tab)
        self.metadata_frame.setObjectName(u"metadata_frame")
        self.metadata_frame.setGeometry(QRect(0, 10, 571, 261))
        self.metadata_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.metadata_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.metadata_lbl = QLabel(self.metadata_frame)
        self.metadata_lbl.setObjectName(u"metadata_lbl")
        self.metadata_lbl.setGeometry(QRect(10, 10, 231, 16))
        self.metadata_lbl.setFont(font)
        self.metadata_tbl = QTableWidget(self.metadata_frame)
        if (self.metadata_tbl.columnCount() < 2):
            self.metadata_tbl.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.metadata_tbl.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.metadata_tbl.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.metadata_tbl.setObjectName(u"metadata_tbl")
        self.metadata_tbl.setGeometry(QRect(10, 40, 541, 151))
        self.widget = QWidget(self.metadata_frame)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(120, 210, 301, 26))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.load_metada_btn = QPushButton(self.widget)
        self.load_metada_btn.setObjectName(u"load_metada_btn")

        self.horizontalLayout_2.addWidget(self.load_metada_btn)

        self.save_metadata_btn = QPushButton(self.widget)
        self.save_metadata_btn.setObjectName(u"save_metadata_btn")

        self.horizontalLayout_2.addWidget(self.save_metadata_btn)

        self.tabWidget.addTab(self.metadata_tab, "")

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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.data_tab), QCoreApplication.translate("rna_app", u"Data", None))
        self.metadata_lbl.setText(QCoreApplication.translate("rna_app", u"Metadata", None))
        ___qtablewidgetitem = self.metadata_tbl.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("rna_app", u"Sample", None));
        ___qtablewidgetitem1 = self.metadata_tbl.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("rna_app", u"Condition", None));
        self.load_metada_btn.setText(QCoreApplication.translate("rna_app", u"Load", None))
        self.save_metadata_btn.setText(QCoreApplication.translate("rna_app", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.metadata_tab), QCoreApplication.translate("rna_app", u"Metadata", None))
    # retranslateUi

