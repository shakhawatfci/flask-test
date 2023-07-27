from flask import Flask, render_template, request, redirect, url_for, flash
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
    message = ''
    if(request.args.get('message')):
        message = request.args.get('message')
    return render_template('index.html',users = all_records , message = message)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user/create')
def createUser():
    return render_template('create_user.html',errors=None)


@app.route('/user',methods=['POST'])
def saveUser():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    errors = validate_input(name, password , email)

    if errors:
        # If there are validation errors, render the form again with the error messages
        return render_template('create_user.html', errors=errors)

    password_hash = generate_password_hash(password)
    user = User(name=name, email=email , password=password_hash)
    db.session.add(user)
    db.session.commit()
    
    return redirect('/')


@app.route('/todo/user/<id>')
def deleteTodo(id):
    user_to_delete = User.query.filter_by(id=id).first()
    if user_to_delete:
     db.session.delete(user_to_delete)
     db.session.commit()
     return redirect('/')
    #  return redirect(url_for('/', message = "User successfully deleted"))

def validate_input(name, password , email):
    errors = []

    # Validate name
    if not name:
        errors.append('Username is required.')
        
    if not email:
        errors.append('email is required.')

    # Validate password
    if not password:
        errors.append('Password is required.')
    elif len(password) < 6:
        errors.append('Password must be at least 6 characters long.')

    return errors

if __name__ == '__main__':
    app.run(debug=True)