from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1OOLAh2DSnPdHEQG2gj_AW86KDSNbYDCXJ4sfbClb8rg'

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('headless')
options.add_argument('window-size=1920x935')
url = "https://p2p.binance.com/ru/trade/all-payments/USDT?fiat=UZS"

driver = webdriver.Chrome(service=Service("C:\\Users\\gumeo\\Desktop\\шлак\\коддинг\\selenium\\chromedriver\\chromedriver.exe"), options=options)

try:
    driver.get(url=url)
    sleep(10)
    elem = driver.find_element(by=By.CLASS_NAME, value="css-1m1f8hn").text

    print(elem)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

# Чтение файла
values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A1:A1',
    majorDimension='COLUMNS'
).execute()
pprint(values)

# Запись в файл
values = service.spreadsheets().values().batchUpdate(   
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {'range':"A1:A1",
            "majorDimension": "ROWS",
            "values": [[elem]]},
	]
    }
).execute()