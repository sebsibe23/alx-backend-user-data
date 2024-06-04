# 0x01. Basic authentication

## Background Context
In this project, I will learn what the authentication process means and implement a Basic Authentication on a simple API.

Basic Authentication is a method for an HTTP user agent (e.g. a web browser) to provide a user name and password when making a request. In Basic Auth, the client sends an "Authorization" header that is constructed by base64-encoding the username and password, separated by a colon.

In the industry, I should not implement my own Basic authentication system and use a module or framework that doing it for you (like in Python-Flask: Flask-HTTPAuth). Here, for the learning purpose, I will walk through each step of this mechanism to understand it by doing.

## Resources
- [REST API Authentication Mechanisms](https://blog.restcase.com/4-most-used-rest-api-authentication-methods/)
- [Base64 in Python](https://docs.python.org/3/library/base64.html)
- [HTTP header Authorization](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Base64 - concept](https://en.wikipedia.org/wiki/Base64)

## Learning Objectives
At the end of this project, I am expected to be able to explain to anyone, without the help of Google:

### General
- What authentication means
- What Base64 is and how it works
- How to encode a string in Base64
- What Basic authentication means and how it works
- How to send the Authorization header in an HTTP request

## Requirements
### Python Scripts
- All your files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- All your files should end with a new line
- The first line of all your files should be exactly `#!/usr/bin/env python3`
- A `README.md` file, at the root of the folder of the project, is mandatory
- Your code should use the `pycodestyle` style (version 2.5)
- All your files must be executable
- The length of your files will be tested using `wc`
- All your modules should have a documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
- All your classes should have a documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
- All your functions (inside and outside a class) should have a documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)'` and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`)
- A documentation is not a simple word, it's a real sentence explaining what's the purpose of the module, class or method (the length of it will be verified)

## Project Tasks
In this project, I will implement the following tasks:

1. **Implement a Basic Authentication**
   - Implement a Basic Authentication for a Flask API.
   - Create a `user_model.py` file that defines a `User` class with the following attributes: `id`, `username`, and `password`.
   - Implement a `basic_auth` function that takes a username and password, and returns a `User` object if the credentials are valid.
   - Implement a `require_basic_auth` decorator that can be used to protect a Flask route with Basic Authentication.
2. **Implement a session expiration**
   - Implement a session expiration mechanism for the Basic Authentication.
   - Whenever a user authenticates successfully, a new session is created and stored in a dictionary.
   - Each session has an expiration time, which is set to 60 minutes by default.
   - Implement a function to check if a session is still valid.
3. **Implement an error handler**
   - Implement an error handler for the Basic Authentication.
   - If a user provides invalid credentials, return a 401 Unauthorized response.
   - If a session has expired, return a 403 Forbidden response.

By the end of this project, I will have a better understanding of the Basic Authentication process and how to implement it in a Flask API.

Now, it's my turn to write the code to implement these tasks. Good luck!

