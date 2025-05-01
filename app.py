from flask import Flask, render_template
from models import db, User
from handlers import crud_handlers, authorize_handlers
from dotenv import load_dotenv
import os
from flask_login import LoginManager, login_required
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    return authorize_handlers.handle_login()


@app.route('/regirter', methods=['GET', 'POST'])
def regirter():
    return authorize_handlers.handle_regiter()


@app.route('/logout')
def logout():
    return authorize_handlers.handle_logout()


@app.route('/create/<type>', methods=['GET', 'POST'])
@login_required
def create(type):
    return crud_handlers.handle_create(type=type)


@app.route('/<type>/<int:id>')
@login_required
def read(type: str, id: int):
    return crud_handlers.handle_read(id=id, type=type)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id: int):
    return crud_handlers.handle_update(id=id)


@app.route('/delete/<type>/<int:id>', methods=['POST'])
@login_required
def delete(type: str, id: int):
    return crud_handlers.handle_delete(id=id, type=type)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
