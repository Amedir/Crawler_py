from __future__ import print_function
from random import sample
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import os.path
import requests
import json 
import time
import pandas as pd

#Getting data from table
options = webdriver.ChromeOptions
# options.binary_location = "C:\Users\ademir\AppData\Local\Programs\Opera GX\launcher.exe"
driver = webdriver.Chrome(executable_path=r'C:\Users\ademir\AppData\Local\Programs\Opera GX\launcher.exe')

driver.quit()