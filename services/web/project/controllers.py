from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from functools import wraps

from . import app, db
from .utils import handle_file_upload
from .models import User, Book, Genre, Profile
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
                'exp' : datetime.now() + timedelta(minutes = 1440)
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
        app.logger.error(f'get_profile view: {str(e)}')
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
        app.logger.error(f'update_profile view: {str(e)}')
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)
    

# Create a new book
@app.route('/add-book', methods=['POST'])
@token_required
def create_book(current_user):
    try:
        data = request.form
        cover_image = request.files.get('cover_image')
        file_location = None

        if cover_image:
            file_location = handle_file_upload(cover_image)

        book = Book(
            isbn=data.get('isbn'),
            title=data.get('title'),
            authors=data.get('authors'),
            publisher=data.get('publisher'),
            publication_date=data.get('publication_date'),
            description=data.get('description'),
            language=data.get('language'),
            num_pages=data.get('num_pages'),
            cover_image=file_location,
            genre_id=data.get('genre_id')
        )
        db.session.add(book)
        db.session.commit()
        return make_response(jsonify({'message': 'Book created successfully!'}), 201)
    except Exception as e:
        app.logger.error(f'create_book view: {str(e)}')
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)


# Get all books
@app.route('/list-books', methods=['GET'])
@token_required
def get_all_books(current_user):
    try:
        books = Book.query.all()
        book_list = []
        for book in books:
            book_data = {
                'id': book.id,
                'isbn': book.isbn,
                'title': book.title,
                'authors': book.authors,
                'publisher': book.publisher,
                'publication_date': book.publication_date,
                'description': book.description,
                'language': book.language,
                'num_pages': book.num_pages,
                'cover_image': book.cover_image,
                'genre_id': book.genre_id
            }
            book_list.append(book_data)
        return jsonify(book_list)
    except Exception as e:
        app.logger.error(f'get_all_books view: {str(e)}')
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)


# Get a specific book
@app.route('/get-book/<int:book_id>', methods=['GET'])
@token_required
def get_book(current_user, book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return make_response(jsonify({'message': 'Book not found!'}), 404)
        book_data = {
            'id': book.id,
            'isbn': book.isbn,
            'title': book.title,
            'authors': book.authors,
            'publisher': book.publisher,
            'publication_date': book.publication_date,
            'description': book.description,
            'language': book.language,
            'num_pages': book.num_pages,
            'cover_image': book.cover_image,
            'genre_id': book.genre_id
        }
        return jsonify(book_data)
    except Exception as e:
        app.logger.error(f'get_book view: {str(e)}')
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)


# Update a book
@app.route('/update-book/<int:book_id>', methods=['PUT'])
@token_required
def update_book(current_user, book_id): 
    try:
        book = Book.query.get(book_id)
        if not book:
            return make_response(jsonify({'message': 'Book not found!'}), 404)

        data = request.form
        cover_image = request.files.get('cover_image')
        file_location = None

        if cover_image:
            file_location = handle_file_upload(cover_image)

        book.isbn = data.get('isbn')
        book.title = data.get('title')
        book.authors = data.get('authors')
        book.publisher = data.get('publisher')
        book.publication_date = data.get('publication_date')
        book.description = data.get('description')
        book.language = data.get('language')
        book.num_pages = data.get('num_pages')
        book.cover_image = file_location if file_location else book.cover_image
        book.genre_id = data.get('genre_id')
        db.session.commit()
        return make_response(jsonify({'message': 'Book updated successfully!'}), 200)
    
    except Exception as e:
        app.logger.error(f'update_book view: {str(e)}')
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)


# Delete a book
@app.route('/delete-book/<int:book_id>', methods=['DELETE'])
@token_required
def delete_book(current_user, book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return make_response(jsonify({'message': 'Book not found!'}), 404)
        db.session.delete(book)
        db.session.commit()
        return make_response(jsonify({'message': 'Book deleted successfully!'}), 200)
    except Exception as e:
        app.logger.error(f'delete_book view: {str(e)}')
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)
    

# CRUD operations for Genre model

# Create a new genre
@app.route('/add-genre', methods=['POST'])
@token_required
def create_genre(current_user):
    try:
        data = request.get_json()
        genre = Genre(
            name=data.get('name')
        )
        db.session.add(genre)
        db.session.commit()
        return make_response(jsonify({'message': 'Genre created successfully!'}), 201)
    except Exception as e:
        app.logger.error(f'create_genre view: {str(e)}')
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)


# Get all genres
@app.route('/list-genres', methods=['GET'])
@token_required
def get_all_genres(current_user):
    try:
        genres = Genre.query.all()
        genre_list = []
        for genre in genres:
            genre_data = {
                'id': genre.id,
                'name': genre.name
            }
            genre_list.append(genre_data)
        return jsonify(genre_list)
    except Exception as e:
        app.logger.error(f'get_all_genres view: {str(e)}')
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)


# Get a specific genre
@app.route('/get-genre/<int:genre_id>', methods=['GET'])
@token_required
def get_genre(current_user, genre_id):
    try:
        genre = Genre.query.get(genre_id)
        if not genre:
            return make_response(jsonify({'message': 'Genre not found!'}), 404)
        genre_data = {
            'id': genre.id,
            'name': genre.name
        }
        return jsonify(genre_data)
    except Exception as e:
        app.logger.error(f'get_genre view: {str(e)}')
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)


# Update a genre
@app.route('/update-genre/<int:genre_id>', methods=['PUT'])
@token_required
def update_genre(current_user, genre_id):
    try:
        genre = Genre.query.get(genre_id)
        if not genre:
            return make_response(jsonify({'message': 'Genre not found!'}), 404)
        data = request.get_json()
        genre.name = data.get('name')
        db.session.commit()
        return make_response(jsonify({'message': 'Genre updated successfully!'}), 200)
    
    except Exception as e:
        app.logger.error(f'update_genre view: {str(e)}')
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)


# Delete a genre
@app.route('/delete-genre/<int:genre_id>', methods=['DELETE'])
@token_required
def delete_genre(current_user, genre_id):
    try:
        genre = Genre.query.get(genre_id)
        if not genre:
            return make_response(jsonify({'message': 'Genre not found!'}), 404)
        db.session.delete(genre)
        db.session.commit()
        return make_response(jsonify({'message': 'Genre deleted successfully!'}), 200)
    
    except Exception as e:
        app.logger.error(f'delete_genre view: {str(e)}')
        return make_response(jsonify({'message': 'Something went wrong!'}), 500)
    
    