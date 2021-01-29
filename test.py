from unittest import TestCase
from app import app, handle_input
from flask import session
from boggle import Boggle
import json

app.config['TESTING'] = True
class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        self.app = app.test_client()

    def test_home_page_routes(self):
        """Test that get requests for home page return 200"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_post_routes(self):
        """Test the two types of post requests made to home page"""
        response = self.app.post('/', json={ "score" : 100}, content_type='application/json')  
        self.assertEqual(session['high_score'], 100)
        response = self.app.post('/', json={"word": "trapezoid"})
        return_string = response.get_data(as_text=True)
        self.assertIn("Your word was", return_string)

    def test_reset(self):
        """Test redirect fired upon restart"""
        self.assertEqual(self.app.get('/reset').status_code, 302)

    def test_duplicate_entry(self):
        with self.app.session_transaction() as test_session:
            test_session['guesses'] = ['cylinder']
            self.assertEqual(handle_input('cylinder'), "already guessed")
                