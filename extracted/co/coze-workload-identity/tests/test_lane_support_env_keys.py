"""Tests for lane support functionality using constants."""

import os
import unittest
from unittest.mock import Mock, patch, MagicMock

from coze_workload_identity import Client
from coze_workload_identity.exceptions import ConfigurationError
from coze_workload_identity.env_keys import *


class TestLaneSupportConstants(unittest.TestCase):
    """Test cases for lane support functionality using constants."""

    def setUp(self):
        """Set up test environment."""
        self.base_env_vars = {
            COZE_WORKLOAD_IDENTITY_CLIENT_ID: 'test_client_id',
            COZE_WORKLOAD_IDENTITY_CLIENT_SECRET: 'test_client_secret',
            COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT: 'https://auth.example.com/token',
            COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT: 'https://auth.example.com/access-token'
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

    @patch.dict(os.environ, {
        COZE_WORKLOAD_IDENTITY_CLIENT_ID: 'test_client_id',
        COZE_WORKLOAD_IDENTITY_CLIENT_SECRET: 'test_client_secret',
        COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT: 'https://auth.example.com/token',
        COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT: 'https://auth.example.com/access-token'
    })
    def test_default_lane_none_with_constants(self):
        """Test that default lane is NONE when COZE_SERVER_ENV is not set using constants."""
        client = Client()
        self.assertEqual(client._lane_env, DEFAULT_COZE_SERVER_ENV)
        client.close()

    @patch.dict(os.environ, {
        COZE_WORKLOAD_IDENTITY_CLIENT_ID: 'test_client_id',
        COZE_WORKLOAD_IDENTITY_CLIENT_SECRET: 'test_client_secret',
        COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT: 'https://auth.example.com/token',
        COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT: 'https://auth.example.com/access-token',
        COZE_SERVER_ENV: 'NONE'
    })
    def test_explicit_lane_none_with_constants(self):
        """Test that lane NONE is handled correctly using constants."""
        client = Client()
        self.assertEqual(client._lane_env, 'NONE')
        client.close()

    @patch.dict(os.environ, {
        COZE_WORKLOAD_IDENTITY_CLIENT_ID: 'test_client_id',
        COZE_WORKLOAD_IDENTITY_CLIENT_SECRET: 'test_client_secret',
        COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT: 'https://auth.example.com/token',
        COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT: 'https://auth.example.com/access-token',
        COZE_SERVER_ENV: 'boe_test_lane'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_boe_lane_headers_with_constants(self, mock_post):
        """Test that boe lane adds correct headers using constants."""
        # Mock responses
        id_token_response = Mock()
        id_token_response.json.return_value = {
            'access_token': 'test_id_token',
            'expires_in': 3600
        }
        id_token_response.raise_for_status.return_value = None

        access_token_response = Mock()
        access_token_response.json.return_value = {
            'access_token': 'test_access_token',
            'expires_in': 3600
        }
        access_token_response.raise_for_status.return_value = None

        mock_post.side_effect = [id_token_response, access_token_response]

        client = Client()
        client.get_access_token()

        # Check that both requests were made with correct headers
        self.assertEqual(mock_post.call_count, 2)

        # Check ID token request headers
        id_token_call = mock_post.call_args_list[0]
        headers = id_token_call[1]['headers']

        self.assertEqual(headers['x-tt-env'], 'boe_test_lane')
        self.assertNotIn('x-use-ppe', headers)  # boe lanes shouldn't have x-use-ppe

        # Check access token request headers
        access_token_call = mock_post.call_args_list[1]
        headers = access_token_call[1]['headers']

        self.assertEqual(headers['x-tt-env'], 'boe_test_lane')
        self.assertNotIn('x-use-ppe', headers)  # boe lanes shouldn't have x-use-ppe

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
        self.assertEqual(COZE_AUTH_OIDC_DISCOVERY_URL, "COZE_AUTH_OIDC_DISCOVERY_URL")
        self.assertEqual(COZE_AUTH_OIDC_CLIENT_ID, "COZE_AUTH_OIDC_CLIENT_ID")
        self.assertEqual(COZE_AUTH_OIDC_CLIENT_SECRET, "COZE_AUTH_OIDC_CLIENT_SECRET")
        self.assertEqual(COZE_AUTH_SESSION_SECRET, "COZE_AUTH_SESSION_SECRET")
        self.assertEqual(COZE_LOOP_API_TOKEN, "COZE_LOOP_API_TOKEN")
        self.assertEqual(COZE_PROJECT_ID, "COZE_PROJECT_ID")
        self.assertEqual(COZE_PROJECT_SPACE_ID, "COZE_PROJECT_SPACE_ID")
        self.assertEqual(COZE_PROJECT_ENV, "COZE_PROJECT_ENV")
        self.assertEqual(COZE_INTEGRATION_BASE_URL, "COZE_INTEGRATION_BASE_URL")


if __name__ == '__main__':
    unittest.main()