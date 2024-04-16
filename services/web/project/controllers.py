from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from functools import wraps

from . import app, db
from .models import User
from .serializers import UserRegistrationSerializer


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 29cebd152c490bc1ef6e401821
        # dop_v1_c489a7e4fadf90e13553f5a610101f1d2c4e2103113c76ea3fd034d93f9d82bb
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
    
    
