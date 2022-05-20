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

doc = DocxTemplate(f'data/Адм иск на невозбуждение.docx')
# context = { 'test' : "ПЕРВЫЙ ТЕСТ",
#             'test2' : "ВТОРОЙ ТЕСТ",
#             'test3' : "ТРЕТИЙ ТЕСТ"}
# doc.render(context)
# doc.save(f'data/Адм иск на невозбуждение_test.docx')

morph = pymorphy3.MorphAnalyzer()

# text = 'Петросян Лейла Кареновна'
# text = 'Петросян Карен Радикович'
text = 'Айрапетян Егише Павелович'
# text = 'Пушкин-Суворов Карен Радикович'
# text = 'Суд Петровского района'
# text = 'Мировой Судья г. Пятигорска'

split_text = text.split()



def one_word():
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

def some_word():
    y = []
    for x in split_text:
        if 'masc' in morph.tag(x)[0]:
            letter2 = morph.parse(x)[0].inflect({'ablt', 'masc'}).word
            s = letter2.title()
        elif 'femn' in morph.tag(x)[0]:
            letter2 = morph.parse(x)[0].inflect({'ablt', 'femn'}).word
            s = letter2.title()
        else:
            s = x

        y.append(s)
    print(' '.join(y))




def declension_by_case(index, word):
    context = {f'{index}': f'{word}',
               f'{index}_ро': f'{word}',
               f'{index}_да': f'{word}',
               f'{index}_ви': f'{word}',
               f'{index}_тв': f'{word}',
               f'{index}_пр': f'{word}'}
    doc.render(context)

some_word()
# two_word()
# one_word()