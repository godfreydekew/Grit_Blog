import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditor, CKEditorField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
import smtplib
from sqlalchemy import Integer, String, Text

# Log in information for SMTPLIB
my_email = "dekewgodfrey@gmail.com"
password = "xibegzoydgxlerka"

app = Flask(__name__)

# Editor for the custom textfield
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# A fake blog api for testing purposes
# posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

# Creating SQLite database
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


class User(db.Model):
    """
    This class represents a user data model
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    name = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


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

    returns:
        str: The Index HTML page
    """
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route('/<int:post_id>')
def show_post(post_id):
    '''
    This function returns a single blog post
    with given id in the database

    returns:
        str: The Post HTML page
    '''
    requested_post = db.get_or_404(BlogPost, post_id)
    # requested_post = db.session.get(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


@app.route('/new-post', methods=['POST', 'GET'])
def new_post():
    """
    Endpoint to create a new blog post
    parameters for POST will be retrieved from the form fields

    returns:
        str: If post request home page is rendered otherwise make_post
    """
    my_form = PostForm()
    x = datetime.datetime.now()
    month = x.strftime("%B")
    day = x.strftime("%d")
    year = x.strftime("%Y")
    if request.method == 'POST':
        if my_form.validate_on_submit():
            # Form was submitted, handle the data here
            my_new_post = BlogPost(
                title=request.form['title'],
                subtitle=request.form['sub_title'],
                author=request.form['author'],
                img_url=request.form['image_url'],
                body=request.form['body'],
                date=f"{month} {day}, {year}",
            )
            db.session.add(my_new_post)
            db.session.commit()

        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=my_form)


@app.route('/edit-post/<post_id>', methods=['GET', 'POST'])
def edit(post_id):
    """
    This endpoint allow users to edit a post dynamically
    the changes will be updated automatically

    returns:
        str: The HTML with flask form to edit the post
    """
    post = db.session.get(BlogPost, post_id)
    edit_form = PostForm(
        title=post.title,
        sub_title=post.subtitle,
        image_url=post.img_url,
        author=post.author,
        body=post.body
    )

    if request.method == 'GET':
        return render_template("make-post.html", form=edit_form)
    else:
        post.title = request.form['title']
        post.subtitle = request.form['sub_title']
        post.img_url = request.form['image_url']
        post.author = request.form['author']
        post.body = request.form['body']
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))


@app.route('/delete/<post_id>')
def delete(post_id):
    """
    This endpoint allow users to delete a post dynamically
    the changes will be updated automatically

    returns:
        str: The HTML of home page with all the post
    """
    post = db.session.get(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


@app.route("/about")
def about():
    """
    This function returns the about page

    returns:
        str: The HTML for the about page
    """
    return render_template("about.html")


# @app.route("/contact")
# def contact():
#     return render_template("contact.html")


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    """
    This function allow users to contact the admin with
    email and, they can send their feedback

    returns:
        str: The HTML for the contact page with a form
    """
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

        # send email to myself with the user information
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=email,
                to_addrs=my_email,
                msg=email_content
            )

        return render_template("contact.html", message=success_message)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
