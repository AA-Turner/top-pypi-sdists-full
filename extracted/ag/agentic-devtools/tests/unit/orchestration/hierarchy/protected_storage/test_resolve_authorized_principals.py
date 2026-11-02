"""Tests for resolving the configured hierarchy storage allowlist."""

from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.protected_storage import resolve_authorized_principals


def test_resolve_authorized_principals_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGDT_HIERARCHY_AUTHORIZED_PRINCIPALS", "alice, bob, alice")
    assert resolve_authorized_principals() == frozenset({"alice", "bob"})


def test_resolve_authorized_principals_from_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AGDT_HIERARCHY_AUTHORIZED_PRINCIPALS", raising=False)
    config_file = tmp_path / "principals"
    config_file.write_text("alice\n# comment\n bob \n", encoding="utf-8")
    assert resolve_authorized_principals(config_file=config_file) == frozenset({"alice", "bob"})


def test_resolve_authorized_principals_rejects_missing_configuration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("AGDT_HIERARCHY_AUTHORIZED_PRINCIPALS", raising=False)
    with pytest.raises(ValueError, match="allowlist"):
        resolve_authorized_principals(config_file=tmp_path / "missing")
