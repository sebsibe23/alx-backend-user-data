#!/usr/bin/env python3
"""Route module for the API.
"""
import os
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)

from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.auth.session_exp_auth import SessionExpAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = getenv('AUTH_TYPE', 'auth')
if auth_type == 'auth':
    auth = Auth()
if auth_type == 'basic_auth':
    auth = BasicAuth()
if auth_type == 'session_auth':
    auth = SessionAuth()
if auth_type == 'session_exp_auth':
    auth = SessionExpAuth()
if auth_type == 'session_db_auth':
    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handler for 404 Not Found error.

    Parameters:
    - error: The error object.

    Returns:
    - JSON response with error message and 404 status code.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handler for 401 Unauthorized error.

    Parameters:
    - error: The error object.

    Returns:
    - JSON response with error message and 401 status code.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handler for 403 Forbidden error.

    Parameters:
    - error: The error object.

    Returns:
    - JSON response with error message and 403 status code.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def authenticate_user():
    """
    Authenticates a user before processing a request.

    Checks if the request path requires authentication and
    verifies the user's credentials.

    Raises:
    - 401 Unauthorized: If the authorization header is missing.
    - 403 Forbidden: If the user is not authenticated.
    """
    if auth:
        excluded_paths = [
            "/api/v1/status/",
            "/api/v1/unauthorized/",
            "/api/v1/forbidden/",
            "/api/v1/auth_session/login/",
        ]
        if auth.require_auth(request.path, excluded_paths):
            user = auth.current_user(request)
            if auth.authorization_header(request) is None and \
                    auth.session_cookie(request) is None:
                abort(401)
            if user is None:
                abort(403)
            request.current_user = user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
