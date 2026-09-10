from pathlib import Path

import pytest

from agentic_devtools.cli.ci.dispatch_state import (
    DispatchIdentity,
    consume_task_creation_capability,
    create_intent,
    load_dispatch_record,
    transition_dispatch,
)
from agentic_devtools.cli.ci.guards import assert_task_creation_allowed

SHA = "b" * 40


def test_requires_durably_persisted_creating_state(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 8, SHA, 1)
    create_intent(path, identity)
    reserved = transition_dispatch(path, identity, "marker_succeeded", marker_comment_id=10)

    with pytest.raises(ValueError):
        assert_task_creation_allowed(path, reserved)

    forged_creating = reserved.with_state("creating", attempt_capability="local-capability")
    with pytest.raises(ValueError):
        assert_task_creation_allowed(path, forged_creating)

    creating = transition_dispatch(path, identity, "preparation_succeeded")

    assert assert_task_creation_allowed(path, creating)

    recovered = load_dispatch_record(path, identity)
    assert recovered is not None
    assert recovered.state.value == "creating"
    assert recovered.attempt_capability_digest is not None

    consume_task_creation_capability(path, creating)
    with pytest.raises(ValueError, match="durably persisted creating marker"):
        assert_task_creation_allowed(path, creating)


def test_rejects_reconstructed_or_malformed_capabilities(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 8, SHA, 1)
    create_intent(path, identity)
    transition_dispatch(path, identity, "marker_succeeded", marker_comment_id=10)
    transition_dispatch(path, identity, "preparation_succeeded")

    recovered = load_dispatch_record(path, identity)
    assert recovered is not None
    with pytest.raises(ValueError, match="non-replayable local attempt capability"):
        assert_task_creation_allowed(path, recovered)

    forged = recovered.with_state("creating", attempt_capability="different-capability")
    with pytest.raises(ValueError, match="durably persisted creating marker"):
        assert_task_creation_allowed(path, forged)


def test_allows_pre_write_failure_before_capability_consumption(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 8, SHA, 1)
    create_intent(path, identity)
    transition_dispatch(path, identity, "marker_succeeded", marker_comment_id=10)
    creating = transition_dispatch(path, identity, "preparation_succeeded")

    assert assert_task_creation_allowed(path, creating)

    recovered = transition_dispatch(path, identity, "pre_write_failure")

    assert recovered.state.value == "reserved"
    assert recovered.retry_count == 1
