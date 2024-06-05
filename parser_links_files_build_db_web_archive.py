'''3. Script that reads csv's of semrush that include all country-category
combination links generated from the main semrush webpage. It browses each
link to find previously archived versions on web.archive.org and generates
the (link, date) combination for each version. It then fetches the intel in
the link as it obtains the ranking of the websites in the archived link
'''

##read files
##create folder historical
##create subfolders: 1/country

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


#finding archived pages for the captured URLs from the current website and getting URLs for
#older pages from web.archive.org
def archived_links_getter(driver,url):
    archive_url='https://web.archive.org/web/20220000000000*/'
    url_to_open='%s%s'%(archive_url,url)

    links=[]
    driver.get(url_to_open)
    archive_years={}
    counter=1
    time.sleep(15)
    if len(driver.find_elements(By.XPATH, '//*[@id="livewebInfo"]/h2')) > 0:
        print('no archived pages found for url: %s' %(url))
        
    else:
        for i in range(1996,2023):
            archive_years[str(i)]=counter
            counter+=1
        try:
            archive_start_year=driver.find_element_by_xpath('//*[@id="react-wayback-search"]/div[2]/span/a[1]').text.split(', ')[1]
            archive_end_year=driver.find_element_by_xpath('//*[@id="react-wayback-search"]/div[2]/span/a[2]').text.split(', ')[1]

            for i in list(archive_years.keys()):
                if i ==archive_start_year:
                    search_start_year=archive_years[i]
                if i ==archive_end_year:
                    search_end_year=archive_years[i]
        except:
            print('years range does not exist... probably only one year')
        try:
            archive_start_year=driver.find_element_by_xpath('//*[@id="react-wayback-search"]/div[2]/a').text.split(', ')[1].split('.')[0]
            archive_end_year=archive_start_year
            for i in list(archive_years.keys()):
                if i ==archive_start_year:
                    search_start_year=archive_years[i]
                    search_end_year=search_start_year
        except:
            print('single year does not exist')

        try:
            for i in range(search_start_year,search_end_year+1):

                print('year: %s'%(i))
                driver.find_element_by_xpath('//*[@id="year-labels"]/span[%s]'%(str(i))).click()
                time.sleep(15)
                print('year clicked')
            
                driver_days=driver.find_elements_by_class_name("calendar-day")
                print('searched for calendar day')
                for _day in driver_days:
                    link_day=_day.find_element_by_tag_name('a').get_attribute('href')
                    print(link_day)
                    links.append(link_day)
        except:
            print('could not fetch page')

    return(links)


def fetching_intel_from_json_in_link(driver,link):
    driver.get(link)
    time.sleep(10)
    try:
        source_data = driver.page_source
        bs_data = bs(source_data, 'html.parser')
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
print("Directorio de trabajo actual:", os.getcwd())
folder='semrush'
entries = os.listdir(folder)
print(entries)
historical_folder='semrush_historical'
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
            archived_links=archived_links_getter(driver,link)
            category_folder=country_folder+os.sep+category
            if not os.path.isdir(category_folder):
                os.makedirs(category_folder)
            for arch_link in archived_links:
                year_month=arch_link.split('web/')[1][:6]
                year=year_month[:4]
                month=year_month[4:]
                try:
                    file_path=category_folder+os.sep+'%s_%s.csv'%(year,month)
                    print(file_path)
                    df_topSites=fetching_intel_from_json_in_link(driver,arch_link)
                    df_topSites.to_csv(file_path,index=False)
                    with open(scraped_pages_path,'a') as f:
                        f.write('%s,%s,%s,%s\n'%(entry.split('.')[0],category,year,month))
                except:
                    with open(failed_pages_path,'a') as f:
                        f.write('%s,%s,%s,%s\n'%(entry.split('.')[0],category,year,month))
