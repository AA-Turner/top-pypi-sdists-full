"""Tests: SAGE re-prompts when an implementation request produces no FILE: output."""

from __future__ import annotations

import pytest

from pathlib import Path

from sage.main import (
    _build_implementation_completion_nudge,
    _resolve_implementation_test_command,
    _suggest_target_paths_for_task,
)


def test_implementation_nudge_mentions_file_run_and_test_command() -> None:
    text = _build_implementation_completion_nudge(
        "fix the login form",
        "[cwd=ai-platform/frontend] npm test -- --run",
        2,
        4,
    )
    assert "FILE:" in text
    assert "RUN:" in text or "npm test" in text
    assert "fix the login form" in text
    assert "2/4" in text


def test_resolve_implementation_test_command_prefers_frontend_vitest(tmp_path: Path) -> None:
    """Firebase/auth tasks should suggest npm test in ai-platform/frontend when present."""
    (tmp_path / "ai-platform" / "frontend").mkdir(parents=True)
    (tmp_path / "ai-platform" / "frontend" / "package.json").write_text("{}", encoding="utf-8")
    cmd = _resolve_implementation_test_command(
        tmp_path,
        "Fix Firebase auth and VITE_ env",
        "python -m pytest -q",
    )
    assert "npm test" in cmd
    assert "ai-platform/frontend" in cmd


def test_suggest_paths_includes_sage_credentials_for_api_key_task(tmp_path: Path) -> None:
    (tmp_path / "ai-platform" / "sage" / "core").mkdir(parents=True)
    (tmp_path / "ai-platform" / "sage" / "core" / "credentials.py").write_text("# ok", encoding="utf-8")
    hints = _suggest_target_paths_for_task(tmp_path, "Fix invalid api key for Groq in Sage CLI")
    assert "credentials.py" in hints
