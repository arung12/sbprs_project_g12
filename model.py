import os
import pickle

import pandas as pd

import nltk
# Download necessary NLTK resources
nltk.download('punkt')

def load_from_pickle(path):
   if os.path.exists(path):
       return pickle.load(open(path,'rb'))
   else:
       print('Not able to locate',path)
       return None

tfidf_vectorizer = load_from_pickle('pickle_files/tfidf_vectorizer.pkl')
model = load_from_pickle('pickle_files/model_final.pkl')
recommendation_matrix = load_from_pickle('pickle_files/user_final_rating.pkl')
products_data = load_from_pickle('pickle_files/products_cleaned_data.pkl')

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