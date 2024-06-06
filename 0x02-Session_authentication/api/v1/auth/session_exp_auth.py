#!/usr/bin/env python3
"""
Session authentication with expiration
module for the API.

This module provides a SessionExpAuth class
that extends the SessionAuth class from the
session_auth module. It adds session expiration
functionality to the authentication system.

The SessionExpAuth class initializes with
a session_duration attribute, which is set to the
value of the SESSION_DURATION environment
variable, or 0 if the variable is not set.

The create_session method overrides the base
class method to create a new session ID and
store it in the user_id_by_session_id dictionary,
along with the user ID and the timestamp
of when the session was created.

The user_id_for_session_id method checks if the
given session ID is present in the
user_id_by_session_id dictionary. If it is,
it checks if the session has expired based on
the session_duration and the creation timestamp.
If the session has not expired, it
returns the associated user ID.
If the session has expired, it returns None.
"""
import os
from flask import request
from datetime import datetime, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Session authentication class with expiration.

    This class extends the SessionAuth class
    to add session expiration functionality.
    """

    def __init__(self) -> None:
        """
        Initializes a new SessionExpAuth instance.

        The session_duration attribute is
        set to the value of the SESSION_DURATION
        environment variable, or 0 if the variable is not set.
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session id for the user.

        This method overrides the base class method
        to create a new session ID and store
        it in the user_id_by_session_id dictionary,
        along with the user ID and the
        timestamp of when the session was created.

        Parameters:
        user_id (str): The user ID to create a session for.

        Returns:
        str: The session ID, or None if there was an error.
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Retrieves the user id of the user associated
        with a given session id.

        This method checks if the given session ID
        is present in the
        user_id_by_session_id dictionary. If it is,
        it checks if the session has
        expired based on the session_duration and the
        creation timestamp. If the
        session has not expired, it returns
        the associated user ID. If the
        session has expired, it returns None.

        Parameters:
        session_id (str): The session ID to
        retrieve the user ID for.

        Returns:
        str: The user ID associated with the session ID,
        or None if the session has expired.
        """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            cur_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = session_dict['created_at'] + time_span
            if exp_time < cur_time:
                return None
            return session_dict['user_id']
