"""
Tests for authentication module
"""
import json
import unittest
from unittest import mock
import base64
from datetime import datetime
import uuid
from typing import Dict, List, Optional, Any

from paymentus_auth.auth import Auth, AuthConfig, TokenResponse, PIXEL_SCOPE_MAP, PixelType
from paymentus_auth.errors import ConfigurationError, TokenError, NetworkError


class MockResponse:
    """Mock for requests.Response"""
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception(f"HTTP Error: {self.status_code}")


class TestAuth(unittest.TestCase):
    """Test Authentication class"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_config = AuthConfig(
            base_url="https://api.example.com",
            pre_shared_key="test-key",
            tla="XYZ",
            scope=["xotp"]
        )

        self.mock_token_response = {
            "token": "test-token-12345",
            "exp": int(datetime.now().timestamp()) + 3600
        }

        # Create a patcher for requests.post
        self.post_patcher = mock.patch('requests.post')
        self.mock_post = self.post_patcher.start()

    def tearDown(self):
        """Tear down test fixtures"""
        self.post_patcher.stop()

    @mock.patch('jwt.encode')
    async def test_fetch_token(self, mock_jwt_encode):
        """Test token fetching works correctly"""
        # Set up mocks
        mock_jwt_encode.return_value = "mocked.jwt.token"
        self.mock_post.return_value = MockResponse(self.mock_token_response, 200)

        # Create auth client and fetch token
        auth_client = Auth(self.mock_config)
        token = await auth_client.fetch_token()

        # Assertions
        self.assertEqual(token, self.mock_token_response["token"])
        self.mock_post.assert_called_once_with(
            f"{self.mock_config.base_url}/api/token/{self.mock_config.tla}",
            json={"jwt": "mocked.jwt.token"},
            headers=mock.ANY,
            timeout=self.mock_config.timeout / 1000,
            verify=False
        )

    async def test_token_invalid_response(self):
        """Test handling of invalid token response"""
        # Set up mock to return invalid response (no token)
        self.mock_post.return_value = MockResponse({"exp": 123456}, 200)

        # Create auth client and attempt to fetch token
        auth_client = Auth(self.mock_config)
        with self.assertRaises(TokenError) as context:
            await auth_client.fetch_token()
        
        self.assertIn("Invalid token response", str(context.exception))

    async def test_network_error(self):
        """Test handling of network errors"""
        # Set up mock to raise an exception
        self.mock_post.side_effect = Exception("Network error")

        # Create auth client and attempt to fetch token
        auth_client = Auth(self.mock_config)
        with self.assertRaises(TokenError) as context:
            await auth_client.fetch_token()
        
        self.assertIn("Failed to fetch token", str(context.exception))

    def test_invalid_base_url(self):
        """Test validation of base_url"""
        config = AuthConfig(
            base_url="",
            pre_shared_key="test-key",
            tla="XYZ",
            scope=["xotp"]
        )
        
        with self.assertRaises(ConfigurationError) as context:
            Auth(config)
        
        self.assertIn("Invalid base_url", str(context.exception))

    def test_invalid_pre_shared_key(self):
        """Test validation of pre_shared_key"""
        config = AuthConfig(
            base_url="https://api.example.com",
            pre_shared_key="",
            tla="XYZ",
            scope=["xotp"]
        )
        
        with self.assertRaises(ConfigurationError) as context:
            Auth(config)
        
        self.assertIn("Invalid pre_shared_key", str(context.exception))

    def test_invalid_tla(self):
        """Test validation of tla"""
        config = AuthConfig(
            base_url="https://api.example.com",
            pre_shared_key="test-key",
            tla="",
            scope=["xotp"]
        )
        
        with self.assertRaises(ConfigurationError) as context:
            Auth(config)
        
        self.assertIn("Invalid tla", str(context.exception))

    def test_no_scope_or_pixels(self):
        """Test validation of empty scope and pixels"""
        config = AuthConfig(
            base_url="https://api.example.com",
            pre_shared_key="test-key",
            tla="XYZ",
            scope=[]
        )
        
        with self.assertRaises(ConfigurationError) as context:
            Auth(config)
        
        self.assertIn("At least one scope or pixel is required", str(context.exception))

    @mock.patch('jwt.encode')
    async def test_multiple_scopes(self, mock_jwt_encode):
        """Test handling of multiple scopes"""
        # Set up mocks
        mock_jwt_encode.return_value = "mocked.jwt.token"
        self.mock_post.return_value = MockResponse(self.mock_token_response, 200)

        # Create auth client with multiple scopes
        config = AuthConfig(
            base_url="https://api.example.com",
            pre_shared_key="test-key",
            tla="XYZ",
            scope=["xotp", "xotp:profile"]
        )
        
        auth_client = Auth(config)
        await auth_client.fetch_token()
        
        # Extract the payload passed to jwt.encode
        mock_jwt_encode.assert_called_once()
        payload = mock_jwt_encode.call_args[1]['payload']
        
        self.assertEqual(payload["requestedScope"], ["xotp", "xotp:profile"])

    @mock.patch('jwt.encode')
    async def test_user_login_in_payload(self, mock_jwt_encode):
        """Test inclusion of userLogin in JWT payload"""
        # Set up mocks
        mock_jwt_encode.return_value = "mocked.jwt.token"
        self.mock_post.return_value = MockResponse(self.mock_token_response, 200)

        # Create auth client with user_login
        config = AuthConfig(
            base_url="https://api.example.com",
            pre_shared_key="test-key",
            tla="XYZ",
            scope=["xotp"],
            user_login="test@example.com"
        )
        
        auth_client = Auth(config)
        await auth_client.fetch_token()
        
        # Extract the payload passed to jwt.encode
        mock_jwt_encode.assert_called_once()
        payload = mock_jwt_encode.call_args[1]['payload']
        
        self.assertEqual(payload["userLogin"], "test@example.com")

    @mock.patch('jwt.encode')
    async def test_pm_token_in_payload(self, mock_jwt_encode):
        """Test inclusion of pmToken in JWT payload"""
        # Set up mocks
        mock_jwt_encode.return_value = "mocked.jwt.token"
        self.mock_post.return_value = MockResponse(self.mock_token_response, 200)

        # Create auth client with pm_token
        config = AuthConfig(
            base_url="https://api.example.com",
            pre_shared_key="test-key",
            tla="XYZ",
            scope=["xotp"],
            pm_token=["token1", "token2"]
        )
        
        auth_client = Auth(config)
        await auth_client.fetch_token()
        
        # Extract the payload passed to jwt.encode
        mock_jwt_encode.assert_called_once()
        payload = mock_jwt_encode.call_args[1]['payload']
        
        self.assertEqual(payload["pmToken"], ["token1", "token2"])

    @mock.patch('jwt.encode')
    async def test_payments_data_in_payload(self, mock_jwt_encode):
        """Test inclusion of paymentsData in JWT payload"""
        # Set up mocks
        mock_jwt_encode.return_value = "mocked.jwt.token"
        self.mock_post.return_value = MockResponse(self.mock_token_response, 200)

        # Create auth client with payments_data
        config = AuthConfig(
            base_url="https://api.example.com",
            pre_shared_key="test-key",
            tla="XYZ",
            scope=["xotp"],
            payments_data=[{
                "accountNumber": "123456",
                "convFeeState": "NY",
                "convFeeCountry": "US"
            }]
        )
        
        auth_client = Auth(config)
        await auth_client.fetch_token()
        
        # Extract the payload passed to jwt.encode
        mock_jwt_encode.assert_called_once()
        payload = mock_jwt_encode.call_args[1]['payload']
        
        self.assertEqual(payload["paymentsData"], [{
            "accountNumber": "123456",
            "convFeeState": "NY",
            "convFeeCountry": "US"
        }])

    @mock.patch('jwt.encode')
    async def test_guest_checkout_pixel_sets_anonymous_pm_token(self, mock_jwt_encode):
        """Test guest-checkout-pixel sets pmToken to anonymousPMOnly"""
        # Set up mocks
        mock_jwt_encode.return_value = "mocked.jwt.token"
        self.mock_post.return_value = MockResponse(self.mock_token_response, 200)

        # Create auth client with guest-checkout-pixel
        config = AuthConfig(
            base_url="https://api.example.com",
            pre_shared_key="test-key",
            tla="XYZ",
            pixels=[PixelType.GUEST_CHECKOUT],
            payments_data=[{"accountNumber": "123456"}]
        )
        
        auth_client = Auth(config)
        await auth_client.fetch_token()
        
        # Extract the payload passed to jwt.encode
        mock_jwt_encode.assert_called_once()
        payload = mock_jwt_encode.call_args[1]['payload']
        
        self.assertEqual(payload["pmToken"], ["anonymousPMOnly"])

    @mock.patch('jwt.encode')
    async def test_guest_checkout_pixel_overrides_pm_token(self, mock_jwt_encode):
        """Test guest-checkout-pixel overrides existing pmToken"""
        # Set up mocks
        mock_jwt_encode.return_value = "mocked.jwt.token"
        self.mock_post.return_value = MockResponse(self.mock_token_response, 200)

        # Create auth client with guest-checkout-pixel and existing pm_token
        config = AuthConfig(
            base_url="https://api.example.com",
            pre_shared_key="test-key",
            tla="XYZ",
            pixels=[PixelType.GUEST_CHECKOUT],
            pm_token=["existingToken1", "existingToken2"],
            payments_data=[{"accountNumber": "123456"}]
        )
        
        auth_client = Auth(config)
        await auth_client.fetch_token()
        
        # Extract the payload passed to jwt.encode
        mock_jwt_encode.assert_called_once()
        payload = mock_jwt_encode.call_args[1]['payload']
        
        self.assertEqual(payload["pmToken"], ["anonymousPMOnly"])

    def test_is_token_expired(self):
        """Test token expiry check"""
        # Create auth client
        auth_client = Auth(self.mock_config)
        
        # No token initially
        self.assertTrue(auth_client.is_token_expired())
        
        # Set expired token
        auth_client.token_expiry = int(datetime.now().timestamp()) - 3600
        self.assertTrue(auth_client.is_token_expired())
        
        # Set valid token
        auth_client.token_expiry = int(datetime.now().timestamp()) + 3600
        self.assertFalse(auth_client.is_token_expired())


if __name__ == "__main__":
    unittest.main()
