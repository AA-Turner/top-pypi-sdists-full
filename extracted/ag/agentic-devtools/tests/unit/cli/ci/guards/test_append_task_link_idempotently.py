from pathlib import Path
from typing import Any, cast

import pytest

from agentic_devtools.cli.ci.dispatch_state import (
    DispatchIdentity,
    consume_task_creation_capability,
    create_intent,
    transition_dispatch,
)
from agentic_devtools.cli.ci.guards import append_task_link_idempotently

SHA = "b" * 40


def _persist_created_record(path: Path, *, task_id: str = "44") -> DispatchIdentity:
    identity = DispatchIdentity("repo", 8, SHA, 1)
    create_intent(path, identity)
    transition_dispatch(path, identity, "marker_succeeded", marker_comment_id=10)
    creating = transition_dispatch(path, identity, "preparation_succeeded")
    consume_task_creation_capability(path, creating)
    transition_dispatch(path, identity, "task_created", task_id=task_id)
    return identity


def test_appends_exactly_one_task_link(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = _persist_created_record(path)
    body = append_task_link_idempotently(path, identity, "marker", "44")
    assert body == "marker\n\n#agent-task-44"
    assert append_task_link_idempotently(path, identity, body, "44") == body


def test_does_not_treat_substrings_as_existing_links(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = _persist_created_record(path)
    body = "marker\n\n#agent-task-444"

    assert append_task_link_idempotently(path, identity, body, "44").endswith("#agent-task-444\n\n#agent-task-44")


def test_rejects_invalid_inputs(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = _persist_created_record(path)
    for invalid in (None, True, 0, 1, "bad/id"):
        with pytest.raises(ValueError):
            append_task_link_idempotently(path, identity, "marker", cast(Any, invalid))
    with pytest.raises(ValueError):
        append_task_link_idempotently(path, identity, cast(Any, None), "44")


def test_requires_matching_persisted_created_record(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = _persist_created_record(path)
    with pytest.raises(ValueError, match="durably persisted created record"):
        append_task_link_idempotently(path, identity, "marker", "45")
    with pytest.raises(ValueError, match="durably persisted created record"):
        append_task_link_idempotently(path, identity, "marker", "044")
