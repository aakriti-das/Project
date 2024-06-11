from pymongo import MongoClient
from models import User

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/library")
db = client["library"]

# collections
users_collection = db["users"]
books_collection = db["books"]
reviews_collection = db["reviews"]
carts_collection = db["carts"]


# model instances
user_model = User(users_collection)
book_model = User(books_collection)
review_model = User(reviews_collection)
cart_model = User(carts_collection)