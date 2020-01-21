import os
import json
import unittest
from flask_sqlalchemy import SQLAlchemy

from app import app
from app.models import setup_db, Actor, Movie
from tests import mock_data
from .auth_setup import get_token

assistant_token = get_token('assistant')
director_token = get_token('director')
producer_token = get_token('producer')


class ActorsTestCase(unittest.TestCase):
    """This class represents the Actors test case """
    def setUp(self):
        """Define test variables and initialize app"""
        self.app = app
        self.client = self.app.test_client
        database_path = os.getenv('TEST_DATABASE_URI')
        setup_db(self.app, database_path)
        self.actor_id = ''
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
            # Add an actor
            self.actor = Actor(
                name="Mugerwa Fred",
                dob='1996-05-07',
                gender="male")
            self.actor.insert()
            self.actor_id = self.actor.id

    def tearDown(self):
        with self.app.app_context():
            for movie in Movie.query.all():
                movie.delete()
            self.db.session.query(Actor).delete()
            self.db.session.commit()

    def test_get_actors_with_assistant_token(self):
        response = self.client().get(
            '/api/v1/actors',
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actors'][0].keys(), mock_data.actor.keys())
        self.assertEqual(data['total-actors'], 1)

    def test_get_actors_with_director_token(self):
        response = self.client().get(
            '/api/v1/actors',
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actors'][0].keys(), mock_data.actor.keys())
        self.assertEqual(data['total-actors'], 1)

    def test_get_actors_with_producer_token(self):
        response = self.client().get(
            '/api/v1/actors',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actors'][0].keys(), mock_data.actor.keys())
        self.assertEqual(data['total-actors'], 1)

    def test_get_actors_with_invalid_page_number(self):
        page = 100  # This page doesn't exist
        response = self.client().get(
            f'/api/v1/actors?page={page}',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, mock_data.not_found_error_response)

    def test_get_actor_with_assistant_token(self):
        actor = Actor.query.get(self.actor_id)

        response = self.client().get(
            f'/api/v1/actors/{self.actor_id}',
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], actor.name)
        self.assertEqual(data['actor']['age'], actor.get_age())
        self.assertEqual(data['actor']['gender'], actor.gender)

    def test_get_actor_with_director_token(self):
        actor = Actor.query.get(self.actor_id)

        response = self.client().get(
            f'/api/v1/actors/{self.actor_id}',
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], actor.name)
        self.assertEqual(data['actor']['age'], actor.get_age())
        self.assertEqual(data['actor']['gender'], actor.gender)

    def test_get_actor_with_producer_token(self):
        actor = Actor.query.get(self.actor_id)

        response = self.client().get(
            f'/api/v1/actors/{self.actor_id}',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], actor.name)
        self.assertEqual(data['actor']['age'], actor.get_age())
        self.assertEqual(data['actor']['gender'], actor.gender)

    def test_get_actor_with_invalid_actor_id(self):
        actor_id = 0  # This actor ID doesn't exist
        response = self.client().get(
            f'/api/v1/actors/{actor_id}',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, mock_data.not_found_error_response)

    def test_add_actor_with_assistant_token(self):
        actor = {
                'name': 'Jane Vanfon',
                'dob': '1999-01-01',
                'gender': 'female'
            }

        response = self.client().post(
            '/api/v1/actors',
            content_type='application/json',
            data=json.dumps(actor),
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data, mock_data.forbidden_error_response)

    def test_add_actor_with_director_token(self):
        actor = {
                'name': 'Jane Vanfon',
                'dob': '1999-01-01',
                'gender': 'female'
            }

        response = self.client().post(
            '/api/v1/actors',
            content_type='application/json',
            data=json.dumps(actor),
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], actor['name'])
        self.assertIsInstance(data['actor']['age'], int)
        self.assertEqual(data['actor']['gender'], actor['gender'])

    def test_add_actor_with_producer_token(self):
        actor = {
                'name': 'Jane Vanfon',
                'dob': '1999-01-01',
                'gender': 'female'
            }

        response = self.client().post(
            '/api/v1/actors',
            content_type='application/json',
            data=json.dumps(actor),
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], actor['name'])
        self.assertIsInstance(data['actor']['age'], int)
        self.assertEqual(data['actor']['gender'], actor['gender'])

    def test_edit_actor_with_assistant_token(self):
        actor = {'name': 'James Peters'}

        response = self.client().patch(
            f'/api/v1/actors/{self.actor_id}',
            content_type='application/json',
            data=json.dumps(actor),
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data, mock_data.forbidden_error_response)

    def test_edit_actor_with_director_token(self):
        actor = {'name': 'James Peters'}
        expected_actor = Actor.query.get(self.actor_id)

        response = self.client().patch(
            f'/api/v1/actors/{self.actor_id}',
            content_type='application/json',
            data=json.dumps(actor),
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], expected_actor.name)
        self.assertEqual(data['actor']['age'], expected_actor.get_age())
        self.assertEqual(data['actor']['gender'], expected_actor.gender)

    def test_edit_actor_with_producer_token(self):
        actor = {'name': 'James Peters'}
        expected_actor = Actor.query.get(self.actor_id)

        response = self.client().patch(
            f'/api/v1/actors/{self.actor_id}',
            content_type='application/json',
            data=json.dumps(actor),
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], expected_actor.name)
        self.assertEqual(data['actor']['age'], expected_actor.get_age())
        self.assertEqual(data['actor']['gender'], expected_actor.gender)

    def test_edit_actor_with_invalid_actor_id_in_request(self):
        actor = {'name': 'James Peters'}
        actor_id = 0  # This actor ID doesn't exist

        response = self.client().patch(
            f'/api/v1/actors/{actor_id}',
            content_type='application/json',
            data=json.dumps(actor),
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data, mock_data.unprocessable_error_response)

    def test_delete_actor_with_assistant_token(self):

        response = self.client().delete(
            f'/api/v1/actors/{self.actor_id}',
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data, mock_data.forbidden_error_response)

    def test_delete_actor_with_director_token(self):

        response = self.client().delete(
            f'/api/v1/actors/{self.actor_id}',
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], self.actor_id)

    def test_delete_actor_with_producer_token(self):

        response = self.client().delete(
            f'/api/v1/actors/{self.actor_id}',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], self.actor_id)

    def test_delete_actor_with_invalid_actor_id(self):
        actor_id = 0  # This actor ID doesn't exist

        response = self.client().delete(
            f'/api/v1/actors/{actor_id}',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data, mock_data.unprocessable_error_response)
