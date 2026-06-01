"""Tests for `efterlev.shell.ai` — Q&A handler + system prompt builder."""

from __future__ import annotations

from pathlib import Path

import pytest
from rich.console import Console

from efterlev.shell import credentials as creds_mod
from efterlev.shell.ai import (
    _build_command_catalog,
    _build_system_prompt,
    _build_workspace_section,
    run_ai_query,
)
from efterlev.shell.commands import ShellContext


@pytest.fixture
def isolated_creds(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point CREDENTIALS_DIR at a tmp dir so tests don't touch ~/.efterlev."""
    monkeypatch.setattr(creds_mod, "CREDENTIALS_DIR", tmp_path)
    monkeypatch.setattr(creds_mod, "CREDENTIALS_PATH", tmp_path / "credentials.toml")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return tmp_path


def test_command_catalog_lists_known_commands() -> None:
    """The catalog must include the slash commands the AI is allowed to suggest."""
    catalog = _build_command_catalog()
    for name in ("/init", "/scan", "/agent", "/report", "/poam", "/setup", "/ai"):
        assert name in catalog, f"{name} not in catalog"


def test_workspace_section_handles_uninitialized(tmp_path: Path) -> None:
    """Uninitialized workspace should still produce a valid JSON section."""
    ctx = ShellContext(root=tmp_path, console=Console(force_terminal=False))
    section = _build_workspace_section(ctx)
    assert '"initialized": false' in section
    assert '"evidence_count": null' in section


def test_system_prompt_includes_all_three_sections(tmp_path: Path) -> None:
    ctx = ShellContext(root=tmp_path, console=Console(force_terminal=False))
    prompt = _build_system_prompt(ctx)
    # Domain primer fragments
    assert "Efterlev shell assistant" in prompt
    assert "KSI" in prompt
    assert "FRMR" in prompt
    # Workspace section
    assert "Current workspace state" in prompt
    # Command catalog
    assert "Available slash commands" in prompt


def test_system_prompt_includes_behavior_rules(tmp_path: Path) -> None:
    """The prompt must tell the model to be terse + cite real numbers + never invent commands."""
    ctx = ShellContext(root=tmp_path, console=Console(force_terminal=False))
    prompt = _build_system_prompt(ctx)
    assert "terse" in prompt.lower() or "brevity" in prompt.lower() or "2-3 sentence" in prompt
    assert "Never claim a command exists" in prompt


def test_run_ai_query_rejects_empty_question(tmp_path: Path, isolated_creds: Path, capsys) -> None:
    """Empty question should print an error and return without an API call."""
    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    changed = run_ai_query(ctx, "")
    assert changed is False
    out = capsys.readouterr().out
    assert "needs a question" in out


def test_run_ai_query_errors_when_no_api_key(tmp_path: Path, isolated_creds: Path, capsys) -> None:
    """With no env var and no credentials file, /ai points the user at /setup."""
    console = Console(force_terminal=False, width=120)
    ctx = ShellContext(root=tmp_path, console=console)
    changed = run_ai_query(ctx, "where do I start?")
    assert changed is False
    out = capsys.readouterr().out
    # v0.1.136: error now mentions no LLM backend (either Anthropic OR Bedrock).
    assert "no LLM backend configured" in out
    assert "/setup" in out
