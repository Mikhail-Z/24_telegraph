import os
from .views_help_functions import *

from flask import render_template, request, redirect, \
    url_for, abort, send_from_directory
from .forms import ArticleForm

from . import app
from .models import db, Article


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


@app.route('/<public_id>/',)
def watch_article(public_id):
    article = Article.query.filter_by(public_id=public_id).first()
    if article is None:
        return abort(404)
    return render_template(
        'article.html',
        article=article,
        is_author=is_user_this_article_author(public_id)
    )


@app.route('/<public_id>/change/', methods=['GET', 'POST'])
@token_required
def change_article(public_id):
    form = ArticleForm()
    article = Article.query.filter_by(public_id=public_id).first()
    if article is None:
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
@token_required
def delete_article(public_id):
    article = Article.query.filter_by(public_id=public_id).first()
    if article is None:
        status_code = 404
        return abort(status_code)

    delete_from_db(article)
    return redirect(url_for('watch_article', public_id=public_id))


@app.errorhandler(code_or_exception=404)
def page_not_found(exception):
    return render_template('404.html')


@app.errorhandler(code_or_exception=403)
def forbidden(exception):
    return render_template('403.html')