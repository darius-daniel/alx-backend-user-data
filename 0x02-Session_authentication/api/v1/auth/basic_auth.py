#!/usr/bin/env python3
""" Implements a class that inherits from Auth
"""
from models.user import User
from typing import Tuple, TypeVar
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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """ Return the decoded value of a Base64 string
        base64_authorization_header
        """
        if (
                base64_authorization_header and
                isinstance(base64_authorization_header, str)
        ):
            try:
                decoded_header = b64decode(
                    base64_authorization_header,
                    validate=True
                )
            except Exception:
                return None
            else:
                return decoded_header.decode('utf-8')

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        """ Returns the user email and password from the Base64 decoded value.
        """
        if (
                decoded_base64_authorization_header and
                isinstance(decoded_base64_authorization_header, str) and
                ':' in decoded_base64_authorization_header
        ):
            credentials = decoded_base64_authorization_header.split(':')
            email = credentials[0]
            pwd = ':'.join(credentials[1:])
            return email, pwd

        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
    ) -> TypeVar('User'):
        """ Returns the User instance based on his email and password
        """
        if (
                user_email and isinstance(user_email, str) and
                user_pwd and isinstance(user_pwd, str) and
                User().search({'email': user_email})
        ):
            users = User().search({'email': user_email})
            if users[0].is_valid_password(user_pwd):
                return users[0]

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Auth and retrieves the User instance for a request
        """
        header = self.authorization_header(request)
        b64_token = self.extract_base64_authorization_header(header)
        token = self.decode_base64_authorization_header(b64_token)
        email, pwd = self.extract_user_credentials(token)
        return self.user_object_from_credentials(email, pwd)
