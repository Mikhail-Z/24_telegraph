from flask import render_template, request, make_response, redirect,\
    url_for, abort, send_from_directory
from sqlalchemy.orm.exc import NoResultFound
from models import db, Article
import uuid
import datetime
import jwt
import os
from forms import ArticleForm
from server import app


def create_public_id():
    return str(uuid.uuid4())


def insert2db(new_row):
    db.session.add(new_row)
    db.session.commit()


def delete_from_db(row):
    db.session.delete(row)
    db.session.commit()


def get_article_info_from_input(input_data):
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


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET', 'POST'])
def create_article():
    form = ArticleForm()
    if request.method == 'GET':
        return render_template('form.html', form=form)
    else:
        input_data = dict(request.form)
        public_id = create_public_id()
        title, text, signature = get_article_info_from_input(input_data)
        new_article = Article(
            public_id=public_id,
            title=title,
            signature=signature,
            text=text
        )
        insert2db(new_article)
        return create_response_with_cookie(public_id, new_article)


def is_user_this_article_author(public_id):
    token = request.cookies.get('{}_author'.format(public_id))
    is_author = False
    if token:
        decoded_json_token = jwt.decode(token, app.config['SECRET_KEY'])
        if public_id == decoded_json_token['public_id']:
            is_author = True
    return is_author


@app.route('/<public_id>/',)
def watch_article(public_id):
    try:
        article = Article.query.filter_by(public_id=public_id).one()
    except NoResultFound:
        return abort(404)
    return render_template(
        'article.html',
        article=article,
        is_author=is_user_this_article_author(public_id)
    )


def get_article_info_from_db(article):
    title = article.title
    text = article.text
    signature = article.signature
    text.replace('\n', '&#013;')
    return title, text, signature


@app.route('/<public_id>/change/', methods=['GET', 'POST'])
def change_article(public_id):
    is_author = is_user_this_article_author(public_id)
    form = ArticleForm()
    if not is_author:
        return abort(403)
    try:
        article = Article.query.filter_by(public_id=public_id).one()
    except NoResultFound:
        return abort(404)
    if request.method == 'GET':
        form.title.data, form.text.data, form.signature.data = get_article_info_from_db(article)
        return render_template('form.html', form=form)
    else:
        article = Article.query.filter_by(public_id=public_id).first()
        input_data = dict(request.form)
        article.title, article.text, article.signature = get_article_info_from_input(input_data)
        db.session.commit()
        return redirect(url_for('watch_article', public_id=public_id))


@app.route('/<public_id>/delete/')
def delete_article(public_id):
    is_author = is_user_this_article_author(public_id)
    if not is_author:
        status_code = 403
        return abort(status_code)
    try:
        article = Article.query.filter_by(public_id=public_id).first()
    except NoResultFound:
        status_code = 404
        return abort(status_code)

    delete_from_db(article)
    return redirect(url_for('watch_article', public_id=public_id))


@app.errorhandler(code_or_exception=404)
def page_not_found(exception):
    status_code = 404
    return render_template('404.html'), status_code


@app.errorhandler(code_or_exception=403)
def page_not_found(exception):
    status_code = 403
    return render_template('403.html'), status_code