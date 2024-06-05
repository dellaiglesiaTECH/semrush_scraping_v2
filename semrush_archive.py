##script that scrapes semrush to obtain list of countries and list of categories for top visited websites

import pandas as pd
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


##def obtain_countries_categories():
##  installing webdriver
#driver = webdriver.Chrome(ChromeDriverManager().install())
csv_file = "datos_semrush_2022.csv"
options = webdriver.ChromeOptions()        
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
##    opening website 2021
#driver.get('https://web.archive.org/web/20211028184132/www.semrush.com/website/top/')
##    opening website 2022
driver.get('https://web.archive.org/web/20221113002510/https://www.semrush.com/website/top/')
time.sleep(10)
##  clicking on drop down menu for countries and extracting list of countries
driver.find_element(By.XPATH,'//*[@id="root"]/div/div[5]/div/section/div/div[1]/div[1]').click()
time.sleep(10)
countries_driver=driver.find_elements(By.XPATH,'//*[@id="2"]/div[3]/div/div/div/div[1]/div')
##  obtaining all existing countries in list format adding global to list
countries=countries_driver[0].text.split('\n')[1:]
print(countries)
##  closing countries drop down menu
driver.find_element(By.XPATH,'//*[@id="root"]/div/div[5]/div/section/div/div[1]/div[1]').click()
time.sleep(5)
##  clicking on drop down menu for categories and extracting list of categories
driver.find_element(By.XPATH,'//*[@id="root"]/div/div[5]/div/section/div/div[1]/div[2]').click()
categories_driver=driver.find_elements(By.XPATH,'//*[@id="2"]/div[3]/div/div/div/div[1]/div')
##  obtaining all existing countries in list format and adding generic category to list

categories=categories_driver[0].text.split('\n')[1:]
print(categories)
mon_year=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[6]/div[1]/h1').text.split(', ')[1]
##ranking=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[5]/section/table/tbody').text.split('\n') 
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