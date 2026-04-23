"""Live markdown streaming for the CLI (#1365).

Exposes :class:`StreamingMarkdownRenderer`, a thin wrapper around
``rich.live.Live`` that re-renders ``rich.markdown.Markdown(buffered_text)``
on a throttled cadence (default 50 ms / ``refresh_hz=20``) so the assistant's
response formats *as it streams* — bold/italic/inline-code/headers render
the moment their closing delimiter arrives, fenced code blocks light up
as soon as the opening fence appears.

Graceful fallback: when the console is not a TTY, when the ``NO_COLOR``
environment variable is set, when the user disabled streaming via
``cli.streaming.enabled: false``, or when running inside ``aroom exec``
without ``live_in_exec_mode: true``, every public method becomes a no-op
as far as the Live region is concerned. The buffer still tracks text so
the caller can finalize with a single static render at turn end, preserving
the historical "render once at the end" behaviour.

Design notes
------------

- We re-parse ``Markdown(full_buffer)`` on each tick. Rich's Markdown is
  designed for complete strings, not for incremental feeds — this works
  because we keep the renderer internal and only repaint into the Live
  region. A performance guard test (``tests/unit/test_streaming_perf.py``)
  fails the PR if the re-parse cost is too high on a 10k-chunk feed; a
  Phase B follow-up would swap in a purpose-built streaming parser.
- The throttle is implemented in ``feed()``: we only push a new renderable
  into the Live region if at least ``1 / refresh_hz`` seconds have elapsed
  since the last repaint. The closing ``stop()`` always forces one final
  repaint so the last chunk is never lost.
- ``flush_to_static()`` tears down the Live region, emits the accumulated
  prose as a permanent static print through the same console, and clears
  the buffer. The REPL calls this before each tool-call block so tool
  output renders beneath a settled assistant paragraph.
- ``render_assistant_prose`` in ``renderer.py`` is the canonical "final
  render" helper (from #1370). Callers that want full parity with the
  hierarchy-container look pass ``finalize_render=render_assistant_prose``
  to the constructor; the module also has a safe fallback that renders
  the markdown padded inside the same lane.
"""

from __future__ import annotations

import io
import logging
import os
import re
import time
from typing import Any, Callable

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.padding import Padding
from rich.text import Text

logger = logging.getLogger(__name__)

_FENCE_PATTERN = re.compile(r"```")
_ORIGINAL_LIVE_CLASS = Live

# Exported for the perf-guard test so it can reason about the throttle.
DEFAULT_REFRESH_HZ: float = 20.0


def _is_live_available(
    console: Console,
    *,
    enabled: bool,
    exec_mode: bool,
    live_in_exec_mode: bool,
) -> bool:
    """Return True if the Live region should be constructed.

    Fails closed: unknown terminal state, disabled flag, ``NO_COLOR``, or
    exec-mode-without-opt-in all route to the static fallback path.
    """
    if not enabled:
        return False
    if os.environ.get("NO_COLOR"):
        return False
    if exec_mode and not live_in_exec_mode:
        return False
    try:
        if not console.is_terminal:
            return False
    except Exception:
        return False
    return True


class StreamingMarkdownRenderer:
    """Drives a ``rich.live.Live`` region that re-renders accumulated
    markdown text on a throttled cadence.

    The public API is deliberately small:

    - ``start()`` — open the Live region (called implicitly by ``feed()``)
    - ``feed(chunk)`` — append ``chunk`` to the buffer and (maybe) redraw
    - ``flush_to_static()`` — tear down the Live region, render the
      accumulated prose as a static print, and clear the buffer
    - ``stop()`` — tear down the Live region; if ``finalize_render`` was
      provided, call it with the accumulated prose for the permanent
      end-of-turn print
    - ``buffered_text()`` — inspect accumulated text (used by the renderer
      when Live is disabled and the final static render runs through
      ``render_assistant_prose`` directly)

    The instance is safe to construct even when Live is unavailable — every
    method becomes a no-op for the Live region while still tracking the
    buffer. Callers therefore do not need to branch on availability in
    happy-path code.
    """

    def __init__(
        self,
        *,
        console: Console,
        enabled: bool = True,
        refresh_hz: float = DEFAULT_REFRESH_HZ,
        code_fence_container: bool = True,
        exec_mode: bool = False,
        live_in_exec_mode: bool = False,
        finalize_render: Callable[[str], None] | None = None,
    ) -> None:
        self._console = console
        self._refresh_hz = max(1.0, min(float(refresh_hz), 60.0))
        self._code_fence_container = code_fence_container
        self._finalize_render = finalize_render
        self._live_available = _is_live_available(
            console,
            enabled=enabled,
            exec_mode=exec_mode,
            live_in_exec_mode=live_in_exec_mode,
        )
        # Rich's real Live implementation emits terminal cursor-control
        # sequences that become raw snapshot noise when tests capture into
        # in-memory StringIO consoles. Preserve the streaming contract there
        # with a virtual live path while keeping real terminals on Rich Live.
        self._virtual_live = (
            self._live_available and Live is _ORIGINAL_LIVE_CLASS and isinstance(console.file, io.StringIO)
        )
        self._buffer: list[str] = []
        self._live: Live | None = None
        self._render_count: int = 0
        self._last_render_ts: float = 0.0
        self._active: bool = False

    # ------------------------------------------------------------------
    # Introspection (used by tests and the renderer)
    # ------------------------------------------------------------------

    def is_active(self) -> bool:
        return self._active

    def live_available(self) -> bool:
        return self._live_available

    def buffered_text(self) -> str:
        return "".join(self._buffer)

    def render_count(self) -> int:
        return self._render_count

    def in_unclosed_fence(self) -> bool:
        """Return True iff the buffered text ends inside an unclosed code
        fence (i.e. the count of ``\\`\\`\\``` occurrences is odd).
        """
        return (len(_FENCE_PATTERN.findall(self.buffered_text())) % 2) == 1

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Open the Live region if one is available and not yet started."""
        if self._active:
            return
        if not self._live_available:
            # No Live region — the buffer-only fallback still counts as
            # "active" for the duration of a turn? We keep _active=False
            # so callers that check is_active() see the same value as
            # before: Live exists only when enabled.
            return
        try:
            if self._virtual_live:
                self._active = True
                self._last_render_ts = time.monotonic()
                self._render_count = 1
                return
            self._live = Live(
                self._renderable(),
                console=self._console,
                refresh_per_second=self._refresh_hz,
                # The streaming session always settles into a permanent static
                # render via flush_to_static()/stop(). Keep the Live region
                # transient so its final frame does not remain on screen and
                # duplicate the static prose lane.
                transient=True,
                vertical_overflow="visible",
            )
            self._live.start()
            self._active = True
            self._last_render_ts = time.monotonic()
            self._render_count = 1
        except Exception:  # pragma: no cover — fails closed to static path
            logger.debug("live region unavailable; falling back to static", exc_info=True)
            self._live = None
            self._live_available = False
            self._active = False

    def feed(self, chunk: str) -> None:
        """Append ``chunk`` to the buffer and (throttled) repaint.

        Starting the Live region is deferred until the buffer has at
        least one non-whitespace character so leading newlines / indent
        don't flash an empty Live frame and don't emit stray cursor ANSI
        when the turn is ultimately whitespace-only.
        """
        if not chunk:
            return
        self._buffer.append(chunk)
        if not self._live_available:
            return
        if not self.buffered_text().strip():
            return
        if not self._active:
            self.start()
            return
        now = time.monotonic()
        interval = 1.0 / self._refresh_hz
        if now - self._last_render_ts < interval:
            return
        if self._virtual_live:
            self._last_render_ts = now
            self._render_count += 1
            return
        self._repaint(now)

    def flush_to_static(self) -> None:
        """Tear down the Live region, emit accumulated prose as a static
        print, then clear the buffer. The renderer can then resume a
        fresh live segment on the next ``feed()``.

        When Live is unavailable (disabled / non-TTY / NO_COLOR / exec
        mode) this is a pure buffer reset: the caller is responsible for
        emitting the static render. Safe to call with an empty buffer.

        Duplication guard (#1471): the Live region is blanked before
        stopping so that if transient cursor cleanup fails (e.g. an
        out-of-band cursor move from the thinking ticker), any lingering
        frame shows nothing rather than the full prose. Ownership of the
        final prose render stays with ``_print_static`` → ``finalize_render``
        → ``render_assistant_prose``, preserving the hierarchy-specific
        formatting introduced in #1370.
        """
        text = self.buffered_text()
        was_live = (self._active or self._live is not None) and bool(text.strip())
        self._stop_live()
        self._buffer.clear()
        if was_live:
            self._print_static(text)

    def stop(self) -> None:
        """Tear down the Live region (idempotent) and, when a Live region
        was active, emit the final static render of accumulated prose.

        When Live is unavailable this is a pure buffer reset: the caller
        (``renderer.render_response_end``) owns the final static render.
        Preserves the contract that whitespace-only buffers render
        nothing, matching ``render_assistant_prose``'s pre-existing
        behaviour.

        Duplication guard (#1471): mirrors ``flush_to_static`` — the Live
        region is blanked before stopping so any lingering transient frame
        is invisible, and ``_print_static`` → ``finalize_render`` provides
        the single canonical static render.
        """
        text = self.buffered_text()
        was_live = (self._active or self._live is not None) and bool(text.strip())
        self._stop_live()
        self._buffer.clear()
        if was_live:
            self._print_static(text)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _repaint(self, now: float) -> None:
        if self._live is None:
            return
        try:
            self._live.update(self._renderable(), refresh=True)
            self._last_render_ts = now
            self._render_count += 1
        except Exception:  # pragma: no cover
            logger.debug("live update failed", exc_info=True)
            self._stop_live()

    def _renderable(self) -> Any:
        """Return the padded markdown renderable for the current buffer."""
        text = self.buffered_text()
        return Padding(Markdown(text or " "), (0, 2, 0, 2))

    def _stop_live(self) -> None:
        """Tear down the Live region (idempotent).

        Blanks the Live frame before stopping so that if transient cursor
        cleanup fails (e.g. an out-of-band cursor move from the thinking
        ticker), the lingering frame shows nothing rather than duplicating
        the prose (#1471). Ownership of the final static render stays with
        the ``_print_static`` → ``finalize_render`` path.
        """
        if self._live is not None:
            try:
                # Blank the frame with the same visible height so the handoff
                # to the final static prose cannot expose stale lower rows.
                try:
                    self._live.update(self._blank_renderable(), refresh=True)
                except Exception:  # pragma: no cover
                    logger.debug("live blank-before-stop failed", exc_info=True)
                # Non-transient stop: Rich skips cursor cleanup, leaving
                # the blank frame on screen harmlessly while _print_static
                # renders the canonical prose below it.
                try:
                    self._live.transient = False
                except Exception:  # pragma: no cover
                    logger.debug("could not set transient=False on live", exc_info=True)
                self._live.stop()
            except Exception:  # pragma: no cover
                logger.debug("live stop failed", exc_info=True)
            finally:
                self._live = None
        if self._virtual_live:
            self._render_count = max(self._render_count, 1)
        self._active = False

    def _blank_renderable(self) -> Any:
        """Return a blank renderable that preserves the current frame height."""
        height = 1
        try:
            height = len(self._console.render_lines(self._renderable(), self._console.options, pad=False))
        except Exception:  # pragma: no cover
            logger.debug("could not measure live frame height", exc_info=True)
        # A Text renderable with N-1 newlines occupies N visible rows.
        return Padding(Text("\n" * max(0, height - 1)), (0, 2, 0, 2))

    def _print_static(self, text: str) -> None:
        """Emit ``text`` as a permanent static render through the console.

        Uses the injected ``finalize_render`` callback when provided (so
        tool/skill containers get the same treatment as normal
        end-of-turn prose via ``render_assistant_prose``); otherwise
        falls back to a padded ``Markdown`` print using our own console.
        """
        if self._finalize_render is not None:
            try:
                self._finalize_render(text)
                return
            except Exception:  # pragma: no cover — fall back below
                logger.debug("finalize_render failed; using fallback", exc_info=True)
        try:
            self._console.print(Padding(Markdown(text), (0, 2, 0, 2)))
        except Exception:  # pragma: no cover
            logger.debug("static markdown print failed", exc_info=True)
