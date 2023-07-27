from flask import Flask , render_template , redirect , url_for , request

import datetime

from flask_sqlalchemy import SQLAlchemy
from model.User import db ,  User
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/python_test'

db.init_app(app)

# Context processor to pass current_year to all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.datetime.now().year}

@app.route('/')
def index():
    all_records = User.query.all()
    message = request.args.get('message')
    return render_template('index.html',users = all_records , message = message)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/todo/<id>')
def showTodo(id):
    return id


@app.route('/todo/delete/<id>')
def deleteTodo(id):
    user_to_delete = User.query.filter_by(id=id).first()
    if user_to_delete:
     db.session.delete(user_to_delete)
     db.session.commit()
     return redirect(url_for('/', message = "User successfully deleted"))



if __name__ == '__main__':
    app.run(debug=True)