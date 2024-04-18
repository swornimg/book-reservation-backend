import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/project/media"
    SECRET_KEY = os.getenv("SECRET_KEY")


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

    WTF_CSRF_ENABLED = False
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    UPLOAD_FOLDER = f"{os.getenv('APP_FOLDER')}/project/uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    