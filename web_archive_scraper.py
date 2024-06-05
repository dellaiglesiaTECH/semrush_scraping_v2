from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import regex
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import json


archive_url='https://web.archive.org/web/20220000000000*/'

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url='https://www.semrush.com/website/top/angola/all'
url_to_open='%s%s'%(archive_url,url)


driver.get(url_to_open)
archive_years={}
counter=1
time.sleep(5)
for i in range(1996,2023):
    archive_years[str(i)]=counter
    counter+=1
##search_start_year=None
##search_end_year=None

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
####clicking on start year
##driver.find_element_by_xpath'//*[@id="year-labels"]/span[%s]'%(search_start_year).click()
##
##driver_days=driver.find_elements_by_class_name("calendar-day")
##
##for _day in driver_days:
##    
##x[0].find_element_by_tag_name('a').get_attribute('href')
##
##
##
####clicking on end year
##driver.find_element_by_xpath'//*[@id="year-labels"]/span[%s]'%(search_end_year).click()

links=[]

delay = 3
for i in range(search_start_year,search_end_year+1):
## clicking on year
    print('year: %s'%(i))
    driver.find_element_by_xpath('//*[@id="year-labels"]/span[%s]'%(str(i))).click()
    time.sleep(15)
    print('year clicked')
## getting archived webpages' links
    driver_days=driver.find_elements_by_class_name("calendar-day")
    print('searched for calendar day')
    for _day in driver_days:
        link_day=_day.find_element_by_tag_name('a').get_attribute('href')
        print(link_day)
        links.append(link_day)
## opening link and fetching data
##        driver.get(link_day)

