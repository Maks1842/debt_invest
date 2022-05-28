'''
!!!ОСНОВНОЙ МОДУЛЬ ДЛЯ ПАРСИНГА ЕСИА!!!

Парсинга сайта Госуслуги.
Раздел ФССП - сведения о наличие ИП.

Авторизация с помощью selenium, парсинг - BeautifulSoup
'''
import os
import logging

import psycopg2
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys     # Модуль для нажатия кнопки (например при авторизации)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    options.add_argument('--headless')     # Бот работает в фоновом режиме

    driver = webdriver.Chrome(
        executable_path="/media/maks/Новый том/Python/work/esia_fssp/webdriver/chromedriver_linux64/chromedriver",
        options=options
    )
    driver.implicitly_wait(10)

    try:
        driver.get("https://bankrot.fedresurs.ru/bankrupts")
        print('start')
        time.sleep(2)

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
            # time.sleep(0.5)
            driver.find_element(By.XPATH, xpath_input_box).send_keys(Keys.ENTER)
            original_window = driver.current_window_handle
            time.sleep(2)
            page_html = driver.page_source
            if 'btn-accept btn-accept_hover btn-accept_properties' in page_html:
                xpath_cookie_disclaimer = '//button[@class="btn-accept btn-accept_hover btn-accept_properties"]'
                driver.find_element(By.XPATH, xpath_cookie_disclaimer).click()

            if 'tab-content' in page_html:
                xpath_info_block = '//div[@class="not-show-tooltip u-card-result u-card-result_mb-standard"]'
                tab_content = driver.find_elements(By.XPATH, xpath_info_block)
                count1 = 0
                for content in tab_content:

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

                    xpath_info_position = '//a[@class="info info_position"]'
                    content.find_elements(By.XPATH, xpath_info_position)[count1].click()
                    # time.sleep(2)
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)

                    # # cookies
                    # cookies = driver.get_cookies()
                    # pickle.dump(cookies, open('cookies.pkl', 'wb'))

                    cookies = pickle.load(open("cookies.pkl", "rb"))
                    for cookie in cookies:
                        driver.add_cookie(cookie)

                    time.sleep(2)


                    xpath_debtor = '//div[@class="subject"]/h2'
                    debtor = driver.find_element(By.XPATH, xpath_debtor).text
                    logging.info(f'{count}_{debtor}: Есть инфа')
                    print(f'{count}_{debtor}: Есть инфа')

                    xpath_debtor_address = '//div[@class="col-9"]'
                    debtor_address = driver.find_element(By.XPATH, xpath_debtor_address).text

                    xpath_debtor_birthday = '//div[@class="mr-3"]'
                    debtor_birthday = driver.find_element(By.XPATH, xpath_debtor_birthday).text

                    xpath_debtor_birthplace = '//div[@class="twert mr-3  taj bPlaceContent"]'
                    debtor_birthplace = driver.find_element(By.XPATH, xpath_debtor_birthplace).text

                    try:
                        xpath_debtor_inn = '//div[@class="df  mb-3"][1]/div[2]'
                        debtor_inn = driver.find_element(By.XPATH, xpath_debtor_inn).text
                    except Exception:
                        debtor_inn = '-'

                    try:
                        xpath_debtor_snils = '//div[@class="df  mb-3"][2]/div[2]'
                        debtor_snils = driver.find_element(By.XPATH, xpath_debtor_snils).text
                    except Exception:
                        debtor_snils = '-'

                    page2_html = driver.page_source
                    if 'Ранее имевшиеся ФИО' in page2_html:
                        xpath_name_old = '//div[@class="row mb-2"]'
                        name_old = driver.find_element(By.XPATH, xpath_name_old).text
                    else:
                        name_old = '-'

                    count1 += 1

                    result.append({
                        'Должник': debtor,
                        'ФИО до изменения': name_old,
                        'Дата рождения': debtor_birthday,
                        'Место рождения': debtor_birthplace,
                        'Адрес регистрации': debtor_address,
                        'ИНН должника': debtor_inn,
                        'СНИЛС должника': debtor_snils,
                        'Судебное производство': info_case,
                        '№ дела о банкротстве': case_number})
                    driver.close()
                    # time.sleep(3)
                    driver.switch_to.window(original_window)

                save_file(result)

            else:
                debtor = name[0]
                logging.info(f'{count}_{debtor}: НЕТ инфы')
                print(f'{count}_{debtor}: НЕТ инфы')
                name_old = '-'
                debtor_birthday = '-'
                debtor_birthplace = '-'
                debtor_address = '-'
                debtor_inn = '-'
                debtor_snils = '-'
                xpath_info_case = '//div[@class="no-result-msg__header"]'
                info_case = driver.find_element(By.XPATH, xpath_info_case).text
                case_number = '-'

                result_non.append({
                    'Должник': debtor,
                    'ФИО до изменения': name_old,
                    'Дата рождения': debtor_birthday,
                    'Место рождения': debtor_birthplace,
                    'Адрес регистрации': debtor_address,
                    'ИНН должника': debtor_inn,
                    'СНИЛС должника': debtor_snils,
                    'Судебное производство': info_case,
                    '№ дела о банкротстве': case_number})

            save_file(result_non)

    except Exception as ex:
        print(f'чтото пошло не так_{ex}')
    finally:
        driver.close()
        driver.quit()


def data_collection():
    pass


def create_file():
    current_date = date.today()
    today = current_date.strftime("%d-%m-%Y")
    with open(f'data/fedresurs_bankrot_{today}.csv', 'w') as file:                 # Создаю файл .csv с заголовками
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Должник',
                         'ФИО до изменения',
                         'Дата рождения',
                         'Место рождения',
                         'Адрес регистрации',
                         'ИНН должника',
                         'СНИЛС должника',
                         'Судебное производство',
                         '№ дела о банкротстве'])


def save_file(items):
    current_date = date.today()
    today = current_date.strftime("%d-%m-%Y")
    for item in items:
        with open(f'data/fedresurs_bankrot_{today}.csv', 'a') as file:                           #Открываю файл на добавление данных: 'a'
            writer = csv.writer(file)
            writer.writerow([item['Должник'],
                             item['ФИО до изменения'],
                             item['Дата рождения'],
                             item['Место рождения'],
                             item['Адрес регистрации'],
                             item['ИНН должника'],
                             item['СНИЛС должника'],
                             item['Судебное производство'],
                             item['№ дела о банкротстве']])

def main():
    select_from_reestr_tab()

    # list_name = ['Абрамов Дмитрий Александрович', 'Баева Галина Александровна', 'Беликов Руслан Игоревич', 'Нурмагомадов Али Умарович']
    # fedresurs_bankrot(list_name)
    # read_html()

if __name__ == '__main__':
    main()