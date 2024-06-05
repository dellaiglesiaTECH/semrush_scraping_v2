##script that scrapes semrush to obtain list of countries and list of categories for top visited websites

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import csv
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


##def obtain_countries_categories():
##  installing webdriver
options = webdriver.ChromeOptions()        
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
csv_file = "datos_semrush_2024.csv"
##    opening website
driver.get('https://www.semrush.com/website/top/')
time.sleep(10)
##  denying cookies
#driver.find_element(By.XPATH,'/html/body/section/div/div[1]/div[2]/div[1]/button[2]').click()
#time.sleep(10)
##  clicking on drop down menu for countries and extracting list of countries
driver.find_element(By.XPATH,'//*[@id="1"]/div/div[1]').click()

countries_driver=driver.find_elements(By.XPATH,'//*[@id="igc-ui-kit-6-scroll-container"]/div')
time.sleep(10)
##  obtaining all existing countries in list format adding global to list
countries=countries_driver[0].text.split('\n')[1:]
print(countries)
##  closing countries drop down menu
driver.find_element(By.XPATH,'//*[@id="1"]/div/div[1]').click()
time.sleep(5)
##  clicking on drop down menu for categories and extracting list of categories
driver.find_element(By.XPATH,'/html/body/div[1]/main/div/div/div/div/div[5]/section/div/div/div[2]/div/div').click()
categories_driver=driver.find_elements(By.XPATH,'/html/body/div[11]/div[2]/div/div/div/div[2]/div')
##  obtaining all existing countries in list format and adding generic category to list
categories=categories_driver[0].text.split('\n')[1:]
print(categories)
mon_year=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[5]/div[1]/h1').text.split(', ')[1]
print(mon_year)
df = pd.DataFrame({'Month_Year': [mon_year]},{'Categories': [categories]}, {'Countries': [countries]})
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Categories', 'Month_Year', 'Countries'])
        writer.writerow([','.join(categories), mon_year, ','.join(countries)])
    print(f'Se ha creado el archivo CSV: {csv_file}')
else:
    print(f'Ya existe el archivo CSV: {csv_file}, se va a modificar')
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Categories', 'Month_Year', 'Countries'])
        writer.writerow([','.join(categories), mon_year, ','.join(countries)])
