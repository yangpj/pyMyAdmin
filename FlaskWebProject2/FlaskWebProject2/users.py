# coding=utf-8
"""用户管理模块"""

from FlaskWebProject2 import app
from flask.ext.login import LoginManager, UserMixin

login_manager = LoginManager()
login_manager.init_app(app)

if app.debug:
    login_manager.session_protection = None

login_manager.login_view = "login"
login_manager.login_message = "Please replace this login message."

class User(UserMixin):
    def __init__(self, userid):
        super(User, self).__init__()
        self.userid = userid

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.userid

loginUserList = {}

@login_manager.user_loader
def load_user(userid):
    return loginUserList.get(userid, None)
