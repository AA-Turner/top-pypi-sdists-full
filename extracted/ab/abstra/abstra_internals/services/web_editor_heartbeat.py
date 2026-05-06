"""Web editor pod liveness heartbeat persisted on the shared EFS.

A web-editor pod periodically writes a small JSON file with the
current UTC timestamp. On boot, the next pod reads that timestamp
and decides whether the .abstra/ shared storage (executions, tasks,
logs) can be safely cleaned: if the last heartbeat is older than
`staleness_threshold`, no peer has been alive recently and the
cleanup is safe; otherwise, preserve the data.

Missing or corrupted heartbeat is treated as "fresh" (do not clean)
to protect projects that already have legacy data on the EFS the
first time this feature is deployed.
"""

import json
import os
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Optional

from abstra_internals.consts.filepaths import WEB_EDITOR_HEARTBEAT_FILE_PATH
from abstra_internals.environment import (
    WEB_EDITOR_HEARTBEAT_INTERVAL_SECONDS,
    WEB_EDITOR_HEARTBEAT_STALENESS_SECONDS,
)
from abstra_internals.logger import AbstraLogger
from abstra_internals.settings import Settings

Clock = Callable[[], datetime]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class WebEditorHeartbeat:
    def __init__(
        self,
        *,
        path: Optional[Path] = None,
        interval: Optional[timedelta] = None,
        staleness_threshold: Optional[timedelta] = None,
        clock: Clock = _utcnow,
    ):
        self._path = path or (Settings.root_path / WEB_EDITOR_HEARTBEAT_FILE_PATH)
        self._interval = interval or timedelta(
            seconds=WEB_EDITOR_HEARTBEAT_INTERVAL_SECONDS
        )
        self._staleness_threshold = staleness_threshold or timedelta(
            seconds=WEB_EDITOR_HEARTBEAT_STALENESS_SECONDS
        )
        self._clock = clock
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    @property
    def path(self) -> Path:
        return self._path

    def _read_updated_at(self) -> Optional[datetime]:
        try:
            if not self._path.exists():
                return None
            raw = self._path.read_text(encoding="utf-8")
            data = json.loads(raw)
            updated_at = data.get("updated_at")
            if not isinstance(updated_at, str):
                self._discard_unreadable("missing or non-string 'updated_at' field")
                return None
            parsed = datetime.fromisoformat(updated_at)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed
        except Exception as e:
            self._discard_unreadable(repr(e))
            return None

    def _discard_unreadable(self, reason: str) -> None:
        AbstraLogger.warning(
            f"[Heartbeat] Discarding unreadable {self._path} ({reason}) "
            "— treating as fresh to avoid wiping shared storage"
        )
        try:
            self._path.unlink(missing_ok=True)
        except Exception as unlink_err:
            AbstraLogger.warning(
                f"[Heartbeat] Failed to remove unreadable {self._path}: {unlink_err!r}"
            )

    def is_stale(self) -> bool:
        last = self._read_updated_at()
        if last is None:
            # Conservative default: missing or corrupted heartbeat is treated
            # as fresh so we never wipe pre-existing data on first deploy
            # of this feature or after a transient read failure.
            return False
        return self._clock() - last > self._staleness_threshold

    def update(self) -> None:
        now = self._clock()
        payload = json.dumps({"updated_at": now.isoformat()})
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self._path.with_suffix(self._path.suffix + ".tmp")
            tmp.write_text(payload, encoding="utf-8")
            os.replace(tmp, self._path)
        except Exception as e:
            AbstraLogger.warning(f"[Heartbeat] Failed to write {self._path}: {e!r}")
            try:
                self._path.with_suffix(self._path.suffix + ".tmp").unlink(
                    missing_ok=True
                )
            except Exception:
                pass

    def _run(self) -> None:
        while not self._stop_event.is_set():
            self.update()
            # Event.wait returns True as soon as stop() is called,
            # so shutdown is near-instant even with long intervals.
            if self._stop_event.wait(self._interval.total_seconds()):
                return

    def start(self) -> None:
        if self._thread is not None:
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run,
            name="WebEditorHeartbeat",
            daemon=True,
        )
        self._thread.start()

    def stop(self, timeout: float = 5.0) -> None:
        self._stop_event.set()
        thread = self._thread
        if thread is not None:
            thread.join(timeout=timeout)
            self._thread = None
