"""Scalar metrics for a model's training run, behind ``Model.log()``.

::

    model.define_metric("optimizer_step", hidden=True)
    model.define_metric("train/*", step_metric="optimizer_step")
    model.log({"optimizer_step": 96, "train/loss": 0.42})

``Model`` forwards both calls to one lazily created :class:`_RunMetrics`,
bound to the model's existing training run and the client's credentials;
there is nothing to initialize or finish. Each ``log()`` call records one
complete observation. Coordinates come from the same call: River never
carries a value from one call to another and never reads ``Model.step``.
Every observation also records ``_river/timestamp`` (Unix seconds at the
call) and ``_river/runtime`` (seconds since the model was created), which
definitions may use as step metrics.

Delivery is memory-only and best effort. Invalid usage raises immediately,
but delivery problems never raise into training: a background thread
batches and retries uploads, a bounded buffer discards its oldest
observations when full, and losses are reported as rate-limited warnings.
Session exit and ``Client.close()`` wait up to 30 seconds for buffered
observations, after model cleanup. Abrupt termination loses the buffer.

A writer belongs to the process that created the model. In a forked child,
calls on an inherited writer are skipped with a warning.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
import logging
import math
import os
import random
import threading
import time
import uuid

import numpy as np

from river_client.metric_events import console_url, encode, format_timestamp, post_batch

_logger = logging.getLogger(__name__)

TIMESTAMP_AXIS = "_river/timestamp"
RUNTIME_AXIS = "_river/runtime"
RESERVED_PREFIX = "_river/"
BUILT_IN_AXES = frozenset({TIMESTAMP_AXIS, RUNTIME_AXIS})

# River Console's ingestion limits.
MAX_NAME_BYTES = 512
MAX_BATCH_VALUES = 1_000
MAX_BATCH_BYTES = 1 << 20
MAX_DEFINITIONS = 1_000

MAX_BUFFER_VALUES = 10_000
MAX_BUFFER_BYTES = 8 << 20
FLUSH_INTERVAL_S = 2.0
RETRY_INITIAL_S = 0.5
RETRY_MAX_S = 30.0
DRAIN_TIMEOUT_S = 30.0
WARNING_INTERVAL_S = 60.0
# Metric names whose definition lookup is remembered, so a run logging
# ever-new names keeps bounded memory.
MAX_RESOLVED_NAMES = 10_000
# A run is visible to River Console shortly after the model exists; until
# then a 404 is retried rather than treated as permanent.
NOT_FOUND_GRACE_S = 120.0

# Bytes of the batch envelope around the producer, definitions and
# observations, plus a separator per element.
_ENVELOPE_BYTES = 64
_RETRYABLE_STATUSES = frozenset({408, 429})
_DISABLING_STATUSES = frozenset({401, 403, 404})


class _RunMetrics:
    """Validates, buffers and delivers one model's metrics."""

    def __init__(
        self,
        *,
        training_run_id: str,
        api_key: str,
        user_agent: str,
        owner_pid: int,
        started_at: float,
        started_monotonic: float,
        send=post_batch,
        flush_interval_s: float = FLUSH_INTERVAL_S,
    ) -> None:
        self._pid = owner_pid
        self._started_monotonic = started_monotonic
        self._training_run_id = training_run_id
        self._api_key = api_key
        self._user_agent = user_agent
        url = console_url(training_run_id, "observations")
        self._url = url or ""
        self._send = send
        self._flush_interval_s = flush_interval_s
        self._producer = encode(
            {
                "producer_id": str(uuid.uuid4()),
                "started_at": format_timestamp(started_at),
            }
        )
        self._lock = threading.Condition()
        self._thread: threading.Thread | None = None

        # Definitions: pattern -> (step_metric, hidden), and their revision.
        self._definitions: dict[str, tuple[str | None, bool]] = {}
        self._version = 0
        self._defined_at = 0.0
        self._resolved: dict[str, str | None] = {}

        # Delivery. Queued and in-flight observations and undelivered
        # revisions count toward the buffer.
        self._seq = 0
        self._queue: deque[_Observation] = deque()
        self._queued_values = 0
        self._queued_bytes = 0
        self._inflight: _Batch | None = None
        # Undelivered revisions still needed: the latest, and any that a
        # queued observation references.
        self._revisions: dict[int, bytes] = {}
        self._revision_bytes = 0
        self._references: dict[int, int] = {}
        self._acknowledged: set[int] = set()
        self._closing = False
        self._stopped = False
        self._disabled: str | None = None
        if not self._api_key:
            self._disabled = "the client has no River API key"
        elif url is None:
            self._disabled = "RIVER_CONSOLE_URL must use HTTPS"

        # Loss accounting, reported in warnings.
        self._dropped = 0
        self._rejected = 0
        self._unconfirmed = 0
        self._warned_at: dict[str, float] = {}
        self._inherited_skipped = 0
        self._inherited_warned_at: float | None = None

    def define_metric(
        self,
        name: str,
        *,
        step_metric: str | None = None,
        hidden: bool | None = None,
    ) -> None:
        """Implements ``Model.define_metric()``."""
        _check_pattern(name)
        if step_metric is not None:
            _check_step_metric(step_metric)
        if hidden is not None and not isinstance(hidden, bool):
            raise TypeError(f"hidden must be a bool, got {type(hidden).__name__}")
        if self._pid != os.getpid():
            self._skip_inherited()
            return
        with self._lock:
            current = self._definitions.get(name)
            current_step, current_hidden = current or (None, False)
            updated = (
                current_step if step_metric is None else step_metric,
                current_hidden if hidden is None else hidden,
            )
            if updated == current:
                return
            definitions = {**self._definitions, name: updated}
            if len(definitions) > MAX_DEFINITIONS:
                raise ValueError(
                    f"a run may define at most {MAX_DEFINITIONS} metric patterns"
                )
            version = self._version + 1
            body = encode(
                {
                    "version": version,
                    "metrics": [
                        {"name": pattern, "step_metric": step, "hidden": hide}
                        for pattern, (step, hide) in sorted(definitions.items())
                    ],
                }
            )
            if len(body) + len(self._producer) + _ENVELOPE_BYTES > MAX_BATCH_BYTES:
                raise ValueError(
                    f"metric definitions exceed {MAX_BATCH_BYTES} bytes; "
                    "use fewer or shorter patterns"
                )
            previous = self._version
            self._definitions = definitions
            self._version = version
            self._defined_at = time.monotonic()
            self._resolved.clear()
            if not self._accepting():
                return
            self._revisions[version] = body
            self._revision_bytes += len(body)
            self._release_revision(previous)
            warnings = [self._overflow_warning(self._enforce_budget()), self._start()]
            self._lock.notify_all()
        for warning in warnings:
            _warn(warning)

    def log(self, data: Mapping[str, float]) -> None:
        """Implements ``Model.log()``."""
        logged_at = time.time()
        elapsed_s = max(time.monotonic() - self._started_monotonic, 0.0)
        values = _check_values(data)
        if self._pid != os.getpid():
            self._skip_inherited()
            return
        warnings = []
        with self._lock:
            if not self._accepting():
                self._dropped += 1
                warnings.append(self._not_accepting_warning())
            else:
                body = encode(
                    {
                        "seq": self._seq,
                        "logged_at": format_timestamp(logged_at),
                        "elapsed_s": elapsed_s,
                        "definition_version": self._version or None,
                        "values": values,
                    }
                )
                if len(body) + len(self._producer) + _ENVELOPE_BYTES > MAX_BATCH_BYTES:
                    raise ValueError(
                        f"model.log() data exceeds {MAX_BATCH_BYTES} bytes once encoded; "
                        "log fewer values per call or shorten metric names"
                    )
                self._seq += 1
                observation = _Observation(
                    body, len(values), self._version, time.monotonic()
                )
                self._queue.append(observation)
                self._queued_values += observation.values
                self._queued_bytes += len(body)
                if observation.version:
                    self._references[observation.version] = (
                        self._references.get(observation.version, 0) + 1
                    )
                warnings.append(self._overflow_warning(self._enforce_budget()))
                warnings.append(self._start())
                self._lock.notify_all()
            warnings.append(self._missing_coordinate_warning(values))
        for warning in warnings:
            _warn(warning)

    # ── Definitions ─────────────────────────────────────────────────────

    def _step_metric(self, name: str) -> str | None:
        """The step metric of ``name``'s definition: exact, else longest prefix."""
        if name in self._resolved:
            return self._resolved[name]
        if len(self._resolved) >= MAX_RESOLVED_NAMES:
            self._resolved.clear()
        definition = self._definitions.get(name)
        if definition is None:
            # Equal-length matching prefixes are the same pattern.
            prefixes = [
                (len(pattern), pattern)
                for pattern in self._definitions
                if pattern.endswith("*") and name.startswith(pattern[:-1])
            ]
            if prefixes:
                definition = self._definitions[max(prefixes)[1]]
        step_metric = definition[0] if definition else None
        self._resolved[name] = step_metric
        return step_metric

    def _missing_coordinate_warning(self, values: dict[str, float]) -> str | None:
        if not self._definitions:
            return None
        for name in values:
            step_metric = self._step_metric(name)
            if (
                step_metric is not None
                and step_metric not in BUILT_IN_AXES
                and step_metric not in values
            ):
                if not self._should_warn("missing coordinate"):
                    return None
                return (
                    f"model.log() recorded {name!r} without its step metric "
                    f"{step_metric!r} in the same call; the value is kept but "
                    "has no coordinate on that axis"
                )
        return None

    # ── Buffer ──────────────────────────────────────────────────────────

    def _accepting(self) -> bool:
        return not (self._closing or self._stopped or self._disabled)

    def _start(self) -> str | None:
        """Start delivery once; if it cannot start, disable it and say so."""
        if self._thread is not None:
            return None
        thread = threading.Thread(
            target=self._run, name="river-run-metrics", daemon=True
        )
        try:
            thread.start()
        except Exception as error:
            self._disabled = f"its delivery thread did not start ({error})"
            self._discard_queue()
            return self._not_accepting_warning()
        self._thread = thread
        return None

    def _over_budget(self) -> bool:
        inflight_values = 0
        inflight_bytes = 0
        if self._inflight is not None:
            inflight_values = self._inflight.values
            # Revisions the batch carries that the buffer no longer holds.
            inflight_bytes = self._inflight.observation_bytes + sum(
                size
                for version, size in self._inflight.revisions.items()
                if version not in self._revisions
            )
        return (
            self._queued_values + inflight_values > MAX_BUFFER_VALUES
            or self._queued_bytes + inflight_bytes + self._revision_bytes
            > MAX_BUFFER_BYTES
        )

    def _enforce_budget(self) -> int:
        """Discard the oldest queued observations while over budget."""
        dropped = 0
        while self._queue and self._over_budget():
            self._pop_oldest()
            dropped += 1
        self._dropped += dropped
        return dropped

    def _pop_oldest(self) -> _Observation:
        observation = self._queue.popleft()
        self._queued_values -= observation.values
        self._queued_bytes -= len(observation.body)
        version = observation.version
        if version:
            remaining = self._references.get(version, 0) - 1
            if remaining > 0:
                self._references[version] = remaining
            else:
                self._references.pop(version, None)
                self._release_revision(version)
        return observation

    def _release_revision(self, version: int) -> None:
        """Forget a revision that is neither the latest nor still referenced."""
        if version == self._version or self._references.get(version):
            return
        self._forget_revision(version)

    def _forget_revision(self, version: int) -> None:
        self._revision_bytes -= len(self._revisions.pop(version, b""))

    def _latest_undelivered(self) -> bool:
        return self._version in self._revisions

    # ── Delivery ────────────────────────────────────────────────────────

    def _run(self) -> None:
        try:
            while True:
                with self._lock:
                    batch = self._next_batch()
                if batch is None:
                    return
                self._deliver(batch)
        except Exception:
            _warn("River run metrics delivery stopped", exc_info=True)
            with self._lock:
                self._disabled = "delivery stopped unexpectedly"
                self._discard_queue()
                self._inflight = None
                self._lock.notify_all()

    def _next_batch(self) -> _Batch | None:
        while True:
            if self._stopped:
                return None
            if not self._queue and not self._latest_undelivered():
                if self._closing or self._disabled:
                    self._lock.notify_all()
                    return None
                self._lock.wait()
                continue
            oldest = self._queue[0].enqueued_at if self._queue else self._defined_at
            waited = time.monotonic() - oldest
            if (
                self._closing
                or waited >= self._flush_interval_s
                or self._queued_values >= MAX_BATCH_VALUES
                or self._queued_bytes >= MAX_BATCH_BYTES
            ):
                self._inflight = self._take_batch()
                return self._inflight
            self._lock.wait(self._flush_interval_s - waited)

    def _take_batch(self) -> _Batch:
        revisions: dict[int, bytes] = {}
        size = _ENVELOPE_BYTES + len(self._producer)
        if self._latest_undelivered():
            revisions[self._version] = self._revisions[self._version]
            size += len(revisions[self._version]) + 1
        observations: list[bytes] = []
        values = 0
        while self._queue:
            observation = self._queue[0]
            version = observation.version
            revision = (
                self._revisions.get(version)
                if version
                and version not in self._acknowledged
                and version not in revisions
                else None
            )
            needed = len(observation.body) + 1 + (len(revision) + 1 if revision else 0)
            if size + needed > MAX_BATCH_BYTES or (
                values + observation.values > MAX_BATCH_VALUES
            ):
                if revision is not None and not observations and not revisions:
                    # Deliver the revision on its own first.
                    revisions[version] = revision
                if observations or revisions:
                    break
            if revision is not None:
                revisions[version] = revision
            self._pop_oldest()
            observations.append(observation.body)
            values += observation.values
            size += needed
        body = b"".join(
            [
                b'{"version":1,"producer":',
                self._producer,
                b',"definitions":[',
                b",".join(revisions.values()),
                b'],"observations":[',
                b",".join(observations),
                b"]}",
            ]
        )
        return _Batch(
            body=body,
            revisions={version: len(body) for version, body in revisions.items()},
            observations=len(observations),
            values=values,
            observation_bytes=sum(len(observation) for observation in observations),
        )

    def _deliver(self, batch: _Batch) -> None:
        delay = RETRY_INITIAL_S
        while True:
            status = self._send(self._url, self._api_key, self._user_agent, batch.body)
            with self._lock:
                # Past the shutdown deadline, the batch was already reported.
                if self._stopped:
                    return
                if status is not None and 200 <= status < 300:
                    self._acknowledged.update(batch.revisions)
                    for version in batch.revisions:
                        self._forget_revision(version)
                    self._inflight = None
                    self._lock.notify_all()
                    return
                if status is not None and not self._retryable(status):
                    warning = self._reject(batch, status)
                    break
                # New observations notify the lock; keep the backoff anyway so
                # an outage never becomes a request storm.
                deadline = time.monotonic() + delay * random.uniform(0.5, 1.5)
                while (
                    not self._stopped and (remaining := deadline - time.monotonic()) > 0
                ):
                    self._lock.wait(remaining)
                if self._stopped:
                    return
            delay = min(delay * 2, RETRY_MAX_S)
        _warn(warning)

    def _retryable(self, status: int) -> bool:
        if status in _RETRYABLE_STATUSES or status >= 500:
            return True
        return (
            status == 404
            and time.monotonic() - self._started_monotonic < NOT_FOUND_GRACE_S
        )

    def _reject(self, batch: _Batch, status: int) -> str | None:
        """Give up on ``batch`` after a permanent HTTP failure."""
        self._inflight = None
        self._rejected += batch.observations
        # A rejected revision would be rejected again; observations that
        # reference it will be too.
        for version in batch.revisions:
            self._forget_revision(version)
        if status in _DISABLING_STATUSES:
            self._disabled = f"River Console answered HTTP {status}"
            self._discard_queue()
        self._lock.notify_all()
        if not self._should_warn(f"rejected {status}"):
            return None
        return (
            f"River Console rejected metrics for training run "
            f"{self._training_run_id} with HTTP {status}"
            + ("; metrics for this run are disabled" if self._disabled else "")
            + f" ({self._rejected} observations rejected so far)"
        )

    def _discard_queue(self) -> None:
        while self._queue:
            self._pop_oldest()
            self._dropped += 1
        for version in list(self._revisions):
            self._forget_revision(version)

    # ── Shutdown ────────────────────────────────────────────────────────

    def _begin_close(self) -> None:
        with self._lock:
            self._closing = True
            self._lock.notify_all()

    def _finish_close(self, deadline: float) -> None:
        with self._lock:
            if self._stopped:
                return
            while (
                self._thread is not None
                and (self._queue or self._inflight or self._latest_undelivered())
                and not self._disabled
                and (remaining := deadline - time.monotonic()) > 0
            ):
                self._lock.wait(remaining)
            if self._inflight is not None:
                self._unconfirmed += self._inflight.observations
                self._inflight = None
            self._discard_queue()
            self._stopped = True
            self._lock.notify_all()
            lost = self._dropped + self._rejected + self._unconfirmed
            report = (
                f"River metrics for training run {self._training_run_id}: "
                f"{lost} observations were not delivered ({self._dropped} "
                f"discarded locally, {self._rejected} rejected by River Console, "
                f"{self._unconfirmed} unconfirmed at shutdown)"
                if lost
                else None
            )
        _warn(report)

    # ── Warnings ────────────────────────────────────────────────────────

    def _should_warn(self, cause: str) -> bool:
        """Rate-limit one warning cause; call with the lock held."""
        now = time.monotonic()
        last = self._warned_at.get(cause)
        if last is not None and now - last < WARNING_INTERVAL_S:
            return False
        self._warned_at[cause] = now
        return True

    def _overflow_warning(self, dropped: int) -> str | None:
        if not dropped or not self._should_warn("overflow"):
            return None
        return (
            f"River metrics buffer for training run {self._training_run_id} is "
            f"full; discarded the oldest observations ({self._dropped} so far)"
        )

    def _not_accepting_warning(self) -> str | None:
        if self._disabled:
            reason = f"metrics delivery is disabled: {self._disabled}"
        else:
            reason = "its session has ended"
        if not self._should_warn("not accepting"):
            return None
        return (
            f"model.log() discarded an observation for training run "
            f"{self._training_run_id} because {reason} "
            f"({self._dropped} discarded so far)"
        )

    def _skip_inherited(self) -> None:
        """Skip a call on a writer inherited through fork, without its lock."""
        self._inherited_skipped += 1
        now = time.monotonic()
        last = self._inherited_warned_at
        if last is not None and now - last < WARNING_INTERVAL_S:
            return
        self._inherited_warned_at = now
        _warn(
            f"Metrics for training run {self._training_run_id} belong to "
            f"process {self._pid}; metrics calls from forked process "
            f"{os.getpid()} are not delivered ({self._inherited_skipped} skipped so far)"
        )


def drain(writers: Iterable[_RunMetrics], timeout_s: float = DRAIN_TIMEOUT_S) -> None:
    """Deliver what ``writers`` buffered within ``timeout_s`` in total; never raises.

    Writers inherited from a parent process are left alone.
    """
    try:
        owned = [writer for writer in writers if writer._pid == os.getpid()]
        deadline = time.monotonic() + timeout_s
        for writer in owned:
            writer._begin_close()
        for writer in owned:
            writer._finish_close(deadline)
    except Exception:
        _warn("River run metrics shutdown failed", exc_info=True)


@dataclass(frozen=True)
class _Observation:
    body: bytes
    values: int
    version: int
    enqueued_at: float


@dataclass(frozen=True)
class _Batch:
    body: bytes
    # Byte size of each definition revision the batch carries.
    revisions: dict[int, int]
    observations: int
    values: int
    observation_bytes: int


def _warn(message: str | None, *, exc_info: bool = False) -> None:
    """Log a diagnostic; a failing log handler never reaches training."""
    if message is None:
        return
    try:
        _logger.warning(message, exc_info=exc_info)
    except Exception:
        pass


def _check_name(kind: str, name: object) -> str:
    if not isinstance(name, str):
        raise TypeError(f"{kind} names must be str, got {type(name).__name__}")
    if not name or len(name.encode("utf-8")) > MAX_NAME_BYTES:
        raise ValueError(f"{kind} names must be 1 to {MAX_NAME_BYTES} bytes: {name!r}")
    return name


def _check_pattern(name: object) -> None:
    pattern = _check_name("definition", name)
    if pattern.startswith(RESERVED_PREFIX):
        raise ValueError(
            f"{pattern!r} is reserved: names starting with {RESERVED_PREFIX!r} belong to River"
        )
    star = pattern.find("*")
    if star != -1 and star != len(pattern) - 1:
        raise ValueError(
            f"definition {pattern!r} may only use * as its last character, "
            'such as "train/*"'
        )


def _check_step_metric(name: object) -> None:
    step_metric = _check_name("step metric", name)
    if "*" in step_metric:
        raise ValueError(
            f"step_metric {step_metric!r} must be a metric name, not a pattern"
        )
    if step_metric.startswith(RESERVED_PREFIX) and step_metric not in BUILT_IN_AXES:
        raise ValueError(
            f"step_metric {step_metric!r} is reserved; River's built-in axes are "
            f"{TIMESTAMP_AXIS!r} and {RUNTIME_AXIS!r}"
        )


def _check_values(data: object) -> dict[str, float]:
    """A copy of ``data`` as finite floats, or an error naming the bad entry."""
    if not isinstance(data, Mapping):
        raise TypeError(
            f"model.log() takes a mapping of metric names to numbers, got {type(data).__name__}"
        )
    if not data:
        raise ValueError("model.log() needs at least one metric value")
    if len(data) > MAX_BATCH_VALUES:
        raise ValueError(
            f"model.log() accepts at most {MAX_BATCH_VALUES} values per call, got {len(data)}"
        )
    values = {}
    for key, value in data.items():
        name = _check_name("metric", key)
        if name.startswith(RESERVED_PREFIX):
            raise ValueError(
                f"metric {name!r} is reserved: names starting with {RESERVED_PREFIX!r} belong to River"
            )
        values[name] = _scalar(name, value)
    return values


def _scalar(name: str, value: object) -> float:
    if isinstance(value, (bool, np.bool_)) or not isinstance(
        value, (int, float, np.integer, np.floating)
    ):
        raise TypeError(
            f"metric {name!r} must be a real number, got {type(value).__name__}; "
            "convert tensors and arrays with .item()"
        )
    try:
        number = float(value)
    except OverflowError:
        raise ValueError(f"metric {name!r} is too large for a float: {value}") from None
    if not math.isfinite(number):
        raise ValueError(f"metric {name!r} must be finite, got {number}")
    return number
