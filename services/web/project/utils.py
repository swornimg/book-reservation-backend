import os
from werkzeug.utils import secure_filename
from . import app


def handle_file_upload(file):
    if file.filename == '':
        return None
    
    if file:
        filename = secure_filename(file.filename)
        print(".... ", os.path.join(app.config["MEDIA_FOLDER"], filename))
        directory = os.path.join(app.config["MEDIA_FOLDER"], filename)
        file.save(directory)
        return directory
    
    return None
