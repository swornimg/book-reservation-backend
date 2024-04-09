from flask import jsonify

from . import app


@app.route('/hello')
def hello():
    return jsonify(hallo="new route...")
