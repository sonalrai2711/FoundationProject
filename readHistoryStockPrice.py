#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install pandas_datareader


# In[1]:


# import libraries
import pandas as pd
from pandas_datareader import data as pdr

    


# In[4]:


# initializing Parameters
start_date = "2021-01-01"
end_date = "2022-12-31"
ticker = 'TSLA'


# In[6]:


# Getting the data
data = pdr.get_data_yahoo(i, start_date, end_date)
filename=ticker+".xlsx"
data.to_excel("C:/Users/sonal/Desktop/Sonal/Assignment/Term 2/Foundation Project/"+filename)


# In[ ]:




