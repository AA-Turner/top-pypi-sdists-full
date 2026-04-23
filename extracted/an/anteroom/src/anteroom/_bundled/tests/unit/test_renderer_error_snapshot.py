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


def _render_to_string(callable_) -> str:  # type: ignore[no-untyped-def]
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
        callable_()
    finally:
        renderer.console = original_console
        renderer._stdout_console = original_stdout_console
        renderer._stdout = original_stdout
    return buf.getvalue()


@pytest.mark.parametrize("theme_name", _THEME_NAMES)
def test_error_snapshot(theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
    renderer.set_theme(CliTheme.load(theme_name))
    out = _render_to_string(
        lambda: renderer.render_error(
            {
                "message": "Cannot connect to API (3 attempts).",
                "suggestion": "Check AI_CHAT_BASE_URL (http://localhost:11434/v1)",
            }
        )
    )
    assert out == snapshot
