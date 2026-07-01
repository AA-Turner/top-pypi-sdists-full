"""Tests for the Fluent Connection gRPC service (v1).

All tests share the single Fluent session started by the ``grpc_channel_and_metadata``
session fixture in ``conftest.py``.
"""

import pytest

from ansys.api.fluent.v1 import connection_pb2, connection_pb2_grpc

_VALID_ERROR_CODES = {
    connection_pb2.CONNECTION_ERROR_UNSPECIFIED,
    connection_pb2.CONNECTION_ERROR_NONE,
    connection_pb2.CONNECTION_ERROR_PASSWORD_MISMATCH,
    connection_pb2.CONNECTION_ERROR_MAX_CONNECTIONS_COUNT_EXCEEDED,
    connection_pb2.CONNECTION_ERROR_UNKNOWN,
    connection_pb2.CONNECTION_ERROR_VERSION_MISMATCH,
    connection_pb2.CONNECTION_ERROR_WAIT_TIME_EXPIRED,
}

_FLUENT_VERSION = "27.1.0"


def _get_password(metadata):
    """Extract the plain-text password from gRPC metadata tuples."""
    for key, value in metadata:
        if key == "password":
            return value
    return ""


@pytest.fixture(scope="module")
def stub(grpc_channel_and_metadata):
    channel, _ = grpc_channel_and_metadata
    return connection_pb2_grpc.ConnectionStub(channel)


def test_connect_returns_stream(stub, grpc_channel_and_metadata):
    """Connect must return a server-streaming iterator without raising."""
    _, metadata = grpc_channel_and_metadata
    password = _get_password(metadata)
    stream = stub.Connect(
        connection_pb2.ConnectRequest(
            request_type=connection_pb2.ConnectRequest.REQUEST_TYPE_CONNECT,
            password=password,
            version=_FLUENT_VERSION,
        ),
        metadata=metadata,
    )
    assert stream is not None
    stream.cancel()


def test_connect_response_has_error_code_field(stub, grpc_channel_and_metadata):
    """ConnectResponse must expose an error_code attribute."""
    _, metadata = grpc_channel_and_metadata
    password = _get_password(metadata)
    stream = stub.Connect(
        connection_pb2.ConnectRequest(
            request_type=connection_pb2.ConnectRequest.REQUEST_TYPE_CONNECT,
            password=password,
            version=_FLUENT_VERSION,
        ),
        metadata=metadata,
    )
    first = next(iter(stream))
    stream.cancel()
    assert hasattr(first, "error_code")


def test_connect_without_version_field(stub, grpc_channel_and_metadata):
    """Connecting without a version string must still return a valid response."""
    _, metadata = grpc_channel_and_metadata
    password = _get_password(metadata)
    stream = stub.Connect(
        connection_pb2.ConnectRequest(
            request_type=connection_pb2.ConnectRequest.REQUEST_TYPE_CONNECT,
            password=password,
        ),
        metadata=metadata,
    )
    first = next(iter(stream))
    stream.cancel()
    assert first.error_code in _VALID_ERROR_CODES
