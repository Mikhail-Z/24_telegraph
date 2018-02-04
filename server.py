from telegraph.models import db
from telegraph import app
from config import FOR_LOCAL_USE, full_local_database_name
import os


if __name__ == "__main__":
    if FOR_LOCAL_USE and not os.path.exists(full_local_database_name):
        db.create_all()
    app.run()
