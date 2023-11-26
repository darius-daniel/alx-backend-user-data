#!/usr/bin/env python3
"""Sessions in Database."""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Another authentication class."""

    def create_session(self, user_id=None):
        """Create and store new instance of UserSession and return the Session
        ID.
        """
        new_session_id = super().create_session(user_id)
        if isinstance(new_session_id, str):
            new_user_session = UserSession(user_id=user_id, session_id=new_session_id)
            new_user_session.save()
        return new_session_id

    def user_id_for_session(self, session_id=None):
        """ Returns the User ID by requesting UserSession in the databse based
        on session_id.
        """
        try:
            sessions = UserSession().search({'session_id': session_id})
        except Exception:
            pass
        else:
            if sessions:
                session = sessions[0]

                curr_t = datetime.now()
                span_t = timedelta(seconds=self.session_duration)
                expiration_t = session.created_at + span_t

                if expiration_t >= curr_t:
                    return session.user_id

        return None

    def destroy_session(self, request=None):
        """ Destroys the UserSession based on the Session ID from the request
        cookie.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            pass
        else:
            if sessions:
                session = sessions[0]
                session.remove()
                return True

        return False
