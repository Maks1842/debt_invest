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

# text = ('Петросян Лейла Кареновна', 'жен')
# text = ('Петросян Карен Радикович', 'муж')
# text = ('Айрапетян Егише Павелович', 'муж')
# text = ('ПУШКИН Карен Радикович', 'муж')
# text = ('Иванов Илья Андреевич', 'муж')
# text = ('Артемова Зульфия Геннадьевна', 'жен')
# index_tab = ''
# cursor.execute('''SELECT * FROM indexes_tab;''')
# indexes_tab = cursor.fetchall()
# # print(f'{index_tab = }')
# for index in indexes_tab:
#     if index[3] != None:
#         try:
#             cursor.execute(f'''{index[3]}''')
#             index_tab = cursor.fetchall()
#         except Exception as _ex:
#             print('[INFO] Error while working with PostgreSQL', _ex)



def declension(text, index_tab):
    text_im = []
    text_ro = []
    text_da = []
    text_vi = []
    text_tv = []
    text_pr = []

    split_text = text[0].split()
    count = 0
    for word in split_text:
        count += 1
        word_imenit = declens_imenit(word, text[1], count, index_tab)
        word_rodit = declens_rodit(word, text[1], count, index_tab)
        word_dat = declens_dat(word, text[1], count, index_tab)
        word_vinit = declens_vinit(word, text[1], count, index_tab)
        word_tvorit = declens_tvorit(word, text[1], count, index_tab)
        word_predl = declens_predl(word, text[1], count, index_tab)
        
        if word_imenit == '':
            word_imenit = word
        if word_rodit == '':
            word_rodit = word
        if word_dat == '':
            word_dat = word
        if word_vinit == '':
            word_vinit = word
        if word_tvorit == '':
            word_tvorit = word
        if word_predl == '':
            word_predl = word


        text_im.append(word_imenit)
        text_ro.append(word_rodit)
        text_da.append(word_dat)
        text_vi.append(word_vinit)
        text_tv.append(word_tvorit)
        text_pr.append(word_predl)

        # print(f'{text_im = }')
        # print(f'{text_ro = }')
        # print(f'{text_da = }')
        # print(f'{text_vi = }')
        # print(f'{text_tv = }')
        # print(f'{text_pr = }')

    text_imenit = ' '.join(text_im)
    text_rodit = ' '.join(text_ro)
    text_dat = ' '.join(text_da)
    text_vinit = ' '.join(text_vi)
    text_tvorit = ' '.join(text_tv)
    text_predl = ' '.join(text_pr)

    return text_imenit, text_rodit, text_dat, text_vinit, text_tvorit, text_predl


def declens_imenit(word, rod, count, index_tab):
    word_imenit = ''

    sogl = 'б|в|г|д|ж|з|к|л|м|н|п|р|с|т|ф|х|ц|ч|ш|щ'
    gl = 'а|е|ё|и|о|у|э|ю|я|ы'
    # print(f'{index[2] = }')

    for index in index_tab:
        if index[1] == count:
            if re.findall(rf'({index[2]})$', word) and index[3] == None:
                if index[4] != None:               # Именительный
                    if re.findall(r'\+', index[4]):
                        new_ending = re.search(r'(?<=\+)\w+', index[4]).group()
                        word_imenit = word + new_ending
                    elif re.findall(r'-', index[4]):
                        old_ending = re.search(r'\w+(?=\-)', index[4]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[4]).group()
                        word_imenit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(муж)|м', index[3]) and re.findall(r'(?i)(муж)|м', rod):
                if index[4] != None:               # Именительный
                    if re.findall(r'\+', index[4]):
                        new_ending = re.search(r'(?<=\+)\w+', index[4]).group()
                        word_imenit = word + new_ending
                    elif re.findall(r'-', index[4]):
                        old_ending = re.search(r'\w+(?=\-)', index[4]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[4]).group()
                        word_imenit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(жен)|ж', index[3]) and re.findall(r'(?i)(жен)|ж', rod):
                if index[4] != None:               # Именительный
                    if re.findall(r'\+', index[4]):
                        new_ending = re.search(r'(?<=\+)\w+', index[4]).group()
                        word_imenit = word + new_ending
                    elif re.findall(r'-', index[4]):
                        old_ending = re.search(r'\w+(?=\-)|.(?=\-)', index[4]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[4]).group()
                        word_imenit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif f'{index[2]}' == 'sogl' and re.findall(rf'({sogl})$', word) and re.findall(r'(?i)(муж)|м', index[3]) and re.findall(r'(?i)(муж)|м', rod):
                if index[4] != None:               # Именительный
                    if re.findall(r'\+', index[4]):
                        new_ending = re.search(r'(?<=\+)\w+', index[4]).group()
                        word_imenit = word + new_ending
                    elif re.findall(r'-', index[4]):
                        old_ending = re.search(r'\w+(?=\-)', index[4]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[4]).group()
                        word_imenit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                        
    return word_imenit


def declens_rodit(word, rod, count, index_tab):
    word_rodit = ''

    sogl = 'б|в|г|д|ж|з|к|л|м|н|п|р|с|т|ф|х|ц|ч|ш|щ'
    gl = 'а|е|ё|и|о|у|э|ю|я|ы'
    # print(f'{index[2] = }')

    for index in index_tab:
        if index[1] == count:
            if re.findall(rf'({index[2]})$', word) and index[3] == None:
                if index[5] != None:               # Родительный
                    if re.findall(r'\+', index[5]):
                        new_ending = re.search(r'(?<=\+)\w+', index[5]).group()
                        word_rodit = word + new_ending
                    elif re.findall(r'-', index[5]):
                        old_ending = re.search(r'\w+(?=\-)', index[5]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[5]).group()
                        word_rodit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(муж)|м', index[3]) and re.findall(r'(?i)(муж)|м', rod):
                if index[5] != None:               # Именительный
                    if re.findall(r'\+', index[5]):
                        new_ending = re.search(r'(?<=\+)\w+', index[5]).group()
                        word_rodit = word + new_ending
                    elif re.findall(r'-', index[5]):
                        old_ending = re.search(r'\w+(?=\-)', index[5]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[5]).group()
                        word_rodit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(жен)|ж', index[3]) and re.findall(r'(?i)(жен)|ж', rod):
                if index[5] != None:               # Именительный
                    if re.findall(r'\+', index[5]):
                        new_ending = re.search(r'(?<=\+)\w+', index[5]).group()
                        word_rodit = word + new_ending
                    elif re.findall(r'-', index[5]):
                        old_ending = re.search(r'\w+(?=\-)|.(?=\-)', index[5]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[5]).group()
                        word_rodit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif f'{index[2]}' == 'sogl' and re.findall(rf'({sogl})$', word) and re.findall(r'(?i)(муж)|м', index[3]) and re.findall(r'(?i)(муж)|м', rod):
                if index[5] != None:               # Именительный
                    if re.findall(r'\+', index[5]):
                        new_ending = re.search(r'(?<=\+)\w+', index[5]).group()
                        word_rodit = word + new_ending
                    elif re.findall(r'-', index[5]):
                        old_ending = re.search(r'\w+(?=\-)', index[5]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[5]).group()
                        word_rodit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

    return word_rodit


def declens_dat(word, rod, count, index_tab):
    word_dat = ''

    sogl = 'б|в|г|д|ж|з|к|л|м|н|п|р|с|т|ф|х|ц|ч|ш|щ'
    gl = 'а|е|ё|и|о|у|э|ю|я|ы'
    # print(f'{index[2] = }')

    for index in index_tab:
        if index[1] == count:
            if re.findall(rf'({index[2]})$', word) and index[3] == None:
                if index[6] != None:               # Родительный
                    if re.findall(r'\+', index[6]):
                        new_ending = re.search(r'(?<=\+)\w+', index[6]).group()
                        word_dat = word + new_ending
                    elif re.findall(r'-', index[6]):
                        old_ending = re.search(r'\w+(?=\-)', index[6]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[6]).group()
                        word_dat = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(муж)|м', index[3]) and re.findall(r'(?i)(муж)|м', rod):
                if index[6] != None:               # Именительный
                    if re.findall(r'\+', index[6]):
                        new_ending = re.search(r'(?<=\+)\w+', index[6]).group()
                        word_dat = word + new_ending
                    elif re.findall(r'-', index[6]):
                        old_ending = re.search(r'\w+(?=\-)', index[6]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[6]).group()
                        word_dat = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(жен)|ж', index[3]) and re.findall(r'(?i)(жен)|ж', rod):
                if index[6] != None:               # Именительный
                    if re.findall(r'\+', index[6]):
                        new_ending = re.search(r'(?<=\+)\w+', index[6]).group()
                        word_dat = word + new_ending
                    elif re.findall(r'-', index[6]):
                        old_ending = re.search(r'\w+(?=\-)|.(?=\-)', index[6]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[6]).group()
                        word_dat = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif f'{index[2]}' == 'sogl' and re.findall(rf'({sogl})$', word) and re.findall(r'(?i)(муж)|м', index[3]) and re.findall(r'(?i)(муж)|м', rod):
                if index[6] != None:               # Именительный
                    if re.findall(r'\+', index[6]):
                        new_ending = re.search(r'(?<=\+)\w+', index[6]).group()
                        word_dat = word + new_ending
                    elif re.findall(r'-', index[6]):
                        old_ending = re.search(r'\w+(?=\-)', index[6]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[6]).group()
                        word_dat = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

    return word_dat


def declens_vinit(word, rod, count, index_tab):
    word_vinit = ''

    sogl = 'б|в|г|д|ж|з|к|л|м|н|п|р|с|т|ф|х|ц|ч|ш|щ'
    gl = 'а|е|ё|и|о|у|э|ю|я|ы'
    # print(f'{index[2] = }')

    for index in index_tab:
        if index[1] == count:
            if re.findall(rf'({index[2]})$', word) and index[3] == None:
                if index[7] != None:               # Родительный
                    if re.findall(r'\+', index[7]):
                        new_ending = re.search(r'(?<=\+)\w+', index[7]).group()
                        word_vinit = word + new_ending
                    elif re.findall(r'-', index[7]):
                        old_ending = re.search(r'\w+(?=\-)', index[7]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[7]).group()
                        word_vinit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(муж)|м', index[3]) and re.findall(r'(?i)(муж)|м', rod):
                if index[7] != None:               # Именительный
                    if re.findall(r'\+', index[7]):
                        new_ending = re.search(r'(?<=\+)\w+', index[7]).group()
                        word_vinit = word + new_ending
                    elif re.findall(r'-', index[7]):
                        old_ending = re.search(r'\w+(?=\-)', index[7]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[7]).group()
                        word_vinit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(жен)|ж', index[3]) and re.findall(r'(?i)(жен)|ж', rod):
                if index[7] != None:               # Именительный
                    if re.findall(r'\+', index[7]):
                        new_ending = re.search(r'(?<=\+)\w+', index[7]).group()
                        word_vinit = word + new_ending
                    elif re.findall(r'-', index[7]):
                        old_ending = re.search(r'\w+(?=\-)|.(?=\-)', index[7]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[7]).group()
                        word_vinit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif f'{index[2]}' == 'sogl' and re.findall(rf'({sogl})$', word) and re.findall(r'(?i)(муж)|м', index[3]) and re.findall(r'(?i)(муж)|м', rod):
                if index[7] != None:               # Именительный
                    if re.findall(r'\+', index[7]):
                        new_ending = re.search(r'(?<=\+)\w+', index[7]).group()
                        word_vinit = word + new_ending
                    elif re.findall(r'-', index[7]):
                        old_ending = re.search(r'\w+(?=\-)', index[7]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[7]).group()
                        word_vinit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

    return word_vinit


def declens_tvorit(word, rod, count, index_tab):
    word_tvorit = ''

    sogl = 'б|в|г|д|ж|з|к|л|м|н|п|р|с|т|ф|х|ц|ч|ш|щ'
    gl = 'а|е|ё|и|о|у|э|ю|я|ы'
    # print(f'{index[2] = }')

    for index in index_tab:
        if index[1] == count:
            if re.findall(rf'({index[2]})$', word) and index[3] == None:
                if index[8] != None:               # Родительный
                    if re.findall(r'\+', index[8]):
                        new_ending = re.search(r'(?<=\+)\w+', index[8]).group()
                        word_tvorit = word + new_ending
                    elif re.findall(r'-', index[8]):
                        old_ending = re.search(r'\w+(?=\-)', index[8]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[8]).group()
                        word_tvorit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(муж)|м', index[3]) and re.findall(r'(?i)(муж)|м', rod):
                if index[8] != None:               # Именительный
                    if re.findall(r'\+', index[8]):
                        new_ending = re.search(r'(?<=\+)\w+', index[8]).group()
                        word_tvorit = word + new_ending
                    elif re.findall(r'-', index[8]):
                        old_ending = re.search(r'\w+(?=\-)', index[8]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[8]).group()
                        word_tvorit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(жен)|ж', index[3]) and re.findall(r'(?i)(жен)|ж', rod):
                if index[8] != None:               # Именительный
                    if re.findall(r'\+', index[8]):
                        new_ending = re.search(r'(?<=\+)\w+', index[8]).group()
                        word_tvorit = word + new_ending
                    elif re.findall(r'-', index[8]):
                        old_ending = re.search(r'\w+(?=\-)|.(?=\-)', index[8]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[8]).group()
                        word_tvorit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif f'{index[2]}' == 'sogl' and re.findall(rf'({sogl})$', word) and re.findall(r'(?i)(муж)|м', index[3]) and re.findall(r'(?i)(муж)|м', rod):
                if index[8] != None:               # Именительный
                    if re.findall(r'\+', index[8]):
                        new_ending = re.search(r'(?<=\+)\w+', index[8]).group()
                        word_tvorit = word + new_ending
                    elif re.findall(r'-', index[8]):
                        old_ending = re.search(r'\w+(?=\-)', index[8]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[8]).group()
                        word_tvorit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

    return word_tvorit


def declens_predl(word, rod, count, index_tab):
    word_predl = ''

    sogl = 'б|в|г|д|ж|з|к|л|м|н|п|р|с|т|ф|х|ц|ч|ш|щ'
    gl = 'а|е|ё|и|о|у|э|ю|я|ы'
    # print(f'{index[2] = }')

    for index in index_tab:
        if index[1] == count:
            if re.findall(rf'({index[2]})$', word) and index[3] == None:
                if index[9] != None:               # Родительный
                    if re.findall(r'\+', index[9]):
                        new_ending = re.search(r'(?<=\+)\w+', index[9]).group()
                        word_predl = word + new_ending
                    elif re.findall(r'-', index[9]):
                        old_ending = re.search(r'\w+(?=\-)', index[9]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[9]).group()
                        word_predl = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(муж)|м', index[3]) and re.findall(r'(?i)(муж)|м', rod):
                if index[9] != None:               # Именительный
                    if re.findall(r'\+', index[9]):
                        new_ending = re.search(r'(?<=\+)\w+', index[9]).group()
                        word_predl = word + new_ending
                    elif re.findall(r'-', index[9]):
                        old_ending = re.search(r'\w+(?=\-)', index[9]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[9]).group()
                        word_predl = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(жен)|ж', index[3]) and re.findall(r'(?i)(жен)|ж', rod):
                if index[9] != None:               # Именительный
                    if re.findall(r'\+', index[9]):
                        new_ending = re.search(r'(?<=\+)\w+', index[9]).group()
                        word_predl = word + new_ending
                    elif re.findall(r'-', index[9]):
                        old_ending = re.search(r'\w+(?=\-)|.(?=\-)', index[9]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[9]).group()
                        word_predl = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif f'{index[2]}' == 'sogl' and re.findall(rf'({sogl})$', word) and re.findall(r'(?i)(муж)|м', index[3]) and re.findall(r'(?i)(муж)|м', rod):
                if index[9] != None:               # Именительный
                    if re.findall(r'\+', index[9]):
                        new_ending = re.search(r'(?<=\+)\w+', index[9]).group()
                        word_predl = word + new_ending
                    elif re.findall(r'-', index[9]):
                        old_ending = re.search(r'\w+(?=\-)', index[9]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[9]).group()
                        word_predl = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

    return word_predl



# declension(text, index_tab)