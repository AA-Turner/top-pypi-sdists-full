"""Tests for next_action function."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.setup.fixloop import ErrorClass, FixAction, next_action


class TestNextActionInputValidation:
    """next_action rejects negative counts (consistent with backoff_seconds)."""

    def test_negative_attempts_raises(self) -> None:
        with pytest.raises(ValueError, match="attempts >= 0"):
            next_action(ErrorClass.MISSING_DEPENDENCY, -1, 0)

    def test_negative_total_raises(self) -> None:
        with pytest.raises(ValueError, match="total >= 0"):
            next_action(ErrorClass.MISSING_DEPENDENCY, 0, -1)

    def test_both_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="attempts >= 0"):
            next_action(ErrorClass.MISSING_DEPENDENCY, -1, -1)


class TestNextActionSuccess:
    """FR-004: SUCCESS always returns no-op."""

    def test_success_returns_noop(self) -> None:
        result = next_action(ErrorClass.SUCCESS, 0, 0)
        assert result == FixAction(give_up=False, remedy=None, re_exec=False)

    def test_success_ignores_high_attempts(self) -> None:
        result = next_action(ErrorClass.SUCCESS, 10, 10)
        assert result == FixAction(give_up=False, remedy=None, re_exec=False)


class TestNextActionAuthSecret:
    """FR-005: AUTH_SECRET always gives up."""

    def test_auth_secret_gives_up_at_zero(self) -> None:
        result = next_action(ErrorClass.AUTH_SECRET, 0, 0)
        assert result == FixAction(give_up=True, remedy=None, re_exec=False)

    def test_auth_secret_gives_up_regardless_of_counts(self) -> None:
        result = next_action(ErrorClass.AUTH_SECRET, 5, 10)
        assert result.give_up is True
        assert result.remedy is None


class TestNextActionUnknown:
    """FR-011: UNKNOWN always gives up."""

    def test_unknown_gives_up(self) -> None:
        result = next_action(ErrorClass.UNKNOWN, 0, 0)
        assert result == FixAction(give_up=True, remedy=None, re_exec=False)

    def test_unknown_gives_up_at_zero_attempts(self) -> None:
        result = next_action(ErrorClass.UNKNOWN, 0, 0)
        assert result.give_up is True


class TestNextActionCaps:
    """FR-006/FR-010: Per-class and total caps."""

    def test_per_class_cap_at_two(self) -> None:
        result = next_action(ErrorClass.MISSING_DEPENDENCY, 2, 0)
        assert result.give_up is True

    def test_per_class_cap_above_two(self) -> None:
        result = next_action(ErrorClass.MISSING_DEPENDENCY, 5, 0)
        assert result.give_up is True

    def test_total_cap_at_six(self) -> None:
        result = next_action(ErrorClass.MISSING_DEPENDENCY, 0, 6)
        assert result.give_up is True

    def test_total_cap_above_six(self) -> None:
        result = next_action(ErrorClass.CERT_CA_FETCH, 0, 10)
        assert result.give_up is True

    def test_below_caps_allows_retry(self) -> None:
        result = next_action(ErrorClass.MISSING_DEPENDENCY, 1, 5)
        assert result.give_up is False


class TestNextActionRetryPermitted:
    """Retryable error classes return remedy when under caps."""

    @pytest.mark.parametrize(
        "error_class",
        [
            ErrorClass.MISSING_DEPENDENCY,
            ErrorClass.STALE_PARTIAL_INSTALL,
            ErrorClass.CERT_CA_FETCH,
            ErrorClass.PATH_PROFILE_NOT_UPDATED,
            ErrorClass.SKILL_INJECTION_PERMS,
            ErrorClass.TRANSIENT_NETWORK,
        ],
    )
    def test_retryable_class_returns_remedy(self, error_class: ErrorClass) -> None:
        result = next_action(error_class, 0, 0)
        assert result.give_up is False
        assert result.remedy is not None
        assert isinstance(result.remedy, str)


class TestNextActionReExec:
    """FR-007: STALE_PARTIAL_INSTALL returns re_exec=True."""

    def test_stale_partial_install_re_exec_true(self) -> None:
        result = next_action(ErrorClass.STALE_PARTIAL_INSTALL, 0, 0)
        assert result.re_exec is True

    def test_missing_dependency_re_exec_false(self) -> None:
        result = next_action(ErrorClass.MISSING_DEPENDENCY, 0, 0)
        assert result.re_exec is False

    def test_cert_ca_fetch_re_exec_false(self) -> None:
        result = next_action(ErrorClass.CERT_CA_FETCH, 0, 0)
        assert result.re_exec is False

    def test_transient_network_re_exec_false(self) -> None:
        result = next_action(ErrorClass.TRANSIENT_NETWORK, 0, 0)
        assert result.re_exec is False
