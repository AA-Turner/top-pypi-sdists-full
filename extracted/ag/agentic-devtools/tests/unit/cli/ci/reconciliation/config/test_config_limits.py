"""Tests for reconciliation configuration limits."""

from __future__ import annotations

import agentic_devtools.cli.ci.reconciliation.config as cfg


def test_max_retry_attempts_positive():
    assert cfg.MAX_RETRY_ATTEMPTS > 0


def test_max_recovery_attempts_positive():
    assert cfg.MAX_RECOVERY_ATTEMPTS > 0


def test_max_pagination_pages_positive():
    assert cfg.MAX_PAGINATION_PAGES_PER_RUN > 0


def test_max_lease_reclaims_per_cycle_positive():
    assert cfg.MAX_LEASE_RECLAIMS_PER_CYCLE > 0


def test_max_lease_reclaim_cycles_positive():
    assert cfg.MAX_LEASE_RECLAIM_CYCLES > 0


def test_max_state_size_bytes_positive():
    assert cfg.MAX_STATE_SIZE_BYTES > 0


def test_max_state_age_seconds_positive():
    assert cfg.MAX_STATE_AGE_SECONDS > 0


def test_max_provider_failure_duration_positive():
    assert cfg.MAX_PROVIDER_FAILURE_DURATION > 0


def test_reconciliation_schedule_interval_positive():
    assert cfg.RECONCILIATION_SCHEDULE_INTERVAL_MINUTES > 0


def test_enable_reconciliation_is_bool():
    assert isinstance(cfg.ENABLE_RECONCILIATION, bool)


def test_enable_due_probe_wakeup_is_bool():
    assert isinstance(cfg.ENABLE_DUE_PROBE_WAKEUP, bool)
