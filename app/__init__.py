from flask import Flask

from app.cache01.views import cache_blue
from app.ext import init_ext
from app.user.views import user_blue

app = Flask(__name__)
app.debug = True


def create_app():
    init_ext(app=app)
    register_blue()
    return app


def register_blue():
    app.register_blueprint(cache_blue, url_prefix='/cache')
    app.register_blueprint(user_blue, url_prefix='/user')
