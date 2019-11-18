# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rules.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 120)
        Dialog.setMinimumSize(QtCore.QSize(500, 120))
        Dialog.setMaximumSize(QtCore.QSize(500, 120))
        self.btnOK = QtWidgets.QPushButton(Dialog)
        self.btnOK.setGeometry(QtCore.QRect(200, 80, 100, 30))
        self.btnOK.setObjectName("btnOK")
        self.cboxDocVid = QtWidgets.QCheckBox(Dialog)
        self.cboxDocVid.setGeometry(QtCore.QRect(10, 10, 471, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cboxDocVid.setFont(font)
        self.cboxDocVid.setObjectName("cboxDocVid")
        self.cboxCodSpec = QtWidgets.QCheckBox(Dialog)
        self.cboxCodSpec.setGeometry(QtCore.QRect(10, 40, 331, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cboxCodSpec.setFont(font)
        self.cboxCodSpec.setObjectName("cboxCodSpec")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Правила"))
        self.btnOK.setText(_translate("Dialog", "Принять"))
        self.cboxDocVid.setText(_translate("Dialog", "Проверить поля \"Вид документа\" и \"Уровень образования\""))
        self.cboxCodSpec.setText(_translate("Dialog", "Проверить поле \"Код специальности\""))
