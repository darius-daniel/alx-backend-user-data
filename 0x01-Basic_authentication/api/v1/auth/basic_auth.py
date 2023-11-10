#!/usr/bin/env python3
""" Implements a class that inherits from Auth
"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Return the decoded value of a Base64 string
        base64_authorization_header
        """
        if (
                base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            try:
                decoded_header = base64.b64decode(base64_authorization_header)
            except Exception:
                return None
            else:
                return decoded_header.decode('utf-8')

    def extract_user_credential(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Returns the user email and password from the Base64 decoded value
        """
        if (
                decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str) or
                ':' not in decoded_base64_authorization_header
            ):
                return None, None
        return tuple(decoded_base64_authorization_header.split(':'))
