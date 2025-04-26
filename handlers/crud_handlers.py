from models import db, Tag, Category, Post
from flask import request, redirect, render_template, abort


def _create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form['category']
        tag_ids = request.form.getlist('tags')

        new_post = Post(title=title, content=content, category_id=category_id)
        new_post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('create_post.html',
                           categories=categories, tags=tags)


def _create_category():
    if request.method == 'POST':
        name = request.form['name']

        new_category = Category(name=name)

        db.session.add(new_category)
        db.session.commit()
        return redirect('/create/category')
    categories = Category.query.order_by(Category.name).all()
    return render_template('create_category.html', categories=categories)


def _create_tag():
    if request.method == 'POST':
        name = request.form['name']

        new_tag = Tag(name=name)

        db.session.add(new_tag)
        db.session.commit()
        return redirect('/create/tag')
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('create_tag.html', tags=tags)


def handle_create(type: str):
    if type == 'post':
        return _create_post()
    elif type == 'category':
        return _create_category()
    elif type == 'tag':
        return _create_tag()
    else:
        abort(404)


def _read_all():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


def _read_post():
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)


def _read_by_category(id: int):
    category = Category.query.get_or_404(id)
    posts = Post.query.filter_by(category_id=id).all()
    return render_template('by_category.html', posts=posts, category=category)


def _read_by_tag(id: int):
    tag = Tag.query.get_or_404(id)
    posts = tag.posts.all()
    return render_template('by_tag.html', posts=posts, tag=tag)


def handle_read(id: int = None, type: str = 'post'):
    if type == 'post' and id is None:
        return _read_all()
    elif type == 'post' and id is not None:
        return _read_post()
    elif type == 'category':
        return _read_by_category(id)
    elif type == 'tag':
        return _read_by_tag(id)
    else:
        abort(404)


def handle_update(id: int):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.category_id = request.form['category']

        tag_ids = request.form.getlist('tags')
        post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        db.session.commit()
        return redirect('/')

    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('update.html',
                           post=post, categories=categories, tags=tags)


def _delete_post(id: int):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')


def _delete_category(id: int):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect('/create/category')


def _delete_tag(id: int):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/create/tag')


def handle_delete(id: int = None, type: str = 'post'):
    if type == 'post':
        return _delete_post(id)
    elif type == 'category':
        return _delete_category(id)
    elif type == 'tag':
        return _delete_tag(id)
    else:
        abort(404)
