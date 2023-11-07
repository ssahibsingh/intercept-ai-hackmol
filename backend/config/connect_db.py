import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def connect_to_mongodb():
    mongodb_uri = os.getenv("MONGODB_URI")
    if mongodb_uri:
        try:
            client = MongoClient(mongodb_uri)
            db = client.get_database("test")
            print("MongoDB Connected Successfully")
            return db
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
    else:
        print("MONGODB_URI not found in environment variables")
    return None
