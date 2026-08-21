"""Tests for the generic Iceberg REST Catalog connection wrapper."""

import json
import unittest
from unittest.mock import Mock, patch

from botocore.exceptions import ClientError

from sagemaker_studio.connections.glue_connection_lib.connections.wrapper.glue_connection_wrapper import (
    GlueConnectionWrapper,
)
from sagemaker_studio.connections.glue_connection_lib.connections.wrapper.glue_connection_wrapper_inputs import (
    GlueConnectionWrapperInputs,
)
from sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.iceberg_rest_catalog_wrapper import (
    IcebergRestCatalogConnectionWrapper,
)

SECRET_ARN = "arn:aws:secretsmanager:us-east-1:123456789012:secret:test-secret"


def _make_connection(connection_type="DATABRICKSICEBERGRESTCATALOG", authentication_type="OAUTH2"):
    """Create a standard mock IRC connection object."""
    return {
        "Name": "test-irc-connection",
        "ConnectionType": connection_type,
        "ConnectionProperties": {
            "INSTANCE_URL": "https://example.cloud.databricks.com/api/2.1/unity-catalog/iceberg-rest",
            "SOURCE_CATALOG_LIST": '["catalog1", "catalog2"]',
        },
        "AuthenticationConfiguration": {
            "AuthenticationType": authentication_type,
            "SecretArn": SECRET_ARN,
        },
    }


def _make_secrets_manager_client(secret=None):
    """Create a mock Secrets Manager client returning the given secret payload."""
    if secret is None:
        secret = {"ACCESS_TOKEN": "secret-access-token"}
    client = Mock()
    client.get_secret_value.return_value = {"SecretString": json.dumps(secret)}
    return client


def _make_wrapper(
    connection=None,
    secrets_manager_client=None,
    glue_client=None,
    omit_glue=False,
    additional_options=None,
):
    """Create an IcebergRestCatalogConnectionWrapper with sensible defaults."""
    if connection is None:
        connection = _make_connection()
    if secrets_manager_client is None:
        secrets_manager_client = _make_secrets_manager_client()
    if glue_client is None and not omit_glue:
        glue_client = Mock()
    wrapper_inputs = GlueConnectionWrapperInputs(
        connection=connection,
        additional_options=additional_options or {},
        kms_client=Mock(),
        secrets_manager_client=secrets_manager_client,
        glue_client=glue_client,
    )
    return IcebergRestCatalogConnectionWrapper(wrapper_inputs)


class TestIcebergRestCatalogConnectionWrapper(unittest.TestCase):
    """Test cases for IcebergRestCatalogConnectionWrapper."""

    def test_get_catalog_configs_success(self):
        """Test successful get_catalog_configs returns properties plus the access token."""
        glue_client = Mock()
        wrapper = _make_wrapper(glue_client=glue_client)

        result = wrapper.get_catalog_configs()

        self.assertEqual(
            result["INSTANCE_URL"],
            "https://example.cloud.databricks.com/api/2.1/unity-catalog/iceberg-rest",
        )
        self.assertEqual(result["SOURCE_CATALOG_LIST"], '["catalog1", "catalog2"]')
        self.assertEqual(result["ACCESS_TOKEN"], "secret-access-token")

    def test_stored_token_used_without_refresh(self):
        """Test a stored OAuth2 token is used as-is, without a Glue refresh round trip."""
        glue_client = Mock()
        wrapper = _make_wrapper(glue_client=glue_client)

        result = wrapper.get_catalog_configs()

        glue_client.refresh_o_auth2_tokens.assert_not_called()
        self.assertEqual(result["ACCESS_TOKEN"], "secret-access-token")

    def test_missing_token_triggers_refresh_via_glue(self):
        """Test an OAuth2 connection with no stored token delegates the refresh to Glue."""
        call_order = []
        glue_client = Mock()
        glue_client.refresh_o_auth2_tokens.side_effect = lambda **_: call_order.append("refresh")

        secrets_manager_client = Mock()
        secret_values = iter([{}, {"ACCESS_TOKEN": "freshly-minted-token"}])

        def _get_secret_value(**_):
            call_order.append("get_secret")
            return {"SecretString": json.dumps(next(secret_values))}

        secrets_manager_client.get_secret_value.side_effect = _get_secret_value

        wrapper = _make_wrapper(
            secrets_manager_client=secrets_manager_client, glue_client=glue_client
        )
        result = wrapper.get_catalog_configs()

        glue_client.refresh_o_auth2_tokens.assert_called_once_with(
            ConnectionName="test-irc-connection"
        )
        self.assertEqual(call_order, ["get_secret", "refresh", "get_secret"])
        self.assertEqual(result["ACCESS_TOKEN"], "freshly-minted-token")

    def test_force_option_triggers_refresh_despite_stored_token(self):
        """Test forceTokenRefresh refreshes even when the secret already holds a token."""
        glue_client = Mock()
        secrets_manager_client = Mock()
        secret_values = iter([{"ACCESS_TOKEN": "stale-token"}, {"ACCESS_TOKEN": "refreshed-token"}])
        secrets_manager_client.get_secret_value.side_effect = lambda **_: {
            "SecretString": json.dumps(next(secret_values))
        }

        wrapper = _make_wrapper(
            secrets_manager_client=secrets_manager_client,
            glue_client=glue_client,
            additional_options={"forceTokenRefresh": "true"},
        )
        result = wrapper.get_catalog_configs()

        glue_client.refresh_o_auth2_tokens.assert_called_once_with(
            ConnectionName="test-irc-connection"
        )
        self.assertEqual(result["ACCESS_TOKEN"], "refreshed-token")

    @patch("sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.iceberg_rest_catalog_wrapper.time.sleep")
    def test_first_use_refresh_retries_until_token_appears(self, mock_sleep):
        """Test the post-refresh read also retries when no token was stored before.

        For a brand-new OAuth2 connection the secret has no token yet, and a lagging
        read-after-write could briefly keep returning an empty secret. The retry must
        cover this case too, not only the changed-value case.
        """
        glue_client = Mock()
        secrets_manager_client = Mock()
        # Initial read (empty), post-refresh lagging read (still empty), then the token.
        secret_values = iter([{}, {}, {"ACCESS_TOKEN": "first-token"}])
        secrets_manager_client.get_secret_value.side_effect = lambda **_: {
            "SecretString": json.dumps(next(secret_values))
        }

        wrapper = _make_wrapper(
            secrets_manager_client=secrets_manager_client, glue_client=glue_client
        )
        result = wrapper.get_catalog_configs()

        self.assertEqual(result["ACCESS_TOKEN"], "first-token")
        self.assertEqual(mock_sleep.call_count, 1)

    @patch("sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.iceberg_rest_catalog_wrapper.time.sleep")
    def test_refresh_reread_retries_until_secret_updates(self, mock_sleep):
        """Test the post-refresh read tolerates Secrets Manager eventual consistency."""
        glue_client = Mock()
        secrets_manager_client = Mock()
        # Initial read, then two stale reads, then the updated value.
        secret_values = iter(
            [
                {"ACCESS_TOKEN": "stale-token"},
                {"ACCESS_TOKEN": "stale-token"},
                {"ACCESS_TOKEN": "stale-token"},
                {"ACCESS_TOKEN": "refreshed-token"},
            ]
        )
        secrets_manager_client.get_secret_value.side_effect = lambda **_: {
            "SecretString": json.dumps(next(secret_values))
        }

        wrapper = _make_wrapper(
            secrets_manager_client=secrets_manager_client,
            glue_client=glue_client,
            additional_options={"forceTokenRefresh": "true"},
        )
        result = wrapper.get_catalog_configs()

        self.assertEqual(result["ACCESS_TOKEN"], "refreshed-token")
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.iceberg_rest_catalog_wrapper.time.sleep")
    def test_refresh_reread_gives_up_after_budget_and_uses_last_value(self, mock_sleep):
        """Test the stale value is used once the consistency retry budget is exhausted."""
        glue_client = Mock()
        secrets_manager_client = _make_secrets_manager_client(
            secret={"ACCESS_TOKEN": "stale-token"}
        )

        wrapper = _make_wrapper(
            secrets_manager_client=secrets_manager_client,
            glue_client=glue_client,
            additional_options={"forceTokenRefresh": "true"},
        )
        result = wrapper.get_catalog_configs()

        # Initial read + REFRESH_READ_ATTEMPTS post-refresh reads, then proceed anyway.
        self.assertEqual(result["ACCESS_TOKEN"], "stale-token")
        self.assertEqual(
            mock_sleep.call_count,
            IcebergRestCatalogConnectionWrapper.REFRESH_READ_ATTEMPTS - 1,
        )

    def test_missing_glue_client_raises(self):
        """Test a helpful error is raised when a refresh is needed but no Glue client given."""
        secrets_manager_client = _make_secrets_manager_client(secret={})
        wrapper = _make_wrapper(secrets_manager_client=secrets_manager_client, omit_glue=True)

        with self.assertRaises(ValueError) as ctx:
            wrapper.get_catalog_configs()

        self.assertIn("Glue client is required", str(ctx.exception))

    def test_missing_connection_name_raises(self):
        """Test a refresh with no connection Name is reported clearly."""
        connection = _make_connection()
        del connection["Name"]
        secrets_manager_client = _make_secrets_manager_client(secret={})
        wrapper = _make_wrapper(
            connection=connection, secrets_manager_client=secrets_manager_client
        )

        with self.assertRaises(ValueError) as ctx:
            wrapper.get_catalog_configs()

        self.assertIn("Connection 'Name' is required", str(ctx.exception))

    def test_get_catalog_configs_reads_secret_by_arn(self):
        """Test the access token is read from the secret referenced by the connection."""
        secrets_manager_client = _make_secrets_manager_client()
        wrapper = _make_wrapper(secrets_manager_client=secrets_manager_client)

        wrapper.get_catalog_configs()

        secrets_manager_client.get_secret_value.assert_called_once_with(SecretId=SECRET_ARN)

    def test_non_oauth2_connection_skips_refresh(self):
        """Test a statically issued bearer token is used without calling Glue."""
        glue_client = Mock()
        connection = _make_connection(authentication_type="CUSTOM")
        wrapper = _make_wrapper(connection=connection, glue_client=glue_client)

        result = wrapper.get_catalog_configs()

        glue_client.refresh_o_auth2_tokens.assert_not_called()
        self.assertEqual(result["ACCESS_TOKEN"], "secret-access-token")

    @patch("sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.iceberg_rest_catalog_wrapper.time.sleep")
    def test_refresh_conflict_falls_back_to_stored_token(self, mock_sleep):
        """Test an in-flight refresh (ConflictException) does not fail the config build.

        Glue holds a per-connection refresh lock; the in-flight refresh persists fresh
        tokens to the same secret, so the wrapper proceeds with the stored token.
        Observed live against Glue: 'RefreshOAuth2Token Failed: Request already in
        progress'.
        """
        glue_client = Mock()
        glue_client.refresh_o_auth2_tokens.side_effect = ClientError(
            {
                "Error": {
                    "Code": "ConflictException",
                    "Message": "RefreshOAuth2Token Failed: Request already in progress",
                }
            },
            "RefreshOAuth2Tokens",
        )
        wrapper = _make_wrapper(
            glue_client=glue_client, additional_options={"forceTokenRefresh": "true"}
        )

        result = wrapper.get_catalog_configs()

        glue_client.refresh_o_auth2_tokens.assert_called_once_with(
            ConnectionName="test-irc-connection"
        )
        self.assertEqual(result["ACCESS_TOKEN"], "secret-access-token")

    def test_refresh_other_client_errors_propagate(self):
        """Test non-conflict ClientErrors from the refresh call are not swallowed."""
        glue_client = Mock()
        glue_client.refresh_o_auth2_tokens.side_effect = ClientError(
            {"Error": {"Code": "AccessDeniedException", "Message": "not authorized"}},
            "RefreshOAuth2Tokens",
        )
        wrapper = _make_wrapper(
            glue_client=glue_client, additional_options={"forceTokenRefresh": "true"}
        )

        with self.assertRaises(ClientError) as ctx:
            wrapper.get_catalog_configs()

        self.assertEqual(ctx.exception.response["Error"]["Code"], "AccessDeniedException")

    def test_custom_auth_reads_bearer_token_from_secret(self):
        """CUSTOM authentication stores its token under BEARER_TOKEN, not ACCESS_TOKEN."""
        glue_client = Mock()
        connection = _make_connection(authentication_type="CUSTOM")
        secrets_manager_client = _make_secrets_manager_client(
            secret={"BEARER_TOKEN": "static-bearer-token"}
        )
        wrapper = _make_wrapper(
            connection=connection,
            secrets_manager_client=secrets_manager_client,
            glue_client=glue_client,
        )

        result = wrapper.get_catalog_configs()

        glue_client.refresh_o_auth2_tokens.assert_not_called()
        self.assertEqual(result["ACCESS_TOKEN"], "static-bearer-token")

    def test_missing_secret_arn_raises(self):
        """Test a missing SecretArn is reported clearly."""
        connection = _make_connection()
        del connection["AuthenticationConfiguration"]["SecretArn"]
        wrapper = _make_wrapper(connection=connection)

        with self.assertRaises(ValueError) as ctx:
            wrapper.get_catalog_configs()

        self.assertIn("SecretArn is required", str(ctx.exception))

    @patch("sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.iceberg_rest_catalog_wrapper.time.sleep")
    def test_missing_access_token_in_secret_raises(self, mock_sleep):
        """Test a secret without an ACCESS_TOKEN entry is reported clearly."""
        secrets_manager_client = _make_secrets_manager_client(secret={"CLIENT_SECRET": "nope"})
        wrapper = _make_wrapper(secrets_manager_client=secrets_manager_client)

        with self.assertRaises(ValueError) as ctx:
            wrapper.get_catalog_configs()

        self.assertIn("ACCESS_TOKEN", str(ctx.exception))

    def test_missing_required_connection_property_raises(self):
        """Test a missing required connection property is reported clearly."""
        connection = _make_connection()
        del connection["ConnectionProperties"]["INSTANCE_URL"]
        wrapper = _make_wrapper(connection=connection)

        with self.assertRaises(ValueError) as ctx:
            wrapper.get_catalog_configs()

        self.assertIn("INSTANCE_URL", str(ctx.exception))

    def test_missing_multiple_required_connection_properties_raises(self):
        """Test all missing required connection properties are reported together."""
        connection = _make_connection()
        connection["ConnectionProperties"] = {}
        wrapper = _make_wrapper(connection=connection)

        with self.assertRaises(ValueError) as ctx:
            wrapper.get_catalog_configs()

        self.assertIn("INSTANCE_URL", str(ctx.exception))
        self.assertIn("SOURCE_CATALOG_LIST", str(ctx.exception))

    def test_secret_retrieval_error_is_wrapped(self):
        """Test Secrets Manager failures surface the shared error message."""
        secrets_manager_client = Mock()
        secrets_manager_client.get_secret_value.side_effect = Exception("Access denied")
        wrapper = _make_wrapper(secrets_manager_client=secrets_manager_client)

        with self.assertRaises(ValueError) as ctx:
            wrapper.get_catalog_configs()

        self.assertIn("Failed to retrieve or parse secret", str(ctx.exception))

    def test_refresh_failure_propagates(self):
        """Test a failed refresh is not silently swallowed."""
        glue_client = Mock()
        glue_client.refresh_o_auth2_tokens.side_effect = Exception("AccessDeniedException")
        wrapper = _make_wrapper(
            glue_client=glue_client, additional_options={"forceTokenRefresh": "true"}
        )

        with self.assertRaises(Exception) as ctx:
            wrapper.get_catalog_configs()

        self.assertIn("AccessDeniedException", str(ctx.exception))


class TestIcebergRestCatalogConnectionRouting(unittest.TestCase):
    """Test that the supported IRC connection types route to the generic wrapper."""

    def test_new_irc_types_route_to_generic_wrapper(self):
        """Test the three delegated IRC types resolve to IcebergRestCatalogConnectionWrapper."""
        for connection_type in (
            "DATABRICKSICEBERGRESTCATALOG",
            "SNOWFLAKEICEBERGRESTCATALOG",
            "ICEBERGRESTCATALOG",
        ):
            with self.subTest(connection_type=connection_type):
                wrapper_inputs = GlueConnectionWrapperInputs(
                    connection=_make_connection(connection_type=connection_type),
                    additional_options={},
                    kms_client=Mock(),
                    secrets_manager_client=_make_secrets_manager_client(),
                    glue_client=Mock(),
                )
                wrapper = GlueConnectionWrapper.create(wrapper_inputs)
                self.assertIsInstance(wrapper, IcebergRestCatalogConnectionWrapper)

    def test_workday_irc_type_is_unchanged(self):
        """Test Workday still routes to its own wrapper."""
        from sagemaker_studio.connections.glue_connection_lib.connections.wrapper.local.workday_irc_wrapper import (
            WorkdayIcebergRestCatalogConnectionWrapper,
        )

        wrapper_inputs = GlueConnectionWrapperInputs(
            connection=_make_connection(connection_type="WORKDAYICEBERGRESTCATALOG"),
            additional_options={},
            kms_client=Mock(),
            secrets_manager_client=_make_secrets_manager_client(),
        )
        wrapper = GlueConnectionWrapper.create(wrapper_inputs)
        self.assertIsInstance(wrapper, WorkdayIcebergRestCatalogConnectionWrapper)


if __name__ == "__main__":
    unittest.main()
