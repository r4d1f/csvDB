# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lvl.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 120)
        Dialog.setMinimumSize(QtCore.QSize(280, 120))
        Dialog.setMaximumSize(QtCore.QSize(280, 120))
        self.radSred = QtWidgets.QRadioButton(Dialog)
        self.radSred.setGeometry(QtCore.QRect(10, 11, 191, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radSred.setFont(font)
        self.radSred.setObjectName("radSred")
        self.radVish = QtWidgets.QRadioButton(Dialog)
        self.radVish.setGeometry(QtCore.QRect(10, 44, 191, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radVish.setFont(font)
        self.radVish.setObjectName("radVish")
        self.btnOK = QtWidgets.QPushButton(Dialog)
        self.btnOK.setGeometry(QtCore.QRect(103, 80, 75, 23))
        self.btnOK.setObjectName("btnOK")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Уровень образования"))
        self.radSred.setText(_translate("Dialog", "Среднее образование"))
        self.radVish.setText(_translate("Dialog", "Высшее образование"))
        self.btnOK.setText(_translate("Dialog", "Принять"))
