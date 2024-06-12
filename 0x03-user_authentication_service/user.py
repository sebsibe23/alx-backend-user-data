#!/usr/bin/env python3
"""
Module: user
This module contains the `User` model which
maps to the `users` table.
The `User` class is a SQLAlchemy declarative
model representing user
records with columns for ID, email, hashed password,
session ID, and
reset token.

Classes:
    User(Base): Represents a record from
    the `user` table.

Attributes:
    id (int): Primary key for the user record.
    email (str): User's email address, required.
    hashed_password (str): User's hashed password, required.
    session_id (str): Optional session ID for the user.
    reset_token (str): Optional reset token for the user.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents a record from the `user` table.

    Attributes:
        id (int): Primary key for the user record.
        email (str): User's email address, required.
        hashed_password (str): User's hashed password, required.
        session_id (str): Optional session ID for the user.
        reset_token (str): Optional reset token for the user.
    """

    __tablename__ = "users"

    try:
        id = Column(Integer, primary_key=True)
        email = Column(String(250), nullable=False)
        hashed_password = Column(String(250), nullable=False)
        session_id = Column(String(250), nullable=True)
        reset_token = Column(String(250), nullable=True)
    except Exception as e:
        print(f"An error occurred while defining the User class: {e}")
