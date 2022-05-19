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


'''
import pymorphy3
from docxtpl import DocxTemplate

# doc = DocxTemplate(f'data/Адм иск на невозбуждение.docx')
# context = { 'test' : "ПЕРВЫЙ ТЕСТ",
#             'test2' : "ВТОРОЙ ТЕСТ",
#             'test3' : "ТРЕТИЙ ТЕСТ"}
# doc.render(context)
# doc.save(f'data/Адм иск на невозбуждение_test.docx')

morph = pymorphy3.MorphAnalyzer()

# text = 'Петросян Лейла Кареновна'
# text = 'Петросян Карен Радикович'
# text = 'Суд Петровского района'
text = 'Мировой Судья г. Пятигорска'
split_text = text.split()

def name_db():
    y = []
    for x in split_text:
        letter2 = morph.parse(x)[0]
        z = letter2.inflect({'ablt', 'masc'}).word
        s = z.title()

        y.append(s)
    print(' '.join(y))

def tribun_db():
    y = []
    x = 2
    if x == 2:
        for x in split_text[0:x]:
            letter3 = morph.tag(x)
            if 'femn' in morph.tag(x)[0]:
                letter2 = morph.parse(x)[0]
                z = letter2.inflect({'ablt', 'masc'}).word
                s = z.title()
                y.append(s)
            elif 'ms-f' in morph.tag(x)[0]:
                letter2 = morph.parse(x)[0]
                z = letter2.inflect({'ablt'}).word
                s = z.title()
                y.append(s)


    print(' '.join(y))

tribun_db()