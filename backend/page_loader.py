from flask import Flask, send_file
import mimetypes

import database
from utils import *

app = register_errorhandlers(Flask(__name__))

@app.route('/') 
def root():
    return send_file('index.html')

@app.route('/<path:slug>')
def load_page(slug):
    if (doc := app.database['pages'].find_one({'slug': slug.lstrip('/')})) is None:
        return send_file('error.html')
    if doc['pending']:
        return send_file('loading.html')
    mime, _ = mimetypes.guess_type(slug)
    return doc['content'], 200, {'Content-Type': mime or 'text/html'}

with app.app_context():
    app.mongodb_client = database.get_client()
    app.database = database.get_database()

if __name__ == '__main__':
    app.run(port=8787)