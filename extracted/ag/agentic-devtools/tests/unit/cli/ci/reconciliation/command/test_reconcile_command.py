"""Tests for reconcile_command() CLI entry point."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from types import MappingProxyType
from unittest.mock import MagicMock, patch

import pytest

import agentic_devtools.cli.ci.reconciliation.config as cfg
from agentic_devtools.cli.ci.cooldown import CooldownRecord
from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.reconciliation.command import (
    _append_metric_event,
    _authoritative_rehydrate_loader,
    _build_live_eligibility_checker,
    _build_live_preflight_checker,
    _create_provider,
    _refresh_inventory,
    _was_unchanged_dispatch,
    reconcile_command,
)
from agentic_devtools.cli.ci.reconciliation.dispatch import DispatchResult
from agentic_devtools.cli.ci.reconciliation.models import (
    DispatchEligibility,
    Lease,
    MetricEvent,
    QueueState,
    ReconciliationAction,
    WorkItem,
    WorkItemStatus,
)
from agentic_devtools.cli.ci.reconciliation.queue_store import InMemoryBackingStore, QueueStore, QueueStoreError


class TestReconcileCommand:
    """Tests for reconcile_command() CLI entry point."""

    @pytest.mark.parametrize("recovery_token", [None, "corrupt-sha"])
    @patch("agentic_devtools.cli.ci.reconciliation.command.rehydrate_state")
    @patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_queue_load_error_rehydrates_before_dispatch(
        self, mock_create, mock_store_cls, mock_rehydrate, recovery_token
    ) -> None:
        """Queue load failures use bounded authoritative recovery before dispatch."""
        state = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])
        mock_store = MagicMock()
        mock_store.load.side_effect = QueueStoreError("corrupt state")
        mock_store.recovery_token.return_value = recovery_token
        mock_store_cls.return_value = mock_store
        mock_rehydrate.return_value = state

        reconcile_command(["--workflow-id", "ci.yml", "--repo", "owner/repo"])

        mock_rehydrate.assert_called_once()
        if recovery_token is None:
            mock_store.save_recovery.assert_not_called()
        else:
            mock_store.save_recovery.assert_called_once_with(state, recovery_token)

    @patch("agentic_devtools.cli.ci.reconciliation.command.rehydrate_state")
    @patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_stale_queue_state_rehydrates_before_dispatch(self, mock_create, mock_store_cls, mock_rehydrate) -> None:
        """Stale queue state uses bounded authoritative recovery before dispatch."""
        state = QueueState(
            repo="owner/repo",
            revision=0,
            items={},
            records=[],
            quarantines=[],
            last_updated_at=datetime.now(UTC) - timedelta(days=2),
        )
        mock_store = MagicMock()
        mock_store.load.return_value = state
        mock_store_cls.return_value = mock_store
        mock_rehydrate.return_value = state

        reconcile_command(["--workflow-id", "ci.yml", "--repo", "owner/repo"])

        mock_rehydrate.assert_called_once()

    def test_authoritative_rehydrate_loader_returns_forced_inventory(self) -> None:
        provider = MagicMock()
        provider.list_relevant_pull_requests.return_value = ([], None)
        store = MagicMock()
        store.save.side_effect = lambda state, expected_revision: state
        state = QueueState(repo="owner/repo", revision=2, items={}, records=[], quarantines=[])

        result = _authoritative_rehydrate_loader(provider, store, state, "owner/repo")

        assert result.full_scan_complete is True

    def test_authoritative_rehydrate_loader_rejects_unavailable_inventory(self) -> None:
        provider = MagicMock()
        provider.list_relevant_pull_requests.side_effect = RuntimeError("unavailable")
        store = MagicMock()
        state = QueueState(repo="owner/repo", revision=2, items={}, records=[], quarantines=[])

        with pytest.raises(RuntimeError, match="unavailable"):
            _authoritative_rehydrate_loader(provider, store, state, "owner/repo")

    @patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work")
    @patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_successful_no_action(self, mock_create, mock_store_cls, mock_dispatch) -> None:
        """Returns 0 when no due work is available."""
        mock_store = MagicMock()
        mock_store.load.return_value = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])
        mock_store_cls.return_value = mock_store
        mock_dispatch.return_value = DispatchResult(
            DispatchEligibility(0, "owner/repo", False, "no_due_work", None, False, ""),
            state=mock_store.load.return_value,
        )

        exit_code = reconcile_command(["--workflow-id", "ci.yml"])

        assert exit_code == 0
        mock_create.assert_called_once_with("github", "")
        mock_store_cls.assert_called_once_with(repo="")

    @patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work")
    @patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_json_output_for_dispatched_work(self, mock_create, mock_store_cls, mock_dispatch, capsys) -> None:
        """--json-output reports a dispatched lease."""
        now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
        lease = Lease(
            lease_id="lease-1",
            claim_id="claim-1",
            pr_number=42,
            repo="owner/repo",
            operation_id="operation-1",
            acquired_at=now,
            expires_at=now + timedelta(minutes=5),
        )
        mock_store = MagicMock()
        mock_store.load.return_value = QueueState(repo="owner/repo", revision=1, items={}, records=[], quarantines=[])
        mock_store_cls.return_value = mock_store
        mock_dispatch.return_value = DispatchResult(
            DispatchEligibility(42, "owner/repo", True, "eligible", lease.acquired_at, True, "due"),
            operation_id="operation-1",
            lease=lease,
            state=mock_store.load.return_value,
        )

        reconcile_command(["--workflow-id", "ci.yml", "--json-output"])

        output = json.loads(capsys.readouterr().out)
        assert output["action"] == ReconciliationAction.RETRIED.value
        assert output["lease_id"] == "lease-1"
        assert output["pr_number"] == 42
        mock_create.assert_called_once_with("github", "")

    @patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work")
    @patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_repeated_dispatch_records_unchanged_metric(self, mock_create, mock_store_cls, mock_dispatch) -> None:
        """Repeated dispatches of the same revision emit an unchanged metric."""
        now = datetime.now(UTC)
        lease = Lease(
            lease_id="lease-1",
            claim_id="claim-1",
            pr_number=42,
            repo="owner/repo",
            operation_id="operation-1",
            acquired_at=now,
            expires_at=now + timedelta(minutes=5),
        )
        item = WorkItem(
            pr_number=42,
            repo="owner/repo",
            change_id="sha-1",
            eligibility="eligible",
            due_at=now,
            status=WorkItemStatus.LEASED,
            claimed_at=now,
            claim_expires_at=lease.expires_at,
            claim_id=lease.claim_id,
            lease_id=lease.lease_id,
            lease_expires_at=lease.expires_at,
            operation_id=lease.operation_id,
        )
        prior_event = MetricEvent(
            event_id="event-1",
            event_type="dispatch_opportunity",
            repo="owner/repo",
            recorded_at=now,
            attributes=MappingProxyType({"pr_number": 42, "change_id": "sha-1"}),
        )
        state = QueueState(
            repo="owner/repo",
            revision=0,
            items={42: item},
            records=[],
            quarantines=[],
            metric_events=[prior_event],
            full_scan_complete=True,
            next_inventory_at=now + timedelta(hours=1),
        )
        mock_create.return_value = MagicMock()
        mock_store = MagicMock()
        mock_store.load.return_value = state
        mock_store_cls.return_value = mock_store
        mock_dispatch.return_value = DispatchResult(
            DispatchEligibility(42, "owner/repo", True, "eligible", now, True, "due"),
            operation_id=lease.operation_id,
            lease=lease,
            state=state,
        )

        reconcile_command(["--workflow-id", "ci.yml", "--repo", "owner/repo"])

        assert mock_store.save.call_count == 1
        saved_state = mock_store.save.call_args.args[0]
        assert saved_state.metric_events[-1].event_type == "unchanged_dispatch"

    @patch("agentic_devtools.cli.ci.reconciliation.command.active_cooldown")
    @patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work")
    @patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_active_cooldown_blocks_provider_work(
        self, mock_create, mock_store_cls, mock_dispatch, mock_active_cooldown, capsys
    ) -> None:
        """Returns no action without inventory or dispatch when a shared cooldown is active."""
        mock_create.return_value = MagicMock()
        mock_active_cooldown.return_value = (
            "github:SPECKIT_PR_TOKEN",
            CooldownRecord(resume_at=2_000_000_000, updated_at=1_000_000_000),
        )

        exit_code = reconcile_command(["--workflow-id", "ci.yml", "--json-output", "--repo", "owner/repo"])

        assert exit_code == 0
        assert json.loads(capsys.readouterr().out)["message"] == "Reconciliation blocked by provider cooldown."
        mock_store_cls.assert_not_called()
        mock_dispatch.assert_not_called()

    @patch(
        "agentic_devtools.cli.ci.reconciliation.command.active_cooldown",
        return_value=("github:GH_TOKEN", CooldownRecord(2_000_000_000)),
    )
    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider", return_value=MagicMock())
    def test_active_cooldown_plain_output(self, _mock_create, _mock_active_cooldown, capsys) -> None:
        """Reports a blocked reconciliation in plain-text mode."""
        assert reconcile_command(["--workflow-id", "ci.yml", "--repo", "owner/repo"]) == 0
        assert capsys.readouterr().out.strip() == "Reconciliation blocked by provider cooldown."

    @patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work")
    @patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_custom_params_are_accepted(self, mock_create, mock_store_cls, mock_dispatch) -> None:
        """Compatibility flags are parsed without altering durable dispatch."""
        state = QueueState(repo="org/repo", revision=0, items={}, records=[], quarantines=[])
        mock_store = MagicMock()
        mock_store.load.return_value = state
        mock_store_cls.return_value = mock_store
        mock_dispatch.return_value = DispatchResult(
            DispatchEligibility(0, "org/repo", False, "no_due_work", None, False, ""),
            state=state,
        )

        reconcile_command(
            [
                "--workflow-id",
                "speckit.yml",
                "--max-attempts",
                "5",
                "--window-hours",
                "48",
                "--repo",
                "org/repo",
            ]
        )

        mock_create.assert_called_once_with("github", "org/repo")
        mock_store_cls.assert_called_once_with(repo="org/repo")
        mock_dispatch.assert_called_once()

    @patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work")
    @patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_no_due_work_skips_live_eligibility_discovery(self, mock_create, mock_store_cls, mock_dispatch) -> None:
        """Stable no-op cycles avoid current-eligibility discovery when nothing is due."""
        provider = MagicMock()
        mock_create.return_value = provider
        state = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])
        mock_store = MagicMock()
        mock_store.load.return_value = state
        mock_store_cls.return_value = mock_store
        mock_dispatch.return_value = DispatchResult(
            DispatchEligibility(0, "owner/repo", False, "no_due_work", None, False, ""),
            state=state,
        )

        assert reconcile_command(["--workflow-id", "ci.yml", "--repo", "owner/repo"]) == 0

        provider.list_eligible_prs.assert_not_called()

    @patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work")
    @patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_verbose_flag_sets_debug_logging(self, mock_create, mock_store_cls, mock_dispatch) -> None:
        """--verbose flag still exercises the debug logging path."""
        state = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])
        mock_store = MagicMock()
        mock_store.load.return_value = state
        mock_store_cls.return_value = mock_store
        mock_dispatch.return_value = DispatchResult(
            DispatchEligibility(0, "owner/repo", False, "no_due_work", None, False, ""),
            state=state,
        )

        exit_code = reconcile_command(["--workflow-id", "ci.yml", "--verbose"])

        assert exit_code == 0
        mock_create.assert_called_once_with("github", "")

    @patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work")
    @patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_unknown_live_check_persists_operational_record(self, mock_create, mock_store_cls, mock_dispatch) -> None:
        """Unknown live checks persist an operational unknown outcome instead of a plain idle cycle."""
        state = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])
        mock_store = MagicMock()
        mock_store.load.return_value = state
        mock_store_cls.return_value = mock_store
        mock_dispatch.return_value = DispatchResult(
            DispatchEligibility(77, "owner/repo", False, "live_eligibility_unknown", datetime.now(UTC), True, "due"),
            state=state,
        )

        assert reconcile_command(["--workflow-id", "ci.yml"]) == 0

        saved_state = mock_store.save.call_args_list[-1].args[0]
        assert saved_state.records[-1].provider_status == "unknown"
        assert saved_state.records[-1].unknown_outcomes == (77,)
        assert saved_state.metric_events[-1].event_type == "provider_failure"

    @patch("agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work", side_effect=RuntimeError("API failure"))
    @patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_runtime_error_returns_1(self, mock_create, mock_store_cls, _mock_dispatch) -> None:
        """Returns 1 when durable dispatch raises RuntimeError."""
        mock_store = MagicMock()
        mock_store.load.return_value = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])
        mock_store_cls.return_value = mock_store

        exit_code = reconcile_command(["--workflow-id", "ci.yml"])

        assert exit_code == 1
        mock_create.assert_called_once_with("github", "")

    @patch(
        "agentic_devtools.cli.ci.reconciliation.command.dispatch_due_work",
        side_effect=ValueError("unexpected config error"),
    )
    @patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore")
    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_unexpected_exception_returns_1(self, mock_create, mock_store_cls, _mock_dispatch) -> None:
        """Returns 1 for unexpected exceptions not caught by RuntimeError/NotImplementedError."""
        mock_store = MagicMock()
        mock_store.load.return_value = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])
        mock_store_cls.return_value = mock_store

        exit_code = reconcile_command(["--workflow-id", "ci.yml"])

        assert exit_code == 1
        mock_create.assert_called_once_with("github", "")

    def test_ado_provider_returns_1(self) -> None:
        """Returns 1 immediately when provider is 'ado' (unsupported persistence)."""
        exit_code = reconcile_command(["--workflow-id", "ci.yml", "--provider", "ado"])

        assert exit_code == 1

    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_feature_flag_disabled_returns_no_action_json(self, mock_create, monkeypatch, capsys) -> None:
        """Disabled reconciliation skips provider creation and reports no_action."""
        monkeypatch.setattr(cfg, "ENABLE_RECONCILIATION", False)

        exit_code = reconcile_command(["--workflow-id", "ci.yml", "--json-output"])

        assert exit_code == 0
        mock_create.assert_not_called()
        output = json.loads(capsys.readouterr().out)
        assert output["action"] == ReconciliationAction.NO_ACTION.value
        assert "disabled" in output["message"].lower()

    @patch("agentic_devtools.cli.ci.reconciliation.command._create_provider")
    def test_feature_flag_disabled_prints_plain_message(self, mock_create, monkeypatch, capsys) -> None:
        """Disabled reconciliation also covers the plain-text output path."""
        monkeypatch.setattr(cfg, "ENABLE_RECONCILIATION", False)

        exit_code = reconcile_command(["--workflow-id", "ci.yml"])

        assert exit_code == 0
        mock_create.assert_not_called()
        assert "disabled" in capsys.readouterr().out.lower()

    def test_refresh_inventory_persists_changed_prs_and_live_checks(self) -> None:
        """Inventory observation persists a changed PR and checks current provider state."""
        provider = MagicMock()
        metadata = PRMetadata(42, "title", "feature", "sha-2", "main")
        provider.list_eligible_prs.return_value = [MagicMock(number=42)]
        provider.list_relevant_pull_requests.return_value = ([metadata], None)
        provider.get_pr_copilot_attribution.return_value = {"review": False, "push": True}
        provider.get_pr_metadata.return_value = metadata
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()

        refreshed = _refresh_inventory(provider, store, state, "owner/repo")

        assert refreshed.items[42].change_id == "sha-2"
        assert refreshed.items[42].due_at is not None
        assert _build_live_eligibility_checker(provider)(refreshed.items[42]) is True
        assert _build_live_preflight_checker(provider)(refreshed.items[42]) is True
        assert store.load().items[42] == refreshed.items[42]

    def test_live_eligibility_checker_ignores_cached_state(self) -> None:
        """Live eligibility checks the provider instead of cached queue eligibility."""
        provider = MagicMock()
        provider.list_eligible_prs.return_value = []
        item = WorkItem(42, "owner/repo", "sha-2", "eligible", None, WorkItemStatus.QUEUED)

        checker = _build_live_eligibility_checker(provider)

        assert checker(item) is False
        provider.list_eligible_prs.assert_called_once_with()

    def test_refresh_inventory_handles_pagination_and_records_observation(self) -> None:
        """Inventory observation skips duplicates and persists its observation timestamp."""
        provider = MagicMock()
        metadata = PRMetadata(42, "title", "feature", "sha-2", "main")
        existing = WorkItem(
            pr_number=42,
            repo="owner/repo",
            change_id="sha-2",
            eligibility="eligible",
            due_at=None,
            status=WorkItemStatus.QUEUED,
        )
        provider.list_eligible_prs.return_value = [MagicMock(number=42)]
        provider.list_relevant_pull_requests.side_effect = [([metadata], "next"), ([metadata], None)]
        provider.get_pr_copilot_attribution.return_value = {"review": False, "push": False}
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()
        state.items[42] = existing
        state = store.save(state, expected_revision=state.revision)

        refreshed = _refresh_inventory(provider, store, state, "owner/repo")

        assert refreshed.revision == state.revision + 1

    def test_refresh_inventory_handles_provider_failure(self) -> None:
        """Inventory failures leave the persisted queue unchanged."""
        provider = MagicMock()
        provider.list_eligible_prs.side_effect = RuntimeError("offline")
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()

        assert _refresh_inventory(provider, store, state, "owner/repo") is state

    def test_refresh_inventory_honors_pagination_limit(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Inventory observation stops after the configured page bound."""
        provider = MagicMock()
        metadata = PRMetadata(42, "title", "feature", "sha-2", "main")
        provider.list_eligible_prs.return_value = [MagicMock(number=42)]
        provider.list_relevant_pull_requests.return_value = ([metadata], "next")
        provider.get_pr_copilot_attribution.return_value = {"review": False, "push": True}
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        monkeypatch.setattr(cfg, "MAX_PAGINATION_PAGES_PER_RUN", 1)

        refreshed = _refresh_inventory(provider, store, store.load(), "owner/repo")

        assert refreshed.items[42].change_id == "sha-2"
        provider.list_relevant_pull_requests.assert_called_once()

    def test_refresh_inventory_returns_state_when_inventory_is_empty(self) -> None:
        """An empty inventory still persists the next observation schedule."""
        provider = MagicMock()
        provider.list_eligible_prs.return_value = []
        provider.list_relevant_pull_requests.return_value = ([], None)
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()

        refreshed = _refresh_inventory(provider, store, state, "owner/repo")

        assert refreshed is not state
        assert refreshed.next_inventory_at is not None

    def test_refresh_inventory_skips_stable_scan_until_next_observation(self) -> None:
        """Stable inventory scans are gated by the persisted observation schedule."""
        provider = MagicMock()
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()
        state.full_scan_complete = True
        state.next_inventory_at = datetime.now(UTC) + timedelta(hours=1)
        state.inventory_invalidated = False

        assert _refresh_inventory(provider, store, state, "owner/repo") is state
        provider.list_relevant_pull_requests.assert_not_called()
        provider.get_pr_copilot_attribution.assert_not_called()

    def test_refresh_inventory_trusted_event_observes_target_and_invalidates_next_scan(self) -> None:
        """Trusted-event runs observe the target PR immediately during a cache window."""
        provider = MagicMock()
        metadata = PRMetadata(42, "title", "feature", "sha-2", "main")
        provider.get_pr_metadata.return_value = metadata
        provider.get_pr_copilot_attribution.return_value = {"review": False, "push": True}
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()
        state.full_scan_complete = True
        state.next_inventory_at = datetime.now(UTC) + timedelta(hours=1)
        state.inventory_invalidated = False

        refreshed = _refresh_inventory(
            provider,
            store,
            state,
            "owner/repo",
            invalidate_inventory=True,
            trusted_pr_number=42,
            trusted_head_sha="sha-2",
        )

        assert refreshed.items[42].change_id == "sha-2"
        assert refreshed.items[42].due_at is not None
        assert refreshed.inventory_invalidated is True
        provider.get_pr_metadata.assert_called_once_with(42)
        provider.get_pr_copilot_attribution.assert_called_once_with(42, observation_watermark="")
        provider.list_relevant_pull_requests.assert_not_called()

    def test_refresh_inventory_trusted_event_continues_full_scan_without_cache_window(self) -> None:
        """Trusted-event reconciliation still performs the bounded inventory scan when needed."""
        provider = MagicMock()
        metadata = PRMetadata(42, "title", "feature", "sha-2", "main")
        provider.get_pr_metadata.return_value = metadata
        provider.get_pr_copilot_attribution.return_value = {"review": False, "push": True}
        provider.list_relevant_pull_requests.return_value = ([], None)
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())

        refreshed = _refresh_inventory(
            provider,
            store,
            store.load(),
            "owner/repo",
            trusted_pr_number=42,
            trusted_head_sha="sha-2",
        )

        assert refreshed.inventory_invalidated is False
        provider.list_relevant_pull_requests.assert_called_once_with(cursor=None)

    def test_refresh_inventory_trusted_event_head_mismatch_only_invalidates(self) -> None:
        """A stale trusted head invalidates the next scan without trusting outdated attribution."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value = PRMetadata(42, "title", "feature", "sha-new", "main")
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()
        state.full_scan_complete = True
        state.next_inventory_at = datetime.now(UTC) + timedelta(hours=1)

        refreshed = _refresh_inventory(
            provider,
            store,
            state,
            "owner/repo",
            trusted_pr_number=42,
            trusted_head_sha="sha-old",
        )

        assert refreshed.inventory_invalidated is True
        provider.get_pr_copilot_attribution.assert_not_called()

    def test_refresh_inventory_trusted_event_failure_still_invalidates(self) -> None:
        """A targeted-observation failure still persists the invalidation signal."""
        provider = MagicMock()
        provider.get_pr_metadata.side_effect = RuntimeError("offline")
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()
        state.full_scan_complete = True
        state.next_inventory_at = datetime.now(UTC) + timedelta(hours=1)

        refreshed = _refresh_inventory(
            provider,
            store,
            state,
            "owner/repo",
            trusted_pr_number=42,
            trusted_head_sha="sha-2",
        )

        assert refreshed.inventory_invalidated is True

    def test_refresh_inventory_trusted_event_updates_pending_change_for_inflight_item(self) -> None:
        """Trusted-event observation preserves in-flight ownership and records the new head."""
        provider = MagicMock()
        metadata = PRMetadata(42, "title", "feature", "sha-new", "main")
        provider.get_pr_metadata.return_value = metadata
        provider.get_pr_copilot_attribution.return_value = {"review": True}
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()
        state.items[42] = WorkItem(
            pr_number=42,
            repo="owner/repo",
            change_id="sha-old",
            eligibility="eligible",
            due_at=None,
            status=WorkItemStatus.CLAIMED,
            claim_id="claim-1",
            claim_expires_at=datetime.now(UTC) + timedelta(minutes=5),
            operation_id="operation-1",
        )
        state.full_scan_complete = True
        state.next_inventory_at = datetime.now(UTC) + timedelta(hours=1)
        state = store.save(state, expected_revision=state.revision)

        refreshed = _refresh_inventory(
            provider,
            store,
            state,
            "owner/repo",
            trusted_pr_number=42,
            trusted_head_sha="sha-new",
        )

        assert refreshed.items[42].status == WorkItemStatus.CLAIMED
        assert refreshed.items[42].pending_change_id == "sha-new"

    def test_refresh_inventory_returns_unchanged_incomplete_state(self) -> None:
        """An unchanged paginated cursor does not create a redundant revision."""
        provider = MagicMock()
        provider.list_relevant_pull_requests.return_value = ([], "next")
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()
        state.pagination_cursor = "next"

        assert _refresh_inventory(provider, store, state, "owner/repo") is state

    def test_refresh_inventory_persists_cursor_progress_without_pr_observations(self) -> None:
        """Pagination cursor advancement is persisted even when the page has no PRs."""
        provider = MagicMock()
        provider.list_relevant_pull_requests.return_value = ([], "next")
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()

        refreshed = _refresh_inventory(provider, store, state, "owner/repo")

        assert refreshed is not state
        assert refreshed.pagination_cursor == "next"
        assert store.load().pagination_cursor == "next"

    def test_refresh_inventory_marks_absent_non_inflight_items_ineligible_after_full_scan(self) -> None:
        """Completed full scans retire queue items no longer present in open inventory."""
        provider = MagicMock()
        metadata = PRMetadata(42, "title", "feature", "sha-2", "main")
        provider.list_relevant_pull_requests.return_value = ([metadata], None)
        provider.get_pr_copilot_attribution.return_value = {"review": False, "push": True}
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()
        state.items[7] = WorkItem(
            pr_number=7,
            repo="owner/repo",
            change_id="sha-7",
            eligibility="eligible",
            due_at=datetime.now(UTC),
            status=WorkItemStatus.QUEUED,
            last_observed_at=datetime.now(UTC) - timedelta(days=1),
        )
        state = store.save(state, expected_revision=state.revision)

        refreshed = _refresh_inventory(provider, store, state, "owner/repo")

        assert refreshed.items[7].eligibility == "ineligible"
        assert refreshed.items[7].due_at is None

    def test_refresh_inventory_does_not_retire_items_seen_earlier_in_paginated_scan(self, monkeypatch) -> None:
        """Final page completion keeps items observed in earlier pages of the same scan."""
        monkeypatch.setattr(cfg, "MAX_PAGINATION_PAGES_PER_RUN", 1)
        provider = MagicMock()
        page_one = PRMetadata(7, "first", "feature", "sha-7", "main")
        page_two = PRMetadata(42, "second", "feature", "sha-2", "main")
        provider.list_relevant_pull_requests.side_effect = [([page_one], "next"), ([page_two], None)]
        provider.get_pr_copilot_attribution.return_value = {"review": False, "push": False}
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())

        first_pass = _refresh_inventory(provider, store, store.load(), "owner/repo")
        second_pass = _refresh_inventory(provider, store, first_pass, "owner/repo")

        assert first_pass.inventory_scan_started_at is not None
        assert second_pass.items[7].eligibility == "eligible"
        assert second_pass.inventory_scan_started_at is None

    def test_refresh_inventory_sets_scan_start_for_legacy_incomplete_state(self) -> None:
        """Legacy states without scan-start metadata set it when cursor advances."""
        provider = MagicMock()
        provider.list_relevant_pull_requests.return_value = ([], "next-2")
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()
        state.pagination_cursor = "next-1"

        refreshed = _refresh_inventory(provider, store, state, "owner/repo")

        assert refreshed.pagination_cursor == "next-2"
        assert refreshed.inventory_scan_started_at is not None

    def test_refresh_inventory_keeps_absent_inflight_items_unchanged(self) -> None:
        """Absent items are not retired while still claimed or leased."""
        provider = MagicMock()
        metadata = PRMetadata(42, "title", "feature", "sha-2", "main")
        provider.list_relevant_pull_requests.return_value = ([metadata], None)
        provider.get_pr_copilot_attribution.return_value = {"review": False, "push": True}
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()
        state.items[7] = WorkItem(
            pr_number=7,
            repo="owner/repo",
            change_id="sha-7",
            eligibility="eligible",
            due_at=datetime.now(UTC),
            status=WorkItemStatus.CLAIMED,
            claimed_at=datetime.now(UTC),
            last_observed_at=datetime.now(UTC) - timedelta(days=1),
            claim_id="claim-1",
            claim_expires_at=datetime.now(UTC) + timedelta(minutes=5),
            operation_id="operation-1",
        )
        state = store.save(state, expected_revision=state.revision)

        refreshed = _refresh_inventory(provider, store, state, "owner/repo")

        assert refreshed.items[7].status == WorkItemStatus.CLAIMED
        assert refreshed.items[7].eligibility == "eligible"

    def test_refresh_inventory_does_not_rewrite_absent_already_ineligible_items(self) -> None:
        """Absent ineligible items with no due-at stay untouched when a scan completes."""
        provider = MagicMock()
        metadata = PRMetadata(42, "title", "feature", "sha-2", "main")
        provider.list_relevant_pull_requests.return_value = ([metadata], None)
        provider.get_pr_copilot_attribution.return_value = {"review": False, "push": True}
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        state = store.load()
        marker = datetime(2026, 1, 1, tzinfo=UTC)
        state.items[7] = WorkItem(
            pr_number=7,
            repo="owner/repo",
            change_id="sha-7",
            eligibility="ineligible",
            due_at=None,
            status=WorkItemStatus.QUEUED,
            last_observed_at=marker,
        )
        state = store.save(state, expected_revision=state.revision)

        refreshed = _refresh_inventory(provider, store, state, "owner/repo")

        assert refreshed.items[7].last_observed_at == marker


class TestPositiveInt:
    """Tests for _positive_int argparse type helper."""

    def test_valid_positive_integer(self) -> None:
        """Positive integer string is parsed correctly."""
        from agentic_devtools.cli.ci.reconciliation.command import _positive_int

        assert _positive_int("5") == 5

    def test_zero_raises_argument_type_error(self) -> None:
        """Zero raises ArgumentTypeError."""
        import argparse

        from agentic_devtools.cli.ci.reconciliation.command import _positive_int

        with pytest.raises(argparse.ArgumentTypeError, match="must be >= 1"):
            _positive_int("0")

    def test_negative_raises_argument_type_error(self) -> None:
        """Negative integer raises ArgumentTypeError."""
        import argparse

        from agentic_devtools.cli.ci.reconciliation.command import _positive_int

        with pytest.raises(argparse.ArgumentTypeError, match="must be >= 1"):
            _positive_int("-3")

    def test_non_integer_string_raises(self) -> None:
        """Non-integer string raises ArgumentTypeError."""
        import argparse

        from agentic_devtools.cli.ci.reconciliation.command import _positive_int

        with pytest.raises(argparse.ArgumentTypeError, match="not a valid integer"):
            _positive_int("abc")


class TestCreateProvider:
    """Tests for _create_provider helper."""

    @patch("agentic_devtools.cli.ci.github_provider.GitHubActionsProvider.__init__", return_value=None)
    def test_github_provider(self, _mock_init) -> None:
        """Creates a GitHubActionsProvider for 'github'."""
        from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

        provider = _create_provider("github", "org/repo")
        assert isinstance(provider, GitHubActionsProvider)

    @patch("agentic_devtools.cli.ci.ado_provider.AzureDevOpsProvider.__init__", return_value=None)
    def test_ado_provider(self, _mock_init) -> None:
        """Creates an AzureDevOpsProvider for 'ado'."""
        from agentic_devtools.cli.ci.ado_provider import AzureDevOpsProvider

        provider = _create_provider("ado", "")
        assert isinstance(provider, AzureDevOpsProvider)

    def test_unknown_provider_raises(self) -> None:
        """Raises ValueError for unknown provider name."""
        with pytest.raises(ValueError, match="Unknown provider"):
            _create_provider("unknown", "")


class TestWasUnchangedDispatch:
    """Tests for repeated dispatch detection."""

    def test_returns_false_without_a_prior_dispatch_for_the_pr(self) -> None:
        """A PR with no prior dispatch opportunity is not unchanged."""
        state = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])

        assert _was_unchanged_dispatch(state, 1, "sha-1") is False

    def test_retains_history_for_full_efficiency_comparison_period(self) -> None:
        """History includes more than the eight-day minimum at a 20-minute cadence."""
        events = [
            MetricEvent(
                event_id=f"event-{index}",
                event_type="idle_cycle",
                repo="owner/repo",
                recorded_at=datetime.now(UTC),
                attributes=MappingProxyType({}),
            )
            for index in range(576)
        ]
        state = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[], metric_events=events)

        updated = _append_metric_event(state, events[-1])

        assert len(updated.metric_events) == 577

    def test_skips_unrelated_metric_events_and_prs(self) -> None:
        """Only the latest dispatch opportunity for the requested PR is considered."""
        events = [
            MetricEvent(
                event_id="event-1",
                event_type="discovery_call",
                repo="owner/repo",
                recorded_at=datetime.now(UTC),
                attributes=MappingProxyType({}),
            ),
            MetricEvent(
                event_id="event-2",
                event_type="dispatch_opportunity",
                repo="owner/repo",
                recorded_at=datetime.now(UTC),
                attributes=MappingProxyType({"pr_number": 2, "change_id": "sha-2"}),
            ),
        ]
        state = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[], metric_events=events)

        assert _was_unchanged_dispatch(state, 1, "sha-1") is False

    def test_returns_true_for_the_same_revision(self) -> None:
        """A repeated dispatch of the same PR revision is unchanged."""
        event = MetricEvent(
            event_id="event-1",
            event_type="dispatch_opportunity",
            repo="owner/repo",
            recorded_at=datetime.now(UTC),
            attributes=MappingProxyType({"pr_number": 1, "change_id": "sha-1"}),
        )
        state = QueueState(
            repo="owner/repo",
            revision=0,
            items={},
            records=[],
            quarantines=[],
            metric_events=[event],
        )

        assert _was_unchanged_dispatch(state, 1, "sha-1") is True

    def test_returns_false_for_a_different_revision(self) -> None:
        """A dispatch after a PR revision changes is not unchanged."""
        event = MetricEvent(
            event_id="event-1",
            event_type="dispatch_opportunity",
            repo="owner/repo",
            recorded_at=datetime.now(UTC),
            attributes=MappingProxyType({"pr_number": 1, "change_id": "sha-1"}),
        )
        state = QueueState(
            repo="owner/repo",
            revision=0,
            items={},
            records=[],
            quarantines=[],
            metric_events=[event],
        )

        assert _was_unchanged_dispatch(state, 1, "sha-2") is False
