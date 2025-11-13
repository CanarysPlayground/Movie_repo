from flask import Flask, request, jsonify, render_template, g, redirect, url_for
import sqlite3
import os

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

# API: list movies
@app.route("/api/movies", methods=["GET"])
def list_movies():
    db = get_db()
    cur = db.execute("SELECT id, title, year, genre, synopsis FROM movies ORDER BY id")
    movies = [dict(row) for row in cur.fetchall()]
    return jsonify(movies)

# API: search movies
@app.route("/api/movies/search", methods=["GET"])
def search_movies():
    query = request.args.get("q", "").strip()
    genre_filter = request.args.get("genre", "").strip()
    year_filter = request.args.get("year", "").strip()
    
    # Input validation
    if not query and not genre_filter and not year_filter:
        return jsonify({"error": "At least one search parameter (q, genre, or year) is required"}), 400
    
    db = get_db()
    sql_parts = ["SELECT id, title, year, genre, synopsis FROM movies WHERE 1=1"]
    params = []
    
    # Case-insensitive partial matching for title
    if query:
        sql_parts.append("AND LOWER(title) LIKE LOWER(?)")
        params.append(f"%{query}%")
    
    # Case-insensitive partial matching for genre
    if genre_filter:
        sql_parts.append("AND LOWER(genre) LIKE LOWER(?)")
        params.append(f"%{genre_filter}%")
    
    # Exact matching for year
    if year_filter:
        try:
            year_int = int(year_filter)
            sql_parts.append("AND year = ?")
            params.append(year_int)
        except ValueError:
            return jsonify({"error": "Year must be a valid integer"}), 400
    
    sql_parts.append("ORDER BY title")
    sql = " ".join(sql_parts)
    
    cur = db.execute(sql, params)
    movies = [dict(row) for row in cur.fetchall()]
    
    return jsonify({
        "results": movies,
        "count": len(movies),
        "query": query,
        "filters": {
            "genre": genre_filter,
            "year": year_filter
        }
    })

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
def add_to_playlist():
    data = request.get_json()
    if not data or "movie_id" not in data:
        return jsonify({"error": "movie_id required"}), 400
    movie_id = data["movie_id"]
    db = get_db()
    # check movie exists
    cur = db.execute("SELECT id FROM movies WHERE id = ?", (movie_id,))
    if not cur.fetchone():
        return jsonify({"error": "movie not found"}), 404
    # insert to playlist
    db.execute("INSERT INTO playlist (movie_id) VALUES (?)", (movie_id,))
    db.commit()
    return jsonify({"status": "added", "movie_id": movie_id})

# API: get playlist
@app.route("/api/playlist", methods=["GET"])
def get_playlist():
    db = get_db()
    cur = db.execute("""
        SELECT p.id as playlist_id, m.id as movie_id, m.title, m.year, m.genre
        FROM playlist p JOIN movies m ON p.movie_id = m.id ORDER BY p.id
    """)
    items = [dict(row) for row in cur.fetchall()]
    return jsonify(items)

if __name__ == "__main__":
    app.run(debug=True)