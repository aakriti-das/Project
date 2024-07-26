from database import users_collection
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from response import Message


# Custom response for JWT authentication errors
def unauthorized_response_callback(error_str):
    return jsonify(Message.format_message("Missing or invalid token", False, None)), 401


# Custom response for JWT expired tokens
def expired_token_response_callback(jwt_header, jwt_data):
    return jsonify(Message.format_message("Token has expired", False, None)), 401


def is_admin():
    current_username = get_jwt_identity()
    user = users_collection.find_one({"username": current_username})
    if user and user.get("type") == "admin":
        return True
    return False
