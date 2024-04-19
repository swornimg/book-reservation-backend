import unittest
from project import app, db
from datetime import datetime
import random
from decimal import Decimal
from project.models import (User, Profile, Genre, Book, BookCopy, 
                            BookRequest, Review, Bookmark, Reservation, 
                            Transaction
)

class UserModelTestCase(unittest.TestCase):
    # Set up the environment before each test method is executed
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

# Clean up the environment after each test method has been executed
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

# Test case for user creation
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


class ProfileModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_profile_creation(self):
        with app.app_context():
            user = User(email='profile@example.com', first_name='Profile', last_name='User', password='password')
            db.session.add(user)
            db.session.commit()
            profile = Profile(user_id=user.id, mobile_number="1234567890", address="123 Test St")
            db.session.add(profile)
            db.session.commit()
            self.assertIsNotNone(user.profile)


class BookModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_book_creation(self):
        with app.app_context():
            book = Book(title="Test Book", isbn="1233", authors="Author Name", publisher="Publisher Name")
            db.session.add(book)
            db.session.commit()
            retrieved = Book.query.first()
            self.assertEqual(retrieved.title, "Test Book")
            self.assertEqual(retrieved.authors, "Author Name")


class BookCopyModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()   

    def test_book_copy_creation(self):
        with app.app_context():
            isbn = str(random.randint(1000, 9999))
            book = Book(isbn=isbn, title="Copy Book", authors="Author Name", publisher="Publisher Name")
            db.session.add(book)
            db.session.commit()
            book_copy = BookCopy(book_id=book.id, book_type="Hardcover", price=Decimal('15.99'))
            db.session.add(book_copy)
            db.session.commit()
            retrieved = BookCopy.query.first()
            self.assertEqual(retrieved.book_type, "Hardcover")
            self.assertAlmostEqual(Decimal(retrieved.price), Decimal('15.99'))


class BookRequestModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_book_request_creation(self):
        with app.app_context():
            user = User(email='request@example.com', first_name='Request', last_name='User', password='password')
            db.session.add(user)
            db.session.commit()
            book_request = BookRequest(user_id=user.id, requested_title="Requested Book", requested_authors="Author Name")
            db.session.add(book_request)
            db.session.commit()
            retrieved = BookRequest.query.first()
            self.assertEqual(retrieved.requested_title, "Requested Book")
            self.assertEqual(retrieved.requested_authors, "Author Name")


class ReviewModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_review_creation(self):
        with app.app_context():
            isbn = str(random.randint(1000, 9999))
            user = User(email='review@example.com', first_name='Review', last_name='User', password='password')
            book = Book(isbn=isbn, title="Review Book", authors="Author Name", publisher="Publisher Name")
            db.session.add_all([user, book])
            db.session.commit()
            review = Review(user_id=user.id, book_id=book.id, review_text="Great book")
            db.session.add(review)
            db.session.commit()
            retrieved = Review.query.first()
            self.assertEqual(retrieved.review_text, "Great book")


class BookmarkModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_bookmark_creation(self):
        with app.app_context():
            user = User(email='bookmark@example.com', first_name='Bookmark', last_name='User', password='password')
            book = Book(isbn='1223', title="Bookmark Book", authors="Author Name", publisher="Publisher Name")
            db.session.add_all([user, book])
            db.session.commit()
            bookmark = Bookmark(user_id=user.id, book_id=book.id)
            db.session.add(bookmark)
            db.session.commit()
            retrieved = Bookmark.query.first()
            self.assertEqual(retrieved.user_id, user.id)
            self.assertEqual(retrieved.book_id, book.id)


class ReservationModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_reservation_creation(self):
        with app.app_context():
            user = User(email='reserve@example.com', first_name='Reserve', last_name='User', password='password')
            book_copy = BookCopy(book_type="Paperback", price=20.00)
            db.session.add_all([user, book_copy])
            db.session.commit()
            reservation = Reservation(user_id=user.id, bookcopy_id=book_copy.id, status="Reserved", reserved_date=datetime.now())
            db.session.add(reservation)
            db.session.commit()
            retrieved = Reservation.query.first()
            self.assertEqual(retrieved.status, "Reserved")


class TransactionModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_transaction_creation(self):
        with app.app_context():
            user = User(email='transaction@example.com', first_name='Transaction', last_name='User', password='password')
            reservation = Reservation(status="Paid", reserved_date=datetime.now())
            db.session.add_all([user, reservation])
            db.session.commit()
            transaction = Transaction(user_id=user.id, reservation_id=reservation.id, amount=Decimal('19.99'), payment_method="Credit Card", transaction_date=datetime.now())
            db.session.add(transaction)
            db.session.commit()
            retrieved = Transaction.query.first()
            self.assertEqual(retrieved.amount, Decimal('19.99'))
            self.assertEqual(retrieved.payment_method, "Credit Card")



# Run the tests
if __name__ == '__main__':
    unittest.main()