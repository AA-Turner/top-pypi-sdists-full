"""Tests for watchdog probe reconciliation before provider dispatch."""

from datetime import UTC, datetime
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci.watchdog_command import _reconcile_due_probes_and_check_availability
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

MODULE = "agentic_devtools.cli.ci.watchdog_command"
NOW = datetime(2026, 10, 25, tzinfo=UTC)


def test_reconciles_probes_without_cooldown_state_and_establishes_availability() -> None:
    with (
        patch(f"{MODULE}._load_cooldown_state", return_value=None),
        patch(f"{MODULE}._seed_cooldown_state", return_value=None),
        patch(f"{MODULE}.run_due_probe_wakeup", return_value=2) as run_probes,
        patch(f"{MODULE}._cooldown_availability", return_value=(True, "available")),
    ):
        result = _reconcile_due_probes_and_check_availability("owner/repo", None, NOW)

    assert result == (2, True, "available")
    run_probes.assert_called_once_with(repo="owner/repo", cooldown_state=None)


def test_reconciles_probes_with_existing_cooldown_state() -> None:
    state = Mock()
    with (
        patch(f"{MODULE}._load_cooldown_state", return_value=state),
        patch(f"{MODULE}._seed_cooldown_state") as seed,
        patch(f"{MODULE}.run_due_probe_wakeup", return_value=1) as run_probes,
        patch(f"{MODULE}._cooldown_availability", return_value=(True, "available")),
    ):
        result = _reconcile_due_probes_and_check_availability("owner/repo", None, NOW)

    assert result == (1, True, "available")
    seed.assert_not_called()
    run_probes.assert_called_once_with(repo="owner/repo", cooldown_state=state)


def test_seeds_cooldown_state_before_probe_reconciliation() -> None:
    state = Mock()
    latest_run = {"status": "completed"}
    with (
        patch(f"{MODULE}._load_cooldown_state", return_value=None),
        patch(f"{MODULE}._seed_cooldown_state", return_value=state) as seed,
        patch(f"{MODULE}.run_due_probe_wakeup", return_value=0) as run_probes,
        patch(f"{MODULE}._cooldown_availability", return_value=(True, "available")),
    ):
        result = _reconcile_due_probes_and_check_availability("owner/repo", latest_run, NOW)

    assert result == (0, True, "available")
    seed.assert_called_once_with(latest_run, NOW)
    run_probes.assert_called_once_with(repo="owner/repo", cooldown_state=state)


def test_probe_reconciliation_failure_fails_closed() -> None:
    with (
        patch(f"{MODULE}._load_cooldown_state", side_effect=RuntimeError("unreadable")),
        patch(f"{MODULE}.run_due_probe_wakeup") as run_probes,
        patch(f"{MODULE}._cooldown_availability") as availability,
    ):
        result = _reconcile_due_probes_and_check_availability("owner/repo", None, NOW)

    assert result == (0, False, "cooldown_state_unknown")
    run_probes.assert_not_called()
    availability.assert_not_called()


def test_blocking_probe_state_prevents_provider_dispatch() -> None:
    with (
        patch(f"{MODULE}._load_cooldown_state", return_value=None),
        patch(f"{MODULE}._seed_cooldown_state", return_value=None),
        patch(f"{MODULE}.run_due_probe_wakeup", return_value=1),
        patch(f"{MODULE}._cooldown_availability", return_value=(False, "cooldown_pending")),
    ):
        result = _reconcile_due_probes_and_check_availability("owner/repo", None, NOW)

    assert result == (1, False, "cooldown_pending")


def test_unreadable_availability_state_fails_closed_after_reconciliation() -> None:
    with (
        patch(f"{MODULE}._load_cooldown_state", return_value=None),
        patch(f"{MODULE}._seed_cooldown_state", return_value=None),
        patch(f"{MODULE}.run_due_probe_wakeup", return_value=3),
        patch(f"{MODULE}._cooldown_availability", side_effect=RuntimeError("unreadable")),
    ):
        result = _reconcile_due_probes_and_check_availability("owner/repo", None, NOW)

    assert result == (3, False, "cooldown_state_unknown")


@pytest.mark.parametrize(
    "error",
    [ProviderRateLimitError(retry_after_seconds=60), RetryableError("limited", retry_after=60, is_rate_limit=True)],
)
@pytest.mark.parametrize("stage", ["_load_cooldown_state", "_cooldown_availability"])
def test_typed_rate_limit_propagates_so_callers_preserve_the_deadline(stage, error) -> None:
    with (
        patch(f"{MODULE}._load_cooldown_state", return_value=None),
        patch(f"{MODULE}._seed_cooldown_state", return_value=None),
        patch(f"{MODULE}.run_due_probe_wakeup", return_value=0),
        patch(f"{MODULE}._cooldown_availability", return_value=(True, "available")),
        patch(f"{MODULE}.{stage}", side_effect=error),
        pytest.raises(type(error)),
    ):
        _reconcile_due_probes_and_check_availability("owner/repo", None, NOW)


def test_non_rate_limit_retryable_error_still_fails_closed() -> None:
    with (
        patch(f"{MODULE}._load_cooldown_state", side_effect=RetryableError("HTTP 502", is_rate_limit=False)),
        patch(f"{MODULE}.run_due_probe_wakeup") as run_probes,
    ):
        result = _reconcile_due_probes_and_check_availability("owner/repo", None, NOW)

    assert result == (0, False, "cooldown_state_unknown")
    run_probes.assert_not_called()
