#!/usr/bin/env python3
"""
DB module.
This module defines the `DB` class which provides methods for
interacting with the `User` model in a SQLite database.It includes
methods for adding, finding, and updating user records.

Classes:
    DB: A class to handle database operations for the `User` model.

Attributes:
    _engine (Engine): SQLAlchemy engine connected to the SQLite database.
    __session (Session): SQLAlchemy session object for database interactions.
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """
    DB class for database operations.

    Methods:
        __init__: Initializes a new DB instance.
        _session: Returns a memoized session object.
        add_user: Adds a new user to the database.
        find_user_by: Finds a user based on a set of filters.
        update_user: Updates a user based on a given id.
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance.
        Creates a new SQLite database connection
        and initializes the
        database schema by dropping all existing tables
        and creating new ones.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object.
        Returns a session object for database interactions.
        The session
        is created on demand and reused for subsequent operations.

        Returns:
            Session: SQLAlchemy session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Parameters:
            email (str): The email address of the new user.
            hashed_password (str): The hashed password
            of the new user.

        Returns:
            User: The newly created user object or
            None if an error occurred.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user based on a set of filters.

        Parameters:
            **kwargs: Arbitrary keyword arguments representing
            the filter criteria.

        Returns:
            User: The user object matching the filter criteria.

        Raises:
            InvalidRequestError: If a filter key is not
            a valid attribute of the User model.
            NoResultFound: If no user matches the filter criteria.
        """
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        result = (
            self._session.query(User)
            .filter(tuple_(*fields).in_([tuple(values)]))
            .first()
        )
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user based on a given id.

        Parameters:
            user_id (int): The ID of the user to be updated.
            **kwargs: Arbitrary keyword arguments representing
            the updated attributes.

        Returns:
            None"""
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        update_source = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                update_source[getattr(User, key)] = value
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            update_source,
            synchronize_session=False,
        )
        self._session.commit()
