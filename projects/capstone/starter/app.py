import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, Role
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    return app


app = create_app()


@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    try:
        actors = Actor.query.order_by(Actor.id).all()
        formated_actors = [actor.format() for actor in actors]
        print(formated_actors)
        return jsonify({
            "success": True,
            "actors": formated_actors
        })
    except BaseException:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    try:
        query = Actor.query.get(actor_id)
        query.delete()
        return jsonify({
            "success": True,
            "deleted": actor_id,
            "total_actors": len(Actor.query.all())
        })
    except BaseException:
        abort(404)


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actor(payload):
    
    try:
        body = request.get_json()

        name = body['name']
        age = body['age']
        gender = body['gender']
        actor = Actor(name=name, gender=gender, age=age)
        actor.insert()

        return jsonify({
            "success": True,
            "created": actor.id,
            "total_actors": len(Actor.query.all())
        })
    except BaseException:
        abort(400)


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')

def update_actor(payload, actor_id):

    data = request.get_json()
    name = data.get('name', None)
    age = data.get('age', None)
    gender = data.get('gender', None)

    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        if name is None:
            abort(400)

        if name is not None:
            actor.name = name

        if age is not None:
            actor.age = age

        if gender is not None:
            actor.gender = gender

        actor.update()

        actors = Actor.query.order_by(Actor.id).all()
        formated_actors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': formated_actors
        }), 200
    except BaseException:
        abort(422)


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')

def get_movies(payload):

    try:

        movies = Movie.query.order_by(Movie.id).all()
        formated_movies = [movie.format() for movie in movies]
        print(formated_movies)

        return jsonify({
            "success": True,
            "movies": formated_movies
        })

    except BaseException:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):

    try:

        query = Movie.query.get(movie_id)
        query.delete()
        return jsonify({
            "success": True,
            "deleted": movie_id,
            "total_movies": len(Movie.query.all())
        })

    except BaseException:
        abort(404)


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movie(payload):

    try:

        body = request.get_json()
        title = body['title']
        release_date = body['release_date']
        movie = Movie(title=title, release_date=release_date)
        movie.insert()

        return jsonify({
            "success": True,
            "created": movie.id,
            "total_movies": len(Movie.query.all())
        })
    except BaseException:
      
      
        abort(400)


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, movie_id):
    data = request.get_json()
    title = data.get('title', None)
    release_date = data.get('release_date', None)
    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        if title is None:
            abort(400)

        if title is not None:
            movie.title = title

        if release_date is not None:
            movie.release_date = release_date

        movie.update()

        movies = Movie.query.order_by(Movie.id).all()
        formated_movies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': formated_movies
        }), 200
    except BaseException:
        abort(422)


@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        "success": False,
        "status_code": 422,
        "message": "Unprocessable Entity"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "status_code": 404,
        "message": "Not Found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "status_code": 400,
        "message": "Bad Request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403

@app.errorhandler(405)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405

@app.errorhandler(AuthError)
def authentication_error(error):

    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description'],
        "code": error.error['code']
    }), error.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)