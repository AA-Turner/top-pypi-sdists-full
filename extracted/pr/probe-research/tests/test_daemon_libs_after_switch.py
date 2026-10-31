"""The daemon's AI libraries after a side-by-side install switched `probe` to a
new environment (2026-10-29): this process still runs from the old one, so its
own import fails, yet the install had just checked them in the new one. The
readiness check uses that checked answer instead of reading missing, and never
guesses an environment from PATH (a conda or pyenv `probe` first on PATH is not
where the service starts the daemon)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from probe.cli import bootstrap, daemon_cli, install_pipeline


@pytest.fixture
def no_local_libraries(monkeypatch):
    monkeypatch.setattr(daemon_cli, "_installed_copy", lambda: None)
    monkeypatch.setitem(sys.modules, "pydantic_ai_harness", None)  # its import raises ImportError
    monkeypatch.setattr(daemon_cli, "_switched_ai_libraries", None)
    monkeypatch.setattr(bootstrap, "_installed_binary", lambda: pytest.fail("readiness never guesses from PATH"))


def _install(monkeypatch, **outcome):
    monkeypatch.setattr(install_pipeline, "install_cli", lambda version, *, mode, person: install_pipeline.CliOutcome(
        env=Path("/tools/1.0.0+g2/probe-research"), version=version, changed=True, **outcome))
    monkeypatch.setattr(daemon_cli, "_fresh_ai_libraries", lambda python: "2.51.0")


def test_a_switched_install_is_ready_in_the_process_that_switched(monkeypatch, no_local_libraries):
    assert daemon_cli.ai_libraries() is None
    _install(monkeypatch, ok=True)
    assert daemon_cli._install_side_by_side("1.0.0") == 0
    assert daemon_cli.ai_libraries() == "2.51.0"


def test_a_switch_still_waiting_for_a_quiet_machine_is_not_ready(monkeypatch, no_local_libraries):
    _install(monkeypatch, ok=True, waiting="the switch waits for a quiet machine")
    daemon_cli._install_side_by_side("1.0.0")
    assert daemon_cli.ai_libraries() is None


def test_a_failed_check_in_the_new_environment_is_not_ready(monkeypatch, no_local_libraries):
    _install(monkeypatch, ok=True)
    monkeypatch.setattr(daemon_cli, "_fresh_ai_libraries", lambda python: None)
    assert daemon_cli._install_side_by_side("1.0.0") == 1
    assert daemon_cli.ai_libraries() is None
