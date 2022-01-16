#!/usr/bin/env python
# coding: utf-8

# In[6]:


#pip install finnhub-python


# In[1]:


import datetime as dt
import pandas as pd


# In[5]:


FINHUB_KEY='c78qouaad3iappd7h4ug'
import finnhub

finnhub_client = finnhub.Client(FINHUB_KEY)

noOfDays=365

EndDate = dt.date.today()
EndDate = EndDate.strftime('%Y-%m-%d')
StartDate = dt.date.today() - dt.timedelta(days = int(noOfDays))
StartDate = StartDate.strftime('%Y-%m-%d')

print(StartDate," ", EndDate)
finnhub_company_news = finnhub_client.company_news('TSLA', _from="2021-01-01", to="2021-12-31")
finnhub_company_news



# In[3]:


data=[]

for news in finnhub_company_news:
    date_time= dt.datetime.fromtimestamp(news['datetime'])
    #print(date_time)
    summary=news['summary']
    data.append([date_time.strftime("%Y-%m-%d"),date_time.strftime("%H:%M:%S"),summary,'FINNHUB'])


# In[34]:


data


# In[35]:


output = pd.DataFrame(parsed_data)
output


# In[19]:


output.to_csv('C:/Users/sonal/Desktop/Sonal/Assignment/Term 2/Foundation Project/data.csv', mode='a', index = False, header=None)


# In[ ]:




