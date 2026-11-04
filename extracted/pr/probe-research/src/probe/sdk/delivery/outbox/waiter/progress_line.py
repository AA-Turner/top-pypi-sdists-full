"""The line a waiting `finish()` prints every ~5 s: writes and bytes left, rate, time left, what is
ahead, and how to stop waiting."""

from __future__ import annotations

import time
from collections import deque

#: The window the rate is measured over, seconds.
_RATE_WINDOW_SECONDS = 30.0


class ProgressLine:
    """Turns successive views of one run into a progress line."""

    def __init__(self, run_ref: str, *, clock=time.monotonic) -> None:
        self.run_ref = run_ref
        self.clock = clock
        self._samples: deque = deque()

    def render(self, view, *, is_server_storing: bool = False) -> str:
        """``view``: a `RunView` from the progress records. ``is_server_storing``: the server holds
        the run's close until its queued data is stored (I15d), which is what the line says then."""
        if is_server_storing:
            points = view.server_pending_points
            amount = f"{points:,} point(s) of it" if points else "its last data"
            return (
                f"probe: run {self.run_ref}: everything was sent; the server is still storing {amount}, "
                "and closes the run once they are stored; Ctrl-C to stop waiting (the close stays queued)"
            )
        now = self.clock()
        self._samples.append((now, view.delivered_total))
        while len(self._samples) > 2 and now - self._samples[0][0] > _RATE_WINDOW_SECONDS:
            self._samples.popleft()
        first_at, first_count = self._samples[0]
        rate = (view.delivered_total - first_count) / (now - first_at) if now > first_at else 0.0
        parts = [f"probe: run {self.run_ref}: {view.pending:,} write(s)"]
        if view.pending_bytes:
            parts[0] += f" ({_size(view.pending_bytes)})"
        parts[0] += " left"
        if rate > 0:
            parts.append(f"{rate:,.1f}/s, about {_duration(view.pending / rate)} to go")
        if view.ahead:
            parts.append(f"{view.ahead:,} write(s) of other runs ahead of yours")
        parts.append("Ctrl-C to stop waiting (the worker keeps sending)")
        return "; ".join(parts)


def _size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:,.0f} {unit}" if unit == "B" else f"{n:,.1f} {unit}"
        n /= 1024
    return f"{n:,.1f} GB"


def _duration(seconds: float) -> str:
    if seconds < 90:
        return f"{max(1, round(seconds))} s"
    if seconds < 5400:
        return f"{round(seconds / 60)} min"
    return f"{seconds / 3600:.1f} h"
