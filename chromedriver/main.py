from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import schedule
import os

from pprint import pprint
c = 1
# a, b, = 1, 1
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1OOLAh2DSnPdHEQG2gj_AW86KDSNbYDCXJ4sfbClb8rg'
# spreadsheet_id = '1TCW2UXCQImCHOPv-Dq_B7JA7lFkW-G_WSpUWp8tqNlU' # таблица Артема

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("C:\\Users\\gumeo\\Desktop\\шлак\\коддинг\\selenium\\chromedriver\\chromedriver.exe"), options=chrome_options)


# driver = webdriver.Chrome(service=Service("C:\\Users\\gumeo\\Desktop\\шлак\\коддинг\\selenium\\chromedriver\\chromedriver.exe"), options=options)


def accept_all():
    sleep(10)
    cookies_accept = driver.find_element(by=By.ID, value="onetrust-accept-btn-handler").click()
    close_window = driver.find_element(by=By.CLASS_NAME, value="css-1pcqseb").click()

def set_amount(amount):
    amount_input = driver.find_element(by=By.ID, value="C2Csearchamount_searchbox_amount")
    amount_input.clear()
    amount_input.send_keys(str(amount))

    button = driver.find_element(by=By.ID, value="C2Csearchamount_btn_search").click()


def get_fiat_UZS():
    global c
    url_fiat = "https://p2p.binance.com/ru/trade/all-payments/USDT?fiat=UZS"
    try:
        driver.get(url=url_fiat)
        if c == 1:
            accept_all()
            c = 0
        set_amount(40000000)
        sleep(10)
        elem = driver.find_element(by=By.CLASS_NAME, value="css-1m1f8hn").text
        return elem
    except Exception as ex:
        print(ex)


def get_tinkoff_USDT():

    url = "https://p2p.binance.com/ru/trade/sell/USDT?fiat=RUB&payment=Tinkoff"
    try:
        driver.get(url=url)
        # accept_all()
        set_amount(300000)
        sleep(10)
        elem = driver.find_element(by=By.CLASS_NAME, value="css-1m1f8hn").text
        return elem
    except Exception as ex:
        print(ex)

# def get_tinkoff_BTC():
#     url = "https://p2p.binance.com/ru/trade/sell/BTC?fiat=RUB&payment=Tinkoff"
#     try:
#         driver.get(url=url)
#         # accept_all()
#         set_amount(100000)
#         sleep(10)
#         elem = driver.find_element(by=By.CLASS_NAME, value="css-1m1f8hn").text
#         return elem
#     except Exception as ex:
#         print(ex)

def work():
    # global a, b
    driver = webdriver.Chrome(service=Service("C:\\Users\\gumeo\\Desktop\\шлак\\коддинг\\selenium\\chromedriver\\chromedriver.exe"), options=options)
    fiat_uzs = get_fiat_UZS()
    tinkoff_USDT = get_tinkoff_USDT()
    # tinkoff_BTC = get_tinkoff_BTC()
    print("фиат UZS --",fiat_uzs)
    print("тиньк USDT --", tinkoff_USDT)
    # print("тиньк BTC --", tinkoff_BTC)
    driver.close()
    driver.quit()
    
    values = service.spreadsheets().values().batchUpdate(   
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {'range':"Калькуляторы!A"+str(a)+":A"+str(a),
            "majorDimension": "ROWS",
            "values": [[float(fiat_uzs.replace(',', ''))]]},
            {'range':"Калькуляторы!B"+str(b)+":B"+str(b),
            "majorDimension": "ROWS",
            "values": [[float(tinkoff_USDT.replace(',', ''))]]}
        ]
        }
    ).execute()
    # a += 1
    # b += 1
    # print(values)

schedule.every(1).minutes.do(work)

while 1:
    schedule.run_pending()
    sleep(10)
