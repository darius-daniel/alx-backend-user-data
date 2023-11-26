#!/usr/bin/env python3
""" New Flask view that handles all routes for the Session authentication
"""
from api.v1.views import app_views
from models.user import User
from flask import jsonify, abort, request
from os import getenv


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def login() -> str:
    """ POST /auth_session/login
    """
    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'email missing'}), 400

    pwd = request.form.get('password')
    if not pwd:
        return jsonify({'error': "password missing"}), 400

    users = User().search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if user.is_valid_password(pwd) is True:
        from api.v1.app import auth

        session_id = auth.create_session(getattr(user, 'id'))
        user_dict_repr = jsonify(user.to_json())
        user_dict_repr.set_cookie(getenv("SESSION_NAME"), str(session_id))

        return user_dict_repr

    return jsonify({'error': 'wrong password'}), 404


@app_views.route(
    '/auth_session/logout',
    methods=["DELETE"],
    strict_slashes=False
)
def delete() -> str:
    """ DELETE /api/v1/auth_session/logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request) is True:
        return jsonify({}), 200
    return abort(404)
