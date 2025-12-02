## we will use streamlit
import os
from dotenv import load_dotenv
load_dotenv()


import streamlit as st
import pickle
import requests

movies_df = pickle.load(open("Movies.pkl",'rb'))
similarity = pickle.load(open("similarity.pkl",'rb'))
movies_list = movies_df['title'].values



#fetch poster from api
api_key = os.getenv('TMDB_API_KEY')

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8b270da3995a7f4f7dfa2a4ed45a91eb&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies_df[movies_df['title']== movie].index[0]
    distances = similarity[movie_index]
    sorted_movies = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters = []
    
    for i in sorted_movies:
        movie_row = movies_df.iloc[i[0]]
        recommended_movies.append(movie_row.title)
        recommended_movies_posters.append(fetch_poster(movie_row['movie_id']))
        
    return recommended_movies,recommended_movies_posters
        
st.title("Movie Recommender System")


selected_movie_name = st.selectbox(
    'How would you like to be connected ?',
    movies_list
    
)
if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
    
    cols = st.columns(3)
    
    # as rows are not supported directly we will use columns to display but 3 columns can show only 3 movies at a time
    # and we went to show 3 more on the next row so we will use range len and mod function to fill the columns first and then next 3 will be shown in next row
    
    
    for idx in range(len(recommendations)):
        with cols[idx % 3]:
            st.text(recommendations[idx])
            st.image(posters[idx])