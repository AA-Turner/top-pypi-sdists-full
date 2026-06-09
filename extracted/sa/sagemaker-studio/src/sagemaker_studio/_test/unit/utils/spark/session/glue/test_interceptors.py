"""Tests for Glue Spark Connect interceptors."""

import datetime
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest

# ---------------------------------------------------------------------------
# Module-level mock setup (must happen before importing the module under test)
# ---------------------------------------------------------------------------

# Ensure grpc has real classes for subclassing (needed by base_interceptors).
# We must handle the case where grpc is already in sys.modules as a Mock.
_grpc_mock = sys.modules.get("grpc")
if _grpc_mock is None:
    _grpc_mock = Mock()
    sys.modules["grpc"] = _grpc_mock

# Always override with real types so BaseSparkConnectGRPCInterceptor can subclass
_grpc_mock.UnaryUnaryClientInterceptor = type("UnaryUnaryClientInterceptor", (), {})
_grpc_mock.UnaryStreamClientInterceptor = type("UnaryStreamClientInterceptor", (), {})
_grpc_mock.StreamUnaryClientInterceptor = type("StreamUnaryClientInterceptor", (), {})
_grpc_mock.StreamStreamClientInterceptor = type("StreamStreamClientInterceptor", (), {})
_grpc_mock.ClientCallDetails = type("ClientCallDetails", (tuple,), {})
_grpc_mock.insecure_channel = Mock()
_grpc_mock.secure_channel = Mock()
_grpc_mock.intercept_channel = Mock()

# Ensure pyspark.sql.connect.client.ChannelBuilder is a real class
_pyspark_client = sys.modules.get("pyspark.sql.connect.client")
if _pyspark_client is None:
    _pyspark_client = Mock()
    sys.modules["pyspark.sql.connect.client"] = _pyspark_client

if not isinstance(getattr(_pyspark_client, "ChannelBuilder", None), type):
    _pyspark_client.ChannelBuilder = type(
        "ChannelBuilder",
        (),
        {
            "__init__": lambda self, url=None, *a, **kw: setattr(self, "_url", url),
            "toChannel": lambda self: Mock(),
        },
    )

# Ensure pyspark error modules exist
for mod in [
    "pyspark",
    "pyspark.sql",
    "pyspark.sql.connect",
    "pyspark.sql.connect.session",
    "pyspark.errors",
    "pyspark.errors.exceptions",
    "pyspark.errors.exceptions.connect",
]:
    if mod not in sys.modules:
        sys.modules[mod] = Mock()


# Create a real SparkConnectGrpcException for testing
class _MockSparkConnectGrpcException(Exception):
    pass


sys.modules["pyspark.errors.exceptions.connect"].SparkConnectGrpcException = (
    _MockSparkConnectGrpcException
)

# Force re-import of the modules under test so they pick up our mock setup
for mod_key in list(sys.modules.keys()):
    if "base_interceptors" in mod_key or "glue.interceptors" in mod_key:
        del sys.modules[mod_key]

from sagemaker_studio.utils.spark.session.glue.interceptors import (  # noqa: E402
    CustomChannelBuilder,
    SparkConnectGRPCInterceptor,
)

# ---------------------------------------------------------------------------
# SparkConnectGRPCInterceptor tests
# ---------------------------------------------------------------------------


class TestSparkConnectGRPCInterceptor:
    """Tests for Glue-specific SparkConnectGRPCInterceptor."""

    def _make_interceptor(self, glue_client=None, **kwargs):
        return SparkConnectGRPCInterceptor(
            glue_session_id="ses-abc123",
            glue_client=glue_client or MagicMock(),
            **kwargs,
        )

    def test_init_stores_glue_client(self):
        client = MagicMock()
        interceptor = self._make_interceptor(glue_client=client)
        assert interceptor.glue_client is client
        assert interceptor.session_id == "ses-abc123"

    def test_do_refresh_token_success_with_datetime_expiry(self):
        """Token refresh succeeds when AuthTokenExpirationTime is a datetime."""
        future = datetime.datetime(2025, 6, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
        client = MagicMock()
        client.get_session_endpoint.return_value = {
            "SparkConnect": {
                "Url": "sc://endpoint:443",
                "AuthToken": "new-token-123",
                "AuthTokenExpirationTime": future,
            }
        }

        interceptor = self._make_interceptor(glue_client=client)
        result = interceptor._do_refresh_token()

        assert result.auth_token == "new-token-123"
        assert result.expiration_time < future  # early refresh margin applied
        client.get_session_endpoint.assert_called_once_with(SessionId="ses-abc123")

    def test_do_refresh_token_success_with_epoch_timestamp(self):
        """Token refresh succeeds when AuthTokenExpirationTime is an epoch int."""
        epoch_ts = 1748779200  # 2025-06-01 12:00:00 UTC
        client = MagicMock()
        client.get_session_endpoint.return_value = {
            "SparkConnect": {
                "Url": "sc://endpoint:443",
                "AuthToken": "epoch-token",
                "AuthTokenExpirationTime": epoch_ts,
            }
        }

        interceptor = self._make_interceptor(glue_client=client)
        result = interceptor._do_refresh_token()

        assert result.auth_token == "epoch-token"
        assert isinstance(result.expiration_time, datetime.datetime)

    def test_do_refresh_token_non_client_error_raises(self):
        """Non-ClientError exceptions are re-raised directly."""
        client = MagicMock()
        client.get_session_endpoint.side_effect = ValueError("unexpected error")

        interceptor = self._make_interceptor(glue_client=client)
        with pytest.raises(ValueError, match="unexpected error"):
            interceptor._do_refresh_token()

    def test_do_refresh_token_entity_not_found_raises_grpc_exception(self):
        """EntityNotFoundException triggers SparkConnectGrpcException for auto-recovery."""
        from botocore.exceptions import ClientError

        error_response = {"Error": {"Code": "EntityNotFoundException", "Message": "Session gone"}}
        client = MagicMock()
        client.get_session_endpoint.side_effect = ClientError(error_response, "GetSessionEndpoint")

        interceptor = self._make_interceptor(glue_client=client)
        with pytest.raises(_MockSparkConnectGrpcException, match="terminated or not ready"):
            interceptor._do_refresh_token()

    def test_do_refresh_token_illegal_session_state_raises_grpc_exception(self):
        """IllegalSessionStateException triggers SparkConnectGrpcException for auto-recovery."""
        from botocore.exceptions import ClientError

        error_response = {"Error": {"Code": "IllegalSessionStateException", "Message": "Bad state"}}
        client = MagicMock()
        client.get_session_endpoint.side_effect = ClientError(error_response, "GetSessionEndpoint")

        interceptor = self._make_interceptor(glue_client=client)
        with pytest.raises(_MockSparkConnectGrpcException, match="terminated or not ready"):
            interceptor._do_refresh_token()

    @patch("time.sleep")
    def test_do_refresh_token_internal_service_exception_retries_and_succeeds(self, mock_sleep):
        """InternalServiceException triggers a retry; success on retry returns token."""
        from botocore.exceptions import ClientError

        future = datetime.datetime(2025, 6, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
        error_response = {"Error": {"Code": "InternalServiceException", "Message": "Transient"}}
        client = MagicMock()
        client.get_session_endpoint.side_effect = [
            ClientError(error_response, "GetSessionEndpoint"),
            {
                "SparkConnect": {
                    "Url": "sc://endpoint:443",
                    "AuthToken": "retry-token",
                    "AuthTokenExpirationTime": future,
                }
            },
        ]

        interceptor = self._make_interceptor(glue_client=client)
        result = interceptor._do_refresh_token()

        assert result.auth_token == "retry-token"
        mock_sleep.assert_called_once_with(2)

    @patch("time.sleep")
    def test_do_refresh_token_operation_timeout_retries_and_fails(self, mock_sleep):
        """OperationTimeoutException retry fails → SparkConnectGrpcException."""
        from botocore.exceptions import ClientError

        error_response = {"Error": {"Code": "OperationTimeoutException", "Message": "Timeout"}}
        client = MagicMock()
        client.get_session_endpoint.side_effect = [
            ClientError(error_response, "GetSessionEndpoint"),
            RuntimeError("retry also failed"),
        ]

        interceptor = self._make_interceptor(glue_client=client)
        with pytest.raises(_MockSparkConnectGrpcException, match="not available"):
            interceptor._do_refresh_token()

        mock_sleep.assert_called_once_with(2)

    def test_do_refresh_token_access_denied_raises_client_error(self):
        """Non-recoverable errors (AccessDenied) are re-raised as-is."""
        from botocore.exceptions import ClientError

        error_response = {"Error": {"Code": "AccessDeniedException", "Message": "Forbidden"}}
        client = MagicMock()
        client.get_session_endpoint.side_effect = ClientError(error_response, "GetSessionEndpoint")

        interceptor = self._make_interceptor(glue_client=client)
        with pytest.raises(ClientError):
            interceptor._do_refresh_token()

    def test_do_refresh_token_fallback_response_format(self):
        """When SparkConnect key missing, falls back to top-level response dict."""
        future = datetime.datetime(2025, 6, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
        client = MagicMock()
        # No "SparkConnect" wrapper — response is the endpoint data directly
        client.get_session_endpoint.return_value = {
            "Url": "sc://endpoint:443",
            "AuthToken": "direct-token",
            "AuthTokenExpirationTime": future,
        }

        interceptor = self._make_interceptor(glue_client=client)
        result = interceptor._do_refresh_token()

        assert result.auth_token == "direct-token"


# ---------------------------------------------------------------------------
# CustomChannelBuilder tests
# ---------------------------------------------------------------------------


class TestCustomChannelBuilder:
    """Tests for Glue CustomChannelBuilder."""

    def test_create_interceptor_returns_glue_interceptor(self):
        future = datetime.datetime(2025, 6, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
        client = MagicMock()
        builder = CustomChannelBuilder(
            glue_session_id="ses-xyz",
            url="sc://endpoint:443",
            glue_client=client,
            initial_auth_token="init-tok",
            initial_token_expiry=future,
        )

        interceptor = builder._create_interceptor()

        assert isinstance(interceptor, SparkConnectGRPCInterceptor)
        assert interceptor.session_id == "ses-xyz"
        assert interceptor.glue_client is client

    def test_init_stores_attributes(self):
        client = MagicMock()
        builder = CustomChannelBuilder(
            glue_session_id="ses-123",
            url="sc://host:443",
            glue_client=client,
            initial_auth_token="tok",
            initial_token_expiry=datetime.datetime.now(datetime.timezone.utc),
        )
        assert builder.glue_session_id == "ses-123"
        assert builder.glue_client is client
        assert builder.initial_auth_token == "tok"
