import unittest
from app import app, db
from models import User, Post

class BloglyPostsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_users_db'
        db.create_all()

        # Create a test user for the posts
        test_user = User(firstname='Test', lastname='User', image_url='http://example.com/image.jpg')
        db.session.add(test_user)
        db.session.commit()

        # Create a test post
        test_post = Post(title='Test Post', content='Test Content', user_id=test_user.id)
        db.session.add(test_post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_post_detail(self):
        test_post = Post.query.first()
        response = self.app.get(f'/users/posts/{test_post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Post', str(response.data))

    def test_add_post(self):
        test_user = User.query.first()
        response = self.app.post(f'/users/{test_user.id}/posts/new', data=dict(
            title='New Test Post',
            description='New Test Description'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('New Test Post', str(response.data))

<<<<<<< HEAD

def test_user_detail(self):
    response = self.app.get('/users/1')
    self.assertEqual(response.status_code, 200)
    self.assertIn('User Detail', str(response.data))


def test_add_post(self):
    self.app.post('/users/new', data=dict(
        firstname='Test',
        lastname='User',
        image_url='http://example.com/image.jpg'
    ))

    response = self.app.post('/users/1/posts/new', data=dict(
        title='New Post',
        description='This is a test post.',
        tags='' 
    ), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn('New Post', str(response.data))

def test_delete_tag(self):

    self.app.post('/tags/new', data=dict(name='TestTag'))
    response = self.app.post('/tags/1/delete', follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    tag_list_response = self.app.get('/tags')
    self.assertNotIn('TestTag', str(tag_list_response.data))
=======
    def test_edit_post(self):
        test_post = Post.query.first()
        response = self.app.post(f'/posts/{test_post.id}/edit/edited', data=dict(
            title='Edited Test Post',
            content='Edited Test Content'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Edited Test Post', str(response.data))

    def test_delete_post(self):
        test_post = Post.query.first()
        response = self.app.post(f'/posts/{test_post.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Test Post', str(response.data))

if __name__ == '__main__':
    unittest.main()
>>>>>>> bb531f135d8d527f2777c551d5058d3877c42f0a
