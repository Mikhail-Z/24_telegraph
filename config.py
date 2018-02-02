import os
import psycopg2

DEBUG = True


SECRET_KEY = 'thisissecretkey'

FOR_LOCAL_USE = False


if FOR_LOCAL_USE:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///anongraph.db'
else:
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
