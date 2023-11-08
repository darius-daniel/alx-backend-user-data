#!/usr/bin/env python3
""" Implements BasicAuth, a class that inherits from Auth
"""
from auth import Auth
from models.user import User
from typing import TypeVar, Union, Tuple
from base64 import b64decode


class BasicAuth(Auth):
    """ BasicAuth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> Union[str, None]:
        """ Returns the Base64 part of the Authorization header for a Basic
        Authentication.
        """
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith('Basic ')
        ):
            return None
        else:
            return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self, base_64_authorization_header: str) -> Union[str, None]:
        """ Returns the decode value of a Base64 string
        base_64_authorization_header
        """
        if (
            base_64_authorization_header is None
            or not isinstance(base_64_authorization_header, str)
        ):
            return None

        try:
            b64decode(base_64_authorization_header)
        except Exception:
            return None
        else:
            return b64decode(base_64_authorization_header).decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """ Returns the user email and password from the Base64 decoded value.
        """
        if (
                decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str) or
                ':' not in decoded_base64_authorization_header
        ):
            return (None, None)
        else:
            email, username = decoded_base64_authorization_header.split(':')
            return email, username

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on his email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        if not (user_email in User().search() and user_pwd in User().search()):
            return None

