#!/usr/bin/env python3
"""
Session authentication module for the API.

This module provides session-based
authentication for the API.
"""

from uuid import uuid4
from flask import request

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session authentication class.

    This class provides methods for
    managing user sessions and
    authentication.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for the user.

        Args:
        - user_id (str): The ID of the user.

        Returns:
        - str: The session ID.
        """
        if type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves the user ID associated
        with a session ID.

        Args:
        - session_id (str): The session ID.

        Returns:
        - str: The user ID associated with
        the session ID.
        """
        if type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """Retrieves the current user
        associated with the request.

        Args:
        - request: The request object.

        Returns:
        - User: The current user object.
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroys an authenticated session.

        Args:
        - request: The request object.

        Returns:
        - bool: True if the session was successfully
        destroyed, False otherwise.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
