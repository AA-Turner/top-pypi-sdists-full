"""Snapshot-style renderer tests for tool-result density (#1367).

Captures the observable output of ``render_tool_call_end`` across the four
density modes and documents the "normal is byte-identical" contract.

These are string-based snapshots (not Syrupy ambr) so they stay readable in
diffs and consistent with the rest of the renderer test suite.
"""

from __future__ import annotations

import io
import re
from typing import Any, Iterable

import pytest
from rich.console import Console

import anteroom.cli.renderer as renderer
from anteroom.cli.density import ToolResultDensity
from anteroom.cli.renderer import (
    Verbosity,
    configure_density,
    render_tool_call_end,
    render_tool_call_start,
    render_tool_expand,
    set_density,
    set_verbosity,
)
from anteroom.cli.themes import CliTheme

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _strip_ansi(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def _capture() -> tuple[Console, io.StringIO]:
    buf = io.StringIO()
    con = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
    return con, buf


@pytest.fixture(autouse=True)
def _reset_renderer_state(monkeypatch: pytest.MonkeyPatch) -> Iterable[None]:
    monkeypatch.delenv("NO_COLOR", raising=False)
    renderer.set_theme(CliTheme.load("midnight"))
    set_verbosity(Verbosity.COMPACT)
    set_density(ToolResultDensity.NORMAL)
    # Reset density knobs to defaults for each test (collapse_repeats is
    # default-True in CliDensityConfig; explicit tests flip it).
    configure_density(
        head_lines=3,
        tail_lines=2,
        diff_context_lines=3,
        collapse_repeats=True,
    )
    renderer._dedup_key = ""
    renderer._dedup_count = 0
    renderer._dedup_first_summary = ""
    renderer._dedup_summary = ""
    renderer._tool_batch_active = False
    renderer._tool_dedup_enabled = True
    renderer._current_turn_tools.clear()
    renderer._tool_history.clear()
    # Reset collapse-repeats rolling state (added for #1367 wiring).
    renderer._repeat_shape_hash = ""
    renderer._repeat_count = 0
    renderer._repeat_summary = ""
    yield
    renderer.set_theme(CliTheme.load("midnight"))
    set_verbosity(Verbosity.COMPACT)
    set_density(ToolResultDensity.NORMAL)
    configure_density(
        head_lines=3,
        tail_lines=2,
        diff_context_lines=3,
        collapse_repeats=True,
    )
    renderer._repeat_shape_hash = ""
    renderer._repeat_count = 0
    renderer._repeat_summary = ""


def _run_tool(tool_name: str, args: dict, status: str, output: dict) -> str:
    con, buf = _capture()
    original_console = renderer.console
    renderer.console = con
    try:
        renderer._tool_start = 0.0  # elapsed will be ~now; strip from output
        render_tool_call_start(tool_name, args)
        render_tool_call_end(tool_name, status, output)
    finally:
        renderer.console = original_console
    text = _strip_ansi(buf.getvalue())
    # Normalise the elapsed-seconds portion so snapshots stay stable.
    text = re.sub(r"\d+\.\d+s", "Xs", text)
    return text


def _run_tool_sequence(calls: list[tuple[str, dict, str, Any]]) -> str:
    """Run multiple tool calls through the renderer, collect the full output.

    ``calls`` is a list of ``(tool_name, args, status, output)`` tuples.
    """
    con, buf = _capture()
    original_console = renderer.console
    renderer.console = con
    try:
        for tool_name, args, status, output in calls:
            renderer._tool_start = 0.0
            render_tool_call_start(tool_name, args)
            render_tool_call_end(tool_name, status, output)
    finally:
        renderer.console = original_console
    text = _strip_ansi(buf.getvalue())
    text = re.sub(r"\d+\.\d+s", "Xs", text)
    return text


def _flush_repeats_for_assertion() -> str:
    """Trigger a repeat-collapse flush and return any emitted text.

    The renderer emits the ``× N`` summary lazily; for tests that want to
    assert on its content we call the flush helper and capture the output.
    """
    con, buf = _capture()
    original_console = renderer.console
    renderer.console = con
    try:
        renderer._flush_repeat_collapse()
    finally:
        renderer.console = original_console
    return _strip_ansi(buf.getvalue())


# ---------------------------------------------------------------------------
# Byte-identical contract: NORMAL is unchanged vs. today
# ---------------------------------------------------------------------------


class TestNormalByteIdentical:
    def test_normal_matches_legacy_success(self) -> None:
        """Density NORMAL must produce exactly the same line the pre-#1367 path emits."""
        out = _run_tool("bash", {"command": "echo hi"}, "success", {"stdout": "hi"})
        # ✓ icon + humanised summary + elapsed
        assert "✓" in out
        assert "Ran echo hi" in out
        # NORMAL does not emit a "[+N lines]" hint.
        assert "[+" not in out

    def test_normal_error_matches_legacy(self) -> None:
        out = _run_tool("bash", {"command": "false"}, "error", {"error": "exit 1"})
        assert "✗" in out
        assert "Ran false" in out
        assert "exit 1" in out


# ---------------------------------------------------------------------------
# MINIMAL: body hidden, success row only
# ---------------------------------------------------------------------------


class TestMinimalMode:
    def test_minimal_hides_body(self) -> None:
        set_density(ToolResultDensity.MINIMAL)
        big_output = "\n".join(f"line-{i}" for i in range(30))
        out = _run_tool("bash", {"command": "ls"}, "success", {"stdout": big_output})
        # The humanised summary is always present.
        assert "Ran ls" in out
        # But the body is not inlined.
        assert "line-0" not in out
        assert "line-29" not in out


# ---------------------------------------------------------------------------
# COMPACT: adds a [+N lines] hint if body is long
# ---------------------------------------------------------------------------


class TestCompactMode:
    def test_compact_adds_hint_for_long_output(self) -> None:
        set_density(ToolResultDensity.COMPACT)
        big_output = "\n".join(f"line-{i}" for i in range(30))
        out = _run_tool("bash", {"command": "ls"}, "success", {"stdout": big_output})
        assert "Ran ls" in out
        # Compact ships a hint indicating the body was trimmed.
        assert "[+" in out and "lines]" in out

    def test_compact_no_hint_for_short_output(self) -> None:
        set_density(ToolResultDensity.COMPACT)
        out = _run_tool("bash", {"command": "echo"}, "success", {"stdout": "hi"})
        assert "Ran echo" in out
        assert "[+" not in out


# ---------------------------------------------------------------------------
# DETAILED: inlines the body
# ---------------------------------------------------------------------------


class TestDetailedMode:
    def test_detailed_inlines_short_output(self) -> None:
        set_density(ToolResultDensity.DETAILED)
        out = _run_tool("bash", {"command": "echo"}, "success", {"stdout": "hello"})
        assert "Ran echo" in out
        # Detailed prints the body inline.
        assert "hello" in out


# ---------------------------------------------------------------------------
# Error salience in non-NORMAL modes
# ---------------------------------------------------------------------------


class TestErrorSalience:
    def test_error_marker_in_compact(self) -> None:
        set_density(ToolResultDensity.COMPACT)
        out = _run_tool("bash", {"command": "false"}, "error", {"error": "boom"})
        assert "✗" in out
        assert "boom" in out

    def test_error_marker_in_minimal(self) -> None:
        set_density(ToolResultDensity.MINIMAL)
        out = _run_tool("bash", {"command": "false"}, "error", {"error": "boom"})
        # Even in minimal mode, errors must be visible.
        assert "✗" in out
        assert "boom" in out


# ---------------------------------------------------------------------------
# collapse_repeats wiring (Blocker 1, #1367 follow-up)
#
# ``cli.density.collapse_repeats`` is a user-facing knob documented and plumbed
# from config; these tests guarantee it actually affects rendering.
# ---------------------------------------------------------------------------


def _count_result_rows(out: str, summary_fragment: str) -> int:
    """Count the number of completed result rows (``✓ <summary>``) in ``out``.

    ``render_tool_call_start`` also prints the summary as a breadcrumb; we
    only want the ``✓`` completion lines for collapse-repeats assertions.

    The completion line produced by ``render_tool_call_completion`` uses a
    past-tense verb form (e.g. ``Ran echo hi`` rather than ``bash echo hi``),
    so for bash-tool cases the caller may pass a partial target fragment
    (``echo hi``) that matches post-``✓`` on the unified line.
    """
    count = 0
    for line in out.split("\n"):
        if "✓" in line and summary_fragment in line:
            count += 1
    return count


class TestCollapseRepeatsCompact:
    """In compact + collapse_repeats=True, identical successive outputs collapse."""

    def test_three_identical_outputs_collapse_to_one_summary_plus_count(self) -> None:
        set_density(ToolResultDensity.COMPACT)
        configure_density(collapse_repeats=True)
        # Disable the verb-level dedup so we isolate collapse_repeats behaviour.
        renderer._tool_dedup_enabled = False

        # Three bash calls with IDENTICAL stdout payload.
        payload = {"stdout": "same-line-1\nsame-line-2"}
        out = _run_tool_sequence(
            [
                ("bash", {"command": "echo hi"}, "success", payload),
                ("bash", {"command": "echo hi"}, "success", payload),
                ("bash", {"command": "echo hi"}, "success", payload),
            ]
        )
        # Flush lazily-emitted "× N" line.
        out += _flush_repeats_for_assertion()

        # Exactly one success row rendered; the other two are suppressed.
        assert _count_result_rows(out, "Ran echo hi") == 1
        # And somewhere we see a repeat indicator with count 3.
        assert "× 3" in out

    def test_compact_collapse_repeats_false_no_collapse(self) -> None:
        """With collapse_repeats=False the legacy render path stays."""
        set_density(ToolResultDensity.COMPACT)
        configure_density(collapse_repeats=False)
        renderer._tool_dedup_enabled = False

        payload = {"stdout": "same-line"}
        out = _run_tool_sequence(
            [
                ("bash", {"command": "echo hi"}, "success", payload),
                ("bash", {"command": "echo hi"}, "success", payload),
                ("bash", {"command": "echo hi"}, "success", payload),
            ]
        )
        out += _flush_repeats_for_assertion()
        # Each call renders its own success row — three total.
        assert _count_result_rows(out, "Ran echo hi") == 3
        # No repeat indicator.
        assert "× " not in out

    def test_different_outputs_do_not_collapse(self) -> None:
        set_density(ToolResultDensity.COMPACT)
        configure_density(collapse_repeats=True)
        renderer._tool_dedup_enabled = False

        out = _run_tool_sequence(
            [
                ("bash", {"command": "echo a"}, "success", {"stdout": "a"}),
                ("bash", {"command": "echo b"}, "success", {"stdout": "b"}),
                ("bash", {"command": "echo c"}, "success", {"stdout": "c"}),
            ]
        )
        out += _flush_repeats_for_assertion()
        # All three distinct success rows render.
        assert _count_result_rows(out, "Ran echo a") == 1
        assert _count_result_rows(out, "Ran echo b") == 1
        assert _count_result_rows(out, "Ran echo c") == 1
        # No collapse count because outputs differ.
        assert "× " not in out


class TestCollapseRepeatsNormal:
    """Normal density must stay byte-identical regardless of collapse_repeats."""

    def test_normal_never_collapses_even_when_enabled(self) -> None:
        """Hard-gate: the ``normal`` default must not change when
        collapse_repeats=True. The knob is an opt-in feature of compact/minimal."""
        set_density(ToolResultDensity.NORMAL)
        configure_density(collapse_repeats=True)
        renderer._tool_dedup_enabled = False

        payload = {"stdout": "same"}
        out = _run_tool_sequence(
            [
                ("bash", {"command": "echo hi"}, "success", payload),
                ("bash", {"command": "echo hi"}, "success", payload),
                ("bash", {"command": "echo hi"}, "success", payload),
            ]
        )
        out += _flush_repeats_for_assertion()
        # Three independent success rows, no collapse marker.
        assert _count_result_rows(out, "Ran echo hi") == 3
        assert "× " not in out


class TestCollapseRepeatsMinimal:
    def test_minimal_collapse_repeats_emits_count(self) -> None:
        set_density(ToolResultDensity.MINIMAL)
        configure_density(collapse_repeats=True)
        renderer._tool_dedup_enabled = False

        payload = {"stdout": "ignored-in-minimal"}
        out = _run_tool_sequence(
            [
                ("bash", {"command": "echo hi"}, "success", payload),
                ("bash", {"command": "echo hi"}, "success", payload),
            ]
        )
        out += _flush_repeats_for_assertion()
        # One success row + a × 2 indicator.
        assert _count_result_rows(out, "Ran echo hi") == 1
        assert "× 2" in out


# ---------------------------------------------------------------------------
# /expand on diff-backed write_file / edit_file (Blocker 2, #1367 follow-up)
# ---------------------------------------------------------------------------


_UNCOLLAPSED_MARKER_RE = re.compile(r"\[\d+ unchanged lines\]")


def _big_edit_payload() -> dict:
    """Return an edit_file success payload with a diff that has a long context run.

    Two changes ~6 lines apart produce a single unified-diff hunk with enough
    unchanged context between them for ``collapse_diff_hunks`` to trigger in
    compact mode.
    """
    old_lines = [f"line-{i}" for i in range(30)]
    new_lines = list(old_lines)
    new_lines[5] = "line-5-CHANGED"
    new_lines[11] = "line-11-CHANGED"
    return {
        "path": "/tmp/example.py",
        "_old_content": "\n".join(old_lines) + "\n",
        "_new_content": "\n".join(new_lines) + "\n",
    }


class TestExpandOnDiffBackedResults:
    """``/expand`` must show the full, un-collapsed diff for write/edit results."""

    def test_expand_on_edit_file_renders_full_diff_without_collapse_marker(self) -> None:
        set_density(ToolResultDensity.COMPACT)
        configure_density(diff_context_lines=1)
        payload = _big_edit_payload()

        # Initial (compact) render — hunks collapse unchanged context.
        initial = _run_tool("edit_file", {"path": "/tmp/example.py"}, "success", payload)
        assert _UNCOLLAPSED_MARKER_RE.search(initial), (
            "Setup: compact density should insert an '[N unchanged lines]' marker"
        )

        # Now call /expand — it must re-render with un-collapsed context.
        con, buf = _capture()
        original_console = renderer.console
        renderer.console = con
        try:
            render_tool_expand()
        finally:
            renderer.console = original_console
        expanded = _strip_ansi(buf.getvalue())

        # The expanded render must NOT contain the collapse marker.
        assert not _UNCOLLAPSED_MARKER_RE.search(expanded), f"/expand must bypass hunk-collapsing; got:\n{expanded}"
        # Both changed lines appear.
        assert "line-5-CHANGED" in expanded
        assert "line-11-CHANGED" in expanded
        # Every middle-context line between the two changes appears
        # (compact would have collapsed some into the [N unchanged lines] marker).
        for i in range(6, 11):
            assert f"line-{i}" in expanded, f"expected middle-context line-{i} in /expand output"

    def test_expand_on_write_file_renders_full_diff_without_collapse_marker(self) -> None:
        set_density(ToolResultDensity.COMPACT)
        configure_density(diff_context_lines=1)
        payload = _big_edit_payload()
        # For write_file we use the diff shape (not the ``action=created`` path).
        initial = _run_tool("write_file", {"path": "/tmp/example.py"}, "success", payload)
        assert _UNCOLLAPSED_MARKER_RE.search(initial)

        con, buf = _capture()
        original_console = renderer.console
        renderer.console = con
        try:
            render_tool_expand()
        finally:
            renderer.console = original_console
        expanded = _strip_ansi(buf.getvalue())

        assert not _UNCOLLAPSED_MARKER_RE.search(expanded)
        assert "line-5-CHANGED" in expanded
        assert "line-11-CHANGED" in expanded
        for i in range(6, 11):
            assert f"line-{i}" in expanded

    def test_normal_render_still_collapses_hunks_per_density(self) -> None:
        """Hard-gate: /expand must not change the normal (non-expand) render path."""
        set_density(ToolResultDensity.COMPACT)
        configure_density(diff_context_lines=1)
        payload = _big_edit_payload()
        out = _run_tool("edit_file", {"path": "/tmp/example.py"}, "success", payload)
        # Compact collapse marker is still present in the normal compact render.
        assert _UNCOLLAPSED_MARKER_RE.search(out)

    def test_expand_still_works_for_non_diff_tool_result(self) -> None:
        """Non-diff tool outputs keep the bulk-text expansion behaviour."""
        set_density(ToolResultDensity.COMPACT)
        big_output = "\n".join(f"line-{i}" for i in range(20))
        _run_tool("bash", {"command": "ls"}, "success", {"stdout": big_output})

        con, buf = _capture()
        original_console = renderer.console
        renderer.console = con
        try:
            render_tool_expand()
        finally:
            renderer.console = original_console
        expanded = _strip_ansi(buf.getvalue())
        # Detailed expansion shows all 20 lines.
        for i in range(20):
            assert f"line-{i}" in expanded


# ---------------------------------------------------------------------------
# Repeat-collapse key must include diff payload (#1367 review follow-up)
#
# Regression for the review blocker: the shape/signature key used by
# ``_repeat_shape_key`` previously stripped all ``_``-prefixed fields, which
# meant two distinct ``write_file`` / ``edit_file`` diffs with the same path
# collapsed into a single ``↻ … × N`` line even though the diffs differed.
# That hid real file changes from the user. The regression tests below pin
# the fixed behaviour: distinct diffs NEVER collapse, identical ones still do.
# ---------------------------------------------------------------------------


class TestCollapseRepeatsDoesNotCollideDistinctDiffs:
    def test_distinct_write_file_diffs_same_path_do_not_collapse(self) -> None:
        """Two write_file calls, same path, DIFFERENT diff payloads must render as TWO rows."""
        set_density(ToolResultDensity.COMPACT)
        configure_density(collapse_repeats=True)
        renderer._tool_dedup_enabled = False

        payload_a = {"path": "/tmp/a.py", "_old_content": "foo\n", "_new_content": "bar\n"}
        payload_b = {"path": "/tmp/a.py", "_old_content": "alpha\n", "_new_content": "omega\n"}
        out = _run_tool_sequence(
            [
                ("write_file", {"path": "/tmp/a.py"}, "success", payload_a),
                ("write_file", {"path": "/tmp/a.py"}, "success", payload_b),
            ]
        )
        out += _flush_repeats_for_assertion()
        # Distinct diffs must NOT be collapsed into a "× N" line.
        assert "× " not in out, f"distinct diffs must not collapse; got:\n{out}"
        # Both concrete diff bodies appear somewhere in the output.
        assert "foo" in out and "bar" in out
        assert "alpha" in out and "omega" in out

    def test_distinct_edit_file_diffs_same_path_do_not_collapse(self) -> None:
        set_density(ToolResultDensity.COMPACT)
        configure_density(collapse_repeats=True)
        renderer._tool_dedup_enabled = False

        payload_a = {"path": "/tmp/b.py", "_old_content": "keep\nline1\n", "_new_content": "keep\nline1-X\n"}
        payload_b = {"path": "/tmp/b.py", "_old_content": "keep\nline2\n", "_new_content": "keep\nline2-Y\n"}
        out = _run_tool_sequence(
            [
                ("edit_file", {"path": "/tmp/b.py"}, "success", payload_a),
                ("edit_file", {"path": "/tmp/b.py"}, "success", payload_b),
            ]
        )
        out += _flush_repeats_for_assertion()
        assert "× " not in out, f"distinct edit diffs must not collapse; got:\n{out}"
        # Confirm both distinct diff bodies are present.
        assert "line1-X" in out
        assert "line2-Y" in out

    def test_identical_write_file_diffs_still_collapse(self) -> None:
        """Symmetric positive test: two IDENTICAL diffs still collapse."""
        set_density(ToolResultDensity.COMPACT)
        configure_density(collapse_repeats=True)
        renderer._tool_dedup_enabled = False

        payload = {"path": "/tmp/c.py", "_old_content": "same\n", "_new_content": "same-CHANGED\n"}
        out = _run_tool_sequence(
            [
                ("write_file", {"path": "/tmp/c.py"}, "success", dict(payload)),
                ("write_file", {"path": "/tmp/c.py"}, "success", dict(payload)),
                ("write_file", {"path": "/tmp/c.py"}, "success", dict(payload)),
            ]
        )
        out += _flush_repeats_for_assertion()
        # Identical diffs must still collapse — shape hash should match.
        assert "× 3" in out, f"identical diffs must still collapse; got:\n{out}"
