"""Test fakes for the workflow runtime — no network, no VMs.

Shipped inside the package (not under ``tests/``) so world test suites can
import them too.
"""

from __future__ import annotations

import asyncio
import inspect
from collections.abc import Callable, Iterable
from typing import Any

from plato.workflows.backend import AgentCallOutcome, AgentCallRequest

#: A scripted entry: a ready outcome, an exception to raise, or a callable
#: receiving the request and returning either (may be async).
ScriptedOutcome = AgentCallOutcome | Exception | Callable[[AgentCallRequest], Any]


class FakeAgentBackend:
    """In-memory :class:`~plato.workflows.backend.AgentBackend`.

    ``outcomes`` are consumed FIFO, one per ``run_call``. Entries may be:

    * an :class:`AgentCallOutcome` — returned as-is;
    * an :class:`Exception` — raised;
    * a callable ``(request) -> AgentCallOutcome | Exception`` (sync or
      async) — invoked per call; a returned exception is raised.

    When the script is exhausted (or empty), a default ``ok`` outcome is
    synthesized: ``result_json={"call_id": ...}`` for schema calls,
    ``result_text="fake-result:<call_id>"`` otherwise.

    Records every request in ``.requests`` and tracks the concurrency
    high-water mark in ``.concurrency_high_water`` (set ``delay_s`` to give
    overlapping calls a chance to stack up).
    """

    def __init__(
        self,
        outcomes: Iterable[ScriptedOutcome] | None = None,
        *,
        delay_s: float = 0.0,
        salvage_ref_on_cancel: str | None = None,
    ) -> None:
        self.outcomes: list[ScriptedOutcome] = list(outcomes or [])
        self.delay_s = delay_s
        self.salvage_ref_on_cancel = salvage_ref_on_cancel
        self.requests: list[AgentCallRequest] = []
        self.concurrency_high_water = 0
        self._in_flight = 0
        self._cancelled_salvage_refs: dict[str, str] = {}

    def take_cancelled_salvage_ref(self, call_id: str) -> str | None:
        return self._cancelled_salvage_refs.pop(call_id, None)

    async def run_call(self, request: AgentCallRequest) -> AgentCallOutcome:
        self.requests.append(request)
        self._in_flight += 1
        self.concurrency_high_water = max(self.concurrency_high_water, self._in_flight)
        try:
            if self.delay_s > 0:
                try:
                    await asyncio.sleep(self.delay_s)
                except asyncio.CancelledError:
                    # Mirror WorldAgentBackend: a call cancelled in flight
                    # stashes its salvage ref for the runtime to collect.
                    if self.salvage_ref_on_cancel is not None:
                        self._cancelled_salvage_refs[request.call_id] = self.salvage_ref_on_cancel
                    raise
            if not self.outcomes:
                return self._default_outcome(request)
            scripted = self.outcomes.pop(0)
            if isinstance(scripted, AgentCallOutcome):
                return scripted
            if isinstance(scripted, Exception):
                raise scripted
            value = scripted(request)
            if inspect.isawaitable(value):
                value = await value
            if isinstance(value, Exception):
                raise value
            return value
        finally:
            self._in_flight -= 1

    @staticmethod
    def _default_outcome(request: AgentCallRequest) -> AgentCallOutcome:
        if request.opts.output_schema is not None:
            return AgentCallOutcome(status="ok", result_json={"call_id": request.call_id})
        return AgentCallOutcome(status="ok", result_text=f"fake-result:{request.call_id}")


class FakeCostSource:
    """A :class:`~plato.workflows.budget.CostSource` with a settable spend."""

    def __init__(self, spend_usd: float = 0.0) -> None:
        self.spend_usd = spend_usd
        self.refresh_count = 0

    def set_spend(self, spend_usd: float) -> None:
        self.spend_usd = spend_usd

    async def refresh(self) -> float:
        self.refresh_count += 1
        return self.spend_usd
