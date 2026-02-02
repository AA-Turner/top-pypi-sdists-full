"""
Unit tests for OAuth version detection logic.

These tests ensure that our OAuth version detection is robust
and handles all edge cases correctly.
"""

import unittest
import os
from unittest.mock import patch

# Add parent directory to path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.oauth_config import OAuthConfig
from auth.oauth_types import OAuthVersionDetectionParams


class TestOAuthVersionDetection(unittest.TestCase):
    """Test OAuth version detection logic."""

    def setUp(self):
        """Set up test fixtures."""
        # Create config with OAuth 2.1 disabled by default
        with patch.dict(os.environ, {"MCP_ENABLE_OAUTH21": "false"}):
            self.config_20 = OAuthConfig()

        # Create config with OAuth 2.1 enabled
        with patch.dict(os.environ, {"MCP_ENABLE_OAUTH21": "true"}):
            self.config_21 = OAuthConfig()

    def test_oauth20_when_disabled(self):
        """When OAuth 2.1 is disabled, always return OAuth 2.0."""
        # Even with PKCE parameters
        params_with_pkce = {
            "client_id": "test",
            "code_challenge": "challenge",
            "code_challenge_method": "S256",
        }

        result = self.config_20.detect_oauth_version(params_with_pkce)
        self.assertEqual(result, "oauth20", "Should return OAuth 2.0 when disabled")

    def test_oauth21_with_pkce(self):
        """When OAuth 2.1 is enabled and PKCE is present, return OAuth 2.1."""
        params_with_pkce = {
            "client_id": "test",
            "code_challenge": "challenge",
            "code_challenge_method": "S256",
        }

        result = self.config_21.detect_oauth_version(params_with_pkce)
        self.assertEqual(result, "oauth21", "Should return OAuth 2.1 with PKCE")

    def test_oauth20_without_pkce(self):
        """When OAuth 2.1 is enabled but no PKCE, return OAuth 2.0 for compatibility."""
        params_without_pkce = {"client_id": "test", "client_secret": "secret"}

        result = self.config_21.detect_oauth_version(params_without_pkce)
        self.assertEqual(result, "oauth20", "Should return OAuth 2.0 without PKCE")

    def test_public_client_without_pkce(self):
        """Public clients without PKCE should fall back to OAuth 2.0."""
        params_public_client = {
            "client_id": "test"
            # No client_secret, no PKCE
        }

        result = self.config_21.detect_oauth_version(params_public_client)
        self.assertEqual(
            result, "oauth20", "Public client without PKCE should use OAuth 2.0"
        )

    def test_code_verifier_triggers_oauth21(self):
        """Code verifier parameter should trigger OAuth 2.1."""
        params_with_verifier = {"client_id": "test", "code_verifier": "verifier"}

        result = self.config_21.detect_oauth_version(params_with_verifier)
        self.assertEqual(result, "oauth21", "Code verifier should trigger OAuth 2.1")

    def test_empty_params(self):
        """Empty parameters should default to OAuth 2.0."""
        result = self.config_21.detect_oauth_version({})
        self.assertEqual(result, "oauth20", "Empty params should default to OAuth 2.0")


class TestOAuthVersionDetectionParams(unittest.TestCase):
    """Test the OAuthVersionDetectionParams data class."""

    def test_from_request(self):
        """Test creating params from request dictionary."""
        request = {
            "client_id": "test_id",
            "client_secret": "test_secret",
            "code_challenge": "challenge",
            "extra_param": "ignored",
        }

        params = OAuthVersionDetectionParams.from_request(request)

        self.assertEqual(params.client_id, "test_id")
        self.assertEqual(params.client_secret, "test_secret")
        self.assertEqual(params.code_challenge, "challenge")
        self.assertIsNone(params.code_verifier)

    def test_has_pkce_with_challenge(self):
        """Test PKCE detection with code_challenge."""
        params = OAuthVersionDetectionParams(
            client_id="test", code_challenge="challenge"
        )

        self.assertTrue(params.has_pkce)

    def test_has_pkce_with_verifier(self):
        """Test PKCE detection with code_verifier."""
        params = OAuthVersionDetectionParams(client_id="test", code_verifier="verifier")

        self.assertTrue(params.has_pkce)

    def test_has_pkce_false(self):
        """Test PKCE detection when absent."""
        params = OAuthVersionDetectionParams(client_id="test", client_secret="secret")

        self.assertFalse(params.has_pkce)

    def test_is_public_client(self):
        """Test public client detection."""
        # Public client (no secret)
        public_params = OAuthVersionDetectionParams(client_id="test")
        self.assertTrue(public_params.is_public_client)

        # Confidential client (has secret)
        confidential_params = OAuthVersionDetectionParams(
            client_id="test", client_secret="secret"
        )
        self.assertFalse(confidential_params.is_public_client)

        # No client at all
        no_client_params = OAuthVersionDetectionParams()
        self.assertFalse(no_client_params.is_public_client)


class TestOAuthConfigMetadata(unittest.TestCase):
    """Test OAuth configuration metadata generation."""

    def test_metadata_oauth20(self):
        """Test metadata generation for OAuth 2.0."""
        with patch.dict(os.environ, {"MCP_ENABLE_OAUTH21": "false"}):
            config = OAuthConfig()

        metadata = config.get_authorization_server_metadata()

        # OAuth 2.0 should support both code and token response types
        self.assertIn("code", metadata["response_types_supported"])
        self.assertIn("token", metadata["response_types_supported"])

        # Should support both S256 and plain for OAuth 2.0
        self.assertIn("S256", metadata["code_challenge_methods_supported"])
        self.assertIn("plain", metadata["code_challenge_methods_supported"])

        # Should not have OAuth 2.1 specific fields
        self.assertNotIn("pkce_required", metadata)

    def test_metadata_oauth21(self):
        """Test metadata generation for OAuth 2.1."""
        with patch.dict(os.environ, {"MCP_ENABLE_OAUTH21": "true"}):
            config = OAuthConfig()

        metadata = config.get_authorization_server_metadata()

        # OAuth 2.1 should only support code (no implicit)
        self.assertEqual(metadata["response_types_supported"], ["code"])

        # Should only support S256 for OAuth 2.1
        self.assertEqual(metadata["code_challenge_methods_supported"], ["S256"])

        # Should have OAuth 2.1 specific fields
        self.assertTrue(metadata.get("pkce_required"))
        self.assertTrue(metadata.get("require_exact_redirect_uri"))

    def test_metadata_with_scopes(self):
        """Test metadata generation with scopes."""
        with patch.dict(os.environ, {"MCP_ENABLE_OAUTH21": "true"}):
            config = OAuthConfig()

        test_scopes = ["scope1", "scope2", "scope3"]
        metadata = config.get_authorization_server_metadata(scopes=test_scopes)

        self.assertEqual(metadata["scopes_supported"], test_scopes)

    def test_metadata_without_scopes(self):
        """Test metadata generation without scopes."""
        with patch.dict(os.environ, {"MCP_ENABLE_OAUTH21": "true"}):
            config = OAuthConfig()

        metadata = config.get_authorization_server_metadata()

        self.assertNotIn("scopes_supported", metadata)


if __name__ == "__main__":
    unittest.main()
