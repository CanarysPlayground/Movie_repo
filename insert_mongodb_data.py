"""
MongoDB Data Insertion Script
This script demonstrates how to connect to MongoDB and insert data
"""

from pymongo import MongoClient
from datetime import datetime

# MongoDB Connection String
MONGODB_URI = "mongodb://localhost:27017/"

# Connection String Examples:
# Local MongoDB: "mongodb://localhost:27017/"
# MongoDB Atlas: "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/"
# With Auth: "mongodb://admin:password@localhost:27017/"

print("=" * 60)
print("MongoDB Connection and Data Insertion Demo")
print("=" * 60)

# Connect to MongoDB
print(f"\n1. Connecting to MongoDB...")
print(f"   URI: {MONGODB_URI}")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    
    # Test connection
    client.admin.command('ping')
    print("   ✓ Connected successfully!")
    
    # Select database and collections
    db = client["movie_website_db"]
    movies_collection = db["movies"]
    playlist_collection = db["playlist"]
    
    print(f"\n2. Database: {db.name}")
    print(f"   Collections: movies, playlist")
    
    # Clear existing data (optional - for demo purposes)
    print(f"\n3. Clearing existing data...")
    movies_collection.delete_many({})
    playlist_collection.delete_many({})
    print("   ✓ Collections cleared")
    
    # Sample movie data
    sample_movies = [
        {
            "title": "The Shawshank Redemption",
            "year": 1994,
            "genre": "Drama",
            "synopsis": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            "rating": 9.3,
            "director": "Frank Darabont",
            "created_at": datetime.utcnow()
        },
        {
            "title": "The Godfather",
            "year": 1972,
            "genre": "Crime",
            "synopsis": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
            "rating": 9.2,
            "director": "Francis Ford Coppola",
            "created_at": datetime.utcnow()
        },
        {
            "title": "The Dark Knight",
            "year": 2008,
            "genre": "Action",
            "synopsis": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological tests.",
            "rating": 9.0,
            "director": "Christopher Nolan",
            "created_at": datetime.utcnow()
        },
        {
            "title": "Inception",
            "year": 2010,
            "genre": "Sci-Fi",
            "synopsis": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.",
            "rating": 8.8,
            "director": "Christopher Nolan",
            "created_at": datetime.utcnow()
        },
        {
            "title": "Pulp Fiction",
            "year": 1994,
            "genre": "Crime",
            "synopsis": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
            "rating": 8.9,
            "director": "Quentin Tarantino",
            "created_at": datetime.utcnow()
        },
        {
            "title": "Interstellar",
            "year": 2014,
            "genre": "Sci-Fi",
            "synopsis": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
            "rating": 8.6,
            "director": "Christopher Nolan",
            "created_at": datetime.utcnow()
        },
        {
            "title": "The Matrix",
            "year": 1999,
            "genre": "Sci-Fi",
            "synopsis": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
            "rating": 8.7,
            "director": "Lana Wachowski, Lilly Wachowski",
            "created_at": datetime.utcnow()
        },
        {
            "title": "Forrest Gump",
            "year": 1994,
            "genre": "Drama",
            "synopsis": "The presidencies of Kennedy and Johnson unfold through the perspective of an Alabama man with an IQ of 75.",
            "rating": 8.8,
            "director": "Robert Zemeckis",
            "created_at": datetime.utcnow()
        }
    ]
    
    # Insert movies
    print(f"\n4. Inserting {len(sample_movies)} movies...")
    result = movies_collection.insert_many(sample_movies)
    print(f"   ✓ Inserted {len(result.inserted_ids)} movies")
    
    # Display inserted movies
    print("\n5. Inserted Movies:")
    print("   " + "-" * 55)
    for movie in movies_collection.find():
        print(f"   • {movie['title']} ({movie['year']}) - {movie['genre']}")
        print(f"     ID: {movie['_id']}")
        print(f"     Rating: {movie['rating']} | Director: {movie['director']}")
    
    # Add some movies to playlist
    print("\n6. Creating sample playlist...")
    first_three_movies = list(movies_collection.find().limit(3))
    
    playlist_items = []
    for movie in first_three_movies:
        playlist_items.append({
            "movie_id": str(movie["_id"]),
            "title": movie["title"],
            "year": movie["year"],
            "genre": movie["genre"],
            "added_at": datetime.utcnow()
        })
    
    if playlist_items:
        playlist_collection.insert_many(playlist_items)
        print(f"   ✓ Added {len(playlist_items)} movies to playlist")
    
    # Display statistics
    print("\n7. Database Statistics:")
    print(f"   • Total Movies: {movies_collection.count_documents({})}")
    print(f"   • Total Playlist Items: {playlist_collection.count_documents({})}")
    print(f"   • Drama Movies: {movies_collection.count_documents({'genre': 'Drama'})}")
    print(f"   • Sci-Fi Movies: {movies_collection.count_documents({'genre': 'Sci-Fi'})}")
    print(f"   • Movies from 1994: {movies_collection.count_documents({'year': 1994})}")
    
    # Demonstrate queries
    print("\n8. Sample Queries:")
    
    # Find movies by genre
    print("\n   a) Sci-Fi Movies:")
    for movie in movies_collection.find({"genre": "Sci-Fi"}):
        print(f"      - {movie['title']} ({movie['year']})")
    
    # Find movies with high rating
    print("\n   b) Movies with rating >= 9.0:")
    for movie in movies_collection.find({"rating": {"$gte": 9.0}}):
        print(f"      - {movie['title']} - Rating: {movie['rating']}")
    
    # Find movies by director
    print("\n   c) Christopher Nolan Movies:")
    for movie in movies_collection.find({"director": {"$regex": "Christopher Nolan"}}):
        print(f"      - {movie['title']} ({movie['year']})")
    
    # Aggregate by genre
    print("\n   d) Movies Count by Genre:")
    pipeline = [
        {"$group": {"_id": "$genre", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    for result in movies_collection.aggregate(pipeline):
        print(f"      - {result['_id']}: {result['count']} movies")
    
    print("\n" + "=" * 60)
    print("✓ MongoDB Data Insertion Complete!")
    print("=" * 60)
    
    print("\n📌 Your MongoDB Connection String:")
    print(f"   {MONGODB_URI}")
    
    print("\n📌 Database Information:")
    print(f"   Database: {db.name}")
    print(f"   Collections: {', '.join(db.list_collection_names())}")
    
    print("\n📌 To view data in MongoDB shell:")
    print("   mongosh")
    print(f"   use {db.name}")
    print("   db.movies.find().pretty()")
    
    print("\n📌 To start the Flask app:")
    print("   python app_mongodb.py")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("\n⚠ Troubleshooting:")
    print("   1. Make sure MongoDB is installed and running")
    print("   2. Check if MongoDB service is started")
    print("   3. Verify connection string is correct")
    print("   4. For Windows: Check Services for 'MongoDB Server'")
    print("\n📖 Installation Guide:")
    print("   https://www.mongodb.com/docs/manual/installation/")
finally:
    # Close connection
    if 'client' in locals():
        client.close()
        print("\n✓ MongoDB connection closed")
