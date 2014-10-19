# coding=utf-8

from FlaskWebProject2 import app
from flask.ext.login import LoginManager, UserMixin

login_manager = LoginManager()
login_manager.init_app(app)

if app.debug:
    login_manager.session_protection = None

login_manager.login_view = "login"
login_manager.login_message = "ssss"

class User(UserMixin):
    def is_authenticated():
        return True

    def is_active():
        return True

    def is_anonymous():
        return False

    def get_id():
        return u'admin'

@login_manager.user_loader
def load_user(userid):
    return User()