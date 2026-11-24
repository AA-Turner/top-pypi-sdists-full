"""The Observer / Reflector provider call is banked on a ledger, exactly once (P8-RUNS, 2026-11-17).

``MemoryLLMAdapter._invoke`` sends through ``UnifiedAIClient.execute`` and BYPASSES the engine loop, so the engine's
per-call spine meter never saw it: its cost lived only in ``cx_observational_memory_event`` (a record, not a ledger).
It now takes the engine's one-shot path: open a ROOT ledger when no run is open (the host's tracker declines inside
one), meter the usage live onto the run that owns the call, settle the root with the same usage.

The host doubles below keep the host's contract (``aidream/services/runtime/loop_control.spine_call_meter`` and
``internal_agent_runs.track_internal_agent_run``): the live meter books a call onto the ambient run; a root's settle
books only the calls that did not land live. A ledger that holds a call twice, or none, fails.

Breaks named:
* the memory call reaches no ledger (the meter is never called, the root never settled);
* a call is banked twice (live AND on the settle);
* a failed call that the provider billed is lost.

Real code: ``MemoryLLMAdapter`` -> the real mandate preparation (inline Holder), the engine's real one-shot helpers.
Doubles: the client (returns a usage), the host's tracker and spine meter, the event writers.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai import _ext
from matrx_ai.code_call_mandate_keys import MEMORY_OBSERVER_MANDATE
from matrx_ai.memory import llm_adapter
from matrx_ai.providers.errors import attach_billed_usage
from matrx_ai.testing.holders import install_inline_holders


class _Usage(SimpleNamespace):
    def calculate_cost(self) -> float:
        return 0.25


class _Host:
    """The host's ledger: a live meter that books onto the ambient run, a root settle that books what did not land."""

    def __init__(self, *, inside_run: bool) -> None:
        self.inside_run = inside_run
        self.ledger: list[tuple[str, int]] = []  # (where, id(usage))
        self.settles: list[str] = []
        self.root_open = False

    def meter(self, usage: Any) -> None:
        if self.inside_run:
            self.ledger.append(("run", id(usage)))
        elif self.root_open:
            self.ledger.append(("root", id(usage)))

    async def tracker(self, *, label: str, source_feature: str, standalone_only: bool = False):
        assert standalone_only, "a one-shot call must ask for a root only when no run is open"
        if self.inside_run:
            return None
        self.root_open = True
        host = self

        async def settle(status: str, *, error: str | None = None, usage_history: list[Any] | None = None) -> None:
            host.settles.append(status)
            landed = {u for _, u in host.ledger}
            for usage in usage_history or []:
                if id(usage) not in landed:
                    host.ledger.append(("root", id(usage)))

        settle.accepts_usage_history = True  # type: ignore[attr-defined]
        return settle


def _wire(monkeypatch: pytest.MonkeyPatch, host: _Host, outcome: Any) -> None:
    install_inline_holders(
        monkeypatch,
        {MEMORY_OBSERVER_MANDATE: {"model": "holder-model", "messages": [
            {"role": "system", "content": "HOLDER"}, {"role": "user", "content": "HOLDER TURN"}]}},
    )

    class _Client:
        async def execute(self, request, *, transient_retries: int = 0):
            if isinstance(outcome, BaseException):
                raise outcome
            return outcome

    async def _nothing(**_kw):
        return None

    monkeypatch.setitem(_ext._registry, _ext._SPINE_CALL_METER_KEY, host.meter)
    monkeypatch.setitem(_ext._registry, _ext._INTERNAL_RUN_TRACKER_KEY, host.tracker)
    monkeypatch.setattr(llm_adapter, "_get_client", lambda: _Client())
    monkeypatch.setattr(llm_adapter, "_write_event", _nothing)
    monkeypatch.setattr(llm_adapter, "_emit_event", _nothing)


async def _observe() -> str:
    adapter = llm_adapter.MemoryLLMAdapter(ctx=SimpleNamespace(metadata={}), conversation_id="c")
    try:
        return await adapter(mandate_key=MEMORY_OBSERVER_MANDATE, messages=[], variables={"m": "x"})
    finally:
        for _ in range(10):
            await asyncio.sleep(0)


def _ok(usage: _Usage) -> Any:
    return SimpleNamespace(
        messages=[SimpleNamespace(role="assistant", content=[SimpleNamespace(text="observed")])], usage=usage
    )


@pytest.mark.parametrize("inside_run", [True, False], ids=["inside_a_run", "outside_any_run"])
async def test_the_memory_call_is_banked_exactly_once(monkeypatch, inside_run: bool) -> None:
    host = _Host(inside_run=inside_run)
    usage = _Usage(input_tokens=10, output_tokens=5, cached_input_tokens=0)
    _wire(monkeypatch, host, _ok(usage))
    assert await _observe() == "observed"
    assert host.ledger == [("run" if inside_run else "root", id(usage))]
    assert host.settles == ([] if inside_run else ["completed"])


async def test_a_billed_failure_is_banked_once_and_the_root_settles_failed(monkeypatch) -> None:
    host = _Host(inside_run=False)
    usage = _Usage(input_tokens=10, output_tokens=0, cached_input_tokens=0)
    exc = RuntimeError("provider failed after billing")
    attach_billed_usage(exc, usage)
    _wire(monkeypatch, host, exc)
    with pytest.raises(RuntimeError):
        await _observe()
    assert host.ledger == [("root", id(usage))]
    assert host.settles == ["failed"]


# --- the shared meter every direct caller uses (memory, media transcription, the ai.transcribe node) -------------


@pytest.mark.parametrize("inside_run", [True, False], ids=["inside_a_run", "outside_any_run"])
async def test_metered_one_shot_banks_each_usage_once(monkeypatch, inside_run: bool) -> None:
    from matrx_ai.orchestrator.executor import metered_one_shot

    host = _Host(inside_run=inside_run)
    monkeypatch.setitem(_ext._registry, _ext._SPINE_CALL_METER_KEY, host.meter)
    monkeypatch.setitem(_ext._registry, _ext._INTERNAL_RUN_TRACKER_KEY, host.tracker)
    first, second = _Usage(input_tokens=1), _Usage(input_tokens=2)
    async with metered_one_shot(None, feature="audio_transcription", label="t") as billed:
        billed.extend([first, second])
    where = "run" if inside_run else "root"
    assert host.ledger == [(where, id(first)), (where, id(second))]
    assert host.settles == ([] if inside_run else ["completed"])


async def test_metered_one_shot_banks_a_billed_failure_once_and_reraises(monkeypatch) -> None:
    from matrx_ai.orchestrator.executor import metered_one_shot

    host = _Host(inside_run=False)
    monkeypatch.setitem(_ext._registry, _ext._SPINE_CALL_METER_KEY, host.meter)
    monkeypatch.setitem(_ext._registry, _ext._INTERNAL_RUN_TRACKER_KEY, host.tracker)
    usage = _Usage(input_tokens=3)
    exc = RuntimeError("billed, then failed")
    attach_billed_usage(exc, usage)
    with pytest.raises(RuntimeError):
        async with metered_one_shot(None, feature="ai.transcribe", label="t"):
            raise exc
    assert host.ledger == [("root", id(usage))]
    assert host.settles == ["failed"]
