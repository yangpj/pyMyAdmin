# coding=utf-8
"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.debug = True
app.secret_key = 'why would I tell you my secret key?'

import FlaskWebProject2.views
