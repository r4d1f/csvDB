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
        Dialog.resize(500, 125)
        Dialog.setMinimumSize(QtCore.QSize(500, 125))
        Dialog.setMaximumSize(QtCore.QSize(500, 125))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.cboxDocVid = QtWidgets.QCheckBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cboxDocVid.setFont(font)
        self.cboxDocVid.setObjectName("cboxDocVid")
        self.verticalLayout.addWidget(self.cboxDocVid)
        self.cboxCodSpec = QtWidgets.QCheckBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cboxCodSpec.setFont(font)
        self.cboxCodSpec.setObjectName("cboxCodSpec")
        self.verticalLayout.addWidget(self.cboxCodSpec)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnOK = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnOK.setFont(font)
        self.btnOK.setObjectName("btnOK")
        self.horizontalLayout.addWidget(self.btnOK)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Правила"))
        self.cboxDocVid.setText(_translate("Dialog", "Проверить поля \"Вид документа\" и \"Уровень образования\""))
        self.cboxCodSpec.setText(_translate("Dialog", "Проверить поле \"Код специальности\""))
        self.btnOK.setText(_translate("Dialog", "Принять"))
