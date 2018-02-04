from telegraph.models import db
from telegraph import app
from config import FOR_LOCAL_USE, SQLALCHEMY_DATABASE_URI
import os


if __name__ == "__main__":
    if FOR_LOCAL_USE and not os.path.exists(SQLALCHEMY_DATABASE_URI):
        db.create_all()
    app.run()
