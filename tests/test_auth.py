import json
import unittest

from app import app
from tests import mock_data


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = app
        self.client = self.app.test_client

    def test_get_actors_without_authorization_headers(self):

        response = self.client().get('/api/v1/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, mock_data.header_missing_response)

    def test_get_actors_with_bearer_missing_from_auth_headers(self):

        response = self.client().get(
            '/api/v1/actors',
            headers={'Authorization': f'{mock_data.casting_asst_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, mock_data.bearer_missing_response)

    def test_get_actors_with_token_missing_from_auth_headers(self):

        response = self.client().get(
            '/api/v1/actors',
            headers={'Authorization': 'Bearer '})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, mock_data.token_missing_response)

    def test_get_actors_with_invalid_auth_headers(self):
        invalid_header = {
            'Authorization': f'Bearer {mock_data.casting_asst_token} token'}

        response = self.client().get(
            '/api/v1/actors',
            headers=invalid_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, mock_data.invalid_auth_header_response)
