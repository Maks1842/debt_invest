'''
Это вспомогательный модуль.
Импорт/Экспорт данных в СУБД Postgresql из excel/csv

!!! Для склонений, в формуле ОБЯЗАТЕЛЬНО должна быть ссылка на поле "РОД"!!!

cursor.fetchone() -- команда вывода первой строки таблицы
cursor.fetchall() -- вывод всех строк БД
cursor.fetchmany(3) -- вывод первых трёх строк БД
'''
from transliterate import translit
import psycopg2
from config import *
from datetime import date
import csv
import openpyxl
import re
import headers_db


# connect to exist database
connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)
connection.autocommit = True    # автоматически сохраняет изменения в БД. Чтобы после каждого запроса ни вставлять connection.commit()

# создать объект cursor для работы с database
cursor = connection.cursor()


def heading_transliterate():
    wookbook = openpyxl.load_workbook('data/Реестр для шаблона_work.xlsx')
    worksheet = wookbook.active
    for i in range(1):
        for col in worksheet.iter_cols(1, 93):
            ru_text = col[i].value
            text = translit(ru_text, language_code='ru', reversed=True)
            text_export = re.sub(' ', '_', text)

            print(text_export)

def create_tab():
    try:
        # # connect to exist database
        # connection = psycopg2.connect(
        #     host=host,
        #     user=user,
        #     password=password,
        #     database=db_name
        # )
        # connection.autocommit = True    # автоматически сохраняет изменения в БД. Чтобы после каждого запроса ни вставлять connection.commit()
        #
        # # вначале необходимо создать объект cursor для работы с database
        # cursor = connection.cursor()

        # создать таблицу
        cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS reestr_test_di({headers_db.headers_di_db});'''
        )
        print('[INFO] Таблица reestr_test2_di создана')

        cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS reestr_230522_di({headers_db.headers_230522_db});'''
        )
        print('[INFO] Таблица reestr_230522_di создана')

        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS indexes_tab(
            id serial PRIMARY KEY,
            variables varchar(30) NOT NULL,
            number_of_words int NOT NULL,
            keyword varchar(20),
            formulas text);'''
        )
        print('[INFO] Таблица indexes_tab создана')

        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS declension_tribun_tab(
            id serial PRIMARY KEY,
            number_word int NOT NULL,
            ending_word varchar(20) NOT NULL,
            condition varchar(20),
            imenit varchar(10),
            rodit varchar(10),
            datel varchar(10),
            vinit varchar(10),
            tvorit varchar(10),
            predl varchar(10));'''
        )
        print('[INFO] Таблица declensions_debt_tab создана')

        # x = 'number_ep'
        # y = 'debtor'
        # z = 'main_debt'
        #
        # cursor.execute(
        #     f'''SELECT {x}, {y}, {z} FROM executive_production_di;'''
        # )
        # ep_column = cursor.fetchall()
        # for ep in ep_column:
        #     # print(ep)
        #     current_date = date.today()
        #     today = current_date.strftime("%d-%m-%Y")
        #     with open(f'data/fssp_{today}.csv', 'a') as file:                 # Создаю файл .csv с заголовками
        #        writer = csv.writer(file, delimiter=',')
        #        writer.writerow(ep)


    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('[INFO] PostgreSQL connection closed')



def insert_in_tab():
    try:
        # добавление строк
        indexies_list = headers_db.indexes
        for index in indexies_list:
            # print(index)
            cursor.execute(
                f'''INSERT INTO indexes_tab (variables, number_of_words, keyword, formulas) VALUES {index};'''
            )
            # print('[INFO] Таблица reest_test2_di создана')

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def select_from_tab():
    try:
        cursor.execute('''SELECT * FROM indexes_tab;''')
        index_tab = cursor.fetchall()
        print(index_tab)
        for index in index_tab:
            x = 1
            cursor.execute(f'''{index[3]}{x}''')
            print(cursor.fetchone())

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def create_file():
    current_date = date.today()
    today = current_date.strftime("%d-%m-%Y")
    with open(f'data/fssp_{today}.csv', 'w') as file:                 # Создаю файл .csv с заголовками
        writer = csv.writer(file, delimiter=',')
        # writer.writerow(['№ Исполнительного производства',
        #                  'Начало ИП',
        #                  'Окончание ИП',
        #                  'Текущая задолженность',
        #                  'Основной долг',
        #                  'Исполнительский сбор',
        #                  'Погашенная часть',
        #                  'Причина',
        #                  'Основание',
        #                  'Должник',
        #                  'Дата рождения',
        #                  'Место рождения',
        #                  # 'Ограничения',
        #                  'Взыскатель',
        #                  'Судебный пристав',
        #                  'Телефон пристава',
        #                  'РОСП',
        #                  'Адрес РОСП'])

    create_tab()


if __name__ == '__main__':
    # create_file()
    # heading_transliterate()
    create_tab()
    # insert_in_tab()
    # select_from_tab()