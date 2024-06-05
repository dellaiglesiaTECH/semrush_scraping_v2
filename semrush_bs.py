'''1. Script that browses semrush, fetches country+category keys from the
webpage and saves them into a <country>.csv file with the format (category,url).
Another script fetches the intel from the generated <country>.csv
'''
import os
from selenium import webdriver
import regex
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import json

options = webdriver.ChromeOptions()        
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#opening website
driver.get('https://www.semrush.com/website/top/')
##driver.get('https://web.archive.org/web/20220330061430/https://www.semrush.com/website/top/')
##driver.get('https://web.archive.org/web/20211028184132/https://www.semrush.com/website/top/')
time.sleep(10)
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
    categories=rankings_json['categories']
    countries=rankings_json['countries']
else:
    rankings_json=json.loads(all_jsons_text[ranking_json_loc])
    ranking_domains=rankings_json['props']['pageProps']['page']['domains']
    categories=rankings_json['props']['pageProps']['page']['categories']
    countries=rankings_json['props']['pageProps']['page']['countries']
print(categories)
print(countries)
print('\n\n\n\n','*'*50)
print(ranking_domains)

##format: https://www.semrush.com/website/top/argentina/all/
##format: https://www.semrush.com/website/top/<country>/<category>

##
##for i in range(20):
##	print(json.dumps(b['props']['pageProps']['page']['domains'][i],sort_keys=True, indent=4))
##	time.sleep(5)
countries_slug=[]
categories_slug=[]

for i in range(len(countries['list'])):
	countries_slug.append(countries['list'][i]['slug'])
	
for i in range(len(categories['list'])):
	categories_slug.append(categories['list'][i]['slug'])

all_links=[]
countries={}

if not os.path.isdir('semrush'):
    os.makedirs('semrush')

for country in countries_slug:
    country_links=[]
    for category in categories_slug:
        new_link='https://www.semrush.com/website/top/%s/%s'%(country,category)
##        country_links.append('https://www.semrush.com/website/top/%s/%s'%(country,category))
##    countries[country]=country_links
        with open('semrush\\%s.csv'%(country),'a') as f:
            if category==categories_slug[-1]:
                f.write('%s,%s'%(category,new_link))
            else:
                f.write('%s,%s\n'%(category,new_link))
        
    
