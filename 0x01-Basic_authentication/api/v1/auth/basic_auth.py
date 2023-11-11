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
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """ Return Base64 part of the Authorization header for a Basic
        Authentication.
        """
        if (
                authorization_header and
                isinstance(authorization_header, str) and
                authorization_header.startswith('Basic ')
                ):
            return authorization_header.split('Basic ')[1]

