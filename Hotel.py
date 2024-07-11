import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import nltk
import seaborn as sns
from nltk.corpus import stopwords

# Read the CSV file into a DataFrame
df = pd.read_csv('hotels.csv')
# define new colmun 
df['positive_review_wc'] = np.nan

# Group the dataset
grouped = df.groupby('hotel_name')

# Get English stopwords
english_stopwords = stopwords.words('english')
if 'the' not in english_stopwords:
    english_stopwords.append('the')
if '' not in english_stopwords: 
    english_stopwords.append('')
    
Words = dict()

# Get positive words count and most used positive words
for index,row in df.iterrows():
    review = row['positive_review']
    List = review.split(' ')
    # Split the review into words and record the words number
    for word in List:
        if word.lower() not in english_stopwords and word not in Words:
            Words[word]=1
        elif word.lower() not in english_stopwords:
            Words[word] = Words[word]+1
    # record the length of positive review 
    if len(review) >0:
        count = len(review.split(' '))
    else:
        count = 0 
    # assign total count of positive review into new column
    df.at[index, 'positive_review_wc'] = count


 
# Store the numbe of reviews of each hotel 
number = dict()
for name,group in grouped:             
    quatile = np.percentile(group['reviewer_score'],[25,75])
    number[name] = [group.shape[0],quatile[1]-quatile[0]]
    
# Rate the top 10 hotel by review number
top_10 = sorted(number.items(), key=lambda item: item[1][0], reverse=True)[:10]
# Rate the least 10 reliable hotels by iqr
least_10 = sorted(number.items(),key = lambda item:item[1][1],reverse=True)[:10]
# Rate the top 10 words
Top_10_words = sorted(Words.items(),key = lambda item:item[1],reverse = True)[:10]

print(Top_10_words)


#Plot least 10 reliable hotels according from highest iqr
x,y = list(),list()
for tuple in least_10:
    x.append(tuple[0])
    y.append(tuple[1][1])
    
plt.figure(figsize=(13, 8))
plt.barh(x,y,color = 'blue')
plt.title('Least 10 reliable hotels by iqr')
plt.xlabel('Interquartile range')
plt.ylabel('Hotel name')
plt.tight_layout()
plt.show()

# Plot the top 10 hotelsl in bar chart
x,y = list(), list()
for tuple in top_10:
    x.append(tuple[0])
    y.append(tuple[1][0])
    
plt.figure(figsize=(13, 8))
plt.barh(x,y,color = 'red')
plt.title('Top 10 hotels by reviews number')
plt.xlabel('Reviews number')
plt.ylabel('Hotel name')
plt.tight_layout()
plt.show()

plt.scatter(df['positive_review_wc'],df['reviewer_score'])
plt.xlabel('Positive review words count')
plt.ylabel('Reviewer score')
plt.title('Positive words count vs reviewer score')
plt.show()






