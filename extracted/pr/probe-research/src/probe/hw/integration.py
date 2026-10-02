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

from probe.hw.grid import HW_STEP_SECONDS
from probe.hw.mappings import MappingPack
from probe.hw.monitor import HwMonitor, elect_leader
from probe.hw.resources.nvidia import NvidiaResource
from probe.hw.resources.openmetrics import OpenMetricsResource
from probe.hw.resources.system import SystemResource

logger = logging.getLogger(__name__)

# A resume-receipt last_step at or above this is in hardware's epoch range
# (floor(unix/60) ≈ 29.7M in 2026; training steps live orders of magnitude
# lower): the server predates the #364 hardware exclusion. Warn and skip
# arming — refusing every training step would gate the run (warn-never-gate).
SUSPECT_RESUME_FLOOR = 10_000_000

_FAMILY_BY_ENDPOINT = {"dcgm": "gpu", "node": "system", "cadvisor": "container"}


def hw_enabled(hw_flag: bool | None, env=None) -> bool:
    """DEFAULT ON (2026-09-21, reversing the opt-in revision of 2026-08-06).

    The opt-in default was conservatism -- a bare run() behaving exactly as
    before the hw rail existed -- and it cost more than it protected. Measured
    over 30 days of production: of 209 crashed runs, FIVE had any hardware
    series. Five of the fourteen crash detectors (`gpu_thermal`, `gpu_cold`,
    `gpu_memory_creep`, `host_memory_pressure`, `disk_filling`) read only
    hardware, and they are the ones that explain an OOM or a SIGKILL -- the
    deaths a researcher can least diagnose alone. Opt-in meant the most
    valuable third of the library was dark for 97.6% of the runs that needed
    it.

    Explicit ``run(hw=...)`` remains authoritative in both directions, so a
    caller who has chosen is never overridden. ``PROBE_HW=0`` (or ``false`` /
    ``off``) disables -- which is what `integration.py`'s own "hardware
    metrics on" log line has claimed since the rail was built.
    """
    if hw_flag is not None:
        return bool(hw_flag)
    env = os.environ if env is None else env
    return str(env.get("PROBE_HW", "1")).strip().lower() not in ("0", "false", "off")


def _default_fetch(url: str) -> str:
    import httpx  # lazy; already a package dep

    from probe.sdk.tls import ssl_context

    resp = httpx.get(url, timeout=2.0, verify=ssl_context())
    resp.raise_for_status()
    return resp.text


class LazyScraper:
    """Exporter scraper whose endpoint discovery happens on the collector
    thread's FIRST TICK — never inside run(). ``families`` starts empty (no
    tier claims until something actually answered) and the discovery tick
    emits nothing, so the floor covers the first window alone rather than
    mixing two estimators into one window."""

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
    """Attribution for cluster-scoped exporters: filter to our own pod when
    the downward API says who we are."""
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

    Async writes (the default): queue it in the journal. A direct write lands
    on the run row while the drainer is delivering the run's own metrics, and
    the server's metric insert takes that row NOWAIT -- the 503 behind 4 of 6
    short runs raising in `finish()` with hardware on. Queued, it drains FIFO
    with the run's other ops, never holds the close, and a refusal (full
    queue, low-disk floor) returns False: dropped quietly.

    Sync writes: direct, ``durable=False``, as before -- nothing drains a sync
    client's journal while the run lives, so a queued point would reach no
    chart until `finish()`. The run's own writes are direct there too, so
    sync mode keeps the old collision (a 503 the SDK retries or spools); the
    collector stops before `finish()` drains, but the inventory thread may not.

    Raises when the write could not be made at all (a broken journal, a failed
    direct write): the caller's bounded buffer or ``except`` owns that."""
    if client.async_writes:
        return client._enqueue_best_effort(method, path, body)
    client.write(method, path, body, durable=False)
    return True


def _emit_for(client, run_handle):
    """The collector's emit (see `_write_to_run`).

    Holds the run WEAKLY: the collector thread outlives any caller, and a
    strong reference from it would keep an abandoned Run alive -- and its
    heartbeat beating -- until the process exits. A collected run's points
    are dropped (`maybe_start` also stops the collector then)."""
    from probe.models import MetricPointIn  # stable import seam over _generated

    handle_ref = weakref.ref(run_handle)
    path = f"/v1/runs/{run_handle.id}/metrics"

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
        # The writer fence every metric op carries (0185), read at EMIT time:
        # a reopen after an outage moves the handle to a new epoch mid-run.
        body = handle._stamp_writer(body)
        del handle
        if not _write_to_run(client, "POST", path, body):
            logger.debug("hw: journal refused %d hardware points; dropped", len(points))

    return emit


def _iso(step: int) -> str:
    from datetime import datetime, timezone

    return datetime.fromtimestamp(step * HW_STEP_SECONDS, tz=timezone.utc).isoformat()


def maybe_start(client, run_handle, hw_flag: bool | None):
    """Start the collector for this run if enabled and this process is the
    node leader. Returns the monitor or None. Never raises."""
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
            # Its own daemon thread; `finish()` waits for it briefly, so in
            # the common case the env_ref PATCH is queued before the close
            # drains, and a slow API never holds the close.
            on_start=functools.partial(
                _publish_from_sources, client, weakref.ref(run_handle), run_handle.id, sources
            ),
        )
        # An abandoned Run (never finished, no references left) stops its
        # collector when it is collected, as its heartbeat does.
        # The callback holds the monitor weakly: finalize() keeps its callback
        # alive as long as the Run, and a finished run's monitor must not be.
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
    """probe() can block (NVML init, HTTP), so this runs off the run() path.
    The run is held weakly, like the collector's emit."""

    def current_env_ref():
        handle = handle_ref()
        # A run that is gone counts as pinned: nothing may overwrite whatever
        # its snapshot left on the row.
        return "<run gone>" if handle is None else handle.env_ref

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
            # Read at the last moment: `Run.env_ref` knows what the handle's
            # own snapshot pinned, even while that PATCH is still queued.
            env_ref=current_env_ref,
            inventory=inventory,
        )
    except Exception:  # noqa: BLE001
        logger.debug("hw: inventory publication failed", exc_info=True)


def _current_env_ref(env_ref) -> str | None:
    """``env_ref`` is a value, or a callable that reads it now."""
    return env_ref() if callable(env_ref) else env_ref


def publish_inventory(client, *, run_id: str, env_ref, inventory: dict) -> None:
    """Mint a minimal execution record carrying the hardware inventory -- but
    only when the run has no env_ref yet: a real snapshot's record is never
    clobbered (its own record already carries `hardware`). ``env_ref`` is the
    run's current env_ref, or a zero-argument callable returning it.

    The record POST stays direct: it is content-addressed, names no run, and
    the PATCH needs the hash the SERVER computes (the client never supplies
    one). The PATCH is a write to the run, so it takes `_write_to_run`:
    queued behind the run's own writes under async writes (plan 0.3)."""
    if not inventory:
        return
    if _current_env_ref(env_ref):
        logger.debug("hw: run %s already has env_ref; inventory mint skipped", run_id)
        return
    record = client.write(
        "POST", "/v1/execution-records", {"hardware": inventory}, durable=False
    )
    content_hash = (record or {}).get("content_hash")
    # Checked again right before queueing: a snapshot() that pinned while the
    # record was in flight must win, and this PATCH would land after its.
    if content_hash and not _current_env_ref(env_ref):
        _write_to_run(client, "PATCH", f"/v1/runs/{run_id}", {"env_ref": content_hash})
