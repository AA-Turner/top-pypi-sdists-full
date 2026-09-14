import pytest

from agentic_devtools.cli.github.single_finding_dispatch import AcceptedTaskIdentity


def test_accepted_task_identity_keeps_optional_session_identity():
    accepted = AcceptedTaskIdentity(task_id="task-1", session_id=None)

    assert accepted.task_id == "task-1"
    assert accepted.session_id is None


@pytest.mark.parametrize("task_id", ["", "bad/id", "bad id", None])
def test_accepted_task_identity_rejects_unsafe_task_ids(task_id):
    with pytest.raises(ValueError, match="task_id"):
        AcceptedTaskIdentity(task_id=task_id, session_id="session-1")


@pytest.mark.parametrize("session_id", ["", "bad/id", "bad id", 1])
def test_accepted_task_identity_rejects_unsafe_session_ids(session_id):
    with pytest.raises(ValueError, match="session_id"):
        AcceptedTaskIdentity(task_id="task-1", session_id=session_id)
