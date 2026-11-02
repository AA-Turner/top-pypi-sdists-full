"""Tests for rollout feature-flag loading."""

from __future__ import annotations

import agentic_devtools.cli.ci.reconciliation.config as config
from agentic_devtools.cli.ci.reconciliation.rollout import load_rollout


def test_load_rollout_uses_config_flag(monkeypatch) -> None:
    monkeypatch.setattr(config, "TRUSTED_RECONCILIATION_ROLLOUT_ENABLED", False)
    rollout = load_rollout()
    assert not rollout.enabled
    assert rollout.shadow_mode


def test_load_rollout_enabled_mode(monkeypatch) -> None:
    monkeypatch.setattr(config, "TRUSTED_RECONCILIATION_ROLLOUT_ENABLED", True)
    rollout = load_rollout()
    assert rollout.enabled
    assert not rollout.shadow_mode
    assert rollout.enforce_fail_closed
