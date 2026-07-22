"""Tests for EMR on EKS Spark Connect interceptors."""

import datetime
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest


# Mock SparkConnectGrpcException as a real exception class
class _MockSparkConnectGrpcException(Exception):
    pass


def _get_spark_connect_grpc_exception():
    """Import SparkConnectGrpcException from the mocked module at call time.

    This avoids cross-test mock contamination when another test file (e.g., Glue)
    sets sys.modules['pyspark.errors.exceptions.connect'] to its own mock class first.
    """
    from pyspark.errors.exceptions.connect import SparkConnectGrpcException

    return SparkConnectGrpcException


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
            mock_module.ClientCallDetails = type("ClientCallDetails", (tuple,), {})
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

    # Other test modules (e.g. test_connection_resolver, the manager test) register a
    # Mock for these in sys.modules. Drop any such mock so we import the REAL classes
    # under this module's mocks, regardless of test collection order.
    sys.modules.pop("sagemaker_studio.utils.spark.session.base_interceptors", None)
    sys.modules.pop("sagemaker_studio.utils.spark.session.emr_eks.interceptors", None)

    from sagemaker_studio.utils.spark.session.base_interceptors import (
        _ClientCallDetails,
    )
    from sagemaker_studio.utils.spark.session.emr_eks.interceptors import (
        EmrEksChannelBuilder,
        EmrEksSparkConnectInterceptor,
    )


_VC_ID = "vc-123"
_ENDPOINT_ID = "ep-abc"
_ROLE = "arn:aws:iam::111122223333:role/Exec"
_AUTH_TOKEN = "initial-token"
_REFRESHED_TOKEN = "refreshed-token"
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


def _credentials_response(token=_REFRESHED_TOKEN, expiry=None):
    return {
        "credentials": {"token": token, "endpointToken": "ep-token"},
        "expiresAt": expiry or _FUTURE,
    }


class TestEmrEksSparkConnectInterceptorInit:
    def test_stores_ids_and_client(self):
        client = MagicMock()
        interceptor = EmrEksSparkConnectInterceptor(
            virtual_cluster_id=_VC_ID,
            endpoint_id=_ENDPOINT_ID,
            emr_client=client,
            execution_role_arn=_ROLE,
        )
        assert interceptor.virtual_cluster_id == _VC_ID
        assert interceptor.endpoint_id == _ENDPOINT_ID
        assert interceptor.session_id == _ENDPOINT_ID
        assert interceptor.emr_client is client
        assert interceptor.execution_role_arn == _ROLE

    def test_seeds_initial_token(self):
        interceptor = EmrEksSparkConnectInterceptor(
            virtual_cluster_id=_VC_ID,
            endpoint_id=_ENDPOINT_ID,
            emr_client=MagicMock(),
            execution_role_arn=_ROLE,
            initial_auth_token=_AUTH_TOKEN,
            initial_token_expiry=_FUTURE,
        )
        assert interceptor._token_state.auth_token == _AUTH_TOKEN


class TestDoRefreshToken:
    def _interceptor(self, client):
        return EmrEksSparkConnectInterceptor(
            virtual_cluster_id=_VC_ID,
            endpoint_id=_ENDPOINT_ID,
            emr_client=client,
            execution_role_arn=_ROLE,
        )

    def test_returns_new_token_state(self):
        client = MagicMock()
        client.get_managed_endpoint_session_credentials.return_value = _credentials_response()
        state = self._interceptor(client)._do_refresh_token()
        assert state.auth_token == _REFRESHED_TOKEN
        client.get_managed_endpoint_session_credentials.assert_called_once_with(
            virtualClusterIdentifier=_VC_ID,
            endpointIdentifier=_ENDPOINT_ID,
            executionRoleArn=_ROLE,
            credentialType="TOKEN",
        )

    def test_subtracts_early_refresh_from_expiry(self):
        expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        client = MagicMock()
        client.get_managed_endpoint_session_credentials.return_value = _credentials_response(
            expiry=expiry
        )
        interceptor = self._interceptor(client)
        state = interceptor._do_refresh_token()
        expected = expiry - datetime.timedelta(seconds=interceptor._early_refresh_seconds)
        assert state.expiration_time == expected

    def test_resource_not_found_raises_grpc_exception(self):
        from botocore.exceptions import ClientError

        error_response = {
            "Error": {"Code": "ResourceNotFoundException", "Message": "Endpoint not found"}
        }
        client = MagicMock()
        client.get_managed_endpoint_session_credentials.side_effect = ClientError(
            error_response, "GetManagedEndpointSessionCredentials"
        )
        with pytest.raises(_get_spark_connect_grpc_exception(), match="terminated or expired"):
            self._interceptor(client)._do_refresh_token()

    def test_other_client_error_reraises(self):
        from botocore.exceptions import ClientError

        error_response = {"Error": {"Code": "AccessDeniedException", "Message": "Not authorized"}}
        client = MagicMock()
        client.get_managed_endpoint_session_credentials.side_effect = ClientError(
            error_response, "GetManagedEndpointSessionCredentials"
        )
        with pytest.raises(ClientError):
            self._interceptor(client)._do_refresh_token()

    def test_non_client_error_reraises(self):
        client = MagicMock()
        client.get_managed_endpoint_session_credentials.side_effect = RuntimeError(
            "network failure"
        )
        with pytest.raises(RuntimeError, match="network failure"):
            self._interceptor(client)._do_refresh_token()


class TestWithMetadata:
    def _make_interceptor(self):
        return EmrEksSparkConnectInterceptor(
            virtual_cluster_id=_VC_ID,
            endpoint_id=_ENDPOINT_ID,
            emr_client=MagicMock(),
            execution_role_arn=_ROLE,
            initial_auth_token=_AUTH_TOKEN,
            initial_token_expiry=_FUTURE,
        )

    def test_injects_auth_token(self):
        details = self._make_interceptor()._with_metadata(_make_call_details())
        assert dict(details.metadata)["x-aws-proxy-auth"] == _AUTH_TOKEN

    def test_token_only_no_emr_ec2_headers(self):
        # EMR on EKS authenticates with the proxy token alone — none of the EMR on EC2
        # headers (authorization / x-emr-username / x-emr-password) should be injected.
        details = self._make_interceptor()._with_metadata(_make_call_details())
        metadata = dict(details.metadata)
        assert "authorization" not in metadata
        assert "x-emr-username" not in metadata
        assert "x-emr-password" not in metadata

    def test_preserves_existing_metadata(self):
        details = self._make_interceptor()._with_metadata(
            _make_call_details(metadata=[("x-custom", "value")])
        )
        metadata = dict(details.metadata)
        assert metadata["x-custom"] == "value"
        assert metadata["x-aws-proxy-auth"] == _AUTH_TOKEN

    def test_preserves_call_details_fields(self):
        original = _make_call_details()
        details = self._make_interceptor()._with_metadata(original)
        assert details.method == original.method
        assert details.timeout == original.timeout
        assert details.credentials == original.credentials
        assert details.wait_for_ready == original.wait_for_ready
        assert details.compression == original.compression

    def test_triggers_refresh_when_token_expired(self):
        client = MagicMock()
        client.get_managed_endpoint_session_credentials.return_value = _credentials_response()
        interceptor = EmrEksSparkConnectInterceptor(
            virtual_cluster_id=_VC_ID,
            endpoint_id=_ENDPOINT_ID,
            emr_client=client,
            execution_role_arn=_ROLE,
            initial_auth_token=_AUTH_TOKEN,
            initial_token_expiry=_PAST,
        )
        details = interceptor._with_metadata(_make_call_details())
        assert dict(details.metadata)["x-aws-proxy-auth"] == _REFRESHED_TOKEN
        client.get_managed_endpoint_session_credentials.assert_called_once()


class TestInterceptMethods:
    @pytest.fixture
    def interceptor(self):
        return EmrEksSparkConnectInterceptor(
            virtual_cluster_id=_VC_ID,
            endpoint_id=_ENDPOINT_ID,
            emr_client=MagicMock(),
            execution_role_arn=_ROLE,
            initial_auth_token=_AUTH_TOKEN,
            initial_token_expiry=_FUTURE,
        )

    def test_intercept_unary_unary(self, interceptor):
        continuation = MagicMock(return_value="response")
        result = interceptor.intercept_unary_unary(continuation, _make_call_details(), "request")
        assert result == "response"
        continuation.assert_called_once()
        metadata = dict(continuation.call_args[0][0].metadata)
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


class TestEmrEksChannelBuilder:
    def _builder(self, client=None):
        return EmrEksChannelBuilder(
            url="sc://host:443/;use_ssl=true",
            virtual_cluster_id=_VC_ID,
            endpoint_id=_ENDPOINT_ID,
            emr_client=client or MagicMock(),
            execution_role_arn=_ROLE,
            initial_auth_token=_AUTH_TOKEN,
            initial_token_expiry=_FUTURE,
        )

    def test_stores_all_params(self):
        client = MagicMock()
        builder = self._builder(client)
        assert builder.virtual_cluster_id == _VC_ID
        assert builder.endpoint_id == _ENDPOINT_ID
        assert builder.emr_client is client
        assert builder.execution_role_arn == _ROLE
        assert builder.initial_auth_token == _AUTH_TOKEN
        assert builder.initial_token_expiry == _FUTURE

    def test_create_interceptor_returns_correct_type(self):
        assert isinstance(self._builder()._create_interceptor(), EmrEksSparkConnectInterceptor)

    def test_create_interceptor_passes_all_params(self):
        client = MagicMock()
        interceptor = self._builder(client)._create_interceptor()
        assert interceptor.virtual_cluster_id == _VC_ID
        assert interceptor.endpoint_id == _ENDPOINT_ID
        assert interceptor.emr_client is client
        assert interceptor.execution_role_arn == _ROLE

    @patch("grpc.intercept_channel")
    def test_to_channel_applies_interceptor(self, mock_intercept):
        mock_intercept.return_value = "intercepted-channel"
        channel = self._builder().toChannel()
        assert channel == "intercepted-channel"
        mock_intercept.assert_called_once()
        interceptor_arg = mock_intercept.call_args[0][1]
        assert isinstance(interceptor_arg, EmrEksSparkConnectInterceptor)
