from flask import Flask, render_template
from models import db
from handlers import crud_handlers
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db.init_app(app)


@app.route('/')
def index():
    return crud_handlers.handle_index()


@app.route('/create/<type>', methods=['GET', 'POST'])
def create(type):
    return crud_handlers.handle_create(type=type)


@app.route('/<type>/<int:id>')
def read(type: str, id: int):
    return crud_handlers.handle_read(id=id, type=type)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id: int):
    return crud_handlers.handle_update(id=id)


@app.route('/delete/<type>/<int:id>', methods=['POST'])
def delete(type: str, id: int):
    return crud_handlers.handle_delete(id=id, type=type)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
