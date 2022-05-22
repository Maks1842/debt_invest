'''
nomn - именительный -- Кто? Что?
gent - родительный -- Кого? Чего?
datv - дательный -- Кому? Чему?
accs - винительный -- Кого? Что?
ablt - творительный -- Кем? Чем?
loct - предложный -- О ком? О чём?
voct - звательный -- Его формы используются при обращении к человеку.

masc - мужской род
femn - женский род
neut - средний род

sing - единственное число
plur - множественное число

'''
import pymorphy3
from docxtpl import DocxTemplate
import psycopg2
import re

from config import *
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

morph = pymorphy3.MorphAnalyzer()


def select_from_reestr_tab():
    try:
        cursor.execute('''SELECT id FROM reestr_test_di;''')
        reestr_tab = cursor.fetchall()
        for data in reestr_tab:
            select_from_indexes_tab(data[0])
            # print(f'{data[0] = }')

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL 1', _ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def select_from_indexes_tab(id_reestr):
    try:
        cursor.execute('''SELECT * FROM indexes_tab;''')
        index_tab = cursor.fetchall()
        print(f'{index_tab = }')
        for index in index_tab:
            if index[2] > 0:
                cursor.execute(f'''{index[4]}{id_reestr}''')
                text = cursor.fetchone()
                some_word(text)
            # elif index[2] == 0 and index[3] == '':
            #     # print('not text')
            # else:
                # print('text')
        x = 1
        #     cursor.execute(f'''{index[3]}{x}''')
        #     print(cursor.fetchone())

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL 2', _ex)

    # finally:
        # if connection:
        #     cursor.close()
            # connection.close()
            # print('[INFO] PostgreSQL connection closed')



def test_doc(index, word):
    doc = DocxTemplate(f'data/Адм иск на невозбуждение.docx')
    context = { 'test5' : "Пустота",
                'test2' : "ВТОРОЙ ТЕСТ",
                'test3' : "ТРЕТИЙ ТЕСТ",
                f'{index}': f'{word}',
                'xnjq': "Чтонибудь"}
    doc.render(context)
    doc.save(f'data/Адм иск на невозбуждение_test.docx')



# text = 'Петросян Лейла Кареновна'
# text = 'Петросян Карен Радикович'
text = 'Айрапетян Егише Павелович'
# text = 'Пушкин-Суворов Карен Радикович'
# text = 'Суд Петровского района'
# text = 'Мировой Судья г. Пятигорска'







def one_word():
    split_text = text.split()
    s = ''
    x = 1
    if x == 1:
        for x in split_text[0:x]:
            if 'femn' in morph.tag(x)[0]:
                letter2 = morph.parse(x)[0].inflect({'datv', 'masc'}).word
                s = letter2.title()
            elif 'masc' in morph.tag(x)[0]:
                letter2 = morph.parse(x)[0].inflect({'datv', 'masc'}).word
                s = letter2.title()
            elif 'ms-f' in morph.tag(x)[0]:
                letter2 = morph.parse(x)[0].inflect({'datv'}).word
                s = letter2.title()
            else:
                s = x
        split_text[0] = s

    print(' '.join(split_text))


def two_word():
    split_text = text.split()

    y = []
    x = 2
    if x == 2:
        for x in split_text[0:x]:
            letter3 = morph.tag(x)
            if 'femn' in morph.tag(x)[0]:
                letter2 = morph.parse(x)[0].inflect({'ablt', 'masc'}).word
                s = letter2.title()
                y.append(s)
            elif 'masc' in morph.tag(x)[0]:
                letter2 = morph.parse(x)[0].inflect({'ablt', 'masc'}).word
                s = letter2.title()
                y.append(s)
            elif 'ms-f' in morph.tag(x)[0]:
                letter2 = morph.parse(x)[0].inflect({'ablt'}).word
                s = letter2.title()
                y.append(s)
            else:
                y.append(x)

        split_text[0] = y[0]
        split_text[1] = y[1]

    print(' '.join(split_text))

def some_word(text):
    print('finish')
    split_text = text[0].split()
    print(f'{split_text = }')

    type = text[1]
    y = []

    for x in split_text:
        if re.findall(r'(?i)(муж)', type):
            print(f'{x = }')
            print(f'{morph.parse(x) = }')
            letter2 = morph.parse(x)[0].inflect({'datv', 'masc'}).word
            s = letter2.title()
        elif re.findall(r'(?i)(жен)', type):
            print(f'{morph.parse(x) = }')
            letter2 = morph.parse(x)[0].inflect({'datv', 'femn'}).word
            s = letter2.title()
        # else:
        #     s = x

        y.append(s)
    print(' '.join(y))




def declension_by_case(index, word):
    context = {f'{index}': f'{word}',
               f'{index}_ро': f'{word}',
               f'{index}_да': f'{word}',
               f'{index}_ви': f'{word}',
               f'{index}_тв': f'{word}',
               f'{index}_пр': f'{word}'}
    # doc.render(context)




# test_doc('test', 'Всё работает')
# some_word()
# two_word()
# one_word()
# select_from_tab()
select_from_reestr_tab()