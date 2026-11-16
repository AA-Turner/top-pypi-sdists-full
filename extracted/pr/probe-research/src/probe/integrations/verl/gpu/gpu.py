"""Return actual serving-device observations with the request output; the trainer binds the final sample key."""

import functools
import contextvars
import inspect
import os
import logging
from contextlib import contextmanager
from collections.abc import Mapping, MutableMapping

from probe.sdk.hardware.requests import GpuRequestGroups
from probe.sdk.run.samples.points import watch_import

from ..wrapping import guard, guard_async, is_wrapped, make_install, set_wrapped

GPU_FIELD = "probe_gpu_observations"
CONTEXT_FIELD = "_probe_gpu_context"
logger = logging.getLogger(__name__)


class GpuCapture:
    _current = contextvars.ContextVar("probe_verl_gpu_capture", default=None)

    def __init__(self, context, recording) -> None:
        self.context = context
        self.recording = recording

    @contextmanager
    def enter(self):
        token = self._current.set(self)
        try:
            yield
        finally:
            self._current.reset(token)

    def record_output(self, output) -> None:
        extra = getattr(output, "extra_fields", None)
        trace = extra.pop(GPU_FIELD, None) if isinstance(extra, MutableMapping) else None
        if isinstance(trace, Mapping) and trace.get("context") == self.context and self.recording is not None:
            self.recording.record_gpu_trace(trace)


def wrap_gpu_client(cls: type) -> bool:
    original = cls.__dict__.get("generate")
    if not callable(original) or is_wrapped(original):
        return False

    @functools.wraps(original)
    async def generate(self, *args, **kwargs):
        capture = GpuCapture._current.get()
        output = await original(self, *args, **kwargs)
        if capture is not None:
            # Consume each partial response before FullyAsyncLLMServerClient rebuilds its output.
            guard(capture.record_output, output)
        return output

    set_wrapped(cls, "generate", generate)
    return True


def get_request_devices(server, arguments) -> str | None:
    """Only the TP group the server explicitly routes to; never every DP group's GPU."""
    visible = os.environ.get("CUDA_VISIBLE_DEVICES")
    config = getattr(server, "config", None)
    parallel = getattr(config, "data_parallel_size", 1)
    if parallel <= 1:
        return visible
    rank_for_session = getattr(server, "_dp_rank_for_session", None)
    rank = rank_for_session(arguments.get("session_id")) if callable(rank_for_session) else None
    width = int(getattr(config, "tensor_model_parallel_size", 1))
    devices = visible.split(",") if visible else []
    if rank is None or len(devices) != parallel * width:
        raise ValueError("The serving worker did not identify this request's local GPU group")
    return ",".join(devices[rank * width:(rank + 1) * width])


def wrap_gpu_server(cls: type) -> bool:
    original = cls.__dict__.get("generate")
    if not callable(original) or is_wrapped(original):
        return False
    signature = inspect.signature(original)

    @functools.wraps(original)
    async def generate(self, *args, **kwargs):
        context = kwargs.pop(CONTEXT_FIELD, None)
        if context is None:
            return await original(self, *args, **kwargs)
        bound = signature.bind(self, *args, **kwargs)
        request_id = str(bound.arguments.get("request_id", ""))
        monitor = getattr(self, "_probe_gpu_requests", None)
        if monitor is None:
            try:
                devices = get_request_devices(self, bound.arguments)
            except ValueError as exc:
                logger.warning("Probe omitted GPU observations with unknown request routing: %s", exc)
                return await original(self, *args, **kwargs)
            groups = getattr(self, "_probe_gpu_monitors", None)
            if groups is None:
                groups = self._probe_gpu_monitors = GpuRequestGroups()
            monitor = groups.get(devices)
        entry = await guard_async(monitor.start_request, request_id)
        trace = None
        try:
            output = await original(self, *args, **kwargs)
        finally:
            if entry is not None:
                trace = await guard_async(monitor.finish_request, entry)
        if trace is not None and isinstance(getattr(output, "extra_fields", None), dict):
            output.extra_fields[GPU_FIELD] = {**trace, "context": context}
        return output

    # Ray validates RPC arguments against the exposed signature before calling the wrapper.
    parameters = list(signature.parameters.values())
    extra = inspect.Parameter(CONTEXT_FIELD, inspect.Parameter.KEYWORD_ONLY, default=None)
    position = next((index for index, parameter in enumerate(parameters)
                     if parameter.kind == inspect.Parameter.VAR_KEYWORD), len(parameters))
    parameters.insert(position, extra)
    generate.__signature__ = signature.replace(parameters=parameters)
    set_wrapped(cls, "generate", generate)
    return True


def watch_gpu_imports() -> None:
    # One registry, one install path. Other serving engines are never guessed to be vLLM.
    for module, name in (("verl.workers.rollout.vllm_rollout.vllm_async_server", "vLLMHttpServer"),):
        watch_import(module, make_install(name, wrap_gpu_server), framework="verl")
    watch_import("verl.workers.rollout.llm_server", make_install("LLMServerClient", wrap_gpu_client), framework="verl")
