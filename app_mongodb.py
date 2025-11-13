from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId
import os

# MongoDB Connection String
# For local MongoDB:
MONGODB_URI = "mongodb://localhost:27017/"
# For MongoDB Atlas (cloud):
# MONGODB_URI = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

# Database and Collection names
DB_NAME = "movie_website_db"
MOVIES_COLLECTION = "movies"
PLAYLIST_COLLECTION = "playlist"

# Initialize MongoDB client
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
movies_collection = db[MOVIES_COLLECTION]
playlist_collection = db[PLAYLIST_COLLECTION]

app = Flask(__name__)

def init_sample_data():
    """Initialize database with sample movie data if empty"""
    if movies_collection.count_documents({}) == 0:
        sample_movies = [
            {
                "title": "The Shawshank Redemption",
                "year": 1994,
                "genre": "Drama",
                "synopsis": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
            },
            {
                "title": "The Godfather",
                "year": 1972,
                "genre": "Crime",
                "synopsis": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
            },
            {
                "title": "The Dark Knight",
                "year": 2008,
                "genre": "Action",
                "synopsis": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests."
            },
            {
                "title": "Inception",
                "year": 2010,
                "genre": "Sci-Fi",
                "synopsis": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea."
            },
            {
                "title": "Pulp Fiction",
                "year": 1994,
                "genre": "Crime",
                "synopsis": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption."
            }
        ]
        result = movies_collection.insert_many(sample_movies)
        print(f"✓ Inserted {len(result.inserted_ids)} sample movies")
    else:
        print(f"✓ Database already has {movies_collection.count_documents({})} movies")

@app.route("/")
def index():
    return render_template("index.html")

# API: list movies
@app.route("/api/movies", methods=["GET"])
def list_movies():
    """Get all movies"""
    movies = list(movies_collection.find({}, {"_id": 0}))
    # Convert ObjectId to string if needed
    for movie in movies:
        if "_id" in movie:
            movie["id"] = str(movie["_id"])
    return jsonify(movies)

# API: movie details
@app.route("/api/movies/<movie_id>", methods=["GET"])
def movie_details(movie_id):
    """Get a specific movie by ID"""
    try:
        # Try to find by ObjectId
        movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
        if not movie:
            # Try to find by title (case-insensitive)
            movie = movies_collection.find_one({"title": {"$regex": f"^{movie_id}$", "$options": "i"}})
        
        if not movie:
            return jsonify({"error": "Movie not found"}), 404
        
        # Convert ObjectId to string
        movie["id"] = str(movie["_id"])
        del movie["_id"]
        return jsonify(movie)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# API: add a new movie
@app.route("/api/movies", methods=["POST"])
def add_movie():
    """Add a new movie to the database"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ["title", "year", "genre", "synopsis"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
    
    # Insert movie
    result = movies_collection.insert_one({
        "title": data["title"],
        "year": int(data["year"]),
        "genre": data["genre"],
        "synopsis": data["synopsis"]
    })
    
    return jsonify({
        "status": "created",
        "id": str(result.inserted_id),
        "message": "Movie added successfully"
    }), 201

# API: update a movie
@app.route("/api/movies/<movie_id>", methods=["PUT"])
def update_movie(movie_id):
    """Update an existing movie"""
    data = request.get_json()
    
    try:
        update_data = {}
        if "title" in data:
            update_data["title"] = data["title"]
        if "year" in data:
            update_data["year"] = int(data["year"])
        if "genre" in data:
            update_data["genre"] = data["genre"]
        if "synopsis" in data:
            update_data["synopsis"] = data["synopsis"]
        
        result = movies_collection.update_one(
            {"_id": ObjectId(movie_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({"error": "Movie not found"}), 404
        
        return jsonify({
            "status": "updated",
            "id": movie_id,
            "message": "Movie updated successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# API: delete a movie
@app.route("/api/movies/<movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    """Delete a movie"""
    try:
        result = movies_collection.delete_one({"_id": ObjectId(movie_id)})
        
        if result.deleted_count == 0:
            return jsonify({"error": "Movie not found"}), 404
        
        # Also remove from playlist
        playlist_collection.delete_many({"movie_id": movie_id})
        
        return jsonify({
            "status": "deleted",
            "message": "Movie deleted successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# API: add movie to playlist
@app.route("/api/playlist", methods=["POST"])
def add_to_playlist():
    """Add a movie to the playlist"""
    data = request.get_json()
    
    if not data or "movie_id" not in data:
        return jsonify({"error": "movie_id required"}), 400
    
    movie_id = data["movie_id"]
    
    try:
        # Check if movie exists
        movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
        if not movie:
            return jsonify({"error": "Movie not found"}), 404
        
        # Check if already in playlist
        existing = playlist_collection.find_one({"movie_id": movie_id})
        if existing:
            return jsonify({"error": "Movie already in playlist"}), 400
        
        # Add to playlist
        playlist_collection.insert_one({
            "movie_id": movie_id,
            "title": movie["title"],
            "year": movie["year"],
            "genre": movie["genre"]
        })
        
        return jsonify({
            "status": "added",
            "movie_id": movie_id,
            "message": "Movie added to playlist"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# API: get playlist
@app.route("/api/playlist", methods=["GET"])
def get_playlist():
    """Get all movies in the playlist"""
    playlist = list(playlist_collection.find({}, {"_id": 0}))
    return jsonify(playlist)

# API: remove from playlist
@app.route("/api/playlist/<movie_id>", methods=["DELETE"])
def remove_from_playlist(movie_id):
    """Remove a movie from the playlist"""
    result = playlist_collection.delete_one({"movie_id": movie_id})
    
    if result.deleted_count == 0:
        return jsonify({"error": "Movie not in playlist"}), 404
    
    return jsonify({
        "status": "removed",
        "message": "Movie removed from playlist"
    })

# API: search movies
@app.route("/api/movies/search", methods=["GET"])
def search_movies():
    """Search movies by title, genre, or year"""
    query = request.args.get("q", "")
    genre = request.args.get("genre", "")
    year = request.args.get("year", "")
    
    search_filter = {}
    
    if query:
        search_filter["$or"] = [
            {"title": {"$regex": query, "$options": "i"}},
            {"synopsis": {"$regex": query, "$options": "i"}}
        ]
    
    if genre:
        search_filter["genre"] = {"$regex": genre, "$options": "i"}
    
    if year:
        search_filter["year"] = int(year)
    
    movies = list(movies_collection.find(search_filter, {"_id": 0}))
    
    for movie in movies:
        if "_id" in movie:
            movie["id"] = str(movie["_id"])
    
    return jsonify(movies)

if __name__ == "__main__":
    # Initialize sample data on startup
    print("Initializing MongoDB...")
    init_sample_data()
    print("✓ MongoDB ready!")
    print(f"✓ Database: {DB_NAME}")
    print(f"✓ Connection: {MONGODB_URI}")
    print("\nStarting Flask application...")
    app.run(debug=True)
