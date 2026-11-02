from pathlib import Path

import pytest

from agentic_devtools.cli.ci.dispatch_state import (
    DispatchIdentity,
    consume_task_creation_capability,
    create_intent,
    load_dispatch_record,
    transition_dispatch,
)

SHA = "c" * 40


def test_consumes_the_persisted_creating_capability_once(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 9, SHA, 1)
    create_intent(path, identity)
    transition_dispatch(path, identity, "marker_succeeded", marker_comment_id=11)
    creating = transition_dispatch(path, identity, "preparation_succeeded")

    consumed = consume_task_creation_capability(path, creating)

    assert consumed.state.value == "creating"
    assert consumed.attempt_capability_digest is None
    persisted = load_dispatch_record(path, identity)
    assert persisted == consumed


def test_rejects_missing_or_mismatched_creating_capabilities(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 9, SHA, 1)
    create_intent(path, identity)
    transition_dispatch(path, identity, "marker_succeeded", marker_comment_id=11)
    creating = transition_dispatch(path, identity, "preparation_succeeded")

    forged = creating.with_state("creating", attempt_capability="different-capability")
    with pytest.raises(ValueError, match="durably persisted creating marker"):
        consume_task_creation_capability(path, forged)

    consumed = consume_task_creation_capability(path, creating)
    with pytest.raises(ValueError, match="durably persisted creating marker"):
        consume_task_creation_capability(path, creating)

    recovered = load_dispatch_record(path, identity)
    assert recovered == consumed
    with pytest.raises(ValueError, match="non-empty string"):
        consume_task_creation_capability(path, recovered)


def test_rejects_missing_persisted_creating_record(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    creating = create_intent(path, DispatchIdentity("repo", 9, SHA, 1)).with_state(
        "reserved",
        marker_comment_id=11,
    )
    local_creating = creating.with_state("creating", attempt_capability="local-capability")

    with pytest.raises(ValueError, match="durably persisted creating marker"):
        consume_task_creation_capability(tmp_path / "missing.json", local_creating)
