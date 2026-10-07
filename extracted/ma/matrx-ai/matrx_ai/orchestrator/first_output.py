"""TIME TO FIRST TOKEN — the one stamp, taken where every model call passes.

Every model call of every run (chat, agent, mandate, batch, MCP agent service,
sub-agent) crosses ``send_once``. For the duration of that provider call this
module puts a thin watcher in front of the context's emitter — providers read
``get_app_context().emitter`` at call time, the same seam the verbalized
decision gate uses — and stamps ``ExecutionState.ttft_first_output_at`` the
first time the provider hands over model output:

* the first non-empty text delta (``send_chunk``) or reasoning delta
  (``send_reasoning_chunk``), whichever comes first;
* otherwise, when the call returns having streamed neither — a non-streaming
  provider, a reply that is only a tool call, or a run with no emitter at all —
  the moment that call's response arrived.

It is measured from the first iteration's ``TimingUsage.start_time`` — the
same origin and the same clock (``time.time()``) as ``total_duration`` — so
``ttft_ms`` can never exceed ``total_duration_ms``. It is persisted by the executor's finalize as ``chat.user_request.metadata.
ttft_ms`` and the completion event's ``timing_stats.first_token_seconds``.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any


class _FirstOutputWatcher:
    """Forwards everything to the real emitter; stamps the first model output."""

    def __init__(self, inner: Any, state: Any) -> None:
        object.__setattr__(self, "_inner", inner)
        object.__setattr__(self, "_state", state)

    def _stamp(self, text: str) -> None:
        if text and self._state.ttft_first_output_at is None:
            self._state.ttft_first_output_at = time.time()

    async def send_chunk(self, text: str) -> None:
        self._stamp(text)
        await self._inner.send_chunk(text)

    async def send_reasoning_chunk(self, text: str) -> None:
        self._stamp(text)
        await self._inner.send_reasoning_chunk(text)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)

    def __setattr__(self, name: str, value: Any) -> None:
        setattr(self._inner, name, value)


@contextmanager
def watching_first_output(state: Any) -> Iterator[None]:
    """Watch one provider call for this execution's first model output."""
    # Only an execution's own state carries the clock (``send_once`` is also
    # driven by probes and replays that pass other state objects).
    if not hasattr(state, "ttft_first_output_at") or state.ttft_first_output_at is not None:
        yield
        return
    from matrx_connect.context.app_context import set_app_context, try_get_app_context

    ctx = try_get_app_context()
    inner = getattr(ctx, "emitter", None) if ctx is not None else None
    watcher = _FirstOutputWatcher(inner, state) if inner is not None else None
    if watcher is not None:
        set_app_context(ctx.with_overrides(emitter=watcher))
    try:
        yield
    finally:
        if watcher is not None:
            current = try_get_app_context()
            if current is not None and current.emitter is watcher:
                set_app_context(current.with_overrides(emitter=inner))
    # Reached only when the call returned: it produced a response, so the
    # model's first output exists even if nothing streamed.
    if state.ttft_first_output_at is None:
        state.ttft_first_output_at = time.time()


def turn_ttft_ms(state: Any, timing_history: Any) -> int | None:
    """Milliseconds from the first iteration's start to the first model output.

    ``timing_history`` is the request's ``TimingUsage`` list — the origin
    ``total_duration`` is measured from. None when either end is missing.
    """
    first = getattr(state, "ttft_first_output_at", None) if state is not None else None
    starts = [t.start_time for t in timing_history or () if isinstance(t.start_time, float)]
    if not isinstance(first, float) or not starts:
        return None
    start = min(starts)
    if first < start:
        return None
    # Truncated, exactly as total_duration_ms is — so ttft_ms <= total_duration_ms.
    return int((first - start) * 1000)
