'''
nomn - именительный -- Кто? Что?
gent - родительный -- Кого? Чего?
datv - дательный -- Кому? Чему?
accs - винительный -- Кого? Что?
ablt - творительный -- Кем? Чем?
loct - предложный -- О ком? О чём?

!!! Для склонений, в формуле ОБЯЗАТЕЛЬНО должна быть ссылка на поле "РОД"!!!
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
        cursor.execute('''SELECT id FROM reestr_230522_di;''')
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
    context = {}
    result_decl = ''
    try:
        cursor.execute('''SELECT * FROM indexes_tab;''')
        indexes_tab = cursor.fetchall()
        # print(f'{index_tab = }')
        for index in indexes_tab:
            if index[3] != None:
                try:
                    cursor.execute(f'''{index[3]}''')
                    index_tab = cursor.fetchall()
                except Exception as _ex:
                    print('[INFO] Error while working with PostgreSQL', _ex)

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
                # print(f'{context = }')

            elif index[3] == None:
                cursor.execute(f'''{index[2]}{id_reestr}''')
                text2 = cursor.fetchone()
                # print(f'{x = }')
                if f'{text2[0]}' != 'None':
                    context[f'{index[1]}'] = f'{text2[0]}'
                    # print(f'{context = }')
                else:
                    context[f'{index[1]}'] = ''
            doc_pattern(context, result_decl, count)

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL 2', _ex)


def doc_pattern(context, word, count):
    doc = DocxTemplate(f'data/УВЕД-ТРЕБ  ЧС_ШАБЛОН.docx')
    doc.render(context)
    doc.save(f'data/Без печати_240522/УВЕД-ТРЕБ {word[0]}_{count}.docx')



# select_from_tab()
select_from_reestr_tab()
# select_from_indexes_tab()
# doc_pattern()