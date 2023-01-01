# %%
import time
import undetected_chromedriver as uc
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import config

from csv import writer
import pandas as pd
from datetime import datetime
import re

# %%
start_time = datetime.now() 
print('Start time: ', start_time)

# %%
driver = uc.Chrome(use_subprocess=True, headless = True)
# detection test
# driver.get('https://nowsecure.nl')
driver.get(url = 'https://www.linkedin.com/login')
WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.ID, "username")))
driver.find_element(By.ID, "username").send_keys('andrey.shivalin@phystech.edu')
driver.find_element(By.ID, "password").send_keys('andrey9012')
driver.find_element(By.CLASS_NAME, "login__form_action_container ").click()
# work long time


# %%
driver.get(url = 'https://www.linkedin.com/in/andrey-shivalin/')
WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.CLASS_NAME, 'pvs-list__item--three-column')))

# profile page base numbers
score = driver.find_elements(By.CLASS_NAME, 'pvs-list__item--three-column')
views = score[0].text.split(' ')[0]
print(views, 'profile views, in 90 days') 
impressions = score[1].text.split(' ')[0]
print(impressions, 'post impressions, all time(?)')
searchs = score[2].text.split(' ')[0] 
print(searchs, 'search appearances, for 7 days, which days(?)') 

# %%
driver.get(url = 'https://www.linkedin.com/analytics/search-appearances/')
WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.CLASS_NAME, 'member-analytics-addon__cta-list-item')))

keywords = []
score = driver.find_elements(By.CLASS_NAME, 'member-analytics-addon__cta-list-item')
for i in score:
    print(i.text)
    keywords.append(i.text)
print('-----------------\n')

pattern = re.compile(r'\b\b\d.\d%')
companies_list = []
job_titles_list = []

score = driver.find_elements(By.CLASS_NAME, 'member-analytics-addon-bar-chart__row')
for i in score:
    print(i.text)
    if pattern.findall(i.text):
        job_titles_list.append(i.text)
    else:
        companies_list.append(i.text)
print('-----------------\n')


# %%
driver.get(url = 'https://www.linkedin.com/sales/ssi')
# WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
try:
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "content-main")))
    print('ssi page downloaded')
except:
    print('element for check was not found')

soup = BeautifulSoup(driver.page_source, 'lxml')
intro = soup.find_all('span', {'class': 'ssi-score__value block mb-3 t-black t-light'})

index = intro[0].get_text(strip = True)
print(index, ' - Current Social Selling Index')

brand = intro[1].get_text(strip = True)
print(brand, ' - Establish your professional brand')

find_people = intro[2].get_text(strip = True)
print(find_people, ' - Find the right people')

engage = intro[3].get_text(strip = True)
print(engage, ' - Engage with insights')

relationships = intro[4].get_text(strip = True)
print(relationships, ' - Build relationships')
print()

people_industry = intro[5].get_text(strip = True)
print(people_industry, ' - People in your industry')
people_network = intro[6].get_text(strip = True)
print(people_network, ' - People in your network')
print()

intro = soup.find_all('div', {'class': 'ssi-rank ssi-report__container group-scores-count--2 container-plain flex flex-1'})
industry_ssi_rank = intro[0].find_all("span")[1].get_text(strip = True)
print(industry_ssi_rank, ' - Top % Industry SSI rank')

network_ssi_rank = intro[1].find_all("span")[1].get_text(strip = True)
print(network_ssi_rank, ' - Top % Network SSI rank')



# %%
script_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
print(script_time)
print('script execution time ',datetime.now() - start_time)

# %%
List = [script_time, views, impressions, searchs, index, brand, find_people, engage, relationships, people_industry, people_network, industry_ssi_rank, network_ssi_rank, keywords,companies_list, job_titles_list]

# %%
with open('linkedin_parsing_results.csv', 'a') as f_object:
 
    writer_object = writer(f_object)
    writer_object.writerow(List)
    f_object.close()

# %%
driver.quit()

# %%
# df = pd.read_csv('linkedin_parsing_results.csv')
# df.head()


# %%



