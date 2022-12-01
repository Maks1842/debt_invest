'''
!!! Тестовый модуль, в боевом режиме не использовал!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

С помощью данного модуля из файла EXCEL извлекаются данные
и через заданные теги вставляются в текст шаблона .DOCX

При необходимости склонения по падежам, слова обрабатываются модулем declensions.py
'''

import re
import time
import pandas
from docxtpl import DocxTemplate

'''
1. Pandas извлекает все данные из excel
2. .iloc - извлекаются данные строки по её номеру
3. Индексам (которые обозначены в шаблоне .docx) присваиваются значения из списка
4. Данные по индексам передаются в шаблон .docx
5. Присваивается имя новому файлу и он сохраняется в указанной директории
'''
def insert_in_doc_pattern():

    excel_data_df = pandas.read_excel('data/30.11.2022/Реестр_тест.xlsx')

    # item = excel_data_df.iloc[0]
    # q = item[1]
    #
    # print(f'{q}')

    z = []
    w = ''
    count = 0


    while not 'stop' in w:

        item = excel_data_df.iloc[count]
        count += 1

        q = item[1]
        w = item[0]
        z.append(q)

        # print(f'{item}')

        debtor = item[1]
        pol = item[2]
        birthday = item[3].strftime('%d.%m.%Y')
        address_debtor = item[14]
        rosp = item[37]
        rosp_address = item[39]
        rosp_region = item[38]
        arbitr = item[42]
        arbitr_address = item[43]
        delo = item[21]
        try:
            delo_date = item[22].strftime('%d.%m.%Y')
        except Exception:
            delo_date = 'б/д'

        dogovor = item[7]
        try:
            dogovor_date = item[8].strftime('%d.%m.%Y')
        except Exception:
            dogovor_date = 'б/д'

        ed = item[24]
        try:
            ed_date = item[25].strftime('%d.%m.%Y')
        except Exception:
            ed_date = 'б/д'

        ed_type = item[20]
        ep = item[32]
        try:
            ep_dateend = item[29].strftime('%d.%m.%Y')
        except Exception:
            ep_dateend = 'б/д'

        ep_comment = item[33]
        summ_cess = item[10]
        summ_od = item[46]
        summ_perсent = item[47]
        percent_on_summ_od = item[49]
        penalty = item[48]

        context = {
                    'Должник': f"{debtor}",
                    'дата_рождения': f"{birthday}",
                    'Адрес_должника': f"{address_debtor}",
                    'РОСП': f"{rosp}",
                    'адрес_РОСП': f"{rosp_address}",
                    'РОСП_регион': f"{rosp_region}",
                    'суд': f"{arbitr}",
                    'адрес_суда': f"{arbitr_address}",
                    'номер_дела': f"{delo}",
                    'дата_дела': f"{delo_date}",
                    'номер_договора': f"{dogovor}",
                    'дата_договора': f"{dogovor_date}",
                    'номер_ИД': f"{ed}",
                    'дата_ИД': f"{ed_date}",
                    'основание_ИД_род': f"{ed_type}",
                    'номер_ИП': f"{ep}",
                    'дата_окончания_ИП': f"{ep_dateend}",
                    'Комментарии_ИП': f"{ep_comment}",
                    'Сумма_цессии': f"{summ_cess}",
                    'остаток_ОД': f"{summ_od}",
                    'остаток_по_процентам': f"{summ_perсent}",
                    'процент_на_од': f"{percent_on_summ_od}",
                    'неустойка': f"{penalty}",

                }

        doc = DocxTemplate(f'data/30.11.2022/Шаблон_1 ПП окон ИП, есть ИЛ.docx')
        doc.render(context)
        doc.save(f"result/ПП окон ИП, есть ИЛ/{debtor}_{dogovor}.docx")

    count_list = []
    data_dict = {}

    # for x in range(330):
    #     count = x+1
    #     count_list.append(count)
    #     dataframe = excel_data_df[count].tolist()
    #
    #     name = dataframe[2]
    #     date = dataframe[4]
    #     web = dataframe[5]
    #     num_person = dataframe[87]
    #     balls = dataframe[7]
    #
    #     # data_dict.update({
    #     #     f"{count}": {
    #     #         'name': name,
    #     #         'date': date,
    #     #         'web': web,
    #     #         'num_person': num_person,
    #     #         'balls': balls}
    #     # })
    #
    #     context = {
    #         'name': f"{name}",
    #         'date': f"{date}",
    #         'num_person': f"{num_person}",
    #         'balls': f"{balls}"
    #     }
    #
    #     name_file = re.sub(r'\"', '', name)
    #
    #     doc = DocxTemplate(f'data/Index шаблон отчета.docx')
    #     doc.render(context)
    #     doc.save(f"result/Отчеты ЧР_обр 2022/Отчет_{name_file}.docx")


insert_in_doc_pattern()