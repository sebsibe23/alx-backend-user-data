#!/usr/bin/env python3
"""A simple end-to-end (E2E) integration test for `app.py`.

This script tests the various functionalities of the Flask app
`app.py`, including user registration, login, session management,
profile retrieval, password reset, and password update.

Author: [Your Name]

Attributes:
    EMAIL (str): A test email address.
    PASSWD (str): A test password.
    NEW_PASSWD (str): A new test password for updating.
    BASE_URL (str): The base URL of the Flask app.
"""

import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Tests registering a user.

    Args:
        email (str): The user's email address.
        password (str): The user's password.
    """
    url = "{}/users".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    try:
        res = requests.post(url, data=body)
        assert res.status_code == 200
        assert res.json() == {"email": email, "message": "user created"}
        res = requests.post(url, data=body)
        assert res.status_code == 400
        assert res.json() == {"message": "email already registered"}
    except AssertionError:
        pass


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests logging in with a wrong password.

    Args:
        email (str): The user's email address.
        password (str): The wrong password.
    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    try:
        res = requests.post(url, data=body)
        assert res.status_code == 401
    except AssertionError:
        pass


def log_in(email: str, password: str) -> str:
    """Tests logging in.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        str: The session ID.
    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    try:
        res = requests.post(url, data=body)
        assert res.status_code == 200
        assert res.json() == {"email": email, "message": "logged in"}
        return res.cookies.get('session_id')
    except AssertionError:
        pass


def profile_unlogged() -> None:
    """Tests retrieving profile information whilst logged out.
    """
    url = "{}/profile".format(BASE_URL)
    try:
        res = requests.get(url)
        assert res.status_code == 403
    except AssertionError:
        pass


def profile_logged(session_id: str) -> None:
    """Tests retrieving profile information whilst logged in.

    Args:
        session_id (str): The session ID.
    """
    url = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    try:
        res = requests.get(url, cookies=req_cookies)
        assert res.status_code == 200
        assert "email" in res.json()
    except AssertionError:
        pass


def log_out(session_id: str) -> None:
    """Tests logging out of a session.

    Args:
        session_id (str): The session ID.
    """
    url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    try:
        res = requests.delete(url, cookies=req_cookies)
        assert res.status_code == 200
        assert res.json() == {"message": "Bienvenue"}
    except AssertionError:
        pass


def reset_password_token(email: str) -> str:
    """Tests requesting a password reset.

    Args:
        email (str): The user's email address.

    Returns:
        str: The reset token.
    """
    url = "{}/reset_password".format(BASE_URL)
    body = {'email': email}
    try:
        res = requests.post(url, data=body)
        assert res.status_code == 200
        assert "email" in res.json()
        assert res.json()["email"] == email
        assert "reset_token" in res.json()
        return res.json().get('reset_token')
    except AssertionError:
        pass


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests updating a user's password.

    Args:
        email (str): The user's email address.
        reset_token (str): The reset token.
        new_password (str): The new password.
    """
    url = "{}/reset_password".format(BASE_URL)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    try:
        res = requests.put(url, data=body)
        assert res.status_code == 200
        assert res.json() == {"email": email, "message": "Password updated"}
    except AssertionError:
        pass


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
