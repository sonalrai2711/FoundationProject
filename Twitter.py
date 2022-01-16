#!/usr/bin/env python
# coding: utf-8

# In[7]:


#pip install snscrape


# In[1]:


import datetime as dt
import snscrape.modules.twitter as sntwitter
import pandas as pd
import re


# In[ ]:


#Get user input
query = input("Query: ")

#As long as the query is valid (not empty or equal to '#')...
if query != '':
    noOfTweet = input("Enter the number of tweets you want to Analyze: ")
    #if noOfTweet != '' :
    noOfDays = input("Enter the number of days you want to Scrape Twitter for: ")
    if noOfDays != '':
    #Creating list to append tweet data
        tweets_list = []
        #now = dt.date.today()
        now=pd.to_datetime("2021-12-31")
        now = now.strftime('%Y-%m-%d')
        #yesterday = dt.date.today() - dt.timedelta(days = int(noOfDays))
        yesterday=pd.to_datetime(now) - dt.timedelta(days = int(noOfDays))
        yesterday = yesterday.strftime('%Y-%m-%d')
        d=yesterday
        for i in range(int(noOfDays)):
            d=(pd.to_datetime(d) + dt.timedelta(days = 1)).strftime('%Y-%m-%d')
            n=(pd.to_datetime(d) + dt.timedelta(days = 1)).strftime('%Y-%m-%d')
            for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query + ' lang:en since:' +  d + ' until:' + n + ' -filter:links -filter:replies').get_items()):
                if i > int(noOfTweet):
                    break
                tweets_list.append([tweet.date.strftime("%Y-%m-%d"),tweet.date.strftime("%H:%M:%S"), tweet.id, tweet.content, tweet.username,'TWITTER'])
                
        #Creating a dataframe from the tweets list above 
        df = pd.DataFrame(tweets_list, columns=['Date','Time', 'Tweet Id', 'Text', 'Username','Source'])
        
                


# In[30]:


df


# In[31]:


# Create a function to clean the tweets
def cleanTxt(text):
    text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
    text = re.sub('#', '', text) # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text) # Removing RT
    text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
    return text

#applying this function to Text column of our dataframe
df["Text"] = df["Text"].apply(cleanTxt)


# In[32]:


df= df[["Date","Time","Text"]]


# In[33]:


df.to_csv('C:/Users/sonal/Desktop/Sonal/Assignment/Term 2/Foundation Project/Twitter.csv', mode='a', index = False, header=None)


# In[ ]:




