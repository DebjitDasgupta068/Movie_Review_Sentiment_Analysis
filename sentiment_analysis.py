from textblob import TextBlob

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.metrics import f1_score,accuracy_score, classification_report

import csv

import re
def getCleanedText(text):

    #nltk.download('stopwords')
    #nltk.download('punkt')
    #nltk.download('wordnet')

    en_stopwords=set(stopwords.words('english'))

    wnet=WordNetLemmatizer()  
    text=text.lower()
    tokens=word_tokenize(text)
    clean=[]
    for words in tokens:
        res=re.sub(r'[^\w\s]',"",words)
        if res!="":
            clean.append(res)
    new_tokens=[i for i in clean if i not in en_stopwords]
    stemmed_tokens=[wnet.lemmatize(i) for i in new_tokens]
    
    return stemmed_tokens

def structurise(text):
  one_list=[]
  element=" "
  for i in text:
    element=element+" "+i
  one_list.append(element)
  return one_list

def predict(text):
  res=[]
  for i in text:
    obj=TextBlob(i)
    sentiment=obj.sentiment.polarity
    if (sentiment>=0):
        res.append("positive")
    else:
        res.append("negative")
  return res

def measure():
    with open('IMDB Dataset.csv','r',encoding="utf8") as csv_file:
        csv_reader=csv.reader(csv_file)
    
        test_reviews=[]
        test_sentiments=[]
        for line in csv_reader:
            test_reviews.append(line[0])
            test_sentiments.append(line[1])


    test_reviews=test_reviews[1:]
    test_sentiments=test_sentiments[1:]


    test_reviews_clean=[getCleanedText(i) for i in test_reviews]
    test_reviews_clean2=[structurise(i) for i in test_reviews_clean]
    
    test_reviews_sentiment=[predict(i) for i in test_reviews_clean2]
    
    print("F1 Score of our model:", f1_score(test_sentiments,test_reviews_sentiment,average=None))
    print("Accuracy of our model:", accuracy_score(test_sentiments,test_reviews_sentiment)*100,"%")
    print(classification_report(test_sentiments,test_reviews_sentiment))
    