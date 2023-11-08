#!/usr/bin/env python3
""" Implements and Auth class
"""
from flask import request
from typing import List, Union, TypeVar


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns True if the path is not in the list of strings
        excluded_paths
        """
        if path is None or not excluded_paths:
            return True

        if not path.endswith('/'):
            path = path + '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> Union[str, None]:
        """ Returns None for now. Full implementation to be handled later
        """
        if request is None or 'Authorization' not in request.headers().keys():
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None for now. Full implementation to be handled later later
        """
        return None
