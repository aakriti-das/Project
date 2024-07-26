import datetime

from auth import expired_token_response_callback, unauthorized_response_callback
from books import books_bp
from database import *
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from models import User
from pymongo import MongoClient
from response import Message
from users import users_bp

app = Flask(__name__)
CORS(app)

jwt = JWTManager(app)
jwt.unauthorized_loader(unauthorized_response_callback)
jwt.expired_token_loader(expired_token_response_callback)
app.config["JWT_SECRET_KEY"] = "aakriti"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(
    days=1
)  # define the life span of the token

# register other routes
app.register_blueprint(users_bp)
app.register_blueprint(books_bp)


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
