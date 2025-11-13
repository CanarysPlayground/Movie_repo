# 🎬 MongoDB Setup Summary

## ✅ What's Been Created

### 1. **MongoDB Application Files**
- ✅ `app_mongodb.py` - Flask app with MongoDB integration
- ✅ `insert_mongodb_data.py` - Script to insert sample movie data
- ✅ `test_connection.py` - Quick connection test script

### 2. **Documentation Files**
- ✅ `MONGODB_SETUP.md` - Complete MongoDB setup guide
- ✅ `MONGODB_CONNECTION_GUIDE.md` - Detailed connection instructions

### 3. **Updated Files**
- ✅ `requirements.txt` - Added pymongo dependency

---

## 🔌 MongoDB Connection Strings

### **For Local MongoDB:**
```
mongodb://localhost:27017/
```

### **For MongoDB Atlas (Cloud - Recommended):**
```
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### **Example (You need to replace with your actual connection string):**
```
mongodb+srv://movieuser:moviepass123@cluster0.ab1cd.mongodb.net/?retryWrites=true&w=majority
```

---

## 🚀 Quick Start (3 Steps)

### **Option A: MongoDB Atlas (Easiest - No Installation)**

#### Step 1: Get MongoDB Atlas Connection String
1. Sign up at: https://www.mongodb.com/cloud/atlas/register
2. Create a free cluster (takes 3-5 minutes)
3. Create database user (username: movieuser, password: moviepass123)
4. Whitelist your IP (0.0.0.0/0 for testing)
5. Copy your connection string

#### Step 2: Update app_mongodb.py
```python
# Line 9 in app_mongodb.py - Replace with YOUR connection string:
MONGODB_URI = "mongodb+srv://movieuser:moviepass123@cluster0.xxxxx.mongodb.net/"
```

Also update `insert_mongodb_data.py` line 9 with the same connection string.

#### Step 3: Run the Application
```powershell
# Test connection first
python test_connection.py

# Insert sample data (8 movies)
python insert_mongodb_data.py

# Start the Flask app
python app_mongodb.py
```

### **Option B: Local MongoDB (Requires Installation)**

#### Step 1: Install MongoDB
- Download from: https://www.mongodb.com/try/download/community
- Choose "Complete" installation
- ✅ Check "Install MongoDB as a Service"
- ✅ Check "Install MongoDB Compass" (GUI)

#### Step 2: Verify Installation
```powershell
# Check if MongoDB service is running
Get-Service -Name MongoDB

# If not running, start it:
Start-Service MongoDB
```

#### Step 3: Run the Application
```powershell
# Test connection
python test_connection.py

# Insert sample data
python insert_mongodb_data.py

# Start Flask app
python app_mongodb.py
```

---

## 📊 Sample Data Included

The `insert_mongodb_data.py` script creates **8 sample movies**:

1. **The Shawshank Redemption** (1994) - Drama - Rating: 9.3
2. **The Godfather** (1972) - Crime - Rating: 9.2
3. **The Dark Knight** (2008) - Action - Rating: 9.0
4. **Inception** (2010) - Sci-Fi - Rating: 8.8
5. **Pulp Fiction** (1994) - Crime - Rating: 8.9
6. **Interstellar** (2014) - Sci-Fi - Rating: 8.6
7. **The Matrix** (1999) - Sci-Fi - Rating: 8.7
8. **Forrest Gump** (1994) - Drama - Rating: 8.8

Each movie includes:
- Title, Year, Genre, Synopsis
- Rating, Director, Created timestamp

Plus 3 movies added to a sample playlist!

---

## 🎯 API Endpoints Available

### Movies Management:
```
GET    /api/movies              # List all movies
GET    /api/movies/<id>         # Get movie details
POST   /api/movies              # Add new movie
PUT    /api/movies/<id>         # Update movie
DELETE /api/movies/<id>         # Delete movie
GET    /api/movies/search       # Search movies
```

### Playlist Management:
```
GET    /api/playlist            # Get playlist
POST   /api/playlist            # Add to playlist
DELETE /api/playlist/<id>       # Remove from playlist
```

---

## 🧪 Testing Your Setup

### Test 1: Connection Test
```powershell
python test_connection.py
```
**Expected output:**
```
✅ SUCCESS! MongoDB connection established!
```

### Test 2: Insert Sample Data
```powershell
python insert_mongodb_data.py
```
**Expected output:**
```
✓ Inserted 8 movies
✓ Added 3 movies to playlist
```

### Test 3: Start Application
```powershell
python app_mongodb.py
```
**Expected output:**
```
✓ MongoDB ready!
* Running on http://127.0.0.1:5000
```

### Test 4: API Test (PowerShell)
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/movies" -Method Get
```

---

## 🔧 Configuration Files to Update

### 1. **app_mongodb.py** (Line 9)
```python
# CHANGE THIS:
MONGODB_URI = "mongodb://localhost:27017/"

# TO YOUR CONNECTION STRING:
MONGODB_URI = "mongodb+srv://movieuser:moviepass123@cluster0.xxxxx.mongodb.net/"
```

### 2. **insert_mongodb_data.py** (Line 9)
```python
# CHANGE THIS:
MONGODB_URI = "mongodb://localhost:27017/"

# TO YOUR CONNECTION STRING:
MONGODB_URI = "mongodb+srv://movieuser:moviepass123@cluster0.xxxxx.mongodb.net/"
```

### 3. **test_connection.py** (Line 10)
```python
# CHANGE THIS:
MONGODB_URI = "mongodb://localhost:27017/"

# TO YOUR CONNECTION STRING:
MONGODB_URI = "mongodb+srv://movieuser:moviepass123@cluster0.xxxxx.mongodb.net/"
```

---

## 📁 Project Structure

```
movie_website/
├── app.py                           # Original SQLite version
├── app_mongodb.py                   # ⭐ New MongoDB version
├── insert_mongodb_data.py           # ⭐ Data insertion script
├── test_connection.py               # ⭐ Connection test
├── requirements.txt                 # Updated with pymongo
├── MONGODB_SETUP.md                 # Setup guide
├── MONGODB_CONNECTION_GUIDE.md      # ⭐ Detailed connection guide
├── README.md                        # Original README
└── templates/
    └── index.html                   # Frontend
```

---

## ❓ Common Issues & Solutions

### Issue 1: "No connection could be made"
**Cause:** MongoDB is not running or not installed.

**Solution:**
- **For Local:** Check if MongoDB service is running: `Get-Service -Name MongoDB`
- **For Atlas:** Verify connection string and internet connection

### Issue 2: "Authentication failed"
**Cause:** Wrong username or password.

**Solution:**
- Check username and password in connection string
- Verify user exists in Atlas Database Access
- Ensure password doesn't contain special characters

### Issue 3: "IP not whitelisted"
**Cause:** Your IP is not allowed to connect to Atlas.

**Solution:**
- Go to Network Access in Atlas
- Add your IP or use 0.0.0.0/0 (allow all IPs)

### Issue 4: "pymongo not installed"
**Solution:**
```powershell
pip install pymongo
```

---

## 🎓 Learning Resources

### MongoDB Basics:
- **Official Docs:** https://www.mongodb.com/docs/
- **MongoDB University** (Free): https://university.mongodb.com/
- **PyMongo Tutorial:** https://pymongo.readthedocs.io/

### MongoDB Atlas:
- **Getting Started:** https://www.mongodb.com/basics/mongodb-atlas-tutorial
- **Free Tier Guide:** https://www.mongodb.com/cloud/atlas

---

## 🔐 Security Best Practices

### For Production:

1. **Never hardcode credentials:**
```python
import os
MONGODB_URI = os.getenv('MONGODB_URI')
```

2. **Use environment variables:**
```powershell
$env:MONGODB_URI = "mongodb+srv://user:pass@cluster.net/"
```

3. **Restrict IP access:**
- Don't use 0.0.0.0/0 in production
- Whitelist only necessary IPs

4. **Use strong passwords:**
- Mix of letters, numbers, symbols
- Avoid common words

5. **Enable encryption:**
- MongoDB Atlas uses TLS/SSL by default

---

## 📞 Getting Help

### Check the Documentation:
1. `MONGODB_CONNECTION_GUIDE.md` - Detailed setup guide
2. `MONGODB_SETUP.md` - Technical reference

### Test Your Setup:
```powershell
python test_connection.py
```

### View Detailed Error Messages:
The test script provides specific troubleshooting steps based on your error.

---

## ✅ Next Steps

1. **Choose your MongoDB option:**
   - ✅ MongoDB Atlas (Recommended - Easiest)
   - ✅ Local MongoDB (Requires installation)
   - ✅ Docker MongoDB (If you have Docker)

2. **Get your connection string**

3. **Update the 3 Python files** with your connection string:
   - `app_mongodb.py`
   - `insert_mongodb_data.py`
   - `test_connection.py`

4. **Test connection:**
   ```powershell
   python test_connection.py
   ```

5. **Insert sample data:**
   ```powershell
   python insert_mongodb_data.py
   ```

6. **Start the application:**
   ```powershell
   python app_mongodb.py
   ```

7. **Visit:** http://localhost:5000

---

## 🎉 You're Ready!

Once you complete the steps above, you'll have:
- ✅ A MongoDB database with 8 sample movies
- ✅ A Flask web application connected to MongoDB
- ✅ RESTful API endpoints for movies and playlists
- ✅ Search and filter functionality
- ✅ A working movie website!

**Need help?** Check `MONGODB_CONNECTION_GUIDE.md` for detailed instructions!

---

**Recommended:** Use MongoDB Atlas for the quickest setup! 🚀
