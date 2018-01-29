from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    title = db.Column(db.String(100))
    signature = db.Column(db.String(50))
    text = db.Column(db.Text)
