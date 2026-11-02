"""Fixtures for isolated CI unit tests."""

import pytest


@pytest.fixture(autouse=True)
def unset_runner_github_actions(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep unit tests independent of the host GitHub Actions runner."""
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
