from flask import Flask, render_template, request, redirect, url_for, flash , session
import datetime

from flask_sqlalchemy import SQLAlchemy
from model.User import db ,  User
from werkzeug.security import generate_password_hash, check_password_hash
from library.UserValidator import validate_input , validate_user_update_input


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/python_test'
app.secret_key = 'mysecretkey'
db.init_app(app)

# Context processor to pass current_year to all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.datetime.now().year}

@app.route('/login')
def login_page():
    return render_template('auth/login.html')

@app.route('/login',methods=['POST'])
def login():
    return render_template('auth/login.html')

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

@app.route('/user/edit/<id>')
def editUser(id):
     user = User.query.filter_by(id=id).first()
     if user : 
        errors = session.pop('errors', {})
        return render_template('edit_user.html', user=user, errors=errors)
     else :
         return "not found"
     
     
@app.route('/user/<id>',methods=['PUT' , 'POST'])
def updateUser(id):
    name = request.form.get('name')
    email = request.form.get('email')
    
    errors = validate_user_update_input(name , email)

    if errors:
        # If there are validation errors, render the form again with the error messages
     session['errors'] = errors
     return redirect(url_for('editUser', id=id))  # Corrected: Use 'editUser' instead of editUser
    
    user = User.query.filter_by(id=id).first()
     
    if user : 
        user.name  = name
        user.email = email
        db.session.commit()
        
        return redirect('/')
 


@app.route('/todo/user/<id>')
def deleteTodo(id):
    user = User.query.filter_by(id=id).first()
    if user:
     db.session.delete(user)
     db.session.commit()
     return redirect('/')
    #  return redirect(url_for('/', message = "User successfully deleted"))



if __name__ == '__main__':
    app.run(debug=True)