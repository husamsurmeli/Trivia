import os, random
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db
from sqlalchemy import func


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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

    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
    
    def test_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])    

    def test_new_question(self):
        test_question = {
            'question': 'testestloremipsum12345testtest',
            'answer': 'test',
            'difficulty': 1,
            'category': 1,
            }
        res = self.client().post('/questions', json=test_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        delnewq = Question.query.filter_by(question='testestloremipsum12345testtest').first_or_404()
        db.session.delete(delnewq)
        db.session.commit()
        db.session.close()

    def test_400_new_question(self):
        test_empty = {
            'question': '',
            'answer': '',
            'difficulty': '',
            'category': '',
            }
        res = self.client().post('/questions', json=test_empty)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")
                

    def test_delete_question(self):
        db.session.add(Question(
            question="test",
            answer="testestloremipsum12345testtest",
            difficulty=1,
            category=1,
        ))
        db.session.commit()
        db.session.close()
        testq = Question.query.filter(Question.answer == 'testestloremipsum12345testtest').with_entities(Question.id)
        for testid in testq:
            print(testid[0])
        res = self.client().delete('/questions/{}'.format(testid[0]))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_404_delete(self):
        #instead of giving a very big number, i queried the max id and add one to it. imagine our app grows so fast :)
        questions = Question.query.with_entities(Question.id).order_by(func.max(Question.id)).group_by(Question.id).limit(1)
        for maxIdq in questions:
            maxQuestion=int(maxIdq[0])
            absentidq=maxQuestion+1
            return absentidq
        res = self.client().delete('/questions/{}'.absentidq)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "not found")

    def test_400_search(self):
        nosearchterm={'searchTerm': None}
        res = self.client().post('/questions/search', json=nosearchterm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_search(self):
        res = self.client().post('/questions/search', json={"searchTerm": ""})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])

    def test_category_based_questions(self):
        #imagine that we have not 6 but lots of categories. not to risk it i queried a random category id
        categories = Category.query.with_entities(Category.id).order_by(func.random()).limit(1)
        for randomId in categories:
            print(randomId[0])
        res = self.client().get('/categories/{}/questions'.format(randomId[0]))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['total_questions'])

    def test_404_category_based_questions(self):
        #same approach as test_404_delete
        categories = Category.query.with_entities(Category.id).order_by(func.max(Category.id)).group_by(Category.id).limit(1)
        for maxIdc in categories:
            maxCategory=int(maxIdc[0])
            absentidc=maxCategory+1
            return absentidc
        res = self.client().get('/categories/{}/questions'.absentidc)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_500_quiz(self):
        test_empty = {
            'quiz_category': None,
            'previous_questions': '',
            }
        res = self.client().post('/quiz', json=test_empty)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "internal server error")

    def test_quiz(self):
        #i want to test the case when user clicks "ALL"
        allCatQuiz={"previous_questions": [], "quiz_category": 0}
        res = self.client().post('/quiz',json=(allCatQuiz))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])

if __name__ == "__main__":
    unittest.main()