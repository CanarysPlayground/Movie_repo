# 🎬 Movie Website - MongoDB Connection & Setup

## 📌 MongoDB Connection Strings

### **Option 1: Local MongoDB** (Requires Installation)
```
mongodb://localhost:27017/
```

### **Option 2: MongoDB Atlas** (Cloud - FREE, No Installation Required) ⭐ RECOMMENDED
```
mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### **Option 3: Docker MongoDB** (If you have Docker installed)
```
mongodb://localhost:27017/
```

---

## 🚀 Quick Start Guide

### Option A: Using MongoDB Atlas (Cloud - Easiest) ⭐

**Step 1: Sign up for MongoDB Atlas**
1. Go to: https://www.mongodb.com/cloud/atlas/register
2. Create a free account (no credit card required)
3. Choose "Free" tier (M0 Sandbox)

**Step 2: Create a Cluster**
1. Choose a cloud provider (AWS, Google Cloud, or Azure)
2. Select a region close to you
3. Click "Create Cluster" (takes 3-5 minutes)

**Step 3: Create Database User**
1. Click "Database Access" in left menu
2. Click "Add New Database User"
3. Username: `movieuser`
4. Password: `moviepass123` (or create your own)
5. Set role to "Atlas Admin" or "Read and write to any database"

**Step 4: Whitelist Your IP**
1. Click "Network Access" in left menu
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (0.0.0.0/0) for development
4. Click "Confirm"

**Step 5: Get Connection String**
1. Click "Database" in left menu
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string (looks like):
   ```
   mongodb+srv://movieuser:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with your actual password

**Step 6: Update app_mongodb.py**
```python
# Replace this line in app_mongodb.py:
MONGODB_URI = "mongodb+srv://movieuser:moviepass123@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
```

**Step 7: Run the Application**
```powershell
python app_mongodb.py
```

---

### Option B: Install MongoDB Locally (Windows)

**Step 1: Download MongoDB**
- Go to: https://www.mongodb.com/try/download/community
- Select Version: 7.0 or latest
- Platform: Windows
- Package: MSI
- Click "Download"

**Step 2: Install MongoDB**
1. Run the downloaded `.msi` file
2. Choose "Complete" installation
3. ✅ Check "Install MongoDB as a Service"
4. ✅ Check "Install MongoDB Compass" (GUI tool)
5. Click "Install"

**Step 3: Verify Installation**
```powershell
# Check if MongoDB service is running
Get-Service -Name MongoDB
```

**Step 4: Test Connection**
```powershell
# Connect to MongoDB shell
mongosh
```

**Step 5: Run Data Insertion**
```powershell
python insert_mongodb_data.py
```

**Step 6: Run Application**
```powershell
python app_mongodb.py
```

---

### Option C: Using Docker (Quick Setup)

**Step 1: Run MongoDB Container**
```powershell
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**Step 2: Insert Data**
```powershell
python insert_mongodb_data.py
```

**Step 3: Run Application**
```powershell
python app_mongodb.py
```

---

## 📝 Complete Example with MongoDB Atlas

### 1. Connection String Format

```python
# General format:
mongodb+srv://<username>:<password>@<cluster-url>/<database>?retryWrites=true&w=majority

# Example:
MONGODB_URI = "mongodb+srv://movieuser:moviepass123@cluster0.ab1cd.mongodb.net/movie_website_db?retryWrites=true&w=majority"
```

### 2. Update app_mongodb.py

```python
# Line 9-10 in app_mongodb.py, replace with your Atlas connection string:
MONGODB_URI = "mongodb+srv://movieuser:moviepass123@cluster0.ab1cd.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "movie_website_db"
```

### 3. Update insert_mongodb_data.py

```python
# Line 9 in insert_mongodb_data.py:
MONGODB_URI = "mongodb+srv://movieuser:moviepass123@cluster0.ab1cd.mongodb.net/?retryWrites=true&w=majority"
```

### 4. Run the scripts

```powershell
# Insert sample data
python insert_mongodb_data.py

# Start the web application
python app_mongodb.py
```

---

## 🎯 Test Your Connection

### Test Script (save as test_connection.py):

```python
from pymongo import MongoClient

# YOUR CONNECTION STRING HERE:
MONGODB_URI = "mongodb+srv://movieuser:moviepass123@cluster0.xxxxx.mongodb.net/"

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
    print(f"Databases: {client.list_database_names()}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

Run:
```powershell
python test_connection.py
```

---

## 📊 Sample Data Structure

### Movies Collection:
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "title": "The Shawshank Redemption",
  "year": 1994,
  "genre": "Drama",
  "synopsis": "Two imprisoned men bond over a number of years...",
  "rating": 9.3,
  "director": "Frank Darabont",
  "created_at": ISODate("2024-01-15T10:30:00Z")
}
```

### Playlist Collection:
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439012"),
  "movie_id": "507f1f77bcf86cd799439011",
  "title": "The Shawshank Redemption",
  "year": 1994,
  "genre": "Drama",
  "added_at": ISODate("2024-01-15T10:30:00Z")
}
```

---

## 🧪 API Testing

### Using PowerShell:

```powershell
# Get all movies
Invoke-RestMethod -Uri "http://localhost:5000/api/movies" -Method Get

# Add a new movie
$body = @{
    title = "Interstellar"
    year = 2014
    genre = "Sci-Fi"
    synopsis = "A team of explorers travel through a wormhole."
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/movies" -Method Post -Body $body -ContentType "application/json"

# Search movies
Invoke-RestMethod -Uri "http://localhost:5000/api/movies/search?q=dark" -Method Get
```

### Using cURL:

```bash
# Get all movies
curl http://localhost:5000/api/movies

# Add a new movie
curl -X POST http://localhost:5000/api/movies \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Interstellar\",\"year\":2014,\"genre\":\"Sci-Fi\",\"synopsis\":\"A team of explorers travel through a wormhole.\"}"

# Search movies
curl "http://localhost:5000/api/movies/search?q=dark"
```

---

## 🔍 MongoDB Compass (GUI Tool)

MongoDB Compass is a free GUI tool for MongoDB:

1. **Download**: https://www.mongodb.com/try/download/compass
2. **Install** the application
3. **Connect** using your connection string
4. **Browse** your data visually
5. **Run queries** with a visual interface

**Connection String for Compass:**
- Local: `mongodb://localhost:27017`
- Atlas: `mongodb+srv://movieuser:moviepass123@cluster0.xxxxx.mongodb.net/`

---

## 🛠️ MongoDB Shell Commands

```javascript
// Connect to your database
use movie_website_db

// Show all collections
show collections

// View all movies
db.movies.find().pretty()

// Count movies
db.movies.countDocuments()

// Find movies by genre
db.movies.find({genre: "Sci-Fi"})

// Find movies by year
db.movies.find({year: 1994})

// Add a movie
db.movies.insertOne({
  title: "The Matrix",
  year: 1999,
  genre: "Sci-Fi",
  synopsis: "A computer hacker learns about the true nature of reality.",
  rating: 8.7,
  director: "Lana Wachowski, Lilly Wachowski"
})

// Update a movie
db.movies.updateOne(
  {title: "The Matrix"},
  {$set: {rating: 8.8}}
)

// Delete a movie
db.movies.deleteOne({title: "The Matrix"})

// Clear all data
db.movies.deleteMany({})
db.playlist.deleteMany({})
```

---

## 🔐 Security Best Practices

### For Production:

1. **Use Environment Variables:**
```python
import os
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
```

2. **Set in PowerShell:**
```powershell
$env:MONGODB_URI = "mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/"
python app_mongodb.py
```

3. **Create .env file:**
```
MONGODB_URI=mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/
```

4. **Use with python-dotenv:**
```python
from dotenv import load_dotenv
load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
```

---

## ❓ Troubleshooting

### Error: "No connection could be made"
- MongoDB service is not running
- Check Windows Services: `Get-Service -Name MongoDB`
- Start service: `Start-Service MongoDB`

### Error: "Authentication failed"
- Wrong username or password
- Check database user in Atlas dashboard
- Verify password doesn't have special characters (URL encode if needed)

### Error: "IP not whitelisted"
- Add your IP to Network Access in Atlas
- Use 0.0.0.0/0 for testing (allow all IPs)

### Error: "pymongo not installed"
```powershell
pip install pymongo
```

### Connection timeout with Atlas
- Check your internet connection
- Verify the connection string is correct
- Ensure Network Access allows your IP

---

## 📚 Additional Resources

- **MongoDB Documentation**: https://www.mongodb.com/docs/
- **PyMongo Documentation**: https://pymongo.readthedocs.io/
- **MongoDB University** (Free Courses): https://university.mongodb.com/
- **MongoDB Atlas Tutorial**: https://www.mongodb.com/basics/mongodb-atlas-tutorial

---

## 🎉 Next Steps

1. ✅ Choose MongoDB Atlas (easiest) or install locally
2. ✅ Get your connection string
3. ✅ Update `app_mongodb.py` with your connection string
4. ✅ Run `python insert_mongodb_data.py` to create sample data
5. ✅ Run `python app_mongodb.py` to start the application
6. ✅ Visit http://localhost:5000 in your browser
7. ✅ Test the API endpoints

**Recommended: Use MongoDB Atlas for the quickest setup!** 🚀
