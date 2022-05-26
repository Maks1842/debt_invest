'''
!!!ОСНОВНОЙ МОДУЛЬ ДЛЯ ПАРСИНГА ЕСИА!!!

Парсинга сайта Госуслуги.
Раздел ФССП - сведения о наличие ИП.

Авторизация с помощью selenium, парсинг - BeautifulSoup
'''
import os
import logging

import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys     # Модуль для нажатия кнопки (например при авторизации)
from config import *
import time
from datetime import date
import datetime
import csv


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

current_date = date.today()
today_log = current_date.strftime("%d-%m-%Y_%H-%M-%S")
logging.basicConfig(filename=f'example_{today_log}.log', filemode='w', level=logging.INFO)


def select_from_reestr_tab():
    try:
        cursor.execute('''SELECT fio FROM reestr_230522_di;''')
        reestr_tab = cursor.fetchall()

        fedresurs_bankrot(reestr_tab)

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL 1', _ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def fedresurs_bankrot(list_name):

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36")

    # options.add_argument('--headless')     # Бот работает в фоновом режиме

    driver = webdriver.Chrome(
        executable_path="/media/maks/Новый том/Python/work/esia_fssp/webdriver/chromedriver_linux64/chromedriver",
        options=options
    )
    driver.implicitly_wait(60)

    try:
        driver.get("https://bankrot.fedresurs.ru/bankrupts")
        print('start')
        time.sleep(5)

        # list_name = list_name[432:]        # Если необходимо возобновить с указанного места, COUNT также необходимо увеличить

        print(len(list_name))
        create_file()
        count = 0
        for name in list_name:
            count += 1
            result = []
            result_non = []
            xpath_input_box = '//input[@class="ng-untouched ng-valid ng-dirty"]'
            driver.find_element(By.XPATH, xpath_input_box).clear()   # очистить поле
            driver.find_element(By.XPATH, xpath_input_box).send_keys(name)
            time.sleep(0.5)
            driver.find_element(By.XPATH, xpath_input_box).send_keys(Keys.ENTER)
            time.sleep(3)

            page_html = driver.page_source
            if 'tab-content' in page_html:
                xpath_info_block = '//div[@class="not-show-tooltip u-card-result u-card-result_mb-standard"]'
                tab_content = driver.find_elements(By.XPATH, xpath_info_block)
                count1 = 0
                for content in tab_content:
                    xpath_debtor = f'//div[@class="u-card-result__name u-card-result__name_mb u-card-result__name_width"]'
                    debtor = content.find_elements(By.XPATH, xpath_debtor)[count1].text
                    logging.info(f'{count}_{debtor}: Есть инфа')
                    print(f'{count}_{debtor}: Есть инфа')

                    xpath_debtor_address = f'//div[@class="u-card-result__value u-card-result__value_adr"]'
                    debtor_address = content.find_elements(By.XPATH, xpath_debtor_address)[count1].text

                    try:
                        xpath_debtor_inn = f'//div[@class="item-id-wrapper"]/div[1]/span[2]'
                        debtor_inn = content.find_elements(By.XPATH, xpath_debtor_inn)[count1].text
                    except Exception:
                        debtor_inn = '-'

                    try:
                        xpath_debtor_snils = f'//div[@class="item-id-wrapper"]/div[2]/span[2]'
                        debtor_snils = content.find_elements(By.XPATH, xpath_debtor_snils)[count1].text
                    except Exception:
                        debtor_snils = '-'

                    try:
                        xpath_info_case = f'//div[@class="u-card-result__value u-card-result__value_cursor-def u-card-result__value_item-property u-card-result__value_width-item"]'
                        info_case = content.find_elements(By.XPATH, xpath_info_case)[count1].text
                    except Exception:
                        info_case = '-'

                    try:
                        xpath_case_number = f'//div[@class="u-card-result__court-case u-card-result__court-case_mb"]/div[@class="flex-column"]/div[2]'
                        case_number = content.find_elements(By.XPATH, xpath_case_number)[count1].text
                    except Exception:
                        case_number = '-'

                    try:
                        xpath_arbitration_manager = f'//div[@class="u-card-result__manager"]/div[@class="flex-column"]/div[2]'
                        arbitration_manager = content.find_elements(By.XPATH, xpath_arbitration_manager)[count1].text
                    except Exception:
                        arbitration_manager = '-'

                    count1 += 1

                    result.append({
                        # '№ ПП': count + 1,
                        'Должник': debtor,
                        'Адрес регистрации': debtor_address,
                        'ИНН должника': debtor_inn,
                        'СНИЛС должника': debtor_snils,
                        'Судебное производство': info_case,
                        '№ судебного дела': case_number,
                        'Арбитражный управляющий': arbitration_manager})
                save_file(result)

            else:
                debtor = name[0]
                logging.info(f'{count}_{debtor}: НЕТ инфы')
                print(f'{count}_{debtor}: НЕТ инфы')
                debtor_address = '-'
                debtor_inn = '-'
                debtor_snils = '-'

                xpath_info_case = '//div[@class="no-result-msg__header"]'
                info_case = driver.find_element(By.XPATH, xpath_info_case).text
                case_number = '-'
                arbitration_manager = '-'

                result_non.append({
                    # '№ ПП': count + 1,
                    'Должник': debtor,
                    'Адрес регистрации': debtor_address,
                    'ИНН должника': debtor_inn,
                    'СНИЛС должника': debtor_snils,
                    'Судебное производство': info_case,
                    '№ судебного дела': case_number,
                    'Арбитражный управляющий': arbitration_manager})

            save_file(result_non)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()




def create_file():
    current_date = date.today()
    today = current_date.strftime("%d-%m-%Y")
    with open(f'data/fedresurs_bankrot_{today}.csv', 'w') as file:                 # Создаю файл .csv с заголовками
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Должник',
                        'Адрес регистрации',
                        'ИНН должника',
                        'СНИЛС должника',
                        'Судебное производство',
                        '№ судебного дела',
                        'Арбитражный управляющий'])


def save_file(items):
    current_date = date.today()
    today = current_date.strftime("%d-%m-%Y")
    for item in items:
        with open(f'data/fedresurs_bankrot_{today}.csv', 'a') as file:                           #Открываю файл на добавление данных: 'a'
            writer = csv.writer(file)
            writer.writerow([item['Должник'],
                             item['Адрес регистрации'],
                             item['ИНН должника'],
                             item['СНИЛС должника'],
                             item['Судебное производство'],
                             item['№ судебного дела'],
                             item['Арбитражный управляющий']])

def main():
    select_from_reestr_tab()

    # list_name = ['Борисова Ирина Петровна', 'Беликов Руслан Игоревич', 'Нурмагомадов Али Умарович']
    # fedresurs_bankrot(list_name)
    # read_html()

if __name__ == '__main__':
    main()