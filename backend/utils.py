from flask import request
from werkzeug.exceptions import HTTPException
import json, threading, time, os, random

class InvalidApiCall(Exception):
    def __init__(self, message):
        self.message = message

def dump(doc):
    return {
        'slug': doc['slug'],
        'description': doc['description'],
        'revisions': doc['revisions'],
        'pending': doc['pending']
    }

def register_errorhandlers(app):
    @app.errorhandler(InvalidApiCall)
    def bad_api_call(e):
        return json.dumps({'status':'error', 'error': e.message}), 400

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        response = e.get_response()
        response.data = json.dumps({
            "error": e.description,
            "code": e.code,
            "name": e.name
        })
        response.content_type = "application/json"
        return response
    
    return app

def get_json(*keys):
    try:
        for k, t in keys:
            o = request.json[k]
            if not isinstance(o, t):
                raise InvalidApiCall(f'Invalid Json Key/Type: {k} is {type(o).__name__}, expected {t.__name__}')
            yield o
    except KeyError:
        raise InvalidApiCall('Missing Json Keys')

def schedule(s=0, m=0, h=0, d=0, once=False):
    h = h + d * 24
    m = m + h * 60
    s = s + m * 60
    def wrapper(func):
        def inner():
            while True:
                time.sleep(s)
                func()
                if once:
                    break
        threading.Thread(target=inner, daemon=True).start()
        return func
    return wrapper

def cookies():
    return os.path.join('cookies', random.choice(os.listdir('cookies')))