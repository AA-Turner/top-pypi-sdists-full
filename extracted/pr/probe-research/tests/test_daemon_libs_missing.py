"""A worker without the daemon's AI libraries (2026-10-12): a newer tap retries,
an older one is still told not to respawn, and `daemon-errors.log` gets the line
once an hour per session, not once per retry."""

from __future__ import annotations

import logging
import sys
import types

import pytest

from probe.daemon import trace as trace_mod
from probe.daemon import worker as worker_mod

SID = "0d5e8a3c-6f8e-4b1a-9c55-2f1f7a0b9c11"


@pytest.fixture
def no_libraries(monkeypatch):
    monkeypatch.setattr(worker_mod, "ai_libraries_importable", lambda: False)


@pytest.fixture
def quiet_root(monkeypatch):
    """`main` installs the session's log handlers on an empty root: give it one and
    close what it opened, as test_daemon_trace.py does."""
    root = logging.getLogger()
    monkeypatch.setattr(root, "handlers", [])
    monkeypatch.setattr(root, "level", root.level)
    for name in trace_mod.NOISY_LOGGERS:
        monkeypatch.setattr(logging.getLogger(name), "level", logging.getLogger(name).level)
    yield
    logging.captureWarnings(False)
    for handler in list(root.handlers):
        handler.close()


def _main(tmp_path) -> int:
    return worker_mod.main(["--session-id", SID, "--transcript", str(tmp_path / "t.jsonl"), "--cwd", str(tmp_path)])


def _errors() -> list[str]:
    path = worker_mod._state_base() / "daemon-errors.log"
    return [line for line in path.read_text().splitlines() if "AI libraries" in line] if path.exists() else []


@pytest.mark.parametrize(
    "retries, code",
    [(None, worker_mod.EXIT_DO_NOT_RESPAWN), ("1", worker_mod.EXIT_RETRY_LIBS)],
)
def test_missing_libraries_exit_by_what_the_supervisor_understands(tmp_path, monkeypatch, no_libraries, quiet_root,
                                                                    retries, code):
    if retries:
        monkeypatch.setenv(worker_mod.SUPERVISOR_RETRIES_LIBS_ENV, retries)
    else:
        monkeypatch.delenv(worker_mod.SUPERVISOR_RETRIES_LIBS_ENV, raising=False)
    assert _main(tmp_path) == code


def test_a_retrying_supervisor_logs_the_missing_libraries_once_an_hour(tmp_path, monkeypatch, no_libraries,
                                                                       quiet_root):
    monkeypatch.setenv(worker_mod.SUPERVISOR_RETRIES_LIBS_ENV, "1")
    for _ in range(3):
        assert _main(tmp_path) == worker_mod.EXIT_RETRY_LIBS
    assert len(_errors()) == 1


def test_a_half_installed_daemon_extra_reads_as_missing(monkeypatch):
    """`pydantic_ai` without `pydantic_ai_harness` must take the libraries exit:
    the harness is imported unconditionally later and would crash instead. Both
    modules are faked: CI installs `.[dev]`, which has neither."""
    monkeypatch.setitem(sys.modules, "pydantic_ai", types.ModuleType("pydantic_ai"))
    monkeypatch.setitem(sys.modules, "pydantic_ai_harness", types.ModuleType("pydantic_ai_harness"))
    assert worker_mod.ai_libraries_importable()
    monkeypatch.setitem(sys.modules, "pydantic_ai_harness", None)  # its import raises ImportError
    assert not worker_mod.ai_libraries_importable()


def test_the_once_an_hour_stamp_lives_in_the_session_folder(tmp_path, monkeypatch, no_libraries, quiet_root):
    """`sweep_stale` deletes a session's folder with it; a stamp anywhere else
    in the daemon's state would stay for good."""
    monkeypatch.setenv(worker_mod.SUPERVISOR_RETRIES_LIBS_ENV, "1")
    _main(tmp_path)
    assert [p.name for p in trace_mod.session_dir(SID).glob("*.stamp")] == ["telemetry-libs-missing.stamp"]
    assert not list(worker_mod._state_base().glob("daemon/*.stamp"))
