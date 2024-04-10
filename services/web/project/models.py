from . import db
import re
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Numeric,
    Date,
    Text
)
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func



class TimestampMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class User(db.Model, TimestampMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(128), unique=True, nullable=False)
    first_name = Column(String(128), nullable=True) 
    last_name = Column(String(128), nullable=True)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean(), default=False, nullable=False)
    active = Column(Boolean(), default=True, nullable=False)
    profile = relationship("Profile", back_populates="user")

    def __init__(self, email, first_name, last_name, password, is_admin=False, active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.email = self.validate_and_set_email(email)
        self.password_hash = self.hash_password(password)
        self.is_admin = is_admin
        self.active = active
    
    def is_valid_email(self, email):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(email_regex, email)

    def validate_and_set_email(self, email):
        if self.is_valid_email(email):
            return email
        else:
            raise ValueError("Invalid email format")

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
        return self.password_hash

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Profile(db.Model, TimestampMixin):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="profile")
    cover_image = Column(String(255), nullable=True)
    mobile_number = Column(String(20), nullable=False)
    address = Column(String(255), nullable=True)


class Genre(db.Model, TimestampMixin): #category
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Book(db.Model, TimestampMixin):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    isbn = Column(String(20), unique=True, nullable=False)
    title = Column(String(100), nullable=False)
    authors = Column(String(255), nullable=False)
    publisher = Column(String(100))
    publication_date = Column(Date)
    description = Column(Text)
    language = Column(String(50))
    num_pages = Column(Integer)
    cover_image = Column(String(255))
    genre_id = Column(Integer, ForeignKey('genre.id'))


class BookCopy(db.Model, TimestampMixin):
    __tablename__ = 'bookcopy'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'))
    book_type = Column(String(50), nullable=False)  # e.g. hardcover, paperback, etc.
    edition = Column(String(50), nullable=True)
    condition = Column(String(50), nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    availability = Column(Boolean, default=True)


class BookRequest(db.Model, TimestampMixin):
    __tablename__ = 'bookrequest'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    requested_title = Column(String(100), nullable=False)
    requested_authors = Column(String(255), nullable=False)
    requested_publisher = Column(String(100))
    description = Column(Text, nullable=True)


class Review(db.Model, TimestampMixin):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    book_id = Column(Integer, ForeignKey('book.id'))
    review_text = Column(String(255), nullable=False)


class Bookmark(db.Model, TimestampMixin):
    __tablename__ = 'bookmark'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    book_id = Column(Integer, ForeignKey('book.id'))


class Reservation(db.Model, TimestampMixin):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    bookcopy_id = Column(Integer, ForeignKey('bookcopy.id'))
    reserved_date = Column(Date, default=func.now())
    return_date = Column(Date, nullable=True)
    returned_date = Column(Date, nullable=True)
    status = Column(String(50), nullable=False)  # e.g. reserved, borrowed, returned
    fine = Column(Numeric(10, 2), nullable=True)
    remarks = Column(Text, nullable=True)
    # user = relationship("User", back_populates="reservation")


class Transaction(db.Model, TimestampMixin):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    reservation_id = Column(Integer, ForeignKey('reservation.id'))
    transaction_date = Column(Date, default=func.now())
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)
    remarks = Column(Text, nullable=True)
    # user = relationship("User", back_populates="transaction")
    # reservation = relationship("Reservation", back_populates="transaction")





