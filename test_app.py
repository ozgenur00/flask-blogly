import unittest
from app import app, db

class BloglyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_users_db'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302) 
        self.assertIn('/users', response.headers['Location'])  
   

    def test_users_index(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Users', str(response.data)) 

    def test_adding_user(self):
        response = self.app.post('/users/new', data=dict(
            firstname='Test',
            lastname='User',
            image_url='http://example.com/image.jpg'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test User', str(response.data)) 

