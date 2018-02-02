from flask import Flask
from models import db
import os
from config import FOR_LOCAL_USE
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    csrf.init_app(app)
    return app


app = create_app()
app.app_context().push()


from views import *

if __name__ == "__main__":
    if FOR_LOCAL_USE and not os.path.exists('anongraph.db'):
        db.create_all()
    app.run()
