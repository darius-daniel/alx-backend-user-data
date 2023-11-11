#!/usr/bin/env python3
""" Implements a class that inherits from Auth
"""
from models.user import User
from typing import TypeVar
from api.v1.auth.auth import Auth
from base64 import b64decode


class BasicAuth(Auth):
    """ BasicAuth implementation.
    """
    pass
