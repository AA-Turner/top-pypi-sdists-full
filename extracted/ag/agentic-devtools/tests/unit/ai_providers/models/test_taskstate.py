import pytest

from agentic_devtools.ai_providers.models import FailureEnvelope, TaskState


def test_task_state_invariants():
    failure = FailureEnvelope(
        category="provider_error",
        message="Oops",
        details=None,
        retryable=True,
    )

    # Valid: lookup miss or failure-backed record
    TaskState(state=None, failure=failure, created_at="2023-01-01T00:00:00Z", metadata={})

    # Invalid: state None, failure None
    with pytest.raises(ValueError, match="state is None requires failure is not None"):
        TaskState(state=None, failure=None, created_at="2023-01-01T00:00:00Z", metadata={})

    # Valid: state failed, failure not None
    TaskState(state="failed", failure=failure, created_at="2023-01-01T00:00:00Z", metadata={})

    # Invalid: state failed, failure None
    with pytest.raises(ValueError, match="If state == 'failed', then failure must not be None"):
        TaskState(state="failed", failure=None, created_at="2023-01-01T00:00:00Z", metadata={})

    with pytest.raises(ValueError, match="failure must be a FailureEnvelope when provided"):
        TaskState(
            state="failed",
            failure="boom",  # type: ignore[arg-type]
            created_at="2023-01-01T00:00:00Z",
            metadata={},
        )

    # Valid: closed state, failure None
    TaskState(
        state="completed",
        failure=None,
        created_at="2023-01-01T00:00:00Z",
        metadata={"nested": {"token": "secret"}},
    )

    # Invalid: closed state, failure not None
    with pytest.raises(ValueError, match="If state is completed, then failure must be None"):
        TaskState(
            state="completed",
            failure=failure,
            created_at="2023-01-01T00:00:00Z",
            metadata={},
        )

    with pytest.raises(ValueError, match="state must be one of"):
        TaskState(
            state="unknown",
            failure=None,
            created_at="2023-01-01T00:00:00Z",
            metadata={},
        )

    with pytest.raises(ValueError, match="state must be one of"):
        TaskState(
            state=["completed"],  # type: ignore[arg-type]
            failure=None,
            created_at="2023-01-01T00:00:00Z",
            metadata={},
        )

    with pytest.raises(ValueError, match="created_at must be a valid ISO-8601 timestamp"):
        TaskState(
            state="completed",
            failure=None,
            created_at="date",
            metadata={},
        )
