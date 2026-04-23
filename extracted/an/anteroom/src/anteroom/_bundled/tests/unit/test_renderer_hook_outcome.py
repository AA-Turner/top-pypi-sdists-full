"""Unit tests for render_hook_outcome in cli/renderer.py (#1491)."""

from __future__ import annotations

import io
import re

import pytest
from rich.console import Console

from anteroom.cli import renderer
from anteroom.cli.themes import CliTheme


def _plain(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


@pytest.fixture(autouse=True)
def _restore_theme(monkeypatch: pytest.MonkeyPatch) -> None:  # type: ignore[return]
    monkeypatch.delenv("NO_COLOR", raising=False)
    yield
    renderer.set_theme(CliTheme.load("midnight"))


def _capture(fn: object) -> str:
    buf = io.StringIO()
    con = Console(file=buf, force_terminal=True, color_system=None, width=120, highlight=False)
    orig = renderer.console
    renderer.console = con
    try:
        fn()  # type: ignore[call-arg]
    finally:
        renderer.console = orig
    return _plain(buf.getvalue())


class TestRenderHookOutcomeDeny:
    def test_label_present(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("deny", "bash"))
        assert "Hook blocked" in out

    def test_tool_name_present(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("deny", "write_file"))
        assert "write_file" in out

    def test_message_present(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("deny", "bash", message="no network"))
        assert "no network" in out

    def test_hook_id_in_output(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("deny", "bash", hook_id="sec-hook"))
        assert "sec-hook" in out

    def test_no_crash_on_empty_tool_name(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("deny", ""))
        assert "Hook blocked" in out


class TestRenderHookOutcomeWarn:
    def test_label_present(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("warn", "bash", message="large output"))
        assert "Hook warning" in out

    def test_tool_name_present(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("warn", "read_file"))
        assert "read_file" in out

    def test_message_present(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("warn", "bash", message="output is large"))
        assert "output is large" in out


class TestRenderHookOutcomeAllow:
    def test_allow_produces_no_output(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("allow", "bash"))
        assert out.strip() == ""

    def test_allow_with_message_still_silent(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("allow", "bash", message="ignored"))
        assert out.strip() == ""


class TestRenderHookOutcomeTimeout:
    def test_timeout_produces_output(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("allow", "bash", error_type="timeout"))
        assert out.strip() != ""

    def test_timeout_mentions_timeout(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("allow", "bash", error_type="timeout"))
        assert "timed out" in out.lower() or "timeout" in out.lower()

    def test_timeout_does_not_say_blocked(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("allow", "bash", error_type="timeout"))
        assert "blocked" not in out.lower()


class TestRenderHookOutcomeException:
    def test_exception_produces_output(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("allow", "bash", error_type="exception"))
        assert out.strip() != ""

    def test_exception_does_not_say_blocked(self) -> None:
        out = _capture(lambda: renderer.render_hook_outcome("allow", "bash", error_type="exception"))
        assert "blocked" not in out.lower()


class TestRenderHookOutcomeAllThemes:
    @pytest.mark.parametrize("theme_name", ["midnight", "dawn", "high-contrast", "accessible"])
    def test_deny_renders_across_themes(self, theme_name: str) -> None:
        renderer.set_theme(CliTheme.load(theme_name))
        out = _capture(lambda: renderer.render_hook_outcome("deny", "bash", message="blocked"))
        assert "Hook blocked" in out
        assert "bash" in out
