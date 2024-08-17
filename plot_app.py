# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plotter.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTabWidget,
    QWidget)

class Ui_plotter(object):
    def setupUi(self, plotter):
        if not plotter.objectName():
            plotter.setObjectName(u"plotter")
        plotter.resize(876, 544)
        self.tabWidget = QTabWidget(plotter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 10, 861, 531))
        self.tabWidget.setDocumentMode(True)
        self.data_tab = QWidget()
        self.data_tab.setObjectName(u"data_tab")
        self.data_frame = QFrame(self.data_tab)
        self.data_frame.setObjectName(u"data_frame")
        self.data_frame.setGeometry(QRect(10, 40, 271, 241))
        self.data_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.data_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.data_frame_lbl = QLabel(self.data_frame)
        self.data_frame_lbl.setObjectName(u"data_frame_lbl")
        self.data_frame_lbl.setGeometry(QRect(10, 10, 231, 16))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.data_frame_lbl.setFont(font)
        self.data_load_lbl = QLabel(self.data_frame)
        self.data_load_lbl.setObjectName(u"data_load_lbl")
        self.data_load_lbl.setGeometry(QRect(10, 80, 231, 16))
        self.data_load_btn = QPushButton(self.data_frame)
        self.data_load_btn.setObjectName(u"data_load_btn")
        self.data_load_btn.setGeometry(QRect(10, 30, 231, 41))
        self.tabWidget.addTab(self.data_tab, "")
        self.plot_tab = QWidget()
        self.plot_tab.setObjectName(u"plot_tab")
        self.xmax_input = QLineEdit(self.plot_tab)
        self.xmax_input.setObjectName(u"xmax_input")
        self.xmax_input.setGeometry(QRect(70, 470, 51, 22))
        self.ymax_lbl = QLabel(self.plot_tab)
        self.ymax_lbl.setObjectName(u"ymax_lbl")
        self.ymax_lbl.setGeometry(QRect(150, 470, 31, 20))
        self.xmin_input = QLineEdit(self.plot_tab)
        self.xmin_input.setObjectName(u"xmin_input")
        self.xmin_input.setGeometry(QRect(70, 440, 51, 22))
        self.plot_select_lbl = QLabel(self.plot_tab)
        self.plot_select_lbl.setObjectName(u"plot_select_lbl")
        self.plot_select_lbl.setGeometry(QRect(0, 0, 111, 16))
        self.title_lbl = QLabel(self.plot_tab)
        self.title_lbl.setObjectName(u"title_lbl")
        self.title_lbl.setGeometry(QRect(250, 20, 31, 16))
        self.title_input = QLineEdit(self.plot_tab)
        self.title_input.setObjectName(u"title_input")
        self.title_input.setGeometry(QRect(290, 20, 431, 22))
        self.xmax_lbl = QLabel(self.plot_tab)
        self.xmax_lbl.setObjectName(u"xmax_lbl")
        self.xmax_lbl.setGeometry(QRect(30, 470, 31, 20))
        self.plot_frame = QFrame(self.plot_tab)
        self.plot_frame.setObjectName(u"plot_frame")
        self.plot_frame.setGeometry(QRect(0, 60, 801, 361))
        self.plot_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.plot_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.ymax_input = QLineEdit(self.plot_tab)
        self.ymax_input.setObjectName(u"ymax_input")
        self.ymax_input.setGeometry(QRect(190, 470, 51, 22))
        self.ymin_lbl = QLabel(self.plot_tab)
        self.ymin_lbl.setObjectName(u"ymin_lbl")
        self.ymin_lbl.setGeometry(QRect(150, 440, 31, 20))
        self.ymin_input = QLineEdit(self.plot_tab)
        self.ymin_input.setObjectName(u"ymin_input")
        self.ymin_input.setGeometry(QRect(190, 440, 51, 22))
        self.plot_combo = QComboBox(self.plot_tab)
        self.plot_combo.addItem("")
        self.plot_combo.setObjectName(u"plot_combo")
        self.plot_combo.setGeometry(QRect(0, 20, 181, 22))
        self.xmin_lbl = QLabel(self.plot_tab)
        self.xmin_lbl.setObjectName(u"xmin_lbl")
        self.xmin_lbl.setGeometry(QRect(30, 440, 31, 20))
        self.tabWidget.addTab(self.plot_tab, "")

        self.retranslateUi(plotter)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(plotter)
    # setupUi

    def retranslateUi(self, plotter):
        plotter.setWindowTitle(QCoreApplication.translate("plotter", u"Plotter", None))
        self.data_frame_lbl.setText(QCoreApplication.translate("plotter", u"Data", None))
        self.data_load_lbl.setText("")
        self.data_load_btn.setText(QCoreApplication.translate("plotter", u"Load DE", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.data_tab), QCoreApplication.translate("plotter", u"Data", None))
        self.xmax_input.setText("")
        self.ymax_lbl.setText(QCoreApplication.translate("plotter", u"ymax:", None))
        self.plot_select_lbl.setText(QCoreApplication.translate("plotter", u"Select plot:", None))
        self.title_lbl.setText(QCoreApplication.translate("plotter", u"Title:", None))
        self.xmax_lbl.setText(QCoreApplication.translate("plotter", u"xmax:", None))
        self.ymax_input.setText("")
        self.ymin_lbl.setText(QCoreApplication.translate("plotter", u"ymin:", None))
        self.plot_combo.setItemText(0, QCoreApplication.translate("plotter", u"Volcano", None))

        self.xmin_lbl.setText(QCoreApplication.translate("plotter", u"xmin:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plot_tab), QCoreApplication.translate("plotter", u"Plot", None))
    # retranslateUi

