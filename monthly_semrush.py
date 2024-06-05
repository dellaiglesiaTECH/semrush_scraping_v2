'''2. Script that fetches URLs and countries from existing <country>.csv
files with format (category,url) and obtains the intel from the url, then
saves it to a new csv that has the ranked websites for the country+category
'''

import datetime
import os
import pandas as pd
from selenium import webdriver
import regex
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import json


def fetching_intel_from_json_in_link(driver,link):
    driver.get(link)
    time.sleep(5)
    try:
        source_data = driver.page_source
        bs_data = bs(source_data, 'html.parser')
        ## pattern to find json within webpage
        pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')

        all_jsons_text=pattern.findall(str(bs_data))
        for i in range(len(all_jsons_text)):
            if "id" in all_jsons_text[i] and "visits" in all_jsons_text[i] and "bounce_rate" in all_jsons_text[i]:
                ranking_json_loc=i
                print(i)
        if '\\u0022' in all_jsons_text[ranking_json_loc]:
            rankings_json=json.loads(all_jsons_text[ranking_json_loc].replace('\\u0022','"').replace('\\u002D','-'))
            ranking_domains=rankings_json['domains']
        else:
            rankings_json=json.loads(all_jsons_text[ranking_json_loc])
            ranking_domains=rankings_json['props']['pageProps']['page']['domains']
        print('\n\n\n\n','*'*50)
        print(ranking_domains)
        df=pd.DataFrame(ranking_domains)
        print(df)
        return(df)
    except:
        print('problem getting the page')



options = webdriver.ChromeOptions()        
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
folder='2022_10_semrush_fetcher_current_month'
entries = os.listdir(folder)[33]
print(entries)
historical_folder='semrush_2024_2'
scraped_pages='scraped.csv'
failed_pages='failed.csv'
scraped_pages_path=historical_folder+os.sep+scraped_pages
failed_pages_path=historical_folder+os.sep+failed_pages
print('scraped pages path: %s'%(scraped_pages_path))
if not os.path.isdir(historical_folder):
    os.makedirs(historical_folder)
print(entries)
for entry in entries:
    if entry.endswith('.csv'):
        file=folder+os.sep+entry
        print(file)
        df=pd.read_csv(file,header=None)
        print(df)
        country_folder=historical_folder+os.sep+entry.split('.')[0]
        if not os.path.isdir(country_folder):
            os.makedirs(country_folder)
        for i in range(len(df)):
            category=df.iloc[i,0]
            link=df.iloc[i,1]
            category_folder=country_folder+os.sep+category
            if not os.path.isdir(category_folder):
                os.makedirs(category_folder)
                
            try:
                file_path=category_folder+os.sep+'intel.csv'
                print(file_path)
                df_topSites=fetching_intel_from_json_in_link(driver,link)
                df_topSites.to_csv(file_path,index=False)
                with open(scraped_pages_path,'a') as f:
                    f.write('%s,%s\n'%(entry.split('.')[0],category))
            except:
                with open(failed_pages_path,'a') as f:
                    f.write('%s,%s\n'%(entry.split('.')[0],category))

