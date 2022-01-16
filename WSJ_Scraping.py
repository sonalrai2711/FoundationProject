#!/usr/bin/env python
# coding: utf-8

# In[35]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os 
from bs4 import BeautifulSoup 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import json
import datetime
#!pip install chromedriver-binary==96.0.4664.45.0
import chromedriver_binary  # Adds chromedriver binary to path
import os
from datetime import datetime
import pandas as pd


# In[36]:


# Automate the WSJ.com page
url = 'https://www.wsj.com/news/archive/2020/march'
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome()#(service=s)
driver.get(url)
time.sleep(5)
sign_in_link = driver.find_element(By.LINK_TEXT, 'Sign In')
sign_in_link.click()
driver.find_element(By.ID, 'username').send_keys("george_abraham_ampba2022s@isb.edu")
contWithPass_button = driver.find_element(By.XPATH, '//button[@class="solid-button continue-submit new-design"]/span')
contWithPass_button.click()

# the page does not allow automatic entering of password
# So, entering and clicking 'Submit' button are to be done manually


# In[109]:


# set the query terms
query_terms="microsoft"
query_file_tag=query_terms.replace('%20','_')
# Load the basic query URL

basic_url ="https://www.wsj.com/search?query={}&isToggleOn=true&operator=AND&sort=date-desc&duration=90d&startDate=2018%2F04%2F01&"    "endDate=2021%2F12%2F31&source=wsjarticle%2Cwsjie%2Cwsjsitesrch%2Cautowire%2Capfeed".format(query_terms)

driver.get(basic_url)


# In[ ]:


# find the number of pages in the daily listing
def get_pages(driver):
    page_counter = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                        '//span[contains(@class,"WSJTheme--total-pages--")]')))
    pages_text=  page_counter.get_attribute('innerHTML')
    no_of_pages=str.replace(pages_text,'of ','').strip()
    return int(no_of_pages)


# In[84]:


# write article links to csv file
def write_article_link_rows(rows,query_file_tag):
    file_name = 'D:/AMPBA from ISB/Term 2/FP-1/Group Project/WSJ Scraping/article_links_' + query_file_tag + '.csv'
    
    if os.path.isfile(file_name)==False:
        with open(file_name, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)
            csv_file.close()
    else:
        with open(file_name, 'a', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)
            csv_file.close()


# In[82]:


# Check if the same URL already exists
def article_link_exists(url,query_file_tag):
    result = True
    
    file_name = 'D:/AMPBA from ISB/Term 2/FP-1/Group Project/WSJ Scraping/article_links_' + query_file_tag + '.csv'
    # wsj_search_article_links_tesla_stock
    if os.path.isfile(file_name)==False:
        result = False
    else:
        article_links = pd.read_csv(file_name,header=None)
        headers=['heading','url']
        article_links.columns=headers
        urls = article_links.url.unique()
        result = url in urls
        
    return result


# In[83]:


# Check if the same URL already exists
def article_text_exists(url,query_file_tag):
    result = True
    file_name = 'D:/AMPBA from ISB/Term 2/FP-1/Group Project/WSJ Scraping/article_text_' + query_file_tag + '.json'
    if os.path.isfile(file_name)==False:
        write_first_json(file_name)
        result = False
    else:
        article_links = pd.read_json(file_name)
        urls = article_links.article_url.unique()
        result = url in urls
        
    return result


# In[110]:


# Collect the article links from each page in the total search result
driver.get(basic_url)
page_count=get_pages(driver)
ls=[]
existing_pages=0
errors=0
saved_links=0
for n in range(1,page_count+1):
    if n==1:
        url=basic_url
    else:
        url=basic_url+'&page={}'.format(n)
    try:
        driver.get(url)
        time.sleep(2)
        article_links=  WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, #visibility_of_all_elements_located
                '//h3[contains(@class,"WSJTheme--headline--") and contains(@class, "WSJTheme--heading-3--") and contains(@class,"typography--serif-display--")]/a')))
    #print(len(article_links))

        for article_link in article_links:
            heading = article_link.get_attribute('innerText')
            url=article_link.get_attribute('href')
            query_index=url.index('?')
            link=url[0:query_index]
            if article_link_exists(link,query_file_tag)==False:
                ls.append([heading,url])
                saved_links+=1
            else:
                existing_pages+=1
    except Exception as e:
        errors+=1
        continue
    
    write_article_link_rows(ls,query_file_tag)
    ls.clear()
    print('Pages:{}, Saved:{}, Errors:{},Existing:{}'.format(n,saved_links,errors,existing_pages))


# In[104]:


def write_first_json(file_name):
    dict=[{"article_date":"1/1/1900",
          "category":"category",
          "article_heading":'article_heading',
          "article_text":'article_text',
          "article_url":"article_url",
          "company":query_file_tag}]
    with open(file_name, "w") as outfile:
        json.dump(dict, outfile, indent=2)
        outfile.close()


# In[87]:


# function to add to JSON
def write_article_text_json(new_data,query_file_tag):
    filename='D:/AMPBA from ISB/Term 2/FP-1/Group Project/WSJ Scraping/article_text_' + query_file_tag + '.json' #search_article_text.json"
    if os.path.isfile(filename)==False:
        write_first_json(filename)
        
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
        file.close()


# In[88]:


# write article data to csv file
def write_article_error_message(rows,query_file_tag):
    file_name = 'D:/AMPBA from ISB/Term 2/FP-1/Group Project/WSJ Scraping/article_error_' + query_file_tag + '.csv'
    if os.path.isfile(file_name)==False:
        with open(file_name, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)
            csv_file.close()
    else:
        with open(file_name, 'a', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)
            csv_file.close()


# In[89]:


def is_month(txt):
    month_list =['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    start = txt[0:3]
    mnth=0
    if start in month_list:
        month_obj = datetime.strptime(start, "%b")
        mnth=month_obj.month
    else:
        mnth=0
    return mnth


# In[100]:


def get_article_date(date_text):
    
    if date_text.find('updated')>-1:
        date_text.replace('updated','')
    
    if date_text.find(' on ')>-1:
        date_text.replace(' on ','')
     
    if date_text.find(' at ')>-1:
        date_text.replace(' at ','')
            
    date_text=date_text.replace(',','').replace('.','').lower()
    mnth=0
    yr=0
    dt=0
    for s in date_text.split():
        if mnth==0:
            mnth = is_month(s)
        elif  (yr==0 and len(s)==4 and s.isnumeric()==True) :
            yr=s
        elif (dt==0 and len(s)<=2 and s.isnumeric()==True):
            dt=s
    
    
    dt_obj=str(dt) +'/'+ str(mnth) +'/' +str(yr)
    return dt_obj


# In[91]:


def get_article_category(driver):
    category=''
    try:
        category_div = driver.find_element(By.XPATH,'//div[contains(@class,"category")]')
        category_li=category_div.find_elements(By.TAG_NAME,'li')
        
        for li in category_li:
            category=category + ',' + li.get_attribute('innerText').strip()
            category=category.strip()
    except Exception as e:
        category=''
        #print(e)

    return category.strip()


# In[108]:


# get article links from csv file, fetch article, get the text and save it to a json file
# original file name : wsj_search_article_links
start_time=time.time()
end_time=time.time()
url_file_name = 'D:/AMPBA from ISB/Term 2/FP-1/Group Project/WSJ Scraping/article_links_' + query_file_tag + '.csv'
with open(url_file_name, 'r', encoding='utf-8') as read_obj:
    csv_reader = csv.reader(read_obj)
    # Iterate over each row in the csv using reader object
    n=1
    saved_article_count=0
    error_article_count=0
    existing_article_count=0
    
    for row in csv_reader:
        article_heading=row[0]
        article_url=row[1]
        
        # check if the url has already been scraped
        if article_text_exists(url,query_file_tag)==False:
            
            try:
                driver.get(article_url)
                time.sleep(2)
                
                category = get_article_category(driver)
                
                article_date_obj = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH,'//time[contains(@class,"timestamp article__timestamp flexbox__flex--1")]')))
                
                article_date=get_article_date(article_date_obj[0].get_attribute('innerText').strip())
                
                # Get the article text
                article = driver.find_element(By.XPATH,'//div[contains(@class,"article-content") or contains(@id,"article-content")]')
                paras = article.find_elements(By.TAG_NAME,'p')
                paras_count=len(paras)
                article_text=''
                
                for i in range(0,paras_count): 
                    para_text=paras[i].get_attribute("innerText")
                    article_text = article_text +' ' + para_text 
            
            
                values={"article_date":article_date,
                      "category":category,
                      "article_heading":article_heading,
                      "article_text":article_text,
                      "article_url":article_url,
                       "company":query_file_tag}
                
                write_article_text_json(values,query_file_tag)
                #print('Saved Article No:',saved_article_count)
                saved_article_count+=1

            except Exception as e:
                er=[]
                error=[article_date,article_heading,article_url, str(e)]
                er.append(error)
                write_article_error_message(er,query_file_tag)
                #print('Article Errors:',error_article_count)
                error_article_count+=1
                continue
        else:
            #print('Existing Articles: ' + existing_article_count)
            existing_article_count+=1
        end=time.time()
        duration = end_time- start_time
        
        print('Total:{}, Saved :{}, Errors:{}, Existing:{},Duration{}'.format(n,saved_article_count,error_article_count,existing_article_count, duration))
        n+=1
        
    read_obj.close()

