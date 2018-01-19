from flask import render_template, request, make_response, redirect, url_for, abort, jsonify
from sqlalchemy.orm.exc import NoResultFound
from models import Article
from server import app
import uuid
from server import db
import datetime
import jwt


@app.route('/', methods=['GET', 'POST'])
def create_article():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        public_id = str(uuid.uuid4())
        input_data = dict(request.form)
        name = input_data['name'][0]
        text = input_data['text'][0]
        signature = input_data['signature'][0]
        new_article = Article(
            public_id=public_id,
            name=name,
            signature=signature,
            text=text
        )
        db.session.add(new_article)
        db.session.commit()
        resp = make_response(redirect(url_for('watch_article', public_id=public_id)))
        token = jwt.encode(
            {
                'public_id': new_article.public_id,
                'time': str(datetime.datetime.utcnow())
            },
            app.config['SECRET_KEY']
        )
        resp.set_cookie('{}_author'.format(public_id), token.decode(),
                        expires=datetime.datetime.now() + datetime.timedelta(365))
        return resp


@app.route('/<public_id>/',)
def watch_article(public_id):
    token = request.cookies.get('{}_author'.format(public_id))
    is_author = False
    if token:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        if public_id == data['public_id']:
            is_author = True
    try:
        article = Article.query.filter_by(public_id=public_id).one()
    except NoResultFound:
        return abort(404)
    return render_template(
        'article.html',
        article=article,
        is_author=is_author
    )


@app.route('/<public_id>/change/', methods=['GET', 'POST'])
def change_article(public_id):
    token = request.cookies.get('{}_author'.format(public_id))
    is_author = False
    if token:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        if public_id == data['public_id']:
            is_author = True
    if not is_author:
        return abort(403)
    try:
        article = Article.query.filter_by(public_id=public_id).one()
    except NoResultFound:
        return abort(404)
    if request.method == 'GET':
        title = article.name
        text = article.text
        signature = article.signature
        text.replace('\n', '&#013;')
        return render_template('form.html', title=title, text=text, signature=signature)
    else:
        article = Article.query.filter_by(public_id=public_id).first()
        input_data = dict(request.form)
        new_name = input_data['name'][0]
        new_text = input_data['text'][0]
        new_signature = input_data['signature'][0]
        article.name = new_name
        article.text = new_text
        article.signature = new_signature
        db.session.commit()
        return redirect(url_for('watch_article', public_id=public_id))


@app.route('/<public_id>/delete/')
def delete_article(public_id):
    token = request.cookies.get('{}_author'.format(public_id))
    is_author = False
    if token:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        if public_id == data['public_id']:
            is_author = True
    if not is_author:
        return abort(403)
    try:
        article = Article.query.filter_by(public_id=public_id).first()
    except NoResultFound:
        return abort(404)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('watch_article', public_id=public_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403