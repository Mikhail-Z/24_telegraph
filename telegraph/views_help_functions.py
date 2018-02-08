import datetime
import uuid
import jwt
from flask import make_response, redirect, url_for, request, abort
from functools import wraps
from . import app
from .models import db


def create_public_id():
    return str(uuid.uuid4())


def insert2db(new_row):
    db.session.add(new_row)
    db.session.commit()


def delete_from_db(row):
    db.session.delete(row)
    db.session.commit()


def get_article_info_from_input(input_data):
    print(input_data)
    title = input_data['title'][0]
    text = input_data['text'][0]
    signature = input_data['signature'][0]
    return title, text, signature


def create_response_with_cookie(public_id, new_article, cookie_duration_in_days=365):
    resp = make_response(
        redirect(url_for('watch_article', public_id=public_id)))
    token = jwt.encode(
        {
            'public_id': new_article.public_id,
            'time': str(datetime.datetime.utcnow())
        },
        app.config['SECRET_KEY']
    )
    resp.set_cookie(
        '{}_author'.format(public_id), token.decode(),
        expires=datetime.datetime.now() + datetime.timedelta(cookie_duration_in_days)
    )
    return resp


def is_user_this_article_author(public_id):
    token = request.cookies.get('{}_author'.format(public_id))
    is_author = False
    if token:
        decoded_json_token = jwt.decode(token, app.config['SECRET_KEY'])
        if public_id == decoded_json_token['public_id']:
            is_author = True
    return is_author


def get_article_info_from_db(article):
    title = article.title
    text = article.text
    signature = article.signature
    text.replace('\n', '&#013;')
    return title, text, signature


def token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        public_id = kwargs['public_id']
        print(public_id)
        if not is_user_this_article_author(public_id):
            return abort(403)
        else:
            return fn(public_id)
    return decorated


