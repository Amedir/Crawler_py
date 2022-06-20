from __future__ import print_function
from random import sample
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from pandas import read_csv
import os.path
import requests
import json 
import time
import pandas as pd

#Getting data from table
gsheetid = "18meNsxfrJAg108IhsGJGHJ8iovn_ZN-k7OOCjKaITV4"
sheet_name = ""
gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, sheet_name)
df = pd.read_csv(gsheet_url)

#Cleaning data
col_str_dic = {column:str for column in list(df)}
df = pd.read_csv(gsheet_url, dtype = col_str_dic)
s_array = df["name"]
driver = webdriver.Chrome(executable_path=r'C:\workspace\PD\Crawler\chromedriver.exe')

for i in range(len(s_array)):
    bla = str(s_array[i])


#Opening page
    driver.get('https://cnpjs.rocks')
    
#first Testing
    try:
        print('testando-1')
        teste = driver.find_element_by_xpath('/html/body/h1').text
        firtre = teste[0]
    except:
#First test ok
        print('passou-1')
        driver.find_element_by_xpath('/html/body/div[1]/form/h3/input[1]').send_keys(bla)
        driver.find_element_by_xpath('/html/body/div[1]/form/h3/input[2]').click()
        time.sleep(2)
        pass
    else:
        print('nnpassou-1')
        if firtre == "S":
            while firtre == "S":
                time.sleep(60)
                teste = driver.find_element_by_xpath('/html/body/h1').text
                firtre = teste[0]
                print(firtre)
                driver.find_element_by_xpath('/html/body/form/h3/input[1]').send_keys(bla)
                driver.find_element_by_xpath('/html/body/form/h3/input[2]').click()
        else:
            time.sleep(60)
            teste = driver.find_element_by_xpath('/html/body/h1').text
            firtre = teste[3]
            print(firtre)
            driver.find_element_by_xpath('/html/body/form/h3/input[1]').send_keys(bla)
            driver.find_element_by_xpath('/html/body/form/h3/input[2]').click()
        


#Second Testing
    try:
        teste = driver.find_element_by_xpath('/html/body/h1').text
        print(firtre)
        time.sleep(10)
        print('a')
        driver.find_element_by_xpath('/html/body/form/h3/input[1]').send_keys(bla)
        driver.find_element_by_xpath('/html/body/form/h3/input[2]').click()
    except:
#Second test ok
        driver.find_element_by_xpath('//*[@id="content"]/ul/li[1]/a[1]').click()
        time.sleep(2)
        pass
    else:
        time.sleep(10)
        driver.find_element_by_xpath('/html/body/form/h3/input[1]').send_keys(bla)
        driver.find_element_by_xpath('/html/body/form/h3/input[2]').click()

    try:
        numero = driver.find_element_by_xpath('//*[@id="content"]/li[1]/a[1]').text
    except:
        numero = ''
    try:
        email = driver.find_element_by_xpath('//*[@id="content"]/li[3]/a[1]').text
    except:
        email =''
    time.sleep(5)
    try:
        addres = driver.find_element_by_xpath('//*[@id="content"]/h3[2]').text
    except:
        addres=''
    try:
        cnpj = driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr[1]/td[2]').text
    except:
        cnpj=''
    print(bla, cnpj)
    time.sleep(40)
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1pH9TYM2GQAR55ji0p3EluNYUZ_M2Me7b84DkJA1m-Is'
    # def main():
    #     creds = None
    
    #     if os.path.exists('token.json'):
    #         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    #     #If there are no (valid) credentials available, let the user log in.
    #     if not creds or not creds.valid:
    #         if creds and creds.expired and creds.refresh_token:
    #             creds.refresh(Request())
    #         else:
    #             flow = InstalledAppFlow.from_client_secrets_file(
    #                 'client_secret.json', SCOPES)
    #             creds = flow.run_local_server(port=0)
    #         #Save the credentials for the next run
    #         with open('token.json', 'w') as token:
    #             token.write(creds.to_json())
    
    #     service = build('sheets', 'v4', credentials=creds)
    #         #Call the Sheets API
    #     sheet = service.spreadsheets()
    #         #result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=SAMPLE_RANGE_NAME).execute()
    #         #values = result.get('values', [])
    #     valores_adicionar = [[numero[i], email[i], addres[i], cnpj[i]]]
    #     SAMPLE_RANGE_NAME = 'Pagina1!A:R'
    #     #result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption="RAW", body={"values":valores_adicionar}).execute()
        
    # if __name__ == '__main__':
    #     main() 