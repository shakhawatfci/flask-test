from flask import Flask , render_template

app = Flask(__name__)

@app.route('/')
def index():
    my_dict = {}
    my_dict['name'] = 'John'
    my_dict['age'] = 30
    my_dict['city'] = 'New York'
    return render_template('index.html',diet = my_dict)

@app.route('/todo')
def about():
    return "This is the About page."


@app.route('/todo/<id>')
def show(id):
    return id



if __name__ == '__main__':
    app.run(debug=True)