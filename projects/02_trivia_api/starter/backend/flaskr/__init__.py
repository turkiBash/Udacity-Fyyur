from crypt import methods
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories',methods=['GET'])
  def get_categories():
      try:
        categories = Category.query.order_by(Category.id).all()
        formated_categories = [category.type.format() for category in categories]
        print(formated_categories)
        return jsonify({
          "success" : True,
          "categories" : formated_categories
        })
      except: 
        abort(422)  
      

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions',methods=['GET'])
  def get_questions():
    try:
      page = request.args.get('page', 1, type=int)
      start = (page-1)*QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      questions = Question.query.order_by(Question.id).all()
      categories = Category.query.order_by(Category.id).all()
      formated_questions = [question.format() for question in questions]
      formated_categories = [category.type.format() for category in categories]
      current_category = None
      selected_questions = questions[start:end]
      
      if len(selected_questions)==0:
        abort(422)
        
      return jsonify({
        "success" : True,
        "questions" : formated_questions[start:end],
        "total_questions": len(formated_questions),
        "categories": formated_categories,
        "current_category": current_category        
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      question.delete()
      
      if question is None:
            abort(404)
      
      return jsonify({
        'success': True,
        'deleted': question_id
            })
    except:
      abort(404)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions',methods=['POST'])
  def post_question():
    try:
      body = request.get_json()
      
      question_text = body['question']
      answer = body['answer']
      difficulty = body['difficulty']
      category = body['category']
      question = Question(question=question_text, answer=answer, category=category, difficulty=difficulty)
      question.insert()

      return jsonify({
        "success" : True,
        "created": question.id,
        "total_questions": len(Question.query.all())
      })
    except:
      abort(400)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def serach_question():
        try:
          searchTerm = request.get_json()['searchTerm']
          questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).order_by(Question.id).all()
          formated_questions = [question.format() for question in questions]
          return jsonify({
        "success" : True,
        "questions" : formated_questions,
        "total_questions" : len(formated_questions),
        "current_category" : None
      })
        except:
          abort(400)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions',methods=['GET'])
  def get_question_by_id(category_id):
        try:
          id = category_id
          category = Category.query.get(id)
          questions = Question.query.filter_by(category=id).order_by(Question.id).all()
          formated_questions = [question.format() for question in questions]
          return jsonify({
            "success" : True,
            "question" : formated_questions,
            "total_questions" : len(formated_questions),
            "corrent_category" : category.type
          })
        except:
          abort(404) 
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes',methods=['POST'])
  def get_question_quizzes():
        try:
          body = request.get_json()
          
          previous_questions = body['previous_questions']
          quiz_category = body['quiz_category']
          questions = Question.query.filter_by(category=quiz_category['id']).filter(Question.id.notin_((previous_questions))).all()
          if len(questions)==0:
            return jsonify({
              "success" : True
            })
          else:
            random_question = random.choice(questions).format()
            return jsonify({
              "success" : True,
              "questions" : random_question
            })
            
        except:
          abort(400)
                    
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  @app.errorhandler(422)
  def unprocessable_entity(error):
        return jsonify({
          "success" : False,
          "status_code" : 422,
          "message" : "Unprocessable Entity"
        }), 422
        
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success" : False,
      "status_code" : 404,
      "message" : "Not Found"
    }), 404  

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success" : False,
      "status_code" : 400,
      "message" : "Bad Request"
    }), 400  
  
  return app

    