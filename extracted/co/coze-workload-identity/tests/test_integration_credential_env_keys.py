"""Tests for integration credential functionality using constants."""

import os
import unittest
from unittest.mock import Mock, patch, MagicMock

from coze_workload_identity import Client
from coze_workload_identity.exceptions import ConfigurationError, TokenRetrievalError
from coze_workload_identity.env_keys import *


class TestIntegrationCredentialConstants(unittest.TestCase):
    """Test cases for get_integration_credential method using constants."""

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
        COZE_WORKLOAD_IDENTITY_CLIENT_ID: 'test_client_id',
        COZE_WORKLOAD_IDENTITY_CLIENT_SECRET: 'test_client_secret',
        COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT: 'https://auth.example.com/token',
        COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT: 'https://auth.example.com/access-token',
        COZE_OUTBOUND_AUTH_ENDPOINT: 'https://auth.example.com/integration-credential'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_integration_credential_success_with_constants(self, mock_post):
        """Test successful integration credential retrieval using constants."""
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
        COZE_WORKLOAD_IDENTITY_CLIENT_ID: 'test_client_id',
        COZE_WORKLOAD_IDENTITY_CLIENT_SECRET: 'test_client_secret',
        COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT: 'https://auth.example.com/token',
        COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT: 'https://auth.example.com/access-token'
        # Note: COZE_OUTBOUND_AUTH_ENDPOINT is missing
    })
    def test_get_integration_credential_missing_endpoint_with_constants(self):
        """Test that ConfigurationError is raised when endpoint is missing using constants."""
        client = Client()

        with self.assertRaises(ConfigurationError) as context:
            client.get_integration_credential('test_integration')

        self.assertIn(COZE_OUTBOUND_AUTH_ENDPOINT, str(context.exception))
        client.close()

    @patch.dict(os.environ, {
        COZE_WORKLOAD_IDENTITY_CLIENT_ID: 'test_client_id',
        COZE_WORKLOAD_IDENTITY_CLIENT_SECRET: 'test_client_secret',
        COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT: 'https://auth.example.com/token',
        COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT: 'https://auth.example.com/access-token',
        COZE_OUTBOUND_AUTH_ENDPOINT: 'https://auth.example.com/integration-credential'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_integration_credential_with_lane_constants(self, mock_post):
        """Test that lane headers are properly added using constants."""
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

        # Test with BOE lane
        os.environ[COZE_SERVER_ENV] = 'boe_test_lane'

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

    def test_constants_values(self):
        """Test that constants have the expected values."""
        self.assertEqual(COZE_WORKLOAD_IDENTITY_CLIENT_ID, "COZE_WORKLOAD_IDENTITY_CLIENT_ID")
        self.assertEqual(COZE_WORKLOAD_IDENTITY_CLIENT_SECRET, "COZE_WORKLOAD_IDENTITY_CLIENT_SECRET")
        self.assertEqual(COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT, "COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT")
        self.assertEqual(COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT, "COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT")
        self.assertEqual(COZE_OUTBOUND_AUTH_ENDPOINT, "COZE_OUTBOUND_AUTH_ENDPOINT")
        self.assertEqual(COZE_SERVER_ENV, "COZE_SERVER_ENV")
        self.assertEqual(DEFAULT_COZE_SERVER_ENV, "NONE")


if __name__ == '__main__':
    unittest.main()