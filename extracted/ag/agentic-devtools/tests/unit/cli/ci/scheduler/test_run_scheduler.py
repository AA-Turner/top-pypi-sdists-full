"""Tests for run_scheduler orchestration."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.cooldown import CooldownRecord
from agentic_devtools.cli.ci.scheduler import EligiblePR, run_scheduler
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _make_provider(
    *,
    eligible: list[EligiblePR] | None = None,
    cursor_var: str | None = None,
    batch_var: str | None = None,
    pool_var: str | None = None,
    cooldown_var: str | None = None,
    token_valid: bool = False,
    dispatch_side_effect: Exception | None = None,
    set_variable_side_effect: Exception | None = None,
) -> MagicMock:
    """Create a mock provider with configurable behavior."""
    provider = MagicMock()
    provider.validate_variable_token.return_value = token_valid
    provider.list_eligible_prs.return_value = eligible or []
    provider.get_recent_dispatch_history.return_value = []

    def get_var(name: str, *, use_writer_token: bool = False) -> str | None:
        if name == "AI_PR_LOOP_LAST_DISPATCHED_PR":
            return cursor_var
        if name == "AI_PR_LOOP_DISPATCH_BATCH_SIZE":
            return batch_var
        if name == "AI_PR_LOOP_ELIGIBLE_PR_LIMIT":
            return pool_var
        if name == "AI_PR_LOOP_PROVIDER_COOLDOWNS":
            return cooldown_var
        return None

    provider.get_variable.side_effect = get_var

    if dispatch_side_effect:
        provider.dispatch_workflow.side_effect = dispatch_side_effect
    if set_variable_side_effect:
        provider.set_variable.side_effect = set_variable_side_effect

    return provider


class TestRunScheduler:
    """Tests for the run_scheduler orchestration function."""

    @patch.dict("os.environ", {}, clear=False)
    def test_happy_path_dispatch_and_persist(self) -> None:
        eligible = [
            EligiblePR(number=2020, created_at="2024-01-01"),
            EligiblePR(number=2021, created_at="2024-01-02"),
            EligiblePR(number=2022, created_at="2024-01-03"),
        ]
        provider = _make_provider(eligible=eligible, cursor_var="2020", token_valid=True, pool_var="10")

        result = run_scheduler(provider)

        assert result.run_mode == "live"
        assert result.dispatched_count == 1
        assert result.dispatched_prs == [2021]
        assert result.cursor_after == 2021
        assert result.had_dispatch_error is False
        provider.dispatch_workflow.assert_called_once_with(
            workflow="ai-pr-loop.yml",
            inputs={"pr_number": "2021", "trigger_reason": "scheduler_round_robin"},
        )
        provider.set_variable.assert_called_once_with("AI_PR_LOOP_LAST_DISPATCHED_PR", "2021")

    @patch.dict("os.environ", {}, clear=False)
    def test_no_eligible_prs_early_exit(self) -> None:
        provider = _make_provider(eligible=[])

        result = run_scheduler(provider)

        assert result.dispatched_count == 0
        assert result.dispatched_prs == []
        assert result.eligible_count == 0
        provider.dispatch_workflow.assert_not_called()

    @patch("agentic_devtools.cli.ci.scheduler.active_cooldown")
    @patch.dict("os.environ", {}, clear=False)
    def test_active_provider_cooldown_pauses_without_advancing_cursor(self, mock_active) -> None:
        mock_active.return_value = (
            "github:GH_TOKEN",
            CooldownRecord(resume_at=200, source="retry-after", updated_at=100),
        )
        provider = _make_provider(
            eligible=[EligiblePR(number=2020, created_at="2024-01-01")],
            cursor_var="2019",
        )

        with patch("agentic_devtools.cli.ci.scheduler.time.time", return_value=150):
            result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cooldown_key == "github:GH_TOKEN"
        assert result.cursor_persisted is False
        provider.list_eligible_prs.assert_not_called()
        provider.dispatch_workflow.assert_not_called()
        provider.set_variable.assert_not_called()

    @patch("agentic_devtools.cli.ci.scheduler.active_cooldown")
    @patch("agentic_devtools.cli.ci.scheduler.persist_cooldown", return_value=None)
    @patch.dict("os.environ", {}, clear=False)
    def test_rate_limit_during_cooldown_gate_pauses_scheduler(self, _mock_persist_cooldown, mock_active) -> None:
        mock_active.side_effect = ProviderRateLimitError(provider="github", source="retry-after", is_rate_limit=True)
        provider = _make_provider()

        result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cooldown_source == "retry-after"
        provider.validate_variable_token.assert_not_called()
        provider.list_eligible_prs.assert_not_called()

    @patch("agentic_devtools.cli.ci.scheduler.active_cooldown")
    @patch.dict("os.environ", {}, clear=False)
    def test_non_rate_limit_during_cooldown_gate_is_propagated(self, mock_active) -> None:
        mock_active.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=False)
        provider = _make_provider()

        with pytest.raises(ProviderRateLimitError):
            run_scheduler(provider)

    @patch.dict(
        "os.environ",
        {"AI_PR_LOOP_CREDENTIAL_IDENTITY": "SPECKIT_PR_TOKEN", "REPO_VARIABLE_WRITER_PAT": "writer"},
        clear=False,
    )
    def test_scheduler_uses_configured_credential_identity_for_cooldown_lookup(self) -> None:
        provider = _make_provider(
            eligible=[EligiblePR(number=2020, created_at="2024-01-01")],
            cursor_var="2019",
            cooldown_var=(
                '{"provider_cooldowns":{"github:SPECKIT_PR_TOKEN":'
                '{"resume_at":200,"source":"retry-after","updated_at":100}}}'
            ),
        )

        with patch("agentic_devtools.cli.ci.scheduler.time.time", return_value=150):
            result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cooldown_key == "github:SPECKIT_PR_TOKEN"
        provider.list_eligible_prs.assert_not_called()

    @patch.dict("os.environ", {"AI_PR_LOOP_CREDENTIAL_IDENTITY": "SPECKIT_PR_TOKEN"}, clear=False)
    def test_scheduler_observes_auxiliary_loop_credential_cooldown(self) -> None:
        provider = _make_provider(
            eligible=[EligiblePR(number=2020, created_at="2024-01-01")],
            cursor_var="2019",
            cooldown_var=(
                '{"provider_cooldowns":{"github:AGDT_PR_APPROVER_PAT":'
                '{"resume_at":240,"source":"retry-after","updated_at":100}}}'
            ),
        )

        with patch("agentic_devtools.cli.ci.scheduler.time.time", return_value=150):
            result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cooldown_key == "github:AGDT_PR_APPROVER_PAT"
        assert result.dispatched_prs == []
        provider.list_eligible_prs.assert_not_called()

    @patch.dict("os.environ", {"AI_PR_LOOP_DISPATCH_BATCH_SIZE": "3"}, clear=False)
    def test_batch_dispatch_multiple_prs(self) -> None:
        eligible = [
            EligiblePR(number=2020, created_at="2024-01-01"),
            EligiblePR(number=2021, created_at="2024-01-02"),
            EligiblePR(number=2022, created_at="2024-01-03"),
            EligiblePR(number=2023, created_at="2024-01-04"),
        ]
        provider = _make_provider(eligible=eligible, cursor_var="2020", batch_var=None, pool_var="10")

        result = run_scheduler(provider)

        assert result.batch_size == 3
        assert result.dispatched_count == 3
        assert result.dispatched_prs == [2021, 2022, 2023]
        assert provider.dispatch_workflow.call_count == 3

    @patch.dict("os.environ", {}, clear=False)
    def test_dispatch_failure_stops_batch(self) -> None:
        eligible = [
            EligiblePR(number=2020, created_at="2024-01-01"),
            EligiblePR(number=2021, created_at="2024-01-02"),
            EligiblePR(number=2022, created_at="2024-01-03"),
        ]
        provider = _make_provider(eligible=eligible, batch_var="3", pool_var="10")
        provider.dispatch_workflow.side_effect = [None, RuntimeError("fail"), None]

        result = run_scheduler(provider)

        # Should stop after first failure
        assert result.dispatched_count == 1
        assert result.dispatched_prs == [2020]
        assert result.had_dispatch_error is True

    @patch.dict("os.environ", {}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler.persist_cooldown")
    def test_rate_limit_during_list_eligible_prs_pauses_scheduler(self, mock_persist_cooldown) -> None:
        provider = _make_provider(pool_var="10")
        provider.list_eligible_prs.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
            source="retry-after",
        )
        mock_persist_cooldown.return_value = (
            "github:SPECKIT_PR_TOKEN",
            CooldownRecord(resume_at=210, source="retry-after", updated_at=100),
        )

        with patch("agentic_devtools.cli.ci.scheduler.time.time", return_value=200):
            result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cooldown_key == "github:SPECKIT_PR_TOKEN"
        assert result.cooldown_remaining_seconds == 10
        provider.dispatch_workflow.assert_not_called()
        provider.set_variable.assert_not_called()
        mock_persist_cooldown.assert_called_once()

    @patch.dict("os.environ", {}, clear=False)
    def test_non_rate_limit_provider_error_during_list_eligible_is_not_paused(self) -> None:
        provider = _make_provider(pool_var="10")
        provider.list_eligible_prs.side_effect = ProviderRateLimitError(is_rate_limit=False)

        with pytest.raises(ProviderRateLimitError):
            run_scheduler(provider)

    @patch.dict("os.environ", {}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler.persist_cooldown", return_value=None)
    def test_rate_limit_during_list_eligible_prs_without_persisted_record(self, mock_persist_cooldown) -> None:
        provider = _make_provider(pool_var="10")
        provider.list_eligible_prs.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
            source="retry-after",
        )

        result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cooldown_key == ""
        assert result.cooldown_source == "retry-after"
        assert result.cooldown_resume_at == ""
        assert result.cooldown_remaining_seconds == 0
        mock_persist_cooldown.assert_called_once()

    @patch.dict("os.environ", {}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler.persist_cooldown")
    def test_rate_limit_during_dispatch_pauses_scheduler(self, mock_persist_cooldown) -> None:
        eligible = [
            EligiblePR(number=2020, created_at="2024-01-01"),
            EligiblePR(number=2021, created_at="2024-01-02"),
        ]
        provider = _make_provider(eligible=eligible, batch_var="2", pool_var="10", token_valid=True)
        provider.dispatch_workflow.side_effect = [
            None,
            ProviderRateLimitError(
                provider="github",
                credential_identity="SPECKIT_PR_TOKEN",
                source="x-ratelimit-reset",
            ),
        ]
        mock_persist_cooldown.return_value = (
            "github:SPECKIT_PR_TOKEN",
            CooldownRecord(resume_at=260, source="x-ratelimit-reset", updated_at=100),
        )

        with patch("agentic_devtools.cli.ci.scheduler.time.time", return_value=200):
            result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.dispatched_prs == [2020]
        assert result.dispatched_count == 1
        assert result.cooldown_key == "github:SPECKIT_PR_TOKEN"
        assert result.cooldown_remaining_seconds == 60
        assert result.cursor_after == 2020
        assert result.cursor_persisted is True
        provider.set_variable.assert_called_once_with("AI_PR_LOOP_LAST_DISPATCHED_PR", "2020")
        mock_persist_cooldown.assert_called_once()

    @patch.dict("os.environ", {}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler.persist_cooldown")
    def test_rate_limit_during_dispatch_cursor_persist_fails(self, mock_persist_cooldown) -> None:
        eligible = [
            EligiblePR(number=2020, created_at="2024-01-01"),
            EligiblePR(number=2021, created_at="2024-01-02"),
        ]
        provider = _make_provider(eligible=eligible, batch_var="2", pool_var="10", token_valid=True)
        provider.dispatch_workflow.side_effect = [
            None,
            ProviderRateLimitError(
                provider="github",
                credential_identity="SPECKIT_PR_TOKEN",
                source="x-ratelimit-reset",
            ),
        ]
        provider.set_variable.side_effect = RuntimeError("network error")
        mock_persist_cooldown.return_value = (
            "github:SPECKIT_PR_TOKEN",
            CooldownRecord(resume_at=260, source="x-ratelimit-reset", updated_at=100),
        )

        with patch("agentic_devtools.cli.ci.scheduler.time.time", return_value=200):
            result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cursor_after == 2020
        assert result.cursor_persisted is False

    @patch.dict("os.environ", {}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler.persist_cooldown", return_value=None)
    def test_rate_limit_during_dispatch_cursor_persist_keeps_paused_outcome(self, _mock_persist_cooldown) -> None:
        eligible = [
            EligiblePR(number=2020, created_at="2024-01-01"),
            EligiblePR(number=2021, created_at="2024-01-02"),
        ]
        provider = _make_provider(eligible=eligible, batch_var="2", pool_var="10", token_valid=True)
        provider.dispatch_workflow.side_effect = [
            None,
            ProviderRateLimitError(provider="github", is_rate_limit=True),
        ]
        provider.set_variable.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)

        result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.dispatched_prs == [2020]
        assert result.cursor_after == 2020

    @patch.dict("os.environ", {}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler.persist_cooldown")
    def test_rate_limit_during_label_propagation_pauses_scheduler(self, mock_persist_cooldown) -> None:
        eligible = [EligiblePR(number=2020, created_at="2024-01-01", labels_to_propagate=("ai-auto-merge-allowed",))]
        provider = _make_provider(eligible=eligible, pool_var="10")
        provider.add_label.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
            source="retry-after",
            is_rate_limit=True,
        )
        mock_persist_cooldown.return_value = (
            "github:SPECKIT_PR_TOKEN",
            CooldownRecord(resume_at=260, source="retry-after", updated_at=100),
        )

        with patch("agentic_devtools.cli.ci.scheduler.time.time", return_value=200):
            result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cooldown_key == "github:SPECKIT_PR_TOKEN"
        provider.dispatch_workflow.assert_not_called()

    @patch.dict("os.environ", {}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler.persist_cooldown", return_value=None)
    def test_rate_limit_during_label_propagation_without_persisted_record(self, _mock_persist_cooldown) -> None:
        eligible = [EligiblePR(number=2020, created_at="2024-01-01", labels_to_propagate=("ai-auto-merge-allowed",))]
        provider = _make_provider(eligible=eligible, pool_var="10")
        provider.add_label.side_effect = ProviderRateLimitError(source="retry-after", is_rate_limit=True)

        result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cooldown_key == ""
        assert result.cooldown_source == "retry-after"

    @patch.dict("os.environ", {}, clear=False)
    def test_non_rate_limit_during_label_propagation_continues(self) -> None:
        eligible = [EligiblePR(number=2020, created_at="2024-01-01", labels_to_propagate=("ai-auto-merge-allowed",))]
        provider = _make_provider(eligible=eligible, pool_var="10")
        provider.add_label.side_effect = ProviderRateLimitError(is_rate_limit=False)

        result = run_scheduler(provider)

        assert result.status == "ok"
        assert result.dispatched_prs == [2020]
        provider.dispatch_workflow.assert_called_once()

    @patch.dict("os.environ", {}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler.propagate_linked_issue_labels")
    def test_non_rate_limit_from_label_propagation_is_propagated(self, mock_propagate) -> None:
        provider = _make_provider(eligible=[EligiblePR(number=2020, created_at="2024-01-01")], pool_var="10")
        mock_propagate.side_effect = ProviderRateLimitError(is_rate_limit=False)

        with pytest.raises(ProviderRateLimitError):
            run_scheduler(provider)

    @patch.dict("os.environ", {}, clear=False)
    def test_non_rate_limit_during_dispatch_is_propagated(self) -> None:
        eligible = [EligiblePR(number=2020, created_at="2024-01-01")]
        provider = _make_provider(eligible=eligible, pool_var="10")
        provider.dispatch_workflow.side_effect = ProviderRateLimitError(is_rate_limit=False)

        with pytest.raises(ProviderRateLimitError):
            run_scheduler(provider)

    @patch.dict("os.environ", {}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler.persist_cooldown", return_value=None)
    def test_rate_limit_during_dispatch_without_persisted_record(self, mock_persist_cooldown) -> None:
        eligible = [EligiblePR(number=2020, created_at="2024-01-01")]
        provider = _make_provider(eligible=eligible, batch_var="1", pool_var="10")
        provider.dispatch_workflow.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
            source="x-ratelimit-reset",
        )

        result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cooldown_key == ""
        assert result.cooldown_source == "x-ratelimit-reset"
        assert result.cooldown_resume_at == ""
        assert result.cooldown_remaining_seconds == 0
        mock_persist_cooldown.assert_called_once()

    @patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": "ghp_valid"}, clear=False)
    def test_cursor_write_failure_with_valid_token_logs_warning(self) -> None:
        eligible = [EligiblePR(number=2020, created_at="2024-01-01")]
        provider = _make_provider(
            eligible=eligible,
            token_valid=True,
            set_variable_side_effect=RuntimeError("no permission"),
        )

        result = run_scheduler(provider)

        assert result.dispatched_count == 1
        assert result.cursor_persisted is False
        provider.set_variable.assert_called_once_with("AI_PR_LOOP_LAST_DISPATCHED_PR", "2020")

    @patch.dict("os.environ", {}, clear=False)
    def test_rate_limit_during_cursor_persist_pauses_scheduler(self) -> None:
        provider = _make_provider(eligible=[EligiblePR(number=2020, created_at="2024-01-01")], token_valid=True)
        provider.set_variable.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="REPO_VARIABLE_WRITER_PAT",
            source="retry-after",
            is_rate_limit=True,
        )

        result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.dispatched_prs == [2020]
        assert result.cooldown_source == "retry-after"
        assert result.cursor_persisted is False

    @patch.dict("os.environ", {}, clear=False)
    def test_dry_run_no_dispatch_no_persist(self) -> None:
        eligible = [
            EligiblePR(number=2020, created_at="2024-01-01"),
            EligiblePR(number=2021, created_at="2024-01-02"),
        ]
        provider = _make_provider(eligible=eligible, pool_var="10")

        result = run_scheduler(provider, dry_run=True)

        assert result.run_mode == "dry_run"
        assert result.dispatched_count == 1
        assert result.dispatched_prs == [2020]
        provider.dispatch_workflow.assert_not_called()
        provider.set_variable.assert_not_called()

    @patch.dict("os.environ", {}, clear=False)
    def test_cursor_fallback_to_history(self) -> None:
        from agentic_devtools.cli.ci.scheduler import DispatchEvent

        eligible = [
            EligiblePR(number=2020, created_at="2024-01-01"),
            EligiblePR(number=2021, created_at="2024-01-02"),
            EligiblePR(number=2022, created_at="2024-01-03"),
        ]
        provider = _make_provider(eligible=eligible, pool_var="10")
        provider.get_recent_dispatch_history.return_value = [
            DispatchEvent(pr_number=2021, created_at="2024-01-02"),
        ]

        # Override get_variable to return None for cursor but keep pool_var
        def get_var(name: str) -> str | None:
            if name == "AI_PR_LOOP_LAST_DISPATCHED_PR":
                return None
            if name == "AI_PR_LOOP_ELIGIBLE_PR_LIMIT":
                return "10"
            return None

        provider.get_variable.side_effect = get_var

        result = run_scheduler(provider)

        # Cursor from history is 2021, so next should be 2022
        assert result.dispatched_prs == [2022]
        assert result.cursor_before == 2021

    @patch.dict("os.environ", {}, clear=False)
    def test_missing_token_logs_info(self, caplog) -> None:
        eligible = [EligiblePR(number=2020, created_at="2024-01-01")]
        provider = _make_provider(eligible=eligible, token_valid=False)

        with caplog.at_level("INFO"):
            result = run_scheduler(provider)

        # Should still dispatch successfully even without token
        assert result.dispatched_count == 1
        assert result.cursor_persisted is False
        provider.validate_variable_token.assert_called_once()
        provider.set_variable.assert_not_called()
        assert "REPO_VARIABLE_WRITER_PAT not configured" in caplog.text
        assert not any(
            record.levelname == "WARNING" and record.name == "agentic_devtools.cli.ci.scheduler"
            for record in caplog.records
        )

    @patch.dict("os.environ", {"REPO_VARIABLE_WRITER_PAT": "ghp_invalid"}, clear=False)
    def test_invalid_token_logs_warning(self, caplog) -> None:
        eligible = [EligiblePR(number=2020, created_at="2024-01-01")]
        provider = _make_provider(eligible=eligible, token_valid=False)

        with caplog.at_level("INFO"):
            result = run_scheduler(provider)

        assert result.dispatched_count == 1
        assert result.cursor_persisted is False
        provider.set_variable.assert_not_called()
        assert "REPO_VARIABLE_WRITER_PAT validation failed" in caplog.text
        assert any(
            record.levelname == "WARNING" and record.name == "agentic_devtools.cli.ci.scheduler"
            for record in caplog.records
        )

    @patch.dict("os.environ", {}, clear=False)
    def test_token_validation_exception_is_non_fatal(self) -> None:
        eligible = [EligiblePR(number=2020, created_at="2024-01-01")]
        provider = _make_provider(eligible=eligible, token_valid=False)
        provider.validate_variable_token.side_effect = NotImplementedError()

        result = run_scheduler(provider)

        assert result.dispatched_count == 1
        provider.dispatch_workflow.assert_called_once()

    @patch.dict("os.environ", {}, clear=False)
    def test_rate_limit_during_token_validation_pauses_scheduler(self) -> None:
        provider = _make_provider()
        provider.validate_variable_token.side_effect = ProviderRateLimitError(
            provider="github", credential_identity="REPO_VARIABLE_WRITER_PAT", is_rate_limit=True
        )

        result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.dispatched_count == 0

    @patch.dict("os.environ", {}, clear=False)
    def test_non_rate_limit_during_token_validation_fails_open(self) -> None:
        provider = _make_provider(eligible=[EligiblePR(number=2020, created_at="2024-01-01")])
        provider.validate_variable_token.side_effect = ProviderRateLimitError(is_rate_limit=False)

        result = run_scheduler(provider)

        assert result.dispatched_prs == [2020]
        assert result.cursor_persisted is False

    @patch.dict("os.environ", {}, clear=False)
    def test_batch_size_variable_read_failure_falls_back_to_default(self) -> None:
        eligible = [EligiblePR(number=2020, created_at="2024-01-01")]
        provider = _make_provider(eligible=eligible, pool_var="10")

        def get_var(name: str) -> str | None:
            if name == "AI_PR_LOOP_DISPATCH_BATCH_SIZE":
                raise RuntimeError("read failed")
            if name == "AI_PR_LOOP_ELIGIBLE_PR_LIMIT":
                return "10"
            return None

        provider.get_variable.side_effect = get_var

        result = run_scheduler(provider)

        assert result.batch_size == 1
        assert result.dispatched_prs == [2020]

    @patch.dict("os.environ", {}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler.persist_cooldown", return_value=None)
    def test_rate_limit_during_batch_size_read_pauses_scheduler(self, mock_persist_cooldown) -> None:
        provider = _make_provider()

        def get_var(name: str, *, use_writer_token: bool = False) -> str | None:
            if name == "AI_PR_LOOP_DISPATCH_BATCH_SIZE":
                raise ProviderRateLimitError(
                    provider="github",
                    credential_identity="REPO_VARIABLE_WRITER_PAT",
                    source="retry-after",
                )
            return None

        provider.get_variable.side_effect = get_var

        result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cooldown_source == "retry-after"
        provider.list_eligible_prs.assert_not_called()
        mock_persist_cooldown.assert_called_once()

    @patch.dict("os.environ", {}, clear=False)
    def test_non_rate_limit_during_batch_size_read_is_propagated(self) -> None:
        provider = _make_provider()

        def get_var(name: str, *, use_writer_token: bool = False) -> str | None:
            if name == "AI_PR_LOOP_DISPATCH_BATCH_SIZE":
                raise ProviderRateLimitError(is_rate_limit=False)
            return None

        provider.get_variable.side_effect = get_var

        with pytest.raises(ProviderRateLimitError):
            run_scheduler(provider)

    @patch.dict("os.environ", {}, clear=False)
    def test_pool_size_variable_read_failure_falls_back_to_default(self) -> None:
        eligible = [
            EligiblePR(number=2020, created_at="2024-01-01"),
            EligiblePR(number=2021, created_at="2024-01-02"),
        ]
        provider = _make_provider(eligible=eligible, batch_var="2")

        def get_var(name: str) -> str | None:
            if name == "AI_PR_LOOP_DISPATCH_BATCH_SIZE":
                return "2"
            if name == "AI_PR_LOOP_ELIGIBLE_PR_LIMIT":
                raise RuntimeError("read failed")
            return None

        provider.get_variable.side_effect = get_var

        result = run_scheduler(provider)

        assert result.pool_size == 1
        assert result.dispatched_prs == [2020]

    @patch.dict("os.environ", {}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler.persist_cooldown", return_value=None)
    def test_rate_limit_during_pool_size_read_pauses_scheduler(self, mock_persist_cooldown) -> None:
        provider = _make_provider()

        def get_var(name: str, *, use_writer_token: bool = False) -> str | None:
            if name == "AI_PR_LOOP_ELIGIBLE_PR_LIMIT":
                raise ProviderRateLimitError(
                    provider="github",
                    credential_identity="REPO_VARIABLE_WRITER_PAT",
                    source="x-ratelimit-reset",
                )
            return None

        provider.get_variable.side_effect = get_var

        result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cooldown_source == "x-ratelimit-reset"
        provider.list_eligible_prs.assert_not_called()
        mock_persist_cooldown.assert_called_once()

    @patch.dict("os.environ", {}, clear=False)
    def test_non_rate_limit_during_pool_size_read_is_propagated(self) -> None:
        provider = _make_provider()

        def get_var(name: str, *, use_writer_token: bool = False) -> str | None:
            if name == "AI_PR_LOOP_ELIGIBLE_PR_LIMIT":
                raise ProviderRateLimitError(is_rate_limit=False)
            return None

        provider.get_variable.side_effect = get_var

        with pytest.raises(ProviderRateLimitError):
            run_scheduler(provider)

    @patch.dict("os.environ", {}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler.persist_cooldown", return_value=None)
    def test_rate_limit_during_cursor_resolution_pauses_scheduler(self, mock_persist_cooldown) -> None:
        provider = _make_provider()

        def get_var(name: str, *, use_writer_token: bool = False) -> str | None:
            if name == "AI_PR_LOOP_LAST_DISPATCHED_PR":
                raise ProviderRateLimitError(
                    provider="github",
                    credential_identity="REPO_VARIABLE_WRITER_PAT",
                    source="retry-after",
                )
            if name == "AI_PR_LOOP_ELIGIBLE_PR_LIMIT":
                return "10"
            return None

        provider.get_variable.side_effect = get_var

        result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cooldown_source == "retry-after"
        provider.list_eligible_prs.assert_not_called()
        mock_persist_cooldown.assert_called_once()

    @patch.dict("os.environ", {}, clear=False)
    def test_non_rate_limit_during_cursor_resolution_is_propagated(self) -> None:
        provider = _make_provider(pool_var="10")

        def get_var(name: str, *, use_writer_token: bool = False) -> str | None:
            if name == "AI_PR_LOOP_ELIGIBLE_PR_LIMIT":
                return "10"
            return None

        provider.get_variable.side_effect = get_var
        with patch(
            "agentic_devtools.cli.ci.scheduler.resolve_cursor",
            side_effect=ProviderRateLimitError(is_rate_limit=False),
        ):
            with pytest.raises(ProviderRateLimitError):
                run_scheduler(provider)

    @patch.dict("os.environ", {}, clear=False)
    def test_pool_size_limits_round_robin_rotation(self) -> None:
        eligible = [
            EligiblePR(number=2020, created_at="2024-01-01"),
            EligiblePR(number=2021, created_at="2024-01-02"),
            EligiblePR(number=2022, created_at="2024-01-03"),
            EligiblePR(number=2023, created_at="2024-01-04"),
            EligiblePR(number=2024, created_at="2024-01-05"),
        ]
        # pool_var=3 means only the 3 oldest (2020, 2021, 2022) are in rotation
        provider = _make_provider(eligible=eligible, pool_var="3", cursor_var="2020")

        result = run_scheduler(provider)

        # batch_size defaults to 1, should dispatch next after cursor (2021)
        assert result.pool_size == 3
        assert result.eligible_count == 5
        assert result.dispatched_prs == [2021]
        provider.list_eligible_prs.assert_called_once_with(max_prs=3)
        # PRs 2023 and 2024 are NOT in the pool

    @patch.dict("os.environ", {}, clear=False)
    def test_pool_size_default_processes_only_oldest(self) -> None:
        eligible = [
            EligiblePR(number=2020, created_at="2024-01-01"),
            EligiblePR(number=2021, created_at="2024-01-02"),
            EligiblePR(number=2022, created_at="2024-01-03"),
        ]
        # No pool_var set — default is 1, so only oldest PR is in rotation
        provider = _make_provider(eligible=eligible)

        result = run_scheduler(provider)

        assert result.pool_size == 1
        assert result.eligible_count == 3
        assert result.dispatched_prs == [2020]

    @patch.dict("os.environ", {"AI_PR_LOOP_ELIGIBLE_PR_LIMIT": "2"}, clear=False)
    def test_pool_size_from_env_overrides_repo_var(self) -> None:
        eligible = [
            EligiblePR(number=2020, created_at="2024-01-01"),
            EligiblePR(number=2021, created_at="2024-01-02"),
            EligiblePR(number=2022, created_at="2024-01-03"),
        ]
        # env says 2, repo says 3 — env wins
        provider = _make_provider(eligible=eligible, pool_var="3", batch_var="2")

        result = run_scheduler(provider)

        assert result.pool_size == 2
        # Only 2020 and 2021 in pool, batch_size=2, start from oldest
        assert result.dispatched_prs == [2020, 2021]

    @patch.dict("os.environ", {}, clear=False)
    def test_falls_back_when_provider_does_not_accept_max_prs(self) -> None:
        eligible = [
            EligiblePR(number=2020, created_at="2024-01-01"),
            EligiblePR(number=2021, created_at="2024-01-02"),
        ]
        provider = _make_provider(eligible=eligible, pool_var="1")
        provider.list_eligible_prs.side_effect = [TypeError("got an unexpected keyword argument 'max_prs'"), eligible]

        result = run_scheduler(provider)

        assert result.dispatched_prs == [2020]
        assert provider.list_eligible_prs.call_count == 2

    @patch.dict("os.environ", {}, clear=False)
    def test_pauses_when_fallback_eligibility_listing_hits_rate_limit(self) -> None:
        provider = _make_provider(pool_var="1")
        provider.list_eligible_prs.side_effect = [
            TypeError("got an unexpected keyword argument 'max_prs'"),
            ProviderRateLimitError(
                provider="github",
                credential_identity="SPECKIT_PR_TOKEN",
                source="x-ratelimit-reset",
                reset_timestamp=220,
            ),
        ]

        with patch("agentic_devtools.cli.ci.scheduler.time.time", return_value=150):
            result = run_scheduler(provider)

        assert result.status == "rate_limit_paused"
        assert result.cooldown_source == "x-ratelimit-reset"
        assert result.cursor_before is None
        assert provider.list_eligible_prs.call_count == 2

    @patch.dict("os.environ", {}, clear=False)
    def test_reraises_fallback_provider_rate_limit_error_when_not_flagged_rate_limit(self) -> None:
        provider = _make_provider(pool_var="1")
        provider.list_eligible_prs.side_effect = [
            TypeError("got an unexpected keyword argument 'max_prs'"),
            ProviderRateLimitError(is_rate_limit=False),
        ]

        with pytest.raises(ProviderRateLimitError):
            run_scheduler(provider)
        assert provider.list_eligible_prs.call_count == 2

    @patch.dict("os.environ", {}, clear=False)
    def test_reraises_unrelated_typeerror_from_provider(self) -> None:
        provider = _make_provider(pool_var="1")
        provider.list_eligible_prs.side_effect = TypeError("unexpected response shape")

        with pytest.raises(TypeError, match="unexpected response shape"):
            run_scheduler(provider)
        assert provider.list_eligible_prs.call_count == 1

    @patch.dict("os.environ", {}, clear=False)
    def test_propagates_linked_issue_labels_before_dispatch(self) -> None:
        eligible = [
            EligiblePR(
                number=2020,
                created_at="2024-01-01",
                labels_to_propagate=("ai-auto-merge-allowed",),
            )
        ]
        provider = _make_provider(eligible=eligible)

        result = run_scheduler(provider)

        provider.add_label.assert_called_once_with(2020, "ai-auto-merge-allowed")
        assert result.dispatched_prs == [2020]

    @patch.dict("os.environ", {}, clear=False)
    def test_no_label_propagation_when_nothing_pending(self) -> None:
        provider = _make_provider(eligible=[EligiblePR(number=2020, created_at="2024-01-01")])

        run_scheduler(provider)

        provider.add_label.assert_not_called()

    @patch.dict("os.environ", {}, clear=False)
    def test_dry_run_does_not_propagate_labels(self) -> None:
        eligible = [
            EligiblePR(
                number=2020,
                created_at="2024-01-01",
                labels_to_propagate=("ai-auto-merge-allowed",),
            )
        ]
        provider = _make_provider(eligible=eligible)

        result = run_scheduler(provider, dry_run=True)

        provider.add_label.assert_not_called()
        assert result.run_mode == "dry_run"

    @patch.dict("os.environ", {}, clear=False)
    def test_label_propagation_failure_does_not_abort_scheduling(self) -> None:
        eligible = [
            EligiblePR(
                number=2020,
                created_at="2024-01-01",
                labels_to_propagate=("ai-auto-merge-allowed",),
            )
        ]
        provider = _make_provider(eligible=eligible)
        provider.add_label.side_effect = RuntimeError("403 Forbidden")

        result = run_scheduler(provider)

        assert result.dispatched_prs == [2020]
        assert result.had_dispatch_error is False

    @patch.dict("os.environ", {}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler.propagate_linked_issue_labels")
    def test_unexpected_propagation_error_does_not_abort_scheduling(self, mock_propagate) -> None:
        mock_propagate.side_effect = RuntimeError("propagation exploded")
        provider = _make_provider(eligible=[EligiblePR(number=2020, created_at="2024-01-01")])

        result = run_scheduler(provider)

        assert result.dispatched_prs == [2020]
        assert result.had_dispatch_error is False
