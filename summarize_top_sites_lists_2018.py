#Modificado a 2018

import os
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def clean_filename(url):
    # Remover caracteres no permitidos en nombres de archivos
    clean_url = re.sub(r'[<>:"/\\|?*]', '_', url)
    return clean_url

screenshots_folder='cookies_screenshots'
if not os.path.isdir(screenshots_folder):
    os.makedirs(screenshots_folder)

if not os.path.exists("HTML"):
    os.makedirs("HTML")

eu_screenshots=screenshots_folder+os.sep+'eu_sites_from_inside_eu_2022'
if not os.path.isdir(eu_screenshots):
    os.makedirs(eu_screenshots)
    
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.maximize_window()

root='semrush_2024'
semrush_files=[]
for path, subdirs, files in os.walk(root):
    for name in files:
        if name.endswith('.csv'):
            semrush_files.append(os.path.join(path, name))

df=pd.DataFrame()

screenshot_list=eu_screenshots+os.sep+'screenshots_eu.csv'
error_list=eu_screenshots+os.sep+'error_eu.csv'
with open(error_list,'a') as f:
    f.write('')        
with open(screenshot_list,'a') as f:
    f.write('website, cookies?\n')
    


for file in semrush_files:
    df_temp = pd.read_csv(file)

    df = pd.concat([df, df_temp], ignore_index=True)

if 'id' in df.columns:
    unique_websites = list(set(df['id']))
else:
    print("Column 'id' does not exist in DataFrame")
    unique_websites = []    
i=0
for site in unique_websites:
    i=i+1
    shot_name=eu_screenshots+os.sep+site+'.png'
    print(i,site)
    if not os.path.exists(shot_name):
        appender='https://web.archive.org/web/20180000000000/'
        if 'http' not in site:
            appender+='http://'
        if 'www' not in site:
            appender+='www.'
        call_site=appender+site
        try:
            driver.get('%s' %call_site)
        except WebDriverException:
            print('error in %s' %site)
            with open(error_list,'a') as f:
                f.write('%s\n'%site)
            continue

        time.sleep(7)
        driver.save_screenshot(shot_name)
        if site == unique_websites[-1]:
            with open(screenshot_list,'a') as f:
                f.write('%s,' %site)
        else:
            with open(screenshot_list,'a') as f:
                f.write('%s,\n' %site)
    ##        
    url = driver.current_url
    html = driver.page_source
    filename = clean_filename(url) + ".html"
    with open(os.path.join("HTML", filename), "w", encoding="utf-8") as file1:
        file1.write(html)
