import streamlit as st
import pickle
import pandas as pd
import requests

# Load the single model file
model_data = pickle.load(open('movie_recommender.pkl', 'rb'))

# Extract movie data and similarity matrix
movies = pd.DataFrame.from_dict(model_data["movies"])  # Convert back to DataFrame
similarity = model_data["similarity"]  # Corrected spelling from 'simlarity'


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=1bbe2706b927088e288d0826a4814af9&language=en-US".format(
        movie_id)
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    movie_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_movies_poster = []

    for i in movie_list[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))  # Fetch poster

    return recommended_movies, recommended_movies_poster


# Title of the web page
st.title('Movie Recommender System')

selected_movie = st.selectbox('Select a Movie!', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
