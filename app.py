import streamlit as st
import pickle
import pandas as pd

# Load precomputed data
new_df = pickle.load(open("movie_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Set dark theme
st.set_page_config(page_title="Movie Recommendation System", page_icon=":clapper:", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>body{background-color: #940404; color: white;}</style>", unsafe_allow_html=True)


st.title('Movie Recommendation System')

# Function to get movie recommendations
def recommend(movie_title):
    if movie_title not in new_df['title'].values:
        return [], "Movie not found in the database."

    index = new_df[new_df['title'] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommendations = [new_df.iloc[i[0]].title for i in distances[1:6]]
    return recommendations, ""

# Create a dynamic selection box
all_movie_titles = new_df['title'].tolist()
selected_movie_title = st.selectbox(
    'Select a movie from the list:',
    all_movie_titles
)

# Display recommendations when a movie is selected
if selected_movie_title:
    recommendations, error = recommend(selected_movie_title)
    if error:
        st.error(error)
    else:
        st.write(f"**Recommendations based on '{selected_movie_title}':**")

        for idx, movie in enumerate(recommendations, start=1):
            st.write(f"{idx}. {movie}")
