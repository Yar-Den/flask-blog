from models import db, Tag, Category, Post, User
from flask import request, redirect, render_template, abort, flash
from flask_login import current_user, login_required


def _create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form['category']
        tag_ids = request.form.getlist('tags')

        new_post = Post(
            title=title,
            content=content,
            category_id=category_id,
            user_id=current_user.id
            )
        new_post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        db.session.add(new_post)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Error: ' + str(e), 'danger')
        flash('Post was published', 'success')
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
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Error: ' + str(e), 'danger')
        flash('Category was added', 'success')
        return redirect('/create/category')
    categories = Category.query.order_by(Category.name).all()
    return render_template('create_category.html', categories=categories)


def _create_tag():
    if request.method == 'POST':
        name = request.form['name']

        new_tag = Tag(name=name)

        db.session.add(new_tag)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Error: ' + str(e), 'danger')
        flash('Tag was added', 'success')
        return redirect('/create/tag')
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('create_tag.html', tags=tags)


@login_required
def handle_create(type: str):
    """
    Обработчик создания сущностей по типу(посты, категории, теги)
    """
    if type == 'post':
        return _create_post()
    elif type == 'category':
        return _create_category()
    elif type == 'tag':
        return _create_tag()
    else:
        abort(404)


@login_required
def handle_index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


def _read_post(id: int):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)


def _read_by_category(id: int):
    category = Category.query.get_or_404(id)
    posts = Post.query.filter_by(category_id=id).all()
    return render_template('by_category.html', posts=posts, category=category)


def _read_by_tag(id: int):
    tag = Tag.query.get_or_404(id)
    posts = tag.posts
    return render_template('by_tag.html', posts=posts, tag=tag)


def _read_by_user(id: int):
    user = User.query.get_or_404(id)
    posts = User.posts
    return render_template('by_user.html', posts=posts, user=user)


@login_required
def handle_read(id: int = None, type: str = 'post'):
    """
    Обработчик для просмотра постов.
    """
    if type == 'post' and id is not None:
        return _read_post(id)
    elif type == 'category':
        return _read_by_category(id)
    elif type == 'tag':
        return _read_by_tag(id)
    elif type == 'user':
        return _read_by_user(id)
    else:
        abort(404)


@login_required
def handle_update(id: int):
    """
    Обработчик обновления постов.
    """
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.category_id = request.form['category']

        new_tag_ids = [int(id) for id in request.form.getlist('tags')]
        current_tag_ids = {tag.id for tag in post.tags}

        for tag_id in new_tag_ids:
            if tag_id not in current_tag_ids:
                tag = Tag.query.get(tag_id)
                post.tags.append(tag)

        for tag in post.tags.copy():
            if tag.id not in new_tag_ids:
                post.tags.remove(tag)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Error: ' + str(e), 'danger')
        flash('Post was updated', 'success')
        return redirect('/')
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('update.html',
                           post=post, categories=categories, tags=tags)


def _delete_post(id: int):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('Error: ' + str(e), 'danger')
    flash('Post was deleted', 'success')
    return redirect('/')


def _delete_tag(id: int):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('Ошибка: ' + str(e), 'danger')
    flash('Тег успешно удалён', 'success')
    return redirect('/create/tag')


@login_required
def handle_delete(id: int = None, type: str = 'post'):
    """
    Обработчик удаления сущностей (посты, категории, теги).
    """
    if type == 'post':
        return _delete_post(id)
    elif type == 'tag':
        return _delete_tag(id)
    else:
        abort(404)
