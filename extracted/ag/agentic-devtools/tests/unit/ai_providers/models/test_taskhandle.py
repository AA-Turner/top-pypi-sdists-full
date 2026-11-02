from types import MappingProxyType

import pytest

from agentic_devtools.ai_providers.models import FailureEnvelope, TaskHandle, TaskState


def _make_failure() -> FailureEnvelope:
    return FailureEnvelope(
        category="transport_error",
        message="connection refused",
        details=None,
        retryable=True,
    )


def _make_state() -> TaskState:
    return TaskState(
        state="queued",
        failure=None,
        created_at="2023-01-01T00:00:00Z",
        metadata={},
    )


def test_task_handle_freezes_metadata():
    metadata = {"token": "secret", "nested": {"safe": [1]}}

    handle = TaskHandle(task_id="task-123", state=None, failure=None, metadata=metadata)

    assert handle.metadata["token"] == "<redacted>"
    assert handle.metadata["nested"]["safe"] == (1,)
    assert isinstance(handle.metadata, MappingProxyType)


def test_task_handle_valid_with_failure_and_no_task_id():
    failure = _make_failure()
    handle = TaskHandle(task_id=None, state=None, failure=failure, metadata={})
    assert handle.task_id is None
    assert handle.failure is failure


def test_task_handle_valid_with_task_id_and_state():
    state = _make_state()
    handle = TaskHandle(task_id="task-456", state=state, failure=None, metadata={})
    assert handle.task_id == "task-456"
    assert handle.state is state


def test_task_handle_rejects_all_none():
    with pytest.raises(ValueError, match="task_id is None requires failure is not None"):
        TaskHandle(task_id=None, state=None, failure=None, metadata={})


def test_task_handle_rejects_non_string_task_id():
    failure = _make_failure()
    with pytest.raises(
        ValueError,
        match=r"task_id must be a non-empty string matching \^\[A-Za-z0-9_-\]\+\$",
    ):
        TaskHandle(task_id=42, state=None, failure=failure, metadata={})  # type: ignore[arg-type]


@pytest.mark.parametrize("task_id", ["", "bad id", "slash/value"])
def test_task_handle_rejects_malformed_task_id(task_id: str):
    failure = _make_failure()
    with pytest.raises(
        ValueError,
        match=r"task_id must be a non-empty string matching \^\[A-Za-z0-9_-\]\+\$",
    ):
        TaskHandle(task_id=task_id, state=None, failure=failure, metadata={})


def test_task_handle_rejects_non_failure_envelope():
    with pytest.raises(ValueError, match="failure must be a FailureEnvelope when provided"):
        TaskHandle(task_id=None, state=None, failure="boom", metadata={})  # type: ignore[arg-type]


def test_task_handle_rejects_non_task_state():
    failure = _make_failure()
    with pytest.raises(ValueError, match="state must be a TaskState when provided"):
        TaskHandle(task_id="task-123", state={"state": "queued"}, failure=failure, metadata={})  # type: ignore[arg-type]


def test_task_handle_rejects_state_and_failure_both_set():
    state = _make_state()
    failure = _make_failure()
    with pytest.raises(ValueError, match="state and failure cannot both be non-None"):
        TaskHandle(task_id="task-123", state=state, failure=failure, metadata={})
