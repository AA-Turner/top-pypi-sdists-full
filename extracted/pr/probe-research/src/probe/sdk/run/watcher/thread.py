"""WatcherThread: the watcher as a thread of the process that starts it (the Probe service, X9).

No process of its own, and the same lease a detached watcher takes (`lease.hold_lease`), so the
service's thread and a `python -m probe.sdk.run.watcher` never both watch one registry.
"""

from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable, Mapping
from pathlib import Path

from probe.sdk.run.watcher import lease, registry, watcher

logger = logging.getLogger(__name__)


class WatcherThread:
    """One registry's watcher, sweeping on a daemon thread while it holds that registry's lease."""

    def __init__(
        self, directory: Path | str, handle, *, env: Mapping[str, str] | None = None,
        on_exit: Callable[[WatcherThread], None] | None = None,
    ) -> None:
        self.directory = Path(directory)
        #: The caller's watcher settings it runs with (`PROBE_WATCHER_*`), for a successor.
        self.env = dict(env or {})
        self.started = time.monotonic()
        self._lease = handle
        self._on_exit = on_exit
        self._stop = threading.Event()
        # The caller's cadence (`PROBE_WATCHER_INTERVAL` / `_IDLE_EXIT`), as a detached watcher
        # started with its environment would read it.
        self._interval = watcher._tunable("INTERVAL", watcher.DEFAULT_INTERVAL_SECONDS, self.env)
        self._idle_exit = watcher._tunable("IDLE_EXIT", watcher.IDLE_EXIT_SECONDS, self.env)
        self._thread = threading.Thread(target=self._run, name=f"probe-watcher-{self.directory}", daemon=True)

    @classmethod
    def start(
        cls, directory: Path | str, *, env: Mapping[str, str] | None = None,
        on_exit: Callable[[WatcherThread], None] | None = None,
    ) -> WatcherThread | None:
        """Take `directory`'s lease and start sweeping; None when a watcher already holds it."""
        handle = lease.hold_lease(directory)
        if handle is None:
            return None
        made = cls(directory, handle, env=env, on_exit=on_exit)
        try:
            made._thread.start()
        except Exception:
            made._release()
            raise
        return made

    def is_alive(self) -> bool:
        return self._thread.is_alive()

    def has_entries(self) -> bool:
        """Whether this registry still lists a run of this machine (one a successor must watch)."""
        return any(registry.is_local(entry) for entry in registry.entries(self.directory))

    def stop(self, wait_s: float = 1.0) -> None:
        """Stop sweeping and let the lease go, waiting up to `wait_s` for a sweep in flight.

        The lease goes even if that sweep is still reporting: a successor may then sweep once
        beside it, and a report is idempotent (`watcher._span_id`)."""
        self._stop.set()
        if self._thread.is_alive() and self._thread is not threading.current_thread():
            self._thread.join(wait_s)
        self._release()

    def _run(self) -> None:
        try:
            watcher.watch_forever(
                interval=self._interval, idle_exit_seconds=self._idle_exit, directory=self.directory,
                sleep=self._stop.wait, should_stop=self._stop.is_set,
            )
        except Exception as exc:  # noqa: BLE001 -- the watcher never breaks its host
            logger.debug("box: watcher thread for %s ended: %s", self.directory, exc)
        finally:
            self._release()
            if self._on_exit is not None:
                try:
                    self._on_exit(self)
                except Exception:  # noqa: BLE001
                    pass

    def _release(self) -> None:
        try:
            self._lease.close()
        except Exception:  # noqa: BLE001 -- closing twice, or a gone fd: the lock is released either way
            pass
