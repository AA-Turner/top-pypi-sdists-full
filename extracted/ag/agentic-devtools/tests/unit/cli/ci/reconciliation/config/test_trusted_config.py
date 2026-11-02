"""Tests for trusted reconciliation config scaffolding."""

from __future__ import annotations

import importlib
import os

from agentic_devtools.cli.ci.reconciliation.config import _safe_csv


def test_safe_csv_parses_and_strips_values(monkeypatch) -> None:
    monkeypatch.setenv("AGDT_TEST_SCOPE", " owner/repo:main , owner/other:release ")
    assert _safe_csv("AGDT_TEST_SCOPE", ()) == ("owner/repo:main", "owner/other:release")


def test_safe_csv_uses_default_for_empty(monkeypatch) -> None:
    monkeypatch.setenv("AGDT_TEST_SCOPE", " , ")
    assert _safe_csv("AGDT_TEST_SCOPE", ("default",)) == ("default",)


def test_trusted_config_constants_reload_from_env(monkeypatch) -> None:
    monkeypatch.setenv("AGDT_TRUSTED_RECONCILIATION_ROLLOUT_ENABLED", "true")
    monkeypatch.setenv("AGDT_TRUSTED_RECONCILIATION_TARGET_BRANCHES", "main,release")
    import agentic_devtools.cli.ci.reconciliation.config as cfg

    reloaded = importlib.reload(cfg)
    assert reloaded.TRUSTED_RECONCILIATION_ROLLOUT_ENABLED is True
    assert reloaded.TRUSTED_RECONCILIATION_TARGET_BRANCHES == ("main", "release")


# Prevent state leakage from reload-dependent test.
os.environ.pop("AGDT_TRUSTED_RECONCILIATION_ROLLOUT_ENABLED", None)
os.environ.pop("AGDT_TRUSTED_RECONCILIATION_TARGET_BRANCHES", None)
