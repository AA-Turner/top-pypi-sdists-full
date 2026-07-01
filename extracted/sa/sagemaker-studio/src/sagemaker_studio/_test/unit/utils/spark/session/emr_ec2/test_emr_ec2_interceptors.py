"""Tests for EMR on EC2 Spark Connect interceptors."""

import datetime
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest


# Mock SparkConnectGrpcException as a real exception class
class _MockSparkConnectGrpcException(Exception):
    pass


with patch("sagemaker_studio.Project"):

    sys.modules["aws_embedded_metrics"] = Mock()
    sys.modules["aws_embedded_metrics.sinks"] = Mock()
    sys.modules["aws_embedded_metrics.sinks.stdout_sink"] = Mock()
    sys.modules["aws_embedded_metrics.logger"] = Mock()
    sys.modules["aws_embedded_metrics.logger.metrics_logger"] = Mock()
    sys.modules["aws_embedded_metrics.logger.metrics_context"] = Mock()
    sys.modules["aws_embedded_metrics.environment"] = Mock()
    sys.modules["aws_embedded_metrics.environment.local_environment"] = Mock()

    pyspark_modules = [
        "pyspark",
        "pyspark.sql",
        "pyspark.sql.session",
        "pyspark.sql.connect",
        "pyspark.sql.connect.session",
        "pyspark.sql.connect.client",
        "grpc",
        "pyspark.errors",
        "pyspark.errors.exceptions",
        "pyspark.errors.exceptions.connect",
    ]

    for module_name in pyspark_modules:
        existing = sys.modules.get(module_name)
        if module_name == "grpc":
            mock_module = existing if existing is not None else Mock()
            mock_module.insecure_channel = Mock()
            mock_module.secure_channel = Mock()
            mock_module.intercept_channel = Mock()
            mock_module.UnaryUnaryClientInterceptor = type("UnaryUnaryClientInterceptor", (), {})
            mock_module.UnaryStreamClientInterceptor = type("UnaryStreamClientInterceptor", (), {})
            mock_module.StreamUnaryClientInterceptor = type("StreamUnaryClientInterceptor", (), {})
            mock_module.StreamStreamClientInterceptor = type(
                "StreamStreamClientInterceptor", (), {}
            )
            mock_module.ClientCallDetails = type("ClientCallDetails", (), {})
            sys.modules[module_name] = mock_module
        elif module_name == "pyspark.sql.connect.client":
            mock_module = existing if existing is not None else Mock()
            mock_module.ChannelBuilder = type(
                "ChannelBuilder",
                (),
                {
                    "__init__": lambda self, url: None,
                    "toChannel": lambda self: Mock(),
                },
            )
            sys.modules[module_name] = mock_module
        elif module_name == "pyspark.errors.exceptions.connect":
            mock_module = existing if existing is not None else Mock()
            mock_module.SparkConnectGrpcException = _MockSparkConnectGrpcException
            sys.modules[module_name] = mock_module
        elif module_name not in sys.modules:
            sys.modules[module_name] = Mock()

    from sagemaker_studio.utils.spark.session.base_interceptors import (
        _ClientCallDetails,
    )
    from sagemaker_studio.utils.spark.session.emr_ec2.interceptors import (
        EmrEc2ChannelBuilder,
        EmrEc2SparkConnectInterceptor,
    )


_SESSION_ID = "sess-abc123"
_CLUSTER_ID = "j-XYZ789"
_AUTH_TOKEN = "initial-token"
_REFRESHED_TOKEN = "refreshed-token"
_USERNAME = "user1"
_PASSWORD = "pass1"
_FUTURE = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
_PAST = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)


def _make_call_details(metadata=None):
    return _ClientCallDetails(
        method="/grpc.Method",
        timeout=30,
        metadata=metadata or [],
        credentials=None,
        wait_for_ready=False,
        compression=None,
    )


class TestEmrEc2SparkConnectInterceptorInit:
    def test_stores_cluster_and_client(self):
        client = MagicMock()
        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=client,
        )
        assert interceptor.session_id == _SESSION_ID
        assert interceptor.cluster_id == _CLUSTER_ID
        assert interceptor.emr_client is client

    def test_stores_initial_credentials(self):
        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=MagicMock(),
            initial_username=_USERNAME,
            initial_password=_PASSWORD,
        )
        assert interceptor._username == _USERNAME
        assert interceptor._password == _PASSWORD

    def test_defaults_credentials_to_none(self):
        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=MagicMock(),
        )
        assert interceptor._username is None
        assert interceptor._password is None

    def test_seeds_initial_token(self):
        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=MagicMock(),
            initial_auth_token=_AUTH_TOKEN,
            initial_token_expiry=_FUTURE,
        )
        assert interceptor._token_state.auth_token == _AUTH_TOKEN


class TestDoRefreshToken:
    def test_returns_new_token_state(self):
        expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        client = MagicMock()
        client.get_session_endpoint.return_value = {
            "AuthToken": _REFRESHED_TOKEN,
            "AuthTokenExpirationTime": expiry,
            "Credentials": {
                "UsernamePassword": {
                    "Username": "new-user",
                    "Password": "new-pass",
                }
            },
        }

        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=client,
        )

        state = interceptor._do_refresh_token()

        assert state.auth_token == _REFRESHED_TOKEN
        client.get_session_endpoint.assert_called_once_with(
            ClusterId=_CLUSTER_ID, SessionId=_SESSION_ID
        )

    def test_updates_username_and_password(self):
        expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        client = MagicMock()
        client.get_session_endpoint.return_value = {
            "AuthToken": _REFRESHED_TOKEN,
            "AuthTokenExpirationTime": expiry,
            "Credentials": {
                "UsernamePassword": {
                    "Username": "refreshed-user",
                    "Password": "refreshed-pass",
                }
            },
        }

        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=client,
            initial_username="old-user",
            initial_password="old-pass",
        )

        interceptor._do_refresh_token()

        assert interceptor._username == "refreshed-user"
        assert interceptor._password == "refreshed-pass"

    def test_handles_empty_credentials(self):
        expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        client = MagicMock()
        client.get_session_endpoint.return_value = {
            "AuthToken": _REFRESHED_TOKEN,
            "AuthTokenExpirationTime": expiry,
            "Credentials": {},
        }

        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=client,
        )

        state = interceptor._do_refresh_token()

        assert state.auth_token == _REFRESHED_TOKEN
        assert interceptor._username is None
        assert interceptor._password is None

    def test_handles_missing_credentials_key(self):
        expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        client = MagicMock()
        client.get_session_endpoint.return_value = {
            "AuthToken": _REFRESHED_TOKEN,
            "AuthTokenExpirationTime": expiry,
        }

        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=client,
        )

        state = interceptor._do_refresh_token()

        assert state.auth_token == _REFRESHED_TOKEN
        assert interceptor._username is None
        assert interceptor._password is None

    def test_subtracts_early_refresh_from_expiry(self):
        expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        client = MagicMock()
        client.get_session_endpoint.return_value = {
            "AuthToken": _REFRESHED_TOKEN,
            "AuthTokenExpirationTime": expiry,
            "Credentials": {},
        }

        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=client,
        )

        state = interceptor._do_refresh_token()

        expected = expiry - datetime.timedelta(seconds=interceptor._early_refresh_seconds)
        assert state.expiration_time == expected

    def test_resource_not_found_raises_grpc_exception(self):
        from botocore.exceptions import ClientError

        error_response = {
            "Error": {"Code": "ResourceNotFoundException", "Message": "Session not found"}
        }
        client = MagicMock()
        client.get_session_endpoint.side_effect = ClientError(error_response, "GetSessionEndpoint")

        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=client,
        )

        # Use the exception class from sys.modules (same one the interceptor will raise)
        from pyspark.errors.exceptions.connect import SparkConnectGrpcException

        with pytest.raises(SparkConnectGrpcException, match="terminated or expired"):
            interceptor._do_refresh_token()

    def test_other_client_error_reraises(self):
        from botocore.exceptions import ClientError

        error_response = {"Error": {"Code": "AccessDeniedException", "Message": "Not authorized"}}
        client = MagicMock()
        client.get_session_endpoint.side_effect = ClientError(error_response, "GetSessionEndpoint")

        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=client,
        )

        with pytest.raises(ClientError):
            interceptor._do_refresh_token()

    def test_non_client_error_reraises(self):
        client = MagicMock()
        client.get_session_endpoint.side_effect = RuntimeError("network failure")

        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=client,
        )

        with pytest.raises(RuntimeError, match="network failure"):
            interceptor._do_refresh_token()


class TestWithMetadata:
    def _make_interceptor(self, username=None, password=None):
        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=MagicMock(),
            initial_auth_token=_AUTH_TOKEN,
            initial_token_expiry=_FUTURE,
            initial_username=username,
            initial_password=password,
        )
        return interceptor

    def test_injects_session_id_as_authorization(self):
        interceptor = self._make_interceptor()
        details = interceptor._with_metadata(_make_call_details())
        metadata = dict(details.metadata)
        assert metadata["authorization"] == _SESSION_ID

    def test_injects_auth_token(self):
        interceptor = self._make_interceptor()
        details = interceptor._with_metadata(_make_call_details())
        metadata = dict(details.metadata)
        assert metadata["x-aws-proxy-auth"] == _AUTH_TOKEN

    def test_injects_username_and_password(self):
        interceptor = self._make_interceptor(username=_USERNAME, password=_PASSWORD)
        details = interceptor._with_metadata(_make_call_details())
        metadata = dict(details.metadata)
        assert metadata["x-emr-username"] == _USERNAME
        assert metadata["x-emr-password"] == _PASSWORD

    def test_omits_username_when_none(self):
        interceptor = self._make_interceptor(username=None, password=_PASSWORD)
        details = interceptor._with_metadata(_make_call_details())
        metadata = dict(details.metadata)
        assert "x-emr-username" not in metadata
        assert metadata["x-emr-password"] == _PASSWORD

    def test_omits_password_when_none(self):
        interceptor = self._make_interceptor(username=_USERNAME, password=None)
        details = interceptor._with_metadata(_make_call_details())
        metadata = dict(details.metadata)
        assert metadata["x-emr-username"] == _USERNAME
        assert "x-emr-password" not in metadata

    def test_preserves_existing_metadata(self):
        interceptor = self._make_interceptor()
        details = interceptor._with_metadata(_make_call_details(metadata=[("x-custom", "value")]))
        metadata = dict(details.metadata)
        assert metadata["x-custom"] == "value"
        assert metadata["authorization"] == _SESSION_ID

    def test_preserves_call_details_fields(self):
        interceptor = self._make_interceptor()
        original = _make_call_details()
        details = interceptor._with_metadata(original)
        assert details.method == original.method
        assert details.timeout == original.timeout
        assert details.credentials == original.credentials
        assert details.wait_for_ready == original.wait_for_ready
        assert details.compression == original.compression

    def test_triggers_refresh_when_token_expired(self):
        client = MagicMock()
        new_expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        client.get_session_endpoint.return_value = {
            "AuthToken": _REFRESHED_TOKEN,
            "AuthTokenExpirationTime": new_expiry,
            "Credentials": {"UsernamePassword": {"Username": "u", "Password": "p"}},
        }

        interceptor = EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=client,
        )

        details = interceptor._with_metadata(_make_call_details())
        metadata = dict(details.metadata)
        assert metadata["x-aws-proxy-auth"] == _REFRESHED_TOKEN
        client.get_session_endpoint.assert_called_once()


class TestInterceptMethods:
    @pytest.fixture
    def interceptor(self):
        return EmrEc2SparkConnectInterceptor(
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=MagicMock(),
            initial_auth_token=_AUTH_TOKEN,
            initial_token_expiry=_FUTURE,
            initial_username=_USERNAME,
            initial_password=_PASSWORD,
        )

    def test_intercept_unary_unary(self, interceptor):
        continuation = MagicMock(return_value="response")
        result = interceptor.intercept_unary_unary(continuation, _make_call_details(), "request")
        assert result == "response"
        continuation.assert_called_once()
        call_details = continuation.call_args[0][0]
        metadata = dict(call_details.metadata)
        assert metadata["authorization"] == _SESSION_ID
        assert metadata["x-aws-proxy-auth"] == _AUTH_TOKEN

    def test_intercept_unary_stream(self, interceptor):
        continuation = MagicMock(return_value="stream-response")
        result = interceptor.intercept_unary_stream(continuation, _make_call_details(), "request")
        assert result == "stream-response"
        continuation.assert_called_once()

    def test_intercept_stream_unary(self, interceptor):
        continuation = MagicMock(return_value="response")
        result = interceptor.intercept_stream_unary(
            continuation, _make_call_details(), iter(["req1"])
        )
        assert result == "response"
        continuation.assert_called_once()

    def test_intercept_stream_stream(self, interceptor):
        continuation = MagicMock(return_value="bidi-response")
        result = interceptor.intercept_stream_stream(
            continuation, _make_call_details(), iter(["req1"])
        )
        assert result == "bidi-response"
        continuation.assert_called_once()


class TestEmrEc2ChannelBuilder:
    def test_stores_all_params(self):
        client = MagicMock()
        builder = EmrEc2ChannelBuilder(
            url="sc://host:443/;use_ssl=true",
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=client,
            initial_auth_token=_AUTH_TOKEN,
            initial_token_expiry=_FUTURE,
            initial_username=_USERNAME,
            initial_password=_PASSWORD,
        )
        assert builder._emr_session_id == _SESSION_ID
        assert builder.cluster_id == _CLUSTER_ID
        assert builder.emr_client is client
        assert builder.initial_auth_token == _AUTH_TOKEN
        assert builder.initial_token_expiry == _FUTURE
        assert builder.initial_username == _USERNAME
        assert builder.initial_password == _PASSWORD

    def test_create_interceptor_returns_correct_type(self):
        builder = EmrEc2ChannelBuilder(
            url="sc://host:443/;use_ssl=true",
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=MagicMock(),
            initial_auth_token=_AUTH_TOKEN,
            initial_token_expiry=_FUTURE,
            initial_username=_USERNAME,
            initial_password=_PASSWORD,
        )
        interceptor = builder._create_interceptor()
        assert isinstance(interceptor, EmrEc2SparkConnectInterceptor)

    def test_create_interceptor_passes_all_params(self):
        client = MagicMock()
        builder = EmrEc2ChannelBuilder(
            url="sc://host:443/;use_ssl=true",
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=client,
            initial_auth_token=_AUTH_TOKEN,
            initial_token_expiry=_FUTURE,
            initial_username=_USERNAME,
            initial_password=_PASSWORD,
        )

        interceptor = builder._create_interceptor()

        assert interceptor.session_id == _SESSION_ID
        assert interceptor.cluster_id == _CLUSTER_ID
        assert interceptor.emr_client is client
        assert interceptor._username == _USERNAME
        assert interceptor._password == _PASSWORD

    @patch("grpc.intercept_channel")
    def test_to_channel_applies_interceptor(self, mock_intercept):
        builder = EmrEc2ChannelBuilder(
            url="sc://host:443/;use_ssl=true",
            session_id=_SESSION_ID,
            cluster_id=_CLUSTER_ID,
            emr_client=MagicMock(),
        )
        mock_intercept.return_value = "intercepted-channel"

        channel = builder.toChannel()

        assert channel == "intercepted-channel"
        mock_intercept.assert_called_once()
        interceptor_arg = mock_intercept.call_args[0][1]
        assert isinstance(interceptor_arg, EmrEc2SparkConnectInterceptor)
