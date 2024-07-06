import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import setup_db, Movie, Actor
from .auth.auth import AuthError, check_permissions, requires_auth, requires_auth_test

# ROUTES

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # MOVIE
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }),200
        
    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie_by_id(payload, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if not movie:
            abort(404)
        else:
            return jsonify({
            'success': True,
            'movie': movie.format()
        }),200
    
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def insert_movies(payload):
        body = request.get_json()
        try:
            movie = Movie(
                title = body.get('title'),
                release_date = body.get('release_date')
            )
            movie.insert()

        except Exception:
            abort(400)

        return jsonify({'success': True, 'message': 'Successfully created movie.'})

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(payload, id):
        body = request.get_json()
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if not movie:
            abort(404)
        try:
            title = body.get('title')
            release_date = body.get('release_date')
            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date
            movie.update()
        except Exception:
            abort(400)

        return jsonify({'success': True, 'message': 'Successfully updated movie with id: %s'%(id)}), 200

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if not movie:
            abort(404)
        try:
            movie.delete()
        except Exception:
            abort(400)

        return jsonify({'success': True, 'message': 'Successfully deleted movie with id: %s'%(id)}), 200


    # Actor
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }),200
        
    @app.route('/actors/<int:id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor_by_id(payload, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if not actor:
            abort(404)
        else:
            return jsonify({
            'success': True,
            'actor': actor.format()
        }),200
        
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def insert_actors(payload):
        body = request.get_json()
        try:
            actor = Actor(
                name = body.get('name'),
                age = body.get('age'),
                gender = body.get('gender')
            )
            actor.insert()

        except Exception:
            abort(400)
        
        return jsonify({'success': True, 'message': 'Successfully created actor.'})

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(payload, id):
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if not actor:
            abort(404)
        try:
            name = body.get('name')
            age = body.get('age')
            gender = body.get('gender')
            if name:
                actor.name = name
            if age:
                actor.age = age
            if gender:
                actor.gender = gender
            actor.update()
        except Exception:
            abort(400)

        return jsonify({'success': True, 'message': 'Successfully updated actor with id: %s'%(id)}), 200

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if not actor:
            abort(404)
        try:
            actor.delete()
        except Exception:
            abort(400)

        return jsonify({'success': True, 'message': 'Successfully deleted actor with id: %s'%(id)}), 200
    
    @app.route('/validate_permission', methods=['POST'])
    @requires_auth_test
    def validate_permission(payload):
        body = request.get_json()
        res = check_permissions(body.get('permission'), payload)
        return jsonify({'success': res})

    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    @app.errorhandler(AuthError)
    def auth_error(error):
        print(error)
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code


    @app.errorhandler(401)
    def unauthorized(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unathorized'
        }), 401


    @app.errorhandler(500)
    def internal_server_error(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500


    @app.errorhandler(400)
    def bad_request(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400


    @app.errorhandler(405)
    def method_not_allowed(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method Not Allowed'
        }), 405
    
    return app    

app = create_app() 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    
    