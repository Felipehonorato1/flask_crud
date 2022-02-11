from functools import wraps
import datetime
from flask import request, jsonify
from werkzeug.security import check_password_hash
import jwt
from app import app
from .users import user_by_username


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message':
                            'Could not authenticate through token'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = user_by_username(data['username'])
        except:
            return jsonify({
                'message': 'Token is expired or invalid',
                'data': []
            }), 401

        return f(current_user, *args, **kwargs)

    return decorated


def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Login required'}), 401

    user = user_by_username(auth.username)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user and check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                'username': user.username,
                'exp': datetime.datetime.now() + datetime.timedelta(hours=12)
            }, app.config['SECRET_KEY'])

        print(token)

        return jsonify({
            'message':
            'Successfully authenticated',
            'token':
            jwt.decode(token, app.config['SECRET_KEY']),
            'exp':
            datetime.datetime.now() + datetime.timedelta(hours=12)
        }), 200

    return jsonify({'message': 'could not verify'}), 401
