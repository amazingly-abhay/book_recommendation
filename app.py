from flask import Flask, render_template, request
import os
import pandas
import pickle
import numpy as np


script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, 'popular.pkl')
pt_path = os.path.join(script_directory, 'pt.pkl')
books_path = os.path.join(script_directory, 'books.pkl')
similarity_score_path = os.path.join(script_directory, 'similarity_score.pkl')
try:
    popular_df = pickle.load(open(file_path, 'rb'))
    pt = pickle.load(open(pt_path, 'rb'))
    books = pickle.load(open(books_path, 'rb'))
    similarity_score = pickle.load(open(similarity_score_path, 'rb'))
except FileNotFoundError:
    print("One or more pickle files not found.")
except Exception as e:
    print(f"An error occurred while loading pickle files: {e}")



app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           year=list(popular_df['Year-Of-Publication'].values),
                           image=list(popular_df['Image-URL-L'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values))

@app.route('/Recommender')
def recommendation():
    return render_template('Recommendation.html'
                           )

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input =request.form.get('user_input')
    index=np.where(pt.index==user_input)[0][0]
    similar_items=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:16]
    data=[]
    for i in similar_items:
        item=[]
        temp=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-L'].values))
        data.append(item)
      
    return render_template('Recommendation.html',data=data) 



