# Grit Blog
___

Grit Blog is a simple web application built using Flask, SQLAlchemy, Flask-WTF, Flask-CKEditor, and Flask-Bootstrap5. It allows users to create, edit, and delete blog posts, as well as contact the admin through a feedback form.

## Features
___

- **Create Blog Posts:** Users can create new blog posts with a title, subtitle, author, image URL, and body content.
- **Edit and Delete Posts:** Users can edit existing posts to update their content or delete them entirely.
- **View Single Post:** Users can view a single blog post along with its details and comments.
- **About Page:** Provides information about the blog and its purpose.
- **Contact Form:** Allows users to send feedback or contact the admin via email.

## Setup
___

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/godfreydekew/Grit_Blog.git
   

2. **Install Dependencies**
   ```bash
   cd Grit_Blog
   pip install -r requirements.txt

3. **Run the Application**
   ```bash
   python main.py
   
4. **Access the Application**
   ```bash
   Open your web browser and navigate to http://localhost:5001/
   
![Home page](/static/assets/img/readme.png)
![New Post](/static/assets/img/newpost.png)
![Contact](/static/assets/img/contact.png)
## Testing
___

**Unit tests are provided to ensure the functionality of the Grit Blog.
To run the tests, execute the following command:**

```bash
python -m unittest test_flask_app.py

