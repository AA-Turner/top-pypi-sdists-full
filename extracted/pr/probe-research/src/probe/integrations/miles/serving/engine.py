"""SGLang's `TokenizerManager.generate_request` (`tokenizer_manager.py:981` at sglang-miles@18a44326), wrapped: each
single generate request's final output carries the GPU readings taken while it ran, in `meta_info[GPU_FIELD]`, read
from its own engine's GPUs (`devices.py`). Batches pass through untouched. Why: DESIGN.md beside this file."""

from __future__ import annotations

import functools
import logging
import os
import time
import uuid
from collections.abc import AsyncIterator, Mapping
from contextlib import aclosing
from typing import Any

from probe.sdk.hardware.requests import GpuRequestGroups

from .serving import GPU_FIELD, TIMING_ENV
from .devices import EngineDevices, read_engine_devices

log = logging.getLogger(__name__)
timing_log = logging.getLogger("probe.miles.serving.timing")
_MARK = "__probe_wrapped__"
_warned: set[str] = set()


class EngineGpu:
    """One engine process's samplers (one per device group) and what its placement says up front."""

    def __init__(self, devices: EngineDevices, groups: GpuRequestGroups | None = None) -> None:
        self.devices = devices
        self.groups = groups or GpuRequestGroups()

    async def start(self, request_input: Any) -> dict | None:
        """The request's sampler entry; None when Probe reads nothing for it. A routed DP request that names no
        group gets an empty, incomplete trace (never another group's GPUs)."""
        rank = getattr(request_input, "routed_dp_rank", None)
        if rank is None:
            rank = getattr(request_input, "data_parallel_rank", None)  # the deprecated alias SGLang normalizes later
        group = self.devices.get_group(rank)
        if group is None:
            return {"unrouted": True}
        requests = self.groups.get(group)
        entry = await requests.start_request(str(request_input.rid))
        entry["requests"] = requests
        return entry

    async def finish(self, entry: dict) -> dict:
        if entry.get("unrouted"):
            return {"readings": [], "dropped": 0, "incomplete": True}
        trace = await entry["requests"].finish_request(entry)
        trace["incomplete"] = bool(trace.get("incomplete")) or self.devices.is_partial
        return trace

    async def drop(self, entry: dict) -> None:
        if not entry.get("unrouted"):
            await entry["requests"].drop_request(entry)


def is_single_request(request_input: Any) -> bool:
    """A single prompt with n=1 (before SGLang normalizes it, `io_struct.py:510-582`): only those carry readings."""
    sampling = getattr(request_input, "sampling_params", None)
    if isinstance(sampling, list):
        return False
    if isinstance(sampling, Mapping) and int(sampling.get("n", 1) or 1) > 1:
        return False
    text, input_ids = getattr(request_input, "text", None), getattr(request_input, "input_ids", None)
    if text is not None:
        return isinstance(text, str)
    if isinstance(input_ids, list):
        return not input_ids or isinstance(input_ids[0], int)
    return False


def is_final(response: Any) -> bool:
    meta = response.get("meta_info") if isinstance(response, Mapping) else None
    return isinstance(meta, dict) and meta.get("finish_reason") is not None


def install_engine(module: Any) -> None:
    """`sglang.srt.managers.tokenizer_manager` as it loads."""
    manager = getattr(module, "TokenizerManager", None)
    original = getattr(manager, "generate_request", None)
    input_class = getattr(module, "GenerateReqInput", None)
    if not callable(original) or getattr(original, _MARK, False) or not isinstance(input_class, type):
        return
    is_timed = os.environ.get(TIMING_ENV, "").strip() == "1"
    if is_timed:
        _setup_timing_log()

    @functools.wraps(original)
    async def generate_request(self: Any, *args: Any, **kwargs: Any) -> AsyncIterator[Any]:
        request_input = args[0] if args else kwargs.get("obj")
        is_ours = isinstance(request_input, input_class) and _call_quietly("check", is_single_request, request_input)
        added = 0.0
        entry = None
        if is_ours:
            began = time.perf_counter()
            entry = await _call_quietly_async("start", _start, self, request_input)
            added += time.perf_counter() - began
        # aclosing: a client disconnect closes SGLang's own generator at once, so its abort path runs unchanged.
        async with aclosing(original(self, *args, **kwargs)) as inner:
            try:
                async for response in inner:
                    if entry is not None and is_final(response):
                        began = time.perf_counter()
                        trace = await _call_quietly_async("finish", self._probe_gpu.finish, entry)
                        entry = None
                        if trace is not None:
                            response["meta_info"][GPU_FIELD] = trace
                        added += time.perf_counter() - began
                        if is_timed:
                            _log_timing(request_input, added, trace)
                    yield response
            finally:
                if entry is not None:  # never finished (an error, a disconnect): forget it without waiting
                    await _call_quietly_async("drop", self._probe_gpu.drop, entry)

    setattr(generate_request, _MARK, True)
    manager.generate_request = generate_request


async def _start(manager: Any, request_input: Any) -> dict | None:
    gpu = getattr(manager, "_probe_gpu", None)
    if gpu is None:
        gpu = manager._probe_gpu = EngineGpu(read_engine_devices(manager.server_args))
    if getattr(request_input, "rid", None) is None:
        request_input.rid = uuid.uuid4().hex  # as SGLang would (`io_struct.py:595`); the sampler needs it first
    return await gpu.start(request_input)


def _setup_timing_log() -> None:
    timing_log.setLevel(logging.INFO)
    if not timing_log.hasHandlers():
        timing_log.addHandler(logging.StreamHandler())


def _log_timing(request_input: Any, added_s: float, trace: dict | None) -> None:
    """One line per finished request for the GPU run's overhead numbers (p50/p99 of `added_ms`)."""
    readings = len(trace.get("readings") or []) if isinstance(trace, Mapping) else 0
    incomplete = bool(trace.get("incomplete")) if isinstance(trace, Mapping) else True
    timing_log.info("probe-gpu-timing rid=%s added_ms=%.3f readings=%d incomplete=%s",
                    getattr(request_input, "rid", ""), added_s * 1000, readings, str(incomplete).lower())


def _call_quietly(what: str, call: Any, *args: Any) -> Any:
    try:
        return call(*args)
    except Exception:  # noqa: BLE001 -- fail open: the request runs as if Probe were absent
        _warn_once(what)
        return None


async def _call_quietly_async(what: str, call: Any, *args: Any) -> Any:
    try:
        return await call(*args)
    except Exception:  # noqa: BLE001 -- fail open: the request runs as if Probe were absent
        _warn_once(what)
        return None


def _warn_once(what: str) -> None:
    if what not in _warned:
        _warned.add(what)
        log.warning("Probe's GPU readings failed to %s a request; generation continues without them", what,
                    exc_info=True)
