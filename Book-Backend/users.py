from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from response import Message
from database import *
from models import *
from pydantic import ValidationError
from pymongo.errors import PyMongoError
import json
from bson import json_util


users_bp = Blueprint('users', __name__)


@users_bp.route("/register", methods=["POST"])
def register():
    new_user = request.get_json()
    try:
        user = UserModel(**new_user)
    except ValidationError as e:
        return jsonify(Message.format_message('Validation Error', False, e.errors())), 400

    if not user.username or not user.password:
        return jsonify(Message.format_message('Username and password are required', False, None)), 400

    existing_user = user_model.find_user_by_username(user.username)
    if existing_user:
        return jsonify(Message.format_message('Username already exists', False, None)), 409

    user_model.create_user(user)
    return jsonify(Message.format_message('User created successfully', True, None)), 200

    

@users_bp.route("/login", methods=["POST"])
def login():
    login_details = request.get_json()
    try:
        user = UserModel(**login_details)
    except ValidationError as e:
        return jsonify(Message.format_message('Validation Error', False, e.errors())), 400

    if not user.username or not user.password:
        return jsonify(Message.format_message('Username and password are required', False, None)), 400

    current_user = user_model.find_user_by_username(user.username)

    if current_user and user_model.check_password(current_user, user.password):
        access_token = create_access_token(identity=user.username)
        return jsonify(Message.format_message('Logged in successfully', True, {"access_token":access_token})), 200

    return jsonify(Message.format_message('Username and password are incorrect', False, None)), 401
    

@users_bp.route("/admin-login", methods=["POST"])
def admin_login():
    login_details = request.get_json()
    try:
        user = UserModel(**login_details)
    except ValidationError as e:
        return jsonify(Message.format_message('Validation Error', False, e.errors())), 400

    if not user.username or not user.password:
        return jsonify(Message.format_message('Username and password are required', False, None)), 400

    current_user = user_model.find_user_by_username(user.username)

    if current_user and user_model.check_password(current_user, user.password):
        if current_user['type'] == "admin":
            access_token = create_access_token(identity=user.username)
            return jsonify(Message.format_message('Admin logged in successfully', True, {"access_token":access_token})), 200
        else:
            return jsonify(Message.format_message('You are not admin', False, None)), 401

    return jsonify(Message.format_message('Username and password are incorrect', False, None)), 401


@users_bp.get("/get-profile")
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()  # Get the user ID from the JWT token


    try:
        # Check if the item is already in the user's cart
        user = users_collection.find_one({'username': user_id}, {'_id': 0})

        print(user)
        return jsonify(Message.format_message('Profile obtained successfully', True, user)), 200

    except PyMongoError as e:
        return jsonify(Message.format_message('Error occurred while processing the request', False)), 500
