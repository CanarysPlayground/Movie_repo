from flask import Flask, request, jsonify, render_template, g, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from functools import wraps

DB_PATH = os.path.join(os.path.dirname(__file__), "movies.db")

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    with open(os.path.join(os.path.dirname(__file__), "schema.sql")) as f:
        db.executescript(f.read())
    db.commit()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Authentication helpers
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    if 'user_id' not in session:
        return None
    db = get_db()
    cur = db.execute("SELECT id, username FROM users WHERE id = ?", (session['user_id'],))
    return cur.fetchone()

# Initialize database if it doesn't exist
if not os.path.exists(DB_PATH):
    with app.app_context():
        init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("index.html")

# API: register user
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "username and password required"}), 400
    
    username = data["username"].strip()
    password = data["password"]
    
    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    
    db = get_db()
    # Check if username already exists
    cur = db.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cur.fetchone():
        return jsonify({"error": "Username already exists"}), 400
    
    # Create user
    password_hash = generate_password_hash(password)
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
    db.commit()
    
    return jsonify({"status": "success", "message": "User registered successfully"}), 201

# API: login
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "username and password required"}), 400
    
    username = data["username"].strip()
    password = data["password"]
    
    db = get_db()
    cur = db.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid username or password"}), 401
    
    session['user_id'] = user["id"]
    session['username'] = user["username"]
    
    return jsonify({"status": "success", "message": "Logged in successfully", "username": user["username"]})

# API: logout
@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"status": "success", "message": "Logged out successfully"})

# API: get current user
@app.route("/api/user", methods=["GET"])
def current_user():
    user = get_current_user()
    if user:
        return jsonify({"username": user["username"], "id": user["id"]})
    return jsonify({"error": "Not authenticated"}), 401

# API: list movies
@app.route("/api/movies", methods=["GET"])
def list_movies():
    db = get_db()
    cur = db.execute("SELECT id, title, year, genre, synopsis FROM movies ORDER BY id")
    movies = [dict(row) for row in cur.fetchall()]
    return jsonify(movies)

# API: movie details
@app.route("/api/movies/<int:movie_id>", methods=["GET"])
def movie_details(movie_id):
    db = get_db()
    cur = db.execute("SELECT id, title, year, genre, synopsis FROM movies WHERE id = ?", (movie_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify(dict(row))

# API: add movie to playlist
@app.route("/api/playlist", methods=["POST"])
@login_required
def add_to_playlist():
    data = request.get_json()
    if not data or "movie_id" not in data:
        return jsonify({"error": "movie_id required"}), 400
    movie_id = data["movie_id"]
    user_id = session['user_id']
    db = get_db()
    # check movie exists
    cur = db.execute("SELECT id FROM movies WHERE id = ?", (movie_id,))
    if not cur.fetchone():
        return jsonify({"error": "movie not found"}), 404
    # check if already in playlist
    cur = db.execute("SELECT id FROM playlist WHERE user_id = ? AND movie_id = ?", (user_id, movie_id))
    if cur.fetchone():
        return jsonify({"error": "Movie already in playlist"}), 400
    # insert to playlist
    db.execute("INSERT INTO playlist (user_id, movie_id) VALUES (?, ?)", (user_id, movie_id))
    db.commit()
    return jsonify({"status": "added", "movie_id": movie_id})

# API: get playlist
@app.route("/api/playlist", methods=["GET"])
@login_required
def get_playlist():
    user_id = session['user_id']
    db = get_db()
    cur = db.execute("""
        SELECT p.id as playlist_id, m.id as movie_id, m.title, m.year, m.genre
        FROM playlist p JOIN movies m ON p.movie_id = m.id 
        WHERE p.user_id = ?
        ORDER BY p.id
    """, (user_id,))
    items = [dict(row) for row in cur.fetchall()]
    return jsonify(items)

if __name__ == "__main__":
    app.run(debug=True)