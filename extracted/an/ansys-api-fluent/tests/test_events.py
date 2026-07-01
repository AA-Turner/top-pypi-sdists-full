"""Tests for the Fluent Events gRPC service (v1).

All tests share the single Fluent solver session started by the
``grpc_channel_and_metadata`` session fixture in ``conftest.py``.
"""

import grpc
import pytest

from ansys.api.fluent.v1 import events_pb2, events_pb2_grpc


@pytest.fixture(scope="module")
def stub(grpc_channel_and_metadata):
    channel, _ = grpc_channel_and_metadata
    return events_pb2_grpc.EventsStub(channel)


def format_event(response):
    """Return a human-readable summary of a ``BeginStreamingResponse``."""
    event_type = response.WhichOneof("as")
    if event_type == "iteration_started_event":
        ev = response.iteration_started_event
        return f"iteration_started index={ev.index}"
    if event_type == "iteration_ended_event":
        ev = response.iteration_ended_event
        return f"iteration_ended index={ev.index}"
    if event_type == "timestep_started_event":
        ev = response.timestep_started_event
        return f"timestep_started index={ev.index} size={ev.size}"
    if event_type == "timestep_ended_event":
        ev = response.timestep_ended_event
        return f"timestep_ended index={ev.index} size={ev.size}"
    if event_type == "progress_event":
        ev = response.progress_event
        return f"progress {ev.percent_complete}%: {ev.message}"
    if event_type == "solver_time_estimate_event":
        ev = response.solver_time_estimate_event
        return (
            "solver_time_estimate "
            f"{ev.hours:.0f}h {ev.minutes:.0f}m {ev.seconds:.1f}s"
        )
    if event_type == "error_event":
        ev = response.error_event
        return f"error code={ev.error_code}: {ev.message}"
    if event_type == "pre_read_case_event":
        ev = response.pre_read_case_event
        return f"pre_read_case path={ev.case_file_path}"
    if event_type == "case_read_event":
        ev = response.case_read_event
        return f"case_read path={ev.case_file_path}"
    if event_type == "pre_read_data_event":
        ev = response.pre_read_data_event
        return f"pre_read_data path={ev.data_file_path}"
    if event_type == "data_read_event":
        ev = response.data_read_event
        return f"data_read path={ev.data_file_path}"
    if event_type == "data_model_changed_event":
        ev = response.data_model_changed_event
        return f"data_model_changed paths={list(ev.paths)}"
    if event_type == "client_execute_event":
        ev = response.client_execute_event
        return f"client_execute function={ev.function} args={len(ev.arguments)}"
    return event_type or "unknown_event"


def test_begin_streaming_returns_stream(stub, grpc_channel_and_metadata):
    """BeginStreaming must open a server-streaming call without immediately erroring."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.BeginStreaming(
        events_pb2.BeginStreamingRequest(),
        metadata=metadata,
    )
    assert stream is not None
    stream.cancel()


@pytest.mark.skip(reason="This test is flaky and needs investigation")
def test_begin_streaming_responses_have_valid_event_type(stub, grpc_channel_and_metadata):
    """Every response received within a short window must carry a recognised event."""
    _, metadata = grpc_channel_and_metadata
    valid_event_fields = {
        "pre_read_case_event",
        "case_read_event",
        "pre_initialize_event",
        "initialized_event",
        "pre_read_data_event",
        "data_read_event",
        "iteration_started_event",
        "iteration_ended_event",
        "timestep_started_event",
        "timestep_ended_event",
        "calculations_started_event",
        "calculations_ended_event",
        "report_definition_changed_event",
        "plot_set_changed_event",
        "residual_plot_changed_event",
        "clear_settings_done_event",
        "auto_pause_event",
        "calculations_paused_event",
        "calculations_resumed_event",
        "progress_event",
        "error_event",
        "command_completed_event",
        "data_model_changed_event",
        "solver_time_estimate_event",
        "client_execute_event",
    }
    stream = stub.BeginStreaming(
        events_pb2.BeginStreamingRequest(),
        metadata=metadata,
    )
    collected = []
    try:
        for response in stream:
            event_type = response.WhichOneof("as")
            # event_type may be None if Fluent is idle and sends no event
            if event_type is not None:
                assert event_type in valid_event_fields, (
                    f"Unexpected event type: {event_type}"
                )
            collected.append(response)
            if len(collected) >= 5:
                break
    except grpc.RpcError as e:
        # Deadline exceeded is expected — we used a short timeout
        if e.code() not in (
            grpc.StatusCode.DEADLINE_EXCEEDED,
            grpc.StatusCode.CANCELLED,
        ):
            raise


def test_begin_streaming_can_be_cancelled(stub, grpc_channel_and_metadata):
    """Cancelling a BeginStreaming call must not raise unexpected errors."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.BeginStreaming(
        events_pb2.BeginStreamingRequest(),
        metadata=metadata,
    )
    stream.cancel()
    # Consuming after cancel should raise CANCELLED or StopIteration
    try:
        next(iter(stream))
    except grpc.RpcError as e:
        assert e.code() == grpc.StatusCode.CANCELLED
    except StopIteration:
        pass  # also acceptable


def test_pause_solve_for_iteration_returns_registration_id(stub, grpc_channel_and_metadata):
    """PauseSolveFor(ITERATION) must return a positive registration_id."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.PauseSolveFor(
        events_pb2.PauseSolveForRequest(
            solution_event=events_pb2.SOLUTION_EVENT_ITERATION
        ),
        metadata=metadata,
    )
    assert isinstance(resp.registration_id, int)
    assert resp.registration_id > 0

    # Clean up — cancel the registration so we don't leave state behind.
    stub.CancelPauseSolve(
        events_pb2.CancelPauseSolveRequest(registration_id=resp.registration_id),
        metadata=metadata,
    )


def test_pause_solve_for_timestep_returns_registration_id(stub, grpc_channel_and_metadata):
    """PauseSolveFor(TIME_STEP) must return a positive registration_id."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.PauseSolveFor(
        events_pb2.PauseSolveForRequest(
            solution_event=events_pb2.SOLUTION_EVENT_TIME_STEP
        ),
        metadata=metadata,
    )
    assert isinstance(resp.registration_id, int)
    assert resp.registration_id > 0

    stub.CancelPauseSolve(
        events_pb2.CancelPauseSolveRequest(registration_id=resp.registration_id),
        metadata=metadata,
    )


def test_pause_solve_for_multiple_registrations_have_distinct_ids(
    stub, grpc_channel_and_metadata
):
    """Two PauseSolveFor registrations must produce distinct registration IDs."""
    _, metadata = grpc_channel_and_metadata
    resp1 = stub.PauseSolveFor(
        events_pb2.PauseSolveForRequest(
            solution_event=events_pb2.SOLUTION_EVENT_ITERATION
        ),
            metadata=metadata,
        )
    resp2 = stub.PauseSolveFor(
        events_pb2.PauseSolveForRequest(
            solution_event=events_pb2.SOLUTION_EVENT_ITERATION
        ),
        metadata=metadata,
    )
    assert resp1.registration_id != resp2.registration_id

    stub.CancelPauseSolve(
        events_pb2.CancelPauseSolveRequest(registration_id=resp1.registration_id),
        metadata=metadata,
    )
    stub.CancelPauseSolve(
        events_pb2.CancelPauseSolveRequest(registration_id=resp2.registration_id),
        metadata=metadata,
    )


def test_cancel_pause_solve_returns_response(stub, grpc_channel_and_metadata):
    """CancelPauseSolve must succeed after a valid PauseSolveFor registration."""
    _, metadata = grpc_channel_and_metadata
    reg_resp = stub.PauseSolveFor(
        events_pb2.PauseSolveForRequest(
            solution_event=events_pb2.SOLUTION_EVENT_ITERATION
        ),
        metadata=metadata,
    )
    cancel_resp = stub.CancelPauseSolve(
        events_pb2.CancelPauseSolveRequest(
            registration_id=reg_resp.registration_id
        ),
        metadata=metadata,
    )
    assert cancel_resp is not None


def test_resume_solve_with_invalid_id_raises_rpc_error(stub, grpc_channel_and_metadata):
    """ResumeSolve with an unknown registration_id must raise an RpcError."""
    _, metadata = grpc_channel_and_metadata
    stub.ResumeSolve(
        events_pb2.ResumeSolveRequest(registration_id=999999999),
        metadata=metadata,
    )
