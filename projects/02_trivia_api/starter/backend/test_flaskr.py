import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('localhost:5433', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['categories']))


    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['current_category'],None)

    def test_422_sent_requesting_beyond_valid_pages(self):
        response = self.client().get('/questions?page=500')
        data = json.loads(response.data)

        self.assertEqual(response.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['message'],"Not Found")

    def test_delete_question(self):
        response = self.client().delete('/questions/1')
        data = json.loads(response.data)

        question = Question.query.get(1)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],1)
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)

    def test_404_if_question_does_not_exist(self):
        response = self.client().delete('/questions/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['message'],"Not Found")

    def test_post_question(self):
        response = self.client().post('/questions', json={'question': ' Which England footballer was famously never given a yellow card?', 'answer' : 'Gary Lineker', 'difficulty' : 3, 'category' : 1})
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])

    def test_400_if_post_question_bad_request(self):
        response = self.client().post('/questions', json={'q': ' Which England footballer was famously never given a yellow card?', 'a' : 'Gary Lineker', 'd' : 3, 'c' : 1})
        data = json.loads(response.data)

        self.assertEqual(response.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['message'],"Bad Request")

    def test_search_question(self):
        response = self.client().post('/questions/search', json={'searchTerm': 'which'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'],None)

    def test_400_if_search_question_bad_request(self):
        response = self.client().post('/questions/search', json={'search': 'which'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['message'],"Bad Request")   

    def test_get_questions_by_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)
        category = Category.query.get(1)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'],category.type)

    def test_404_sent_requesting_beyond_valid_categories(self):
        response = self.client().get('/categories/1000/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['message'],"Not Found")     

    def test_get_question_quizzes(self):
        category = Category.query.get(4)
        questions = Question.query.filter_by(category=category.id).all()

        previous_questions = [question.id for question in questions]

        response = self.client().post('/quizzes', json={"quiz_category": category.format(), "previous_questions": previous_questions})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_get_question_quizzes_bad_request(self):
        category = Category.query.get(4)
        questions = Question.query.filter_by(category=category.id).all()

        previous_questions = [question.id for question in questions]

        response = self.client().post('/quizzes', json={"category": category.format(), "questions": previous_questions})
        data = json.loads(response.data)

        self.assertEqual(response.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['message'],"Bad Request")   


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()