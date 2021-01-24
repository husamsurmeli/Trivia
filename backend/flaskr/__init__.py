import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy, functools
from flask_cors import CORS
from models import setup_db, Question, Category, db
from sqlalchemy import func

def create_app(test_config=None):
  app = Flask(__name__)
  app.config.from_object('config')
  db.init_app(app)
  CORS(app)
  
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      return response
  #if used more then once, i defined them beforehand
  def start(request):
      page = request.args.get('page', 1, type=int)
      start = (page-1) * 10
      return start

  def allcategories():
      allcategories={category.id: category.type for category in Category.query.all()}
      return allcategories
        
  @app.route('/categories')
  def categories():
      try:
          return jsonify({
          'success': True,
          'categories': allcategories(),
          })
      except:
          abort(422)

  @app.route('/questions')
  def questions():
      try:
          return jsonify({
              'success': True,
              'questions': [question.format() for question in Question.query.offset(start(request)).limit(10)],
              'total_questions': len(Question.query.all()),
              'categories': allcategories(),
              'current_category': None
              })
      except:
          abort(422)

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete(question_id):
      question = Question.query.filter(Question.id == question_id).scalar()
      if question is None:
          abort(404)
      try:
          question.delete()
          return jsonify({
          'success': True,
          })
      except:
          abort(422)

  @app.route('/questions', methods=['POST'])
  def create():
      Front = request.json
      question = Front['question']
      answer = Front['answer']
      # chehcking here question and answer is enough. because categories is there by an another method via frontend
      if len(question)>0 and len(answer)>0 :
          difficulty = Front['difficulty']
          category = Front['category']
      else:
          abort(400)        
      try:
          db.session.add(Question(
              question=question,
              answer=answer,
              difficulty=difficulty,
              category=category,
              ))
          db.session.commit()
          db.session.close()
          return jsonify({
              'success': True,
              })
      except:
          abort(422)
              
  @app.route('/questions/search', methods=['POST'])
  def search():
      Front = request.json
      SearchTerm =Front['searchTerm']
      if SearchTerm is None:
          abort(400)
      questions = [question.format() for question in Question.query.filter(Question.question.ilike(f'%{SearchTerm}%')).all()]
      try:
          return jsonify({
          'success': True,
          'questions': questions,
          'total_questions': len(questions)
          })
      except:
        abort(422)
      
 
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def getcategory(category_id):
    categoryGiven = Category.query.filter(Category.id == category_id).one_or_none()
    if categoryGiven is None:
        abort(404)
    try:
        questions=[question.format() for question in Question.query.filter(Question.category == category_id).offset(start(request)).limit(10)]
        return jsonify({
            'success': True,
            'questions': questions,
            'current_category': Category.query.get(category_id).format(),
            'total_questions': len(questions)
        })
    except:
        abort(422)

  @app.route('/quiz', methods=['POST'])
  def quiz():
      Front = request.json
      category = Front['quiz_category']
      pre = Front['previous_questions']
      #for the sake of testing 500 at least once :lets assume a case ; if categories dont load it should be a an internal sever here.
      if category is None:
          abort(500)
      question = None
      if category != 0:
          questions = Question.query.filter(Question.id.notin_(pre), Question.category == category).order_by(func.random()).all()
      else:
          questions = Question.query.filter(Question.id.notin_(pre)).order_by(func.random()).all()
      if len(questions)>0:
          question = questions[0].format()
      try:
          return jsonify({
              'success': True,
              'question': question
              })
      except:
        abort(422)
  
  @app.errorhandler(404)
  def notfound(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'not found'
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'unprocessable'
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(500)
  def server(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "internal server error"
      }), 500

  return app