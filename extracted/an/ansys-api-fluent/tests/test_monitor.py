"""Tests for the Fluent Monitor gRPC service (v1).

All tests share the single Fluent solver session started by the
``grpc_channel_and_metadata`` session fixture in ``conftest.py``.
"""

import grpc
import pytest

from ansys.api.fluent.v1 import monitor_pb2, monitor_pb2_grpc

_VALID_MONITOR_TYPES = {
    monitor_pb2.MONITOR_TYPE_UNSPECIFIED,
    monitor_pb2.MONITOR_TYPE_RESIDUAL,
    monitor_pb2.MONITOR_TYPE_SOLUTION,
}

_VALID_XAXIS_TYPES = {
    monitor_pb2.XAXIS_TYPE_UNSPECIFIED,
    monitor_pb2.XAXIS_TYPE_ITERATION,
    monitor_pb2.XAXIS_TYPE_TIME,
}


# ---------------------------------------------------------------------------
# Stub fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def stub(grpc_channel_and_metadata):
    channel, _ = grpc_channel_and_metadata
    return monitor_pb2_grpc.MonitorStub(channel)


# ---------------------------------------------------------------------------
# Discovery fixture — resolved once per module
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def monitor_sets(stub, grpc_channel_and_metadata):
    """Return list[MonitorSet] from GetMonitors."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetMonitors(
        monitor_pb2.GetMonitorsRequest(),
        metadata=metadata,
    )
    return list(resp.monitor_sets)


def test_get_monitors_returns_response(stub, grpc_channel_and_metadata):
    """GetMonitors must return a GetMonitorsResponse with a monitor_sets field."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetMonitors(
        monitor_pb2.GetMonitorsRequest(),
        metadata=metadata,
    )
    assert hasattr(resp, "monitor_sets")
    assert isinstance(list(resp.monitor_sets), list)


def test_get_monitors_sets_have_non_empty_name(monitor_sets):
    """Every MonitorSet must have a non-empty name."""
    for ms in monitor_sets:
        assert len(ms.name) > 0, f"MonitorSet has empty name: {ms}"


def test_get_monitors_sets_have_valid_type(monitor_sets):
    """Every MonitorSet.type must be a recognised MonitorType enum value."""
    for ms in monitor_sets:
        assert ms.type in _VALID_MONITOR_TYPES, (
            f"MonitorSet '{ms.name}' has unknown type: {ms.type}"
        )


def test_get_monitors_sets_have_valid_axis(monitor_sets):
    """Every MonitorSet.axis must be a recognised XAxisType enum value."""
    for ms in monitor_sets:
        assert ms.axis in _VALID_XAXIS_TYPES, (
            f"MonitorSet '{ms.name}' has unknown axis type: {ms.axis}"
        )


def test_get_monitors_sets_have_non_negative_frequency(monitor_sets):
    """Every MonitorSet.frequency must be >= 0."""
    for ms in monitor_sets:
        assert ms.frequency >= 0, (
            f"MonitorSet '{ms.name}' has negative frequency: {ms.frequency}"
        )


def test_get_monitors_sets_contain_monitor_names(monitor_sets):
    """Every MonitorSet must list at least one monitor name."""
    for ms in monitor_sets:
        assert len(ms.monitors) > 0, (
            f"MonitorSet '{ms.name}' has no monitor entries"
        )


def test_get_monitors_unit_info_factor_is_non_negative(monitor_sets):
    """UnitData.factor must be >= 0 when a unit is specified."""
    for ms in monitor_sets:
        if ms.unit_info.unit:
            assert ms.unit_info.factor >= 0, (
                f"MonitorSet '{ms.name}' has negative unit factor: {ms.unit_info.factor}"
            )


def test_get_monitors_multiple_calls_are_consistent(stub, grpc_channel_and_metadata):
    """Two consecutive GetMonitors calls must return the same monitor set names."""
    _, metadata = grpc_channel_and_metadata
    resp1 = stub.GetMonitors(
        monitor_pb2.GetMonitorsRequest(), metadata=metadata,
    )
    resp2 = stub.GetMonitors(
        monitor_pb2.GetMonitorsRequest(), metadata=metadata,
    )
    names1 = sorted(ms.name for ms in resp1.monitor_sets)
    names2 = sorted(ms.name for ms in resp2.monitor_sets)
    assert names1 == names2, "GetMonitors returned different sets on consecutive calls"


def test_begin_streaming_opens_stream(stub, grpc_channel_and_metadata):
    """BeginStreaming must open a server-streaming call without immediate error."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.BeginStreaming(
        monitor_pb2.StreamingRequest(),
        metadata=metadata,
    )
    assert stream is not None
    stream.cancel()


def test_begin_streaming_can_be_cancelled(stub, grpc_channel_and_metadata):
    """Cancelling a BeginStreaming call must not raise unexpected errors."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.BeginStreaming(
        monitor_pb2.StreamingRequest(),
        metadata=metadata,
    )
    stream.cancel()
    try:
        next(iter(stream))
    except grpc.RpcError as e:
        assert e.code() == grpc.StatusCode.CANCELLED
    except StopIteration:
        pass  # also acceptable


def test_begin_streaming_responses_have_x_axis_data(stub, grpc_channel_and_metadata):
    """Each StreamingResponse must include an x_axis_data field."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.BeginStreaming(
        monitor_pb2.StreamingRequest(),
        metadata=metadata,
    )
    try:
        sample = next(iter(stream))
        assert hasattr(sample, "x_axis_data"), "StreamingResponse missing x_axis_data"
    except StopIteration:
        pytest.skip("BeginStreaming ended without a sample — solver may be idle")
    except grpc.RpcError as e:
        if e.code() in (grpc.StatusCode.DEADLINE_EXCEEDED, grpc.StatusCode.CANCELLED):
            pytest.skip(f"No samples received: {e.code()}")
        raise
    finally:
        stream.cancel()


def test_begin_streaming_x_axis_type_is_valid(stub, grpc_channel_and_metadata):
    """x_axis_data.x_axis_type in every sample must be a known XAxisType."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.BeginStreaming(
        monitor_pb2.StreamingRequest(),
        metadata=metadata,
    )
    try:
        sample = next(iter(stream))
        assert sample.x_axis_data.x_axis_type in _VALID_XAXIS_TYPES, (
            f"Unexpected x_axis_type: {sample.x_axis_data.x_axis_type}"
        )
    except StopIteration:
        pytest.skip("No samples available")
    except grpc.RpcError as e:
        if e.code() in (grpc.StatusCode.DEADLINE_EXCEEDED, grpc.StatusCode.CANCELLED):
            pytest.skip(f"No samples received: {e.code()}")
        raise
    finally:
        stream.cancel()


def test_begin_streaming_y_axis_values_have_name_and_value(stub, grpc_channel_and_metadata):
    """Each MonitorData entry in y_axis_values must have a non-empty name."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.BeginStreaming(
        monitor_pb2.StreamingRequest(),
        metadata=metadata,
    )
    try:
        sample = next(iter(stream))
        for y in sample.y_axis_values:
            assert len(y.name) > 0, "MonitorData.name must be non-empty"
            assert isinstance(y.value, float), "MonitorData.value must be a float"
    except StopIteration:
        pytest.skip("No samples available")
    except grpc.RpcError as e:
        if e.code() in (grpc.StatusCode.DEADLINE_EXCEEDED, grpc.StatusCode.CANCELLED):
            pytest.skip(f"No samples received: {e.code()}")
        raise
    finally:
        stream.cancel()


def test_begin_streaming_with_iteration_filter(stub, grpc_channel_and_metadata):
    """BeginStreaming with an XAXIS_TYPE_ITERATION filter must open without error."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.BeginStreaming(
        monitor_pb2.StreamingRequest(
            filters=[
                monitor_pb2.MonitorFilter(
                    x_axis_type=monitor_pb2.XAXIS_TYPE_ITERATION
                )
            ]
        ),
        metadata=metadata,
    )
    assert stream is not None
    stream.cancel()
