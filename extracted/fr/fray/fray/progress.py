"""
Fray Progress — shared progress bar for all fray commands.

Provides a consistent animated progress bar with:
  - Percentage and count
  - Elapsed time
  - Currently running task labels
  - Last completed task indicator

Thread-safe for concurrent task execution.
"""

import sys
import time
import threading
from typing import Optional


class FrayProgress:
    """Real-time progress output for fray commands."""

    def __init__(self, total: int, title: str = "", quiet: bool = False):
        self._total = max(total, 1)
        self._done = 0
        self._start = time.time()
        self._quiet = quiet
        self._title = title
        self._active: set = set()
        self._lock = threading.Lock()
        if not quiet and title:
            sys.stderr.write(f"\n  {title}\n\n")
            sys.stderr.flush()

    def _bar(self) -> str:
        bar_len = 20
        filled = int(bar_len * self._done / self._total) if self._total else 0
        return "\u2588" * filled + "\u2591" * (bar_len - filled)

    def _render(self, last_done: str = "") -> None:
        if self._quiet:
            return
        elapsed = time.time() - self._start
        pct = int(self._done / self._total * 100) if self._total else 0
        with self._lock:
            running = sorted(self._active)
        run_str = ", ".join(running[:3])
        if len(running) > 3:
            run_str += f" +{len(running) - 3}"
        done_mark = f"\u2713 {last_done}" if last_done else ""
        line = (f"\r  [{self._bar()}] {pct:3d}% ({self._done}/{self._total}) "
                f"{elapsed:5.1f}s  {done_mark:<30}")
        if run_str and self._done < self._total:
            line += f"\n  \u2192 {run_str:<60}"
        sys.stderr.write(f"\033[2K\033[A\033[2K{line}")
        sys.stderr.flush()

    def start(self, label: str) -> None:
        if self._quiet:
            return
        with self._lock:
            self._active.add(label)
        self._render()

    def done(self, label: str) -> None:
        if self._quiet:
            return
        with self._lock:
            self._active.discard(label)
        self._done += 1
        self._render(last_done=label)
        if self._done >= self._total:
            sys.stderr.write("\n")
            sys.stderr.flush()

    def status(self, msg: str) -> None:
        if self._quiet:
            return
        elapsed = time.time() - self._start
        sys.stderr.write(f"\033[2K\r  \u23f3 {elapsed:5.1f}s  {msg}")
        sys.stderr.flush()

    def finish(self) -> None:
        """Force-finish the progress bar."""
        if self._quiet:
            return
        if self._done < self._total:
            self._done = self._total
            elapsed = time.time() - self._start
            sys.stderr.write(
                f"\033[2K\r  [{self._bar()}] 100% ({self._total}/{self._total}) "
                f"{elapsed:5.1f}s  \u2713 Done\n"
            )
            sys.stderr.flush()
