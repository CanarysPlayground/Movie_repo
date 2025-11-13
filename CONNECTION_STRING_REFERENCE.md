# 🔌 MongoDB Connection Strings - Quick Reference

## Connection String Formats

### **Local MongoDB (Default)**
```
mongodb://localhost:27017/
```
- Used when MongoDB is installed on your computer
- Default port: 27017
- No authentication required (development)

---

### **Local MongoDB with Authentication**
```
mongodb://username:password@localhost:27017/
```
- Example: `mongodb://admin:secret123@localhost:27017/`
- Used when you've set up authentication on local MongoDB

---

### **MongoDB Atlas (Cloud)**
```
mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```
- Example: `mongodb+srv://movieuser:moviepass123@cluster0.ab1cd.mongodb.net/?retryWrites=true&w=majority`
- Free tier available (no credit card required)
- Managed service (no installation needed)
- ⭐ **RECOMMENDED for quick setup**

---

### **MongoDB Atlas with Database Name**
```
mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority
```
- Example: `mongodb+srv://movieuser:pass@cluster0.ab1cd.mongodb.net/movie_website_db?retryWrites=true&w=majority`
- Explicitly specifies the database to use

---

### **Docker MongoDB**
```
mongodb://localhost:27017/
```
- Same as local MongoDB
- Run container: `docker run -d -p 27017:27017 mongo`

---

### **MongoDB with Custom Port**
```
mongodb://localhost:27018/
```
- Used when MongoDB runs on a non-standard port

---

### **Multiple Hosts (Replica Set)**
```
mongodb://host1:27017,host2:27017,host3:27017/?replicaSet=myReplicaSet
```
- For high availability setups

---

## Complete Connection String Anatomy

```
mongodb+srv://username:password@host:port/database?options
          │         │         │     │      │        │
          │         │         │     │      │        └─ Connection options
          │         │         │     │      └────────── Database name (optional)
          │         │         │     └───────────────── Port (default: 27017)
          │         │         └─────────────────────── Hostname/cluster URL
          │         └───────────────────────────────── Password
          └─────────────────────────────────────────── Username
```

---

## Common Connection Options

### **Basic Options**
```
?retryWrites=true&w=majority
```
- `retryWrites=true` - Automatically retry failed writes
- `w=majority` - Write concern (wait for acknowledgment from majority of nodes)

### **Timeout Options**
```
?connectTimeoutMS=5000&socketTimeoutMS=30000
```
- `connectTimeoutMS` - Connection timeout in milliseconds
- `socketTimeoutMS` - Socket timeout in milliseconds

### **SSL/TLS**
```
?ssl=true&tls=true
```
- Enable secure connections

### **Authentication Database**
```
?authSource=admin
```
- Specify which database to authenticate against

---

## Example Configurations

### **Development (No Auth)**
```python
MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "movie_website_db"
```

### **Development (With Auth)**
```python
MONGODB_URI = "mongodb://devuser:devpass@localhost:27017/"
DB_NAME = "movie_website_db"
```

### **Production (MongoDB Atlas)**
```python
MONGODB_URI = "mongodb+srv://produser:strongpass@cluster0.xxxxx.mongodb.net/movie_website_db?retryWrites=true&w=majority&ssl=true"
DB_NAME = "movie_website_db"
```

### **Using Environment Variables**
```python
import os
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'movie_website_db')
```

---

## Where to Use the Connection String

### **1. app_mongodb.py (Line 9)**
```python
MONGODB_URI = "YOUR_CONNECTION_STRING_HERE"
```

### **2. insert_mongodb_data.py (Line 9)**
```python
MONGODB_URI = "YOUR_CONNECTION_STRING_HERE"
```

### **3. test_connection.py (Line 10)**
```python
MONGODB_URI = "YOUR_CONNECTION_STRING_HERE"
```

---

## Getting Your Connection String

### **MongoDB Atlas (Cloud):**
1. Login to https://cloud.mongodb.com
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string
5. Replace `<password>` with your actual password

### **Local MongoDB:**
1. Default: `mongodb://localhost:27017/`
2. No setup needed if MongoDB is running

### **Verify It Works:**
```powershell
python test_connection.py
```

---

## Security Notes

### ⚠️ **Never commit credentials to Git!**

**Bad (Hardcoded):**
```python
MONGODB_URI = "mongodb+srv://myuser:mypassword@cluster.net/"
```

**Good (Environment Variables):**
```python
import os
MONGODB_URI = os.getenv('MONGODB_URI')
```

### **Set Environment Variable (PowerShell):**
```powershell
$env:MONGODB_URI = "mongodb+srv://user:pass@cluster.net/"
```

### **Set Environment Variable (CMD):**
```cmd
set MONGODB_URI=mongodb+srv://user:pass@cluster.net/
```

### **.env File (with python-dotenv):**
```
MONGODB_URI=mongodb+srv://user:pass@cluster.net/
DB_NAME=movie_website_db
```

```python
from dotenv import load_dotenv
load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
```

---

## Troubleshooting Connection Strings

### **Error: Invalid URI**
- Check for typos in the connection string
- Ensure proper URL encoding for special characters in password
- Verify the protocol (mongodb:// or mongodb+srv://)

### **Error: Authentication Failed**
- Double-check username and password
- Ensure user exists in database
- Verify password doesn't contain unencoded special characters

### **URL Encode Special Characters:**
```python
from urllib.parse import quote_plus

username = quote_plus("user@email.com")
password = quote_plus("p@ssw0rd!")

MONGODB_URI = f"mongodb+srv://{username}:{password}@cluster.net/"
```

### **Error: Connection Timeout**
- Verify MongoDB is running
- Check firewall settings
- For Atlas: Ensure IP is whitelisted
- Test internet connection

---

## Quick Test Commands

### **Test Connection (Python):**
```python
from pymongo import MongoClient
client = MongoClient("YOUR_CONNECTION_STRING")
client.admin.command('ping')
print("Connected!")
```

### **Test Connection (MongoDB Shell):**
```bash
mongosh "YOUR_CONNECTION_STRING"
```

### **Test with Our Script:**
```powershell
python test_connection.py
```

---

## Need Help?

📖 **Full Guides:**
- `MONGODB_CONNECTION_GUIDE.md` - Complete setup instructions
- `MONGODB_SETUP.md` - Technical reference
- `MONGODB_SUMMARY.md` - Quick start guide

🧪 **Test Your Connection:**
```powershell
python test_connection.py
```

🌐 **MongoDB Resources:**
- Atlas Dashboard: https://cloud.mongodb.com
- Documentation: https://docs.mongodb.com
- University (Free): https://university.mongodb.com

---

**Remember:** Use MongoDB Atlas for the easiest setup! No installation required. 🚀
