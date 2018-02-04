from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField


class ArticleForm(FlaskForm):
    title = StringField()
    signature = StringField()
    text = TextAreaField()
