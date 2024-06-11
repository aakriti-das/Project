# Library System (Flask API)

This is a Flask API project that provides endpoints for user registration, login, book management, and customer cart functionality using MongoDB as the database.

## Introduction

This Flask project implements a RESTful API that allows users to register, login, manage books, and add books to their cart in a simple library system. Users can create an account, login with their credentials, and perform CRUD (Create, Read, Update, Delete) operations on books in the library. Additionally, customers can add books to their cart to keep track of items they wish to purchase.

The project uses Flask as the web framework, PyMongo for MongoDB integration, and Flask-JWT-Extended for JSON Web Token (JWT) authentication.

## Prerequisites

Before running this project, make sure you have the following prerequisites:

- Python 3.6 or later installed
- MongoDB installed and running
- `pip` package manager installed

## Installation

1. Clone the repository to your local machine:

```bash
    git clone https://github.com/Roshan54321/Library-System-Backend.git
    cd Library-System-Backend
```

2. Install the required dependencies:

```bash
    pip install -r requirements.txt
```

3. Create a .env file in the root directory of the project and set the following environment variables:

```bash
    JWT_SECRET_KEY=your_secret_key_here
    JWT_ACCESS_TOKEN_EXPIRES=1
    MONGO_URI=your_mongodb_uri_here
```


## Usage

To run the Flask application, execute the following command:

```bash
    python main.py
```


## Dependencies

<ul>
<li>Flask</li>
<li>PyMongo</li>
<li>Flask-JWT-Extended</li>
<li>python-dotenv</li>
</ul>



## License

This project is licensed under the <u style="color: blue;">MIT License</u>.