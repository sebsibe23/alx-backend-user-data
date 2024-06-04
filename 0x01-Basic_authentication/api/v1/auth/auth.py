#!/usr/bin/env python3
"""Authentication module for the API.
"""
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Authentication class."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a path requires authentication.

        Parameters:
        - path (str): The path to check.
        - excluded_paths (List[str]): List of paths that
        do not require authentication.

        Returns:
        - bool: True if the path requires authentication, False otherwise.
        """

        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ""
                if exclusion_path[-1] == "*":
                    pattern = "{}.*".format(exclusion_path[0:-1])
                elif exclusion_path[-1] == "/":
                    pattern = "{}/*".format(exclusion_path[0:-1])
                else:
                    pattern = "{}/*".format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Gets the authorization header field from the request.

        Parameters:
        - request: The Flask request object.

        Returns:
        - str: The authorization header value or None if not present.
        """

        if request is not None:
            return request.headers.get("Authorization", None)
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Gets the current user from the request.

        Parameters:
        - request: The Flask request object.

        Returns:
        - User: The current user or None.
        """

        return None
