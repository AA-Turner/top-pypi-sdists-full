# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Job driver heartbeats, so readers can tell a live driver from a dead one.

While a job's driver runs, a background thread overwrites one small JSON object
per job, ``_heartbeats/<job_id>.json``, inside the jobs table's directory.
Overwriting an object creates no Lance version, so heartbeats add no commits to
the jobs table however often they are written. Each heartbeat carries the lease
its driver promises to renew within; a reader that finds the lease expired knows
the driver died without recording a final job status.
"""

from __future__ import annotations

import enum
import json
import logging
import os
import socket
import tempfile
import threading
import time
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

import attrs

from geneva.utils import dt_now_utc

if TYPE_CHECKING:
    from collections.abc import Callable

    from lance.file import LanceFileSession

_LOG = logging.getLogger(__name__)

HEARTBEAT_DIR = "_heartbeats"
HEARTBEAT_SCHEMA_VERSION = 1

HEARTBEAT_INTERVAL_ENV = "GENEVA_DRIVER_HEARTBEAT_INTERVAL_S"
HEARTBEAT_LEASE_ENV = "GENEVA_DRIVER_HEARTBEAT_LEASE_S"
DEFAULT_HEARTBEAT_INTERVAL_S = 30.0
# A driver is presumed dead after this many intervals without a heartbeat, so a
# few slow or failed writes don't make a live driver look dead.
DEFAULT_LEASE_INTERVALS = 4
# Bound on stopping, so a hung object store never holds up the driver's exit.
HEARTBEAT_STOP_TIMEOUT_S = 30.0
# Each heartbeat request is abandoned after this fraction of the interval, so a
# hung write can't hold back the next beat.
_REQUEST_TIMEOUT_INTERVALS = 0.8
_MIN_REQUEST_TIMEOUT_S = 1.0

# Logs a failing writer's warning on the first failure and every Nth after it.
_FAILURE_LOG_EVERY = 10

DRIVER_RUNNING = "running"
DRIVER_EXITED = "exited"

_LOCAL_FILE = "heartbeat.json"


@enum.unique
class DriverLiveness(enum.Enum):
    """Whether an unfinished job still has a live driver."""

    # The driver renewed its heartbeat within its lease.
    ALIVE = "ALIVE"
    # No heartbeat landed within the lease: the driver died, or it cannot
    # reach storage. Returns to ALIVE if its writes recover.
    STALE = "STALE"
    # The driver exited without recording a final job status.
    EXITED = "EXITED"
    # No heartbeat: the driver has not started, or its geneva predates them.
    UNKNOWN = "UNKNOWN"


@attrs.define(kw_only=True, frozen=True)
class DriverHeartbeat:
    """The latest heartbeat of one job's driver."""

    job_id: str
    # DRIVER_RUNNING while the driver works, DRIVER_EXITED once it has stopped.
    state: str
    started_at: datetime
    written_at: datetime
    interval_s: float
    lease_s: float
    seq: int
    phase: str | None = None
    host: str | None = None
    pid: int | None = None
    ray_job_id: str | None = None
    ray_node_id: str | None = None
    geneva_version: str | None = None

    @property
    def lease_expires_at(self) -> datetime:
        """When readers stop trusting this heartbeat."""
        return self.written_at + timedelta(seconds=self.lease_s)

    def liveness(self, now: datetime | None = None) -> DriverLiveness:
        """Classify the driver as of ``now`` (default: the current time).

        ``written_at`` comes from the driver's clock, so clock skew between the
        driver and the reader shifts the result by the skew; the lease is
        minutes long so ordinary skew does not matter.
        """
        if self.state == DRIVER_EXITED:
            return DriverLiveness.EXITED
        if (now or dt_now_utc()) > self.lease_expires_at:
            return DriverLiveness.STALE
        return DriverLiveness.ALIVE

    def to_json(self) -> bytes:
        """Serialize for storage."""
        record: dict[str, Any] = attrs.asdict(self)
        record["started_at"] = self.started_at.isoformat()
        record["written_at"] = self.written_at.isoformat()
        record["schema_version"] = HEARTBEAT_SCHEMA_VERSION
        return json.dumps(record, sort_keys=True).encode()

    @classmethod
    def from_json(cls, data: bytes) -> DriverHeartbeat:
        """Parse a stored heartbeat, ignoring fields this version doesn't know."""
        record = json.loads(data)
        known = {f.name for f in attrs.fields(cls)}
        values = {k: v for k, v in record.items() if k in known}
        values["started_at"] = datetime.fromisoformat(values["started_at"])
        values["written_at"] = datetime.fromisoformat(values["written_at"])
        return cls(**values)


def heartbeat_path(job_id: str) -> str:
    """Object path of a job's heartbeat, relative to the jobs table root."""
    return f"{HEARTBEAT_DIR}/{quote(job_id, safe='')}.json"


class HeartbeatStore:
    """Driver heartbeat objects stored inside the jobs table's directory.

    Paths are relative to the table's dataset root, as with checkpoints, so the
    table's own (possibly vended) credentials cover them, and Lance cleanup
    leaves them alone because they are not Lance files.
    """

    def __init__(self, session_factory: Callable[[], LanceFileSession]) -> None:
        self._session_factory = session_factory
        self._session: LanceFileSession | None = None
        self._lock = threading.Lock()

    def _get_session(self) -> LanceFileSession:
        with self._lock:
            if self._session is None:
                self._session = self._session_factory()
            return self._session

    def _reset_session(self) -> None:
        """Drop the session so the next call reopens it, e.g. with fresh creds."""
        with self._lock:
            self._session = None

    def write(self, heartbeat: DriverHeartbeat) -> None:
        """Overwrite the job's heartbeat object."""
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                local = os.path.join(tmp_dir, _LOCAL_FILE)
                with open(local, "wb") as f:
                    f.write(heartbeat.to_json())
                self._get_session().upload_file(local, heartbeat_path(heartbeat.job_id))
        except Exception:
            self._reset_session()
            raise

    def delete(self, job_id: str) -> None:
        """Remove the job's heartbeat object, if it has one."""
        path = heartbeat_path(job_id)
        try:
            session = self._get_session()
            try:
                session.delete_file(path)
            except OSError:
                # Some stores fail to delete a missing object; that's not an error.
                if session.contains(path):
                    raise
        except Exception:
            self._reset_session()
            raise

    def read(self, job_id: str) -> DriverHeartbeat | None:
        """The job's latest heartbeat, or None if its driver never wrote one."""
        path = heartbeat_path(job_id)
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                local = os.path.join(tmp_dir, _LOCAL_FILE)
                session = self._get_session()
                try:
                    session.download_file(path, local)
                except OSError:
                    if not session.contains(path):
                        return None
                    raise
                with open(local, "rb") as f:
                    data = f.read()
        except Exception:
            self._reset_session()
            raise
        try:
            return DriverHeartbeat.from_json(data)
        except (ValueError, TypeError, KeyError):
            _LOG.warning("Ignoring malformed heartbeat for job %s", job_id)
            return None


_ACTIVE_WRITERS: dict[str, DriverHeartbeatWriter] = {}
_ACTIVE_WRITERS_LOCK = threading.Lock()


def set_driver_phase(job_id: str | None, phase: str) -> None:
    """Report ``phase`` on the next heartbeat of a driver in this process.

    A no-op when this process runs no driver for ``job_id``.
    """
    if not job_id:
        return
    with _ACTIVE_WRITERS_LOCK:
        writer = _ACTIVE_WRITERS.get(job_id)
    if writer is not None:
        writer.set_phase(phase)


def _ray_identity() -> tuple[str | None, str | None]:
    """The Ray job and node ids of this process, when it runs under Ray."""
    try:
        import ray

        if not ray.is_initialized():
            return None, None
        ctx = ray.get_runtime_context()
        return ctx.get_job_id(), ctx.get_node_id()
    except Exception:  # noqa: BLE001 - identity is informational only
        return None, None


class DriverHeartbeatWriter:
    """Background thread that keeps one job driver's heartbeat fresh.

    Writes a running heartbeat at once and then every ``interval_s`` seconds,
    and an exited heartbeat when stopped. A failed write is logged and retried
    on the next beat; heartbeats never fail the job.
    """

    def __init__(
        self,
        store: HeartbeatStore,
        job_id: str,
        *,
        interval_s: float,
        lease_s: float,
    ) -> None:
        from geneva import __version__

        self._store = store
        self._job_id = job_id
        self._interval_s = interval_s
        self._lease_s = lease_s
        self._phase: str | None = None
        self._seq = 0
        self._consecutive_failures = 0
        self._written = threading.Event()
        self._last_written: float | None = None
        self._listeners: list[Callable[[float], None]] = []
        self._started_at = dt_now_utc()
        self._host = os.environ.get("HOSTNAME") or socket.gethostname()
        self._pid = os.getpid()
        self._ray_job_id, self._ray_node_id = _ray_identity()
        self._geneva_version = __version__
        self._stop_evt = threading.Event()
        self._thread = threading.Thread(
            target=self._run, name=f"geneva-heartbeat-{job_id}", daemon=True
        )

    @property
    def interval_s(self) -> float:
        """Seconds between heartbeats."""
        return self._interval_s

    @property
    def lease_s(self) -> float:
        """Seconds each heartbeat promises the driver stays alive."""
        return self._lease_s

    def wait_written(self, timeout: float) -> bool:
        """Wait at most ``timeout`` for a heartbeat to land; True once one has."""
        return self._written.wait(timeout)

    def seconds_since_written(self) -> float | None:
        """Seconds since the heartbeat that last landed was written, or None if
        none has landed yet."""
        last = self._last_written
        return None if last is None else time.monotonic() - last

    def add_listener(self, listener: Callable[[float], None]) -> None:
        """Call ``listener`` each time a heartbeat lands, with the monotonic time
        it was written, which readers see as its ``written_at``. Runs on the
        heartbeat thread, so it must not block."""
        self._listeners.append(listener)

    def start(self) -> None:
        """Start heartbeating."""
        with _ACTIVE_WRITERS_LOCK:
            _ACTIVE_WRITERS[self._job_id] = self
        self._thread.start()

    def set_phase(self, phase: str) -> None:
        """Report ``phase`` on subsequent heartbeats."""
        self._phase = phase

    def stop(self, timeout: float = HEARTBEAT_STOP_TIMEOUT_S) -> None:
        """Write the exited heartbeat and stop, waiting at most ``timeout``."""
        with _ACTIVE_WRITERS_LOCK:
            if _ACTIVE_WRITERS.get(self._job_id) is self:
                del _ACTIVE_WRITERS[self._job_id]
        self._stop_evt.set()
        if self._thread.ident is None:
            return
        self._thread.join(timeout)
        if self._thread.is_alive():
            _LOG.warning(
                "Driver heartbeat for job %s did not stop within %.0fs",
                self._job_id,
                timeout,
            )

    def _run(self) -> None:
        while not self._stop_evt.is_set():
            self._beat(DRIVER_RUNNING)
            self._stop_evt.wait(self._interval_s)
        self._beat(DRIVER_EXITED)

    def _beat(self, state: str) -> None:
        self._seq += 1
        written = time.monotonic()
        heartbeat = DriverHeartbeat(
            job_id=self._job_id,
            state=state,
            started_at=self._started_at,
            written_at=dt_now_utc(),
            interval_s=self._interval_s,
            lease_s=self._lease_s,
            seq=self._seq,
            phase=self._phase,
            host=self._host,
            pid=self._pid,
            ray_job_id=self._ray_job_id,
            ray_node_id=self._ray_node_id,
            geneva_version=self._geneva_version,
        )
        try:
            self._store.write(heartbeat)
        except Exception:
            self._consecutive_failures += 1
            n = self._consecutive_failures
            if n == 1 or n % _FAILURE_LOG_EVERY == 0:
                _LOG.warning(
                    "Failed to write driver heartbeat for job %s "
                    "(%d consecutive failures)",
                    self._job_id,
                    n,
                    exc_info=n == 1,
                )
            return
        self._last_written = written
        self._written.set()
        for listener in list(self._listeners):
            try:
                listener(written)
            except Exception:  # noqa: BLE001, PERF203 - a listener never stops heartbeats
                _LOG.warning("Driver heartbeat listener failed", exc_info=True)
        if self._consecutive_failures:
            _LOG.info(
                "Driver heartbeat for job %s recovered after %d failed writes",
                self._job_id,
                self._consecutive_failures,
            )
            self._consecutive_failures = 0


def _env_seconds(name: str, default: float) -> float:
    """A non-negative seconds value from ``name``, or ``default`` if unusable."""
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        value = float(raw)
    except ValueError:
        value = -1.0
    if value < 0:
        _LOG.warning("Ignoring invalid %s=%r; using %ss", name, raw, default)
        return default
    return value


def heartbeat_interval_s() -> float:
    """Seconds between driver heartbeats; 0 disables them."""
    return _env_seconds(HEARTBEAT_INTERVAL_ENV, DEFAULT_HEARTBEAT_INTERVAL_S)


def heartbeat_lease_s(interval_s: float) -> float:
    """Seconds a heartbeat stays valid; must exceed ``interval_s``."""
    default = interval_s * DEFAULT_LEASE_INTERVALS
    lease_s = _env_seconds(HEARTBEAT_LEASE_ENV, default)
    if lease_s <= interval_s:
        _LOG.warning(
            "Ignoring %s=%s: it must exceed the %ss heartbeat interval; using %ss",
            HEARTBEAT_LEASE_ENV,
            lease_s,
            interval_s,
            default,
        )
        return default
    return lease_s


def heartbeat_storage_options(interval_s: float) -> dict[str, str]:
    """Object store options that bound every heartbeat request to under a beat.

    The object store client otherwise retries a hung request for minutes, and
    beats are written one at a time, so one stuck write would hold back every
    later beat. Each request times out a bit under ``interval_s`` and isn't
    retried: the writer's next beat is the retry.
    """
    if interval_s <= 0:
        interval_s = DEFAULT_HEARTBEAT_INTERVAL_S
    timeout_s = max(_MIN_REQUEST_TIMEOUT_S, interval_s * _REQUEST_TIMEOUT_INTERVALS)
    return {"timeout": f"{round(timeout_s * 1000)}ms", "client_max_retries": "0"}
