#!/usr/bin/env python3
""" DB mdoule
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """ DB class
    """
    def __init__(self) -> None:
        """ Initialize a new DB instance
        """
        self._engine = create_engine('sqlite:///a.db', echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Saves a user to the database.
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Returns the first row found in the users table as filtered by the
        method's input arguments.
        """
        column_names = []
        column_values = []
        for key, value in kwargs.items():
            if hasattr(User, key) is False:
                raise InvalidRequestError()

            column_names.append(getattr(User, key))
            column_values.append(value)

        first_row = self._session.query(User).filter(
            tuple_(*column_names).in_([column_values])
        ).first()

        if not first_row:
            raise NoResultFound()

        return first_row

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates a user's attributes by using self.find_user_by() to locate
        the user to update.
        """
        try:
            user = self.find_user_by(id=user_id)
        except (NoResultFound, InvalidRequestError):
            pass
        else:
            for k, v in kwargs.items():
                if getattr(User, k):
                    setattr(user, k, v)
                else:
                    raise ValueError()
            self._session.commit()
