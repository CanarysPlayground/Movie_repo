# MongoDB Setup Guide for Movie Website

## MongoDB Connection Strings

### 1. **Local MongoDB** (Recommended for Development)
```
mongodb://localhost:27017/
```

### 2. **MongoDB Atlas** (Cloud - Free Tier Available)
```
mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### 3. **MongoDB with Authentication**
```
mongodb://<username>:<password>@localhost:27017/
```

---

## Installation Steps

### Step 1: Install MongoDB Locally (Option A)

**Windows:**
1. Download MongoDB Community Server from: https://www.mongodb.com/try/download/community
2. Run the installer (choose Complete installation)
3. MongoDB will run as a Windows service automatically
4. Default connection: `mongodb://localhost:27017/`

**OR use MongoDB Atlas (Option B - Cloud)**
1. Sign up for free at: https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get your connection string from Atlas dashboard

### Step 2: Install Python Dependencies

```powershell
pip install -r requirements.txt
```

Or install individually:
```powershell
pip install Flask==2.2.5
pip install pymongo==4.6.0
```

### Step 3: Run the Application

```powershell
python app_mongodb.py
```

---

## Connection String Configuration

Edit `app_mongodb.py` and update the connection string:

```python
# For local MongoDB:
MONGODB_URI = "mongodb://localhost:27017/"

# For MongoDB Atlas:
MONGODB_URI = "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

# For local MongoDB with authentication:
MONGODB_URI = "mongodb://admin:password123@localhost:27017/"
```

---

## Database Schema

### Database: `movie_website_db`

### Collection: `movies`
```json
{
  "_id": ObjectId("..."),
  "title": "The Shawshank Redemption",
  "year": 1994,
  "genre": "Drama",
  "synopsis": "Two imprisoned men bond over a number of years..."
}
```

### Collection: `playlist`
```json
{
  "_id": ObjectId("..."),
  "movie_id": "507f1f77bcf86cd799439011",
  "title": "The Shawshank Redemption",
  "year": 1994,
  "genre": "Drama"
}
```

---

## Sample Data

The application automatically creates 5 sample movies on first run:

1. **The Shawshank Redemption** (1994) - Drama
2. **The Godfather** (1972) - Crime
3. **The Dark Knight** (2008) - Action
4. **Inception** (2010) - Sci-Fi
5. **Pulp Fiction** (1994) - Crime

---

## API Endpoints

### Movies
- `GET /api/movies` - List all movies
- `GET /api/movies/<id>` - Get movie details
- `POST /api/movies` - Add new movie
- `PUT /api/movies/<id>` - Update movie
- `DELETE /api/movies/<id>` - Delete movie
- `GET /api/movies/search?q=<query>&genre=<genre>&year=<year>` - Search movies

### Playlist
- `GET /api/playlist` - Get playlist
- `POST /api/playlist` - Add movie to playlist (body: `{"movie_id": "..."}`)
- `DELETE /api/playlist/<movie_id>` - Remove from playlist

---

## Testing with MongoDB Shell

Connect to MongoDB:
```bash
mongosh
```

View databases:
```javascript
show dbs
```

Use your database:
```javascript
use movie_website_db
```

View collections:
```javascript
show collections
```

View all movies:
```javascript
db.movies.find().pretty()
```

Add a movie manually:
```javascript
db.movies.insertOne({
  title: "Interstellar",
  year: 2014,
  genre: "Sci-Fi",
  synopsis: "A team of explorers travel through a wormhole in space..."
})
```

Count documents:
```javascript
db.movies.countDocuments()
```

Delete all data:
```javascript
db.movies.deleteMany({})
db.playlist.deleteMany({})
```

---

## Testing with cURL

### List all movies:
```bash
curl http://localhost:5000/api/movies
```

### Add a new movie:
```bash
curl -X POST http://localhost:5000/api/movies \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Interstellar",
    "year": 2014,
    "genre": "Sci-Fi",
    "synopsis": "A team of explorers travel through a wormhole in space."
  }'
```

### Search movies:
```bash
curl "http://localhost:5000/api/movies/search?q=dark&genre=Action"
```

---

## Troubleshooting

### Error: "pymongo not installed"
```powershell
pip install pymongo
```

### Error: "Connection refused"
- Make sure MongoDB is running
- Check if MongoDB service is started (Windows Services)
- Verify connection string is correct

### Error: "Authentication failed"
- Check username and password in connection string
- Verify user has correct permissions in MongoDB

### Port 27017 already in use
- Another MongoDB instance might be running
- Change the port in connection string: `mongodb://localhost:27018/`

---

## Migration from SQLite to MongoDB

The original SQLite version is in `app.py`. The MongoDB version is in `app_mongodb.py`.

**Key Differences:**
- MongoDB uses `ObjectId` instead of auto-increment IDs
- No schema enforcement (flexible documents)
- Better scalability and performance
- Native JSON support
- Rich query capabilities

---

## Production Deployment

For production, use:
1. **MongoDB Atlas** (managed cloud service)
2. Enable authentication
3. Use environment variables for connection string:

```python
import os
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
```

4. Add connection pooling and error handling
5. Implement data validation
6. Enable SSL/TLS for connections

---

## Resources

- MongoDB Official Docs: https://www.mongodb.com/docs/
- PyMongo Documentation: https://pymongo.readthedocs.io/
- MongoDB Atlas Free Tier: https://www.mongodb.com/cloud/atlas
- MongoDB Compass (GUI): https://www.mongodb.com/products/compass
