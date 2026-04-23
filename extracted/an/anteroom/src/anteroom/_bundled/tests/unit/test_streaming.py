"""Unit tests for the StreamingMarkdownRenderer (#1365).

Verifies the live-markdown streaming module's core contract:

- feed() accumulates text and renders a Markdown renderable into a Live region
- feed() is safe at every markdown boundary (mid-bold, mid-inline-code,
  mid-link, mid-code-fence, mid-table)
- the throttle respects refresh_hz (re-render cadence bounded)
- fallback path: non-TTY / NO_COLOR / disabled => true no-op
- stop() is idempotent
- flush_to_static() replaces the live region with a static print
"""

from __future__ import annotations

import io
from typing import Iterator

import pytest
from rich.console import Console

from anteroom.cli.streaming import StreamingMarkdownRenderer


@pytest.fixture
def tty_console() -> Console:
    """Return a capture Console that is recognised as a terminal."""
    buf = io.StringIO()
    return Console(
        file=buf,
        force_terminal=True,
        color_system="truecolor",
        width=80,
        highlight=False,
    )


@pytest.fixture
def nontty_console() -> Console:
    """Return a capture Console that is NOT a terminal."""
    buf = io.StringIO()
    return Console(
        file=buf,
        force_terminal=False,
        color_system=None,
        width=80,
        highlight=False,
    )


@pytest.fixture(autouse=True)
def _clear_no_color(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)


# ---------------------------------------------------------------------------
# Core lifecycle
# ---------------------------------------------------------------------------


class TestLifecycle:
    def test_starts_not_active(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        assert not r.is_active()

    def test_start_then_stop_roundtrip(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        r.start()
        assert r.is_active()
        r.stop()
        assert not r.is_active()

    def test_stop_is_idempotent(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        r.start()
        r.stop()
        # Second stop must not raise
        r.stop()
        assert not r.is_active()

    def test_feed_without_start_auto_starts(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        r.feed("hello")
        assert r.is_active()
        r.stop()

    def test_buffered_text_accumulates(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        r.feed("hello ")
        r.feed("world")
        assert r.buffered_text() == "hello world"
        r.stop()

    def test_stop_clears_buffer(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        r.feed("hello")
        r.stop()
        assert r.buffered_text() == ""

    def test_live_region_is_transient_before_static_finalize(self, tty_console: Console, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        seen: dict[str, bool] = {}

        class _FakeLive:
            def __init__(self, renderable, *, console, refresh_per_second, transient, vertical_overflow) -> None:
                seen["transient"] = transient

            def start(self) -> None:
                return None

            def stop(self) -> None:
                return None

            def update(self, renderable, refresh: bool = True) -> None:
                return None

        monkeypatch.setattr("anteroom.cli.streaming.Live", _FakeLive)
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        r.feed("hello")
        assert seen["transient"] is True
        r.stop()


# ---------------------------------------------------------------------------
# Fallback path — enabled=False or non-TTY is a pure no-op
# ---------------------------------------------------------------------------


class TestFallbackNoOp:
    def test_disabled_is_noop(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=False, refresh_hz=20.0)
        assert not r.live_available()
        r.feed("hello")
        assert not r.is_active()
        r.stop()
        # Output buffer must be empty (no Live attached)
        assert tty_console.file.getvalue() == ""  # type: ignore[attr-defined]

    def test_non_tty_auto_disables(self, nontty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=nontty_console, enabled=True, refresh_hz=20.0)
        assert not r.live_available()
        r.feed("some text")
        assert not r.is_active()
        r.stop()

    def test_no_color_env_auto_disables(self, tty_console: Console, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("NO_COLOR", "1")
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        assert not r.live_available()

    def test_disabled_accumulates_buffered_text(self, tty_console: Console) -> None:
        """Even when Live is disabled, the buffer still tracks text so the
        caller can finalize via a single render at turn end."""
        r = StreamingMarkdownRenderer(console=tty_console, enabled=False, refresh_hz=20.0)
        r.feed("part-one ")
        r.feed("part-two")
        assert r.buffered_text() == "part-one part-two"


# ---------------------------------------------------------------------------
# Incremental feed — final render matches complete-string render
# ---------------------------------------------------------------------------


def _chunked(text: str, size: int) -> Iterator[str]:
    for i in range(0, len(text), size):
        yield text[i : i + size]


class TestIncrementalFeed:
    def test_mid_bold_boundary_does_not_crash(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        for chunk in ["This is ", "**partial", " bold**", " closed."]:
            r.feed(chunk)
        assert "**partial bold**" in r.buffered_text()
        r.stop()

    def test_mid_inline_code_boundary_does_not_crash(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        for chunk in ["use ", "`foo", "_bar", "`", " function"]:
            r.feed(chunk)
        assert "`foo_bar`" in r.buffered_text()
        r.stop()

    def test_mid_link_boundary_does_not_crash(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        for chunk in ["see ", "[text](", "https://example.com", ")"]:
            r.feed(chunk)
        assert r.buffered_text() == "see [text](https://example.com)"
        r.stop()

    def test_mid_code_fence_does_not_crash(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        for chunk in ["intro\n", "```py\n", "def f():\n", "    return 1\n", "```\n", "done"]:
            r.feed(chunk)
        text = r.buffered_text()
        assert text.count("```") == 2
        assert "def f()" in text
        r.stop()

    def test_mid_table_does_not_crash(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        for chunk in ["| a | b |\n", "|---|---|\n", "| 1 | 2 |"]:
            r.feed(chunk)
        assert "| a | b |" in r.buffered_text()
        r.stop()


# ---------------------------------------------------------------------------
# Fenced-code awareness
# ---------------------------------------------------------------------------


class TestFencedCodeAwareness:
    def test_detects_unclosed_fence(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(
            console=tty_console,
            enabled=True,
            refresh_hz=20.0,
            code_fence_container=True,
        )
        r.feed("before ```py\ndef f()")
        assert r.in_unclosed_fence() is True
        r.stop()

    def test_closes_fence_on_trailing_triple_backticks(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(
            console=tty_console,
            enabled=True,
            refresh_hz=20.0,
            code_fence_container=True,
        )
        r.feed("```py\ndef f():\n    return 1\n```\n")
        assert r.in_unclosed_fence() is False
        r.stop()

    def test_even_fence_count_is_closed(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        r.feed("```a```b```c```")  # four fences => all closed pairs
        assert r.in_unclosed_fence() is False
        r.stop()

    def test_odd_fence_count_is_open(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        r.feed("start ```py\ncode")
        assert r.in_unclosed_fence() is True
        r.stop()


# ---------------------------------------------------------------------------
# Throttle — re-render count bounded by refresh_hz over wall-clock time
# ---------------------------------------------------------------------------


class TestThrottle:
    def test_many_feeds_dont_render_more_than_refresh_rate(self, tty_console: Console) -> None:
        """1000 rapid feed() calls must not issue 1000 renders.

        The exact count depends on refresh_hz and elapsed wall-clock time.
        We assert an upper bound that is clearly below the feed count so a
        regression to per-feed rendering shows up as a failure.
        """
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        for i in range(1000):
            r.feed(f"x{i}")
        # Render count should be far below 1000.
        assert r.render_count() < 100
        r.stop()


# ---------------------------------------------------------------------------
# flush_to_static — mid-turn tool-call interleave
# ---------------------------------------------------------------------------


class TestFlushToStatic:
    def test_flush_to_static_stops_live_and_prints(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        r.feed("mid-turn **narration**")
        r.flush_to_static()
        # After flush_to_static the Live region must be torn down and the
        # buffer cleared so the next feed starts a fresh turn segment.
        assert not r.is_active()
        assert r.buffered_text() == ""
        # Output was emitted through the console.
        output = tty_console.file.getvalue()  # type: ignore[attr-defined]
        assert "narration" in output

    def test_flush_to_static_preserves_live_height_on_blank(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        seen: dict[str, int] = {}
        probe_width = 24

        def _visible_rows(renderable: object) -> int:
            buf = io.StringIO()
            probe = Console(
                file=buf,
                force_terminal=True,
                color_system="truecolor",
                width=probe_width,
                highlight=False,
            )
            probe.print(renderable)
            return buf.getvalue().count("\n")

        class _HeightRecordingLive:
            def __init__(self, renderable, *, console, refresh_per_second, transient, vertical_overflow) -> None:
                self.console = console
                self.renderable = renderable
                seen["initial_height"] = _visible_rows(renderable)

            def start(self) -> None:
                return None

            def update(self, renderable, refresh: bool = True) -> None:
                self.renderable = renderable
                seen["blank_height"] = _visible_rows(renderable)

            def stop(self) -> None:
                return None

        monkeypatch.setattr("anteroom.cli.streaming.Live", _HeightRecordingLive)

        capture = Console(
            file=io.StringIO(),
            force_terminal=True,
            color_system="truecolor",
            width=probe_width,
            highlight=False,
        )
        r = StreamingMarkdownRenderer(console=capture, enabled=True, refresh_hz=20.0)
        r.feed("Here is code:\n```text\nalpha\nbeta\ngamma\n```")
        r.flush_to_static()

        assert seen["initial_height"] > 1
        assert seen["blank_height"] >= seen["initial_height"]

    def test_flush_to_static_noop_on_empty(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        # No feed yet — flush should be safe.
        r.flush_to_static()
        assert not r.is_active()

    def test_feed_after_flush_starts_new_region(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        r.feed("first segment")
        r.flush_to_static()
        r.feed("second segment")
        assert r.is_active()
        assert r.buffered_text() == "second segment"
        r.stop()


# ---------------------------------------------------------------------------
# Exec-mode gating
# ---------------------------------------------------------------------------


class TestExecMode:
    def test_exec_mode_disabled_without_override(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(
            console=tty_console,
            enabled=True,
            refresh_hz=20.0,
            exec_mode=True,
            live_in_exec_mode=False,
        )
        assert not r.live_available()

    def test_exec_mode_opt_in_enables_live(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(
            console=tty_console,
            enabled=True,
            refresh_hz=20.0,
            exec_mode=True,
            live_in_exec_mode=True,
        )
        assert r.live_available()


# ---------------------------------------------------------------------------
# Final render equivalence — finalize() emits same text via static render
# ---------------------------------------------------------------------------


class TestFinalize:
    def test_finalize_emits_full_text(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        r.feed("This is ")
        r.feed("**bold** and ")
        r.feed("`inline` code.")
        r.stop()
        # After stop(), the full text should have been rendered via the
        # console at least once (final static print).
        output = tty_console.file.getvalue()  # type: ignore[attr-defined]
        assert "bold" in output
        assert "inline" in output

    def test_finalize_whitespace_only_is_noop(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        r.feed("   \n  ")
        r.stop()
        output = tty_console.file.getvalue()  # type: ignore[attr-defined]
        # No visible content rendered (whitespace only is suppressed like
        # render_assistant_prose).
        assert output.strip() == ""


# ---------------------------------------------------------------------------
# Safety — never raises on pathological input
# ---------------------------------------------------------------------------


class TestSafety:
    def test_empty_feed_is_safe(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        r.feed("")
        r.stop()

    def test_very_long_run_is_safe(self, tty_console: Console) -> None:
        r = StreamingMarkdownRenderer(console=tty_console, enabled=True, refresh_hz=20.0)
        for _ in range(200):
            r.feed("lorem ipsum dolor sit amet. ")
        assert len(r.buffered_text()) == 200 * len("lorem ipsum dolor sit amet. ")
        r.stop()
