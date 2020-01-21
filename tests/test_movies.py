import os
import json
import unittest
from flask_sqlalchemy import SQLAlchemy
from datetime import date

from app import app
from app.models import setup_db, Actor, Movie
from tests import mock_data
from .auth_setup import get_token


assistant_token = get_token('assistant')
director_token = get_token('director')
producer_token = get_token('producer')


class MoviesTestCase(unittest.TestCase):
    """This class represents the Movies test case """
    def setUp(self):
        """Define test variables and initialize app"""
        self.app = app
        self.client = self.app.test_client
        database_path = os.getenv('TEST_DATABASE_URI')
        setup_db(self.app, database_path)
        self.movie_id = ''
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
            # Add a movie
            self.movie = Movie(
                title='The Hatchet',
                release_date=date(2020, 12, 11)
            )
            self.movie.insert()
            self.movie_id = self.movie.id

    def tearDown(self):
        with self.app.app_context():
            for actor in Actor.query.all():
                actor.delete()
            self.db.session.query(Movie).delete()
            self.db.session.commit()

    def test_get_movies_with_assistant_token(self):
        release_date = date(2020, 12, 11)
        movie = {
            'title': 'The Hatchet',
            'release_date': release_date.isoformat()
        }

        response = self.client().get(
            '/api/v1/movies?page=1',
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movies'][0]['title'], movie['title'])
        self.assertEqual(data['total-movies'], 1)

    def test_get_movies_with_director_token(self):
        release_date = date(2020, 12, 11)
        movie = {
            'title': 'The Hatchet',
            'release_date': release_date.isoformat()
        }

        response = self.client().get(
            '/api/v1/movies?page=1',
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movies'][0]['title'], movie['title'])
        self.assertEqual(data['total-movies'], 1)

    def test_get_movies_with_producer_token(self):
        release_date = date(2020, 12, 11)
        movie = {
            'title': 'The Hatchet',
            'release_date': release_date.isoformat()
        }

        response = self.client().get(
            '/api/v1/movies?page=1',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movies'][0]['title'], movie['title'])
        self.assertEqual(data['total-movies'], 1)

    def test_get_movies_with_invalid_page_number(self):
        page = 100  # This page doesn't exist
        response = self.client().get(
            f'/api/v1/movies?page={page}',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, mock_data.not_found_error_response)

    def test_get_movie_with_assistant_token(self):
        response = self.client().get(
            f'/api/v1/movies/{self.movie_id}',
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_movie_with_director_token(self):
        response = self.client().get(
            f'/api/v1/movies/{self.movie_id}',
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_movie_with_producer_token(self):
        response = self.client().get(
            f'/api/v1/movies/{self.movie_id}',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_movie_with_invalid_movie_id(self):
        movie_id = 0  # invalid movie ID

        response = self.client().get(
            f'/api/v1/movies/{movie_id}',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, mock_data.not_found_error_response)

    def test_add_movie_with_assistant_token(self):
        release_date = date(2020, 2, 9)
        movie = {
            'title': 'Above The Storm',
            'release_date': release_date.isoformat()
        }

        response = self.client().post(
                    '/api/v1/movies',
                    content_type='application/json',
                    data=json.dumps(movie),
                    headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data, mock_data.forbidden_error_response)

    def test_add_movie_with_director_token(self):
        release_date = date(2020, 2, 9)
        movie = {
            'title': 'Above The Storm',
            'release_date': release_date.isoformat()
        }

        response = self.client().post(
                    '/api/v1/movies',
                    content_type='application/json',
                    data=json.dumps(movie),
                    headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data, mock_data.forbidden_error_response)

    def test_add_movie_with_producer_token(self):
        release_date = date(2020, 2, 9)
        movie = {
            'title': 'Above The Storm',
            'release_date': release_date.isoformat()
        }

        response = self.client().post(
                    '/api/v1/movies',
                    content_type='application/json',
                    data=json.dumps(movie),
                    headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], movie['title'])

    def test_edit_movie_with_assistant_token(self):
        release_date = date(2020, 2, 9)
        movie = {
            'release_date': release_date.isoformat()
        }

        response = self.client().patch(
                        f'/api/v1/movies/{self.movie_id}',
                        content_type='application/json',
                        data=json.dumps(movie),
                        headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data, mock_data.forbidden_error_response)

    def test_edit_movie_with_director_token(self):
        release_date = date(2020, 2, 9)
        movie = {
            'release_date': release_date.isoformat()
        }

        response = self.client().patch(
                        f'/api/v1/movies/{self.movie_id}',
                        content_type='application/json',
                        data=json.dumps(movie),
                        headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['id'], self.movie_id)

    def test_edit_movie_with_producer_token(self):
        release_date = date(2020, 2, 9)
        movie = {
            'release_date': release_date.isoformat()
        }

        response = self.client().patch(
                        f'/api/v1/movies/{self.movie_id}',
                        content_type='application/json',
                        data=json.dumps(movie),
                        headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['id'], self.movie_id)

    def test_edit_movie_with_invalid_movie_id(self):
        movie_id = 0  # invalid movie ID
        release_date = date(2020, 2, 9)
        movie = {
            'release_date': release_date.isoformat()
        }

        response = self.client().patch(
                        f'/api/v1/movies/{movie_id}',
                        content_type='application/json',
                        data=json.dumps(movie),
                        headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data, mock_data.unprocessable_error_response)

    def test_delete_movie_with_assistant_token(self):

        response = self.client().delete(
            f'/api/v1/movies/{self.movie_id}',
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data, mock_data.forbidden_error_response)

    def test_delete_movie_with_director_token(self):

        response = self.client().delete(
            f'/api/v1/movies/{self.movie_id}',
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(response.data)
        print("Response in director delete ", response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data, mock_data.forbidden_error_response)

    def test_delete_movie_with_producer_token(self):

        response = self.client().delete(
            f'/api/v1/movies/{self.movie_id}',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('success')
        self.assertEqual(data['deleted'], self.movie_id)

    def test_delete_movie_with_invalid_id(self):
        movie_id = 0  # invalid movie_id

        response = self.client().delete(
            f'/api/v1/movies/{movie_id}',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)
        print("Response in delete invalid id", response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data, mock_data.unprocessable_error_response)

    def test_405_error_response(self):
        # there is no PATCH /api/v1/movies endpoint
        response = self.client().patch(
                        '/api/v1/movies',
                        headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data, mock_data.not_allowed_error_response)
