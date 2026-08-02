"""Tests for the Workload Identity Client."""

import os
import time
import unittest
from unittest.mock import Mock, patch, MagicMock
import requests

from coze_workload_identity import Client
from coze_workload_identity.exceptions import ConfigurationError, TokenRetrievalError, TokenExchangeError


class TestClient(unittest.TestCase):
    """Test cases for Client class."""

    def setUp(self):
        """Set up test environment."""
        self.env_vars = {
            'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
            'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
            'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
            'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
        }

        # Clear the global cache before each test to ensure fresh state
        from coze_workload_identity.client import _global_token_cache, _global_cache_lock
        with _global_cache_lock:
            if _global_token_cache is not None:
                _global_token_cache._cache.clear()

    def tearDown(self):
        """Clean up test environment."""
        # Remove any environment variables we set
        for var in self.env_vars:
            if var in os.environ:
                del os.environ[var]

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
    })
    def test_client_initialization_success(self):
        """Test successful client initialization."""
        client = Client()
        self.assertIsNotNone(client)
        client.close()

    def test_client_initialization_missing_env_vars(self):
        """Test client initialization with missing environment variables."""
        with self.assertRaises(ConfigurationError):
            Client()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_access_token_success(self, mock_post):
        """Test successful access token retrieval."""
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

        # Set up mock to return different responses for different calls
        mock_post.side_effect = [id_token_response, access_token_response]

        client = Client()
        token = client.get_access_token()

        self.assertEqual(token, 'test_access_token')
        self.assertEqual(mock_post.call_count, 2)
        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_access_token_id_token_failure(self, mock_post):
        """Test access token retrieval when ID token request fails."""
        mock_post.side_effect = requests.exceptions.RequestException("Network error")

        client = Client()
        with self.assertRaises(TokenRetrievalError):
            client.get_access_token()
        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_get_access_token_exchange_failure(self, mock_post):
        """Test access token retrieval when token exchange fails."""
        # Mock successful ID token response
        id_token_response = Mock()
        id_token_response.json.return_value = {
            'access_token': 'test_id_token',
            'expires_in': 3600
        }
        id_token_response.raise_for_status.return_value = None

        # Mock failed access token response
        access_token_response = Mock()
        access_token_response.json.return_value = {
            'error': 'invalid_token',
            'error_description': 'Invalid subject token'
        }
        access_token_response.raise_for_status.return_value = None

        mock_post.side_effect = [id_token_response, access_token_response]

        client = Client()
        with self.assertRaises(TokenRetrievalError):
            client.get_access_token()
        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_access_token_caching(self, mock_post):
        """Test that only access tokens are cached, ID tokens are always fetched fresh."""
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

        # First call should make HTTP requests (ID token + Access token)
        token1 = client.get_access_token()
        self.assertEqual(token1, 'test_access_token')
        self.assertEqual(mock_post.call_count, 2)

        # Second call should use cached access token (no additional HTTP calls)
        token2 = client.get_access_token()
        self.assertEqual(token2, 'test_access_token')
        self.assertEqual(mock_post.call_count, 2)  # No additional HTTP calls

        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_id_token_not_cached(self, mock_post):
        """Test that ID tokens are always fetched fresh (not cached)."""
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

        # First call
        token1 = client.get_access_token()
        self.assertEqual(token1, 'test_access_token')
        self.assertEqual(mock_post.call_count, 2)  # ID token + Access token

        # Second call should use cached access token (no HTTP calls)
        token2 = client.get_access_token()
        self.assertEqual(token2, 'test_access_token')
        self.assertEqual(mock_post.call_count, 2)  # No additional HTTP calls (access token cached)

        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
    })
    @patch('coze_workload_identity.client.requests.Session.post')
    def test_access_token_expiration_fresh_tokens(self, mock_post):
        """Test that expired access tokens trigger fresh ID token and access token fetch."""
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
            'expires_in': 1  # 1 second expiration
        }
        access_token_response.raise_for_status.return_value = None

        mock_post.side_effect = [id_token_response, access_token_response]

        client = Client()

        # First call
        token1 = client.get_access_token()
        self.assertEqual(token1, 'test_access_token')
        self.assertEqual(mock_post.call_count, 2)

        # Wait for access token to expire (with 1 minute buffer)
        time.sleep(2)

        # Reset mock for new responses
        mock_post.reset_mock()
        mock_post.side_effect = [id_token_response, access_token_response]

        # Second call should fetch fresh ID token and access token
        token2 = client.get_access_token()
        self.assertEqual(token2, 'test_access_token')
        self.assertEqual(mock_post.call_count, 2)  # Fresh ID token + Access token

        client.close()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://auth.example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://auth.example.com/access-token'
    })
    def test_context_manager(self):
        """Test that client works as a context manager."""
        with Client() as client:
            self.assertIsNotNone(client)


class TestTokenCache(unittest.TestCase):
    """Test cases for TokenCache class."""

    def setUp(self):
        """Set up test environment."""
        from coze_workload_identity.client import TokenCache
        self.cache = TokenCache()

    def test_cache_set_and_get(self):
        """Test basic cache set and get operations."""
        self.cache.set('test_key', 'test_token', 3600)
        token = self.cache.get('test_key')
        self.assertEqual(token, 'test_token')

    def test_cache_expiration(self):
        """Test that expired tokens are not returned."""
        self.cache.set('test_key', 'test_token', 1)  # 1 second expiration
        time.sleep(2)
        token = self.cache.get('test_key')
        self.assertIsNone(token)

    def test_cache_nonexistent_key(self):
        """Test that nonexistent keys return None."""
        token = self.cache.get('nonexistent_key')
        self.assertIsNone(token)

    def test_cache_thread_safety(self):
        """Test that cache operations are thread-safe."""
        import threading

        def set_token(cache, key, token, expires_in):
            cache.set(key, token, expires_in)

        def get_token(cache, key):
            return cache.get(key)

        threads = []
        for i in range(10):
            t = threading.Thread(target=set_token, args=(self.cache, f'key_{i}', f'token_{i}', 3600))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Verify all tokens were set correctly
        for i in range(10):
            token = self.cache.get(f'key_{i}')
            self.assertEqual(token, f'token_{i}')


class TestGlobalTokenCache(unittest.TestCase):
    """Test cases for global process-level token cache."""

    def setUp(self):
        """Set up test environment."""
        # Clear the global cache before each test
        from coze_workload_identity.client import _global_token_cache, _global_cache_lock
        with _global_cache_lock:
            if _global_token_cache is not None:
                _global_token_cache._cache.clear()

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://example.com/access_token'
    })
    def test_global_cache_shared_across_clients(self):
        """Test that global cache is shared across multiple Client instances."""
        from coze_workload_identity.client import Client

        # Create first client and cache a token
        client1 = Client()
        client1._token_cache.set('shared_key', 'shared_token', 3600)

        # Create second client and verify it can access the same cache
        client2 = Client()
        token = client2._token_cache.get('shared_key')

        self.assertEqual(token, 'shared_token')

        # Verify both clients use the same cache instance
        self.assertIs(client1._token_cache, client2._token_cache)

    @patch.dict(os.environ, {
        'COZE_WORKLOAD_IDENTITY_CLIENT_ID': 'test_client_id',
        'COZE_WORKLOAD_IDENTITY_CLIENT_SECRET': 'test_client_secret',
        'COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT': 'https://example.com/token',
        'COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT': 'https://example.com/access_token'
    })
    def test_global_cache_thread_safety(self):
        """Test that global cache is thread-safe with multiple clients."""
        import threading
        from coze_workload_identity.client import Client

        clients = [Client() for _ in range(5)]
        results = []

        def cache_operation(client, key, token):
            client._token_cache.set(key, token, 3600)
            results.append(client._token_cache.get(key))

        threads = []
        for i, client in enumerate(clients):
            t = threading.Thread(target=cache_operation, args=(client, f'key_{i}', f'token_{i}'))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Verify all operations completed successfully
        self.assertEqual(len(results), 5)
        for i, result in enumerate(results):
            self.assertEqual(result, f'token_{i}')

    def test_global_cache_singleton_pattern(self):
        """Test that get_global_token_cache returns the same instance."""
        from coze_workload_identity.client import get_global_token_cache

        cache1 = get_global_token_cache()
        cache2 = get_global_token_cache()

        self.assertIs(cache1, cache2)


if __name__ == '__main__':
    unittest.main()