import logging
import os
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy import text
from flask_migrate import Migrate
import jwt



app = Flask(__name__)

# Enable CORS
CORS(app)

# Logging
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler("app.log")
formatter = logging.Formatter('%(asctime)s - %(message)s')  # Include the date in the log messages
handler.setFormatter(formatter)  # Set the formatter for the handler
app.logger.addHandler(handler)

# Load configuration
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from . import controllers


@app.route("/")
def home():
    try:
        db.session.execute(text('SELECT 1'))
        return 'Database is connected!'
    except Exception as e:
        app.logger.error(f'Database connection error: {str(e)}')
        return f'Database connection error: {str(e)}'

@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)

@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == '':
            return "No selected file"
        if file:
            filename = secure_filename(file.filename)
            print(".... ", os.path.join(app.config["MEDIA_FOLDER"], filename))
            file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
            return 'File uploaded successfully'
    return """
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """

