#!/usr/bin/env python3
"""User session module.
"""
from models.base import Base


class UserSession(Base):
    """This class represents a user session,
        which is used to track user
    authentication and authorization information.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initializes a User session instance.

        Parameters:
        *args (list): Positional arguments to be passed to the parent
        class constructor.
        **kwargs (dict): Keyword arguments to be passed to the parent
        class constructor. The 'user_id' and 'session_id' keys are used
        to initialize the corresponding instance attributes.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
