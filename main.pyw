## -*- coding: utf-8 -*-

import sys  
from PyQt5 import QtWidgets
import design  
import os
import source
import rules
import setempty

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.btnBrowse.clicked.connect(self.browse_folder)
        self.btnAddToDB.clicked.connect(self.add_to_db)
        self.btnRules.clicked.connect(self.set_rules)
        self.btnEmpty.clicked.connect(self.set_empty)
        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle('Информация')
        self.msg.setText('Файлы успешно добавлены в базу данных')
        self.rules_arr = [False, False]
        self.empty_arr = [False for _ in range(0, 33)]
        for i in range(25, 33):
            self.empty_arr[i] = True
    def browse_folder(self):
        self.listWidget.clear() 
        path = QtWidgets.QFileDialog.getOpenFileNames(self, "Выберите файлы", filter = "(*.csv)")

        if path:  
            for file_name in path[0]:  
                self.listWidget.addItem(file_name)  
    def add_to_db(self):
        files = []
        for i in range(self.listWidget.count()):
            files.append(self.listWidget.item(i).text())
        if source.f(self.rules_arr, self.empty_arr, files, self):
            self.msg.exec()

    def set_rules(self):
        win = RulesWin(self.rules_arr)
        win.setModal(True)
        win.exec()
        self.rules_arr = win.get_rules()

    def set_empty(self):
        win = EmptyWin(self.empty_arr)
        win.setModal(True)
        win.exec()
        self.empty_arr = win.get_empty()

    def error_file(self, file):
        self.errmsg = QtWidgets.QMessageBox()
        self.errmsg.setWindowTitle('Ошибка')
        self.errmsg.setText(f'Ошибка в файле {file}')
        self.errmsg.exec()

class RulesWin(QtWidgets.QDialog, rules.Ui_Dialog):
        def __init__(self, rules_arr):
            super().__init__()
            self.setupUi(self)  
            self.btnOK.clicked.connect(self.accept_rules)
            self.cboxDocVid.setChecked(rules_arr[0])
            self.cboxCodSpec.setChecked(rules_arr[1])
            self.rules_arr = rules_arr
        def accept_rules(self):
            if self.cboxDocVid.isChecked():
                self.rules_arr[0] = True
            else:
                self.rules_arr[0] = False
            if self.cboxCodSpec.isChecked():
                self.rules_arr[1] = True
            else:
                self.rules_arr[1] = False
            self.close()
        def get_rules(self):
            return self.rules_arr

class EmptyWin(QtWidgets.QDialog, setempty.Ui_Dialog):
    def __init__(self, empty_arr):
            super().__init__()
            self.setupUi(self)  
            self.btnOK.clicked.connect(self.accept_empty)
            i = 0
            for checkbox in self.groupBox.findChildren(QtWidgets.QCheckBox):
                checkbox.setChecked(empty_arr[i])
                i += 1
            self.empty_arr = empty_arr
    def accept_empty(self):
            i = 0
            for checkbox in self.groupBox.findChildren(QtWidgets.QCheckBox):
                self.empty_arr[i] = checkbox.isChecked()
                i += 1
            self.close()
    def get_empty(self):
        return self.empty_arr


def main():
    app = QtWidgets.QApplication(sys.argv) 
    window = ExampleApp()  
    window.show()  
    app.exec_() 

if __name__ == '__main__':  
    main()  