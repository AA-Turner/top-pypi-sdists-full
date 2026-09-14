import pytest

from agentic_devtools.cli.github.single_finding_dispatch import (
    AcceptancePersistenceError,
    AcceptedTaskIdentity,
    AmbiguousTaskCreationError,
    SingleFindingDispatchAdapter,
    SingleFindingDispatchResult,
    TaskAcceptance,
)


def test_adapter_rejects_expired_deadline_before_reserving(handoff, payload, fake_host):
    host = fake_host()
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 200)

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "budget_exhausted"
    assert host.calls == []


def test_adapter_blocks_when_branch_write_reservation_is_not_acquired(handoff, payload, fake_host):
    host = fake_host(reservation_result=False)
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "blocked"
    assert "reservation" in result.reason
    assert [name for name, _ in host.calls] == ["reserve"]


def test_adapter_rejects_mismatched_expected_head_without_task_write(handoff, payload, fake_host):
    host = fake_host(
        acceptance=TaskAcceptance(
            "head_changed",
            None,
            "current head differs from expected head",
        )
    )
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "head_changed"
    assert result.task_id is None
    assert [name for name, _ in host.calls] == ["reserve", "create"]


@pytest.mark.parametrize("field", ["base_ref", "head_ref"])
def test_adapter_rejects_payload_refs_not_bound_to_handoff(field, handoff, payload, fake_host):
    mismatched_payload = payload.__class__(
        prompt=payload.prompt,
        model=payload.model,
        base_ref="other" if field == "base_ref" else payload.base_ref,
        head_ref="other" if field == "head_ref" else payload.head_ref,
        custom_agent=payload.custom_agent,
        create_pull_request=payload.create_pull_request,
    )
    adapter = SingleFindingDispatchAdapter(fake_host(), clock=lambda: 100)

    with pytest.raises(ValueError, match="payload refs"):
        adapter.dispatch(handoff, mismatched_payload)


def test_adapter_rejects_payload_not_bound_to_selected_finding(handoff, payload, fake_host):
    mismatched_payload = payload.__class__(
        prompt="repair another finding",
        model=payload.model,
        base_ref=payload.base_ref,
        head_ref=payload.head_ref,
        custom_agent=payload.custom_agent,
        create_pull_request=payload.create_pull_request,
    )
    host = fake_host()
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    with pytest.raises(ValueError, match="payload digest"):
        adapter.dispatch(handoff, mismatched_payload)
    assert host.calls == []


def test_adapter_returns_already_resolved_without_persisting_or_returning_identity(handoff, payload, fake_host):
    host = fake_host(acceptance=TaskAcceptance("already_resolved", None, "thread was resolved concurrently"))
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "already_resolved"
    assert result.task_id is None
    assert result.session_id is None
    assert [name for name, _ in host.calls] == ["reserve", "create"]


def test_adapter_returns_blocked_without_persisting_or_returning_identity(handoff, payload, fake_host):
    host = fake_host(acceptance=TaskAcceptance("blocked", None, "thread lookup failed"))
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "blocked"
    assert result.task_id is None
    assert result.session_id is None
    assert [name for name, _ in host.calls] == ["reserve", "create"]


def test_adapter_persists_and_returns_accepted_task_and_session(handoff, payload, fake_host):
    identity = AcceptedTaskIdentity("task-1", "session-1")
    host = fake_host(acceptance=TaskAcceptance("accepted", identity, "accepted"))
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    result = adapter.dispatch(handoff, payload)

    assert result == SingleFindingDispatchResult(
        outcome="accepted",
        reason="accepted task identity persisted",
        expected_head="a" * 40,
        finding_id=handoff.finding_id,
        attempt_id="attempt-1",
        task_id="task-1",
        session_id="session-1",
    )
    assert [name for name, _ in host.calls] == ["reserve", "create", "persist"]
    assert host.timeouts == [("reserve", 100), ("create", 100), ("persist", 100)]


def test_adapter_reports_acceptance_unknown_when_persistence_fails(handoff, payload, fake_host):
    identity = AcceptedTaskIdentity("task-1", None)
    host = fake_host(
        acceptance=TaskAcceptance("accepted", identity, "accepted"),
        persistence_result=False,
    )
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "acceptance_unknown"
    assert result.task_id == "task-1"
    assert result.session_id is None


def test_adapter_normalizes_accepted_persistence_error(handoff, payload, fake_host, monkeypatch):
    identity = AcceptedTaskIdentity("task-1", "session-1")
    host = fake_host(acceptance=TaskAcceptance("accepted", identity, "accepted"))
    monkeypatch.setattr(
        host,
        "persist_acceptance",
        lambda *_: (_ for _ in ()).throw(AcceptancePersistenceError("storage timed out")),
    )
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "acceptance_unknown"
    assert result.reason == "storage timed out"
    assert result.task_id == "task-1"
    assert result.session_id == "session-1"


def test_adapter_normalizes_unknown_persistence_error(handoff, payload, fake_host, monkeypatch):
    identity = AcceptedTaskIdentity("task-1", "session-1")
    host = fake_host(acceptance=TaskAcceptance("unknown", identity, "provider response was ambiguous"))
    monkeypatch.setattr(
        host,
        "persist_acceptance",
        lambda *_: (_ for _ in ()).throw(AcceptancePersistenceError("storage unavailable")),
    )
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "acceptance_unknown"
    assert result.reason == "storage unavailable"
    assert result.task_id == "task-1"
    assert result.session_id == "session-1"


def test_adapter_reports_unknown_provider_acceptance(handoff, payload, fake_host):
    identity = AcceptedTaskIdentity("task-1", "session-1")
    host = fake_host(acceptance=TaskAcceptance("unknown", identity, "provider response was ambiguous"))
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "acceptance_unknown"
    assert result.task_id == "task-1"
    assert result.session_id == "session-1"
    assert [name for name, _ in host.calls] == ["reserve", "create", "persist"]


def test_adapter_maps_ambiguous_create_failure_to_unknown_acceptance(handoff, payload, fake_host):
    identity = AcceptedTaskIdentity("task-1", "session-1")
    host = fake_host(
        acceptance=AmbiguousTaskCreationError(
            "provider timed out after delivering the task",
            identity,
        )
    )
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "acceptance_unknown"
    assert result.reason == "provider timed out after delivering the task"
    assert result.task_id == "task-1"
    assert result.session_id == "session-1"
    assert [name for name, _ in host.calls] == ["reserve", "create", "persist"]


def test_adapter_reports_unknown_when_observed_identity_persistence_fails(handoff, payload, fake_host):
    identity = AcceptedTaskIdentity("task-1", None)
    host = fake_host(
        acceptance=TaskAcceptance("unknown", identity, "provider response was ambiguous"),
        persistence_result=False,
    )
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "acceptance_unknown"
    assert result.reason == "unknown task acceptance could not be persisted"
    assert result.task_id == "task-1"
    assert [name for name, _ in host.calls] == ["reserve", "create", "persist"]


def test_adapter_reports_unknown_when_unknown_acceptance_reaches_deadline_before_persistence(
    handoff, payload, fake_host
):
    identity = AcceptedTaskIdentity("task-1", "session-1")
    host = fake_host(acceptance=TaskAcceptance("unknown", identity, "provider response was ambiguous"))
    adapter = SingleFindingDispatchAdapter(host, clock=iter([100, 100, 200]).__next__)

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "acceptance_unknown"
    assert result.reason == "unknown task acceptance could not be persisted before deadline"
    assert result.task_id == "task-1"
    assert [name for name, _ in host.calls] == ["reserve", "create"]


def test_adapter_reports_unknown_when_accepted_identity_reaches_deadline_before_persistence(
    handoff, payload, fake_host
):
    identity = AcceptedTaskIdentity("task-1", "session-1")
    host = fake_host(acceptance=TaskAcceptance("accepted", identity, "accepted"))
    adapter = SingleFindingDispatchAdapter(host, clock=iter([100, 100, 200]).__next__)

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "acceptance_unknown"
    assert result.reason == "accepted task identity could not be persisted before deadline"
    assert result.task_id == "task-1"
    assert [name for name, _ in host.calls] == ["reserve", "create"]


def test_adapter_rejects_untyped_unknown_persistence_result(handoff, payload, fake_host, monkeypatch):
    host = fake_host(acceptance=TaskAcceptance("unknown", None, "provider response was ambiguous"))
    monkeypatch.setattr(host, "persist_acceptance", lambda *_: None)
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    with pytest.raises(TypeError, match="persist_acceptance"):
        adapter.dispatch(handoff, payload)


def test_adapter_stops_after_deadline_expires_while_reserved(handoff, payload, fake_host):
    times = iter([100, 200])
    host = fake_host()
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: next(times))

    result = adapter.dispatch(handoff, payload)

    assert result.outcome == "budget_exhausted"
    assert [name for name, _ in host.calls] == ["reserve"]


def test_adapter_validates_public_arguments(handoff, payload, fake_host):
    adapter = SingleFindingDispatchAdapter(fake_host(), clock=lambda: 100)

    with pytest.raises(TypeError, match="clock"):
        SingleFindingDispatchAdapter(fake_host(), clock=None)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="SingleFindingHandoff"):
        adapter.dispatch({}, payload)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="AgentTasksPayload"):
        adapter.dispatch(handoff, {})  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="clock"):
        SingleFindingDispatchAdapter(fake_host(), clock=lambda: 1.5).dispatch(handoff, payload)


def test_adapter_rejects_host_returning_an_untyped_acceptance(handoff, payload, fake_host):
    host = fake_host(acceptance=object())
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    with pytest.raises(TypeError, match="TaskAcceptance"):
        adapter.dispatch(handoff, payload)


@pytest.mark.parametrize("method", ["reserve_branch_write", "persist_acceptance"])
def test_adapter_rejects_hosts_returning_untyped_boolean(method, handoff, payload, fake_host, monkeypatch):
    host = fake_host(acceptance=None)
    if method == "reserve_branch_write":
        monkeypatch.setattr(host, method, lambda *_: None)
    else:
        identity = AcceptedTaskIdentity("task-1", None)
        host.acceptance = TaskAcceptance("accepted", identity, "accepted")
        monkeypatch.setattr(host, method, lambda *_: None)
    adapter = SingleFindingDispatchAdapter(host, clock=lambda: 100)

    with pytest.raises(TypeError, match=method):
        adapter.dispatch(handoff, payload)
