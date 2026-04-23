import streamlit as st
import pickle
from recommend import recommend

movies = pickle.load(open('models/movies.pkl', 'rb'))

st.set_page_config(
    page_title="Movie Recommender",
    layout="wide"
)

st.title("Recommendations")

# ---------------- SELECT MOVIE ---------------- #
selected_movie = st.selectbox(
    "Choose a movie",
    movies['title'].values,
    index=None,
    placeholder="Select a movie"
)

# ---------------- BUTTON ---------------- #
if st.button("Recommend"):

    if selected_movie is None:
        st.warning("Please select a movie first!")
    
    else:
        recommendations = recommend(selected_movie)

        st.subheader("Recommended Movies:")

        # ✅ Correct indentation
        for movie in recommendations:
            st.markdown(f"""
            <p style='font-size:18px; margin-bottom:2px;'>
              <b>{movie['title']}</b> ({movie['year']})
            </p>

            <p style='font-size:13px; color:gray; margin-top:0;'>
              Director: {movie['director']}
            </p>
            <hr>
            """, unsafe_allow_html=True)