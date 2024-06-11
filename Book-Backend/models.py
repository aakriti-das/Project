# models.py
from pymongo.collection import Collection
import hashlib
from pydantic import BaseModel

class UserModel(BaseModel):
    username: str
    password: str
    type: str = "customer"

class BookModel(BaseModel):
    isbn: str
    name: str
    published_date: str
    author_name: str
    category: str
    description: str
    image_url: str = None
    rating: int = 0
    price: int

class BookRatingRequest(BaseModel):
    isbn: str
    rating: int = 0

class BookReview(BaseModel):
    isbn: str
    comment: str

class CartItemModel(BaseModel):
    user_id: str
    book_isbn: str
    quantity: int


class User:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_user(self, user_model: UserModel):
        encrypted_password = hashlib.sha256(user_model.password.encode("utf-8")).hexdigest()
        user_data = {
            'username': user_model.username,
            'password': encrypted_password,
            'type': user_model.type
        }
        return self.collection.insert_one(user_data)

    def find_user_by_username(self, username):
        return self.collection.find_one({'username': username})

    def check_password(self, user, password):
        encrypted_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return user['password'] == encrypted_password
    
