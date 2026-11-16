"""One sampler per serving device group; concurrent requests share honest device observations, never invented shares.
An arrival reads only for requests still waiting for their first reading; a fixed 1 Hz tick fills every request. A
request holds only reads that began while it ran: one that ends inside a read gap holds none (below the sampling
resolution, not missing data) and is never given a later read; one that outlived two gaps with none (a slow read held
the sampler) says incomplete."""

import asyncio
import functools
import math
import logging
import socket
import time
from datetime import datetime, timezone

from ..resources.nvidia import NvidiaResource
from ..trace import GpuTrace

logger = logging.getLogger(__name__)


#: The shortest gap between two sensor reads (s): arrivals inside it share the next read (D7, at most 10 reads/s).
MIN_READ_GAP_S = 0.1
#: How long one read may take before the sampler gives up on the sensors for good (s). The first read also starts
#: NVML for the device group, which a busy many-GPU node can take seconds over.
READ_TIMEOUT_S = 0.5
FIRST_READ_TIMEOUT_S = 10.0


class GpuRequests:
    def __init__(self, *, create_resource=None, interval=1.0, max_readings=512, visible_devices=None,
                 min_gap=MIN_READ_GAP_S) -> None:  # fmt: skip
        self._create_resource = create_resource or functools.partial(NvidiaResource.create, strict_visible=True,
                                                                    visible_devices=visible_devices)
        self._resource = None
        self._interval = interval
        self._min_gap = min(min_gap, interval)
        self._max_readings = max_readings
        self._active = {}
        self._lock = asyncio.Lock()
        self._wake = asyncio.Event()
        self._task = None
        self._is_initialized = False
        self._has_failed = False
        self._is_abandoned = False

    async def start_request(self, request_id: str) -> dict:
        entry = {"request_id": request_id, "trace": GpuTrace(self._max_readings), "sampled": asyncio.Event(),
                 "started": time.monotonic()}
        self._active[id(entry)] = entry
        self._wake.set()
        if self._is_abandoned:
            entry["trace"].is_incomplete = True
            entry["sampled"].set()
        if self._task is None:
            self._task = asyncio.create_task(self._sample_until_idle())
        return entry

    async def finish_request(self, entry: dict) -> dict:
        """The request's readings. It waits only for a read that began while the request ran: neither a previous
        request's observation nor one taken after it ended stands in for its first, and the reply never waits for the
        next read gap."""
        entry["ended"] = True
        try:
            if entry.get("is_in_read") and not entry["sampled"].is_set():
                try:
                    await asyncio.wait_for(entry["sampled"].wait(), timeout=READ_TIMEOUT_S)
                except asyncio.TimeoutError:
                    entry["trace"].is_incomplete = True
            elif not entry["sampled"].is_set() and time.monotonic() - entry["started"] > 2 * self._min_gap:
                entry["trace"].is_incomplete = True  # a read should have begun while it ran: the sampler was held up
        finally:
            self._active.pop(id(entry), None)
        return entry["trace"].to_dict()

    async def drop_request(self, entry: dict) -> None:
        """Forget a request without waiting for its reading (one Probe will not report, e.g. a batch)."""
        self._active.pop(id(entry), None)

    async def _sample_until_idle(self) -> None:
        """A tick fills every active request once per interval, on a fixed clock an arrival never resets; between
        ticks, an arrival's read fills only requests still waiting for their first reading. Reads are at least
        `min_gap` apart, so arrivals inside one gap share a read."""
        loop = asyncio.get_running_loop()
        last_read = -math.inf
        next_tick = loop.time()
        try:
            while self._active:
                self._wake.clear()
                now = loop.time()
                is_tick = now >= next_tick
                if not is_tick and not self._has_waiting():
                    try:
                        await asyncio.wait_for(self._wake.wait(), timeout=next_tick - now)
                    except asyncio.TimeoutError:
                        pass
                    continue
                gap = last_read + self._min_gap - now
                if gap > 0:
                    await asyncio.sleep(gap)
                    continue
                last_read = loop.time()
                await self._sample(is_arrival=not is_tick)
                if is_tick:
                    next_tick = max(next_tick + self._interval, loop.time())
        finally:
            self._task = None

    def _has_waiting(self) -> bool:
        return any(not entry["sampled"].is_set() and not entry.get("ended") for entry in self._active.values())

    async def close(self) -> None:
        self._active.clear()
        if self._task is not None:
            self._task.cancel()
            await asyncio.gather(self._task, return_exceptions=True)
        if self._resource is not None:
            await asyncio.to_thread(self._resource.close)

    async def _sample(self, *, is_arrival: bool = False) -> None:
        """One read. A request takes only readings whose read began after it arrived (the snapshot below)."""
        async with self._lock:
            running = [entry for entry in self._active.values() if not entry.get("ended")]
            entries = tuple(entry for entry in running if not is_arrival or not entry["sampled"].is_set())
            active = len(running)  # the overlap when the read began, every running request counted
            for entry in entries:
                entry["is_in_read"] = True
            if self._is_abandoned:
                for entry in entries:
                    entry["trace"].is_incomplete = True
                    entry["sampled"].set()
                return
            # NVML initialization and sensors can block. They never run on the serving event loop.
            timeout = READ_TIMEOUT_S if self._is_initialized else FIRST_READ_TIMEOUT_S
            try:
                observed_at, devices = await asyncio.wait_for(asyncio.to_thread(self._read_devices), timeout=timeout)
            except asyncio.TimeoutError:
                self._is_abandoned = True
                for entry in entries:
                    entry["trace"].is_incomplete = True
                    entry["sampled"].set()
                logger.warning("Probe serving GPU sensors timed out; generation continues without further sensor reads")
                return
            host = socket.gethostname()
            for entry in entries:
                if id(entry) not in self._active:
                    continue
                entry["trace"].is_incomplete |= self._has_failed or self._resource is None
                for device, metrics in devices.items():
                    reading = {"wall_clock": observed_at, "host": host, "device": device,
                               "request_id": entry["request_id"], "active_requests": active,
                               "attribution": "shared_device", "metrics": metrics}
                    entry["trace"].append(reading)
                entry["sampled"].set()

    def _read_devices(self) -> tuple[str, dict]:
        now = time.time()
        devices = {}
        try:
            if not self._is_initialized:
                self._is_initialized = True
                self._resource = self._create_resource()
            if self._resource is not None and not self._has_failed:
                for sample in self._resource.sample(now):
                    if sample.key.startswith("hw/gpu/") and math.isfinite(sample.value):
                        device = self._resource.get_device_uuid(sample.coords["gpu"])
                        devices.setdefault(device, {})[sample.key.removeprefix("hw/")] = sample.value
        except Exception as exc:
            self._has_failed = True
            logger.warning("Probe could not read serving GPU observations; generation continues: %s", exc)
        return datetime.fromtimestamp(now, timezone.utc).isoformat(), devices
