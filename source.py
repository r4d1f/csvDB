import pypyodbc
import os
import csv
import re
import win32com.client
import datetime
import traceback

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

#user_rules_dict = {'Проверять соответствие уровня образования виду документа об образовании': 0,
#                  'Проверять код специальности': 0}

#empty_cells = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, \
#               '15': 0, '16': 0, '17': 0, '18': 0, '19': 0,'20': 0, '21': 0, '22': 0, '23': 0, '24': 0, '25': 0, '26': 0, '27': 0, '28': 0, '29': 0, \
#               '30': 0, '31': 0, '32': 0, '33': 0}


def create_db():
    db_path = os.getcwd() + '/DB.mdb'
    if (not os.path.exists(db_path)):
        pypyodbc.win_create_mdb(db_path)    
    db = pypyodbc.win_connect_mdb(db_path) 
    return db

def get_files_and_OGRN_KPP_from_name(files):
    csv_files_in_directory = []
    for f in files:
        csv_files_in_directory.append(re.search(r'\d+-\d+[\s\S]*\.csv', f)[0])
    OGRN = []
    KPP = []
    for i in range(len(files)):
        OGRN.append(csv_files_in_directory[i][0:13])
        KPP.append(csv_files_in_directory[i][14:23])
    return (OGRN, KPP)

def get_data_from_csv_and_check_num_delimiters(path_to_csv):
    data = []
    for i in range(len(path_to_csv)):
        with open(path_to_csv[i], newline='') as csvfile:
            data.append(list(csv.reader(csvfile, delimiter=';')))
            for j in range(1, len(data[i])):
                if (len(data[i][j]) < 34):
                    if re.search(r'\d\d\d\d\d\d\d\d',data[i][0]):
                        while (len(data[i][j]) < 34):
                            data[i][j].append('')
                    else:
                        while (len(data[i][j]) < 34):
                            data[i][j].insert(0,'') 
                if (len(data[i][j]) > 34):
                     data[i][j] = data[i][j][0:-(len(data[i][j]) - 34)]
    return data
           
def check_data_logic(user_rules_dict, empty_cells, data):
    for k in range(len(data)):
        for i in range(1,len(data[k])):
            try:
                int(data[k][i][0])
            except:
                data[k][i][0] =  "Ошибка! Ожидалось число; " + data[k][i][0] 
                ERROR_DICT['Ожидалось число'] += 1
            try:
                int(data[k][i][10])
            except:
                data[k][i][10] = "Ошибка! Ожидалось число; " + data[k][i][10]
                ERROR_DICT['Ожидалось число'] += 1
            try:
                int(data[k][i][11])
            except:
                data[k][i][11] = "Ошибка! Ожидалось число; " + data[k][i][11]
                ERROR_DICT['Ожидалось число'] += 1
            try:
                int(data[k][i][13])
            except:
                data[k][i][13] = "Ошибка! Ожидалось число; " + data[k][i][13]
                ERROR_DICT['Ожидалось число'] += 1
            try:
                int(data[k][i][18])
            except:
                data[k][i][18] = "Ошибка! Ожидалось число; " + data[k][i][18]
                ERROR_DICT['Ожидалось число'] += 1
            try:
                int(data[k][i][19])
            except:
                data[k][i][19] = "Ошибка! Ожидалось число; " + data[k][i][19]
                ERROR_DICT['Ожидалось число'] += 1
                int(data[k][i][20])
            try:
                if data[k][i][29] != '':
                    int(data[k][i][28])
            except:
                data[k][i][28] = "Ошибка! Ожидалось число; " + data[k][i][28]
                ERROR_DICT['Ожидалось число'] += 1
            try:
                if data[k][i][29] != '':
                    int(data[k][i][29])
            except:
                data[k][i][29] = "Ошибка! Ожидалось число; " + data[k][i][29]
                ERROR_DICT['Ожидалось число'] += 1

            if (re.search(r'Ошибка!', data[k][i][20]) == None) & (re.search(r'Ошибка!', data[k][i][19]) == None) & (re.search(r'Ошибка!', data[k][i][18]) == None):
                if int(data[k][i][20]) != int(data[k][i][19]) - int(data[k][i][18]):
                        data[k][i][20] = "Ошибка! Неверный срок обучения; " + data[k][i][20]
                        ERROR_DICT['Неверный срок обучения'] += 1
            else:
                data[k][i][20] = data[k][i][20] + " Предупреждение! Невозможно проверить срок обучения."

            if re.search(r'[a-zA-Z0-9]', data[k][i][21]):
                data[k][i][21] = "Ошибка! Латинские буквы или цифры в строке; " + data[k][i][21]
                ERROR_DICT['Латинские буквы или цифры в строке'] += 1
            if re.search(r'[a-zA-Z0-9]', data[k][i][22]):
                data[k][i][22] = "Ошибка! Латинские буквы или цифры в строке; " + data[k][i][22]
                ERROR_DICT['Латинские буквы или цифры в строке'] += 1
            if re.search(r'[a-zA-Z0-9]', data[k][i][23]):
                data[k][i][23] = "Ошибка! Латинские буквы или цифры в строке; " + data[k][i][23]
                ERROR_DICT['Латинские буквы или цифры в строке'] += 1
            if re.search(r'[a-zA-Z0-9]', data[k][i][31]):
                data[k][i][31] = "Ошибка! Латинские буквы или цифры в строке; " + data[k][i][31]
                ERROR_DICT['Латинские буквы или цифры в строке'] += 1
            if re.search(r'[a-zA-Z0-9]', data[k][i][32]):
                data[k][i][32] = "Ошибка! Латинские буквы или цифры в строке; " + data[k][i][32]
                ERROR_DICT['Латинские буквы или цифры в строке'] += 1
            if re.search(r'[a-zA-Z0-9]', data[k][i][33]):
                data[k][i][33] = "Ошибка! Латинские буквы или цифры в строке; " + data[k][i][33]
                ERROR_DICT['Латинские буквы или цифры в строке'] += 1

            if re.search(r'\d\d.\d\d.\d\d\d\d', data[k][i][12]) == None:
                data[k][i][12] = "Ошибка! Ожидалась дата; " + data[k][i][12]
                ERROR_DICT['Ожидалась дата'] += 1
            if re.search(r'\d\d.\d\d.\d\d\d\d', data[k][i][24]) == None:
                data[k][i][24] = "Ошибка! Ожидалась дата; " + data[k][i][24]
                ERROR_DICT['Ожидалась дата'] += 1
            else:
                if len(data[k][i][18]) == 4:
                    if (int(data[k][i][18]) - int(data[k][i][24][6:10])) < 15:
                       data[k][i][24] = "Ошибка! Некорректная дата рождения; " + data[k][i][24]
                       ERROR_DICT['Некорректная дата рождения'] += 1
            if data[k][i][30] != '':
                if re.search(r'\d\d.\d\d.\d\d\d\d', data[k][i][30]) == None: 
                    data[k][i][30] = "Ошибка! Ожидалась дата; " + data[k][i][30]
                    ERROR_DICT['Ожидалась дата'] += 1

            if user_rules_dict[1] == True:
                if re.search(r'\d\d.\d\d.\d\d$', data[k][i][14]) == None:
                    if re.search(r'\d\d.\d\d.\d\d\d\d', data[k][i][14]): 
                        data[k][i][14] = "Ошибка! Неверный код специальности; " + data[k][i][14] + "; Возможно имелось в виду: " + data[k][i][14][0:6] + data[k][i][14][8:len(data[k][i][14])]
                        ERROR_DICT['Неверный код специальности'] += 1
                    elif re.search(r'\d\d\d\d\d\d', data[k][i][14]):
                        data[k][i][14] = "Ошибка! Неверный код специальности; " + data[k][i][14] + "; Возможно имелось в виду: " + data[k][i][14][0:2] + '.'\
                                                                                + data[k][i][14][2:4] + '.' + data[k][i][14][4:6]
                        ERROR_DICT['Неверный код специальности'] += 1
                    else:
                        data[k][i][14] = "Ошибка! Неверный код специальности; " + data[k][i][14]
                        ERROR_DICT['Неверный код специальности'] += 1
                else:
                    if re.search(r'специалистов', data[k][i][9]):
                        if data[k][i][14][3:5] != '02':
                            data[k][i][14] = "Ошибка! Код специальности не совпадает с уровнем образования; " + data[k][i][14]
                            ERROR_DICT['Код специальности не совпадает с уровнем образования'] += 1
                    if re.search(r'рабочих', data[k][i][9]):
                        if data[k][i][14][3:5] != '01':
                            data[k][i][14] = "Ошибка! Код специальности не совпадает с уровнем образования; " + data[k][i][14]
                            ERROR_DICT['Код специальности не совпадает с уровнем образования'] += 1

            if user_rules_dict[0] == True:
                if (re.search(r'средн[а-я ]+проф', data[k][i][5])):
                    if re.search(r'Средн[а-я ]+проф', data[k][i][9]) == None:
                        data[k][i][9] = "Ошибка! Несоответствие виду документа об образовании; " + data[k][i][9]
                        ERROR_DICT['Несоответствие виду документа об образовании'] += 1

                if (re.search(r'высш[а-я ]+проф', data[k][i][5])):
                    if re.search(r'[Вв]ысш[а-я ]+проф', data[k][i][9]) == None:
                        data[k][i][9] = "Ошибка! Несоответствие виду документа об образовании; " + data[k][i][9]
                        ERROR_DICT['Несоответствие виду документа об образовании'] += 1

            if (data[k][i][25] == "Муж") | (data[k][i][25] == "Жен"):
                if data[k][i][23] != '':
                    if (re.search(r'[А-Яа-я]+ич', data[k][i][23]) != None) & (data[k][i][25] == "Жен"):
                        data[k][i][25] = "Ошибка! Неверно указан пол; " + data[k][i][25]
                        ERROR_DICT['Неверно указан пол'] += 1
                    if (re.search(r'[А-Яа-я]+на', data[k][i][23]) != None) & (data[k][i][25] == "Муж"):
                        data[k][i][25] = "Ошибка! Неверно указан пол; " + data[k][i][25]
                        ERROR_DICT['Неверно указан пол'] += 1
            else:
                data[k][i][25] = "Ошибка! Неверные данные; " + data[k][i][25]
                ERROR_DICT['Неверные данные'] += 1

            for j in range(33):
                if empty_cells[j] == False:
                    if data[k][i][j+1] == '':
                        data[k][i][j+1] = "Ошибка! Пустое значение;"
                        ERROR_DICT['Пустое значение'] += 1
    return data

def check_OGRN_KPP_get_num_sub_RF(OGRN, KPP):
    num_sub_RF = []
    priznak_organiz_from_KPP = []
    flag = 0
    for i in range(len(OGRN)):
        if len(OGRN[i]) == 13:
            tmp = int(OGRN[i][0:-1])
            if tmp % 11 <= 9:
                tmp_2 = tmp % 11
            else:
                tmp_2 = (tmp % 11) % 10
            if tmp_2 != int(OGRN[i][12]):
                OGRN[i] = "Ошибка! Недопустимая контрольная сумма ОГРН " + OGRN[i]
                ERROR_DICT['Недопустимая контрольная сумма ОГРН'] += 1
                flag = 1
            if flag == 0:
                num_sub_RF.append(OGRN[i][3:5])
            else:
                num_sub_RF.append("Ошибка в ОГРН")
        else:
            OGRN[i] = "Ошибка! Недопустимое количество символов ОГРН: " + len(OGRN[i]) + ", Нужно 13; " + OGRN[i]
            ERROR_DICT['Недопустимое количество символов ОГРН'] += 1
            num_sub_RF.append("Ошибка в ОГРН")
        OGRN[i] = OGRN[i]
        if len(KPP[i]) != 9:
            KPP[i] = "Ошибка! Недопустимое количество символов КПП: " + len(KPP[i]) + ", Нужно 9; " + KPP[i]
            ERROR_DICT['Недопустимое количество символов КПП'] += 1
        KPP[i] = KPP[i] 
        priznak_organiz_from_KPP.append(KPP[i][4:6])
    return (OGRN, KPP, num_sub_RF, priznak_organiz_from_KPP)

def log(path_to_csv, path_to_directory, data):
    txt_patx = path_to_directory + '/log.log'
    if os.path.exists(txt_patx):
       os.remove(txt_patx)
    count = 0
    num_rec = 0
    for i in range(len(data)):
        num_rec += len(data[i])
    num_rec -= len(data)
    n = 0
    with open(txt_patx,'w') as out:
        out.write('Количество файлов: ' + str(len(path_to_csv)) + '\n')
        out.write('Всего записей: ' + str(num_rec) + '\n')
        out.write('Количество ошибок: \n')
        for key,val in ERROR_DICT.items():
            out.write('    {}: {}\n'.format(key,val))
            count += val
        out.write('Всего ошибок: ' + str(count) + '\n')
        for k in range(len(data)):
            for i in range(1, len(data[k])):
                n += 1
                for j in range(len(data[k][i])):
                    if re.search(r'Ошибка!', data[k][i][j]):
                        if j < 5:
                            out.write('Ячейка с id: ' + str(data[k][i][0]) + ', столбец: ' + str(j+1) + ' содержит ошибку: ' + str(re.search(' [А-Яа-я ]+;', data[k][i][j])[0]) + '\n')
                        else:
                            out.write('Ячейка с id: ' + str(data[k][i][0]) + ', столбец: ' + str(j+3) + ' содержит ошибку: ' + str(re.search(' [А-Яа-я ]+;', data[k][i][j])[0]) + '\n')
   
def create_table(db, data):
    sql = 'CREATE TABLE t1( \
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
                [' + data[0][33] + '] VARCHAR(50)\
                );'
    try:
        db.cursor().execute(sql)
        db.commit()
    except pypyodbc.ProgrammingError:
            print('Таблица t1 уже существует')


def add_data(db, data, OGRN, KPP, num_sub_RF, priznak_organiz_from_KPP, objWindow):
    progBar = objWindow.progressBar
    filesCount = len(data)
    completed = 0
    for j in range(len(data)):
        completed += 100/filesCount
        progBar.setValue(completed)
        for i in range(1, len(data[j])):
            db.cursor().execute("INSERT INTO t1 VALUES\
                           ('" + data[j][i][0] + "','" + data[j][i][1] + "','" + data[j][i][2] + "','" + OGRN[j] + "','" + num_sub_RF[j] + "','" + KPP[j] + "','" + priznak_organiz_from_KPP[j] + "','"\
                               + data[j][i][5] + "','" + data[j][i][6] + "','" + data[j][i][7] + "','" + data[j][i][8] + "','" + data[j][i][9] + "','"\
                               + data[j][i][10] + "','" + data[j][i][11] + "','" + data[j][i][12] + "','" + data[j][i][13] + "','" + data[j][i][14] + "','"\
                               + data[j][i][15] + "','" + data[j][i][16] + "','" + data[j][i][17] + "','" + data[j][i][18] + "','" + data[j][i][19] + "','"\
                               + data[j][i][20] + "','" + data[j][i][21] + "','" + data[j][i][22] + "','" + data[j][i][23] + "','" + data[j][i][24] + "','"\
                               + data[j][i][25] + "','" + data[j][i][26] + "','" + data[j][i][27] + "','" + data[j][i][28] + "','" + data[j][i][29] + "','"\
                               + data[j][i][30] + "','" + data[j][i][31] + "','" + data[j][i][32] + "','" + data[j][i][33] + "');")
    db.commit()
    db.close()
    progBar.setValue(100)

def f(user_rules_dict, empty_cells, files, objWindow):
    print("Start time: " + str(datetime.datetime.now()))
    try:
        db = create_db()
        OGRN, KPP = get_files_and_OGRN_KPP_from_name(files)
        data = get_data_from_csv_and_check_num_delimiters(files)
        print("Обработка csv: " + str(datetime.datetime.now()))
        data = check_data_logic(user_rules_dict, empty_cells, data)
        OGRN, KPP, num_sub_RF, priznak_organiz_from_KPP = check_OGRN_KPP_get_num_sub_RF(OGRN, KPP)
        log(files, os.getcwd(), data)
        create_table(db, data[0])
        print("Добавленние в бд: " + str(datetime.datetime.now()))
        add_data(db, data, OGRN, KPP, num_sub_RF, priznak_organiz_from_KPP, objWindow)
        global ERROR_DICT
        ERROR_DICT = ERROR_DICT.fromkeys(ERROR_DICT, 0)
        print("Done! End time: " + str(datetime.datetime.now()) + "\n")
        return 1
    except:
        print("Error! End time: " + str(datetime.datetime.now()) + "\n")
        print('Ошибка:\n', traceback.format_exc())
        return 0