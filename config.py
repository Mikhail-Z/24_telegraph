import os
import psycopg2


SECRET_KEY = 'thisissecretkey'

FOR_LOCAL_USE = True

basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_prefix = 'sqlite:///'
local_database_name = 'anongraph.db'
full_local_database_name = '{}{}'.format(
    sqlite_prefix,
    os.path.join(basedir, local_database_name)
)

if FOR_LOCAL_USE:
    SQLALCHEMY_DATABASE_URI = full_local_database_name
else:
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
