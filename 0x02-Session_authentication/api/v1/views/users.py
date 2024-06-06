#!/usr/bin/env python3
"""Module of Users views.

This module contains views for interacting
 with User objects.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GRetrieve all User objects.

    Returns:
    - str: A JSON representation of
    a list of all User objects.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    Retrieve a single User object by ID.

    Args:
    - user_id (str): The ID of the User to retrieve.

    Returns:
    - str: A JSON representation of the User object.
    - 404: If the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        else:
            return jsonify(request.current_user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    Delete a User object by ID.

    Args:
    - user_id (str): The ID of the User to delete.

    Returns:
    - str: An empty JSON object if
    the User has been correctly deleted.
    - 404: If the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """
    Create a new User object.

    JSON body:
    - email (str): The email of the new User.
    - password (str): The password of the new User.
    - last_name (str, optional): The last
    name of the new User.
    - first_name (str, optional): The first name
    of the new User.

    Returns:
    - str: A JSON representation of
    the new User object.
    - 400: If the request is in the wrong
    format or missing required fields.
    """
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        error_msg = "Wrong format"
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and rj.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User()
            user.email = rj.get("email")
            user.password = rj.get("password")
            user.first_name = rj.get("first_name")
            user.last_name = rj.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """
    Update a User object by ID.

    Args:
    - user_id (str): The ID of the User to update.

    JSON body:
    - last_name (str, optional): The new last
    name of the User.
    - first_name (str, optional): The new first
    name of the User.

    Returns:
    - str: A JSON representation of the
    updated User object.
    - 404: If the User ID doesn't exist.
    - 400: If the request is in the wrong format.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    rj = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
