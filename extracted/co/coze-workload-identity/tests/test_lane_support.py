"""Tests for lane support functionality."""

import os
import unittest
from unittest.mock import Mock, patch, MagicMock

from coze_workload_identity import Client
from coze_workload_identity.exceptions import ConfigurationError


class TestLaneSupport(unittest.TestCase):
    """Test cases for lane support functionality."""

    def setUp(self):
        """Set up test environment."""
        self.base_env_vars = {
            'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
            'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
            'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
            'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
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
        for var in ['COZE_SERVER_ENV'] + list(self.base_env_vars.keys()):
            if var in os.environ:
                del os.environ[var]

        # Reset the global token cache to avoid cross-test leakage.
        from coze_workload_identity.client import _global_token_cache, _global_cache_lock
        with _global_cache_lock:
            if _global_token_cache is not None:
                _global_token_cache._cache.clear()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
    })
    def test_default_lane_none(self):
        """Test that default lane is NONE when COZE_SERVER_ENV is not set."""
        client = Client()
        self.assertEqual(client._lane_env, 'NONE')
        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_SERVER_ENV': 'NONE'
    })
    def test_explicit_lane_none(self):
        """Test that lane NONE is handled correctly."""
        client = Client()
        self.assertEqual(client._lane_env, 'NONE')
        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_SERVER_ENV': 'boe_test_lane'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_boe_lane_headers(self, mock_post):
        """Test that boe lane adds correct headers."""
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

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_SERVER_ENV': 'ppe_production_lane'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_ppe_lane_headers(self, mock_post):
        """Test that ppe lane adds correct headers."""
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

        self.assertEqual(headers['x-tt-env'], 'ppe_production_lane')
        self.assertEqual(headers['x-use-ppe'], '1')

        # Check access token request headers
        access_token_call = mock_post.call_args_list[1]
        headers = access_token_call[1]['headers']

        self.assertEqual(headers['x-tt-env'], 'ppe_production_lane')
        self.assertEqual(headers['x-use-ppe'], '1')

        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token',
        'COZE_SERVER_ENV': 'custom_lane'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_custom_lane_headers(self, mock_post):
        """Test that custom lane (not boe_/ppe_) adds only x-tt-env header."""
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

        self.assertEqual(headers['x-tt-env'], 'custom_lane')
        self.assertNotIn('x-use-ppe', headers)  # custom lanes shouldn't have x-use-ppe

        # Check access token request headers
        access_token_call = mock_post.call_args_list[1]
        headers = access_token_call[1]['headers']

        self.assertEqual(headers['x-tt-env'], 'custom_lane')
        self.assertNotIn('x-use-ppe', headers)  # custom lanes shouldn't have x-use-ppe

        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_no_lane_headers_when_none(self, mock_post):
        """Test that no lane headers are added when COZE_SERVER_ENV is NONE."""
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

        # Check that both requests were made without lane headers
        self.assertEqual(mock_post.call_count, 2)

        # Check ID token request headers
        id_token_call = mock_post.call_args_list[0]
        headers = id_token_call[1]['headers']

        self.assertNotIn('x-tt-env', headers)
        self.assertNotIn('x-use-ppe', headers)

        # Check access token request headers
        access_token_call = mock_post.call_args_list[1]
        headers = access_token_call[1]['headers']

        self.assertNotIn('x-tt-env', headers)
        self.assertNotIn('x-use-ppe', headers)

        client.close()


if __name__ == '__main__':
    unittest.main()