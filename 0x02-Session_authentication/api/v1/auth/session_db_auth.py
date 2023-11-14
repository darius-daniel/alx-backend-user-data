#!/usr/bin/env python3
""" Sessions in Database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Another authentication class.
    """
    def create_session(self, user_id=None):
        """ Creates and store new instance of UserSession and returns the
        Session ID
        """
        session_id = super.create_session(user_id)
        if isinstance(session_id, str):   
            user_session = UserSession({
                'user_id': user_id,
                'session_id': session_id
            })
            user_session.save()
        return user_session.session_id

    def user_id_for_session(self, session_id=None):
        """ Returns the User ID by requesting UserSession in the databse based
        on session_id.
        """
        try:
            sessions = UserSession().search({'session_id': session_id})
        except Exception:
            return None
        if sessions:
            curr_t = datetime.now()
            span_t = timedelta(seconds=self.session_duration)
            expiration_t = sessions[0].created_at + span_t

            if expiration_t >= curr_t:
                return sessions[0].user_id

        return None
            
    def destroy_session(self, request=None):
        """ Destroys the UserSession based on the Session ID from the request
        cookie.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False

        if sessions:
            sessions[0].remove()
            return True

        return False
        