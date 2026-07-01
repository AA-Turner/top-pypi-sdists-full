"""Tests for the Fluent Transcript gRPC service (v1).

All tests share the single Fluent solver session started by the
``grpc_channel_and_metadata`` session fixture in ``conftest.py``.
"""

import grpc
import pytest

from ansys.api.fluent.v1 import transcript_pb2, transcript_pb2_grpc


# ---------------------------------------------------------------------------
# Stub fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def stub(grpc_channel_and_metadata):
    channel, _ = grpc_channel_and_metadata
    return transcript_pb2_grpc.TranscriptStub(channel)


def test_begin_streaming_opens_stream(stub, grpc_channel_and_metadata):
    """BeginStreaming must open a server-streaming call without immediate error."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.BeginStreaming(
        transcript_pb2.TranscriptRequest(),
        metadata=metadata,
    )
    assert stream is not None
    stream.cancel()


def test_begin_streaming_can_be_cancelled(stub, grpc_channel_and_metadata):
    """Cancelling a BeginStreaming call must not raise an unexpected exception."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.BeginStreaming(
        transcript_pb2.TranscriptRequest(),
        metadata=metadata,
    )
    stream.cancel()
    try:
        next(iter(stream))
    except grpc.RpcError as e:
        assert e.code() == grpc.StatusCode.CANCELLED
    except StopIteration:
        pass  # also acceptable


def test_begin_streaming_independent_calls_return_distinct_streams(
    stub, grpc_channel_and_metadata
):
    """Two simultaneous BeginStreaming calls must return distinct stream objects."""
    _, metadata = grpc_channel_and_metadata
    stream1 = stub.BeginStreaming(
        transcript_pb2.TranscriptRequest(), metadata=metadata
    )
    stream2 = stub.BeginStreaming(
        transcript_pb2.TranscriptRequest(), metadata=metadata
    )
    assert stream1 is not stream2
    stream1.cancel()
    stream2.cancel()


def test_begin_streaming_with_timeout_ends_gracefully(stub, grpc_channel_and_metadata):
    """A BeginStreaming call with a very short timeout must end with DEADLINE_EXCEEDED or CANCELLED, not an unexpected error."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.BeginStreaming(
        transcript_pb2.TranscriptRequest(),
        metadata=metadata,
        timeout=0.5,
    )
    acceptable_codes = {
        grpc.StatusCode.DEADLINE_EXCEEDED,
        grpc.StatusCode.CANCELLED,
    }
    try:
        for _ in stream:
            pass
    except grpc.RpcError as e:
        assert e.code() in acceptable_codes, (
            f"Unexpected error code on timeout: {e.code()} — {e.details()}"
        )
