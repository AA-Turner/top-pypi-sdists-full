"""Syrupy visual snapshot tests for tool-call lifecycle rendering (#1364).

Per `.claude/rules/ux-testing.md`: ``cli/renderer.py`` changes require Syrupy
snapshot coverage. Each snapshot captures the exact ANSI output for a tool-call
completion line across all four built-in themes so layout/ANSI drift shows up
as a reviewable diff.

The running-phase snapshot uses ``_tool_phase_label()`` after ``enter_tool_phase``
to confirm the ambient status label behaviour is unchanged.
"""

from __future__ import annotations

import io

import pytest
from rich.console import Console

import anteroom.cli.renderer as renderer
from anteroom.cli.themes import CliTheme

# Resolve Verbosity lazily via the live module — sibling test_renderer.py
# reloads the module, which would otherwise leave us with a stale enum class.
Verbosity = renderer.Verbosity

_THEME_NAMES = ["midnight", "dawn", "high-contrast", "accessible"]


@pytest.fixture(autouse=True)
def _clear_no_color(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)


@pytest.fixture(autouse=True)
def _restore_state() -> None:  # type: ignore[return]
    global Verbosity
    Verbosity = renderer.Verbosity
    renderer.set_theme(CliTheme.load("midnight"))
    renderer.set_verbosity(Verbosity.COMPACT)
    renderer.configure_live_tools(
        show_args_in_verbose=True,
        show_metric_suffix=True,
        metric_max_chars=40,
    )
    renderer._reset_tool_phase()
    yield
    Verbosity = renderer.Verbosity
    renderer.set_theme(CliTheme.load("midnight"))
    renderer.set_verbosity(Verbosity.COMPACT)
    renderer.configure_live_tools(
        show_args_in_verbose=True,
        show_metric_suffix=True,
        metric_max_chars=40,
    )
    renderer._reset_tool_phase()


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
    prev_console = renderer.console
    prev_stdout = renderer._stdout_console
    renderer.console = capture
    renderer._stdout_console = capture
    try:
        callable_()
    finally:
        renderer.console = prev_console
        renderer._stdout_console = prev_stdout
    return buf.getvalue()


class TestToolCompletionSuccess:
    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_snapshot(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        renderer.set_verbosity(Verbosity.COMPACT)
        out = _render_to_string(
            lambda: renderer.render_tool_call_completion(
                "read_file",
                "success",
                elapsed=0.5,
                arguments={"path": "src/foo.py"},
                output={"content": "a\nb\nc\nd\ne"},
            )
        )
        assert out == snapshot


class TestToolCompletionFailure:
    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_snapshot(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        renderer.set_verbosity(Verbosity.COMPACT)
        out = _render_to_string(
            lambda: renderer.render_tool_call_completion(
                "bash",
                "error",
                elapsed=1.2,
                arguments={"command": "ls /nope"},
                output={"error": "No such file or directory", "exit_code": 2},
            )
        )
        assert out == snapshot


class TestToolCompletionSuccessNoMetric:
    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_snapshot(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        renderer.set_verbosity(Verbosity.COMPACT)
        renderer.configure_live_tools(
            show_args_in_verbose=True,
            show_metric_suffix=False,
            metric_max_chars=40,
        )
        out = _render_to_string(
            lambda: renderer.render_tool_call_completion(
                "read_file",
                "success",
                elapsed=0.5,
                arguments={"path": "src/foo.py"},
                output={"content": "a\nb\nc\nd\ne"},
            )
        )
        assert out == snapshot


class TestToolCompletionVerboseWithArgs:
    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_snapshot(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        renderer.set_verbosity(Verbosity.VERBOSE)
        out = _render_to_string(
            lambda: renderer.render_tool_call_completion(
                "bash",
                "success",
                elapsed=0.4,
                arguments={"command": "echo hi"},
                output={"stdout": "hi\n", "exit_code": 0},
            )
        )
        assert out == snapshot


class TestRunningPhaseLabel:
    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_snapshot(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        renderer._reset_tool_phase()
        renderer.enter_tool_phase("read_file", {"path": "src/foo.py"})
        label = renderer._tool_phase_label()
        renderer._reset_tool_phase()
        # Snapshot the raw label string (theme-independent in shape); include
        # the theme name so any accidental theming change shows up per-theme.
        assert f"{theme_name}: {label}" == snapshot
