from __future__ import print_function
from lib2to3.pgen2 import driver
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import time
import pandas as pd

#Getting data from table
gsheetid = "1DmTENt26YQzAAqewKWXltD1NoZRRD0KlU8j6pIXAy-o"
sheet_name = ""
gsheet_url = 'https://docs.google.com/spreadsheets/d/{}/edit#gid=1884258144'.format(gsheetid)
url_1 = gsheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(url_1)

#Cleaning data
col_str_dic = {column:str for column in list(df)}
df = pd.read_csv(url_1, dtype = col_str_dic)
nomes_empresas = df["name"]
cnpj_empreasas = df["cnpj"]
phone_empresas = df["bussines_phone"]
email_empresas = df["bussines_email"]

# COnfiguração para o Google Chrome do Heroku
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1DmTENt26YQzAAqewKWXltD1NoZRRD0KlU8j6pIXAy-o'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
    
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
    #Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
#Call the Sheets API
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

for i in range(len(nomes_empresas)):
    nome = str(nomes_empresas[i])
    cnpj = str(cnpj_empreasas[i])
    phone = str(phone_empresas[i])
    email = str(email_empresas[i])
    if cnpj == 'nan':
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get('https://cnpjs.rocks')
        try:
            #Opening page
            time.sleep(5)
            driver.switch_to.window(driver.window_handles[0])
            driver.find_element(by=By.XPATH, value='/html/body/header/form/input[1]').send_keys(nome)
            driver.find_element(by=By.XPATH, value='/html/body/header/form/input[2]').click()
            driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/div/a').click()
            achou = True
        except:
            achou = False
            cnpj = 'Não achou'
            try:
                vqd = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div').text
                if vqd[0] == 'V':
                    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[2]/div/div[1]/div[1]/div/a').click()
                    achou = True
            except:
                try:
                    evd = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div/div[2]').text
                    print(evd)
                    if evd[0] == 'E':
                        driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div/div[2]/a').click()
                        time.sleep(2)
                        driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/div/a').click()
                        achou = True
                except:
                    achou = False
                    cnpj = 'Não achou'
        if achou:
            try:
                time.sleep(5)
                driver.switch_to.window(driver.window_handles[1])
                cnpj = driver.find_element(by=By.XPATH, value='/html/body/div/div[2]/ul[1]/li[1]/strong').text
                driver.close() 

                valores_adicionar = [[cnpj]]
                SAMPLE_RANGE_NAME = 'Empresas Tableau!A'+str(i+2)+':A'+str(i+2)
                result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption="RAW", body={"values":valores_adicionar}).execute()
            except:
                cnpj = 'Não achou'
        print("Nome da empresa: ", nome, " CNPJ: ", cnpj)
        driver.quit()
    if phone == 'nan':
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get('https://cnpjs.rocks')
        try:
            #Opening page
            time.sleep(5)
            driver.switch_to.window(driver.window_handles[0])
            driver.find_element(by=By.XPATH, value='/html/body/header/form/input[1]').send_keys(nome)
            driver.find_element(by=By.XPATH, value='/html/body/header/form/input[2]').click()
            driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/div/a').click()
            achou = True
        except:
            achou = False
            phone = 'Não achou'
            try:
                vqd = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div').text
                if vqd[0] == 'V':
                    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[2]/div/div[1]/div[1]/div/a').click()
                    achou = True
            except:
                try:
                    evd = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div/div[2]').text
                    print(evd)
                    if evd[0] == 'E':
                        driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div/div[2]/a').click()
                        time.sleep(2)
                        driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/div/a').click()
                        achou = True
                except:
                    achou = False
                    phone = 'Não achou'
        if achou:
            try:
                time.sleep(5)
                driver.switch_to.window(driver.window_handles[1])
                phone = driver.find_element(by=By.XPATH, value='/html/body/div/div[2]/ul[5]/li[1]/strong').text
                driver.close()
                valores_adicionar = [[phone]]
                SAMPLE_RANGE_NAME = 'Empresas Tableau!E'+str(i+2)+':E'+str(i+2)
                result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption="RAW", body={"values":valores_adicionar}).execute()
            except:
                phone = 'Não achou'
        print("Nome da empresa: ", nome, " Phone: ", phone)
        driver.quit()
    if email == 'nan':
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get('https://cnpjs.rocks')
        try:
            #Opening page
            time.sleep(5)
            driver.switch_to.window(driver.window_handles[0])
            driver.find_element(by=By.XPATH, value='/html/body/header/form/input[1]').send_keys(nome)
            driver.find_element(by=By.XPATH, value='/html/body/header/form/input[2]').click()
            driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/div/a').click()
            achou = True
        except:
            achou = False
            email = 'Não achou'
            try:
                vqd = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div').text
                if vqd[0] == 'V':
                    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[2]/div/div[1]/div[1]/div/a').click()
                    achou = True
            except:
                try:
                    evd = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div/div[2]').text
                    print(evd)
                    if evd[0] == 'E':
                        driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div/div[2]/a').click()
                        time.sleep(2)
                        driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/p/div/div/div/div/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/div/a').click()
                        achou = True
                except:
                    achou = False
                    email = 'Não achou'
        if achou:
            try:
                time.sleep(5)
                driver.switch_to.window(driver.window_handles[1])
                email = driver.find_element(by=By.XPATH, value='/html/body/div/div[2]/ul[5]/li[2]/strong').text
                driver.close() 

                valores_adicionar = [[email]]
                SAMPLE_RANGE_NAME = 'Empresas Tableau!F'+str(i+2)+':F'+str(i+2)
                result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption="RAW", body={"values":valores_adicionar}).execute()
            except:
                email = 'Não achou'
        print("Nome da empresa: ", nome, " Email: ", email)
        driver.quit()