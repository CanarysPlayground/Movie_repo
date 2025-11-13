"""
Quick MongoDB Connection Test
Replace the MONGODB_URI with your actual connection string
"""

from pymongo import MongoClient
import sys

# ============================================
# 🔧 CONFIGURATION - UPDATE THIS LINE:
# ============================================
MONGODB_URI = "mongodb://localhost:27017/"

# For MongoDB Atlas, use:
# MONGODB_URI = "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/"

print("=" * 60)
print("🔌 MongoDB Connection Test")
print("=" * 60)
print(f"\nAttempting to connect to: {MONGODB_URI}")
print("\nTesting connection...")

try:
    # Try to connect with a timeout
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    
    # Test the connection
    client.admin.command('ping')
    
    print("✅ SUCCESS! MongoDB connection established!")
    
    # Get database list
    databases = client.list_database_names()
    print(f"\n📊 Available databases ({len(databases)}):")
    for db_name in databases:
        print(f"   • {db_name}")
    
    # Check if our database exists
    if "movie_website_db" in databases:
        db = client["movie_website_db"]
        collections = db.list_collection_names()
        print(f"\n🎬 Movie Website Database found!")
        print(f"   Collections: {', '.join(collections) if collections else 'None'}")
        
        # Count documents
        if "movies" in collections:
            count = db["movies"].count_documents({})
            print(f"   Movies: {count}")
        
        if "playlist" in collections:
            count = db["playlist"].count_documents({})
            print(f"   Playlist: {count}")
    else:
        print(f"\n⚠️  'movie_website_db' not found. Run insert_mongodb_data.py to create it.")
    
    print("\n" + "=" * 60)
    print("✅ Connection test completed successfully!")
    print("=" * 60)
    print("\n📌 Your connection string is valid:")
    print(f"   {MONGODB_URI}")
    print("\n🚀 You can now run:")
    print("   python insert_mongodb_data.py  # Insert sample data")
    print("   python app_mongodb.py          # Start the application")
    
    client.close()
    sys.exit(0)
    
except Exception as e:
    print("❌ FAILED! Could not connect to MongoDB")
    print(f"\nError: {str(e)}")
    print("\n" + "=" * 60)
    print("🛠️  TROUBLESHOOTING:")
    print("=" * 60)
    
    if "localhost" in MONGODB_URI:
        print("\n📍 Local MongoDB (localhost) detected:")
        print("   1. Is MongoDB installed? Download from:")
        print("      https://www.mongodb.com/try/download/community")
        print("\n   2. Is MongoDB service running? Check with:")
        print("      Get-Service -Name MongoDB")
        print("\n   3. Start MongoDB service:")
        print("      Start-Service MongoDB")
        print("\n   4. Or use MongoDB Atlas (cloud - free):")
        print("      https://www.mongodb.com/cloud/atlas/register")
    
    elif "mongodb+srv" in MONGODB_URI:
        print("\n☁️  MongoDB Atlas detected:")
        print("   1. Verify your connection string is correct")
        print("   2. Check username and password")
        print("   3. Ensure your IP is whitelisted:")
        print("      - Go to Network Access in Atlas")
        print("      - Add your IP or use 0.0.0.0/0 (allow all)")
        print("   4. Check your internet connection")
    
    else:
        print("\n🔧 General tips:")
        print("   1. Verify your connection string format")
        print("   2. Check if MongoDB server is accessible")
        print("   3. Test network connectivity")
    
    print("\n📖 See MONGODB_CONNECTION_GUIDE.md for detailed setup instructions")
    print("=" * 60)
    
    client.close() if 'client' in locals() else None
    sys.exit(1)
