# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'musical.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(549, 289)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pbtn_reflash = QPushButton(self.centralwidget)
        self.pbtn_reflash.setObjectName(u"pbtn_reflash")
        self.pbtn_reflash.setGeometry(QRect(189, 120, 171, 41))
        font = QFont()
        font.setPointSize(13)
        self.pbtn_reflash.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pbtn_reflash.setText(QCoreApplication.translate("MainWindow", u"Reflash", None))
    # retranslateUi

