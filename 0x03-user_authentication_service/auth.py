#!/usr/bin/env python3
"""A module for authentication-related routines.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.

    Args:
    - password (str): The password to hash.

    Returns:
    - bytes: The hashed password.
    """
    try:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    except Exception as e:
        print(f"An error occurred: {e}")


def _generate_uuid() -> str:
    """Generates a UUID.

    Returns:
    - str: The generated UUID.
    """
    try:
        return str(uuid4())
    except Exception as e:
        print(f"An error occurred: {e}")


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user in the database.

        Args:
        - email (str): The email address of the user.
        - password (str): The password of the user.

        Returns:
        - User: The newly registered user object.

        Raises:
        - ValueError: If the user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            try:
                return self._db.add_user(email, _hash_password(password))
            except Exception as e:
                print(f"An error occurred: {e}")
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if the login details are valid for a user.

        Args:
        - email (str): The email address of the user.
        - password (str): The password of the user.

        Returns:
        - bool: True if the login details are valid, False otherwise.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Creates a new session for a user.

        Args:
        - email (str): The email address of the user.

        Returns:
        - str: The session ID for the user.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        try:
            self._db.update_user(user.id, session_id=session_id)
        except Exception as e:
            print(f"An error occurred: {e}")
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieves a user based on a session ID.

        Args:
        - session_id (str): The session ID of the user.

        Returns:
        - Union[User, None]: The user object if found, None otherwise.
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroys a session associated with a user.

        Args:
        - user_id (int): The ID of the user.
        """
        if user_id is None:
            return None
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for a user.

        Args:
        - email (str): The email address of the user.

        Returns:
        - str: The password reset token.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        try:
            self._db.update_user(user.id, reset_token=reset_token)
        except Exception as e:
            print(f"An error occurred: {e}")
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password given a reset token.

        Args:
        - reset_token (str): The reset token for the user.
        - password (str): The new password for the user.
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        new_password_hash = _hash_password(password)
        try:
            self._db.update_user(
                user.id,
                hashed_password=new_password_hash,
                reset_token=None,
            )
        except Exception as e:
            print(f"An error occurred: {e}")
