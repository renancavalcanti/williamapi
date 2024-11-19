from flask import Blueprint, jsonify, request
from database.__init__ import database
from models.user_model import User
import controllers.user_controller as user_controller
from helpers.token_validation import validate_token

user = Blueprint("user", __name__)

@user.route('/v0/users/signup', methods=['POST'])
def add_user():
    try:
        user_data = request.json
        print(user_data)

        if 'email' not in user_data:
            return jsonify({'error': 'Email is required in the request!'}), 400
        if 'name' not in user_data:
            return jsonify({'error': 'Name is required in the request!'}), 400
        if 'password' not in user_data:
            return jsonify({'error': 'Password is required in the request!'}), 400

        new_user = User(user_data['name'], user_data['email'], user_data['password'])

        created_user = user_controller.create_user(new_user)
        
        if created_user == "Duplicated User":
            return jsonify({'error': 'Email already exists!'}), 400
        
        if not created_user.inserted_id:
            return jsonify({'error': 'Something went wrong!'}), 500

        return jsonify({'id': str(created_user.inserted_id)})
    except:
        return jsonify({'error': 'Something went wrong!'}), 500

@user.route('/v0/users/login', methods=['POST'])
def login():
    try:
        user_data = request.json

        if 'email' not in user_data:
                return jsonify({'error': 'Email is required in the request!'}), 400
        if 'password' not in user_data:
            return jsonify({'error': 'Password is required in the request!'}), 400

        login_user = user_controller.login_user(user_data)

        if login_user == "Invalid Email":
            return jsonify({'error': 'Invalid Email or Password!'}), 400
        if login_user == "Invalid Password":
            return jsonify({'error': 'Invalid Email or Password!'}), 400

        return login_user
    except:
        return jsonify({'error': 'Something went wrong on Login!'}), 500

@user.route('/v0/users/all', methods=['GET'])
def get_users():
    try:
        token = validate_token()
        print(token)

        if token == 400:
            return jsonify({'error': 'Token is missing!'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid Token!'}), 401
        
        return user_controller.fetch_users()
    except:
        return jsonify({'error': 'Error on fetching users!'}), 500

