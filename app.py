from flask import Flask, render_template
from models import db, User
from handlers import crud_handlers
from dotenv import load_dotenv
import os
from flask_login import LoginManager, current_user, login_required, logout_user, login_user
from flask_migrate import Migrate


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return crud_handlers.handle_index()


@app.route('/create/<type>', methods=['GET', 'POST'])
def create(type):
    if current_user.is_authenticated:
        return crud_handlers.handle_create(type=type)
    else:
        pass


@app.route('/<type>/<int:id>')
def read(type: str, id: int):
    if current_user.is_authenticated:
        return crud_handlers.handle_read(id=id, type=type)
    else:
        pass


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id: int):
    if current_user.is_authenticated:
        return crud_handlers.handle_update(id=id)
    else:
        pass


@app.route('/delete/<type>/<int:id>', methods=['POST'])
def delete(type: str, id: int):
    if current_user.is_authenticated:
        return crud_handlers.handle_delete(id=id, type=type)
    else:
        pass


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
