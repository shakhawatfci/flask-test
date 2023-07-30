from flask import Flask, render_template, request, redirect, url_for, flash , session 
import datetime
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from model.User import db ,  User
from werkzeug.security import generate_password_hash, check_password_hash
from library.UserValidator import validate_input , validate_user_update_input
import uuid
import os
import random


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/python_test'
app.secret_key = 'mysecretkey'
db.init_app(app)
# socketio = SocketIO(app)
socketio = SocketIO(app) 

UPLOAD_FOLDER = 'static/images/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Context processor to pass current_year to all templates

# @socketio.on('connect')
# def on_connect():
#     print('Client connected')
  

# @socketio.on('disconnect')
# def on_disconnect():
#     print('Client disconnected')

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
    page = int(request.args.get('page', 1))
    per_page = 5
    all_records = User.query.order_by(desc(User.created_at)).paginate(page=page, per_page=per_page)
    message = ''
    if(request.args.get('message')):
        message = request.args.get('message')
    
    socketio.emit('USER11', {'logout': random.random()})    
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
        return render_template('create_user.html', errors=errors)
    
    password_hash = generate_password_hash(password)
    user = User()
    user.name = name
    user.email = email
    user.password = password_hash
    file = request.files['image']
    if file:
        filename = file.filename
        _, file_extension = os.path.splitext(filename)
        unique_string = str(uuid.uuid4()) + file_extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_string))
        user.image = unique_string;
        
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
     session['errors'] = errors
     return redirect(url_for('editUser', id=id))
    
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

@app.route('/static/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename=filename), code=301)



if __name__ == '__main__':
    app.run(debug=True)