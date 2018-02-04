from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .models import db


csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    csrf.init_app(app)
    return app


app = create_app()
app.app_context().push()

from . import views
