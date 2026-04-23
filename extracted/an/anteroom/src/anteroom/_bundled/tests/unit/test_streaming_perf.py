"""Performance guard for live markdown streaming (#1365).

This benchmark fails the PR if per-tick Markdown re-parsing proves too
expensive on a realistic 10k-chunk feed. Failing here is the signal
(from Phase A plan) that Phase B (custom streaming parser) is required.

We use wall-clock time with a generous threshold because the test runs
on every CI matrix runner (including slow ones). The throttle
(``refresh_hz=20``) limits actual repaints to ~N*0.05s where N is the
number of seconds the feed loop takes — so the Rich re-parse cost is
strictly bounded, not linear in the 10k feed count.
"""

from __future__ import annotations

import io
import time

from rich.console import Console

from anteroom.cli.streaming import StreamingMarkdownRenderer


def _make_capture() -> Console:
    buf = io.StringIO()
    return Console(
        file=buf,
        force_terminal=True,
        color_system="truecolor",
        width=80,
        highlight=False,
    )


def test_10k_chunk_feed_completes_under_threshold() -> None:
    """A 10k-chunk feed (each chunk ~20 chars) must complete well under
    2 seconds wall clock.

    Measured headroom on the reference Mac is ~30x; we set a generous
    threshold so slow CI runners don't flake, while still catching a
    regression that would render Phase A unusable.
    """
    console = _make_capture()
    r = StreamingMarkdownRenderer(console=console, enabled=True, refresh_hz=20.0)

    # Deterministic 10k chunks: representative mix of plain text, markdown
    # formatting, and fenced code.
    chunks: list[str] = []
    for i in range(10_000):
        if i % 500 == 0 and i > 0:
            chunks.append("\n```python\nprint('hi')\n```\n")
        elif i % 31 == 0:
            chunks.append(" **bold** ")
        elif i % 17 == 0:
            chunks.append(" `code` ")
        else:
            chunks.append(" token ")

    start = time.monotonic()
    for chunk in chunks:
        r.feed(chunk)
    r.stop()
    elapsed = time.monotonic() - start

    # 2 seconds is a very loose ceiling — the throttle keeps the actual
    # repaint count bounded regardless of feed count, so even Rich's
    # full-string re-parse runs only a handful of times during this feed.
    assert elapsed < 2.0, f"streaming feed of 10k chunks took {elapsed:.3f}s (threshold 2.0s)"
    # Sanity: the throttle must have kept render count well below the
    # chunk count. If this assertion fails, the throttle regressed.
    assert r.render_count() < 200
