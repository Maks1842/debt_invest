'''
Основной модуль для формирования документов .docx.

Необходимо создать таблицу в БД:
- столбцы - наименование полей из которых брать необходимую информацию, для добавления в .docx;
- строки - должники, по которым формировать документы.

Последовательность импортирования данных в БД, с помощью модуля sql_db.py
1. heading_transliterate() - Извлечение заголовков столбцов, transliterat кирилицы в латиницу. Полученные данные
скопировать и вставить в headers_db.py
2. В модуле headers_db.py отформатировать названия столбцов, согласно требованиям, задать формат полей.
Сразу подготовить поля для # Для функции insert_in_tab() insert_headers_01122022 =
3. create_tab() - Создание таблицы в БД Postgresql, используя поля из headers_db.py
4. insert_in_tab() - Импорт данных в БД Postgresql из .csv


В моделе indexes_tab, хранятся индексы применяемые в шаблоне и sql-запросы из таблицы с должниками - declension_tribun,
а также запросы к таблицам со склонениями - declension_debt.

В шаблоне .docx индексация осуществляется по тегам. Пример: {{Адрес_должника}}, {{Номер_КД}};
если необходимо склонение, то - {{Должник_дат}}


nomn - именительный -- Кто? Что?
gent - родительный -- Кого? Чего?
datv - дательный -- Кому? Чему?
accs - винительный -- Кого? Что?
ablt - творительный -- Кем? Чем?
loct - предложный -- О ком? О чём?

!!! Для склонений, в формуле ОБЯЗАТЕЛЬНО должна быть ссылка на поле "РОД" (Модель - index_tab, поле - formulas)!!!
пример - SELECT FIO, pol FROM reestr_230522_di WHERE id =
'''
from docxtpl import DocxTemplate
import psycopg2
import re

from config import *
import declensions
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



def select_from_reestr_tab():
    try:
        cursor.execute('''SELECT id FROM reestr_01122022;''')
        reestr_tab = cursor.fetchall()
        count = 1455
        for data in reestr_tab:
            select_from_indexes_tab(data[0], count)
            count += 1

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL 1', _ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def select_from_indexes_tab(id_reestr, count):
    context_dict = {}
    context = {}
    result_decl = ''
    count_debt = 0

    cursor.execute('''SELECT * FROM indexes_tab;''')
    indexes_tab = cursor.fetchall()
    # print(f'{index_tab = }')
    for index in indexes_tab:
        count_debt += 1
        if index[3] != None:
            try:
                cursor.execute(f'''{index[3]}''')
                index_tab = cursor.fetchall()
            except Exception as _ex:
                print('[INFO] Error while working with PostgreSQL (index[3])', _ex)

            try:
                cursor.execute(f'''{index[2]}{id_reestr}''')
                text = cursor.fetchone()
                # print(f'{text = }')
                result_decl = declensions.declension(text, index_tab)
                context = { f'{index[1]}': f'{result_decl[0]}',
                            f'{index[1]}_им': f'{result_decl[0]}',
                            f'{index[1]}_род': f'{result_decl[1]}',
                            f'{index[1]}_дат': f'{result_decl[2]}',
                            f'{index[1]}_вин': f'{result_decl[3]}',
                            f'{index[1]}_твор': f'{result_decl[4]}',
                            f'{index[1]}_пред': f'{result_decl[5]}',
                            f'Порядковый': f'{count}'
                            }
            except Exception as _ex:
                print('[INFO] Error while working with PostgreSQL (declensions)', _ex)

            context_dict.update(context)

        elif index[3] == None:
            try:
                cursor.execute(f'''{index[2]}{id_reestr}''')
                text2 = cursor.fetchone()
                # print(f'{text2[0] = }')
                if f'{text2[0]}' != '':
                    context[f'{index[1]}'] = f'{text2[0]}'
                    # print(f'{context = }')
                else:
                    context[f'{index[1]}'] = ''
            except Exception as _ex:
                print('[INFO] Error while working with PostgreSQL (text2)', _ex)

            context_dict.update(context)

    doc_pattern(context_dict, count)


def doc_pattern(context_dict, count):
    doc = DocxTemplate(f'data/30.11.2022/1 ПП окон ИП, есть ИЛ_ШАБЛОН.docx')
    name = context_dict.get('Должник')
    num = context_dict.get('номер_договора')
    doc.render(context_dict)
    doc.save(f'result/ПП окон ИП, есть ИЛ/{name}_{num}.docx')



# select_from_tab()
select_from_reestr_tab()
# select_from_indexes_tab()
# doc_pattern()