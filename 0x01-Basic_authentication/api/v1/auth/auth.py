#!/usr/bin/env python3
""" Implements a class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Manages API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Return True if path is not in the list of strings excluded_paths
        """
        if not path or not excluded_paths:
            return True

        if not path.endswith('/'):
            path = '{}/'.format(path)

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Validates all requests to secure the API
        """
        if request is None or request.headers.get('Authorization') is None:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Full implementation later
        """
        return None