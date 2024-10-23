from pymongo import MongoClient

connection_string = f"mongodb+srv://victorabuke:BoogeymaN1%2A@tutorial.mzgufcd.mongodb.net/?retryWrites=true&w=majority&appName=tutorial"
client = MongoClient(connection_string)

db = client['EduTrack']
users = db['users']
db_names = db.list_collection_names()
print(db)

