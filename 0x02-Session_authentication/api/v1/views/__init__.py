#!/usr/bin/env python3
""" Module initialization for app views.
"""
from flask import Blueprint

# Create a Blueprint for the app views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views to register routes with the blueprint
from api.v1.views.index import *
from api.v1.views.users import *

# Load user data from a file
User.load_from_file()
