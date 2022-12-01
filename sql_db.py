'''
Это вспомогательные модули.
Последовательность использования
1. heading_transliterate() - Извлечение заголовков столбцов, transliterat кирилицы в латиницу. Полученные данные
скопировать и вставить в headers_db.py
2. В модуле headers_db.py отформатировать названия столбцов, согласно требованиям, задать формат полей.
Сразу подготовить поля для # Для функции insert_in_tab() insert_headers_01122022 =
3. create_tab() - Создание таблицы в БД Postgresql, используя поля из headers_db.py
4. insert_in_tab() - Импорт данных в БД Postgresql из .csv

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
# автоматически сохраняет изменения в БД. Чтобы после каждого запроса ни вставлять connection.commit()
connection.autocommit = True

# создать объект cursor для работы с database
cursor = connection.cursor()


'''
Извлечение заголовков столбцов, transliterat кирилицы в латиницу

Полученные заголовки необходимо отформатировать:
- запрещены символы ()/'%
- заменить: / на _
- заменить: % на percent

Формат столбцов:
- текст до 100 символов (в т.ч. даты, ссылки и пр.) --> varchar(100);
- текст более 100 символов --> text;
- суммы --> float. Если данные в float не грузятся, то сначало сделать формат numeric, а затем float;
'''
def heading_transliterate():
    wookbook = openpyxl.load_workbook('data/30.11.2022/реестр для пп_ОСН.xlsx')
    worksheet = wookbook.active
    for i in range(1):
        for col in worksheet.iter_cols(1, 47):
            ru_text = col[i].value
            text = translit(ru_text, language_code='ru', reversed=True)
            text_export = re.sub(' ', '_', text)

            print(text_export)


'''
Создание таблицы в БД, с наименованием полей, в которой будут храниться данные для обработки (например реестр должников)
!!!Таблица создается без данных.
'''
def create_tab():
    try:
        # создать таблицу
        cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS reestr_01122022({headers_db.headers_01122022});'''
        )
        print('[INFO] Таблица reestr_bankrot создана')

        # cursor.execute(
        #     '''CREATE TABLE IF NOT EXISTS declension_tribun_tab(
        #     id serial PRIMARY KEY,
        #     number_word int NOT NULL,
        #     ending_word varchar(20) NOT NULL,
        #     condition varchar(20),
        #     imenit varchar(10),
        #     rodit varchar(10),
        #     datel varchar(10),
        #     vinit varchar(10),
        #     tvorit varchar(10),
        #     predl varchar(10));'''
        # )
        # print('[INFO] Таблица declensions_debt_tab создана')

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


'''
Данные из excel (например из реестра должников) заливаются в таблицу БД, созданную в def create_tab().
'''
def insert_in_tab():
    with open('data/30.11.2022/реестр для пп_ОСН.csv', 'r') as file:
        data = csv.reader(file, delimiter=",")

        try:
            # добавление строк
            count = 0
            for row in data:
                index = str(row)[1:-1]
                if count > 0:
                    cursor.execute(
                        f'''INSERT INTO reestr_01122022 ({headers_db.insert_headers_01122022}) VALUES ({index});'''
                    )
                count += 1


        except Exception as _ex:
            print('[INFO] Error while working with PostgreSQL', _ex)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print('[INFO] PostgreSQL connection closed')




    # try:
    #     # добавление строк
    #     indexies_list = headers_db.indexes
    #     for index in indexies_list:
    #         # print(index)
    #         cursor.execute(
    #             f'''INSERT INTO indexes_tab (variables, number_of_words, keyword, formulas) VALUES {index};'''
    #         )
    #         # print('[INFO] Таблица reest_test2_di создана')
    #
    # except Exception as _ex:
    #     print('[INFO] Error while working with PostgreSQL', _ex)
    #
    # finally:
    #     if connection:
    #         cursor.close()
    #         connection.close()
    #         print('[INFO] PostgreSQL connection closed')



'''
Извлечение данных из даблицы БД
'''
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

    # heading_transliterate()
    # create_file()
    # create_tab()
    insert_in_tab()
    # select_from_tab()