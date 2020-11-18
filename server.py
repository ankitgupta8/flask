from flask import Flask, render_template, request, redirect
import csv
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail
from datetime import date

app = Flask(__name__)

with open('config.json', 'r') as js:
    params = json.load(js)["params"]
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'ankit.kapilvastu@gmail.com',
    MAIL_PASSWORD = 'Ankit@123'
)

mail = Mail(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
db = SQLAlchemy(app)



class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text(100), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(50), nullable=False)
    sub_title = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = date.today()

class User_post(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    
    date = date.today()

@app.route('/')
def index():
    posts = Post.query.filter_by().all()
    user_post = User_post.query.filter_by().all()
    return render_template('index.html', params=params, posts=posts, user_post=user_post)


@app.route('/post/<string:post_slug>', methods=['GET'])
def post_route(post_slug):

    post = Post.query.filter_by(slug=post_slug).first()


    return render_template('single-post.html', post=post)


@app.route('/create_post', methods=['POST', 'GET'])
def create_posts():

    if request.method == 'POST':
        name2 = request.form.get('name')
        email2 = request.form.get('email')
        content2 = request.form.get('content')
        entry2 = User_post(name=name2, email=email2, content=content2)
        db.session.add(entry2)
        db.session.commit()
    posts = Post.query.filter_by().all()
    user_post = User_post.query.filter_by().all()
    return render_template('index.html', params=params, user_post=user_post,posts=posts)

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Contacts(name=name, email=email, message=message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message(name+ ' messaged you', 
            sender = email,
            recipients = 'ankit.kapilvastu@gmail.com'.split(),
            body = message)
    return redirect('contact.html')


@app.route('/<page_name>')
def func(page_name):
    return render_template(page_name, params=params)



# def write_to_csv(data):
#     with open("database.csv", mode="a") as db2:
#         email = data['email']
#         subject = data['subject']
#         message = data['message']
#         # db.write(f"\n{email}, {subject}, {message}")
#         csv_write = csv.writer(
#             db2, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         csv_write.writerow([email, subject, message])


# @app.route('/submit_form', methods=['POST', 'GET'])
# def submit_form():
#     data = request.form.to_dict()
#     write_to_csv(data)

#     return render_template("index.html", post=data)
    # if request.method == 'POST':
    #     data = request.form.to_dict()
    #     write_to_csv(data)
    #     return redirect("thankyou.html")
    # else:
    #     return "Something got wrong!"

    # return 'Form Submitted Successfully !! '
