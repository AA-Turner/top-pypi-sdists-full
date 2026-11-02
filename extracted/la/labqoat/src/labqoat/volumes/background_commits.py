"""Commit a worker's writable mounts every so often, so work done between explicit commits is not lost."""

from __future__ import annotations

import sys
import threading
from collections.abc import Callable


class BackgroundCommits:
    """A daemon thread committing every ``interval`` seconds; a failed commit is reported and tried again later."""

    def __init__(self, commit: Callable[[], None], interval: float) -> None:
        """Run ``commit`` periodically once started."""
        self._commit = commit
        self._interval = interval
        self._stopped = threading.Event()
        self._thread = threading.Thread(target=self._run, name="labqoat-volume-commits", daemon=True)

    def start(self) -> None:
        """Begin committing in the background."""
        self._thread.start()

    def stop(self) -> None:
        """Stop after any commit in progress."""
        self._stopped.set()
        self._thread.join()

    def _run(self) -> None:
        """Commit until stopped."""
        while not self._stopped.wait(self._interval):
            try:
                self._commit()
            except Exception as error:
                print(f"Volume background commit failed and will be retried: {error}", file=sys.stderr, flush=True)
