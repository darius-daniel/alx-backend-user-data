#!/usr/bin/env python3
""" Sessions in database.
"""
from models.base import Base


class UserSession(Base):
    """ A class that inherits from Base
    """
    def __init__(self, *args, **kwargs):
        """ Initializes a new instance of UserSession.
        """
        super().__init__()
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')