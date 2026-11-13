"""Sync GRPO's tool calls inside their own sample's rollout (RL sample capture, plan S0): TRL calls each completion's
tools from that completion's own dicts, rebuilt every call (`_sync_tool_dicts[i]`, `_async_tool_dicts[i]`,
`grpo_trainer.py:2480-2499`, called at `:2056-2093`), so each tool runs inside its sample's `RolloutCapture` and
`probe.samples.attach_file` from a tool reaches that sample. Line refs are `huggingface/trl@4ae4d34a86f3`."""

from __future__ import annotations

import functools
from collections.abc import Callable, Coroutine, MutableMapping, Sequence
from typing import Any

from probe.sdk.run.samples.rollout import RolloutCapture


class ToolRollouts:
    """One generation call's captures, by completion index (this process's rows only)."""

    def __init__(self) -> None:
        self._captures: dict[int, RolloutCapture] = {}
        #: Each completion's async tool calls in TRL's call order, True for one that raised when called (bad
        #: arguments): TRL files its result with the sync and failed ones, before the gathered ones (`:2068-2078`).
        self._async_calls: dict[int, list[bool]] = {}

    def reset(self) -> None:
        """Forget the last batch: until `start` runs, every row reads as not watched, so its links are refused."""
        self._captures, self._async_calls = {}, {}

    def start(self, trainer: Any, run: Any, keys: Sequence[str]) -> None:
        """Wrap completion ``i``'s tools to run inside the capture of sample ``keys[i]`` and note which async calls
        raise when called. With no run (another rank, or no open run) only the async tools are wrapped, to note those
        failures, as every row's result links need them. Earlier captures this call never exported are dropped."""
        self.reset()
        sync_dicts = getattr(trainer, "_sync_tool_dicts", None) or []
        async_dicts = getattr(trainer, "_async_tool_dicts", None) or []
        for index, key in enumerate(keys):
            if index >= max(len(sync_dicts), len(async_dicts)):
                break
            capture = None
            if run is not None:
                capture = self._captures[index] = RolloutCapture(run, key)
                _wrap_each(sync_dicts, index, lambda tool, capture=capture: _wrap_sync(tool, capture))
            calls = self._async_calls[index] = []
            _wrap_each(async_dicts, index, lambda tool, capture=capture, calls=calls: _wrap_async(tool, capture, calls))

    def get_failed_async_calls(self, index: int) -> list[int] | None:
        """Positions, among completion ``index``'s async tool calls in call order, of those that raised when called;
        None when its calls were not watched (its result links then refuse any reply with an async call)."""
        calls = self._async_calls.get(index)
        return None if calls is None else [position for position, is_failed in enumerate(calls) if is_failed]

    def finish(self, index: int) -> dict | None:
        """Completion ``index``'s capture exported (`RolloutCapture.export`: files and span), or None when it had
        none. Waits for its uploads."""
        capture = self._captures.pop(index, None)
        return None if capture is None else capture.export()


def _wrap_each(dicts: Sequence[Any], index: int, wrap: Callable[[Callable[..., Any]], Callable[..., Any]]) -> None:
    tools = dicts[index] if index < len(dicts) else None
    if isinstance(tools, MutableMapping):
        for name, tool in list(tools.items()):
            if callable(tool):
                tools[name] = wrap(tool)


def _wrap_sync(tool: Callable[..., Any], capture: RolloutCapture) -> Callable[..., Any]:
    """A sync tool runs on the trainer's thread, one call at a time (`:2063`): inside its rollout's capture."""

    @functools.wraps(tool)
    def call_tool(*args: Any, **kwargs: Any) -> Any:
        with capture:
            return tool(*args, **kwargs)

    return call_tool


def _wrap_async(tool: Callable[..., Any], capture: RolloutCapture | None, calls: list[bool]) -> Callable[..., Any]:
    """An async tool: TRL calls it for a coroutine (bad arguments fail right there, in TRL's own result order) and
    gathers a completion's coroutines (`:2072,2085-2088`). The wrapper stays sync, so the call is TRL's own; the
    coroutine runs inside its rollout's capture (when there is one), which each gathered task enters for itself
    (PR1b). ``calls`` notes whether each call raised, for the result links (`rows.link_tool_results`)."""

    @functools.wraps(tool)
    def call_tool(*args: Any, **kwargs: Any) -> Any:
        try:
            coroutine = tool(*args, **kwargs)
        except BaseException:
            calls.append(True)
            raise
        calls.append(False)
        return coroutine if capture is None else _await_inside(coroutine, capture)

    return call_tool


async def _await_inside(coroutine: Coroutine[Any, Any, Any], capture: RolloutCapture) -> Any:
    with capture:
        return await coroutine
