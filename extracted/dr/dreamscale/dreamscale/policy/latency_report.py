"""Per-request latency reports: what each obs→act request spent where.

Each request leaves a small record of the timings the SDK already measures (client
pre/post-processing, encode, the round trip, and the server's own times from the chunk). The
session sends them to the control plane in the background, every ``FLUSH_EVERY_S`` and at
close, never on a request's path. Records carry durations, byte counts and engine/transport
labels only: no observations, actions or instructions.

Off when ``DREAMSCALE_TELEMETRY`` is ``0``/``false``/``off``/``no``, when ``DO_NOT_TRACK`` is
set, or with ``[telemetry] enabled = false`` in config.toml.
"""

from __future__ import annotations

import asyncio
import math
import os
import time
from collections.abc import Awaitable, Callable, Mapping
from contextlib import suppress
from typing import Any

OPT_OUT_ENV = "DREAMSCALE_TELEMETRY"
FLUSH_EVERY_S = 30.0
FLUSH_TIMEOUT_S = 2.0
MAX_BUFFER = 900
MAX_PHASES = 32
_OFF = frozenset({"0", "false", "off", "no"})
_ON = frozenset({"1", "true", "yes", "on"})

Send = Callable[[list[dict[str, Any]], int], Awaitable[Any]]


def reports_enabled(environ: Mapping[str, str] | None = None) -> bool:
    environ = os.environ if environ is None else environ
    if (environ.get(OPT_OUT_ENV) or "").strip().lower() in _OFF:
        return False
    if (environ.get("DO_NOT_TRACK") or "").strip().lower() in _ON:
        return False
    try:
        from dreamscale.config import load_config

        return bool(getattr(load_config(), "telemetry", True))
    except Exception:  # an unreadable config.toml doesn't stop a session
        return True


def _ms(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float) or not math.isfinite(value):
        return None
    return round(max(0.0, float(value)), 3)


def _server_phases(chunk: Any) -> tuple[dict[str, float], str | None]:
    metadata = getattr(chunk, "runtime_metadata", None)
    server = getattr(metadata, "server", None) if metadata is not None else None
    if not isinstance(server, Mapping):
        return {}, None
    phases = {}
    for key, value in server.items():
        if isinstance(key, str) and key.endswith("_ms") and (ms := _ms(value)) is not None:
            phases[key] = ms
            if len(phases) >= MAX_PHASES:
                break
    engine = server.get("engine")
    return phases, engine if isinstance(engine, str) else None


def record(
    result: Any,
    *,
    started_unix_ns: int,
    client_pre_ms: float,
    client_post_ms: float,
    calibration: bool = False,
) -> dict[str, Any]:
    """One request's record, from its ``ActionChunkResult``."""
    timing = result.timing
    phases, engine = _server_phases(getattr(result, "raw_chunk", None))
    fields = {
        "started_unix_ns": int(started_unix_ns),
        "obs_to_action_ms": _ms(timing.obs_to_action_ms),
        "client_pre_ms": _ms(client_pre_ms),
        "client_post_ms": _ms(client_post_ms),
        "client_encode_ms": _ms(timing.client_encode_ms),
        "transport_send_ms": _ms(timing.transport_send_ms),
        "server_ms": _ms(timing.server_total_ms),
        "server_pre_ms": _ms(timing.server_queue_ms),
        "worker_inference_ms": _ms(timing.worker_inference_ms),
        "worker_queue_ms": _ms(timing.worker_queue_ms),
        "data_plane_rtt_ms": _ms(timing.data_plane_rtt_ms),
        "uplink_ms": _ms(getattr(timing, "uplink_ms", None)),
        "downlink_ms": _ms(getattr(timing, "downlink_ms", None)),
        "clock_offset_uncertainty_ms": _ms(getattr(timing, "clock_offset_uncertainty_ms", None)),
        "upload_bytes": timing.upload_bytes,
        "transport": getattr(result, "transport_mode", None),
        "engine": getattr(result, "engine", None) or engine,
        "calibration": calibration or None,
        "server_phases": phases or None,
    }
    return {key: value for key, value in fields.items() if value is not None}


class LatencyReporter:
    """Buffers a session's records and sends them in the background."""

    def __init__(
        self,
        send: Send | None,
        *,
        enabled: bool,
        spawn: Callable[[Awaitable[Any]], Any],
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._send = send
        self.enabled = enabled and send is not None
        self._spawn = spawn
        self._clock = clock
        self._buffer: list[dict[str, Any]] = []
        self._dropped = 0
        self._last_flush = clock()
        self._flushing = False
        # Wall clock = monotonic + this, taken once: no wall-clock read per request.
        self._wall_offset_ns = time.time_ns() - time.monotonic_ns()

    def wall_ns(self, monotonic_ns: int) -> int:
        return int(monotonic_ns) + self._wall_offset_ns

    def add(self, entry: dict[str, Any]) -> None:
        if not self.enabled:
            return
        if len(self._buffer) >= MAX_BUFFER:
            self._dropped += 1
        else:
            self._buffer.append(entry)
        if not self._flushing and self._clock() - self._last_flush >= FLUSH_EVERY_S:
            self._flushing = True
            self._spawn(self.flush())

    async def flush(self) -> None:
        """Send what is buffered; failures are dropped, and a control plane without the
        endpoint (or an ended session) turns reporting off."""
        records, dropped = self._buffer, self._dropped
        self._buffer, self._dropped = [], 0
        self._last_flush = self._clock()
        try:
            if records and self.enabled and self._send is not None:
                with suppress(Exception):
                    await asyncio.wait_for(self._send(records, dropped), FLUSH_TIMEOUT_S)
        finally:
            self._flushing = False

    async def close(self) -> None:
        if self.enabled and self._buffer:
            await self.flush()
        self.enabled = False

    def disable(self) -> None:
        self.enabled = False
        self._buffer = []
