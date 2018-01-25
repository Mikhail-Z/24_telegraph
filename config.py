import os
import psycopg2

DEBUG = True

# для production
SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

# для local
# SQLALCHEMY_DATABASE_URI = 'sqlite:///anongraph.db'


SECRET_KEY = 'thisissecretkey'
