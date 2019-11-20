##-*- coding: utf-8 -*-

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
        self.msg0 = QtWidgets.QMessageBox()
        self.msg0.setWindowTitle('Информация')
        self.msg0.setText('Ошибка! Проверьте файлы')
        self.msg1 = QtWidgets.QMessageBox()
        self.msg1.setWindowTitle('Информация')
        self.msg1.setText('Файлы успешно добавлены в базу данных')
        self.msg2 = QtWidgets.QMessageBox()
        self.msg2.setWindowTitle('Информация')
        self.msg2.setText('В некоторых файлах обнаружены ошибки, нажмите "OK" для получения Информации')
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
        self.centralwidget.setEnabled(False)
        ans, wrong_files = source.f1(self.rules_arr, self.empty_arr, files, self)
        if ans == 0:
            self.msg0.exec()
        if ans == 1:
            self.msg1.exec()
        if ans == 2:
            self.msg2.exec()
            self.error_file(wrong_files)
        self.centralwidget.setEnabled(True)

    def on_update(self, data):
        self.progressBar.setValue(data)

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

    def error_file(self, files):
        self.errmsg = QtWidgets.QMessageBox()
        self.errmsg.setWindowTitle('Ошибка')
        error_str = 'Ошибка в файлах:\n'
        for file in files:
            error_str+= str(file) + '\n'
        self.errmsg.setText(error_str)
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