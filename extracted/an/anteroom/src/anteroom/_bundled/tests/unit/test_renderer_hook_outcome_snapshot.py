"""Syrupy visual snapshot tests for render_hook_outcome (#1491).

Covers all outcome variants across all built-in themes:
- deny with message
- deny without message (bare block)
- warn with message
- allow (should produce no output)
- timeout (error_type="timeout")
- exception (error_type="exception")
"""

from __future__ import annotations

import io
import sys

import pytest
from rich.console import Console

from anteroom.cli import renderer
from anteroom.cli.themes import CliTheme

_THEME_NAMES = ["midnight", "dawn", "high-contrast", "accessible"]


@pytest.fixture(autouse=True)
def _restore_midnight_theme(monkeypatch: pytest.MonkeyPatch) -> None:  # type: ignore[return]
    monkeypatch.delenv("NO_COLOR", raising=False)
    yield
    renderer.set_theme(CliTheme.load("midnight"))


def _render_to_string(callable_: object) -> str:
    buf = io.StringIO()
    capture = Console(
        file=buf,
        force_terminal=True,
        color_system="truecolor",
        width=80,
        highlight=False,
        record=False,
    )
    original_console = renderer.console
    original_stdout_console = renderer._stdout_console
    original_stdout = renderer._stdout
    renderer.console = capture
    renderer._stdout_console = capture
    renderer._stdout = sys.stdout
    try:
        callable_()  # type: ignore[call-arg]
    finally:
        renderer.console = original_console
        renderer._stdout_console = original_stdout_console
        renderer._stdout = original_stdout
    return buf.getvalue()


# ---------------------------------------------------------------------------
# deny with message
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("theme_name", _THEME_NAMES)
def test_hook_outcome_deny_with_message_snapshot(theme_name: str, snapshot: object) -> None:
    renderer.set_theme(CliTheme.load(theme_name))
    out = _render_to_string(
        lambda: renderer.render_hook_outcome(
            "deny",
            "bash",
            message="Network access is not permitted",
            hook_id="security-hook",
        )
    )
    assert out == snapshot


# ---------------------------------------------------------------------------
# deny without message
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("theme_name", _THEME_NAMES)
def test_hook_outcome_deny_no_message_snapshot(theme_name: str, snapshot: object) -> None:
    renderer.set_theme(CliTheme.load(theme_name))
    out = _render_to_string(lambda: renderer.render_hook_outcome("deny", "write_file"))
    assert out == snapshot


# ---------------------------------------------------------------------------
# warn (non-blocking)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("theme_name", _THEME_NAMES)
def test_hook_outcome_warn_snapshot(theme_name: str, snapshot: object) -> None:
    renderer.set_theme(CliTheme.load(theme_name))
    out = _render_to_string(
        lambda: renderer.render_hook_outcome(
            "warn",
            "bash",
            message="Large output detected",
        )
    )
    assert out == snapshot


# ---------------------------------------------------------------------------
# allow — must produce no output
# ---------------------------------------------------------------------------


def test_hook_outcome_allow_is_silent() -> None:
    out = _render_to_string(lambda: renderer.render_hook_outcome("allow", "bash"))
    assert out.strip() == ""


# ---------------------------------------------------------------------------
# timeout (error_type="timeout") — surfaced as warning
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("theme_name", _THEME_NAMES)
def test_hook_outcome_timeout_snapshot(theme_name: str, snapshot: object) -> None:
    renderer.set_theme(CliTheme.load(theme_name))
    out = _render_to_string(
        lambda: renderer.render_hook_outcome(
            "allow",
            "bash",
            hook_id="slow-hook",
            error_type="timeout",
        )
    )
    assert out == snapshot


# ---------------------------------------------------------------------------
# exception (error_type="exception") — surfaced as warning
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("theme_name", _THEME_NAMES)
def test_hook_outcome_exception_snapshot(theme_name: str, snapshot: object) -> None:
    renderer.set_theme(CliTheme.load(theme_name))
    out = _render_to_string(
        lambda: renderer.render_hook_outcome(
            "allow",
            "bash",
            hook_id="buggy-hook",
            error_type="exception",
        )
    )
    assert out == snapshot
