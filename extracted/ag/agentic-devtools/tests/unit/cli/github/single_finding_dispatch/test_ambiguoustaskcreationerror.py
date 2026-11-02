import pytest

from agentic_devtools.cli.github.single_finding_dispatch import (
    AcceptedTaskIdentity,
    AmbiguousTaskCreationError,
)


def test_ambiguous_task_creation_error_preserves_reason_and_identity():
    identity = AcceptedTaskIdentity("task-1", "session-1")

    error = AmbiguousTaskCreationError("provider response was lost", identity)

    assert str(error) == "provider response was lost"
    assert error.reason == "provider response was lost"
    assert error.identity == identity


@pytest.mark.parametrize(
    "reason,identity,error_type",
    [
        (" ", None, ValueError),
        ("provider response was lost", object(), TypeError),
    ],
)
def test_ambiguous_task_creation_error_rejects_invalid_values(reason, identity, error_type):
    with pytest.raises(error_type):
        AmbiguousTaskCreationError(reason, identity)
