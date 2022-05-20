'''Импорт/Экспорт данных в СУБД Postgresql из excel/csv
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


def heading_transliterate():
    wookbook = openpyxl.load_workbook('data/база_test.xlsx')
    worksheet = wookbook.active
    for i in range(1):
        for col in worksheet.iter_cols(1, 93):
            # print(col[i].value)


            ru_text = col[i].value
            text = translit(ru_text, language_code='ru', reversed=True)
            text_export = re.sub(' ', '_', text)

            print(text_export)

def connect_postgres():
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True    # автоматически сохраняет изменения в БД. Чтобы после каждого запроса ни вставлять connection.commit()

        # вначале необходимо создать объект cursor для работы с database
        cursor = connection.cursor()

        # создать таблицу
        cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS reest_test2_di({headers_db.headers_di_db});'''
        )
        print('[INFO] Таблица создана')

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

    connect_postgres()


if __name__ == '__main__':
    # create_file()
    # heading_transliterate()
    connect_postgres()