from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User
from recommender import recommend, get_complete_movie_details
import requests

app = Flask(__name__)

# -----------------------------
# Configuration
# -----------------------------
app.secret_key = "movie_recommendation_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# -----------------------------
# OMDb API
# -----------------------------
API_KEY = "495c0026"


# -----------------------------
# Trending Movies
# -----------------------------
def get_trending_movies():

    trending_titles = [
    "Avatar",
    "Avatar: The Way of Water",
    "Avengers",
    "Avengers: Infinity War",
    "Avengers: Endgame",
    "Iron Man",
    "Iron Man 2",
    "Iron Man 3",
    "Captain America: The First Avenger",
    "Captain America: Civil War",
    "Thor",
    "Thor: Ragnarok",
    "Black Panther",
    "Doctor Strange",
    "Spider-Man",
    "Spider-Man: Homecoming",
    "Spider-Man: Far From Home",
    "Spider-Man: No Way Home",
    "The Batman",
    "The Dark Knight",
    "Batman Begins",
    "The Dark Knight Rises",
    "Joker",
    "Superman Returns",
    "Man of Steel",
    "Wonder Woman",
    "Aquaman",
    "Justice League",
    "Titanic",
    "Inception",
    "Interstellar",
    "The Prestige",
    "Oppenheimer",
    "Tenet",
    "Dunkirk",
    "The Matrix",
    "The Matrix Reloaded",
    "The Matrix Revolutions",
    "John Wick",
    "John Wick: Chapter 2",
    "John Wick: Chapter 3 - Parabellum",
    "John Wick: Chapter 4",
    "Mission: Impossible",
    "Top Gun",
    "Top Gun: Maverick",
    "Jurassic Park",
    "Jurassic World",
    "The Lion King",
    "Frozen",
    "Frozen II",
    "Toy Story",
    "Toy Story 2",
    "Toy Story 3",
    "Toy Story 4",
    "Finding Nemo",
    "Finding Dory",
    "Cars",
    "Coco",
    "Moana",
    "Inside Out",
    "Soul",
    "Up",
    "Shrek",
    "Kung Fu Panda",
    "How to Train Your Dragon",
    "Harry Potter and the Sorcerer's Stone",
    "Harry Potter and the Chamber of Secrets",
    "Harry Potter and the Prisoner of Azkaban",
    "Harry Potter and the Goblet of Fire",
    "Harry Potter and the Order of the Phoenix",
    "Harry Potter and the Half-Blood Prince",
    "Harry Potter and the Deathly Hallows: Part 1",
    "Harry Potter and the Deathly Hallows: Part 2",
    "The Lord of the Rings: The Fellowship of the Ring",
    "The Lord of the Rings: The Two Towers",
    "The Lord of the Rings: The Return of the King",
    "The Hobbit",
    "The Hobbit: The Desolation of Smaug",
    "The Hobbit: The Battle of the Five Armies",
    "Pirates of the Caribbean: The Curse of the Black Pearl",
    "Pirates of the Caribbean: Dead Man's Chest",
    "Pirates of the Caribbean: At World's End",
    "Pirates of the Caribbean: On Stranger Tides",
    "Pirates of the Caribbean: Dead Men Tell No Tales",
    "Fast & Furious",
    "Fast Five",
    "Furious 7",
    "The Fate of the Furious",
    "No Time to Die",
    "Skyfall",
    "Casino Royale",
    "The Hunger Games",
    "The Maze Runner",
    "Divergent",
    "The Shawshank Redemption",
    "Forrest Gump",
    "Gladiator",
    "The Godfather",
    "The Godfather Part II"
    ]

    trending = []

    for title in trending_titles:

        try:

            url = f"https://www.omdbapi.com/?t={title}&apikey={API_KEY}"

            data = requests.get(url).json()

            if data.get("Response") == "True":

                trending.append({

                    "title": data["Title"],

                    "poster": data["Poster"]

                })

        except:
            pass

    return trending


# -----------------------------
# Home
# -----------------------------
@app.route("/")
def home():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        username=session["user"],
        trending=get_trending_movies()
    )


# -----------------------------
# Register
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]

        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user:

            return "Username or Email already exists."

        hashed_password = generate_password_hash(password)

        new_user = User(

            username=username,

            email=email,

            password=hashed_password

        )

        db.session.add(new_user)

        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            session["user"] = user.username

            return redirect(url_for("home"))

        return "Invalid Username or Password"

    return render_template("login.html")


# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# -----------------------------
# Recommendation
# -----------------------------
@app.route("/recommend", methods=["POST"])
def recommend_movies():

    if "user" not in session:
        return redirect(url_for("login"))

    movie = request.form["movie"]

    recommendations = recommend(movie)

    return render_template(

        "index.html",

        username=session["user"],

        movie=movie,

        recommendations=recommendations,

        trending=get_trending_movies()

    )


# -----------------------------
# Movie Details
# -----------------------------
@app.route("/movie/<path:title>")
def movie_page(title):

    if "user" not in session:
        return redirect(url_for("login"))

    movie = get_complete_movie_details(title)

    if movie is None:
        return redirect(url_for("home"))

    return render_template(

        "movie.html",

        username=session["user"],

        movie=movie

    )


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)