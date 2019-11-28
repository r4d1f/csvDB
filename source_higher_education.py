import pypyodbc
import os
import csv
import re
import win32com.client
import datetime
import traceback
import sys
import time
from PyQt5 import QtCore

class SlowTask(QtCore.QThread):
    updated = QtCore.pyqtSignal(int)
    

    def __init__(self, *args, **kwargs):
        super(SlowTask, self).__init__(*args, **kwargs)
        self.percent = 0
        self.updated.emit(int(self.percent))

    def run(self, user_rules_dict, empty_cells, files, objWindow):
        print("Start time: " + str(datetime.datetime.now()))
        try:
            db = self.create_db()
            OGRN, KPP, wrong_files, correct_files = self.get_files_and_OGRN_KPP_from_name(files)
            if len(correct_files) != 0:
                data, wrong_files = self.get_data_from_csv_and_check_num_delimiters(correct_files, wrong_files)
                print("Обработка csv: " + str(datetime.datetime.now()))
                data, errors = self.check_data_logic(user_rules_dict, empty_cells, data)
                len_err = [len(data[i])-1 for i in range(len(data))]
                OGRN, KPP, num_sub_RF, priznak_organiz_from_KPP, errors = self.check_OGRN_KPP_get_num_sub_RF(OGRN, KPP, errors, len_err)
                self.log(files, os.getcwd(), errors, data)
                self.create_table(db, data[0])
                print("Добавленние в бд: " + str(datetime.datetime.now()))
                self.add_data(db, data, OGRN, KPP, num_sub_RF, priznak_organiz_from_KPP, objWindow, errors)
                global ERROR_DICT
                ERROR_DICT = ERROR_DICT.fromkeys(ERROR_DICT, 0)
                print("Done! End time: " + str(datetime.datetime.now()) + "\n")
                db.close()
                if len(wrong_files) == 0:
                    return (1, [])
                else:
                    return (2, wrong_files)
            else:
                return (0, wrong_files)
        except:
            print("Error! End time: " + str(datetime.datetime.now()) + "\n")
            print('Ошибка:\n', traceback.format_exc())
            return (0, [])

    def create_db(self):
        db_path = os.getcwd() + '/DB_h_e.mdb'
        if (not os.path.exists(db_path)):
            pypyodbc.win_create_mdb(db_path)    
        db = pypyodbc.win_connect_mdb(db_path) 
        return db

    def get_files_and_OGRN_KPP_from_name(self, files):
        csv_files_in_directory = []
        wrong_files = []
        correct_files = []
        for f in files:
            try:
                csv_files_in_directory.append(re.search(r'\d+-\d+[\s\S]*\.csv', f)[0])
                correct_files.append(f)
            except:
                wrong_files.append(f)
        OGRN = []
        KPP = []
        for i in range(len(csv_files_in_directory)):
            base = csv_files_in_directory[i][:-4]
            base = base.split('-')
            OGRN.append(base[0])
            KPP.append(base[1])
        return (OGRN, KPP, wrong_files, correct_files)

    def get_data_from_csv_and_check_num_delimiters(self, path_to_csv, wrong_files):
        data = []
        filesCount = len(path_to_csv)
        for i in range(filesCount):
            self.percent += 20/filesCount
            self.updated.emit(int(self.percent))
            try:
                with open(path_to_csv[i], newline='') as csvfile:
                    try:
                        data.append(list(csv.reader(csvfile, delimiter=';')))
                    except:
                        wrong_files.append(csvfile)
            except:
                path_to_csv[i] += ' - не удалось открыть'
                wrong_files.append(path_to_csv[i])
        for i in range(len(data)):
            j=1
            while (j < len(data[i])-1):
                if (data[i][j+1][0].isdigit()):
                    j+=1
                else:
                    data[i][j][-1] += data[i][j+1][0]
                    data[i][j+1].pop(0)
                    data[i][j] += data[i][j+1]
                    data[i].pop(j+1)
                
            for j in range(1, len(data[i])):
                if(len(data[i][j]) < 38):
                    while(len(data[i][j]) < 38):
                        data[i][j].append('')
                elif(len(data[i][j]) > 38):
                    data[i][j] = data[i][j][0:-(len(data[i][j]) - 38)]
        
        self.percent = 20
        self.updated.emit(int(self.percent))
        return (data, wrong_files)

    def check_OGRN_KPP_get_num_sub_RF(self, OGRN, KPP, errors, len_err):
        num_sub_RF = []
        priznak_organiz_from_KPP = []
        for i in range(len(OGRN)):
            if len(OGRN[i]) == 13:
                tmp = int(OGRN[i][0:-1])
                if tmp % 11 <= 9:
                    tmp_2 = tmp % 11
                else:
                    tmp_2 = (tmp % 11) % 10
                if tmp_2 != int(OGRN[i][12]):
                    n = 0
                    for k in range(i):
                        n += len_err[k]
                    for j in range(len_err[i]):
                        errors[n] += "(ОГРН) Неверная контрольная сумма; "
                        errors[n] += "(Номер субъекта РФ) Ошибка в ОГРН; "
                        n += 1
                    ERROR_DICT['Недопустимая контрольная сумма ОГРН'] += 1
                    num_sub_RF.append("--")
                else:
                    num_sub_RF.append(OGRN[i][3:5])
            else:
                n = 0
                for k in range(i):
                    n += len_err[k]
                for j in range(len_err[i]):
                    errors[n] += "(ОГРН) Недопустимое количество символов; "
                    errors[n] += "(Номер субъекта РФ) Ошибка в ОГРН; "
                    n += 1
                ERROR_DICT['Недопустимое количество символов ОГРН'] += 1
                num_sub_RF.append("--")
            if len(KPP[i]) != 9:
                n = 0
                for k in range(i):
                    n += len_err[k]
                for j in range(len_err[i]):
                    errors[n] += "(КПП) Недопустимое количество символов; "
                    errors[n] += "(Признак филиала, либо головной организации) Ошибка в КПП; "
                    n += 1
                    priznak_organiz_from_KPP.append('--')
                ERROR_DICT['Недопустимое количество символов КПП'] += 1
            else:
                priznak_organiz_from_KPP.append(KPP[i][4:6])
        return (OGRN, KPP, num_sub_RF, priznak_organiz_from_KPP, errors)
               
    def check_data_logic(self, user_rules_dict, empty_cells, data):
        len_data = 0
        for j in range(len(data)):
            for i in range(1, len(data[j])):
                len_data += 1
        errors = ['']*len_data
        n = 0
        for k in range(len(data)):
            for i in range(1,len(data[k])):
                try:
                    int(data[k][i][0])
                except:
                    errors[n] += "(id) Ожидалось число; "
                    ERROR_DICT['Ожидалось число'] += 1
                try:
                    int(data[k][i][10])
                except:
                    errors[n] += "(Серия документа) Ожидалось число; "
                    ERROR_DICT['Ожидалось число'] += 1
                try:
                    int(data[k][i][11])
                except:
                    errors[n] += "(Номер документа) Ожидалось число; "
                    ERROR_DICT['Ожидалось число'] += 1
                try:
                    int(data[k][i][13])
                except:
                    errors[n] += "(Регистрационный номер) Ожидалось число; "
                    ERROR_DICT['Ожидалось число'] += 1
                try:
                    int(data[k][i][18])
                except:
                    errors[n] += "(Год поступления) Ожидалось число; "
                    ERROR_DICT['Ожидалось число'] += 1
                try:
                    int(data[k][i][19])
                except:
                    errors[n] += "(Год окончания) Ожидалось число; "
                    ERROR_DICT['Ожидалось число'] += 1

                if re.search(r'[a-zA-Z0-9]', data[k][i][21]):
                    errors[n] += "(Фамилия получателя) Латинские буквы или цифры в строке; "
                    ERROR_DICT['Латинские буквы или цифры в строке'] += 1
                if re.search(r'[a-zA-Z0-9]', data[k][i][22]):
                    errors[n] += "(Имя получателя) Латинские буквы или цифры в строке; "
                    ERROR_DICT['Латинские буквы или цифры в строке'] += 1
                if re.search(r'[a-zA-Z0-9]', data[k][i][23]):
                    errors[n] += "(Отчество получателя) Латинские буквы или цифры в строке; "
                    ERROR_DICT['Латинские буквы или цифры в строке'] += 1
                if re.search(r'[a-zA-Z0-9]', data[k][i][35]):
                    errors[n] += "(Фамилия получателя (оригинала)) Латинские буквы или цифры в строке; "
                    ERROR_DICT['Латинские буквы или цифры в строке'] += 1
                if re.search(r'[a-zA-Z0-9]', data[k][i][36]):
                    errors[n] += "(Имя получателя (оригинала)) Латинские буквы или цифры в строке; "
                    ERROR_DICT['Латинские буквы или цифры в строке'] += 1
                if re.search(r'[a-zA-Z0-9]', data[k][i][37]):
                    errors[n] += "(Отчество получателя (оригинала)) Латинские буквы или цифры в строке; "
                    ERROR_DICT['Латинские буквы или цифры в строке'] += 1

                if re.search(r'\d\d.\d\d.\d\d\d\d', data[k][i][12]) == None:
                    errors[n] += "(Дата выдачи) Ожидалась дата; "
                    ERROR_DICT['Ожидалась дата'] += 1
                if re.search(r'\d\d.\d\d.\d\d\d\d', data[k][i][24]) == None:
                    errors[n] += "(Дата рождения получателя) Ожидалась дата; "
                    ERROR_DICT['Ожидалась дата'] += 1
                else:
                    if len(data[k][i][18]) == 4:
                        if ((int(data[k][i][18]) - int(data[k][i][24][6:10])) < 11) | ((int(data[k][i][18]) - int(data[k][i][24][6:10])) > 75):
                           errors[n] += "(Дата рождения получателя) Некорректная дата рождения; "
                           ERROR_DICT['Некорректная дата рождения'] += 1
                if data[k][i][34] != '':
                    if re.search(r'\d\d.\d\d.\d\d\d\d', data[k][i][34]) == None: 
                        errors[n] += "(Дата выдачи (оригинала)) Ожидалась дата; "
                        ERROR_DICT['Ожидалась дата'] += 1

                if user_rules_dict[1] == True:
                    if re.search(r'\d\d\d\d\d\d$', data[k][i][14]) == None:
                        errors[n] += "(Код специальности, направления подготовки) Неверный код специальности; "
                        ERROR_DICT['Неверный код специальности'] += 1
                    else:
                        if re.search(r'бакалавр', data[k][i][9]):
                            if data[k][i][14][2:4] != '03':
                                errors[n] += "(Код специальности, направления подготовки) Код специальности не совпадает с уровнем образования; "
                                ERROR_DICT['Код специальности не совпадает с уровнем образования'] += 1
                        elif re.search(r'магистр', data[k][i][9]):
                            if data[k][i][14][2:4] != '04':
                                errors[n] += "(Код специальности, направления подготовки) Код специальности не совпадает с уровнем образования; "
                                ERROR_DICT['Код специальности не совпадает с уровнем образования'] += 1
                        elif re.search(r'спец', data[k][i][9]):
                            if data[k][i][14][2:4] != '05':
                                errors[n] += "(Код специальности, направления подготовки) Код специальности не совпадает с уровнем образования; "
                                ERROR_DICT['Код специальности не совпадает с уровнем образования'] += 1

                    if (re.search(r'бакалавр', data[k][i][5])):
                        if re.search(r'бакалавр', data[k][i][9]) == None:
                            errors[n] += "(Уровень образования) Несоответствие виду документа об образовании; "
                            ERROR_DICT['Несоответствие виду документа об образовании'] += 1
                    elif (re.search(r'спец', data[k][i][5])):
                        if re.search(r'спец', data[k][i][9]) == None:
                            errors[n] += "(Уровень образования) Несоответствие виду документа об образовании; "
                            ERROR_DICT['Несоответствие виду документа об образовании'] += 1

                if (data[k][i][25] == "Муж") | (data[k][i][25] == "Жен"):
                    if data[k][i][23] != '':
                        if (data[k][i][23][-1] == "ч") & (data[k][i][25] == "Жен"):
                            errors[n] += "(Пол получателя) Неверно указан пол; "
                            ERROR_DICT['Неверно указан пол'] += 1
                        if (data[k][i][23][-1] == "а") & (data[k][i][25] == "Муж"):
                            errors[n] += "(Пол получателя) Неверно указан пол; "
                            ERROR_DICT['Неверно указан пол'] += 1
                else:
                    errors[n] += "(Пол получателя) Неверные данные; "
                    ERROR_DICT['Неверные данные'] += 1

                f_c_c = ['РФ', '', 'лица без гражданства', 'дальнее (других иностранных - кроме стран СНГ, Балтии, Грузии, Абхазии и Южной Осетии)', 'ближнее (из стран СНГ, Балтии, Грузии, Абхазии и Южной Осетии)', 'ближнее (из стран СНГ, Балтии, Грузии, Абхазии и Южной Осетии)']
                e_f = ['Очно-заочная (вечерняя)', '', 'Очная', 'Заочная']
                s_f = ['Целевое обучение', '', 'Платное обучение', 'Обучение за счет бюджетных ассигнований']
                h_e_r_f_t = ['Да', 'Нет', '']

                if data[k][i][26] not in f_c_c:
                	errors[n] += "(Гражданин иностранного государства) Неверное значение; "
                	ERROR_DICT['Неверные данные'] += 1
                if data[k][i][27] not in e_f:
                	errors[n] += "(Форма обучения) Неверное значение; "
                	ERROR_DICT['Неверные данные'] += 1
                if data[k][i][28] not in s_f:
                	errors[n] += "(Источник финансирования обучения) Неверное значение; "
                	ERROR_DICT['Неверные данные'] += 1
                if data[k][i][29] not in h_e_r_f_t:
                	errors[n] += "(Высшее образование, получаемое впервые) Неверное значение; "
                	ERROR_DICT['Неверные данные'] += 1

                for j in range(33):
                    if empty_cells[j] == False:
                        if data[k][i][j+1] == '':
                            errors[n] += "(" + str(data[0][0][j+1]) + ") Пустое значение; "
                            ERROR_DICT['Пустое значение'] += 1
                n += 1
        return (data, errors)

    def log(self, path_to_csv, path_to_directory, errors, data):
        name = datetime.datetime.now().strftime("%d-%m-%y--%H-%M-%S") + '.log'
        txt_patx = path_to_directory + '/' + name
        count = 0
        with open(txt_patx,'w') as out:
            out.write('Количество файлов: ' + str(len(path_to_csv)) + '\n')
            out.write('Всего записей: ' + str(len(errors)) + '\n')
            out.write('Количество ошибок: \n')
            for key,val in ERROR_DICT.items():
                out.write('    {}: {}\n'.format(key,val))
                count += val
            out.write('Всего ошибок: ' + str(count) + '\n')
            id_arr = []
            for i in range(len(data)):
                for j in range(1,len(data[i])):
                    id_arr.append(data[i][j][0])
            for k in range(len(errors)):
                if errors[k] != '':
                    out.write('id: (' + id_arr[k] + ')  Столбец: ' + str(errors[k]))
                    out.write('\n')

    def create_table(self, db, data):
        sql = 'CREATE TABLE Tcsv( \
                    [' + data[0][0] + '] VARCHAR(50), \
                    [' + data[0][1] + '] VARCHAR(50),\
                    [' + data[0][2] + '] VARCHAR(100),\
                    [' + data[0][3] + '] VARCHAR(100),\
                    [Номер субъекта РФ (из ОГРН)] VARCHAR(2),\
                    [' + data[0][4] + '] VARCHAR(100),\
                    [Признак филиала, либо головной организации] VARCHAR(2),\
                    [' + data[0][5] + '] VARCHAR(100),\
                    [' + data[0][6] + '] VARCHAR(50),\
                    [' + data[0][7] + '] VARCHAR(50),\
                    [' + data[0][8] + '] VARCHAR(50),\
                    [' + data[0][9] + '] VARCHAR(50),\
                    [' + data[0][10] + '] VARCHAR(50),\
                    [' + data[0][11] + '] VARCHAR(50),\
                    [' + data[0][12] + '] VARCHAR(50),\
                    [' + data[0][13] + '] VARCHAR(50),\
                    [' + data[0][14] + '] VARCHAR(150),\
                    [' + data[0][15] + '] VARCHAR(50),\
                    [' + data[0][16] + '] VARCHAR(50),\
                    [' + data[0][17] + '] VARCHAR(50),\
                    [' + data[0][18] + '] VARCHAR(50),\
                    [' + data[0][19] + '] VARCHAR(50),\
                    [' + data[0][20] + '] VARCHAR(100),\
                    [' + data[0][21] + '] VARCHAR(50),\
                    [' + data[0][22] + '] VARCHAR(50),\
                    [' + data[0][23] + '] VARCHAR(50),\
                    [' + data[0][24] + '] VARCHAR(50),\
                    [' + data[0][25] + '] VARCHAR(50),\
                    [' + data[0][26] + '] VARCHAR(50),\
                    [' + data[0][27] + '] VARCHAR(50),\
                    [' + data[0][28] + '] VARCHAR(50),\
                    [' + data[0][29] + '] VARCHAR(50),\
                    [' + data[0][30] + '] VARCHAR(50),\
                    [' + data[0][31] + '] VARCHAR(50),\
                    [' + data[0][32] + '] VARCHAR(50),\
                    [' + data[0][33] + '] VARCHAR(50),\
                    [' + data[0][34] + '] VARCHAR(50),\
                    [' + data[0][35] + '] VARCHAR(50),\
                    [' + data[0][36] + '] VARCHAR(50),\
                    [' + data[0][37] + '] VARCHAR(50),\
                    [Информация об ошибках] MEMO\
                    );'
        try:
            db.cursor().execute(sql)
            db.commit()
        except pypyodbc.ProgrammingError:
                print('Таблица Tcsv уже существует')


    def add_data(self, db, data, OGRN, KPP, num_sub_RF, priznak_organiz_from_KPP, objWindow, errors):
        filesCount = len(data)
        k = 0
        for j in range(len(data)):
            self.percent += 80/filesCount
            self.updated.emit(int(self.percent))
            for i in range(1, len(data[j])):
                db.cursor().execute("INSERT INTO Tcsv VALUES\
                               ('" + data[j][i][0] + "','" + data[j][i][1] + "','" + data[j][i][2] + "','" + OGRN[j] + "','" + num_sub_RF[j] + "','" + KPP[j] + "','" + priznak_organiz_from_KPP[j] + "','"\
                                   + data[j][i][5] + "','" + data[j][i][6] + "','" + data[j][i][7] + "','" + data[j][i][8] + "','" + data[j][i][9] + "','"\
                                   + data[j][i][10] + "','" + data[j][i][11] + "','" + data[j][i][12] + "','" + data[j][i][13] + "','" + data[j][i][14] + "','"\
                                   + data[j][i][15] + "','" + data[j][i][16] + "','" + data[j][i][17] + "','" + data[j][i][18] + "','" + data[j][i][19] + "','"\
                                   + data[j][i][20] + "','" + data[j][i][21] + "','" + data[j][i][22] + "','" + data[j][i][23] + "','" + data[j][i][24] + "','"\
                                   + data[j][i][25] + "','" + data[j][i][26] + "','" + data[j][i][27] + "','" + data[j][i][28] + "','" + data[j][i][29] + "','"\
                                   + data[j][i][30] + "','" + data[j][i][31] + "','" + data[j][i][32] + "','" + data[j][i][33] + "','" + data[j][i][34] + "','"\
                                   + data[j][i][35] + "','" + data[j][i][36] + "','" + data[j][i][37] + "','" + errors[k] + "');")
                k += 1
        self.updated.emit(int(100))
        db.commit()


ERROR_DICT = {'Неверные данные': 0,
              'Ожидалось число': 0,
              'Неверный срок обучения': 0,
              'Латинские буквы или цифры в строке': 0,
              'Ожидалась дата': 0,
              'Некорректная дата рождения': 0,
              'Недопустимая контрольная сумма ОГРН': 0,
              'Недопустимое количество символов ОГРН': 0,
              'Недопустимое количество символов КПП': 0,
              'Несоответствие виду документа об образовании': 0,
              'Пустое значение': 0,
              'Неверно указан пол': 0,
              'Неверный код специальности': 0,
              'Код специальности не совпадает с уровнем образования': 0}



def f1(user_rules_dict, empty_cells, files, objWindow):
    task = SlowTask()
    task.updated.connect(objWindow.on_update)
    return (task.run(user_rules_dict, empty_cells, files, objWindow))