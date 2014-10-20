# coding=utf-8
"""
The flask application package.
"""

from datetime import datetime
from flask import Flask

app = Flask(__name__)
app.debug = True
app.secret_key = 'why would I tell you my secret key?'
app.jinja_env.globals['year'] = datetime.now().year

import FlaskWebProject2.views
