"""Tests for project environment variables functionality."""

import os
import unittest
from unittest.mock import Mock, patch, MagicMock

from coze_workload_identity import Client
from coze_workload_identity.exceptions import ConfigurationError, TokenRetrievalError
from coze_workload_identity.env_keys import *
from coze_workload_identity.models import ProjectEnvVar, ProjectEnvVars


class TestProjectEnvVars(unittest.TestCase):
    """Test cases for get_project_env_vars method."""

    def setUp(self):
        """Set up test environment."""
        self.base_env_vars = {
            COZE_WORKLOAD_IDENTITY_CLIENT_ID: 'test_client_id',
            COZE_WORKLOAD_IDENTITY_CLIENT_SECRET: 'test_client_secret',
            COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT: 'https://auth.example.com/token',
            COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT: 'https://auth.example.com/access-token',
            COZE_OUTBOUND_AUTH_ENDPOINT: 'https://auth.example.com/integration-credential'
        }

    def tearDown(self):
        """Clean up test environment."""
        # Remove any environment variables we set
        for var in [COZE_SERVER_ENV] + list(self.base_env_vars.keys()):
            if var in os.environ:
                del os.environ[var]

    def _setup_token_mocks(self):
        """Helper method to set up token response mocks."""
        # Mock ID token response
        id_token_response = Mock()
        id_token_response.json.return_value = {
            'access_token': 'test_id_token',
            'expires_in': 3600
        }
        id_token_response.raise_for_status.return_value = None

        # Mock access token response
        access_token_response = Mock()
        access_token_response.json.return_value = {
            'access_token': 'test_access_token',
            'expires_in': 3600
        }
        access_token_response.raise_for_status.return_value = None

        return id_token_response, access_token_response

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential'
    })
    @patch('coze_workload_identity.client.requests.Session.get')
    def test_get_project_env_vars_success(self, mock_get):
        """Test successful project environment variables retrieval."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock project environment variables response
        env_vars_response = Mock()
        env_vars_response.status_code = 200
        env_vars_response.json.return_value = {
            'code': 0,
            'msg': 'success',
            'data': {
                'secrets': [
                    {'key': 'DATABASE_URL', 'value': 'postgresql://localhost:5432/mydb'},
                    {'key': 'API_KEY', 'value': 'secret_api_key_123'},
                    {'key': 'DEBUG_MODE', 'value': 'true'}
                ]
            }
        }

        # Set up mock to return different responses for different calls
        with patch('coze_workload_identity.client.requests.Session.post') as mock_post:
            mock_post.side_effect = [id_token_response, access_token_response]
            mock_get.return_value = env_vars_response

            client = Client()
            project_env_vars = client.get_project_env_vars()

            # Verify the result
            self.assertIsInstance(project_env_vars, ProjectEnvVars)
            self.assertEqual(len(project_env_vars), 3)

            # Check individual variables
            self.assertEqual(project_env_vars.get('DATABASE_URL'), 'postgresql://localhost:5432/mydb')
            self.assertEqual(project_env_vars.get('API_KEY'), 'secret_api_key_123')
            self.assertEqual(project_env_vars.get('DEBUG_MODE'), 'true')
            self.assertIsNone(project_env_vars.get('NONEXISTENT_KEY'))

            # Verify the GET request was made correctly
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            self.assertEqual(call_args[0][0], 'https://auth.example.com/integration-credential/env')
            self.assertNotIn('params', call_args[1])  # No params should be passed

            # Verify headers
            headers = call_args[1]['headers']
            self.assertEqual(headers['Authorization'], 'Bearer test_access_token')
            self.assertEqual(headers['Content-Type'], 'application/json')

            client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
        # Note: COZE_OUTBOUND_AUTH_ENDPOINT is missing
    })
    def test_get_project_env_vars_missing_endpoint(self):
        """Test that ConfigurationError is raised when endpoint is missing."""
        client = Client()

        with self.assertRaises(ConfigurationError) as context:
            client.get_project_env_vars()

        self.assertIn("COZE_OUTBOUND_AUTH_ENDPOINT", str(context.exception))
        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential'
    })
    @patch('coze_workload_identity.client.requests.Session.get')
    def test_get_project_env_vars_4xx_error(self, mock_get):
        """Test handling of 4xx client errors."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock 4xx error response
        env_vars_response = Mock()
        env_vars_response.status_code = 400
        env_vars_response.json.return_value = {
            'code': 400,
            'msg': 'Bad Request: Invalid project ID'
        }

        with patch('coze_workload_identity.client.requests.Session.post') as mock_post:
            mock_post.side_effect = [id_token_response, access_token_response]
            mock_get.return_value = env_vars_response

            client = Client()

            with self.assertRaises(Exception) as context:
                client.get_project_env_vars()

            self.assertIn("Client error (400)", str(context.exception))
            self.assertIn("Bad Request: Invalid project ID", str(context.exception))

            client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential'
    })
    @patch('coze_workload_identity.client.requests.Session.get')
    def test_get_project_env_vars_5xx_error(self, mock_get):
        """Test handling of 5xx server errors."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock 5xx error response
        env_vars_response = Mock()
        env_vars_response.status_code = 500
        env_vars_response.json.return_value = {
            'code': 500,
            'msg': 'Internal Server Error'
        }

        with patch('coze_workload_identity.client.requests.Session.post') as mock_post:
            mock_post.side_effect = [id_token_response, access_token_response]
            mock_get.return_value = env_vars_response

            client = Client()

            with self.assertRaises(Exception) as context:
                client.get_project_env_vars()

            self.assertIn("Server error (500)", str(context.exception))
            self.assertIn("Internal Server Error", str(context.exception))

            client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential'
    })
    @patch('coze_workload_identity.client.requests.Session.get')
    def test_get_project_env_vars_api_error_code(self, mock_get):
        """Test handling of API error codes (non-zero code field)."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock API error response (HTTP 200 but code != 0)
        env_vars_response = Mock()
        env_vars_response.status_code = 200
        env_vars_response.json.return_value = {
            'code': 1002,
            'msg': 'Project not found',
            'data': None
        }

        with patch('coze_workload_identity.client.requests.Session.post') as mock_post:
            mock_post.side_effect = [id_token_response, access_token_response]
            mock_get.return_value = env_vars_response

            client = Client()

            with self.assertRaises(Exception) as context:
                client.get_project_env_vars()

            self.assertIn("Project environment variables API error: code=1002, msg=Project not found", str(context.exception))

            client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential'
    })
    @patch('coze_workload_identity.client.requests.Session.get')
    def test_get_project_env_vars_invalid_response_format(self, mock_get):
        """Test handling of invalid response formats."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Test cases for different invalid response formats
        test_cases = [
            # Missing data field
            {
                'code': 0,
                'msg': 'success'
            },
            # Invalid data field type
            {
                'code': 0,
                'msg': 'success',
                'data': 'invalid'
            },
            # Missing secrets field
            {
                'code': 0,
                'msg': 'success',
                'data': {}
            },
            # Invalid secrets type
            {
                'code': 0,
                'msg': 'success',
                'data': {
                    'secrets': 'invalid'
                }
            },
            # Invalid secret format (missing key)
            {
                'code': 0,
                'msg': 'success',
                'data': {
                    'secrets': [
                        {'value': 'missing_key'}
                    ]
                }
            },
            # Invalid secret format (wrong value type)
            {
                'code': 0,
                'msg': 'success',
                'data': {
                    'secrets': [
                        {'key': 'TEST_KEY', 'value': 12345}  # Should be string
                    ]
                }
            }
        ]

        for i, invalid_response in enumerate(test_cases):
            with self.subTest(response=invalid_response):
                # Reset mock for each test case
                mock_get.reset_mock()

                env_vars_response = Mock()
                env_vars_response.status_code = 200
                env_vars_response.json.return_value = invalid_response

                with patch('coze_workload_identity.client.requests.Session.post') as mock_post:
                    mock_post.side_effect = [id_token_response, access_token_response]
                    mock_get.return_value = env_vars_response

                    client = Client()

                    with self.assertRaises(Exception) as context:
                        client.get_project_env_vars()

                    # Verify that an exception was raised
                    self.assertTrue(len(str(context.exception)) > 0)

                    client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential',
        'COZE_SERVER_ENV': 'boe_test_lane'
    })
    @patch('coze_workload_identity.client.requests.Session.get')
    def test_get_project_env_vars_with_boe_lane(self, mock_get):
        """Test that BOE lane headers are properly added to project env vars requests."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock project environment variables response
        env_vars_response = Mock()
        env_vars_response.status_code = 200
        env_vars_response.json.return_value = {
            'code': 0,
            'msg': 'success',
            'data': {
                'secrets': [
                    {'key': 'TEST_KEY', 'value': 'test_value'}
                ]
            }
        }

        with patch('coze_workload_identity.client.requests.Session.post') as mock_post:
            mock_post.side_effect = [id_token_response, access_token_response]
            mock_get.return_value = env_vars_response

            client = Client()
            project_env_vars = client.get_project_env_vars()

            # Verify the GET request has BOE lane headers
            call_args = mock_get.call_args
            headers = call_args[1]['headers']

            self.assertEqual(headers['x-tt-env'], 'boe_test_lane')
            self.assertNotIn('x-use-ppe', headers)  # BOE lanes don't have x-use-ppe

            client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential',
        'COZE_SERVER_ENV': 'ppe_production_lane'
    })
    @patch('coze_workload_identity.client.requests.Session.get')
    def test_get_project_env_vars_with_ppe_lane(self, mock_get):
        """Test that PPE lane headers are properly added to project env vars requests."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock project environment variables response
        env_vars_response = Mock()
        env_vars_response.status_code = 200
        env_vars_response.json.return_value = {
            'code': 0,
            'msg': 'success',
            'data': {
                'secrets': [
                    {'key': 'TEST_KEY', 'value': 'test_value'}
                ]
            }
        }

        with patch('coze_workload_identity.client.requests.Session.post') as mock_post:
            mock_post.side_effect = [id_token_response, access_token_response]
            mock_get.return_value = env_vars_response

            client = Client()
            project_env_vars = client.get_project_env_vars()

            # Verify the GET request has PPE lane headers
            call_args = mock_get.call_args
            headers = call_args[1]['headers']

            self.assertEqual(headers['x-tt-env'], 'ppe_production_lane')
            self.assertEqual(headers['x-use-ppe'], '1')

            client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential'
    })
    @patch('coze_workload_identity.client.requests.Session.get')
    def test_get_project_env_vars_network_error(self, mock_get):
        """Test handling of network errors."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock network error for env vars request
        import requests
        def side_effect(*args, **kwargs):
            if args[0].endswith('/env'):
                raise requests.exceptions.ConnectionError("Network error")
            return Mock()

        with patch('coze_workload_identity.client.requests.Session.post') as mock_post:
            mock_post.side_effect = [id_token_response, access_token_response]
            mock_get.side_effect = side_effect

            client = Client()

            with self.assertRaises(Exception) as context:
                client.get_project_env_vars()

            self.assertIn("Failed to retrieve project environment variables", str(context.exception))
            self.assertIn("Network error", str(context.exception))

            client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential'
    })
    @patch('coze_workload_identity.client.requests.Session.get')
    def test_get_project_env_vars_empty_secrets(self, mock_get):
        """Test handling of empty secrets list."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock empty secrets response
        env_vars_response = Mock()
        env_vars_response.status_code = 200
        env_vars_response.json.return_value = {
            'code': 0,
            'msg': 'success',
            'data': {
                'secrets': []
            }
        }

        with patch('coze_workload_identity.client.requests.Session.post') as mock_post:
            mock_post.side_effect = [id_token_response, access_token_response]
            mock_get.return_value = env_vars_response

            client = Client()
            project_env_vars = client.get_project_env_vars()

            # Verify empty result
            self.assertIsInstance(project_env_vars, ProjectEnvVars)
            self.assertEqual(len(project_env_vars), 0)
            self.assertEqual(project_env_vars.vars, [])

            client.close()


if __name__ == '__main__':
    unittest.main()