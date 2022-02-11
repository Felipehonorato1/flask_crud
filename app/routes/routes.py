from app import app
from flask import jsonify
from ..views import users, helpers


@app.route('/', methods=['GET'])
def handle_root():
    return jsonify({'message': 'Hello brother'})


@app.route('/auth', methods=['POST'])
def authenticate():
    return helpers.auth()


@app.route('/create_user', methods=['POST'])
def create_user():
    return users.post_user()


@app.route('/delete_user/<id>', methods=['DELETE'])
@helpers.token_required
def delete_user(id):
    return users.delete_user(id)


@app.route('/get_users', methods=['GET'])
def get_users():
    return users.get_users()


@app.route('/get_user/<id>', methods=['GET'])
def get_user(id):
    return users.get_user(id)
