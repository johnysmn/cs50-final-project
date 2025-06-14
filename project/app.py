import os
import requests
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY not set")


@app.route("/")
def index():
    """Show Homepage"""
    user_id = session.get("user_id")
    username = None
    if user_id:
        user = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        if user:
            username = user[0]["username"]
    return render_template("index.html", username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("Username is required!")
            return render_template("register.html")

        if not password:
            flash("Password is required!")
            return render_template("register.html")

        if password != confirmation:
            flash("Passwords do not match!")
            return render_template("register.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            flash("This username is already taken!")
            return render_template("register.html")

        hash = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        flash("Account created succesfully! Please, log in")
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            flash("Must provider username")
            return render_template("login.html")
        elif not request.form.get("password"):
            flash("Must provide password")
            return render_template("login.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username and/or password")
            return render_template("login.html")

        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/search", methods=["POST"])
def search():
    """Search for games using RAWG API"""
    query = request.form.get("query")
    if not query:
        flash("You must provide a search query")
        return redirect("/")
    url = f"https://api.rawg.io/api/games?key={API_KEY}&search={query}&page_size=10"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        flash(f"Failed to retrieve data from API: {e}")
        return redirect("/")

    data = response.json()
    games = data.get("results", [])

    return render_template("search_results.html", games=games)


# Não se esqueça de adicionar url_for aos seus imports do flask no topo do arquivo!
# from flask import Flask, flash, redirect, render_template, request, session, url_for

@app.route("/game/<int:game_id>", methods=["GET", "POST"])
def game_details(game_id):
    """Show game details and handle review submission."""

    if request.method == "POST":
        if "user_id" not in session:
            flash("You must be logged in to write a review.")
            return redirect("/login")

        user_id = session["user_id"]
        rating = request.form.get("rating")
        content = request.form.get("content")

        if not rating:
            flash("Rating is required.")
            return redirect(url_for("game_details", game_id=game_id))

        existing_review = db.execute(
            "SELECT id FROM reviews WHERE user_id = ? AND game_id = ?", user_id, game_id
        )
        if existing_review:
            flash("You have already reviewed this game.")
            return redirect(url_for("game_details", game_id=game_id))

        db.execute(
            "INSERT INTO reviews (user_id, game_id, rating, content) VALUES (?, ?, ?, ?)",
            user_id,
            game_id,
            rating,
            content,
        )

        flash("Review submitted successfully!")
        return redirect(url_for("game_details", game_id=game_id))

    game_api_url = f"https://api.rawg.io/api/games/{game_id}?key={API_KEY}"
    try:
        response = requests.get(game_api_url)
        response.raise_for_status()
        game_data = response.json()
    except requests.RequestException:
        flash("Could not load game details from API.")
        return redirect("/")

    reviews = db.execute(
        """
        SELECT reviews.rating, reviews.content, users.username
        FROM reviews JOIN users ON reviews.user_id = users.id
        WHERE reviews.game_id = ? ORDER BY reviews.created_at DESC
        """,
        game_id,
    )

    return render_template("game_detail.html", game=game_data, reviews=reviews)
