#!/usr/bin/env python
# coding: utf-8

# In[188]:


import pandas as pd
import matplotlib
import numpy as np


# In[199]:


data = pd.read_csv('/Users/vikrantdhawan/Dropbox/My Mac (Vikrant’s MacBook Air)/Downloads/Twitter_output.csv')
data.head(10)


# In[200]:


Grouped_Data_Twit = data.groupby(['Date']).agg({ 'POSITIVE_TW':[ np.mean],'NEGATIVE_TW':[ np.mean],'NEUTRAL_TW':[ np.mean]}).stack(1)


# In[201]:


Grouped_Data_Twit


# In[202]:


data = pd.read_csv('/Users/vikrantdhawan/Dropbox/My Mac (Vikrant’s MacBook Air)/Downloads/WallStreet_output.csv')
data.head(10)


# In[203]:


Grouped_Data_WS = data.groupby(['Date']).agg({ 'POSITIVE_WS':[ np.mean],'NEGATIVE_WS':[ np.mean],'NEUTRAL_WS':[ np.mean]}).stack(1)


# In[207]:


Grouped_Data_WS


# In[214]:


Grouped_Data_TW_WS = pd.merge(Grouped_Data_Twit,Grouped_Data_WS,on='Date',how='left' )


# In[217]:


Grouped_Data_TW_WS['POSITIVE_TW'].fillna(Grouped_Data_TW_WS['POSITIVE_TW'].median(), inplace=True)
Grouped_Data_TW_WS['NEGATIVE_TW'].fillna(Grouped_Data_TW_WS['NEGATIVE_TW'].median(), inplace=True)
Grouped_Data_TW_WS['NEUTRAL_TW'].fillna(Grouped_Data_TW_WS['NEUTRAL_TW'].median(), inplace=True)
Grouped_Data_TW_WS['POSITIVE_WS'].fillna(Grouped_Data_TW_WS['POSITIVE_WS'].median(), inplace=True)
Grouped_Data_TW_WS['NEGATIVE_WS'].fillna(Grouped_Data_TW_WS['NEGATIVE_WS'].median(), inplace=True)
Grouped_Data_TW_WS['NEUTRAL_WS'].fillna(Grouped_Data_TW_WS['NEUTRAL_WS'].median(), inplace=True)


# In[218]:


Grouped_Data_TW_WS


# In[219]:


data2 = pd.read_csv('/Users/vikrantdhawan/Dropbox/My Mac (Vikrant’s MacBook Air)/Downloads/TSLA_Stock.csv')
data2.head(10)


# In[220]:


data2['lag(Close,1)'] = data2['Close']. shift(1)
data2['Change'] = data2['Close']/data2['lag(Close,1)']

data2['stock_movment']= np.where(data2['Change'] > 1, 1,0)


# In[221]:


Data_Stock = data2[['Date','stock_movment']]
Data_Stock


# In[223]:


Final = pd.merge(Data_Stock,Grouped_Data_TW_WS,on='Date',how='left' )


# In[224]:


Final['stock_movment_lag'] = data2['stock_movment']. shift(-1)


# In[225]:


def clean_dataset(Final):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)


# In[226]:


Final.replace([np.inf, -np.inf], np.nan, inplace=True)


# In[267]:


Final.dropna(inplace=True)


# In[273]:


Final.to_csv("Final.csv")


# In[274]:


Final


# In[233]:


y = Final['stock_movment_lag']
x = Final[['POSITIVE_WS','NEGATIVE_WS','NEUTRAL_WS','POSITIVE_TW','NEGATIVE_TW','NEUTRAL_TW']]


# In[241]:


x.shape
y.shape


# In[257]:


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = .20)


# In[258]:


print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)


# In[259]:


from sklearn.naive_bayes import GaussianNB
nb = GaussianNB()
nb.fit(x_train, y_train)

y_predicted = nb.predict(x_test)


# In[260]:


# Calculate the accuracy of the prediction
from sklearn.metrics import accuracy_score
print("Accuracy = ")
print(format(accuracy_score(y_test, y_predicted)*100))


# In[262]:


print("Accuracy:",metrics.accuracy_score(y_test, y_predicted))
print("Precision:",metrics.precision_score(y_test, y_predicted))
print("Recall:",metrics.recall_score(y_test, y_predicted))


# In[265]:


# import the class
from sklearn.linear_model import LogisticRegression

# instantiate the model (using the default parameters)
logreg = LogisticRegression(solver='liblinear')

# fit the model with data
logreg.fit(x_train, y_train)

# Predict on test data
y_pred = logreg.predict(x_test)


# In[269]:


print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))


# In[275]:


from sklearn.neighbors import KNeighborsClassifier

# Create a KNN model instance with n_neighbors=1
knn = KNeighborsClassifier(n_neighbors = 1)

# Fit the model
knn.fit(x_train, y_train)

# predict on testing dataset
pred = knn.predict(x_test)

# COnfusion Matrics
from sklearn.metrics import classification_report, confusion_matrix

print(confusion_matrix(y_test, pred))


# In[276]:


print("Accuracy = ")
print(format(accuracy_score(y_test, pred)*100))


# In[272]:


print(classification_report(y_test, pred))

