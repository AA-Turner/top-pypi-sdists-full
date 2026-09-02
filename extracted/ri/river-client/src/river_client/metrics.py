"""Fire-and-forget run metric ingestion for River Console."""

from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import json
import logging
import math
import os
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request as _UrlRequest
from urllib.request import urlopen as _urlopen

_logger = logging.getLogger(__name__)

_DEFAULT_BASE_URL = "https://console.river.ai"
_USER_AGENT = "river-client/0.1"
_MAX_BATCH_SIZE = 1_000
_HTTP_TIMEOUT_S = 5.0
_RETRY_INITIAL_S = 0.5
_RETRY_MAX_S = 30.0
_CLOSE_DRAIN_TIMEOUT_S = 5.0
_MAX_U64 = (1 << 64) - 1


@dataclass(frozen=True)
class _MetricPoint:
    metric: str
    step: int
    value: float
    logged_at: str


class RunMetricsLogger:
    """Buffers and sends run metrics without interrupting training."""

    def __init__(
        self,
        api_key: str,
        training_run_id: str,
        base_url: str | None = None,
        flush_interval_s: float = 2.0,
        max_buffer: int = 10_000,
    ) -> None:
        self._api_key = api_key
        self._training_run_id = training_run_id
        if base_url is None:
            base_url = os.environ.get("RIVER_CONSOLE_URL", _DEFAULT_BASE_URL)
        self._base_url = base_url.rstrip("/")
        self._flush_interval_s = max(float(flush_interval_s), 0.0)
        self._max_buffer = max(int(max_buffer), 1)
        self._pending: deque[_MetricPoint] = deque()
        self._inflight: list[_MetricPoint] = []
        self._condition = threading.Condition()
        self._warning_causes: set[str] = set()
        self._flush_requested = False
        self._closed = False
        self._abandon = False
        self._next_attempt_at: float | None = None
        self._retry_delay_s = _RETRY_INITIAL_S
        self._permanent_rejection_count = 0
        self._disabled = False
        self._worker = threading.Thread(
            target=self._run,
            name="river-run-metrics",
            daemon=True,
        )
        self._worker.start()

    def __enter__(self) -> RunMetricsLogger:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.close()
        return False

    def log(self, metric: str, step: int, value: float) -> None:
        """Queue one metric point and return without waiting for the network."""
        try:
            point = self._new_point(metric, step, value)
            if point is None:
                return
            with self._condition:
                if self._closed:
                    self._warn_once(
                        "closed logger",
                        "Run metrics logger is closed; dropping metric point",
                    )
                    return
                if self._disabled:
                    return
                if len(self._pending) + len(self._inflight) == self._max_buffer:
                    if self._pending:
                        self._pending.popleft()
                    else:
                        self._warn_once(
                            "full buffer",
                            "Run metrics buffer is full; dropping a metric point",
                        )
                        return
                    self._warn_once(
                        "full buffer",
                        "Run metrics buffer is full; dropping the oldest metric point",
                    )
                self._pending.append(point)
                self._condition.notify()
        except Exception as error:
            _logger.warning("Run metrics logger dropped a metric point: %s", error)

    def flush(self) -> None:
        """Request prompt delivery of the points currently in the buffer."""
        try:
            with self._condition:
                self._flush_requested = True
                self._condition.notify()
        except Exception as error:
            _logger.warning("Run metrics logger could not flush: %s", error)

    def close(self) -> None:
        """Drain buffered points when possible, then stop the worker."""
        try:
            with self._condition:
                if self._closed:
                    return
                self._closed = True
                self._flush_requested = True
                self._condition.notify()
            self._worker.join(_CLOSE_DRAIN_TIMEOUT_S)
            if self._worker.is_alive():
                with self._condition:
                    self._abandon = True
                    self._condition.notify()
                self._worker.join(_HTTP_TIMEOUT_S)
                self._warn_once(
                    "close timeout",
                    "Run metrics logger stopped before it could drain all metric points",
                )
        except Exception as error:
            _logger.warning("Run metrics logger could not close: %s", error)

    def _new_point(
        self,
        metric: str,
        step: int,
        value: float,
    ) -> _MetricPoint | None:
        if not isinstance(metric, str) or not metric:
            self._warn_once(
                "invalid metric", "Run metrics logger skipped an invalid metric"
            )
            return None
        if (
            not isinstance(step, int)
            or isinstance(step, bool)
            or not 0 <= step <= _MAX_U64
        ):
            self._warn_once(
                "invalid step", "Run metrics logger skipped an invalid step"
            )
            return None
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            self._warn_once(
                "invalid value", "Run metrics logger skipped an invalid value"
            )
            return None
        if not math.isfinite(numeric_value):
            _logger.warning("Run metrics logger skipped a non-finite metric value")
            return None
        return _MetricPoint(
            metric=metric,
            step=step,
            value=numeric_value,
            logged_at=datetime.now(UTC).isoformat(timespec="milliseconds"),
        )

    def _run(self) -> None:
        while True:
            with self._condition:
                batch = self._next_batch()
                if batch is None:
                    return
            status = _post_metric_points(
                api_key=self._api_key,
                base_url=self._base_url,
                training_run_id=self._training_run_id,
                points=batch,
            )
            with self._condition:
                if status == 204:
                    self._inflight = []
                    self._retry_delay_s = _RETRY_INITIAL_S
                    self._next_attempt_at = None
                    self._permanent_rejection_count = 0
                elif status is not None and 400 <= status < 500:
                    self._inflight = []
                    self._retry_delay_s = _RETRY_INITIAL_S
                    self._next_attempt_at = None
                    self._permanent_rejection_count += 1
                    self._warn_once(
                        f"HTTP {status}",
                        f"Run metrics server rejected a batch with HTTP {status}; dropping it",
                    )
                    if self._permanent_rejection_count >= 3:
                        self._pending.clear()
                        self._disabled = True
                        self._abandon = True
                        self._warn_once(
                            "repeated rejections",
                            "Run metrics logger disabled after repeated rejections",
                        )
                else:
                    self._permanent_rejection_count = 0
                    self._next_attempt_at = time.monotonic() + self._retry_delay_s
                    self._retry_delay_s = min(self._retry_delay_s * 2, _RETRY_MAX_S)

    def _next_batch(self) -> list[_MetricPoint] | None:
        while True:
            if self._abandon:
                return None
            if not self._inflight:
                if not self._pending:
                    self._flush_requested = False
                    if self._closed:
                        return None
                    self._condition.wait()
                    continue
                if self._flush_requested and self._next_attempt_at is None:
                    self._inflight = self._take_batch()
                    return self._inflight
                if self._next_attempt_at is None:
                    self._next_attempt_at = time.monotonic() + self._flush_interval_s
            next_attempt_at = self._next_attempt_at
            if next_attempt_at is None:
                next_attempt_at = time.monotonic() + self._flush_interval_s
                self._next_attempt_at = next_attempt_at
            remaining = next_attempt_at - time.monotonic()
            if remaining <= 0:
                self._next_attempt_at = None
                if not self._inflight:
                    self._inflight = self._take_batch()
                return self._inflight
            self._condition.wait(remaining)

    def _take_batch(self) -> list[_MetricPoint]:
        size = min(len(self._pending), _MAX_BATCH_SIZE)
        return [self._pending.popleft() for _ in range(size)]

    def _warn_once(self, cause: str, message: str) -> None:
        with self._condition:
            if cause in self._warning_causes:
                return
            self._warning_causes.add(cause)
        _logger.warning(message)


def _post_metric_points(
    api_key: str,
    base_url: str,
    training_run_id: str,
    points: list[_MetricPoint],
) -> int | None:
    request = _UrlRequest(
        f"{base_url}/api/metrics/runs/{quote(training_run_id, safe='')}/points",
        data=json.dumps({"points": [asdict(point) for point in points]}).encode(
            "utf-8"
        ),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": _USER_AGENT,
        },
        method="POST",
    )
    try:
        with _urlopen(request, timeout=_HTTP_TIMEOUT_S) as response:
            return response.getcode()
    except HTTPError as error:
        error.read()
        return error.code
    except (OSError, URLError):
        return None
    except Exception:
        return None
