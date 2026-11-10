"""The `--custom-generate-function-path` door (W30 spike M1-M3), with no Miles commit: every generate function Miles'
`GenerateState` hands out runs inside `ProbeGenerate`, which names each try before its first model request, marks the
samples it returns, and runs a retried try again in its slot. `generate_and_rm` and `generate_and_rm_group` end each
try once Miles graded it. Wrapped as `inference_rollout_common` loads (`samples/wraps.py`)."""

from __future__ import annotations

import copy
import dataclasses
import functools
import logging
import os
import threading
from contextvars import ContextVar
from typing import Any

from .engines import CURRENT
from .live import LIVE, LiveRollouts
from .rollout import Rollout

log = logging.getLogger(__name__)

#: The tries one `generate_and_rm` call started (a retry adds its next try), so it can end them once graded.
STARTED: ContextVar[list[Rollout] | None] = ContextVar("probe_miles_started", default=None)
#: `PROBE_MILES_LIVE=0`: no live samples, no request ids, Miles' functions untouched.
OFF_VALUES = frozenset({"0", "false", "off", "no"})
_MARK = "__probe_wrapped__"
#: The upstream agent generate function (`agentic_tool_call.py:204`) and how a wrapper says it delegates there.
AGENT_MODULE = "miles.rollout.generate_hub.agentic_tool_call"
AGENT_FLAG = "reads_sample_agent_fields"


def is_live_on() -> bool:
    return os.environ.get("PROBE_MILES_LIVE", "").strip().lower() not in OFF_VALUES


class ProbeGenerate:
    """A Miles generate function (`async (GenerateFnInput) -> GenerateFnOutput`, `base_types.py:117-135`) whose tries
    are live samples. Miles reads attributes off it (`add_arguments`, `reads_sample_agent_fields`): they pass through."""

    def __init__(self, inner: Any, live: LiveRollouts) -> None:
        self.inner = inner
        self._live = live
        self.is_agent = bool(getattr(inner, AGENT_FLAG, False)) or getattr(inner, "__module__", "") == AGENT_MODULE
        self.can_abort = not self.is_agent and live.stamp.stamp(inner)
        live.record_generate(is_agent=self.is_agent, can_abort=self.can_abort)

    def __getattr__(self, name: str) -> Any:
        if name == "inner":
            raise AttributeError(name)
        return getattr(self.inner, name)

    async def __call__(self, input: Any) -> Any:
        sample = getattr(input, "sample", None)
        started = STARTED.get()
        try:
            # A retry runs again on the call's own sampling parameters (a generate function may change its copy).
            sampling = copy.deepcopy(input.sampling_params) if dataclasses.is_dataclass(input) else None
            rollout = self._live.start(sample, is_eval=bool(getattr(input, "evaluation", False)),
                                       is_agent=self.is_agent, can_abort=self.can_abort, can_retry=sampling is not None,
                                       args=getattr(input, "args", None))  # fmt: skip
        except Exception as exc:  # noqa: BLE001 -- fail open: this try runs unrecorded
            _warn_once("start", exc)
            rollout = None
        if rollout is None:
            return await self.inner(input)
        token = CURRENT.set(rollout)
        try:
            while True:
                if started is not None:
                    started.append(rollout)
                try:
                    output = await self.inner(input)
                except BaseException as exc:
                    _call_quietly(self._live.end_raised, rollout, exc)
                    raise
                outputs = output.samples if isinstance(output.samples, list) else [output.samples]
                retried = _call_quietly(self._live.finish_try, rollout, outputs, sample, input.args)
                if retried is None:
                    return output
                rollout = retried
                CURRENT.set(rollout)
                input = _replace_sampling(input, sampling)
        finally:
            CURRENT.reset(token)


def _replace_sampling(input: Any, sampling: Any) -> Any:
    """The next try's input: the same call with a fresh copy of its sampling parameters (else the same input)."""
    try:
        return dataclasses.replace(input, sampling_params=copy.deepcopy(sampling))
    except Exception as exc:  # noqa: BLE001 -- the retry still runs, on the input it had
        _warn_once("retry input", exc)
        return input


_wrapped: dict[int, tuple[Any, ProbeGenerate]] = {}
_wrapped_lock = threading.Lock()


def forget_wrapped() -> None:
    with _wrapped_lock:
        _wrapped.clear()


def wrap_generate(inner: Any, live: LiveRollouts = LIVE) -> Any:
    """``inner`` as a `ProbeGenerate`, once per function (Miles builds each path's function once)."""
    if inner is None or isinstance(inner, ProbeGenerate) or not is_live_on():
        return inner
    with _wrapped_lock:
        found = _wrapped.get(id(inner))
        if found is not None and found[0] is inner:
            return found[1]
    try:
        wrapped = ProbeGenerate(inner, live)
    except Exception as exc:  # noqa: BLE001 -- fail open: Miles' own function runs
        _warn_once("wrap", exc)
        return inner
    with _wrapped_lock:
        _wrapped[id(inner)] = (inner, wrapped)
    return wrapped


def wrap_rollout_common(module: Any, live: LiveRollouts = LIVE) -> None:
    """`miles.rollout.inference_rollout.inference_rollout_common`, once: `GenerateState`'s generate functions (the
    fork sets `generate_function` in `__init__`; upstream adds `generate_function_for`, `:56-64`), and the two calls
    that grade (`generate_and_rm` `:71-157`, `generate_and_rm_group` `:160-210`)."""
    if not is_live_on():
        return
    state = getattr(module, "GenerateState", None)
    _wrap_state_init(state)
    _wrap_function_for(state)
    original = getattr(module, "generate_and_rm", None)
    if callable(original) and not getattr(original, _MARK, False):
        module.generate_and_rm = _make_generate_and_rm(original, live)
    original = getattr(module, "generate_and_rm_group", None)
    if callable(original) and not getattr(original, _MARK, False):
        module.generate_and_rm_group = _make_generate_and_rm_group(original, live)


def _wrap_state_init(state: Any) -> None:
    original = getattr(state, "__init__", None)
    if not callable(original) or getattr(original, _MARK, False):
        return

    @functools.wraps(original)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        original(self, *args, **kwargs)
        self.generate_function = wrap_generate(getattr(self, "generate_function", None))

    setattr(__init__, _MARK, True)
    state.__init__ = __init__


def _wrap_function_for(state: Any) -> None:
    original = getattr(state, "generate_function_for", None)
    if not callable(original) or getattr(original, _MARK, False):
        return

    @functools.wraps(original)
    def generate_function_for(self, *args: Any, **kwargs: Any) -> Any:
        return wrap_generate(original(self, *args, **kwargs))

    setattr(generate_function_for, _MARK, True)
    state.generate_function_for = generate_function_for


def _make_generate_and_rm(original: Any, live: LiveRollouts) -> Any:
    @functools.wraps(original)
    async def generate_and_rm(state: Any, *args: Any, **kwargs: Any) -> Any:
        started: list[Rollout] = []
        token = STARTED.set(started)
        try:
            result = await original(state, *args, **kwargs)
        except BaseException as exc:
            _call_quietly(live.end_unscored, started, exc)
            raise
        finally:
            STARTED.reset(token)
        _call_quietly(live.end_scored, started, getattr(state, "args", None))
        return result

    setattr(generate_and_rm, _MARK, True)
    return generate_and_rm


def _make_generate_and_rm_group(original: Any, live: LiveRollouts) -> Any:
    @functools.wraps(original)
    async def generate_and_rm_group(state: Any, group: Any, *args: Any, **kwargs: Any) -> Any:
        result = await original(state, group, *args, **kwargs)
        _call_quietly(live.end_named, _flatten(result), getattr(state, "args", None))
        return result

    setattr(generate_and_rm_group, _MARK, True)
    return generate_and_rm_group


def _flatten(items: Any) -> list:
    found: list = []
    for item in items if isinstance(items, list) else [items]:
        found.extend(_flatten(item) if isinstance(item, list) else [item])
    return found


_warned: set[str] = set()


def _warn_once(what: str, error: BaseException) -> None:
    if what not in _warned:
        _warned.add(what)
        log.warning("Probe could not record a Miles sample's live %s; Miles continues: %s", what, error)


def _call_quietly(call: Any, *args: Any) -> Any:
    try:
        return call(*args)
    except Exception as exc:  # noqa: BLE001 -- fail open: Miles never sees a Probe error
        _warn_once(getattr(call, "__name__", "call"), exc)
        return None
