"""A REAL call never builds a replay key, and a key that cannot be built never fails a run (L-REPLAY3, urgent).

Red before: ``mandate_action._mandate_start_body`` built ``request_fingerprint(request)`` on every call, before
the host said whether it was replaying; a request the key could not read (``vars()`` on a str) raised out of
the step and failed a real user's run."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from matrx_ai import mandate_taps
from matrx_ai.mandate_taps import ReplayKey, record_answer, replay_answer


class _Host:
    def __init__(self, active: bool) -> None:
        self.is_active = active
        self.lookups: list[dict[str, Any]] = []
        self.stores: list[dict[str, Any]] = []

    async def active(self, _run_id: str | None) -> bool:
        return self.is_active

    async def lookup(self, _door: str, _key: str, _run: str | None, fingerprint: dict[str, Any]) -> Any:
        self.lookups.append(fingerprint)
        return None

    async def store(self, _door: str, _key: str, _run: str | None, fingerprint: dict[str, Any], _r: Any) -> None:
        self.stores.append(fingerprint)


@pytest.fixture()
def host():
    def install(active: bool) -> _Host:
        h = _Host(active)
        mandate_taps.set_mandate_replay(h)
        return h

    yield install
    mandate_taps.set_mandate_replay(None)


def _broken() -> dict[str, Any]:
    raise TypeError("vars() argument must have __dict__ attribute")


def test_a_real_call_never_builds_the_key(host) -> None:
    built: list[int] = []
    h = host(False)
    key = ReplayKey(lambda: built.append(1) or {"k": 1})
    assert asyncio.run(replay_answer("m", None, key)) is None
    asyncio.run(record_answer("m", None, key, {"final_text": "x"}))
    assert built == [] and h.lookups == [] and h.stores == []


def test_a_key_that_raises_is_a_real_unrecorded_call(host) -> None:
    h = host(True)
    key = ReplayKey(_broken, label="m")
    assert asyncio.run(replay_answer("m", None, key)) is None
    asyncio.run(record_answer("m", None, key, {"final_text": "x"}))
    assert h.lookups == [] and h.stores == []


def test_in_a_session_the_key_is_built_once(host) -> None:
    built: list[int] = []
    h = host(True)
    key = ReplayKey(lambda: built.append(1) or {"k": 1})
    asyncio.run(replay_answer("m", None, key))
    asyncio.run(record_answer("m", None, key, {"final_text": "x"}))
    assert built == [1] and h.lookups == [{"k": 1}] and h.stores == [{"k": 1}]


def test_the_run_mandate_step_runs_when_its_key_cannot_be_built(host, monkeypatch: pytest.MonkeyPatch) -> None:
    """Through the real step body: the request is one the key cannot read, the host is NOT replaying, and the
    step still reaches the real agent run. Then with the host replaying: still runs (a miss, loudly logged)."""
    from types import SimpleNamespace

    from matrx_ai.graph_nodes import mandate_action as ma
    from matrx_ai.graph_nodes.agent_action import StepAgent
    from matrx_ai.graph_nodes.shared import AiExecutionResult

    ran: list[str] = []

    async def resolve(*_a: Any, **_k: Any) -> StepAgent:
        return StepAgent(agent_id="agent-1", is_version=False, config_overrides=None, declared_output_kind=None)

    async def limit(_ctx: Any, _v: Any) -> Any:
        return SimpleNamespace(value=5, name_on=lambda r: r)

    async def walled(*_a: Any, **_k: Any) -> Any:
        ran.append("real")
        return AiExecutionResult(conversation_id="c", request_id="r", iterations=1, final_text="live"), None

    async def bind(inputs: Any, _resolved: Any) -> Any:
        return inputs

    monkeypatch.setattr(ma, "resolve_step_agent_full", resolve)
    monkeypatch.setattr(ma, "resolve_step_iteration_limit", limit)
    monkeypatch.setattr(ma, "_bind_provision_values", bind)
    monkeypatch.setattr(ma, "build_agent_request", lambda *a, **k: "a request the key cannot read")
    monkeypatch.setattr(ma, "run_walled_step_agent", walled)
    ctx = SimpleNamespace(node_id="ask", run_id="run-1", organization_id="org")
    inputs = ma.MandateStartInput.model_validate({"mandate_key": "x.job"})
    for active in (False, True):
        h = host(active)
        out = asyncio.run(ma._mandate_start_body(ctx, inputs, None))
        assert out.result.final_text == "live"
        assert h.lookups == [] and h.stores == []
    assert ran == ["real", "real"]
