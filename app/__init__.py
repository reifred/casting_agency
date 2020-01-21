import os
import json

from sqlalchemy import exc
from flask_cors import CORS
from dateutil.parser import parse

from flask import Flask, request, jsonify, abort
from app.models import Actor, Movie, setup_db
from auth.auth import requires_auth, AuthError

app = Flask(__name__)
setup_db(app)
CORS(app)


PER_PAGE = 10

# ROUTES
'''
Retrieves a paginated list of actors.
'''
@app.route('/api/v1/actors', methods=['GET'])
@requires_auth(permission='get:actors')
def retrieve_actors():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', PER_PAGE, type=int)
    offset = (page - 1) * limit
    try:
        actors = Actor.query.offset(offset).limit(limit).all()
        if not actors:
            abort(404)
        data = [actor.format() for actor in actors]
        total_actors = len(Actor.query.all())
        return jsonify({
                'success': True,
                'actors': data,
                'total-actors': total_actors
            }), 200
    except Exception as error:
        raise error


'''
Retrieves a single actor by their ID.
'''
@app.route('/api/v1/actors/<int:id>', methods=['GET'])
@requires_auth(permission='get:actors')
def retrieve_actor(id):
    try:
        actor = Actor.query.get(id)
        if not actor:
            abort(404)
        return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200
    except Exception as error:
        raise error


'''
Creates a new actor.
'''
@app.route('/api/v1/actors', methods=['POST'])
@requires_auth(permission='post:actors')
def add_actor():
    try:
        data = json.loads(request.data)
        actor = Actor(**data)
        actor.insert()
        return jsonify({
                'success': True,
                'actor': actor.format()
            }), 201
    except Exception as error:
        raise error


'''
Edits an actor's details.
'''
@app.route('/api/v1/actors/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:actors')
def edit_actor(id):
    try:
        actor = Actor.query.get(id)
        if not actor:
            abort(422)
        data = json.loads(request.data)
        for key, value in data.items():
            setattr(actor, key, value)
        actor.update()
        return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200
    except Exception as error:
        raise error


'''
Deletes an actor.
'''
@app.route('/api/v1/actors/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:actors')
def delete_actor(id):
    try:
        actor = Actor.query.get(id)
        if not actor:
            abort(422)
        actor.delete()
        return jsonify({
                'success': True,
                'deleted': actor.id
            }), 200
    except Exception as error:
        raise error


'''
Retrieves a paginated list of movies.
'''
@app.route('/api/v1/movies', methods=['GET'])
@requires_auth(permission='get:movies')
def retrieve_movies():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', PER_PAGE, type=int)
    offset = (page - 1) * limit
    try:
        movies = Movie.query.offset(offset).limit(limit).all()
        if not movies:
            abort(404)
        data = [movie.format() for movie in movies]
        total_movies = len(Movie.query.all())
        return jsonify({
                'success': True,
                'movies': data,
                'total-movies': total_movies
            }), 200
    except Exception as error:
        raise error


'''
Retrieves a single movie.
'''
@app.route('/api/v1/movies/<int:id>', methods=['GET'])
@requires_auth(permission='get:movies')
def retrieve_movie(id):
    try:
        movie = Movie.query.get(id)
        if not movie:
            abort(404)
        return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200
    except Exception as error:
        raise error


'''
Creates a movie.
'''
@app.route('/api/v1/movies', methods=['POST'])
@requires_auth(permission='post:movies')
def add_movie():
    try:
        data = json.loads(request.data)
        movie = Movie(**data)
        movie.insert()
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 201
    except Exception as error:
        raise error


'''
Edits a movie.
'''
@app.route('/api/v1/movies/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:movies')
def edit_movie(id):
    try:
        movie = Movie.query.get(id)
        if not movie:
            abort(422)
        data = json.loads(request.data)
        for key, value in data.items():
            setattr(movie, key, value)
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    except Exception as error:
        raise error


'''
Deletes a movie.
'''
@app.route('/api/v1/movies/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:movies')
def delete_movie(id):
    try:
        movie = Movie.query.get(id)
        if not movie:
            abort(422)
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': id
        }), 200
    except Exception as error:
        raise error


'''
Error handling for resource not found.
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


'''
Error handling for bad request.
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


'''
Error handling for unprocessable entity.
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unable to process request'
    }), 422


'''
Error handling for method not allowed.
'''
@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


'''
Error handling for internal server errors.
'''
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500


'''
Error handling for Authentication errors.
Returns 401, 403 error codes.
'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': f"{error.error['code']}: {error.error['description']}"
    }), error.status_code
