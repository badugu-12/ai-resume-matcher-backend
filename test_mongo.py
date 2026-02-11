from pymongo import MongoClient

uri = "mongodb+srv://bhanubadugu95_db_user:qNhZ6rs9P2ZqZnjS@cluster0.x5fvbwt.mongodb.net/resume_matcher"
client = MongoClient(uri)

print(client.list_database_names())
