from unittest import TestCase

from flask import Flask

from src.auth import bearer_required


class AuthBearerTestCase(TestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def index():
            return 'Anonymous'

        @self.app.route('/authorized')
        @bearer_required('SOME-TOKEN')
        def authorized():
            return 'Authorized'

    def test_anonymous(self):
        with self.app.test_client() as c:
            result = c.get('/')
            self.assertEqual('Anonymous', result.data.decode())

    def test_auth_required(self):
        with self.app.test_client() as c:
            result = c.get('/authorized')
            self.assertEqual(401, result.status_code)
            self.assertEqual('Bearer token is required', result.data.decode())

    def test_auth_basic_schema(self):
        with self.app.test_client() as c:
            result = c.get('/authorized', headers={'Authorization': 'Basic Rk9POkJBUg=='})
            self.assertEqual(401, result.status_code)
            self.assertEqual('Bearer token is required', result.data.decode())

    def test_auth_partial_value(self):
        with self.app.test_client() as c:
            result = c.get('/authorized', headers={'Authorization': 'Bearer '})
            self.assertEqual(401, result.status_code)
            self.assertEqual('Authorization is malformed', result.data.decode())

    def test_auth_wrong_token(self):
        with self.app.test_client() as c:
            result = c.get('/authorized', headers={'Authorization': 'Bearer FAKE'})
            self.assertEqual(401, result.status_code)
            self.assertEqual('The token is incorrect', result.data.decode())

    def test_auth_correct_token(self):
        with self.app.test_client() as c:
            result = c.get('/authorized', headers={'Authorization': 'Bearer SOME-TOKEN'})
            self.assertEqual(200, result.status_code)
            self.assertEqual('Authorized', result.data.decode())
