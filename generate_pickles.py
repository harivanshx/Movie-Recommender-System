"""
Script to generate pickle files from CSV data.
Run this script to create Movies.pkl and similarity.pkl files.
"""

import pandas as pd
import numpy as np
import ast
import nltk
from nltk import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

print("Loading CSV files...")
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

print("Merging datasets...")
movies = movies.merge(credits, on='title')

# Select relevant columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Drop null values
movies.dropna(inplace=True)

print("Processing genres...")
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

print("Processing cast...")
def convertcast(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L

movies['cast'] = movies['cast'].apply(convertcast)

print("Processing crew...")
def fetchDirector(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

movies['crew'] = movies['crew'].apply(fetchDirector)

print("Processing overview...")
movies['overview'] = movies['overview'].apply(lambda x: x.split())

print("Removing spaces from names...")
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['overview'] = movies['overview'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])

print("Creating tags...")
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

moviedf = movies[['movie_id', 'title', 'tags']]
moviedf['tags'] = moviedf['tags'].apply(lambda x: " ".join(x))
moviedf['tags'] = moviedf['tags'].apply(lambda x: x.lower())

print("Stemming words...")
ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

moviedf['tags'] = moviedf['tags'].apply(stem)

print("Vectorizing tags...")
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(moviedf['tags']).toarray()

print("Computing similarity matrix...")
similarity = cosine_similarity(vectors)

print("Saving pickle files...")
pickle.dump(moviedf, open('Movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("✓ Successfully generated Movies.pkl and similarity.pkl")
print(f"  - Movies.pkl: {moviedf.shape[0]} movies")
print(f"  - similarity.pkl: {similarity.shape}")
