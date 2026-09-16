"""Tests for non-dispatch trusted reconciliation command modes."""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.reconciliation.command import _handle_trusted_state_mode, reconcile_command
from agentic_devtools.cli.ci.reconciliation.models import (
    OperationStatus,
    QueueState,
    ReconciliationRecord,
    WorkItem,
    WorkItemStatus,
)
from agentic_devtools.cli.ci.reconciliation.queue_store import QueueStoreError


def _queue_state() -> QueueState:
    now = datetime(2026, 9, 15, 12, 0, tzinfo=UTC)
    item = WorkItem(
        pr_number=10,
        repo="owner/repo",
        change_id="sha-10",
        eligibility="eligible",
        due_at=now + timedelta(minutes=5),
        status=WorkItemStatus.QUEUED,
        last_observed_at=now,
        observation_watermark="sha-10",
        operation_status=OperationStatus.ACTIVE,
    )
    record = ReconciliationRecord(
        record_id="rec-1",
        repo="owner/repo",
        run_id="run-1",
        started_at=now,
        completed_at=now,
        provider_status="success",
        message="ok",
    )
    return QueueState(
        repo="owner/repo",
        revision=3,
        items={10: item},
        records=[record],
        quarantines=[],
        recovery_epoch=2,
    )


@patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
def test_inspect_inventory_mode_outputs_metadata(mock_store_cls, mock_create_provider, capsys) -> None:
    mock_store = MagicMock()
    mock_store.load.return_value = _queue_state()
    mock_store_cls.return_value = mock_store

    exit_code = reconcile_command(
        ["--workflow-id", "ai-pr-loop.yml", "--mode", "inspect-inventory", "--repo", "owner/repo", "--json-output"]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["mode"] == "inspect-inventory"
    assert payload["records"][0]["record_id"] == "owner/repo#10"
    mock_create_provider.assert_not_called()


@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
def test_inspect_runs_mode_returns_durable_run_records(mock_store_cls, capsys) -> None:
    mock_store = MagicMock()
    mock_store.load.return_value = _queue_state()
    mock_store_cls.return_value = mock_store

    exit_code = reconcile_command(["--workflow-id", "ai-pr-loop.yml", "--mode", "inspect-runs", "--json-output"])

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["mode"] == "inspect-runs"
    assert payload["runs"][0]["record_id"] == "rec-1"


@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
def test_inspect_ledger_mode_supports_record_filter(mock_store_cls, capsys) -> None:
    mock_store = MagicMock()
    mock_store.load.return_value = _queue_state()
    mock_store_cls.return_value = mock_store

    exit_code = reconcile_command(
        [
            "--workflow-id",
            "ai-pr-loop.yml",
            "--mode",
            "inspect-ledger",
            "--record-id",
            "owner/repo#10",
            "--json-output",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["mode"] == "inspect-ledger"
    assert payload["ledgers"][0]["record_id"] == "owner/repo#10"


@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
def test_inspection_modes_support_plain_output_and_non_matching_filters(mock_store_cls, capsys) -> None:
    mock_store = MagicMock()
    mock_store.load.return_value = _queue_state()
    mock_store_cls.return_value = mock_store

    assert (
        reconcile_command(
            [
                "--workflow-id",
                "ai-pr-loop.yml",
                "--mode",
                "inspect-inventory",
                "--record-id",
                "owner/repo#999",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["records"] == []

    assert (
        reconcile_command(
            [
                "--workflow-id",
                "ai-pr-loop.yml",
                "--mode",
                "inspect-ledger",
                "--record-id",
                "owner/repo#999",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["ledgers"] == []


@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
def test_inspect_inventory_reports_unknown_freshness(mock_store_cls, capsys) -> None:
    mock_store = MagicMock()
    state = _queue_state()
    item = replace(state.items[10], last_observed_at=None)
    mock_store.load.return_value = replace(state, items={10: item})
    mock_store_cls.return_value = mock_store

    assert reconcile_command(["--workflow-id", "ai-pr-loop.yml", "--mode", "inspect-inventory"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["records"][0]["observation_freshness_state"] == "unknown"


@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
def test_non_dispatch_mode_reports_queue_load_errors(mock_store_cls) -> None:
    mock_store = MagicMock()
    mock_store.load.side_effect = QueueStoreError("broken state")
    mock_store_cls.return_value = mock_store
    assert reconcile_command(["--workflow-id", "ai-pr-loop.yml", "--mode", "inspect-runs"]) == 1


@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
def test_restart_recovery_epoch_mode_requires_validation_inputs(mock_store_cls) -> None:
    mock_store = MagicMock()
    mock_store.load.return_value = _queue_state()
    mock_store_cls.return_value = mock_store

    assert reconcile_command(["--workflow-id", "ai-pr-loop.yml", "--mode", "restart-recovery-epoch"]) == 1


@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
def test_restart_recovery_epoch_mode_persists_advanced_epoch(mock_store_cls, capsys, monkeypatch) -> None:
    initial_state = _queue_state()
    monkeypatch.setenv("GITHUB_ACTOR", "ops-user")
    mock_store = MagicMock()
    mock_store.load.return_value = initial_state
    mock_store.save.side_effect = lambda updated, expected_revision: updated
    mock_store_cls.return_value = mock_store

    exit_code = reconcile_command(
        [
            "--workflow-id",
            "ai-pr-loop.yml",
            "--mode",
            "restart-recovery-epoch",
            "--actor",
            "ops-user",
            "--reason",
            "manual-recovery",
            "--prior-epoch",
            "2",
            "--no-late-write-confirmed",
            "--json-output",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["previous_recovery_epoch"] == 2
    assert payload["recovery_epoch"] == 3


@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
def test_restart_recovery_epoch_mode_requires_authenticated_actor(mock_store_cls, monkeypatch) -> None:
    mock_store = MagicMock()
    mock_store.load.return_value = _queue_state()
    mock_store_cls.return_value = mock_store
    monkeypatch.delenv("GITHUB_ACTOR", raising=False)

    assert (
        reconcile_command(
            [
                "--workflow-id",
                "ai-pr-loop.yml",
                "--mode",
                "restart-recovery-epoch",
                "--actor",
                "ops-user",
            ]
        )
        == 1
    )

    monkeypatch.setenv("GITHUB_ACTOR", "authenticated-user")
    assert (
        reconcile_command(
            [
                "--workflow-id",
                "ai-pr-loop.yml",
                "--mode",
                "restart-recovery-epoch",
                "--actor",
                "ops-user",
            ]
        )
        == 1
    )


@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
def test_restart_recovery_epoch_mode_validates_reason_prior_epoch_and_confirmation(mock_store_cls, monkeypatch) -> None:
    mock_store = MagicMock()
    mock_store.load.return_value = _queue_state()
    mock_store_cls.return_value = mock_store
    monkeypatch.setenv("GITHUB_ACTOR", "ops-user")

    assert (
        reconcile_command(
            [
                "--workflow-id",
                "ai-pr-loop.yml",
                "--mode",
                "restart-recovery-epoch",
                "--actor",
                "ops-user",
            ]
        )
        == 1
    )
    assert (
        reconcile_command(
            [
                "--workflow-id",
                "ai-pr-loop.yml",
                "--mode",
                "restart-recovery-epoch",
                "--actor",
                "ops-user",
                "--reason",
                "restart",
            ]
        )
        == 1
    )
    assert (
        reconcile_command(
            [
                "--workflow-id",
                "ai-pr-loop.yml",
                "--mode",
                "restart-recovery-epoch",
                "--actor",
                "ops-user",
                "--reason",
                "restart",
                "--prior-epoch",
                "2",
            ]
        )
        == 1
    )


@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
def test_restart_recovery_epoch_mode_rejects_prior_epoch_mismatch_and_active_work(mock_store_cls, monkeypatch) -> None:
    mock_store = MagicMock()
    state = _queue_state()
    mock_store.load.return_value = state
    mock_store_cls.return_value = mock_store
    monkeypatch.setenv("GITHUB_ACTOR", "ops-user")

    assert (
        reconcile_command(
            [
                "--workflow-id",
                "ai-pr-loop.yml",
                "--mode",
                "restart-recovery-epoch",
                "--actor",
                "ops-user",
                "--reason",
                "restart",
                "--prior-epoch",
                "1",
                "--no-late-write-confirmed",
            ]
        )
        == 1
    )

    active_item = state.items[10]
    state_with_active = QueueState(
        repo=state.repo,
        revision=state.revision,
        items={
            10: WorkItem(
                pr_number=active_item.pr_number,
                repo=active_item.repo,
                change_id=active_item.change_id,
                eligibility=active_item.eligibility,
                due_at=active_item.due_at,
                status=WorkItemStatus.CLAIMED,
                claimed_at=active_item.last_observed_at,
                claim_expires_at=active_item.due_at,
                claim_id="claim",
                operation_id="op",
            )
        },
        records=state.records,
        quarantines=state.quarantines,
        recovery_epoch=state.recovery_epoch,
    )
    mock_store.load.return_value = state_with_active
    assert (
        reconcile_command(
            [
                "--workflow-id",
                "ai-pr-loop.yml",
                "--mode",
                "restart-recovery-epoch",
                "--actor",
                "ops-user",
                "--reason",
                "restart",
                "--prior-epoch",
                "2",
                "--no-late-write-confirmed",
            ]
        )
        == 1
    )


@patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
def test_restart_recovery_epoch_mode_surfaces_save_errors(mock_store_cls, monkeypatch) -> None:
    mock_store = MagicMock()
    mock_store.load.return_value = _queue_state()
    mock_store.save.side_effect = QueueStoreError("save failed")
    mock_store_cls.return_value = mock_store
    monkeypatch.setenv("GITHUB_ACTOR", "ops-user")
    assert (
        reconcile_command(
            [
                "--workflow-id",
                "ai-pr-loop.yml",
                "--mode",
                "restart-recovery-epoch",
                "--actor",
                "ops-user",
                "--reason",
                "restart",
                "--prior-epoch",
                "2",
                "--no-late-write-confirmed",
            ]
        )
        == 1
    )


def test_handle_trusted_state_mode_rejects_unknown_mode() -> None:
    args = MagicMock()
    args.mode = "unknown"
    args.record_id = ""
    args.json_output = True
    assert _handle_trusted_state_mode(args, MagicMock(), _queue_state()) == 1
