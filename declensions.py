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
text = ('Иванов Аркадий Андреевич', 'муж')
index_tab = ''

index_signal = True

try:
    cursor.execute('''SELECT * FROM declensions_debt_tab;''')
    index_tab = cursor.fetchall()
    # print(f'{index_tab = }')

except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)

# def declension(text, index_tab):
#     y = []
#     split_text = text[0].split()
#     count = 0
#     for word in split_text:
#         count += 1
#         for index in index_tab:
#             if index[1] == count:
#                 word_imenit = declens_imenit(word, text[1], index)
#                 word_rodit = declens_imenit(word, text[1], index)
#                 word_datel = declens_imenit(word, text[1], index)
#                 word_vinit = declens_imenit(word, text[1], index)
#                 word_tvorit = declens_imenit(word, text[1], index)
#                 word_predl = declens_imenit(word, text[1], index)
#                 v = word_dec
#             print(f'{v= }')


                # text = cursor.fetchone()
                # some_word(text)

        # else:
        #     y.append(word)


def declension(text, index_tab):
    y = []
    split_text = text[0].split()
    count = 0
    for word in split_text:
        count += 1
        word_dec = word_declens(word, text[1], count, index_tab)
        print(f'{word_dec = }')


                    # text = cursor.fetchone()
                    # some_word(text)



def word_declens(word, rod,  count, index_tab):
    word_imenit = ''
    word_rodit = ''
    word_datel = ''
    word_vinit = ''
    word_tvorit = ''
    word_predl = ''

    declensions_word = []


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
                elif index[5] != None:               # Родительный
                    if re.findall(r'\+', index[5]):
                        new_ending = re.search(r'(?<=\+)\w+', index[5]).group()
                        word_rodit = word + new_ending
                    elif re.findall(r'-', index[5]):
                        old_ending = re.search(r'\w+(?=\-)', index[5]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[5]).group()
                        word_rodit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[6] != None:               # Дательный
                    if re.findall(r'\+', index[6]):
                        new_ending = re.search(r'(?<=\+)\w+', index[6]).group()
                        word_datel = word + new_ending
                    elif re.findall(r'-', index[6]):
                        old_ending = re.search(r'\w+(?=\-)', index[6]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[6]).group()
                        word_datel = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[7] != None:               # Винительный
                    if re.findall(r'\+', index[7]):
                        new_ending = re.search(r'(?<=\+)\w+', index[7]).group()
                        word_vinit = word + new_ending
                    elif re.findall(r'-', index[7]):
                        old_ending = re.search(r'\w+(?=\-)', index[7]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[7]).group()
                        word_vinit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[8] != None:               # Творетельный
                    if re.findall(r'\+', index[8]):
                        new_ending = re.search(r'(?<=\+)\w+', index[8]).group()
                        word_tvorit = word + new_ending
                        print(f'{word_tvorit = }')
                    elif re.findall(r'-', index[8]):
                        old_ending = re.search(r'\w+(?=\-)', index[8]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[8]).group()
                        word_tvorit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                        print(f'{word_tvorit = }')
                elif index[9] != None:               # Предложный
                    if re.findall(r'\+', index[9]):
                        new_ending = re.search(r'(?<=\+)\w+', index[9]).group()
                        word_predl = word + new_ending
                    elif re.findall(r'-', index[9]):
                        old_ending = re.search(r'\w+(?=\-)', index[9]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[9]).group()
                        word_predl = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(муж)', index[3]) and re.findall(r'(?i)(муж)', rod):
                if index[4] != None:               # Именительный
                    if re.findall(r'\+', index[4]):
                        new_ending = re.search(r'(?<=\+)\w+', index[4]).group()
                        word_imenit = word + new_ending
                    elif re.findall(r'-', index[4]):
                        old_ending = re.search(r'\w+(?=\-)', index[4]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[4]).group()
                        word_imenit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[5] != None:               # Родительный
                    if re.findall(r'\+', index[5]):
                        new_ending = re.search(r'(?<=\+)\w+', index[5]).group()
                        word_rodit = word + new_ending
                    elif re.findall(r'-', index[5]):
                        old_ending = re.search(r'\w+(?=\-)', index[5]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[5]).group()
                        word_rodit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[6] != None:               # Дательный
                    if re.findall(r'\+', index[6]):
                        new_ending = re.search(r'(?<=\+)\w+', index[6]).group()
                        word_datel = word + new_ending
                    elif re.findall(r'-', index[6]):
                        old_ending = re.search(r'\w+(?=\-)', index[6]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[6]).group()
                        word_datel = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[7] != None:               # Винительный
                    if re.findall(r'\+', index[7]):
                        new_ending = re.search(r'(?<=\+)\w+', index[7]).group()
                        word_vinit = word + new_ending
                    elif re.findall(r'-', index[7]):
                        old_ending = re.search(r'\w+(?=\-)', index[7]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[7]).group()
                        word_vinit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[8] != None:               # Творетельный
                    if re.findall(r'\+', index[8]):
                        new_ending = re.search(r'(?<=\+)\w+', index[8]).group()
                        word_tvorit = word + new_ending
                        print(f'{word_tvorit = }')
                    elif re.findall(r'-', index[8]):
                        old_ending = re.search(r'\w+(?=\-)', index[8]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[8]).group()
                        word_tvorit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                        print(f'{word_tvorit = }')
                elif index[9] != None:               # Предложный
                    if re.findall(r'\+', index[9]):
                        new_ending = re.search(r'(?<=\+)\w+', index[9]).group()
                        word_predl = word + new_ending
                    elif re.findall(r'-', index[9]):
                        old_ending = re.search(r'\w+(?=\-)', index[9]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[9]).group()
                        word_predl = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(rf'({index[2]})$', word) and re.findall(r'(?i)(жен)', index[3]) and re.findall(r'(?i)(жен)', rod):
                if index[4] != None:               # Именительный
                    if re.findall(r'\+', index[4]):
                        new_ending = re.search(r'(?<=\+)\w+', index[4]).group()
                        word_imenit = word + new_ending
                    elif re.findall(r'-', index[4]):
                        old_ending = re.search(r'\w+(?=\-)', index[4]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[4]).group()
                        word_imenit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[5] != None:               # Родительный
                    if re.findall(r'\+', index[5]):
                        new_ending = re.search(r'(?<=\+)\w+', index[5]).group()
                        word_rodit = word + new_ending
                    elif re.findall(r'-', index[5]):
                        old_ending = re.search(r'\w+(?=\-)', index[5]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[5]).group()
                        word_rodit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[6] != None:               # Дательный
                    if re.findall(r'\+', index[6]):
                        new_ending = re.search(r'(?<=\+)\w+', index[6]).group()
                        word_datel = word + new_ending
                    elif re.findall(r'-', index[6]):
                        old_ending = re.search(r'\w+(?=\-)', index[6]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[6]).group()
                        word_datel = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[7] != None:               # Винительный
                    if re.findall(r'\+', index[7]):
                        new_ending = re.search(r'(?<=\+)\w+', index[7]).group()
                        word_vinit = word + new_ending
                    elif re.findall(r'-', index[7]):
                        old_ending = re.search(r'\w+(?=\-)', index[7]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[7]).group()
                        word_vinit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[8] != None:               # Творетельный
                    if re.findall(r'\+', index[8]):
                        new_ending = re.search(r'(?<=\+)\w+', index[8]).group()
                        word_tvorit = word + new_ending
                        print(f'{word_tvorit = }')
                    elif re.findall(r'-', index[8]):
                        old_ending = re.search(r'\w+(?=\-)', index[8]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[8]).group()
                        word_tvorit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                        print(f'{word_tvorit = }')
                elif index[9] != None:               # Предложный
                    if re.findall(r'\+', index[9]):
                        new_ending = re.search(r'(?<=\+)\w+', index[9]).group()
                        word_predl = word + new_ending
                    elif re.findall(r'-', index[9]):
                        old_ending = re.search(r'\w+(?=\-)', index[9]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[9]).group()
                        word_predl = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif f'{index[2]}' == 'sogl' and re.findall(rf'({sogl})$', word) and re.findall(r'(?i)(муж)', index[3]) and re.findall(r'(?i)(муж)', rod):
                if index[4] != None:               # Именительный
                    if re.findall(r'\+', index[4]):
                        new_ending = re.search(r'(?<=\+)\w+', index[4]).group()
                        word_imenit = word + new_ending
                    elif re.findall(r'-', index[4]):
                        old_ending = re.search(r'\w+(?=\-)', index[4]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[4]).group()
                        word_imenit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[5] != None:               # Родительный
                    if re.findall(r'\+', index[5]):
                        new_ending = re.search(r'(?<=\+)\w+', index[5]).group()
                        word_rodit = word + new_ending
                    elif re.findall(r'-', index[5]):
                        old_ending = re.search(r'\w+(?=\-)', index[5]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[5]).group()
                        word_rodit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[6] != None:               # Дательный
                    if re.findall(r'\+', index[6]):
                        new_ending = re.search(r'(?<=\+)\w+', index[6]).group()
                        word_datel = word + new_ending
                    elif re.findall(r'-', index[6]):
                        old_ending = re.search(r'\w+(?=\-)', index[6]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[6]).group()
                        word_datel = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[7] != None:               # Винительный
                    if re.findall(r'\+', index[7]):
                        new_ending = re.search(r'(?<=\+)\w+', index[7]).group()
                        word_vinit = word + new_ending
                    elif re.findall(r'-', index[7]):
                        old_ending = re.search(r'\w+(?=\-)', index[7]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[7]).group()
                        word_vinit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                elif index[8] != None:               # Творетельный
                    if re.findall(r'\+', index[8]):
                        new_ending = re.search(r'(?<=\+)\w+', index[8]).group()
                        word_tvorit = word + new_ending
                        print(f'{word_tvorit = }')
                    elif re.findall(r'-', index[8]):
                        old_ending = re.search(r'\w+(?=\-)', index[8]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[8]).group()
                        word_tvorit = re.sub(rf'({old_ending})$', rf'{new_ending}', word)
                        print(f'{word_tvorit = }')
                elif index[9] != None:               # Предложный
                    if re.findall(r'\+', index[9]):
                        new_ending = re.search(r'(?<=\+)\w+', index[9]).group()
                        word_predl = word + new_ending
                    elif re.findall(r'-', index[9]):
                        old_ending = re.search(r'\w+(?=\-)', index[9]).group()
                        new_ending = re.search(r'(?<=\-)\w+', index[9]).group()
                        word_predl = re.sub(rf'({old_ending})$', rf'{new_ending}', word)

            elif re.findall(r'(.)$', word) != f'{index[2]}':
                word_imenit = word

    declensions_word = {'Иментельный': word_imenit,
                        'Родительный': word_rodit,
                        'Дательный': word_datel,
                        'Винительный': word_vinit,
                        'Творительный': word_tvorit,
                        'Предложный': word_predl
                        }

    return declensions_word












declension(text, index_tab)