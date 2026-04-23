"""Visual snapshot tests for live markdown streaming (#1365).

Snapshots capture what the user sees at deterministic mid-stream boundaries
across all four built-in themes plus NO_COLOR. Chunks are fed deterministically
(no timing) and the Live region is driven into a fixed-width capture Console
so any ANSI/layout drift shows up as a reviewable Syrupy diff.
"""

from __future__ import annotations

import io
import re

import pytest
from rich.console import Console

from anteroom.cli import renderer
from anteroom.cli.streaming import StreamingMarkdownRenderer
from anteroom.cli.themes import CliTheme

_THEME_NAMES = ["midnight", "dawn", "high-contrast", "accessible"]
_ANSI_CSI_RE = re.compile(r"\x1b\[([0-9;?]*)([A-Za-z])")
_REDRAW_PREFIX_RE = re.compile(r"(?:\r?\x1b\[(?:\d+)?[AK])+")


@pytest.fixture(autouse=True)
def _clear_no_color(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)


@pytest.fixture(autouse=True)
def _restore_midnight_theme() -> None:  # type: ignore[return]
    yield
    renderer.set_theme(CliTheme.load("midnight"))


def _capture_console() -> tuple[Console, io.StringIO]:
    buf = io.StringIO()
    c = Console(
        file=buf,
        force_terminal=True,
        color_system="truecolor",
        width=80,
        highlight=False,
    )
    return c, buf


def _render_stream_to_string(chunks: list[str]) -> str:
    """Feed ``chunks`` through StreamingMarkdownRenderer with Live enabled,
    forcing a repaint opportunity after each chunk so the final snapshot
    reflects the deterministic visible output after the transient Live region
    settles into the canonical static render.
    """
    c, buf = _capture_console()
    # refresh_hz=60 (max) + monotonic advance forces near-per-chunk repaint.
    r = StreamingMarkdownRenderer(console=c, enabled=True, refresh_hz=60.0)
    for chunk in chunks:
        r.feed(chunk)
        # Force next feed to pass the throttle gate deterministically.
        r._last_render_ts = 0.0  # type: ignore[attr-defined]
    r.stop()
    return buf.getvalue()


def _render_narration_then_tool_to_string(narration: str) -> str:
    """Simulate the narration → tool_call_start → done sequence driving only
    the streaming renderer (the piece under test for #1471).

    ``flush_to_static`` is what ``render_tool_call_start`` calls before
    emitting tool output; ``stop`` is what ``render_response_end`` calls at
    end-of-turn. The sequence must settle the narration prose exactly once.

    Returns the output written by ``finalize_render`` — the canonical
    end-of-turn static render path — so the snapshot captures only what
    the user actually sees rather than the intermediate Live repaints and
    blank-frame operations that precede it.
    """
    from rich.markdown import Markdown
    from rich.padding import Padding

    c_live, _ = _capture_console()  # Live region writes here (cursor-movement noise)
    c_final, buf_final = _capture_console()  # finalize_render writes here (signal)
    r = StreamingMarkdownRenderer(
        console=c_live,
        enabled=True,
        refresh_hz=60.0,
        # Mirror render_assistant_prose's padding so the snapshot reflects
        # what that helper actually produces in production.
        finalize_render=lambda text: c_final.print(Padding(Markdown(text), (0, 2, 1, 2))),
    )
    r.feed(narration)
    r.flush_to_static()
    r.stop()
    return buf_final.getvalue()


def _normalize_snapshot_text(text: str) -> str:
    """Reduce Rich redraw output to the last visible frame."""
    sanitized = text
    last_redraw = None
    for match in _REDRAW_PREFIX_RE.finditer(sanitized):
        last_redraw = match
    if last_redraw is not None:
        sanitized = sanitized[last_redraw.end() :]

    scrubbed: list[str] = []
    i = 0
    while i < len(sanitized):
        if sanitized[i] == "\x1b":
            match = _ANSI_CSI_RE.match(sanitized, i)
            if match is None:
                i += 1
                continue
            _, final = match.groups()
            if final == "m":
                scrubbed.append(match.group(0))
            i = match.end()
            continue
        if sanitized[i] == "\r":
            i += 1
            continue
        scrubbed.append(sanitized[i])
        i += 1

    lines = "".join(scrubbed).splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(line.rstrip() for line in lines)


# ---------------------------------------------------------------------------
# Snapshots: three deterministic mid-stream boundaries x all themes + NO_COLOR
# ---------------------------------------------------------------------------


_PROSE_CHUNKS = [
    "This is ",
    "**bold** text ",
    "and `inline` code.",
]

_CODE_FENCE_CHUNKS = [
    "Here is Python:\n",
    "```python\n",
    "def hello():\n",
    "    return 'world'\n",
    "```\n",
    "Done.",
]

_TABLE_CHUNKS = [
    "| col A | col B |\n",
    "|-------|-------|\n",
    "| 1     | 2     |\n",
    "| 3     | 4     |\n",
]


class TestSnapshotNormalization:
    def test_strips_cursor_visibility_sequences(self) -> None:
        text = "\x1b[?25l  hello\nworld\x1b[?25h\n\n"
        assert _normalize_snapshot_text(text) == "  hello\nworld"

    def test_reduces_redraw_transcript_to_final_frame(self) -> None:
        text = (
            "  This is \x1b[1mbold\x1b[0m text\n"
            "\x1b[2K  This is \x1b[1mbold\x1b[0m text and "
            "\x1b[1;36;40minline\x1b[0m code.\n"
            "\x1b[2K  This is \x1b[1mbold\x1b[0m text and "
            "\x1b[1;36;40minline\x1b[0m code.\n\n"
            "\x1b[1A\x1b[2K  This is \x1b[1mbold\x1b[0m text and "
            "\x1b[1;36;40minline\x1b[0m code.\n"
        )
        assert _normalize_snapshot_text(text) == (
            "  This is \x1b[1mbold\x1b[0m text and \x1b[1;36;40minline\x1b[0m code."
        )


class TestProseBoundary:
    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_final_snapshot(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        out = _normalize_snapshot_text(_render_stream_to_string(_PROSE_CHUNKS))
        assert out == snapshot

    def test_no_color_snapshot(self, monkeypatch: pytest.MonkeyPatch, snapshot) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setenv("NO_COLOR", "1")
        renderer.set_theme(CliTheme.load("midnight"))
        out = _normalize_snapshot_text(_render_stream_to_string(_PROSE_CHUNKS))
        # With NO_COLOR set, Live is unavailable, so the streaming module
        # renders nothing itself (the caller handles the final static
        # render). The snapshot therefore captures the empty-Live branch.
        assert out == snapshot


class TestCodeFenceBoundary:
    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_final_snapshot(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        out = _normalize_snapshot_text(_render_stream_to_string(_CODE_FENCE_CHUNKS))
        assert out == snapshot


class TestTableBoundary:
    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_final_snapshot(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        out = _normalize_snapshot_text(_render_stream_to_string(_TABLE_CHUNKS))
        assert out == snapshot


# ---------------------------------------------------------------------------
# #1471: narration → tool → done must not duplicate the narration prose
# ---------------------------------------------------------------------------


_NARRATION_1471 = "I'm checking the config file layout first."


class TestNarrationBeforeToolBoundary:
    """Snapshot the visible output of a narration→tool→done sequence (#1471).

    Confirms that ``finalize_render`` (→ ``render_assistant_prose``) is
    invoked exactly once after ``flush_to_static()`` across all built-in
    themes. The snapshot captures only the ``finalize_render`` output —
    the canonical static render — so intermediate Live repaints and the
    blank-frame operation never pollute the assertion.

    A regression would show up as zero or two occurrences of the narration
    text in the ``finalize_render`` output and fail the explicit count
    assertion.
    """

    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_final_snapshot(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        raw = _render_narration_then_tool_to_string(_NARRATION_1471)
        out = _normalize_snapshot_text(raw)
        # finalize_render must be called exactly once — the count is taken
        # against the finalize_render-only buffer so Live repaints cannot
        # inflate it.
        import re as _re

        plain = _re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]", "", raw)
        assert plain.count(_NARRATION_1471) == 1
        assert out == snapshot

    def test_no_color_snapshot(self, monkeypatch: pytest.MonkeyPatch, snapshot) -> None:  # type: ignore[no-untyped-def]
        monkeypatch.setenv("NO_COLOR", "1")
        renderer.set_theme(CliTheme.load("midnight"))
        raw = _render_narration_then_tool_to_string(_NARRATION_1471)
        out = _normalize_snapshot_text(raw)
        # NO_COLOR disables Live: was_live=False so _print_static is skipped
        # and finalize_render is never called from this module. The caller
        # (renderer.render_response_end) owns the static render in that path.
        # The finalize_render-only buffer is therefore empty.
        assert raw == ""
        assert out == snapshot
