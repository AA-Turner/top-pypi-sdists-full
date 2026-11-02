"""Wiring between the SDK and the collector: default-on at ``run()``,
election, identity snapshot, the wire emit, and inventory publication.

Everything here is fail-open: a broken collector must never touch the run.
"""

from __future__ import annotations

import functools
import logging
import os
import socket
import weakref

from probe.sdk.hardware.grid import HW_STEP_SECONDS
from probe.sdk.hardware.mappings import MappingPack
from probe.sdk.hardware.hardware import HwMonitor, elect_leader
from probe.sdk.hardware.resources.nvidia import NvidiaResource
from probe.sdk.hardware.resources.openmetrics import OpenMetricsResource
from probe.sdk.hardware.resources.system import SystemResource
from probe.sdk.routes import WriteOp, path_for

logger = logging.getLogger(__name__)

# A resume-receipt last_step at or above this is in hardware's epoch range (floor(unix/60) ≈ 29.7M in
# 2026; training steps are far lower): the server predates the #364 hardware exclusion. Warn and
# skip arming, since refusing every training step would gate the run (warn-never-gate).
SUSPECT_RESUME_FLOOR = 10_000_000

_FAMILY_BY_ENDPOINT = {"dcgm": "gpu", "node": "system", "cadvisor": "container"}


def hw_enabled(hw_flag: bool | None, env=None) -> bool:
    """DEFAULT ON (2026-09-21, reversing the opt-in of 2026-08-06): over 30 days of production only 5
    of 209 crashed runs had any hardware series, yet five of the fourteen crash detectors
    (`gpu_thermal`, `gpu_cold`, `gpu_memory_creep`, `host_memory_pressure`, `disk_filling`) read only
    hardware and explain OOMs and SIGKILLs; opt-in left them dark for 97.6% of the runs needing them.

    Explicit ``run(hw=...)`` stays authoritative both ways. ``PROBE_HW=0`` (or ``false``/``off``)
    disables, as `integration.py`'s "hardware metrics on" log line has always claimed.
    """
    if hw_flag is not None:
        return bool(hw_flag)
    env = os.environ if env is None else env
    return str(env.get("PROBE_HW", "1")).strip().lower() not in ("0", "false", "off")


def _default_fetch(url: str) -> str:
    import httpx  # lazy; already a package dep

    from probe.foundation.tls.tls import ssl_context

    resp = httpx.get(url, timeout=2.0, verify=ssl_context())
    resp.raise_for_status()
    return resp.text


class LazyScraper:
    """Exporter scraper whose endpoint discovery runs on the collector's FIRST TICK, never inside run().
    ``families`` starts empty (no tier claims until something answered) and the discovery tick emits
    nothing, so the floor covers the first window alone instead of mixing two estimators."""

    def __init__(self, fetch=_default_fetch, label_filters: dict | None = None):
        self.families: frozenset = frozenset()
        self._fetch = fetch
        self._filters = label_filters if label_filters is not None else _pod_filters()
        self._inner: OpenMetricsResource | None = None
        self._discovered = False

    def sample(self, ts: float):
        if not self._discovered:
            self._discovered = True
            found = OpenMetricsResource.discover(fetch=self._fetch)
            if found:
                self._inner = OpenMetricsResource(
                    endpoints=found,
                    fetch=self._fetch,
                    pack=MappingPack.default(),
                    label_filters=self._filters,
                )
                self.families = frozenset(
                    _FAMILY_BY_ENDPOINT[name]
                    for name in found
                    if name in _FAMILY_BY_ENDPOINT
                )
            return []
        if self._inner is None:
            return []
        return self._inner.sample(ts)

    def probe(self) -> dict:
        return self._inner.probe() if self._inner else {}


def _pod_filters() -> dict:
    """Filter cluster-scoped exporters to our own pod when the downward API names it."""
    pod = os.environ.get("PROBE_HW_POD_NAME") or os.environ.get("POD_NAME")
    return {"pod": pod} if pod else {}


def build_sources() -> list:
    sources: list = [LazyScraper()]  # tier 2 first: live claims suppress the floor
    system = SystemResource.create()
    if system is not None:
        system.families = frozenset({"system"})
        sources.append(system)
    nvml = NvidiaResource.create()
    if nvml is not None:
        nvml.families = frozenset({"gpu"})
        sources.append(nvml)
    return sources


def _write_to_run(client, method: str, path: str, body: dict) -> bool:
    """The rail's one door for a write TO its run (plan 0.3, D2).

    Async (default): queue in the journal. A direct write collides with the drainer delivering the
    run's metrics (the server's insert takes the row NOWAIT): the 503 behind 4 of 6 short runs raising
    in `finish()`. Queued, it drains FIFO, never holds the close, and a refusal (full queue, low-disk
    floor) returns False: dropped quietly.

    Sync: direct, ``durable=False`` (nothing drains a sync client's journal mid-run, so a queued point
    would reach no chart until `finish()`); the old collision stays (a 503 the SDK retries or spools).
    The collector stops before `finish()` drains; the inventory thread may not.

    Raises if the write could not be made at all; the caller's buffer or ``except`` owns that."""
    if client.async_writes:
        return client._enqueue_best_effort(method, path, body)
    client.write(method, path, body, durable=False)
    return True


def _emit_for(client, run_handle):
    """The collector's emit (see `_write_to_run`).

    Holds the run WEAKLY: a strong reference from the long-lived collector thread would keep an
    abandoned Run (and its heartbeat) alive until exit. A collected run's points are dropped
    (`maybe_start` also stops the collector then)."""
    from probe.models import MetricPointIn  # stable import seam over _generated

    handle_ref = weakref.ref(run_handle)
    path = path_for(WriteOp.METRICS, run_handle.id)

    def emit(points) -> None:
        handle = handle_ref()
        if handle is None:
            return
        body = {
            "points": [
                MetricPointIn(
                    key=p.key,
                    kind="hardware",
                    value=p.value,
                    step_index=p.step,
                    wall_clock=_iso(p.step),
                    dimensions=p.coords or None,
                    agg=p.agg,
                ).model_dump(mode="json", exclude_none=True)
                for p in points
            ]
        }
        # The writer fence every metric op carries (0185), read at EMIT time: a reopen moves the handle to a new epoch mid-run.
        body = handle._stamp_writer(body)
        del handle
        if not _write_to_run(client, "POST", path, body):
            logger.debug("hw: journal refused %d hardware points; dropped", len(points))

    return emit


def _iso(step: int) -> str:
    from datetime import datetime, timezone

    return datetime.fromtimestamp(step * HW_STEP_SECONDS, tz=timezone.utc).isoformat()


def maybe_start(client, run_handle, hw_flag: bool | None):
    """Start the collector if enabled and this process is the node leader. Returns the monitor or None. Never raises."""
    try:
        if not hw_enabled(hw_flag):
            return None
        if not elect_leader(run_handle.id):
            return None
        sources = build_sources()
        if not sources:
            return None
        identity = {"host": socket.gethostname()}
        monitor = HwMonitor(
            sources=sources,
            emit=_emit_for(client, run_handle),
            identity=identity,
            interval=float(os.environ.get("PROBE_HW_INTERVAL", "15")),
            # Own daemon thread; `finish()` waits briefly, so the env_ref PATCH is normally queued before
            # the close drains and a slow API never holds it.
            on_start=functools.partial(
                _publish_from_sources, client, weakref.ref(run_handle), run_handle.id, sources
            ),
        )
        # An abandoned Run (never finished, unreferenced) stops its collector when collected, like its
        # heartbeat. The callback holds the monitor weakly: finalize() keeps it alive as long as the Run.
        weakref.finalize(run_handle, _request_stop, weakref.ref(monitor))
        monitor.start()
        logger.info(
            "probe: hardware metrics on for %s (PROBE_HW=0 or run(hw=False) disables)",
            run_handle.id,
        )
        return monitor
    except Exception:  # noqa: BLE001 — a broken collector must never touch the run
        logger.debug("hw: collector failed to start", exc_info=True)
        return None


def _request_stop(monitor_ref) -> None:
    monitor = monitor_ref()
    if monitor is not None:
        monitor.request_stop()


def _publish_from_sources(client, handle_ref, run_id: str, sources) -> None:
    """probe() can block (NVML init, HTTP), so this runs off the run() path. The run is held weakly, like emit."""

    def current_env_ref():
        handle = handle_ref()
        # A gone run counts as pinned: never overwrite what its snapshot left.
        if handle is None:
            return "<run gone>"
        # The open's snapshot asks for its record on a thread of its own (bounded): its pin
        # comes once that answers, so ask after it, or a hardware-only record races it. Once
        # the run is closing, nothing may pin: a PATCH queued now lands after the status.
        if not handle._wait_for_open_record():
            return handle.env_ref or "<run closing>"
        return handle.env_ref

    try:
        inventory: dict = {}
        for src in sources:
            try:
                inventory.update(src.probe() or {})
            except Exception:  # noqa: BLE001
                continue
        if handle_ref() is None:
            return  # an abandoned run: nothing left to describe
        publish_inventory(
            client,
            run_id=run_id,
            # Read at the last moment: `Run.env_ref` knows what the snapshot pinned even while its PATCH is queued.
            env_ref=current_env_ref,
            inventory=inventory,
        )
    except Exception:  # noqa: BLE001
        logger.debug("hw: inventory publication failed", exc_info=True)


def _current_env_ref(env_ref) -> str | None:
    """``env_ref`` is a value, or a callable that reads it now."""
    return env_ref() if callable(env_ref) else env_ref


def publish_inventory(client, *, run_id: str, env_ref, inventory: dict) -> None:
    """Mint a minimal execution record with the hardware inventory, only if the run has no env_ref yet
    (a real snapshot's record, which already carries `hardware`, is never clobbered). ``env_ref`` is the
    run's current env_ref or a zero-argument callable returning it.

    The record POST stays direct (content-addressed, names no run; the PATCH needs the SERVER-computed
    hash). The PATCH goes through `_write_to_run`: queued behind the run's writes under async (plan 0.3)."""
    if not inventory:
        return
    if _current_env_ref(env_ref):
        logger.debug("hw: run %s already has env_ref; inventory mint skipped", run_id)
        return
    record = client.send(
        "POST", "/v1/execution-records", {"hardware": inventory}, durable=False
    )
    content_hash = (record or {}).get("content_hash")
    # Re-checked before queueing: a snapshot() that pinned while the record was in flight must win.
    if content_hash and not _current_env_ref(env_ref):
        _write_to_run(client, "PATCH", path_for(WriteOp.RUN_PATCH, run_id), {"env_ref": content_hash})
