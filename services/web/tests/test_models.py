import unittest
from project import app, db
from project.models import User


class UserModelTestCase(unittest.TestCase):
    
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
            # Create a User instance
            user = User(email='test@example.com', first_name='Test', last_name='User', password='password')
            
            # Add it to the session and commit
            db.session.add(user)
            db.session.commit()
            
            # Retrieve the user from the database
            retrieved = User.query.filter_by(email='test@example.com').first()
            
            # Assert that the retrieved details match
            self.assertEqual(retrieved.email, 'test@example.com')
            self.assertEqual(retrieved.first_name, 'Test')
            self.assertTrue(retrieved.verify_password('password'))
            self.assertFalse(retrieved.is_admin)  # Default value is False

# Run the tests
if __name__ == '__main__':
    unittest.main()