import pickle
import requests
from urllib.parse import quote

# -----------------------------
# Load Trained Model
# -----------------------------

movies = pickle.load(open("model/movies.pkl", "rb"))
similarity = pickle.load(open("model/similarity.pkl", "rb"))

# -----------------------------
# OMDb API Key
# -----------------------------

API_KEY = "495c0026"


# -----------------------------
# Fetch Movie Details
# -----------------------------

def get_movie_details(title):

    try:

        clean_title = title.split(" (")[0]

        url = f"https://www.omdbapi.com/?t={quote(clean_title)}&apikey={API_KEY}"

        response = requests.get(url)

        data = response.json()

        if data.get("Response") == "True":

            return {
                "title": data.get("Title"),
                "poster": data.get("Poster")
                if data.get("Poster") != "N/A"
                else "https://via.placeholder.com/300x450?text=No+Poster",

                "rating": data.get("imdbRating", "N/A"),

                "year": data.get("Year", "N/A"),

                "genre": data.get("Genre", "N/A")
            }

    except Exception:

        pass

    return {
        "title": title,
        "poster": "https://via.placeholder.com/300x450?text=No+Poster",
        "rating": "N/A",
        "year": "N/A",
        "genre": "N/A"
    }


# -----------------------------
# Recommend Movies
# -----------------------------

def recommend(movie_name):

    movie_name = movie_name.lower().strip()

    matches = movies[
        movies["title"].str.lower().str.contains(
            movie_name,
            na=False
        )
    ]

    if matches.empty:
        return []

    movie_index = matches.index[0]

    distances = similarity[movie_index]

    recommended_movies = sorted(

        list(enumerate(distances)),

        key=lambda x: x[1],

        reverse=True

    )[1:6]

    recommendations = []

    for movie in recommended_movies:

        title = movies.iloc[movie[0]].title

        recommendations.append(

            get_movie_details(title)

        )

    return recommendations


# -----------------------------
# Complete Movie Details
# -----------------------------

def get_complete_movie_details(title):

    try:

        clean_title = title.split(" (")[0]

        url = f"https://www.omdbapi.com/?t={quote(clean_title)}&apikey={API_KEY}"

        response = requests.get(url)

        data = response.json()

        if data.get("Response") == "True":

            return data

    except Exception:

        pass

    return None