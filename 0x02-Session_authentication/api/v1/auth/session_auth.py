#!/usr/bin/env python3
""" Implements a class SessionAuth that inherits from Auth.
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ SessionAuth inherits from Auth.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id.
        """
        if user_id and isinstance(user_id, str):
            session_id = uuid.uuid4()
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID.
        """
        if session_id and isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
