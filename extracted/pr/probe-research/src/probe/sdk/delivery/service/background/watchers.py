"""WatcherThreads: the service's run watchers, one thread per box registry (X9), so a run's watcher
costs no process while a service runs; at the service's stop, a detached watcher takes over."""

from __future__ import annotations

import os
import sys
import threading
import time
from collections.abc import Callable, Mapping
from typing import TYPE_CHECKING

from probe.foundation.service_api.vocabularies import BackgroundRefusal, BackgroundState

if TYPE_CHECKING:  # the watcher loads on the first `box.watch`: the start path stays stdlib-only
    from probe.sdk.run.watcher.thread import WatcherThread

#: The caller's variables that decide where a watcher's reports go: its login (the CLI config) and
#: its network. A caller whose values differ from the service's gets a child on its own environment
#: instead (`BackgroundHost.watch_box`): a thread here would report through the service's.
REPORT_ENV = (
    # Never a caller's key: one watcher serves every run in its registry, so one job's PROBE_TOKEN
    # would report another job's runs to that job's server (#4287 review). A job with only an
    # environment key gets no crash report from the watcher (a follow-up: per-entry credentials).
    "PROBE_CONFIG_PATH", "XDG_CONFIG_HOME",
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "all_proxy", "no_proxy",
    "SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE",
)
#: A watcher thread asked to stop waits this long for a sweep in flight.
STOP_WAIT_S = 1.0


def is_same_report_env(env: Mapping[str, str]) -> bool:
    """Whether a thread of this service reports as a watcher started on `env` would (unset == empty)."""
    return all((env.get(name) or None) == (os.environ.get(name) or None) for name in REPORT_ENV)


class WatcherThreads:
    """The service's watcher threads by key (`box:<registry>`); each holds its registry's lease."""

    def __init__(self, *, log: Callable[[str], None], spawn: Callable[..., object], cwd: Callable[[], str]) -> None:
        self.log = log
        #: Starts the hand-off watcher (`BackgroundHost._spawn`: a session of its own, a clean env).
        self._spawn = spawn
        self._cwd = cwd
        self._lock = threading.Lock()
        self._threads: dict[str, WatcherThread] = {}
        self._is_closed = False
        self.started = 0

    def count(self) -> int:
        with self._lock:
            return sum(1 for t in self._threads.values() if t.is_alive())

    def start(self, key: str, directory: str, env: Mapping[str, str], *, room: int) -> dict:
        """STARTED (a new thread), RUNNING (ours runs, or a watcher holds the lease), else refused:
        STOPPING, or BUSY when `room` (watchers this service may still add besides these threads,
        counted here under the lock so two starts cannot both take the last place) is spent."""
        with self._lock:
            if self._is_closed:
                return {"accepted": False, "reason": BackgroundRefusal.STOPPING}
            mine = self._threads.get(key)
            if mine is not None and mine.is_alive():
                return {"accepted": True, "state": BackgroundState.RUNNING}
            if room - sum(1 for t in self._threads.values() if t.is_alive()) <= 0:
                return {"accepted": False, "reason": BackgroundRefusal.BUSY}
            try:
                from probe.sdk.run.watcher.thread import WatcherThread

                made = WatcherThread.start(directory, env=_get_watcher_settings(env), on_exit=self._forget)
            except Exception as exc:  # noqa: BLE001 -- no thread: the caller spawns its own
                self.log(f"background: could not start the watcher thread for {key}: {exc!r}")
                return {"accepted": False, "reason": BackgroundRefusal.UNUSABLE}
            if made is None:
                return {"accepted": True, "state": BackgroundState.RUNNING}
            self._threads[key] = made
            self.started += 1
        self.log(f"background: watcher thread started for {key}")
        return {"accepted": True, "state": BackgroundState.STARTED}

    def list_rows(self) -> list[dict]:
        """`service.status`'s `box_watchers` rows for the threads (the pid is the service's)."""
        now = time.monotonic()
        with self._lock:
            return [{"pid": os.getpid(), "running_s": round(now - t.started, 1)}
                    for t in self._threads.values() if t.is_alive()]

    def close(self) -> None:
        """Take nothing more; stop every thread, and hand each registry that still lists a run to a
        detached watcher (`python -m probe.sdk.run.watcher`), so its runs stay watched after this
        service is gone. Blocks up to STOP_WAIT_S per thread: the server calls it on a thread."""
        with self._lock:
            self._is_closed = True
            threads = list(self._threads.items())
        for key, made in threads:
            made.stop(STOP_WAIT_S)
            if made.has_entries():
                self._hand_off(key, made)

    def _hand_off(self, key: str, made: WatcherThread) -> None:
        env = {**made.env, "PROBE_WATCHER_DIR": str(made.directory)}
        try:
            from probe.foundation.service_api.start import build_module_argv, get_package_dir
            from probe.sdk.run.watcher import lease

            # This service's interpreter, `-I`, its own `probe` folder first (H1, H4a).
            argv = build_module_argv(sys.executable, lease.WATCHER_MODULE, [], get_package_dir())
            self._spawn(argv, env, cwd=self._cwd(), log_path=None)
        except Exception as exc:  # noqa: BLE001 -- the next run to start spawns one
            self.log(f"background: could not hand {key} to a detached watcher: {exc!r}")
            return
        self.log(f"background: {key} handed to a detached watcher")

    def _forget(self, made: WatcherThread) -> None:
        """A thread ended (its box went quiet, or it was stopped): it leaves the books."""
        with self._lock:
            for key, known in list(self._threads.items()):
                if known is made:
                    del self._threads[key]
                    if not self._is_closed:
                        self.log(f"background: watcher thread for {key} ended")


def _get_watcher_settings(env: Mapping[str, str]) -> dict[str, str]:
    """The caller's watcher settings (`PROBE_WATCHER_*`, the old `PROBE_BOX_*`), which a thread
    reads in place of the service's own environment."""
    return {name: value for name, value in env.items() if name.startswith(("PROBE_WATCHER_", "PROBE_BOX_"))}
