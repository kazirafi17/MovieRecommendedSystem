import pickle
import streamlit as st
import requests

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=YOUR_TMDB_API_KEY&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies
def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Load movie list from pickle file
@st.cache(allow_output_mutation=True)
def load_movies():
    url = 'https://drive.google.com/file/d/1lnzEeYuvweJ_O4EkYI_cEVML4aeMhlVP/view?usp=drive_link'
    response = requests.get(url)
    return pickle.loads(response.content)

# Load similarity matrix from pickle file in Google Drive
@st.cache(allow_output_mutation=True)
def load_similarity():
    url = 'https://drive.google.com/file/d/1Bw-lYMFe8Lf1r-4EEye7_Ik91IJWRrCX/view?usp=drive_link'
    response = requests.get(url)
    return pickle.loads(response.content)

# Main Streamlit app
def main():
    st.header('Movie Recommender System')

    # Load movies and similarity matrix
    movies = load_movies()
    similarity = load_similarity()

    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, similarity)
        cols = st.beta_columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])

if __name__ == '__main__':
    main()
