# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 390)
        MainWindow.setMinimumSize(QtCore.QSize(550, 390))
        MainWindow.setMaximumSize(QtCore.QSize(550, 390))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(9, 9, 531, 291))
        self.listWidget.setObjectName("listWidget")
        self.btnBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowse.setGeometry(QtCore.QRect(300, 352, 91, 31))
        self.btnBrowse.setIconSize(QtCore.QSize(16, 16))
        self.btnBrowse.setObjectName("btnBrowse")
        self.btnAddToDB = QtWidgets.QPushButton(self.centralwidget)
        self.btnAddToDB.setGeometry(QtCore.QRect(410, 352, 135, 31))
        self.btnAddToDB.setObjectName("btnAddToDB")
        self.btnEmpty = QtWidgets.QPushButton(self.centralwidget)
        self.btnEmpty.setGeometry(QtCore.QRect(10, 360, 101, 21))
        self.btnEmpty.setObjectName("btnEmpty")
        self.btnRules = QtWidgets.QPushButton(self.centralwidget)
        self.btnRules.setGeometry(QtCore.QRect(10, 330, 75, 23))
        self.btnRules.setObjectName("btnRules")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавление csv в БД"))
        self.btnBrowse.setText(_translate("MainWindow", "Выбрать файлы"))
        self.btnAddToDB.setText(_translate("MainWindow", "Добавить в базу данных"))
        self.btnEmpty.setText(_translate("MainWindow", "Пустые поля"))
        self.btnRules.setText(_translate("MainWindow", "Правила"))
