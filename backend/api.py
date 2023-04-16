from flask import Flask, jsonify, request
from flask_cors import CORS
import re

import database
from utils import *
from worker import run_worker

app = register_errorhandlers(Flask(__name__))
CORS(app)
slug_regex = re.compile(r'^[-a-zA-Z0-9_]+$')

@app.route('/list')
def get_pages():
    page = request.args.get('page', default=0, type=int)
    count = request.args.get('count', default=20, type=int)
    pages = app.database['pages'].find().skip(page * count).limit(count)
    return jsonify([{k: v for k, v in dump(doc).items() if k != 'revisions'} for doc in pages])

@app.route('/details', methods=['POST'])
def get_details():
    slug, = get_json(
        ('slug', str)
    )
    slug = slug.lstrip('/')
    if (doc := app.database['pages'].find_one({'slug': slug})) is None:
        raise InvalidApiCall('does not exist')
    return jsonify(dump(doc))

@app.route('/new', methods=['POST'])
def new_page():
    slug, description = get_json(
        ('slug', str),
        ('description', str)
    )
    slug = slug.lstrip('/').replace(' ', '-')
    if not slug_regex.match(slug):
        raise InvalidApiCall('invalid slug')
    if app.database['pages'].find_one({'slug': slug}):
        raise InvalidApiCall('already exists')
    app.database['pages'].insert_one({
        'slug': slug,
        'description': description,
        'revisions': [],
        'content': '',
        'pending': True
    })
    run_worker(slug, description=description)
    return jsonify({'status':'pending'})

@app.route('/check', methods=['POST'])
def check():
    slug = get_json(
        ('slug', str)
    )
    slug = slug.lstrip('/')
    if (doc := app.database['pages'].find_one({'slug': slug})) is None:
        raise InvalidApiCall('does not exist')
    return jsonify({'status': 'pending' if doc['pending'] else 'success'})

@app.route('/revise', methods=['POST'])
def edit_page():
    slug, revision = get_json(
        ('slug', str),
        ('revision', str)
    )
    slug = slug.lstrip('/')
    if (doc := app.database['pages'].find_one({'slug': slug})) is None:
        raise InvalidApiCall('does not exist')
    revisions = doc['revisions']
    revisions.append(revision)
    app.database['pages'].update_one({
        '_id': doc['_id']
    }, {
        '$set': {
            'revisions': revisions,
            'pending': True
        }
    })
    run_worker(slug, revision=revision)
    return jsonify({'status': 'pending'})

@app.route('/delete', methods=['POST'])
def delete_page():
    slug, = get_json(
        ('slug', str)
    )
    slug = slug.lstrip('/')
    if (doc := app.database['pages'].find_one({'slug': slug})) is None:
        raise InvalidApiCall('does not exist')
    app.database['pages'].delete_one({
        '_id': doc['_id']
    })
    return jsonify({'status': 'success'})

@app.route('/export', methods=['POST'])
def export():
    slug, = get_json(
        ('slug', str)
    )
    slug = slug.lstrip('/')
    if (doc := app.database['pages'].find_one({'slug': slug})) is None:
        raise InvalidApiCall('does not exist')
    if doc['pending']:
        raise InvalidApiCall('page is pending')
    return doc['content'], 200, {'Content-Disposition': 'attachment'}

with app.app_context():
    app.mongodb_client = database.get_client()
    app.database = database.get_database()

if __name__ == '__main__':
    app.run(port=8686)