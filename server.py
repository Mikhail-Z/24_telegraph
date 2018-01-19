from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from views import *


if __name__ == "__main__":
    app.run()
