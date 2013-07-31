import logging
import os
import sys
import datetime
from functools import update_wrapper
from flask import Flask, session, redirect, flash, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel, lazy_gettext
from sqlalchemy import func
from websocket import handle_websocket
from database import db_session, init_db
from models import *
from formalchemy import FieldSet, Field

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hendpos.db'
app.secret_key = os.urandom(24)
app.debug = True
babel = Babel(app)
#logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(msg)s", filename="log.txt")

def login_required(url = None):
    def decorator(fn):
        def decorated_function (*args, **kwargs):
            if session.get('AuthUser'):
                return fn(*args, **kwargs)
            else:
                flash(lazy_gettext('Error: User not logged in') )
                if url=='/' :
                    return redirect(url_for('login'))
                else:
                    return redirect(url_for('login', next=request.url))
        return update_wrapper(decorated_function, fn)
    return decorator

def url_for_static(filename):
    root = app.config.get('STATIC_ROOT','')
    path = os.path.join(root, filename)
    return path

app.jinja_env.globals.update(url_for_static=url_for_static)

init_db()

def my_app(environ, start_response):
    path = environ["PATH_INFO"]
    if path == "/":
        return app(environ, start_response)
    elif path == "/websocket":
        handle_websocket(environ["wsgi.websocket"])
    else:
        return app(environ, start_response)

import views

