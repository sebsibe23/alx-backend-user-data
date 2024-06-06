#!/usr/bin/env python3
"""
Module of session authenticating views.
This module contains views for
session-based user authentication.
"""
import os
from typing import Tuple
from flask import abort, jsonify, request

from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """
    Handle user login authentication.

    Method: POST
    Endpoint: /api/v1/auth_session/login
    Body Parameters:
      - email (str): User's email
      - password (str): User's password
    Returns:
      - JSON representation of a User object.
    Response Codes:
      - 200: Successful login
      - 400: Missing email or password
      - 401: Wrong password
      - 404: No user found for the email
    Cookies:
      - Sets a session cookie for the authenticated user.
    """
    not_found_res = {"error": "no user found for this email"}
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(not_found_res), 404
    if len(users) <= 0:
        return jsonify(not_found_res), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        sessiond_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        res.set_cookie(os.getenv("SESSION_NAME"), sessiond_id)
        return res
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """
    Handle user logout.

    Method: DELETE
    Endpoint: /api/v1/auth_session/logout
    Returns:
      - An empty JSON object.
    Response Codes:
      - 200: Successful logout
      - 404: Session not found or already destroyed
    """
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({})
