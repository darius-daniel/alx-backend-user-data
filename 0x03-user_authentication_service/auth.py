#!/usr/bin/env python3
""" 4. Hash Password
"""
from bcrypt import hashpw, checkpw, gensalt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """ Returns the byte representation of a password string
    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """ Returns the string representation of a new UUID
    """
    return str(uuid4())


class Auth:
    """ Auth class to interact with the authentication database.
    """
    def __init__(self):
        """ Initialize a new instance of the Auth class
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a new user.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
        else:
            raise ValueError("User {} already exists".format(email))

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Locates a user by email and checks if the password argument matches
        the user's password (if he exists)
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> Union[str, None]:
        """ Finds a user corresponding to the email, generate a new UUID and
        store it in the database as the user's session_id.
        Return:
          - The session ID
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        else:
            new_session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=new_session_id)

        return new_session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Find a user with the corresponding session_id
        """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
            except Exception:
                ueer = None
            else:
                if user:
                    return user

    def destroy_session(self, user_id: int) -> None:
        """ Updates the corresponding user's session ID to None
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Finds the user with the corresponding engine, the generates a UUID
        and update the user's reset_token database field.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            user = None
        else:
            if user is not Nene:
                raise ValueError

            new_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=new_token)
            return new_token
