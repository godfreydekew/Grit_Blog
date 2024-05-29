from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime
import requests
import smtplib


my_email = "dekewgodfrey@gmail.com"
password = "xibegzoydgxlerka"

#A fake blog api for testing purposes
#posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


class BlogPost(db.Model):
    """
    This class represents a blog post data model
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    """
    Create the database tables if they don't exist
    """
    db.create_all()

class PostForm(FlaskForm):
    """
    This class represents a form for creating a blog post
    """
    title = StringField('Title')
    sub_title = StringField('Subtitle')
    author = StringField('Author')
    image_url = StringField('Image_url')
    body = CKEditorField('Body')  # <--
    submit = SubmitField('Submit')

@app.route('/')
def get_all_posts():
    """
    This function returns all the blog posts
    """
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


# @app.route("/contact")
# def contact():
#     return render_template("contact.html")


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    else:
        name = request.form['name']
        email = request.form['email']
        number = request.form['phone']
        message = request.form['message']

        success_message = 'Successfully sent your message'
        subject = "Contact Form Submission"

        # Construct the email content with proper formatting
        email_content = f"Subject: {subject}\n\n"
        email_content += f"Name: {name}\n"
        email_content += f"Email: {email}\n"
        email_content += f"Number: {number}\n"
        email_content += f"Message:\n{message}"
        #sendimh email to myself

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=email,
                to_addrs=my_email,
                msg=email_content
            )

        return render_template("contact.html", message=success_message)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)



if __name__ == "__main__":
    app.run(debug=True, port=5001)
