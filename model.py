import os
import pickle

import pandas as pd
import numpy as np
import spacy
import re

import nltk
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

nlp = spacy.load('en_core_web_sm',  disable=["parser", "ner"])

def load_from_pickle(path):
   if os.path.exists(path):
       return pickle.load(open(path,'rb'))
   else:
       print('Not able to locate',path)
       return None

tfidf_vectorizer = load_from_pickle('pickle_files/tfidf_vectorizer.pkl')
model = load_from_pickle('pickle_files/model_final.pkl')
recommendation_matrix = load_from_pickle('pickle_files/user_final_rating.pkl')
products_data = load_from_pickle('pickle_files/products_data.pkl')

def pre_process_text(text):
    #converting text to lower
    text = text.lower()

    #removing any punctuation character by selecting anything other than word and space
    text = re.sub(r'[^\w\s]',"",text)

    #removing the promotion message
    text = re.sub(r'This review was collected as part of a promotion', '', text)
    
    #removing stop words and extrating lemma
    tokens = nlp(text)
    text = [token.lemma_ for token in tokens if not token.is_stop]

    #removing spaces at the front and end
    text = ' '.join(text)
    text = text.strip()

    return text

def get_popular_users():
    user_popularity = recommendation_matrix.sum(axis=1)
    sorted_users = user_popularity.sort_values(ascending=False)
    users = sorted_users.head(25).index.tolist()
    users.append('Other')
    return users

def get_recommended_products(username):
    if username in recommendation_matrix.index:
        recommendations = recommendation_matrix.loc[username].sort_values(ascending=False)[0:20]
        top20_recommendations = pd.DataFrame({'id': recommendations.index, 'cosine_similarity_score' : recommendations})
        top20_recommended_products = products_data[products_data['id'].isin(top20_recommendations['id'])]
        top20_recommended_products = top20_recommended_products[['id','name','combined_review']]
        top20_recommended_products = top20_recommended_products.drop_duplicates()

        X = tfidf_vectorizer.transform(top20_recommended_products['combined_review'])
        top20_recommended_products['predicted_sentiment'] = model.predict(X)

        grouped_df = top20_recommended_products.groupby(['id'])['predicted_sentiment'].agg(['sum', 'count'])
        grouped_df['positive_percentage'] = grouped_df['sum'] / grouped_df['count'] * 100
        top5_recommendations = grouped_df.sort_values(by='positive_percentage', ascending=False).head(5)
        top5_recommended_products = products_data[products_data['id'].isin(top5_recommendations.index)]
        top5_recommended_products = top5_recommended_products[['id','name','brand','categories',	'manufacturer']]
        top5_recommended_products = top5_recommended_products.drop_duplicates()

        recommendations_final = pd.merge(top5_recommended_products,top5_recommendations,left_on='id',right_on='id', how = 'left')
        recommendations_final = recommendations_final[['id','name','brand','categories',	'manufacturer','positive_percentage']].sort_values(by='positive_percentage', ascending=False)
        return recommendations_final
    else:
        return None