"""A run that has started is never refused midway for a limit or a tier (USAGE-GATE.md rule 5).

Incident (live 2026-11-16, chat.agent_run 7a1ca3ff): a free-plan person's podcast died at its audio
step after the script and six covers were paid for — the free-tier model ceiling's seam backstop
refused the voice model the platform itself picked, mid-run. Owner ruling: once a run starts it
finishes; a refusal can only happen BEFORE the run starts.

SUT: ``UnifiedAIClient._dispatch_with_billing_net`` (the one seam every paid provider call passes)
and the gates it calls. Each "never refused inside" test has its twin "a NEW run IS refused at its
start", so neither direction can rot silently.

Breaks named:
* the free-tier backstop refuses a premium model with no stand-in inside an admitted run;
* the seam reads admission AFTER the usage gate remembered the run, so a run's very first call
  (its start) is never refused at all;
* a resume leg in a fresh process (empty memo) is refused although it carries ``usage_admitted``;
* machine work (workflow / system origin) never records admission, so its later steps are judged
  as starts;
* the usage gate cuts off a run whose person crossed the line mid-run.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai.providers import free_tier_models as ftm
from matrx_ai.providers import usage_gate as gate
from matrx_ai.providers.unified_client import UnifiedAIClient

USER = "0f0e0d0c-0b0a-4908-8706-050403020100"
FREE = ftm.FreeTierPolicy(tier="free", max_cost_rating=4, default_model="cheap-chat")
_TTS = {"input": ["text"], "output": ["audio"], "interaction": "turn"}

ROWS: dict[str, SimpleNamespace] = {
    "cheap-chat": SimpleNamespace(
        id="id-cheap", name="cheap-chat", cost_rating=1, is_premium=False, metadata={},
        guest_fallback_id=None, mid_fallback_id=None, provider_id="p-1",
        capabilities={"input": ["text"], "output": ["text"], "interaction": "turn"},
    ),
    # A premium voice with NO in-ceiling stand-in anywhere (the incident's shape before the
    # automatic stand-in existed).
    "premium-voice": SimpleNamespace(
        id="id-voice", name="premium-voice", cost_rating=5, is_premium=True, metadata={},
        guest_fallback_id=None, mid_fallback_id=None, provider_id="p-1", capabilities=_TTS,
    ),
}


def _profile(name: str) -> SimpleNamespace:
    return SimpleNamespace(
        vendor="google", model_name=name, model_id=ROWS[name].id, endpoint_id="google-test",
        base_url=None, offering_metadata={}, model_cost_rating=ROWS[name].cost_rating,
        capabilities=SimpleNamespace(interaction="turn"),
    )


@pytest.fixture(autouse=True)
def _wiring(monkeypatch: pytest.MonkeyPatch):
    async def _load(name_or_id: str):
        return ROWS.get(name_or_id) or next((r for r in ROWS.values() if r.id == name_or_id), None)

    async def _all():
        return list(ROWS.values())

    monkeypatch.setattr(ftm, "_load", _load)
    monkeypatch.setattr(ftm, "_all_models", _all)
    ftm.set_free_tier_policy_resolver(lambda ctx: FREE)
    gate.reset_usage_gate_state()
    yield
    ftm.set_free_tier_policy_resolver(None)
    gate.set_usage_verdict_resolver(None)
    gate.reset_usage_gate_state()


def _rid(n: int) -> str:
    return f"00000000-0000-4000-8000-{n:012d}"


def _ctx(request_id: str, **kw: Any) -> AppContext:
    return AppContext(
        emitter=SilentEmitter(), user_id=USER, auth_type="token", is_authenticated=True,
        request_id=request_id, **kw,
    )


async def _paid_call(ctx: AppContext, model: str, spent: list[str]) -> BaseException | None:
    token = set_app_context(ctx)
    try:

        async def _provider() -> str:
            spent.append(model)
            return "ok"

        await UnifiedAIClient._dispatch_with_billing_net(_provider, profile=_profile(model))
    except BaseException as exc:  # noqa: BLE001
        return exc
    finally:
        clear_app_context(token)
    return None


# --- the free-tier model ceiling (unit) ------------------------------------------------------


def test_free_tier_backstop_never_refuses_inside_an_admitted_run() -> None:
    ctx = _ctx(_rid(1))
    token = set_app_context(ctx)
    try:
        asyncio.run(ftm.admit_free_tier_model(_profile("premium-voice"), in_admitted_run=True))
    finally:
        clear_app_context(token)
    assert ctx.metadata[ftm.MODEL_CEILING_KEY] == {
        "decision": "admitted_run", "model": "premium-voice", "tier": "free",
    }, "the run-as-asked decision must ride the call's chat.request row"


def test_free_tier_backstop_refuses_a_new_run_at_its_start() -> None:
    token = set_app_context(_ctx(_rid(2)))
    try:
        with pytest.raises(ftm.FreeTierModelRefusedError):
            asyncio.run(ftm.admit_free_tier_model(_profile("premium-voice"), in_admitted_run=False))
    finally:
        clear_app_context(token)


# --- the seam: admission is read before any gate remembers the run ---------------------------


def test_seam_a_later_step_of_a_started_run_is_never_refused() -> None:
    """The incident: the script (in-ceiling) was paid, then the audio step hit a premium model."""
    root = _rid(3)
    spent: list[str] = []
    assert asyncio.run(_paid_call(_ctx(root), "cheap-chat", spent)) is None  # the run starts
    step = _ctx(_rid(4), root_request_id=root)  # a stage / sub-agent of the same run
    refused = asyncio.run(_paid_call(step, "premium-voice", spent))
    assert refused is None, f"a started run was refused midway: {refused!r}"
    assert spent == ["cheap-chat", "premium-voice"]


def test_seam_a_new_run_over_the_ceiling_is_refused_at_its_start() -> None:
    spent: list[str] = []
    refused = asyncio.run(_paid_call(_ctx(_rid(5)), "premium-voice", spent))
    assert isinstance(refused, ftm.FreeTierModelRefusedError)
    assert spent == [], "the start of a run over the ceiling reached the provider"


def test_seam_a_resume_leg_in_a_fresh_process_keeps_its_admission() -> None:
    """A workflow resume leg / reaped agent-run resume lands on a process whose memo is empty;
    admission rides the context (``usage_admitted``), set by the code that resumes the run."""
    gate.reset_usage_gate_state()  # another ECS task, or after a release restart
    spent: list[str] = []
    resumed = _ctx(_rid(6), origin_class="workflow", usage_admitted=True)
    assert asyncio.run(_paid_call(resumed, "premium-voice", spent)) is None
    gate.reset_usage_gate_state()
    fresh = _ctx(_rid(7), origin_class="workflow")  # a start leg of a new run
    assert isinstance(asyncio.run(_paid_call(fresh, "premium-voice", spent)), ftm.FreeTierModelRefusedError)
    assert spent == ["premium-voice"]


def test_seam_machine_work_records_its_admission() -> None:
    """A workflow run is not a usage-gated person, but its later steps are still a started run."""
    root = _rid(8)
    spent: list[str] = []
    assert asyncio.run(_paid_call(_ctx(root, origin_class="workflow"), "cheap-chat", spent)) is None
    step = _ctx(_rid(9), root_request_id=root, origin_class="workflow")
    assert asyncio.run(_paid_call(step, "premium-voice", spent)) is None
    assert spent == ["cheap-chat", "premium-voice"]


# --- the usage limit -------------------------------------------------------------------------


def _over_and_enforced() -> None:
    usage = {"state": "over", "plan_key": "free", "binding_period": "week", "windows": []}
    verdict = gate.UsageVerdict(state="over", refuse=True, enforced=True, usage=usage)
    gate.set_usage_verdict_resolver(lambda user_id: verdict)


def test_usage_limit_never_refuses_a_run_that_crossed_it_midway() -> None:
    root = _rid(10)
    spent: list[str] = []
    assert asyncio.run(_paid_call(_ctx(root), "cheap-chat", spent)) is None
    _over_and_enforced()  # the person crosses the line during the run
    step = _ctx(_rid(11), root_request_id=root)
    assert asyncio.run(_paid_call(step, "cheap-chat", spent)) is None
    assert spent == ["cheap-chat", "cheap-chat"]


def test_usage_limit_refuses_a_new_run_at_its_start() -> None:
    _over_and_enforced()
    spent: list[str] = []
    assert isinstance(asyncio.run(_paid_call(_ctx(_rid(12)), "cheap-chat", spent)), gate.UsageLimitReachedError)
    assert spent == []
