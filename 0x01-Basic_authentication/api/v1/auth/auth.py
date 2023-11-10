#!/usr/bin/env python3
""" Implements a class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Manages API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Full implementation later
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Full implementation later
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Full implementation later
        """
        return None
