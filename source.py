import win32com.client
import os 
import pyodbc
import csv
import glob
import re
import datetime
class DB:
    def __init__(self, path, cnxn = None, crsr = None):
        self.path = path  + '\\db.mdb'
        if (os.path.isfile(self.path)):
            pass
        else:
            oAccess = win32com.client.Dispatch('Access.Application')
            DbFile = self.path
            dbLangGeneral = ';LANGID=0x0419;CP=1252;COUNTRY=0'
            dbVersion = 64
            oAccess.DBEngine.CreateDatabase(DbFile, dbLangGeneral, dbVersion)
            oAccess.Quit()
            del oAccess
        conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=%s;'%(self.path)
        )
        self.cnxn = pyodbc.connect(conn_str)
        self.crsr = self.cnxn.cursor()

    def __del__ (self):
        self.cnxn.close()


    def create_table(self, name):
        sql = '''
        CREATE TABLE %s(
        id varchar(255),
        [Название документа] varchar(255),
        Организация  varchar(255),
        ОГРН  varchar(255),
        [Порядковый номер субъекта] varchar(255),
        КПП varchar(255),
        [Признак филиала, либо головной организации] varchar(255), 
        [Вид документа] varchar(255),
        [Статус документа] varchar(255),
        [Подтверждение утраты] varchar(255),
        [Подтверждение обмена] varchar(255),
        [Уровень образования] varchar(255),
        [Серия документа] varchar(255),
        [Номер документа] varchar(255),
        [Дата выдачи] varchar(255),
        [Регистрационный номер] varchar(255),
        [Код специальности, направления подготовки] varchar(255),
        [Наименование специальности, направления подготовки] varchar(255),
        [Наименование квалификации] varchar(255),
        [Образовательная программа] varchar(255),
        [Год поступления] varchar(255),
        [Год окончания] varchar(255), 
        [Срок обучения, лет] varchar(255),
        [Фамилия получателя] varchar(255),
        [Имя получателя] varchar(255),
        [Отчество получателя] varchar(255),
        [Дата рождения получателя] varchar(255),
        [Пол получателя] varchar(255),
        [Наименование документа об образовании (оригинала)] varchar(255),
        [Серия (оригинала)] varchar(255),
        [Номер (оригинала)] varchar(255),
        [Регистрационный N (оригинала)] varchar(255),
        [Дата выдачи (оригинала)] varchar(255),
        [Фамилия получателя (оригинала)] varchar(255),
        [Имя получателя (оригинала)] varchar(255),
        [Отчество получателя (оригинала)] varchar(255)
        )
        '''%(name)
        try:
            self.crsr.execute(sql)
            self.cnxn.commit()
        except pyodbc.ProgrammingError:
            print('Таблица %s уже существует'%(name))

    def insert(self, tb_name, orgvals, base, filename, log, rules_arr, empty_arr):
        def ogrn_check(ogrn):
            return  ((int(ogrn[:-1]) % 11 == int(ogrn[-1:]) or \
                    (int(ogrn[:-1]) % 11 == 10 and int(ogrn[-1:]) == 0)) and
                    (len(ogrn) == 13) )
        def name_check(name):
            return re.search('[a-zA-Z0-9]+', name) is not None
        def birthday_check(date, yearin):
            year = int(yearin) - int(date.split('.')[2])
            return ( year < 15 or year > 100)
        def sex_check(sex, patr):
            if patr != '':
                if (sex.lower() != 'муж' and sex.lower() != 'жен'):
                    return True
                elif ((patr[-1] == 'ч' and sex.lower() != 'муж') or (patr[-1] == 'а' and sex.lower() != 'жен')):
                    return True
                else:
                    return False
            else:
                return True
        def code_check(code, lvl):
            if (re.fullmatch(r'\d{2}\.\d{2}\.\d{2}', code)):
                return 0
            elif (re.fullmatch(r'\d{6}', code)):
                return 1
            elif (re.fullmatch(r'\d{2}\.\d{2}\.\d{4}', code)):
                return 2

            elif (len(code.replace('.', '')) != 6):
                return 4
            elif (code[3:5] == '01' and not re.search(r'[\w\s]*рабочих[\w\s]*', lvl)):
                return 5
            elif (code[3:5] == '02' and not re.search(r'[\w\s]*специалистов[\w\s]*', lvl)):
                return 6
            elif (code[3:5] == '03' and not re.search(r'[\w\s]*бакалавр[\w\s]*', lvl)):
                return 7
            elif (code[3:5] == '04' and not re.search(r'[\w\s]*магистр[\w\s]*', lvl)):
                return 8
            elif (code[3:5] == '05' and not re.search(r'[\w\s]*специал[\w\s]*', lvl)):
                return 9
            else:
                return -1

        str_ind = [1, 2, 7, 8, 9, 10, 11, 17, 18, 19, 27]
        int_ind = [0, 3, 4, 5, 6, 20, 21]
        date_ind = [14, 26]
        base = base.split('-')
        ogrn = base[0]
        kpp = base[1]
        for vals in orgvals:
            vals = list(dict(vals).values())
            if (not(vals[3] == '' and empty_arr[3])):
                try:
                    if (ogrn_check(ogrn)):
                        vals[3] = ogrn
                        vals.insert(4, ogrn[3:5])
                    elif len(ogrn) != 13:
                        vals[3] = f'Ошибка: неверное количество символов ({vals[3]})'
                        vals.insert(4, 'Ошибка: неверный ОГРН')
                        log.addErr(filename, vals[0], 4, vals[3])
                        log.addErr(filename, vals[0], 5, 'Ошибка: неверный ОГРН')
                    else:
                        vals[3] = f'Ошибка: неверное контрольное число ({vals[3]})' 
                        vals.insert(4, 'Ошибка: неверный ОГРН')
                        log.addErr(filename, vals[0], 4, vals[3])
                        log.addErr(filename, vals[0], 5, 'Ошибка: неверный ОГРН')
                except ValueError:
                    vals[3] = f'Ошибка: неверный тип ОГРН ({vals[3]})'
                    vals.insert(4, 'Ошибка: неверный ОГРН')
                    log.addErr(filename, 4, vals[0], vals[3])
                    log.addErr(filename, 5, vals[0], 'Ошибка: неверный ОГРН')
            if (not(vals[5] == '' and empty_arr[5])):
                try:
                    int(kpp)
                    if len(kpp) == 9:
                        vals[5] = kpp
                        vals.insert(6, kpp[4:6])
                    else:
                        vals[5] = f'Ошибка: неверная длина КПП ({vals[5]})'
                        vals.insert(6, 'Ошибка: неверный КПП')
                        log.addErr(filename, vals[0], 6, vals[5])
                        log.addErr(filename, vals[0], 7, 'Ошибка: неверный КПП')
                except ValueError:
                    vals[5] = f'Ошибка: неверный тип КПП ({vals[5]})'
                    vals.insert(6, 'Ошибка: неверный КПП')
                    log.addErr(filename, 6, vals[0], vals[5])
                    log.addErr(filename, 7, vals[0], 'Ошибка: неверный КПП')

            for i in (str_ind):
                if (vals[i].isdigit()):
                    vals[i] = f'Ошибка: текстовое поле содержит число ({vals[i]})'
                    log.addErr(filename, vals[0], i+1, vals[i])

            for i in (int_ind):
                if (not vals[i].isdigit() and vals[i] != ''):
                    vals[i] = f'Ошибка: числовое поле содержит текст ({vals[i]})'
                    log.addErr(filename, vals[0], i+1, vals[i])
            if (not(vals[11] == '' and empty_arr[11])):
                if (rules_arr[0]):
                    if (re.search(r'[\w\s]*сред[\w\s]*проф[\w\s]*', vals[7].lower()) and not re.search(r'[\w\s]*сред[\w\s]*проф[\w\s]*', vals[11].lower())):
                        vals[11] = f"Ошибка: несоответсвие с полем \"Вид документа\" ({vals[11]})"
                        log.addErr(filename, vals[0], 12, vals[11])
                    elif (re.search(r'[\w\s]*высш[\w\s]*проф[\w\s]*', vals[7]) and not re.search(r'[\w\s]*высш[\w\s]*проф[\w\s]*', vals[11])):
                        vals[11] = f"Ошибка: несоответсвие с полем \"Вид документа\" ({vals[11]})"
                        log.addErr(filename, vals[0], 12, vals[11])
            if (not(vals[16] == '' and empty_arr[16])):
                if (rules_arr[1]):
                    c_check = code_check(vals[16], vals[11])
                    if (c_check == 1):
                        vals[16] = 'Ошибка: неверное значение({0}), возможно имелось ввиду {1}'.format(vals[16], vals[16][0:2] + '.' + vals[16][2:4] + '.' + vals[16][4:6])
                        log.addErr(filename, vals[0], 17, vals[16])
                    elif (c_check == 2):
                        vals[16] = 'Ошибка: неверное значение({0}), возможно имелось ввиду {1}'.format(vals[16], vals[16][0:3] + vals[16][3:6] + vals[16][8:10])
                        log.addErr(filename, vals[0], 17, vals[16])
                    elif (c_check == 4):
                        vals[16] = f'Ошибка: неверная длина строки ({vals[16]})'
                        log.addErr(filename, vals[0], 17, vals[16])
                    elif c_check in [5, 6, 7, 8, 9]:
                        vals[16] = f'Ошибка: код специальности не совпадает с уровнем образования ({vals[16]})'
                        log.addErr(filename, vals[0], 17, vals[16])
                    elif (c_check == -1):
                        vals[16] = f'Ошибка: неверный тип поля ({vals[16]})'
                        log.addErr(filename, vals[0], 17, vals[16])



            for i in range(23, 26):
                try:
                    if (name_check(vals[i])):
                        vals[i] = f'Ошибка: поле содержит символы латинского алфавита или цифры ({vals[i]})'
                        log.addErr(filename, vals[0], i+1, vals[i])
                except TypeError:
                    vals[i] = f'Ошибка: неверный тип поля ({vals[i]})'
                    log.addErr(filename, vals[0], i+1, vals[i])
            for i in range(33, 36):
                try:
                    if (name_check(vals[i])):
                        vals[i] = f'Ошибка: поле содержит символы латинского алфавита или цифры ({vals[i]})'
                        log.addErr(filename, vals[0], i+1, vals[i])
                except TypeError:
                    vals[i] = f'Ошибка: неверный тип поля ({vals[i]})'
                    log.addErr(filename, vals[0], i+1, vals[i])

            for i in (date_ind):
                if (not(vals[i] == '' and empty_arr[i])):
                    try:
                        datetime.datetime.strptime(vals[i], '%d.%m.%Y')
                        if i == 26:
                            try:
                                if (birthday_check(vals[26], vals[20])):
                                    vals[26] = f'Ошибка: неверный возраст ({vals[26]})'
                                    log.addErr(filename, vals[0], 27, vals[26])
                            except IndexError:
                                vals[26] = f'Ошибка: неверный тип поля ({vals[26]})'
                                log.addErr(filename, vals[0], 27, vals[26])
                    except ValueError:
                        vals[i] = f'Ошибка: неверная дата ({vals[i]})'
                        log.addErr(filename, vals[0], i+1, vals[i])
            if (not(vals[27] == '' and empty_arr[27])):
                if(sex_check(vals[27], vals[25])):
                    vals[27] = f'Ошибка: неверный пол ({vals[27]})'
                    log.addErr(filename, vals[0], 28, vals[27])

            for i in range(len(empty_arr)):
                if (not empty_arr[i] and vals[i] == ''):
                    vals[i] = 'Ошибка: пустое поле'
                    log.addErr(filename, vals[0], i+1, vals[i])

            sql = f'''
                INSERT INTO {tb_name} 
                VALUES (?, ?, ? , ?, ? , ?,
                        ?, ?, ? , ? , ?, ?,
                        ?, ?, ? , ? , ?,
                        ?, ?, ? , ? , ?,
                        ?, ?, ? , ? , ?,
                        ?, ?, ? , ? , ?,
                        ?, ?, ? , ?)
                '''
            self.crsr.execute(sql,  (vals[0], vals[1], vals[2], vals[3], vals[4],
                                    vals[5], vals[6], vals[7], vals[8], vals[9],
                                    vals[10], vals[11], vals[12], vals[13], vals[14],
                                    vals[15], vals[16], vals[17], vals[18], vals[19],
                                    vals[20], vals[21], vals[22], vals[23], vals[24],
                                    vals[25], vals[26], vals[27], vals[28], vals[29],
                                    vals[30], vals[31], vals[32], vals[33], vals[34], vals[35]))
            '''
        id 0
        [Название документа] 1
        Организация 2
        ОГРН    3
        [Порядковый номер субъекта] 4
        КПП 5
        [Признак филиала, либо головной организации] 6
        [Вид документа] 7
        [Статус документа] 8
        [Подтверждение утраты] 9
        [Подтверждение обмена] 10  
        [Уровень образования] 11 
        [Серия документа]   12
        [Номер документа]   13
        [Дата выдачи]   14
        [Регистрационный номер]     15
        [Код специальности, направления подготовки]     16
        [Наименование специальности, направления подготовки] 17
        [Наименование квалификации] 18
        [Образовательная программа] 19
        [Год поступления] 20
        [Год окончания] 21
        [Срок обучения, лет] 22
        [Фамилия получателя] 23
        [Имя получателя] 24
        [Отчество получателя] 25
        [Дата рождения получателя] 26
        [Пол получателя] 27
        [Наименование документа об образовании (оригинала)] 28
        [Серия (оригинала)] 29
        [Номер (оригинала)] 30
        [Регистрационный N (оригинала)] 31
        [Дата выдачи (оригинала)] 32
        [Фамилия получателя (оригинала)] 33
        [Имя получателя (оригинала)] 34
        [Отчество получателя (оригинала)] 35
        str_ind = [1, 2, 7, 8, 9, 10, 11, 17, 18, 19, 23, 24, 25, 27]
        int_ind = [0, 3, 4, 5, 6, 12, 13, 15, 20, 21, 22]
        date_ind = [14, 26]

            '''
        self.cnxn.commit()

class Log:
    def __init__(self):
        self.fileCount = 0
        self.rows = []
        self.files = []
        self.errors = []

    def __del__(self):
        del self.fileCount
        del self.rows
        del self.files
        del self.errors

    def addFile(self, filename):
        self.fileCount += 1
        self.files.append(filename)
    def addRec(self, filename, rowCount):
        self.rows.append((filename, rowCount))
    def addErr(self, filename, rID, index, err):
        self.errors.append((filename, rID, index, err))
    def getFiles(self):
        return(self.files, self.fileCount)
    def getRecs(self):
        return(self.rows)
    def getErr(self):
        return(self.errors)
    def createLog(self, name = None):
        name = datetime.datetime.now().strftime("%d-%m-%y--%H-%M-%S") + '.log'
        with open(name, 'w') as file:
            file.write (f'Добавленные файлы ({self.fileCount}):\n')
            for i in range(len(self.files)):
                file.write(self.files[i] + f' = {self.rows[i][1]} записей\n')
            file.write (f'------------------------------------------\nОшибки ({len(self.errors)})\n')
            for i in self.errors:
                file.write(f'Имя файла: {i[0]}\nID: {i[1]}\nЯчейка: {i[2]}\n{i[3]}\n')



def fileCheck(filename):
    with open(filename, 'r') as file:
        data = file.readlines()

    i = 1
    while (i < len(data) - 1):
        if (data[i+1][0].isdigit()):
            i+=1
        else:
            data[i] = data[i][:-1] + ''
            data[i] = data[i] + data[i+1]
            data.pop(i+1)
        

    for i in range(len(data)):
        if (data[i].count(';') < 33):
            data[i] = data[i][:-1] + ';'*(33 - data[i].count(';')) + data[i][-1:]
        elif (data[i].count(';') > 33):
            data[i] = data[i][:(32-data[i].count(';'))] + data[i][-1:]
    with open(filename, 'w') as file:
        file.writelines(data)





def main(rules_arr, empty_arr, files, obj):
    progBar = obj.progressBar
    test = DB(os.getcwd())
    test.create_table('Tcsv')
    log = Log()
    m_empty_arr = empty_arr.copy()
    m_empty_arr.insert(0, False)
    m_empty_arr.insert(4, False)
    m_empty_arr.insert(6, False)
    filesCount = len(files)
    completed = 0
    for filename in files:
        try:
            completed += 1/filesCount * 100
            progBar.setValue(completed)
            a = []
            fileCheck(filename)
            log.addFile(filename)
            with open(filename, "r", newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                rowCount = 0
                for line in reader:            
                    a.append(line)
                    rowCount += 1
                log.addRec(filename, rowCount)
                base = os.path.splitext(os.path.basename(filename))[0]
                test.insert('Tcsv', a, base, filename, log, rules_arr, m_empty_arr)
        except:
            obj.error_file(filename)
            continue
            

    progBar.setValue(100)
    log.createLog()
    del log
    return 1