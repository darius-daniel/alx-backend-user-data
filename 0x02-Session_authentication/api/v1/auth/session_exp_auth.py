#!/usr/bin/env python3
""" Implements a class SessionExpAuth that inherits from SessionAuth
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ class SessionExpAuth
    """
    def __init__(self):
        """ Initializes a new instance of SessionExpAuth
        """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURARION'))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Creates and new Session ID created and returns its value
        """
        session_id = super().create_session(user_id)
        if session_id is not None and isinstance(session_id, str):
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            return session_id

        return None

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID.
        """
        if (
                session_id is None and
                session_id not in self.user_id_by_session_id.keys()
        ):
            return None

        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict['user_id']
        if 'created_at' not in session_dict.keys():
            return None

        created_at = session_dict['created_at']
        if (
                created_at +
                timedelta(seconds=self.session_duration) <
                datetime.now()
        ):
            return None

        return session_dict['user_id']
