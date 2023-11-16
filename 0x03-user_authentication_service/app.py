#!/usr/bin/env python3
""" Flask App
"""
from flask import Flask, jsonify, abort, request, redirect, url_for
from auth import Auth
from typing import Union


app = Flask(__name__)
Auth = Auth()


@app.route('/', methods=["GET"], strict_slashes=False)
def home() -> str:
    """ GET '/'
    Return:
      - a payload in the form {'message': 'Bienvenue'}
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def users() -> Union[str, None]:
    """ POST /users
    Registers a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        Auth.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login() -> str:
    """ POST /sessions
    """
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not Auth.valid_login(email, pwd):
        abort(401)

    request.cookies['session_id'] = Auth.create_session(email)
    return jsonify({"email": email, "message": "logged in"})


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """ DELETE /sessions
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_user_from_session_id(session_id)
    if user:
        Auth.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ GET /profile
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_user_from_session_id(session_id)
    email = request.form.get('email')
    if user:
        return jsonify({'email': email})
    abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
