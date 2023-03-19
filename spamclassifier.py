# -*- coding: utf-8 -*-
"""SpamClassifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ntp94fyLEmDLoZ7FAHRcyJZrIBunI0HK
"""

import pandas as pd
import nltk

#import dataset
messages = pd.read_csv('/SMSSpamCollection', sep = '\t', names = ["label","message"])
#messages

#Data cleaning and preprocessing
import re
nltk.download('punkt')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

ps = PorterStemmer()
wordnet=WordNetLemmatizer()
corpus = []
for i in range(0, len(messages)):
    review = re.sub('[^a-zA-Z]', ' ', messages['message'][i])
    review = review.lower()
    review = review.split()
    #review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = [wordnet.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    corpus.append(review)

#creating Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000)
X = cv.fit_transform(corpus).toarray()

#create dummy variable for label variable
#using messages as independant variable and label column as dependant variable

y = pd.get_dummies(messages['label']) 
#created 2 dummy variables for ham and spam

y = y.iloc[:,1].values 
#using one dummy variable as dependant variable

#Train Test Split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state= 0)

#Training model using Naive Bayes Classifier
from sklearn.naive_bayes import MultinomialNB
spam_detect_model = MultinomialNB().fit(X_train, y_train)

#Prediction w.r.t. Test data
y_pred = spam_detect_model.predict(X_test)

#No.of elements correcty predicted
from sklearn.metrics import confusion_matrix
confusion_m = confusion_matrix(y_test, y_pred)

#Finding accuracy score
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
accuracy