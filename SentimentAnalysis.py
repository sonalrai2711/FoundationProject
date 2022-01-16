#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime


# In[3]:


data =pd.read_csv("C:/Users/sonal/Desktop/Sonal/Assignment/Term 2/Foundation Project/Twitter.csv")
data.head()


# In[35]:


#datetime_object = datetime.strptime(data['DATE'], '%b %d %Y %I:%M%p')
#datetime_object

#data['DATETIME']=pd.to_datetime(data['DATETIME'])

#data['DATE'].dt.date


# In[4]:


vader=SentimentIntensityAnalyzer()


# In[5]:


compond=lambda summary: vader.polarity_scores(summary)['compound']
data['Compound']=data['SUMMARY'].apply(compond)

negative=lambda summary: vader.polarity_scores(summary)['neg']
data['Negative']=data['SUMMARY'].apply(negative)

neutral=lambda summary: vader.polarity_scores(summary)['neu']
data['Neutral']=data['SUMMARY'].apply(neutral)

positive=lambda summary: vader.polarity_scores(summary)['pos']
data['Positive']=data['SUMMARY'].apply(positive)
data


# In[6]:


data.to_csv('Twitter_output.csv',mode='a',index = False, header=None)


# In[58]:


#Sentiment Analysis
def percentage(part,whole):
    return 100 * float(part)/float(whole)

#Assigning Initial Values
positive = 0
negative = 0
neutral = 0
#Creating empty lists
summary_list = []
neutral_list = []
negative_list = []
positive_list = []


# In[59]:




#Iterating over the Summary in the dataframe
for summary in data['SUMMARY']:
    summary_list.append(summary)
    analyzer = SentimentIntensityAnalyzer().polarity_scores(summary)
    neg = analyzer['neg']
    neu = analyzer['neu']
    pos = analyzer['pos']
    comp = analyzer['compound']
    
    if neg > pos:
        negative_list.append(summary) #appending the tweet that satisfies this condition
        negative += 1 #increasing the count by 1
    elif pos > neg:
        positive_list.append(summary) #appending the tweet that satisfies this condition
        positive += 1 #increasing the count by 1
    elif pos == neg:
        neutral_list.append(summary) #appending the tweet that satisfies this condition
        neutral += 1 #increasing the count by 1 

positive = percentage(positive, len(data)) #percentage is the function defined above
negative = percentage(negative, len(data))
neutral = percentage(neutral, len(data))


# In[61]:


#Converting lists to pandas dataframe
summary_list = pd.DataFrame(summary_list)
neutral_list = pd.DataFrame(neutral_list)
negative_list = pd.DataFrame(negative_list)
positive_list = pd.DataFrame(positive_list)
#using len(length) function for counting
print("Last 30 days, there have been", len(summary_list) ,  "tweets/news on TSLA" ,  end='\n*')
print("Positive Sentiment:", '%.2f' % len(positive_list), end='\n*')
print("Neutral Sentiment:", '%.2f' % len(neutral_list), end='\n*')
print("Negative Sentiment:", '%.2f' % len(negative_list), end='\n*')


# In[20]:





# In[ ]:




