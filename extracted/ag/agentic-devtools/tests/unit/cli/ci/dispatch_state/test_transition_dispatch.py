from pathlib import Path

import pytest

from agentic_devtools.cli.ci.dispatch_state import (
    DispatchIdentity,
    DispatchState,
    consume_task_creation_capability,
    create_intent,
    load_dispatch_record,
    transition_dispatch,
)

SHA = "a" * 40


def test_persists_transitioned_record(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 7, SHA, 1)
    create_intent(path, identity)

    transitioned = transition_dispatch(path, identity, "marker_success", marker_comment_id=3)

    assert transitioned.state is DispatchState.RESERVED
    assert load_dispatch_record(path, identity) == transitioned


def test_persists_pre_write_failure_from_creating(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 7, SHA, 1)
    create_intent(path, identity)
    transition_dispatch(path, identity, "marker_success", marker_comment_id=3)
    transition_dispatch(path, identity, "preparation_succeeded")

    transitioned = transition_dispatch(path, identity, "pre_write_failure")

    assert transitioned.state is DispatchState.RESERVED
    assert transitioned.retry_count == 1
    assert load_dispatch_record(path, identity) == transitioned


def test_persists_pre_write_failure_from_intent(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 7, SHA, 1)
    create_intent(path, identity)

    transitioned = transition_dispatch(path, identity, "pre_write_failure")

    assert transitioned.state is DispatchState.INTENT
    assert transitioned.retry_count == 1
    assert load_dispatch_record(path, identity) == transitioned


def test_persists_and_clears_creation_capability_digest(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 7, SHA, 1)
    create_intent(path, identity)
    transition_dispatch(path, identity, "marker_success", marker_comment_id=3)

    creating = transition_dispatch(path, identity, "preparation_succeeded")

    assert creating.attempt_capability is not None
    assert creating.attempt_capability_digest is not None
    assert load_dispatch_record(path, identity) == creating

    consume_task_creation_capability(path, creating)
    created = transition_dispatch(path, identity, "task_created", task_id="task-9")

    assert created.attempt_capability_digest is None


def test_rejects_task_results_before_capability_consumption(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 7, "b" * 40, 1)
    create_intent(path, identity)
    transition_dispatch(path, identity, "marker_success", marker_comment_id=3)
    transition_dispatch(path, identity, "preparation_succeeded")

    with pytest.raises(ValueError, match="capability consumption"):
        transition_dispatch(path, identity, "task_created", task_id="task-9")


def test_rejects_pre_write_failure_after_capability_consumption(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 7, SHA, 1)
    create_intent(path, identity)
    transition_dispatch(path, identity, "marker_success", marker_comment_id=3)
    creating = transition_dispatch(path, identity, "preparation_succeeded")

    consume_task_creation_capability(path, creating)

    with pytest.raises(ValueError, match="capability consumption"):
        transition_dispatch(path, identity, "pre_write_failure")


def test_raises_when_record_does_not_exist(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        transition_dispatch(tmp_path / "dispatch.json", DispatchIdentity("repo", 7, SHA, 1), "replay")
