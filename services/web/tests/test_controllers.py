import unittest
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project.controllers import app, db, User

class TestControllers(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        with app.app_context():
            user = User(email='test@example.com', first_name='Test', last_name='User', password='password')
            db.session.add(user)
            db.session.commit()
            retrieved = User.query.filter_by(email='test@example.com').first()
            self.assertEqual(retrieved.email, 'test@example.com')
            self.assertEqual(retrieved.first_name, 'Test')
            self.assertTrue(retrieved.verify_password('password'))
            self.assertFalse(retrieved.is_admin)

    def test_signup(self):
        response = self.app.post('/register', data={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['message'], 'User created successfully!')

    # def test_login(self):
    #     # Sample data to be sent to the login form
    #     form_data = {
    #         'email': 'test@example.com',
    #         'password': 'password'
    #     }

    #     # Send POST request to the '/login' route
    #     response = self.client.post('/login', data=form_data)

    #     self.assertEqual(response.status_code, 201)
    #     self.assertIn('token', response.json)

    # def test_login(self):
    #     response = self.app.post('/login', data={
    #         'email': 'test@example.com',
    #         'password': 'password'
    #     })
        
    #     self.assertEqual(response.status_code, 201)
    #     self.assertIn('token', response.json)

    # def test_get_profile(self):
    #     response = self.app.get('/profile/1')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('first_name', response.json)
    #     self.assertIn('last_name', response.json)
    #     self.assertIn('email', response.json)
    #     self.assertIn('address', response.json)
    #     self.assertIn('cover_image', response.json)
    #     self.assertIn('mobile_number', response.json)

    # def test_update_profile(self):
    #     response = self.app.put('/profile/update/1', data={
    #         'first_name': 'New First Name',
    #         'last_name': 'New Last Name',
    #         'address': 'New Address',
    #         'cover_image': 'New Cover Image',
    #         'mobile_number': 'New Mobile Number'
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json['message'], 'Profile updated successfully!')

    # def test_create_genre(self):
    #     response = self.app.post('/add-genre', data={
    #         'name': 'Genre'
    #     })
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(response.json['message'], 'Genre created successfully!')

    # def test_create_book(self):
    #     response = self.app.post('/add-book', data={
    #         'isbn': '1234567890',
    #         'title': 'Test Book',
    #         'authors': 'Test Author',
    #         'publisher': 'Test Publisher',
    #         'publication_date': datetime.now(),
    #         'description': 'Test Description',
    #         'language': 'English',
    #         'num_pages': 100,
    #         'genre_id': 1
    #     })
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(response.json['message'], 'Book created successfully!')

    # def test_get_all_books(self):
    #     response = self.app.get('/list-books')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.json, list)

    # def test_get_book(self):
    #     response = self.app.get('/get-book/1')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('isbn', response.json)
    #     self.assertIn('title', response.json)
    #     self.assertIn('authors', response.json)
    #     self.assertIn('publisher', response.json)
    #     self.assertIn('publication_date', response.json)
    #     self.assertIn('description', response.json)
    #     self.assertIn('language', response.json)
    #     self.assertIn('num_pages', response.json)
    #     self.assertIn('cover_image', response.json)
    #     self.assertIn('genre_id', response.json)

    # def test_update_book(self):
    #     response = self.app.put('/update-book/1', data={
    #         'isbn': '1234567890',
    #         'title': 'Updated Book',
    #         'authors': 'Updated Author',
    #         'publisher': 'Updated Publisher',
    #         'publication_date': '2022-01-01',
    #         'description': 'Updated Description',
    #         'language': 'English',
    #         'num_pages': 100,
    #         'genre_id': 1
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json['message'], 'Book updated successfully!')

    # def test_delete_book(self):
    #     response = self.app.delete('/delete-book/1')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json['message'], 'Book deleted successfully!')

    

    # def test_get_all_genres(self):
    #     response = self.app.get('/list-genres')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.json, list)

    # def test_get_genre(self):
    #     response = self.app.get('/get-genre/1')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('name', response.json)

    # def test_update_genre(self):
    #     response = self.app.put('/update-genre/1', json={
    #         'name': 'Updated Genre'
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json['message'], 'Genre updated successfully!')

    # def test_delete_genre(self):
    #     response = self.app.delete('/delete-genre/1')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json['message'], 'Genre deleted successfully!')

    # def test_search_books(self):
    #     response = self.app.get('/search-books?keyword=test')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.json, list)



if __name__ == '__main__':
    unittest.main()
