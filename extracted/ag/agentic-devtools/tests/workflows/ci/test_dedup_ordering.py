from pathlib import Path

import pytest

from agentic_devtools.cli.ci.dispatch_state import (
    DispatchIdentity,
    DispatchState,
    consume_task_creation_capability,
    create_intent,
    load_dispatch_record,
    record_remote_evidence,
    transition_dispatch,
)
from agentic_devtools.cli.ci.guards import (
    append_task_link_idempotently,
    assert_task_creation_allowed,
    build_dispatch_marker_comment,
    build_task_prompt_header,
)


class _FakeMarkerTransport:
    def __init__(self, events: list[str]) -> None:
        self.body = ""
        self._events = events

    def post(self, body: str) -> int:
        self._events.append("remote:marker_post")
        self.body = body
        return 9

    def edit(self, body: str) -> None:
        self._events.append("remote:marker_edit")
        self.body = body


class _FakeTaskTransport:
    def __init__(self, events: list[str]) -> None:
        self.prompt = ""
        self._events = events

    def post(self, prompt: str) -> str:
        self._events.append("remote:task_post")
        self.prompt = prompt
        return "task-9"


def _persisted_event(path: Path, identity: DispatchIdentity) -> str:
    record = load_dispatch_record(path, identity)
    assert record is not None
    if record.state is DispatchState.CREATING and record.attempt_capability_digest is None:
        return "persist:creating_capability_consumed"
    return f"persist:{record.state.value}"


def test_durable_records_interleave_persistence_with_remote_side_effects(tmp_path: Path) -> None:
    events: list[str] = []
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 3, "c" * 40, 1)
    marker_transport = _FakeMarkerTransport(events)
    task_transport = _FakeTaskTransport(events)
    create_intent(path, identity)
    events.append(_persisted_event(path, identity))

    marker_id = marker_transport.post(build_dispatch_marker_comment(identity))
    reserved = transition_dispatch(path, identity, "marker_succeeded", marker_comment_id=marker_id)
    assert reserved.state is DispatchState.RESERVED
    events.append(_persisted_event(path, identity))

    creating = transition_dispatch(path, identity, "preparation_succeeded")
    events.append(_persisted_event(path, identity))
    assert_task_creation_allowed(path, creating)
    consume_task_creation_capability(path, creating)
    events.append(_persisted_event(path, identity))

    task_id = task_transport.post(build_task_prompt_header(identity))
    transition_dispatch(path, identity, "task_created", task_id=task_id)
    events.append(_persisted_event(path, identity))

    marker_transport.edit(append_task_link_idempotently(path, identity, marker_transport.body, task_id))
    transition_dispatch(path, identity, "link_succeeded")
    events.append(_persisted_event(path, identity))

    assert events == [
        "persist:intent",
        "remote:marker_post",
        "persist:reserved",
        "persist:creating",
        "persist:creating_capability_consumed",
        "remote:task_post",
        "persist:created",
        "remote:marker_edit",
        "persist:linked",
    ]


def test_replayed_marker_intent_requires_reconciliation_before_retrying_marker(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 4, "d" * 40, 1)

    first = create_intent(path, identity)
    replayed = create_intent(path, identity)

    assert first.state is DispatchState.INTENT
    assert replayed.state is DispatchState.NEEDS_RECONCILIATION

    with pytest.raises(ValueError, match="not valid from 'needs_reconciliation'"):
        transition_dispatch(path, identity, "marker_succeeded", marker_comment_id=9)

    reset = transition_dispatch(path, identity, "reconcile_marker_miss")
    reserved = transition_dispatch(path, identity, "marker_succeeded", marker_comment_id=9)

    assert reset.state is DispatchState.INTENT
    assert reserved.state is DispatchState.RESERVED


def test_task_post_crash_window_requires_reconciliation_before_retry_or_link(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.json"
    identity = DispatchIdentity("repo", 5, "e" * 40, 1)

    create_intent(path, identity)
    transition_dispatch(path, identity, "marker_succeeded", marker_comment_id=9)
    creating = transition_dispatch(path, identity, "preparation_succeeded")

    assert assert_task_creation_allowed(path, creating)
    retryable = transition_dispatch(path, identity, "pre_write_failure")

    assert retryable.state is DispatchState.RESERVED

    creating = transition_dispatch(path, identity, "preparation_succeeded")
    assert assert_task_creation_allowed(path, creating)
    consume_task_creation_capability(path, creating)

    with pytest.raises(ValueError, match="capability consumption"):
        transition_dispatch(path, identity, "pre_write_failure")
    with pytest.raises(ValueError, match="durably persisted created record"):
        append_task_link_idempotently(path, identity, "marker", "task-9")

    uncertain = record_remote_evidence(path, identity, reason="timeout", evidence={"pages": 1}, event="task_uncertain")
    created = transition_dispatch(path, identity, "reconcile_task_unique", task_id="task-9")
    body = append_task_link_idempotently(path, identity, "marker", "task-9")

    assert uncertain.state is DispatchState.NEEDS_RECONCILIATION
    assert created.state is DispatchState.CREATED
    assert body == "marker\n\n#agent-task-task-9"
