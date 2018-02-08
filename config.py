import os


SECRET_KEY = 'thisissecretkey'


basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_prefix = 'sqlite:///'
local_database_name = 'anongraph.db'
default_database_url = '{}{}'.format(
    sqlite_prefix,
    os.path.join(basedir, local_database_name)
)


if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = default_database_url
else:
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
