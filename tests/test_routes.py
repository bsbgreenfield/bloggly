from unittest import TestCase
from app import app
from models import db, User
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

            resp = client.get(f'/users/4/edit')
            self.assertEqual(resp.status_code, 200)

            post_resp = client.post(f'/users/4/edit', data = {'f_name': 'Benji',
                                                          'l_name': 'Green',
                                                          'username': 'BenjiGreen',
                                                          'img_url': ''},
                                                          follow_redirects=True)
            self.assertEqual(post_resp.status_code, 200)

            html = post_resp.get_data(as_text=True)
            self.assertIn('<li>First Name : Benji</li>', html)

    def test_delete(self):
        with app.test_client() as client:
            goner = User(first_name = 'goner', last_name = 'goner', username = 'goner', image_url = '')
            db.session.add(goner)
            db.session.commit()
            resp = client.post(f'/users/{goner.id}/delete')

            self.assertEqual(resp.status_code, 302)
            