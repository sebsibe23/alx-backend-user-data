# 0x03. User Authentication Service

## Overview
This project, "0x03. User Authentication Service," focuses on creating a user authentication service using Flask and SQLAlchemy. The goal is to understand the mechanism of authentication by implementing it step-by-step, despite the industry best practice of using existing modules or frameworks like Flask-User for such tasks.

## Project Details
- **Start Date:** June 10, 2024, 6:00 AM
- **End Date:** June 14, 2024, 6:00 AM
- **Checker Release Date:** June 11, 2024, 6:00 AM
- **Auto Review:** At the deadline

## Objective
The primary objective of this project is to learn and understand the implementation of user authentication mechanisms in a Flask application. This includes declaring API routes, handling cookies, retrieving form data, and returning appropriate HTTP status codes.

## Learning Objectives
By the end of this project, I should be able to:
- Declare API routes in a Flask app.
- Get and set cookies.
- Retrieve request form data.
- Return various HTTP status codes.

## Key Concepts

### API Routes in Flask
- **Declaration:** Learn how to declare and handle different API routes in a Flask application. This involves defining endpoints and associating them with specific view functions to handle user authentication tasks such as registration, login, and logout.

### Cookies
- **Get and Set:** Understand how to manage cookies in a Flask application to maintain user sessions. This includes setting cookies upon successful login, retrieving them to verify user sessions, and clearing them during logout.

### Request Form Data
- **Retrieval:** Learn how to retrieve data from request forms submitted by users. This involves parsing form data to extract user credentials for authentication purposes.

### HTTP Status Codes
- **Response:** Learn how to return different HTTP status codes based on the outcome of the API requests. This includes returning appropriate codes for success (200 OK), client errors (400 Bad Request), and unauthorized access (401 Unauthorized).

## Resources
### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/): Comprehensive guide on using Flask for web development.
- [Requests Module](https://docs.python-requests.org/en/latest/): Guide on using the Requests module to handle HTTP requests.
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status): Detailed information on various HTTP status codes and their meanings.

## Requirements
- **Editors:** vi, vim, emacs
- **Environment:** Ubuntu 18.04 LTS, Python 3.7
- **File Requirements:**
  - All files should end with a new line.
  - The first line of all files should be exactly `#!/usr/bin/env python3`.
  - Use `pycodestyle` style (version 2.5).
  - Use SQLAlchemy 1.3.x for database interactions.
  - All files must be executable.
  - The length of files will be tested using `wc`.
  - All modules should have documentation that explains their purpose.
  - All classes should have documentation that explains their purpose.
  - All functions (inside and outside classes) should have documentation that explains their purpose.
  - Functions should be type annotated.
  - The Flask app should only interact with the `Auth` class and never directly with the database.
  - Only public methods of `Auth` and `DB` should be used outside these classes.

## Task
### User Authentication Service
- **Description:** Implement a user authentication service in a Flask application. This service should handle user registration, login, and logout functionalities.
- **Constraints:**
  - Use SQLAlchemy for all database interactions.
  - Ensure all code is documented and adheres to the specified style guidelines.
  - Implement type annotations for all functions.
  - Design the service so that the Flask app interacts only with the `Auth` class and never directly with the database.

### Example
```python
#!/usr/bin/env python3
"""
User Authentication Service
"""
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auth import Auth

app = Flask(__name__)

# Database setup
engine = create_engine('sqlite:///users.db')
Session = sessionmaker(bind=engine)
session = Session()

auth = Auth(session)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    try:
        auth.register(username, password)
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if auth.login(username, password):
        response = jsonify({"message": "Login successful"})
        response.set_cookie('session_id', auth.create_session(username))
        return response, 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session_id = request.cookies.get('session_id')
    if auth.logout(session_id):
        response = jsonify({"message": "Logout successful"})
        response.delete_cookie('session_id')
        return response, 200
    return jsonify({"error": "Invalid session"}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

## Repository
- **GitHub Repository:** `alx-backend-user-data`
- **Directory:** `0x03-user_authentication_service`

By mastering these concepts and utilizing the provided resources, I will be able to implement a robust user authentication service, enhancing my understanding of authentication mechanisms and Flask application development.
sebsibe solomon
