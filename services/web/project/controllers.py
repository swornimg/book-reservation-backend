from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from functools import wraps

from . import app, db
from .models import User, Profile
from .serializers import UserRegistrationSerializer


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 29cebd152c490bc1ef6e401821
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(email = data['public_id'])\
                .first()
        except Exception as e:
            app.logger.error(f'token_required view: {str(e)}')
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated


@app.route('/signup', methods=['POST'])
def signup():
    try:
        serializer = UserRegistrationSerializer(request.form)
        is_valid, response = serializer.response()

        if not is_valid:
            return response

        email = response.get('email')
        first_name, last_name = response.get('first_name'), response.get('last_name')
        password = response.get('password')
        
        user = User.query\
            .filter_by(email = email)\
            .first()
        
        if user:
            return make_response(jsonify({'message': 'User already exists!'}), 409)
        
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return make_response(jsonify({'message': 'User created successfully!'}), 201)
    
    except Exception as e:
        app.logger.error(f'signup view: {str(e)}')
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)


@app.route('/login', methods=['POST'])
def login():
    try:
        app.logger.info('login view callled...')
        auth = request.form

        if not auth or not auth.get('email') or not auth.get('password'):
            return make_response(
                'Email or Password required!', 
                401, 
                {'WWW-Authenticate': 'Basic realm="Login required!"'}
            )
        
        user = User.query.filter_by(email=auth.get('email')).first()

        if not user:
            return make_response(
                'Invalid Credentials!', 
                401, 
                {'WWW-Authenticate': 'Basic realm="User does not exist!"'}
            )
        
        if check_password_hash(user.password_hash, auth.get('password')):
            token = jwt.encode({
                'public_id': user.email,
                'exp' : datetime.now() + timedelta(minutes = 30)
            }, app.config['SECRET_KEY'])

            return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
        
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
        )
    except Exception as e:
        app.logger.error(f'login view: {str(e)}')   
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)


@app.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'message': 'User not found!'}), 404)

        # Check if the profile exists, assuming a one-to-one relationship managed correctly
        if not user.profile:
            return make_response(jsonify({'message': 'Profile not found for this user!'}), 404)

        # Extract profile data
        profile_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'address': user.profile[0].address,  # Ensure user.profile is not a list
            'cover_image': user.profile[0].cover_image,
            'mobile_number': user.profile[0].mobile_number
        }

        return make_response(jsonify(profile_data), 200)

    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)


@app.route('/profile/update/<int:user_id>', methods=['PUT'])
@token_required
def update_profile(current_user, user_id):
    try:
        data = request.form

        # Retrieve the user
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return make_response(jsonify({'message': 'User not found!'}), 404)

        # Retrieve or create the user's profile
        if not user.profile:
            profile = Profile(user_id=user.id)
            db.session.add(profile)
        else:
            profile = user.profile

        # Update the fields if provided in the request
        if 'first_name' in data:
            user.first_name = data['first_name']  # Assuming user has first_name
        if 'last_name' in data:
            user.last_name = data['last_name']  # Assuming user has last_name
        if 'address' in data:
            profile.address = data['address']
        if 'cover_image' in data:
            profile.cover_image = data['cover_image']
        if 'mobile_number' in data:
            profile.mobile_number = data['mobile_number']

        # Commit the changes to the database
        db.session.commit()

        return make_response(jsonify({'message': 'Profile updated successfully!'}), 200)

    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)
