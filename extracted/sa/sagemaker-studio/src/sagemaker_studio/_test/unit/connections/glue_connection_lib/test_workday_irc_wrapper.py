"""Tests for Workday Iceberg REST Catalog connection wrapper."""

import json
import unittest
from unittest.mock import Mock, patch

from sagemaker_studio.connections.glue_connection_lib.connections.wrapper.glue_connection_wrapper_inputs import (
    GlueConnectionWrapperInputs,
)
from sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.workday_irc_wrapper import (
    WorkdayIcebergRestCatalogConnectionWrapper,
)


def _make_connection():
    """Create a standard mock Workday IRC connection object."""
    return {
        "Name": "test-workday-irc-connection",
        "ConnectionType": "WORKDAY",
        "ConnectionProperties": {
            "INSTANCE_URL": "https://workday.example.com",
            "SOURCE_CATALOG_LIST": "catalog1,catalog2",
            "TENANT_ID": "test-tenant",
        },
        "AuthenticationConfiguration": {
            "OAuth2Properties": {
                "OAuth2ClientApplication": {
                    "UserManagedClientApplicationClientId": "test-client-id",
                },
                "TokenUrl": "https://workday.example.com/oauth/token",
                "Scope": "workday:scope",
            },
            "SecretArn": "arn:aws:secretsmanager:us-east-1:123456789012:secret:test-secret",
        },
    }


def _make_wrapper(connection=None, secrets_manager_client=None):
    """Create a WorkdayIcebergRestCatalogConnectionWrapper with defaults."""
    if connection is None:
        connection = _make_connection()
    if secrets_manager_client is None:
        secrets_manager_client = Mock()
        secrets_manager_client.get_secret_value.return_value = {
            "SecretString": json.dumps(
                {"USERNAME": "test-user", "PRIVATE_KEY_PEM": "test-private-key"}
            )
        }
    wrapper_inputs = GlueConnectionWrapperInputs(
        connection=connection,
        additional_options={},
        kms_client=Mock(),
        secrets_manager_client=secrets_manager_client,
    )
    return WorkdayIcebergRestCatalogConnectionWrapper(wrapper_inputs)


class TestWorkdayIcebergRestCatalogConnectionWrapper(unittest.TestCase):
    """Test cases for WorkdayIcebergRestCatalogConnectionWrapper."""

    @patch(
        "sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.workday_irc_wrapper"
        ".WorkdayIcebergRestCatalogConnectionWrapper._get_access_token"
    )
    def test_get_catalog_configs_success(self, mock_get_token):
        """Test successful get_catalog_configs populates SparkProperties."""
        mock_get_token.side_effect = lambda opts: {**opts, "ACCESS_TOKEN": "mock-token"}

        wrapper = _make_wrapper()
        result = wrapper.get_catalog_configs()

        self.assertEqual(result["INSTANCE_URL"], "https://workday.example.com")
        self.assertEqual(result["SOURCE_CATALOG_LIST"], "catalog1,catalog2")
        self.assertEqual(result["TENANT_ID"], "test-tenant")
        self.assertEqual(result["CLIENT_ID"], "test-client-id")
        self.assertEqual(result["TOKEN_URL"], "https://workday.example.com/oauth/token")
        self.assertEqual(result["USERNAME"], "test-user")
        self.assertEqual(result["PRIVATE_KEY_PEM"], "test-private-key")
        self.assertEqual(result["ACCESS_TOKEN"], "mock-token")

    @patch(
        "sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.workday_irc_wrapper"
        ".WorkdayIcebergRestCatalogConnectionWrapper._get_access_token"
    )
    def test_get_catalog_configs_calls_secret_manager(self, mock_get_token):
        """Test that get_catalog_configs retrieves secrets from Secrets Manager."""
        mock_get_token.side_effect = lambda opts: opts

        mock_sm = Mock()
        mock_sm.get_secret_value.return_value = {
            "SecretString": json.dumps({"USERNAME": "secret-user", "PRIVATE_KEY_PEM": "secret-key"})
        }

        wrapper = _make_wrapper(secrets_manager_client=mock_sm)
        result = wrapper.get_catalog_configs()

        mock_sm.get_secret_value.assert_called_once_with(
            SecretId="arn:aws:secretsmanager:us-east-1:123456789012:secret:test-secret"
        )
        self.assertEqual(result["USERNAME"], "secret-user")
        self.assertEqual(result["PRIVATE_KEY_PEM"], "secret-key")

    def test_get_catalog_configs_secret_manager_error(self):
        """Test get_catalog_configs raises when secret retrieval fails."""
        mock_sm = Mock()
        mock_sm.get_secret_value.side_effect = Exception("Access denied")

        wrapper = _make_wrapper(secrets_manager_client=mock_sm)

        with self.assertRaises(ValueError) as ctx:
            wrapper.get_catalog_configs()

        self.assertIn("Failed to retrieve or parse secret", str(ctx.exception))

    def test_get_catalog_configs_missing_connection_property(self):
        """Test get_catalog_configs raises on missing ConnectionProperties key."""
        connection = _make_connection()
        del connection["ConnectionProperties"]["INSTANCE_URL"]

        wrapper = _make_wrapper(connection=connection)

        with self.assertRaises(KeyError):
            wrapper.get_catalog_configs()

    def test_get_catalog_configs_missing_oauth2_property(self):
        """Test get_catalog_configs raises on missing OAuth2Properties key."""
        connection = _make_connection()
        del connection["AuthenticationConfiguration"]["OAuth2Properties"]["OAuth2ClientApplication"]

        wrapper = _make_wrapper(connection=connection)

        with self.assertRaises(KeyError):
            wrapper.get_catalog_configs()

    @patch("sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.workday_irc_wrapper.requests")
    @patch("sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.workday_irc_wrapper.jwt")
    @patch("sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.workday_irc_wrapper.uuid")
    @patch("sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.workday_irc_wrapper.time")
    def test_get_access_token_success(self, mock_time, mock_uuid, mock_jwt, mock_requests):
        """Test _get_access_token returns options with ACCESS_TOKEN on success."""
        mock_time.time.return_value = 1000
        mock_uuid.uuid4.return_value = "test-uuid"
        mock_jwt.encode.return_value = "encoded-jwt"
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"access_token": "workday-access-token"}
        mock_requests.post.return_value = mock_resp

        options = {
            "CLIENT_ID": "cid",
            "USERNAME": "user",
            "TENANT_ID": "tenant",
            "TOKEN_URL": "https://token.url",
            "PRIVATE_KEY_PEM": "pem-key",
            "SCOPE": "workday:scope",
        }

        wrapper = _make_wrapper()
        result = wrapper._get_access_token(options)

        self.assertEqual(result["ACCESS_TOKEN"], "workday-access-token")
        mock_jwt.encode.assert_called_once_with(
            {
                "iss": "cid",
                "sub": "user",
                "aud": "tenant",
                "exp": 1300,
                "iat": 1000,
                "jti": "test-uuid",
            },
            "pem-key",
            algorithm="RS256",
        )
        mock_requests.post.assert_called_once()

    @patch("sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.workday_irc_wrapper.requests")
    @patch("sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.workday_irc_wrapper.jwt")
    @patch("sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.workday_irc_wrapper.time")
    def test_get_access_token_failure(self, mock_time, mock_jwt, mock_requests):
        """Test _get_access_token raises on non-200 response."""
        mock_time.time.return_value = 1000
        mock_jwt.encode.return_value = "encoded-jwt"
        mock_resp = Mock()
        mock_resp.status_code = 401
        mock_resp.text = "Unauthorized"
        mock_requests.post.return_value = mock_resp

        options = {
            "CLIENT_ID": "cid",
            "USERNAME": "user",
            "TENANT_ID": "tenant",
            "TOKEN_URL": "https://token.url",
            "PRIVATE_KEY_PEM": "pem-key",
            "SCOPE": "workday:scope",
        }

        wrapper = _make_wrapper()
        with self.assertRaises(Exception) as ctx:
            wrapper._get_access_token(options)

        self.assertIn("Token request failed: 401 Unauthorized", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
