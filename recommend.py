import pickle

# Load data
movies = pickle.load(open('models/movies.pkl', 'rb'))
similarity = pickle.load(open('models/similarity.pkl', 'rb'))

def recommend(movie):
    movie = movie.lower()

    # Find matching movie
    matched = movies[movies['title'].str.lower() == movie]

    if matched.empty:
        return [{"title": "Movie not found", "year": "-", "director": "-"}]

    index = matched.index[0]

    # Get similarity scores
    distances = similarity[index]

    # Sort movies based on similarity
    movie_list = sorted(
        enumerate(distances),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_movies = []

    for i in movie_list:
        row = movies.iloc[i[0]]

        recommended_movies.append({
            "title": row.title,
            "year": row.year,
            "director": row.director
        })

    return recommended_movies