# -*- coding: UTF-8 -*-
#Импорт билблиотек
from sqllex import *
from termcolor import colored
import os
import sys
import time
import random
import string
import re
import pyAesCrypt

#Анонимная функция для очистки терминала 
clear = lambda: os.system('cls')

#Функция досрочного завершения программы, что шифрует БД (Не реализованно)
def bye(name, password):
    print(colored("Программа завершена.", 'green'))
    encrypt_file(name, password)
    time.sleep(1)

#Функция генерации безопасного пароля
def generate_random_password(length):
    letters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', #Список цифр и спец символов
    '<', '>', '$', '/', '"', '_', '+', '=']
    lists = string.ascii_letters #Создание строки, содержащей буквы латинского алфовита в обоих регистрах
    letters = list(lists) + 3 * letters #Первод полученной строки букв и трех одинаковых массивов спец символов, для усложнения пароля
    password = ''.join(random.choice(letters) for i in range(length)) #Цикл, случайно выбирающий символы из массива и записывающий их в строку
    return password #Функция возвращает пароль

#Функция шифрования БД, принимает название БД и пароль
def encrypt_file(file, passowrd):
    file = file + ".db" #Название БД
    buffer = 512 * 1024 #Назначение размера буфера для последующего шифрования
    pyAesCrypt.encryptFile( #Метод шифрования
        str(file), #Старое название файла
        str(file) + '.crp', #Старое название файла с расширением ".crp"
        passowrd, #Пароль для шифрования
        buffer #Буфер
    )
    os.remove(file) #Удаляеться не зашифрованная версия файла

#Функция для дешифрования БД
def decrypt_file(file, passowrd): 
    file = file + ".db.crp" #Название зашифровоного файла
    buffer = 512 * 1024 #Назначение размера буфера для последующего дешифрования
    pyAesCrypt.decryptFile( #Метод дешифрования
        str(file), #Название зашифрового файла
        str(os.path.splitext(file)[0]), #Название дешифровоного файла, убираеться расширение ".crp" из названия файла
        passowrd, #Пароль для дешифрования
        buffer #Буфер
    )
    os.remove(file) #Удаляеться зашифрованная версия файла

#Функция анимации загрузки программы
def qute_animation():
    hello = list(("Приветствую, ")) #Массив символов
    name_system_user = list(os.getlogin()) #Массив символов имени пользователя, выполняющего программу
    string_start = "" #Пустая строка
    for i in range (len(hello)): #Цикл, постепенно заполняющий строку
        string_start = str(string_start + hello[i])
        print(colored(string_start, "yellow"))
        time.sleep(0.1) #Время между кадрами анимации
        clear() #Очистка терминала для следующего кадра анимации
    for i in range (len(name_system_user)): #Цикл, постепенно заполняющий строку
        string_start = string_start + name_system_user[i] 
        print(colored(string_start, "yellow")) 
        if i == len(name_system_user) - 1: #Если вывод закончился, строка будет на экране ще 30млс
            time.sleep(0.5)
            clear() #Очистка терминала
        time.sleep(0.1) #Время между кадрами анимации
        clear() #Очистка терминала для следующего кадра анимации

def start_program():
    if os.path.exists('DataBases\\') == False: #Првоерка наличия директории "DataBases", если такой нет, то создает
        os.mkdir('DataBases') #Создание новой директории "DataBases"
    animation = ['\\', '|', '/', '-', '\\', '|', '/', '-', '\\', '|', '/', '-', '\\', '|', '/', '-'] #Фрагменты анимации загрузки
    qute_animation()
    for i in range(14): #Цикл анимации
        print(colored('UTOPIA PROJECT', 'green')) #Название программы
        print('Загрузка...',animation[i]) #Строчка с анимации
        time.sleep(0.1) #Время между кадрами анимации
        clear() #Очистка терминала для следующего кадра анимации

#Функция создания БД
def create_database():
    print(colored("Создание базы данных", "yellow"), colored("\nОтмена - !", "magenta"))
    name = input(colored("Введите название вашией базыданных: ", 'cyan'))
    if name == "!":
        return
    print(colored('ВНИМАНИЕ', 'red'), 'ДЛЯ ПОЛУЧЕНИЯ ЛУЧШЕЙ БЕЗПАСНОСТИ - ', colored('\nНЕ ХРАНИТЕ ПАРОЛЬ НА КОМПЬТЕРЕ.', 'red'))
    print(colored('Для получения лучшей безопасности, храните пароль \nна внешнем носителе или на листке бумаги.', 'yellow'))
    password = input(colored("Введите пароль для вашей базы данных: ", 'cyan'))
    db = SQLite3x(name + ".db") #Путь к файлу
    db.create_table( #Создание таблицы в БД
        'passwords',
        {
            'name': [TEXT, PRIMARY_KEY, UNIQUE], #Название пароля
            'password': [TEXT, UNIQUE] #Пароль
        }
    )
    encrypt_file(name, password)
    return db #Функция возвращает переменную, содержащую базу данных

#Функция использования базы данных
def use_database(name, password):
    try:
        decrypt_file(name, password)
        while True:  # Цикл, продолжающийся до тех пор, пока не прерветься
            path_to_db = name + ".db"  # Путь к файлу
            clear()  # Очищение терминала
            if os.path.isfile(path_to_db) == True:  # Проверка наличия такого файла
                return path_to_db  # Возвращает путь к файлу
            else:
                # Если такой фаул отсутсвует, вам предлагаеться следующий выбор
                print(colored('Такая БД отсутвтвует, создать?', 'yellow'), '\n 1 - Да \n 2 - Нет')
                anserwe = input(colored(colored('\n Введите команду: ', 'cyan')))
                if anserwe == '1':
                    clear()
                    create_database()  # Функция создания БД
                    break
                elif anserwe == '2':
                    clear()
                    break  # Цикл останавливается
                elif anserwe == "!":
                    clear()
                    break  # Цикл останавливается
                else:
                    print(colored('Неверная команда.', 'red'))  # Введена неверная команда
                    time.sleep(1)
                    clear()
                    continue  # Цикл продолжается
    #Исключение, работающие при введении неаерного имени БД или\и пароля
    except BaseException:
        clear() #Очищение терминала
        print(colored('Неверное имя БД или пароль БД, или такая БД не существует', 'red'))
        input(colored('\n Нажмите любую клавишу, чтобы продолжить...', 'green'))


#Функция добавления новой записи в БД
def add_new(data_base):
    new_in_db = data_base['passwords'] #Запись в переменную таблицы из БД
    print(colored("Добавление новой записи", "yellow"), colored("\nОтмена - !", "magenta"))
    new_name = input(colored("Введите название для пароля: ", 'cyan'))
    new_name = re.sub(r"^\s+|\s+$", "", new_name) #Исключение из конца названия пробел
    if new_name != "!":
        length_password = int(input(colored("Пароль будет создан случайно, введите длинну пароля: ", 'cyan')))
        new_password = generate_random_password(length_password)  # Генерация пароля из указанной длинны
        # Проверка на наличие записи, при помощи исключений
        try:
            new_in_db.insert(name=new_name, password=new_password)  # В таблицу вносяться новые записи
        except BaseException:
            print(colored('Запись с таким именем уже есть.', 'red'))
    elif new_name == "!":
        return

#Функция взаимодействия с БД
def text_of_func():
    print(colored('Вы можете выполнить следующие действия: ', 'yellow'), '\n 1 - Создать новую запись \n 2 - Получить запись \n 3 - Получить все записи \n 4 - Удалить запись \n 5 - Сохранить и Закрыть')
    command = input(colored('Введите команду: ', 'cyan'))
    return command

def all_in_db(db):
    print(colored("Все названия паролей", "yellow"))
    users_group_1 = db.select(  # Запрос на выборку пароля по его названию
        'passwords',
        'name'
    )
    return print(users_group_1)

clear() #Очищение окна терминала
start_program() #Начало программы
os.chdir('DataBases\\') #Изменение директории
#Цикл, действиющий, пока не будет прерван
while True:
    print(colored('Вы можете выполнить следующие действия: ', 'yellow'), '\n 1 - Создать БД паролей \n 2 - Использовать БД паролей \n 3 - Закрыть программу \n ? - Помощь')
    command = input(colored('Введите команду: ', 'cyan'))
    clear() #Очистка окна терминала
    if command == '1': #Создание БД
        create_database() #Создание БД
        clear()

    elif command == '2': #Использование БД
        try:
            files = os.listdir(".")
            print("Список всех доступных баз данных:")
            for i in range(len(files)):
                file_name = files[i].split(".")[0]
                print(file_name)
            print(colored("Использование базы данных", "yellow"), colored("\nОтмена - !", "magenta"))
            name = str(input(colored("Введите название вашей базы данных: ", 'cyan')))
            name = re.sub(r"^\s+|\s+$", "", name)  # Исключение из конца названия пробел
            if name != "!":
                password = str(input(colored("Введите пароль для вашей базы данных: ", 'cyan')))
                password = re.sub(r"^\s+|\s+$", "", password)  # Исключение из конца пароля пробел
                db = SQLite3x(path=use_database(name, password))  # Присвоение переменной "path" значения пути к БД
                db.connect()
                while True:
                    command = text_of_func()  # Выбор команды
                    if command == '1':
                        clear()
                        all_in_db(db)
                        add_new(db)  # Добавление новой записи в БД
                        clear()  # Очищение окна терминала

                    elif command == '2':
                        clear()  # Очищение окна терминала
                        all_in_db(db)
                        print(colored("Получить запись пароля", "yellow"), colored("\nОтмена - !", "magenta"))
                        name_password = input(colored('Введите название пароля: ', 'cyan'))
                        if name_password != "!":
                            users_group_1 = db.select(  # Запрос на выборку пароля по его названию
                                'passwords',
                                WHERE={'name': name_password}
                            )
                            clear()  # Очищение окна терминала
                            print(users_group_1)
                            input(colored('\n Нажмите любую клавишу, чтобы продолжить...', 'green'))
                            clear()
                        elif name_password == "!":
                            clear()
                            continue

                    elif command == '3':
                        clear()  # Очищение окна терминала
                        all_in_db(db)
                        print(colored("Все названия паролей", "yellow"))
                        users_group_1 = db.select(  # Запрос на выборку пароля по его названию
                            'passwords',
                            'name'
                        )
                        clear()  # Очищение окна терминала
                        print(users_group_1)
                        input(colored('\n Нажмите любую клавишу, чтобы продолжить...', 'green'))
                        clear()

                    elif command == '4':
                        clear()  # Очищение окна терминала
                        all_in_db(db)
                        print(colored("Удаление записи", "yellow"), colored("\nОтмена - !", "magenta"))
                        name_password = input(colored('Введите название пароля: ', 'cyan'))
                        if name_password != "!":
                            db.delete(  # Запрос на удаление записи по имени пароля
                                TABLE='passwords',
                                WHERE={'name': name_password}
                            )
                            print(colored("Запись пароля успешно удалена", "green"))
                            time.sleep(1)
                            clear()
                        elif name_password == "!":
                            clear()
                            continue

                    elif command == '5':
                        db.disconnect()  # Отключение БД
                        clear()  # Очищение окна терминала
                        encrypt_file(name, password)  # БД шифруется
                        break  # Прерывание цикла
            elif name == "!": #Если введен "!", то 
                clear()
        #В случие введения неверного названия файла или пароля вызываеться исключение.
        except BaseException:
            clear()
            print(colored("Неверное название файла или пароль.", "red"))
            time.sleep(1)
            clear()
            continue

    if command == '3': #Закрытие  программы
        clear() #Очищение окна терминала
        print(colored("Программа завершена.", 'green'))
        time.sleep(1) #Остановка выполнения программы на 1 секунду
        clear()
        sys.exit(0) #Закрытие окна программы

    if command == '?': #Вывод информации о программе и краткая сводка об использовании программы
        clear() #Очищение окна терминала
        print(colored(' UTOPIA PROJECT', 'green'), '- это бесплатная и свободная программа \nдля создания безопасных паролей, для повышения уровня \nконфиденциальности, при помощи создания зашифрованных \nбаз данных паролей.')
        print(colored('\nДля начала работы вам необходимо:', 'cyan'), '\n Поместить вашу базу данных в папку -', colored('DataBases', 'yellow'), "\n\n  Автор source-code -", colored("https://t.me/Flotry", "cyan"))
        input(colored('\n Нажмите любую клавишу, чтобы продолжить...', 'green')) #Ожидание нажатия любой клавиши
        clear() #Очищение окна терминала
