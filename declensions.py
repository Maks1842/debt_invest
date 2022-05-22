import psycopg2
from config import *
import re

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


# text = 'Петросян Лейла Кареновна'
# text = 'Петросян Карен Радикович'
# text = 'Айрапетян Егише Павелович'
# text = 'Пушкин-Суворов Карен Радикович'
text = 'Иванов Аркадий Андреевич'
index_tab = ''

index_signal = True

try:
    cursor.execute('''SELECT * FROM declensions_debt_tab;''')
    index_tab = cursor.fetchall()
    print(f'{index_tab = }')


except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)

def declension(text, index_tab):
    y = []
    split_text = text.split()
    count = 0
    for word in split_text:
        count += 1
        if index_signal == True:
            for index in index_tab:
                if index[1] == count:
                    word_dec = word_declens(word, index)
                    v = word_dec

                    # text = cursor.fetchone()
                    # some_word(text)

        else:
            y.append(word)


def word_declens(word, index):
    x = word
    v = index[2]
    if re.findall(rf'{index[2]}$', word) and index[3] == None:
        t = index[2]
        u = index[4]
        i = index[5]
        if index[4] != None:
            if re.findall(r'\+', index[4]):
                new_ending = re.search(r'(?<=\+)\w+', index[5]).group()
                word_dec = word + new_ending
            elif re.findall(r'-', index[4]):
                old_ending = re.search(r'\w+(?=\-)', index[4]).group()
                new_ending = re.search(r'(?<=\-)\w+', index[4]).group()
                word_dec = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
        elif index[5] != None:
            if re.findall(r'\+', index[5]):
                new_ending = re.search(r'(?<=\+)\w+', index[5]).group()
                word_dec = word + new_ending
                print(word_dec)
            elif re.findall(r'-', index[5]):
                old_ending = re.search(r'\w+(?=\-)', index[5]).group()
                new_ending = re.search(r'(?<=\-)\w+', index[5]).group()
                word_dec = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                print(word_dec)


    elif re.findall(rf'{index[2]}$', word) and re.search(r'(?i)(муж)', index[3]).group():
        t = index[2]
        u = index[4]
        i = index[5]
        if index[4] != None:
            if re.findall(r'\+', index[4]):
                new_ending = re.search(r'(?<=\+)\w+', index[5]).group()
                word_dec = word + new_ending
            elif re.findall(r'\-', index[4]):
                old_ending = re.search(r'\w+(?=\-)', index[4]).group()
                new_ending = re.search(r'(?<=\-)\w+', index[4]).group()
                word_dec = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
        elif index[5] != None:
            if re.findall(r'\+', index[5]):
                new_ending = re.search(r'(?<=\+)\w+', index[5]).group()
                word_dec = word + new_ending
                print(word_dec)
            elif re.findall(r'\-', index[5]):
                old_ending = re.search(r'\w+(?=\-)', index[5]).group()
                new_ending = re.search(r'(?<=\-)\w+', index[5]).group()
                word_dec = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                x = word_dec












declension(text, index_tab)