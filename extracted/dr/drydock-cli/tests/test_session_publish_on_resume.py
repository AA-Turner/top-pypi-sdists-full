"""Regression: resume_existing_session must publish marker files too.

Without this, drydocks that resume an existing session don't write
to ~/.drydock/sessions_by_pid/<pid>.txt or <cwd>/.drydock/current_session.txt,
so external watchers can't find them. Discovered 2026-05-18 when the
operator's running drydock was invisible to the new TUI capture
pipeline (no per-pid marker even though messages.jsonl was active).
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from drydock.core.config._settings import SessionLoggingConfig
from drydock.core.session.session_logger import SessionLogger


def test_init_publishes_markers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    sc = SessionLoggingConfig(
        save_dir=str(tmp_path / "sessions"),
        session_prefix="session",
        enabled=True,
    )
    sl = SessionLogger(session_config=sc, session_id="abcd1234-5678-90ef-1234-567890abcdef")
    # Per-pid
    marker = tmp_path / ".drydock" / "sessions_by_pid" / f"{os.getpid()}.txt"
    assert marker.exists()
    assert str(sl.session_dir) in marker.read_text()


def test_resume_publishes_markers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The bug: a fresh-from-scratch SessionLogger that then resumes
    must publish on resume — not only at __init__."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    sc = SessionLoggingConfig(
        save_dir=str(tmp_path / "sessions"),
        session_prefix="session",
        enabled=True,
    )
    sl = SessionLogger(session_config=sc, session_id="initial-uuid")

    # Simulate a previous session on disk.
    target_dir = tmp_path / "sessions" / "session_20260518_010101_aabbccdd"
    target_dir.mkdir(parents=True)
    (target_dir / "messages.jsonl").write_text("")
    meta = {
        "session_id": "aabbccdd-...",
        "start_time": "2026-05-18T01:01:01+00:00",
        "end_time": None,
        "environment": {"working_directory": str(tmp_path)},
        "git_commit": None,
        "git_branch": None,
        "username": "test",
        "stats": {},
        "title": None,
        "total_messages": 0,
        "tools_available": [],
    }
    import json
    (target_dir / "meta.json").write_text(json.dumps(meta))

    # Reset the marker file to detect that resume re-publishes.
    marker = tmp_path / ".drydock" / "sessions_by_pid" / f"{os.getpid()}.txt"
    marker.unlink(missing_ok=True)

    sl.resume_existing_session("aabbccdd-...", target_dir)

    # The marker should exist again, pointing at the resumed dir.
    assert marker.exists(), "resume_existing_session did not republish per-pid marker"
    assert str(target_dir) in marker.read_text()


def test_disabled_logger_does_not_publish(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    sc = SessionLoggingConfig(save_dir=str(tmp_path), session_prefix="s", enabled=False)
    sl = SessionLogger(session_config=sc, session_id="x")
    sl.resume_existing_session("y", tmp_path)
    marker = tmp_path / ".drydock" / "sessions_by_pid" / f"{os.getpid()}.txt"
    assert not marker.exists()
