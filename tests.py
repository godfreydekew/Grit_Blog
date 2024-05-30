import unittest
from main import app, db, BlogPost
from flask import url_for

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_home_page(self):
        with app.test_request_context():
            response = self.client.get(url_for('get_all_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Grit Blog", response.data)

    def test_new_post_page(self):
        with app.test_request_context():
            response = self.client.get(url_for('new_post'))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        with app.test_request_context():
            response = self.client.post(url_for('new_post'), data={
                'title': 'Test Title',
                'sub_title': 'Test Subtitle',
                'author': 'Test Author',
                'image_url': 'http://example.com/image.jpg',
                'body': 'Test body content',
                'submit': True
            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_show_post(self):
        with app.test_request_context():
            post = BlogPost(
                title='Test Title',
                subtitle='Test Subtitle',
                author='Test Author',
                img_url='http://example.com/image.jpg',
                body='Test body content',
                date='January 1, 2023'
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id
        with app.test_request_context():
            response = self.client.get(url_for('show_post', post_id=post_id))
        self.assertEqual(response.status_code, 200)

    def test_edit_post_page(self):
        with app.test_request_context():
            post = BlogPost(
                title='Test Title',
                subtitle='Test Subtitle',
                author='Test Author',
                img_url='http://example.com/image.jpg',
                body='Test body content',
                date='January 1, 2023'
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id
            response = self.client.get(url_for('edit', post_id=post_id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit Post", response.data)

    def test_edit_post(self):
        with app.test_request_context():
            post = BlogPost(
                title='Test Title',
                subtitle='Test Subtitle',
                author='Test Author',
                img_url='http://example.com/image.jpg',
                body='Test body content',
                date='January 1, 2023'
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id
            response = self.client.post(url_for('edit', post_id=post_id), data={
                'title': 'Updated Title',
                'sub_title': 'Updated Subtitle',
                'author': 'Updated Author',
                'image_url': 'http://example.com/updated_image.jpg',
                'body': 'Updated body content',
                'submit': True
            }, follow_redirects=True)
            updated_post = BlogPost.query.get(post_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_post.title, 'Updated Title')
        self.assertEqual(updated_post.author, 'Updated Author')

    def test_delete_post(self):
        with app.test_request_context():
            post = BlogPost(
                title='Test Title',
                subtitle='Test Subtitle',
                author='Test Author',
                img_url='http://example.com/image.jpg',
                body='Test body content',
                date='January 1, 2023'
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id
            response = self.client.get(url_for('delete', post_id=post_id), follow_redirects=True)
            deleted_post = BlogPost.query.get(post_id)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(deleted_post)

    def test_about_page(self):
        with app.test_request_context():
            response = self.client.get(url_for('about'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"About", response.data)

    def test_contact_page(self):
        with app.test_request_context():
            response = self.client.get(url_for('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Contact", response.data)

    def test_contact_form_submission(self):
        with app.test_request_context():
            response = self.client.post(url_for('contact'), data={
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '123456789',
                'message': 'This is a test message',
            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Successfully sent your message", response.data)

    # Add more test methods as needed

if __name__ == "__main__":
    unittest.main()
