#!/usr/bin/env python3
""" Implements a class that inherits from Auth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth implementation.
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Return Base64 part of the Authorization header for a Basic
        Authentication
        """
        if (
                authorization_header is None or
                not isinstance(authorization_header, str) or
                not authorization_header.startswith('Basic ')):
            return None
        return authorization_header.split('Basic ')[1]
