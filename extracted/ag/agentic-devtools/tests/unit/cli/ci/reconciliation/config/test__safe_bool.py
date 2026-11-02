"""Tests for _safe_bool()."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.reconciliation.config import _safe_bool


def test_returns_true_for_true_spellings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGDT_ENABLE_RECONCILIATION", "true")
    assert _safe_bool("AGDT_ENABLE_RECONCILIATION", False) is True


def test_returns_false_for_false_spellings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGDT_ENABLE_RECONCILIATION", "false")
    assert _safe_bool("AGDT_ENABLE_RECONCILIATION", True) is False


def test_returns_default_true_for_unrecognized_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGDT_ENABLE_RECONCILIATION", "treu")
    assert _safe_bool("AGDT_ENABLE_RECONCILIATION", True) is True


def test_returns_default_false_for_unrecognized_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGDT_ENABLE_RECONCILIATION", "treu")
    assert _safe_bool("AGDT_ENABLE_RECONCILIATION", False) is False
