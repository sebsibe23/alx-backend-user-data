#!/usr/bin/env python3
"""User module.
"""
import hashlib
from models.base import Base


class User(Base):
    """User class. Represents a user entity."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a User instance.

        Parameters:
            args (list): Additional arguments.
            kwargs (dict): Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get("email")
        self._password = kwargs.get("_password")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")

    @property
    def password(self) -> str:
        """Getter of the password.

        Returns:
            str: The encrypted password.
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """Setter of a new password: encrypt in SHA256.

        WARNING: Use a better password hashing algorithm like argon2
        or bcrypt in real-world projects.

        Parameters:
            pwd (str): The new password to set.
        """
        if pwd is None or type(pwd) is not str:
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """Validate a password.

        Parameters:
            pwd (str): The password to validate.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        if pwd is None or type(pwd) is not str:
            return False
        if self.password is None:
            return False
        pwd_e = pwd.encode()
        return hashlib.sha256(pwd_e).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """Display User name based on email/first_name/last_name.

        Returns:
            str: The displayed name.
        """
        if self.email is None and self.first_name is None \
                and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)
