from unittest import TestCase
from app import app
from models import db, User, Post
from flask import request

class Tester(TestCase):

    def setUp(self):
        tester = User(first_name = 'test', last_name = 'test', username = 'testerino', image_url = '')
        db.session.add(tester)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        User.query.filter_by(first_name='test').delete()
        db.session.commit()


    def test_home(self):
        """should redirect to /users"""
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 302)


   
    
    def test_create(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            self.assertEqual(resp.status_code, 200)

            post_resp = client.post('/users/new', data = {'f_name': 'testTwo',
                                                          'l_name': 'testTwo',
                                                          'username': 'testerTwo',
                                                          'img_url': ''},
                                                          follow_redirects=True)
            self.assertEqual(post_resp.status_code, 200)

            html = post_resp.get_data(as_text=True)
            self.assertIn('<li>First Name : testTwo</li>', html)

            User.query.filter_by(first_name='testTwo').delete()
            db.session.commit()

    
    def test_edit(self):
        with app.test_client() as client:
            tester = User.query.filter(User.username == 'testerino').first()
            resp = client.get(f'/users/{tester.id}/edit')
            self.assertEqual(resp.status_code, 200)

            post_resp = client.post(f'/users/{tester.id}/edit', data = {'f_name': 'test',
                                                          'l_name': 'test',
                                                          'username': 'testerino',
                                                          'img_url': ''},
                                                          follow_redirects=True)
            self.assertEqual(post_resp.status_code, 200)

            html = post_resp.get_data(as_text=True)
            self.assertIn('<li>First Name : test</li>', html)

    def test_delete(self):
        with app.test_client() as client:
            goner = User(first_name = 'goner', last_name = 'goner', username = 'goner', image_url = '')
            db.session.add(goner)
            db.session.commit()
            resp = client.post(f'/users/{goner.id}/delete')

            self.assertEqual(resp.status_code, 302)
            
    def make_new_post(self):
        with app.test_client as client:
            tester = User.query.filter(User.username == 'testerino').first()
            resp = client.get(f'/users/{tester.id}/post')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<textarea name="content" cols="30" rows="10">', html)
    
    def submit_new_post(self):
        with app.test_client as client:
            tester = User.query.filter(User.username == 'testerino').first()
            resp = client.post(f'/users/{tester.id}/post', data = {'title': 'test', 'content': 'test'}, 
                               follow_redirects=True)

            html = resp.get_data(as_text=True)

            test_post = Post.query.filter_by(title = 'test').first()
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<form action="/posts/{test_post.id}/delete" method="POST"><button>Delete</button></form>', html)
            test_post.delete()
            db.commit()


