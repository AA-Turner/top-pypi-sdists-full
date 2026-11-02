from __future__ import annotations

from agentic_devtools.cli import pull_request_approval as commands


def test_prefers_explicit_value() -> None:
    assert commands._state_or("explicit", "missing") == "explicit"


def test_returns_none_when_keys_are_missing(monkeypatch) -> None:
    monkeypatch.setattr(commands, "get_value", lambda _: None)
    assert commands._state_or(None, "missing") is None
