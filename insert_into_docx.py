'''
nomn - именительный -- Кто? Что?
gent - родительный -- Кого? Чего?
datv - дательный -- Кому? Чему?
accs - винительный -- Кого? Что?
ablt - творительный -- Кем? Чем?
loct - предложный -- О ком? О чём?
voct - звательный -- Его формы используются при обращении к человеку.


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
        cursor.execute('''SELECT id FROM reestr_test_di;''')
        reestr_tab = cursor.fetchall()
        count = 100
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

    try:
        cursor.execute('''SELECT * FROM indexes_tab;''')
        indexes_tab = cursor.fetchall()
        # print(f'{index_tab = }')
        for index in indexes_tab:
            if 'Должник' in index:
                try:
                    cursor.execute('''SELECT * FROM declensions_debt_tab;''')
                    index_tab = cursor.fetchall()
                except Exception as _ex:
                    print('[INFO] Error while working with PostgreSQL', _ex)

                cursor.execute(f'''{index[2]}{id_reestr}''')
                text = cursor.fetchone()
                # print(f'{text = }')
                result_decl = declensions.declension(text, index_tab)
                # print(f'{result_decl = }')
                doc_pattern(index, result_decl, count)
            # elif 'Остаток_долга' in index:
            #     try:
            #         cursor.execute('''SELECT * FROM declensions_debt_tab;''')
            #         index_tab = cursor.fetchall()
            #     except Exception as _ex:
            #         print('[INFO] Error while working with PostgreSQL', _ex)
            #
            #     cursor.execute(f'''{index[2]}{id_reestr}''')
            #     text = cursor.fetchone()
            #     # print(f'{text = }')
            #     result_decl = declensions.declension(text, index_tab)
            #     # print(f'{result_decl = }')
            #     doc_pattern(index, result_decl, count)


    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL 2', _ex)

    # finally:
        # if connection:
        #     cursor.close()
            # connection.close()
            # print('[INFO] PostgreSQL connection closed')



def doc_pattern(index, word, count):
    doc = DocxTemplate(f'data/Адм иск ШАБЛОН.docx')

    context = { f'{index[1]}': f'{word[0]}',
                f'{index[1]}_им': f'{word[0]}',
                f'{index[1]}_род': f'{word[1]}',
                f'{index[1]}_дат': f'{word[2]}',
                f'{index[1]}_вин': f'{word[3]}',
                f'{index[1]}_твор': f'{word[4]}',
                f'{index[1]}_пред': f'{word[5]}',
                f'Счётчик': f'{count}'
                }
    doc.render(context)
    doc.save(f'data/Адм иск {word[0]}.docx')




# test_doc('test', 'Всё работает')
# some_word()
# two_word()
# one_word()
# select_from_tab()
select_from_reestr_tab()
# select_from_indexes_tab()