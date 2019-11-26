##-*- coding: utf-8 -*-

import sys  
from PyQt5 import QtWidgets
import design  
import os
import source
import source_higher_education
import rules
import setempty
import lvl

class Message():
    def __init__(self, title, text):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle(title)
        self.msg.setText(text)
    def exec(self):
        self.msg.exec()

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.btnBrowse.clicked.connect(self.browse_folder)
        self.btnAddToDB.clicked.connect(self.add_to_db)
        self.btnRules.clicked.connect(self.set_rules)
        self.btnEmpty.clicked.connect(self.set_empty)
        self.btnLvl.clicked.connect(self.set_lvl)
        self.errCheckFilesMsg = Message('Ошибка', 'Ошибка! Проверьте файлы')
        self.errGetInfoMsg = Message('Ошибка', 'В некоторых файлах обнаружены ошибки, нажмите "OK" для получения Информации')
        self.errLvl = Message('Ошибка', 'Не выбран уровень образования!')
        self.succMsg = Message('Успешно', 'Файлы успешно добавлены в базу данных')
        self.rules_arr = [False, False]
        self.empty_arr = [False for _ in range(0, 33)]
        self.lvl_arr = [False, False]
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
        if (self.lvl_arr[0] == False and self.lvl_arr[1] == False):
            self.errLvl.exec()
            return
        elif self.lvl_arr[0] == True:
            ans, wrong_files = source.f1(self.rules_arr, self.empty_arr, files, self)
        elif self.lvl_arr[1] == True:
            ans, wrong_files = source_higher_education.f1(self.rules_arr, self.empty_arr, files, self)   
        if ans == 0:
            self.errCheckFilesMsg.exec()
        elif ans == 1:
            self.succMsg.exec()
        elif ans == 2:
            self.errGetInfoMsg.exec()
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

    def set_lvl(self):
        win = LvlWin(self.lvl_arr)
        win.setModal(True)
        win.exec()
        self.lvl_arr = win.get_lvl()

    def error_file(self, files):
        error_str = 'Ошибка в файлах:\n'
        for file in files:
            error_str+= str(file) + '\n'
        self.errFilesMsg = Message('Ошибка', error_str)
        self.errFilesMsg.exec()

class RulesWin(QtWidgets.QDialog, rules.Ui_Dialog):
        def __init__(self, rules_arr):
            super().__init__()
            self.setupUi(self)  
            self.btnOK.clicked.connect(self.accept_rules)
            self.cboxDocVid.setChecked(rules_arr[0])
            self.cboxCodSpec.setChecked(rules_arr[1])
            self.rules_arr = rules_arr
        def accept_rules(self):
            self.rules_arr[0] = self.cboxDocVid.isChecked()
            self.rules_arr[1] = self.cboxCodSpec.isChecked()
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

class LvlWin(QtWidgets.QDialog, lvl.Ui_Dialog):
    def __init__(self, lvl_arr):
        super().__init__()
        self.setupUi(self)  
        self.btnOK.clicked.connect(self.accept_lvl)
        self.radSred.setChecked(lvl_arr[0]) 
        self.radVish.setChecked(lvl_arr[1])
        self.lvl_arr = lvl_arr
    def accept_lvl(self):
        self.lvl_arr[0] = self.radSred.isChecked()
        self.lvl_arr[1] = self.radVish.isChecked()
        self.close()
    def get_lvl(self):
        return self.lvl_arr


def main():
    app = QtWidgets.QApplication(sys.argv) 
    window = ExampleApp()  
    window.show()  
    app.exec_() 

if __name__ == '__main__':  
    main()  