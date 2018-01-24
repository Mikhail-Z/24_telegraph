import os
import psycopg2

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
SECRET_KEY = 'thisissecretkey'
