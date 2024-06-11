from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from pymongo import DESCENDING
from models import *
from response import Message
from database import *
from pydantic import ValidationError
from pymongo.errors import PyMongoError
from auth import is_admin
from bson.json_util import dumps, RELAXED_JSON_OPTIONS



books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.get("/list")
def get_all_books():
    try:
        books = list(books_collection.find({}, {'_id': False}).sort('published_date', DESCENDING))
    except Exception as e:
        return jsonify(Message.format_message(f"Error while fetching books: {str(e)}", False)), 500

    return jsonify(Message.format_message('Successfully obtained books', True, books))


@books_bp.get("/newly-arrived")
def get_newly_arrived_book():
    limit = int(request.args.get('limit', 10))
    try:
        books = list(books_collection.find({}, {'_id': False}).sort('published_date', DESCENDING).limit(limit))
    except Exception as e:
        return jsonify(Message.format_message(f"Error while fetching newly arrived books: {str(e)}", False)), 500

    return jsonify(Message.format_message('Successfully obtained newly arrived books', True, books))



@books_bp.get("/details")
def get_book_details():
    isbn = request.args.get('isbn')
    if not isbn:
        return jsonify(Message.format_message('ISBN is required', False)), 400

    try:
        book = books_collection.find_one({'isbn': isbn}, {'_id': False})
    except Exception as e:
        return jsonify(Message.format_message(f"Error while fetching book details: {str(e)}", False)), 500

    if book:
        return jsonify(Message.format_message('Book details', True, book))
    else:
        return jsonify(Message.format_message(f'Could not find book with ISBN {isbn}', False))



@books_bp.post("/add-book")
@jwt_required()
def add_book():
    print("next check admin")
    if not is_admin():
        print("check admin")
        return jsonify(Message.format_message('Unauthorized to add a book', False)), 403
    
    print("next make model")
    try:
        print("make model")
        req = BookModel(**request.get_json())
    except ValidationError as e:
        print(e)
        return jsonify(Message.format_message('Validation Error', False, e.errors())), 400

    exist_book = books_collection.find_one({'isbn': req.isbn})

    if exist_book:
        print("books already exists")
        return jsonify(Message.format_message(f'Book with ISBN {req.isbn} already exists', False))

    try:
        book = books_collection.insert_one(req.dict())
        print("insert book")
    except Exception as e:
        print(e)
        return jsonify(Message.format_message(f"Error while adding the book: {str(e)}", False)), 500

    return jsonify(Message.format_message('Book added successfully', True))



@books_bp.post("/update-book")
@jwt_required()
def update_book():
    if not is_admin():
        return jsonify(Message.format_message('You do not have permission to perform this action', False)), 403

    req = request.get_json()
    print(req)
    
    isbn = req['isbn']
    book = books_collection.find_one({'isbn': isbn})
    print(book['isbn'])
    
    if not book:
        return jsonify(Message.format_message(f'Book with ISBN {isbn} not found', False)), 404

    update_data = {
        'name': req.get('name', book['name']),
        'published_date': req.get('published_date', book['published_date']),
        'author_name': req.get('author_name', book['author_name']),
        'category': req.get('category', book['category']),
        'description': req.get('description', book['description']),
        'image_url': req.get('image_url', book['image_url']),
        'rating': int(req.get('rating', book['rating'])),
        'price': int(req.get('price', book['price'])),
    }

    books_collection.update_one({'isbn': isbn}, {'$set': update_data})
    return jsonify(Message.format_message(f'Book with ISBN {isbn} updated successfully', True)), 200


@books_bp.get("/delete")
@jwt_required()
def delete_book():
    if not is_admin():
        return jsonify(Message.format_message('Unauthorized to add a book', False)), 403
    
    isbn = request.args.get('isbn')
    if not isbn:
        return jsonify(Message.format_message('ISBN is required', False)), 400

    try:
        book = books_collection.delete_one({"isbn": isbn})
    except Exception as e:
        return jsonify(Message.format_message(f"Error while deleting the book: {str(e)}", False)), 500

    return jsonify(Message.format_message("Book Deleted successfully", True))



@books_bp.post("/rating")
@jwt_required()
def book_rating():
    try:
        req = BookRatingRequest(**request.get_json())
    except ValidationError as e:
        return jsonify(Message.format_message('Validation Error', False, e.errors())), 400

    filter = {"isbn": req.isbn}
    update = {"$set": {"rating": req.rating}}
    try:
        book = books_collection.update_one(filter, update)
    except Exception as e:
        return jsonify(Message.format_message(f"Error while updating the book rating: {str(e)}", False)), 500

    return jsonify(Message.format_message(f"Rating updated to {req.rating}", True))



@books_bp.post("/add-review")
@jwt_required()
def add_book_review():
    try:
        req = BookReview(**request.get_json())
    except ValidationError as e:
        return jsonify(Message.format_message('Validation Error', False, e.errors())), 400

    try:
        book = reviews_collection.insert_one(req.dict())
    except Exception as e:
        return jsonify(Message.format_message(f"Error while adding the book review: {str(e)}", False)), 500

    return jsonify(Message.format_message("Review Added successfully", True))



@books_bp.post("/delete-review")
@jwt_required()
def delete_book_review():
    isbn = request.args.get('isbn')
    if not isbn:
        return jsonify(Message.format_message('ISBN is required', False)), 400

    try:
        book = reviews_collection.delete_one({"isbn": isbn})
    except Exception as e:
        return jsonify(Message.format_message(f"Error while deleting the book review: {str(e)}", False)), 500

    return jsonify(Message.format_message("Review Deleted successfully", True))



@books_bp.get("/get-review")
def get_book_review():
    isbn = request.args.get('isbn')
    if not isbn:
        return jsonify(Message.format_message('ISBN is required', False)), 400

    try:
        book = reviews_collection.find_one({"isbn": isbn}, {'_id': False})
    except Exception as e:
        return jsonify(Message.format_message(f"Error while fetching the book review: {str(e)}", False)), 500

    response = book if book else {
        "status": False,
        "msg": "Cannot find the review."
    }
    return jsonify(Message.format_message('Book review obtained successfully', True, response))


@books_bp.post("/add-to-cart")
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    try:
        req = CartItemModel(user_id=user_id, **request.get_json())
    except ValidationError as e:
        return jsonify(Message.format_message('Validation error', False, e.errors())), 400
    
    book_isbn = req.book_isbn
    quantity = req.quantity

    book = books_collection.find_one({'isbn': book_isbn})
    if not book:
        return jsonify(Message.format_message(f'Book with ISBN {book_isbn} not found', False)), 404

    try:
        # Check if the item is already in the user's cart
        cart_item = carts_collection.find_one({'user_id': user_id, 'book_isbn': book_isbn})
        if cart_item:
            # If the item is already in the cart, update its quantity
            new_quantity = cart_item['quantity'] + quantity
            carts_collection.update_one({'_id': cart_item['_id']}, {'$set': {'quantity': new_quantity}})
        else:
            # If the item is not in the cart, add it as a new cart item
            cart_item_data = {
                'user_id': user_id,
                'book_isbn': book_isbn,
                'quantity': quantity
            }
            carts_collection.insert_one(cart_item_data)
    except PyMongoError as e:
        return jsonify(Message.format_message('Error occurred while processing the request', False)), 500

    return jsonify(Message.format_message('Item added to cart successfully', True)), 200


@books_bp.post("/update-cart")
@jwt_required()
def update_cart():
    user_id = get_jwt_identity()  # Get the user_id from the JWT token
    req = request.get_json()
    print(req)

    book_isbn = req['book_isbn']
    quantity = req['quantity']

    try:
        cart_item = carts_collection.find_one({"user_id": user_id, "book_isbn": book_isbn})

        if cart_item:
            carts_collection.update_one(
                {"user_id": user_id, "book_isbn": book_isbn},
                {"$set": {"quantity": quantity}}
            )
            return jsonify(Message.format_message('Cart updated successfully', True))

        else:
            return jsonify(Message.format_message('Cart not found', False)), 404
        
    except PyMongoError as e:
        return jsonify(Message.format_message('Error occurred while processing the request', False)), 500


@books_bp.get("/get-cart-books")
@jwt_required()
def get_my_cart_books():
    user_id = get_jwt_identity()

    # Find the carts for the current user
    carts = carts_collection.find({"user_id": user_id})

    # Check if there are any carts
    if not carts:
        return jsonify(Message.format_message('Books not found in the cart', False, None)), 404

    # Create a list to hold the formatted cart items
    cart_items = []

    # Iterate through the carts and format the data
    for cart in carts:
        book = books_collection.find_one({"isbn": cart["book_isbn"]})
        if book:
            item = {
                "quantity": cart["quantity"],
                "book": {
                    "isbn": book["isbn"],
                    "name": book["name"],
                    "published_date": book["published_date"],
                    "author_name": book["author_name"],
                    "category": book["category"],
                    "description": book["description"],
                    "image_url": book["image_url"],
                    "rating": book["rating"],
                    "price": book["price"]
                }
            }
            cart_items.append(item)


    return jsonify(Message.format_message("Successfully retrieved cart items", True, cart_items)), 200


@books_bp.get("/get-cart")
@jwt_required()
def get_my_cart():
    user_id = get_jwt_identity()
    book_isbn = request.args.get('isbn')

    try:
        # Find the carts for the current user
        cart = carts_collection.find_one({"user_id": user_id, "book_isbn": book_isbn}, {"_id": 0})
        print(cart)

    except PyMongoError as e:
        return jsonify(Message.format_message('Error occurred while processing the request', False)), 500


    return jsonify(Message.format_message("Successfully retrieved cart", True, cart)), 200


@books_bp.get("/get-book")
def get_book():
    book_isbn = request.args.get('isbn')
    try:
        book = books_collection.find_one({"isbn": book_isbn}, {"_id": 0})

    except PyMongoError as e:
        return jsonify(Message.format_message('Error occurred while processing the request', False)), 500


    return jsonify(Message.format_message('Successfully obtained books', True, book))


@books_bp.get("/delete-cart")
@jwt_required()
def delete_cart():
    user_id = get_jwt_identity()
    book_isbn = request.args.get('isbn')

    try:
        # Find the carts for the current user
        cart = carts_collection.delete_one({"user_id": user_id, "book_isbn": book_isbn})

    except PyMongoError as e:
        return jsonify(Message.format_message('Error occurred while processing the request', False)), 500


    return jsonify(Message.format_message("Successfully deleted cart", True, None)), 200




@books_bp.get("/get-carts-price")
@jwt_required()
def get_my_carts_price():
    user_id = get_jwt_identity()

    # Find the carts for the current user
    carts = carts_collection.find({"user_id": user_id})

    # Check if there are any carts
    if not carts:
        return jsonify(Message.format_message('Books not found in the cart', False, None)), 404

    # Create a list to hold the formatted cart items
    data = {
        'price': 0,
        'quantity': 0
    }

    # Iterate through the carts and format the data
    for cart in carts:
        book = books_collection.find_one({"isbn": cart["book_isbn"]})
        if book:
            data['price'] = data['price'] + book["price"] * cart["quantity"]
            data['quantity'] = data['quantity'] + cart["quantity"]


    return jsonify(Message.format_message("Successfully retrieved carts price", True, data)), 200