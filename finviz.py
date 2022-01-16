#!/usr/bin/env python
# coding: utf-8

# In[14]:


from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from dateutil.parser import parse


# In[2]:


finviz_url='https://finviz.com/quote.ashx?t=TSLA'
req=Request(url=finviz_url, headers={'user-agent':'my-app'})
response=urlopen(req)
html =BeautifulSoup(response,'html')
news_table=html.find(id='news-table')
news_table


# In[23]:


parsed_data = []
for row in news_table.findAll('tr'):
        title = row.a.text
        timestamp = row.td.text.split(' ')
        if len(timestamp) == 1:
            time=timestamp[0]
        else:
            date=timestamp[0]
            time=timestamp[1]
        parsed_data.append([parse(date).strftime("%Y-%m-%d"),parse(time).strftime("%H:%M:%S"),title,'FINVIZ'])


# In[24]:


output = pd.DataFrame(parsed_data)
output


# In[25]:


output.to_csv('C:/Users/sonal/Desktop/Sonal/Assignment/Term 2/Foundation Project/data.csv', mode='a', index = False, header=None)


# In[ ]:




