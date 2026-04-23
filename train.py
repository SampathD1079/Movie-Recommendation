import pandas as pd
import numpy as np
import ast
import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create models folder if not exists
os.makedirs('models', exist_ok=True)

# Load datasets
movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')

# Merge datasets
movies = movies.merge(credits, on='title')

# ✅ Include release_date here
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew','release_date']]

movies.dropna(inplace=True)

# ---------------- FUNCTIONS ---------------- #

def convert(text):
    return [i['name'] for i in ast.literal_eval(text)]

def convert_cast(text):
    L = []
    for i, item in enumerate(ast.literal_eval(text)):
        if i < 3:
            L.append(item['name'])
    return L

def fetch_director(text):
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            return [i['name']]
    return ["Unknown"]

# ---------------- TRANSFORM ---------------- #

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(lambda x: x.split())

# remove spaces
for col in ['genres','keywords','cast','crew']:
    movies[col] = movies[col].apply(lambda x: [i.replace(" ", "") for i in x])

# ---------------- TAGS ---------------- #

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# ---------------- NEW DF ---------------- #

new_df = movies[['movie_id','title','tags','crew','release_date']].copy()

# convert tags to string
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

# extract year
new_df['year'] = new_df['release_date'].apply(lambda x: x.split('-')[0])

# extract director
new_df['director'] = new_df['crew'].apply(lambda x: x[0] if len(x) > 0 else "Unknown")

# drop unnecessary columns
new_df = new_df[['movie_id','title','tags','year','director']]

# ---------------- VECTOR ---------------- #

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# ---------------- SIMILARITY ---------------- #

similarity = cosine_similarity(vectors)

# ---------------- SAVE ---------------- #

pickle.dump(new_df, open('models/movies.pkl', 'wb'))
pickle.dump(similarity, open('models/similarity.pkl', 'wb'))

print("Done")