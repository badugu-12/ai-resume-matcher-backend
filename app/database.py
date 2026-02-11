import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

print("MONGODB_URI =", MONGODB_URI)
print("DB_NAME =", DB_NAME)

if not DB_NAME:
    raise RuntimeError("❌ DB_NAME is not set in .env file")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

matches_collection = db["matches"]
users_collection = db["users"]
