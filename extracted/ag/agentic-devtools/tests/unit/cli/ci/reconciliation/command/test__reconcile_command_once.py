"""Tests for _reconcile_command_once()."""

from __future__ import annotations

import json
import logging
from dataclasses import replace
from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest

import agentic_devtools.cli.ci.reconciliation.dispatch as dispatch_module
from agentic_devtools.cli.ci.agent_task_inventory import (
    AgentTaskInventoryAvailability,
    AgentTaskInventoryLoadResult,
    FailureCategory,
)
from agentic_devtools.cli.ci.exceptions import ProviderRateLimitError
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.reconciliation.command import _reconcile_command_once, reconcile_command
from agentic_devtools.cli.ci.reconciliation.contention import QueueTransitionRetryExhaustedError
from agentic_devtools.cli.ci.reconciliation.models import OperationStatus, QueueState, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import ConcurrentModificationError, QueueStoreError
from tests.unit.cli.ci.reconciliation.command.test_reconcile_command import _make_leased_dispatch


def _reclaimed_item(item: WorkItem) -> WorkItem:
    return replace(
        item,
        status=WorkItemStatus.QUEUED,
        claim_id="",
        lease_id="",
        lease_expires_at=None,
        claim_expires_at=None,
        claimed_at=None,
        operation_status=OperationStatus.EXPIRED,
    )


def _session_state_for_inventory_scenario(scenario: str) -> SessionState:
    failed = scenario == "http-500"
    session_downgrade = scenario.startswith("session-downgrade")
    category = (
        FailureCategory.PROVIDER_UNAVAILABLE
        if failed
        else FailureCategory.MALFORMED_RESPONSE
        if scenario == "session-downgrade"
        else None
    )
    return SessionState(
        SessionOutcome.ACTIVE
        if scenario == "known-active-writer"
        else SessionOutcome.UNKNOWN
        if session_downgrade
        else SessionOutcome.NONE,
        inventory_availability=(
            AgentTaskInventoryAvailability.UNAVAILABLE
            if failed or session_downgrade
            else AgentTaskInventoryAvailability.COMPLETE
        ),
        failure_category=category,
        http_status=500 if failed else 503 if session_downgrade else None,
        failure_source=(
            "captured-inventory-source" if failed else "lifecycle-session-source" if session_downgrade else None
        ),
    )


@pytest.mark.parametrize("is_rate_limit", [True, False])
def test_entrypoint_classifies_only_typed_rate_limits(is_rate_limit, capsys, caplog) -> None:
    """The entrypoint only returns neutral deferred output for true classifications."""
    with patch(
        "agentic_devtools.cli.ci.reconciliation.command._create_provider",
        side_effect=ProviderRateLimitError(is_rate_limit=is_rate_limit),
    ):
        assert reconcile_command(["--workflow-id", "ai-pr-loop.yml", "--json-output"]) == (0 if is_rate_limit else 1)
    output = capsys.readouterr().out
    if is_rate_limit:
        assert json.loads(output)["action"] == "deferred"
        assert "Unexpected reconciliation error" not in caplog.text
    else:
        assert output == ""
        assert "Unexpected reconciliation error" in caplog.text


@pytest.mark.parametrize(
    ("is_rate_limit", "fence_failure"),
    [
        (True, None),
        (True, "load"),
        (True, "save"),
        (True, "conflict"),
        (True, "unexpected"),
        (False, None),
        (False, "load"),
        (False, "save"),
        (False, "conflict"),
    ],
)
@patch("agentic_devtools.cli.ci.reconciliation.command._release_dispatch_lease")
@patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work")
@patch("agentic_devtools.cli.ci.reconciliation.command._refresh_inventory")
@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
@patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
def test_rate_limit_after_dispatch_preserves_unknown_outcome(
    mock_create,
    mock_store_cls,
    mock_refresh,
    mock_dispatch,
    mock_release,
    fence_failure,
    is_rate_limit,
    monkeypatch,
    tmp_path,
    capsys,
    caplog,
) -> None:
    """Deferred success requires durable fencing; unrelated exhaustion still fails."""
    lease, state, dispatch = _make_leased_dispatch()
    monkeypatch.setenv("AGDT_STATE_DIR", str(tmp_path))
    store = mock_store_cls.return_value
    store.load.return_value = state
    mock_refresh.return_value = state
    mock_dispatch.return_value = dispatch
    provider = mock_create.return_value
    provider.get_pr_metadata.return_value.head_sha = "a" * 40
    provider.dispatch_workflow.side_effect = ProviderRateLimitError(is_rate_limit=is_rate_limit)
    if fence_failure == "load":
        store.load.side_effect = [state, QueueStoreError("fence load failed")]
    elif fence_failure == "save":
        store.save_alert.side_effect = QueueStoreError("fence save failed")
    elif fence_failure == "conflict":
        store.save_alert.side_effect = ConcurrentModificationError("fence conflict")
    elif fence_failure == "unexpected":
        store.load.side_effect = [state, ValueError("unexpected fence failure")]
    if fence_failure not in {"load", "save", "conflict", "unexpected"}:

        def persist_alert_and_capture_readback(alerted_state, **kwargs):
            assert capsys.readouterr().out == ""
            store.load.side_effect = None
            store.load.return_value = alerted_state

        store.save_alert.side_effect = persist_alert_and_capture_readback

    with caplog.at_level(logging.INFO):
        status = reconcile_command(["--workflow-id", "ai-pr-loop.yml", "--repo", "owner/repo", "--json-output"])

    deferred = is_rate_limit and fence_failure is None
    assert status == (0 if deferred else 1)
    provider.dispatch_workflow.assert_called_once()
    mock_release.assert_not_called()
    store.save.assert_not_called()
    if fence_failure not in {"load", "unexpected"}:
        fenced = store.save_alert.call_args.args[0]
        assert fenced.items[42].status == WorkItemStatus.UNKNOWN
        assert fenced.items[42].lease_id == lease.lease_id
        assert fenced.records[-1].unknown_outcomes == (42,)
    output = capsys.readouterr().out
    if deferred:
        payload = json.loads(output)
        assert payload["action"] == "deferred"
        assert payload["pr_number"] == 42
        assert "dispatch outcome remains unknown" in payload["message"]
        assert all(record.levelno < logging.ERROR for record in caplog.records)
    else:
        assert output == ""
        assert any(record.levelno == logging.ERROR for record in caplog.records)


def test_reclaimed_queued_item_does_not_emit_deferred_success(monkeypatch, tmp_path, capsys, caplog) -> None:
    """A reclaimed queued winner is preserved and blocks deferred success."""
    _lease, state, dispatch = _make_leased_dispatch()
    reclaimed_item = _reclaimed_item(state.items[42])
    reclaimed_state = replace(state, items={42: reclaimed_item})
    store = MagicMock()
    store.load.side_effect = [state, reclaimed_state]

    def persist_alert_and_capture_readback(alerted_state, **kwargs) -> None:
        store.load.side_effect = None
        store.load.return_value = alerted_state

    store.save_alert.side_effect = persist_alert_and_capture_readback
    provider = MagicMock()
    provider.get_pr_metadata.return_value.head_sha = "a" * 40
    provider.dispatch_workflow.side_effect = ProviderRateLimitError(is_rate_limit=True)
    monkeypatch.setenv("AGDT_STATE_DIR", str(tmp_path))

    with (
        patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore", return_value=store),
        patch("agentic_devtools.cli.ci.reconciliation.command._create_provider", return_value=provider),
        patch("agentic_devtools.cli.ci.reconciliation.command._refresh_inventory", return_value=state),
        patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work", return_value=dispatch),
        patch("agentic_devtools.cli.ci.reconciliation.command._release_dispatch_lease") as release_lease,
        caplog.at_level(logging.INFO),
    ):
        status = reconcile_command(["--workflow-id", "ai-pr-loop.yml", "--repo", "owner/repo", "--json-output"])

    assert status == 1
    release_lease.assert_not_called()
    assert store.save_alert.call_args.args[0].items[42] == reclaimed_item
    assert [item.pr_number for item in dispatch_module.select_due_work(store.save_alert.call_args.args[0])] == [42]
    assert "does not fence unknown dispatch" in caplog.text
    assert capsys.readouterr().out == ""


@patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work")
@patch("agentic_devtools.cli.ci.reconciliation.command._refresh_inventory")
@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
@patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
@patch("agentic_devtools.cli.ci.reconciliation.command.active_cooldown", return_value=False)
def test_reconcile_command_once_fails_on_exhausted_dispatch_cas(
    _mock_cooldown,
    _mock_create_provider,
    mock_store_class,
    mock_refresh_inventory,
    mock_dispatch,
    tmp_path,
    monkeypatch,
    caplog,
) -> None:
    """An exhausted dispatch CAS retry budget is reported as a command failure."""
    state = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])
    mock_store = MagicMock()
    mock_store.load.return_value = state
    mock_store_class.return_value = mock_store
    mock_refresh_inventory.return_value = state
    mock_dispatch.side_effect = dispatch_module.DispatchRetryExhaustedError("retry budget of 1 exhausted: conflict")
    monkeypatch.setenv("AGDT_STATE_DIR", str(tmp_path))

    with caplog.at_level(logging.ERROR):
        result = _reconcile_command_once(["--workflow-id", "ai-pr-loop.yml", "--repo", "owner/repo"])

    assert result == 1
    assert "Dispatch queue CAS retry budget exhausted" in caplog.text
    assert "retry budget of 1 exhausted: conflict" in caplog.text


@patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work")
@patch("agentic_devtools.cli.ci.reconciliation.command._refresh_inventory")
@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
@patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
@patch("agentic_devtools.cli.ci.reconciliation.command.active_cooldown", return_value=False)
def test_exhausted_dispatch_cas_is_deferred_for_confirmed_winner(
    _mock_cooldown,
    _mock_create_provider,
    mock_store_class,
    mock_refresh_inventory,
    mock_dispatch,
    tmp_path,
    monkeypatch,
    capsys,
) -> None:
    """A trusted event defers only after reloading its matching due queue row."""
    item = WorkItem(42, "owner/repo", "head-1", "eligible", datetime.now(UTC), WorkItemStatus.QUEUED)
    state = QueueState(repo="owner/repo", revision=1, items={42: item}, records=[], quarantines=[])
    store = mock_store_class.return_value
    store.load.return_value = state
    mock_refresh_inventory.return_value = state
    mock_dispatch.side_effect = dispatch_module.DispatchRetryExhaustedError(
        "retry budget exhausted",
        pr_number=42,
        change_id="head-1",
        operation_id=dispatch_module.derive_dispatch_operation_id(item),
    )
    monkeypatch.setenv("AGDT_STATE_DIR", str(tmp_path))

    result = _reconcile_command_once(
        [
            "--workflow-id",
            "ai-pr-loop.yml",
            "--repo",
            "owner/repo",
            "--trusted-pr-number",
            "42",
            "--trusted-head-sha",
            "head-1",
            "--json-output",
        ]
    )

    assert result == 0
    assert json.loads(capsys.readouterr().out)["action"] == "deferred"
    assert store.load.call_count == 2


@patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work")
@patch("agentic_devtools.cli.ci.reconciliation.command._refresh_inventory")
@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
@patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
@patch("agentic_devtools.cli.ci.reconciliation.command.active_cooldown", return_value=False)
def test_typed_transition_exhaustion_is_deferred_only_for_confirmed_due_work(
    _mock_cooldown,
    _mock_create_provider,
    mock_store_class,
    mock_refresh_inventory,
    mock_dispatch,
    tmp_path,
    monkeypatch,
    capsys,
) -> None:
    """Typed pre-dispatch exhaustion uses the winner while generic failures still fail."""
    item = WorkItem(42, "owner/repo", "head-1", "eligible", datetime.now(UTC), WorkItemStatus.QUEUED)
    state = QueueState(repo="owner/repo", revision=1, items={42: item}, records=[], quarantines=[])
    store = mock_store_class.return_value
    store.load.return_value = state
    mock_refresh_inventory.side_effect = QueueTransitionRetryExhaustedError(
        "exhausted", operation_id=dispatch_module.derive_dispatch_operation_id(item)
    )
    monkeypatch.setenv("AGDT_STATE_DIR", str(tmp_path))

    args = [
        "--workflow-id",
        "ai-pr-loop.yml",
        "--repo",
        "owner/repo",
        "--trusted-pr-number",
        "42",
        "--trusted-head-sha",
        "head-1",
        "--json-output",
    ]
    assert _reconcile_command_once(args) == 0
    assert json.loads(capsys.readouterr().out)["action"] == "deferred"
    assert store.load.call_count == 2
    mock_dispatch.assert_not_called()

    mock_refresh_inventory.side_effect = RuntimeError("unrelated runtime failure")
    assert _reconcile_command_once(args) == 1
    assert capsys.readouterr().out == ""


def _assert_inventory_dispatch_control(scenario, dispatch, payload, item):
    """Only complete evidence with matching-head preflight may reach dispatch."""
    if scenario == "fresh-complete-matching-head":
        dispatch.assert_called_once_with(
            "ai-pr-loop.yml",
            {"pr_number": "42", "head_sha": item.change_id, "operation_id": payload["operation_id"]},
        )
        assert payload["action"] == "retried"
        assert payload["pr_number"] == item.pr_number
        assert payload["lease_id"]
    else:
        dispatch.assert_not_called()


def _assert_inventory_diagnostics(
    scenario, payload, summary, item, metadata, checker, store, failed, partial, session_category
):
    session_downgrade = scenario.startswith("session-downgrade")
    unknown = scenario in {
        "timeout",
        "http-500",
        "partial-with-rows-and-eligible-members",
        "session-downgrade",
        "session-downgrade-without-category",
    }
    expected_source = (
        "captured-inventory-source" if failed else "lifecycle-session-source" if session_downgrade else None
    )
    expected_reason = (
        "page_failed" if failed else session_category.value if session_category else "page_limit" if partial else None
    )
    assert payload["inventory_status"] == ("unknown" if unknown else "complete")
    assert payload["inventory_source"] == expected_source
    assert payload["inventory_reason"] == expected_reason
    assert payload["inventory_http_status"] == (500 if failed else 503 if session_downgrade else None)
    assert payload["inventory_failure_category"] == (
        FailureCategory.PROVIDER_UNAVAILABLE if failed else session_category
    )
    assert payload["inventory_row_count"] == (None if scenario == "timeout" else 1 if partial else 0)
    assert payload["inventory_availability"] == ("partial" if partial else "unavailable" if unknown else "complete")
    summary_text = summary.read_text()
    for key in (
        "inventory_status",
        "inventory_source",
        "inventory_reason",
        "inventory_http_status",
        "inventory_failure_category",
    ):
        assert f"{key}: {payload[key] if payload[key] is not None else 'unknown'}" in summary_text
    if unknown:
        assert metadata.head_sha == item.change_id
        if not session_downgrade:
            assert checker.call_args.args[0] == frozenset({42})
        assert "blocked" in payload["message"]
        assert "No due reconciliation work found" not in payload["message"]
        assert store.load().items[42].status is WorkItemStatus.QUEUED


@pytest.mark.parametrize(
    "scenario",
    [
        "timeout",
        "http-500",
        "partial-with-rows-and-eligible-members",
        "session-downgrade",
        "session-downgrade-without-category",
        "complete-empty",
        "known-active-writer",
        "fresh-complete-changed-head",
        "fresh-complete-matching-head",
        "no-due-work",
    ],
)
def test_inventory_diagnostic_is_emitted_in_json_and_summary(scenario, monkeypatch, tmp_path, capsys):
    """The actual provider scan blocks unknown inventories and exports same-scan facts."""
    from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
    from agentic_devtools.cli.ci.models import PRMetadata
    from agentic_devtools.cli.ci.reconciliation.inventory_diagnostics import LiveEligibilityChecker
    from agentic_devtools.cli.ci.reconciliation.queue_store import InMemoryBackingStore, QueueStore

    now = datetime.now(UTC)
    item = WorkItem(42, "owner/repo", "head-1", "eligible", now, WorkItemStatus.QUEUED)
    state = QueueState("owner/repo", 0, {} if scenario == "no-due-work" else {42: item}, [], [])
    store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
    state = store.save(state, expected_revision=0)
    provider = GitHubActionsProvider(repo="owner/repo")
    summary = tmp_path / "summary"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    monkeypatch.setenv("AGDT_STATE_DIR", str(tmp_path))
    partial = scenario == "partial-with-rows-and-eligible-members"
    failed = scenario == "http-500"
    session_downgrade = scenario.startswith("session-downgrade")
    session_category = (
        FailureCategory.MALFORMED_RESPONSE
        if session_downgrade and scenario != "session-downgrade-without-category"
        else None
    )
    inventory = AgentTaskInventoryLoadResult(
        tasks=({"id": "partial-row"},) if partial else (),
        complete=not (partial or failed),
        incomplete_reasons=("page_failed",) if failed else ("page_limit",) if partial else (),
        failure_category=FailureCategory.PROVIDER_UNAVAILABLE if failed else None,
        http_status=500 if failed else None,
    )
    node = {
        "number": 42,
        "databaseId": 123,
        "createdAt": "2024-01-01T00:00:00Z",
        "headRefName": "feature/test",
        "headRefOid": "head-1",
        "title": "[WIP] Feature" if scenario == "complete-empty" else "Feature",
        "changedFiles": 1,
        "labels": {"nodes": [{"name": "ai-auto-merge-allowed"}]},
    }
    response = json.dumps(
        {"data": {"repository": {"pullRequests": {"nodes": [node], "pageInfo": {"hasNextPage": False}}}}}
    )
    metadata = PRMetadata(
        42,
        "Feature",
        "feature/test",
        "changed-head" if scenario == "fresh-complete-changed-head" else item.change_id,
        "main",
    )
    with (
        patch("agentic_devtools.cli.ci.reconciliation.command._create_provider", return_value=provider),
        patch("agentic_devtools.cli.ci.reconciliation.command.active_cooldown", return_value=False),
        patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore", return_value=store),
        patch("agentic_devtools.cli.ci.reconciliation.command._refresh_inventory", return_value=state),
        patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=response),
        patch(
            "agentic_devtools.cli.ci.reconciliation.inventory_diagnostics.LiveEligibilityChecker",
            wraps=LiveEligibilityChecker,
        ) as checker,
        patch(
            "agentic_devtools.cli.ci.pipeline.session_detector.get_latest_session_state",
            return_value=_session_state_for_inventory_scenario(scenario),
        ),
        patch.object(
            provider,
            "_list_agent_task_inventory",
            return_value=inventory,
            side_effect=TimeoutError() if scenario == "timeout" else None,
        ) as load,
        patch.object(provider, "get_pr_metadata", return_value=metadata),
        patch.object(provider, "dispatch_workflow") as dispatch,
    ):
        assert (
            _reconcile_command_once(["--workflow-id", "ai-pr-loop.yml", "--repo", "owner/repo", "--json-output"]) == 0
        )
    payload = json.loads(capsys.readouterr().out)
    _assert_inventory_dispatch_control(scenario, dispatch, payload, item)
    if scenario == "no-due-work":
        load.assert_not_called()
        assert "inventory_status" not in payload
        assert not summary.exists()
        return
    load.assert_called_once()
    _assert_inventory_diagnostics(
        scenario, payload, summary, item, metadata, checker, store, failed, partial, session_category
    )
