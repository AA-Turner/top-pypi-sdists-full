"""Tests for integration credential functionality."""

import os
import unittest
from unittest.mock import Mock, patch, MagicMock

from coze_workload_identity import Client
from coze_workload_identity.exceptions import ConfigurationError, TokenRetrievalError
from coze_workload_identity.env_keys import *


class TestIntegrationCredential(unittest.TestCase):
    """Test cases for get_integration_credential method."""

    def setUp(self):
        """Set up test environment."""
        self.base_env_vars = {
            COZE_WORKLOAD_IDENTITY_CLIENT_ID: 'test_client_id',
            COZE_WORKLOAD_IDENTITY_CLIENT_SECRET: 'test_client_secret',
            COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT: 'https://auth.example.com/token',
            COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT: 'https://auth.example.com/access-token',
            COZE_OUTBOUND_AUTH_ENDPOINT: 'https://auth.example.com/integration-credential'
        }

        # Clear the global token cache so each test makes real (mocked) HTTP
        # calls instead of returning a token left behind by a prior test.
        from coze_workload_identity.client import _global_token_cache, _global_cache_lock
        with _global_cache_lock:
            if _global_token_cache is not None:
                _global_token_cache._cache.clear()

    def tearDown(self):
        """Clean up test environment."""
        # Remove any environment variables we set
        for var in [COZE_SERVER_ENV] + list(self.base_env_vars.keys()):
            if var in os.environ:
                del os.environ[var]

        # Reset the global token cache to avoid cross-test leakage.
        from coze_workload_identity.client import _global_token_cache, _global_cache_lock
        with _global_cache_lock:
            if _global_token_cache is not None:
                _global_token_cache._cache.clear()

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
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_integration_credential_success(self, mock_post):
        """Test successful integration credential retrieval."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock integration credential response
        credential_response = Mock()
        credential_response.status_code = 200
        credential_response.json.return_value = {
            'code': 0,
            'msg': 'success',
            'data': {
                'credential': 'test_integration_credential_12345'
            }
        }

        # Set up mock to return different responses for different calls
        mock_post.side_effect = [id_token_response, access_token_response, credential_response]

        client = Client()
        credential = client.get_integration_credential('test_integration')

        self.assertEqual(credential, 'test_integration_credential_12345')
        self.assertEqual(mock_post.call_count, 3)  # ID token + access token + credential

        # Verify the third call (integration credential) has correct headers
        credential_call = mock_post.call_args_list[2]
        headers = credential_call[1]['headers']

        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertEqual(headers['Authorization'], 'Bearer test_access_token')

        # Verify the request data
        request_data = credential_call[1]['json']
        self.assertEqual(request_data['integration_name'], 'test_integration')

        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
        # Note: COZE_OUTBOUND_AUTH_ENDPOINT is missing
    })
    def test_get_integration_credential_missing_endpoint(self):
        """Test that ConfigurationError is raised when endpoint is missing."""
        client = Client()

        with self.assertRaises(ConfigurationError) as context:
            client.get_integration_credential('test_integration')

        self.assertIn("COZE_OUTBOUND_AUTH_ENDPOINT", str(context.exception))
        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_integration_credential_4xx_error(self, mock_post):
        """Test handling of 4xx client errors."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock 4xx error response
        credential_response = Mock()
        credential_response.status_code = 400
        credential_response.json.return_value = {
            'code': 400,
            'msg': 'Bad Request: Invalid integration name'
        }

        mock_post.side_effect = [id_token_response, access_token_response, credential_response]

        client = Client()

        with self.assertRaises(Exception) as context:
            client.get_integration_credential('invalid_integration')

        self.assertIn("Client error (400)", str(context.exception))
        self.assertIn("Bad Request: Invalid integration name", str(context.exception))

        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_integration_credential_5xx_error(self, mock_post):
        """Test handling of 5xx server errors."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock 5xx error response
        credential_response = Mock()
        credential_response.status_code = 500
        credential_response.json.return_value = {
            'code': 500,
            'msg': 'Internal Server Error'
        }

        mock_post.side_effect = [id_token_response, access_token_response, credential_response]

        client = Client()

        with self.assertRaises(Exception) as context:
            client.get_integration_credential('test_integration')

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
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_integration_credential_api_error_code(self, mock_post):
        """Test handling of API error codes (non-zero code field)."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock API error response (HTTP 200 but code != 0)
        credential_response = Mock()
        credential_response.status_code = 200
        credential_response.json.return_value = {
            'code': 1001,
            'msg': 'Integration not found',
            'data': None
        }

        mock_post.side_effect = [id_token_response, access_token_response, credential_response]

        client = Client()

        with self.assertRaises(Exception) as context:
            client.get_integration_credential('nonexistent_integration')

        self.assertIn("Integration credential API error: code=1001, msg=Integration not found", str(context.exception))

        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_integration_credential_invalid_response_format(self, mock_post):
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
            # Missing credential field
            {
                'code': 0,
                'msg': 'success',
                'data': {}
            },
            # Invalid credential type
            {
                'code': 0,
                'msg': 'success',
                'data': {
                    'credential': 12345  # Should be string
                }
            }
        ]

        for i, invalid_response in enumerate(test_cases):
            with self.subTest(response=invalid_response):
                # Reset mock for each test case
                mock_post.reset_mock()

                credential_response = Mock()
                credential_response.status_code = 200
                credential_response.json.return_value = invalid_response

                mock_post.side_effect = [id_token_response, access_token_response, credential_response]

                client = Client()

                with self.assertRaises(Exception) as context:
                    client.get_integration_credential('test_integration')

                # Verify that an exception was raised
                self.assertTrue(len(str(context.exception)) > 0)

                client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_integration_credential_with_lane_support(self, mock_post):
        """Test that lane headers are properly added to integration credential requests."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock integration credential response
        credential_response = Mock()
        credential_response.status_code = 200
        credential_response.json.return_value = {
            'code': 0,
            'msg': 'success',
            'data': {
                'credential': 'test_integration_credential'
            }
        }

        mock_post.side_effect = [id_token_response, access_token_response, credential_response]

        client = Client()
        credential = client.get_integration_credential('test_integration')

        self.assertEqual(credential, 'test_integration_credential')

        # Verify the integration credential call has no lane headers (NONE lane)
        credential_call = mock_post.call_args_list[2]
        headers = credential_call[1]['headers']

        self.assertNotIn('x-tt-env', headers)  # NONE lane doesn't add headers
        self.assertNotIn('x-use-ppe', headers)

        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_OUTBOUND_AUTH_ENDPOINT': 'https://auth.example.com/integration-credential',
        'COZE_SERVER_ENV': 'boe_test_lane'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_integration_credential_with_boe_lane(self, mock_post):
        """Test that BOE lane headers are properly added to integration credential requests."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock integration credential response
        credential_response = Mock()
        credential_response.status_code = 200
        credential_response.json.return_value = {
            'code': 0,
            'msg': 'success',
            'data': {
                'credential': 'test_integration_credential'
            }
        }

        mock_post.side_effect = [id_token_response, access_token_response, credential_response]

        client = Client()
        credential = client.get_integration_credential('test_integration')

        self.assertEqual(credential, 'test_integration_credential')

        # Verify the integration credential call has BOE lane headers
        credential_call = mock_post.call_args_list[2]
        headers = credential_call[1]['headers']

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
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_integration_credential_with_ppe_lane(self, mock_post):
        """Test that PPE lane headers are properly added to integration credential requests."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock integration credential response
        credential_response = Mock()
        credential_response.status_code = 200
        credential_response.json.return_value = {
            'code': 0,
            'msg': 'success',
            'data': {
                'credential': 'test_integration_credential'
            }
        }

        mock_post.side_effect = [id_token_response, access_token_response, credential_response]

        client = Client()
        credential = client.get_integration_credential('test_integration')

        self.assertEqual(credential, 'test_integration_credential')

        # Verify the integration credential call has PPE lane headers
        credential_call = mock_post.call_args_list[2]
        headers = credential_call[1]['headers']

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
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_integration_credential_network_error(self, mock_post):
        """Test handling of network errors."""
        # Set up token mocks
        id_token_response, access_token_response = self._setup_token_mocks()

        # Mock network error for credential request
        import requests
        def side_effect(*args, **kwargs):
            if mock_post.call_count == 3:  # Third call is the credential request
                raise requests.exceptions.ConnectionError("Network error")
            elif mock_post.call_count == 1:  # First call is ID token
                return id_token_response
            else:  # Second call is access token
                return access_token_response

        mock_post.side_effect = side_effect

        client = Client()

        with self.assertRaises(Exception) as context:
            client.get_integration_credential('test_integration')

        self.assertIn("Failed to retrieve integration credential", str(context.exception))
        self.assertIn("Network error", str(context.exception))

        client.close()


if __name__ == '__main__':
    unittest.main()