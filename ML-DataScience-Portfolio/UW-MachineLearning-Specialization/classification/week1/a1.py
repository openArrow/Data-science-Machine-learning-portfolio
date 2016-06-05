import sframe
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model, datasets
products = sframe.SFrame('amazon_baby.gl/')

def remove_punctuation(text):
    import string
    return text.translate(None, string.punctuation) 

products['review_clean'] = products['review'].apply(remove_punctuation)
products = products.fillna('review','')  
products = products[products['rating'] != 3]
train_data, test_data = products.random_split(.8, seed=1)

vectorizer = CountVectorizer(token_pattern=r'\b\w+\b')
     # Use this token pattern to keep single-letter words
# First, learn vocabulary from the training data and assign columns to words
# Then convert the training data into a sparse matrix
train_matrix = vectorizer.fit_transform(train_data['review_clean'])
# Second, convert the test data into a sparse matrix, using the same word-column mapping
test_matrix = vectorizer.transform(test_data['review_clean'])

from sklearn import linear_model
logreg = linear_model.LogisticRegression()
logreg.fit(train_matrix, train_data['sentiment'])
