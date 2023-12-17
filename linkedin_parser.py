# %%
# from selenium_stealth import stealth
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from seleniumbase import Driver
from bs4 import BeautifulSoup

from csv import writer
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
from dateutil.parser import parse

# %%
import config
my_email = config.email
my_password = config.password
linkedin_link = config.linkedin_link

# %%
# need to add check about internet connection.

# %%
start_time = datetime.now() 
print('Start time: ', start_time)

# %%
# driver = uc.Chrome(use_subprocess=True), headless = True)
# driver = uc.Chrome(use_subprocess=True)
driver = Driver(uc=True)
# detection test
# driver.get('https://nowsecure.nl')
driver.get(url = 'https://www.linkedin.com/login')
WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.ID, "username")))
driver.find_element(By.ID, "username").send_keys(my_email)
time.sleep(1)
driver.find_element(By.ID, "password").send_keys(my_password)
print('login and pass placed')
time.sleep(1)
driver.find_element(By.CLASS_NAME, "login__form_action_container ").click()
print('login ready')
# work long time


# %%
# open link
try:
    driver.get(url = f'https://www.linkedin.com/dashboard/')
    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.CLASS_NAME, 'pcd-analytics-view-item')))

    # profile page base numbers
    score = driver.find_elements(By.CLASS_NAME, 'pcd-analytics-view-item')

    impressions = score[0].text.split('\n')[0]
    print(impressions, 'post impressions past 7 days(?)')

    followers = score[1].text.split('\n')[0].replace(",", "")
    print(followers, 'total followers') 

    views = score[2].text.split('\n')[0] 
    print(views, 'profiles viewers past 90 days')

    searchs = score[3].text.split('\n')[0] 
    print(searchs, 'search appearances previous week') 
except:
    print('analytics page have problems')


# %%
driver.get(url = 'https://www.linkedin.com/analytics/search-appearances/')
WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.CLASS_NAME, 'member-analytics-addon-bar-chart__row')))
time.sleep(1)

# search period parsing
try:
    search_period = driver.find_element(By.CLASS_NAME, 'member-analytics-addon-analytics-view__subtitle').text
    dt1 = parse(search_period.split('between ')[1].split(' - ')[0])
    dt2 = parse(search_period.split('between ')[1].split(' - ')[1].split('.')[0])
    if dt1 > dt2:
        dt1 = dt1 - relativedelta(years = 1)
    print('Search period: ', dt1, ' - ', dt2)
    print('-----------------\n')
except:
    print('No search period or problems with search period')
    print('-----------------\n')

try: 
    keywords = []
    score = driver.find_elements(By.CLASS_NAME, 'member-analytics-addon__cta-list-item')
    for i in score:
        print(i.text)
        keywords.append(i.text)
    print('-----------------\n')
except:
    print('No keywords or problems with keywords')
    print('-----------------\n')

pattern = re.compile(r'\b\b\d{1,2}.\d{1,2}%')
pattern2 = re.compile(r'\b\b\d{1,2}%')
companies_list = []
job_titles_list = []

try:
    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.CLASS_NAME, 'member-analytics-addon-bar-chart__row')))
    score = driver.find_elements(By.CLASS_NAME, 'member-analytics-addon-bar-chart__row')
    for i in score:
        if pattern.findall(i.text) or pattern2.findall(i.text):
            job_titles_list.append(i.text)
        else:
            companies_list.append(i.text)
    print(job_titles_list)
    print(companies_list)
    print('-----------------\n')
except:
    print('No companies or problems with companies')
    print('-----------------\n')

# %%
driver.get(url = 'https://www.linkedin.com/sales/ssi')
# WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
try:
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "content-main")))
    print('ssi page downloaded')
except:
    print('element for check was not found')

soup = BeautifulSoup(driver.page_source, 'html')
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
List = [script_time, views, impressions, searchs, index, brand, find_people, engage, relationships, people_industry, people_network, industry_ssi_rank, network_ssi_rank, keywords,companies_list, job_titles_list, dt1, dt2, followers]

# %%
print(List)

# %%
with open('linkedin_parsing_results.csv', 'a', encoding='utf-8') as f_object:
 
    writer_object = writer(f_object)
    writer_object.writerow(List)
    f_object.close()

# %%
driver.quit()

# %%
# df = pd.read_csv('linkedin_parsing_results.csv')
# df.tail()


# %%


# %%



