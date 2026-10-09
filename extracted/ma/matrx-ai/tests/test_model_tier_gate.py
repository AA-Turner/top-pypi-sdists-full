"""The top-tier model gate: a model rated 6 reaches the provider only for a person whose
top-tier access is on — on EVERY paid call, every origin, no fallback model.

SUT: ``UnifiedAIClient._dispatch_with_billing_net`` (the one seam every paid provider call
passes) and ``matrx_ai.providers.model_tier_gate``.

Doubles: the host resolver (a set of people who are on) and the provider dispatch (a coroutine
recording that money was spent).

Breaks named:
* a person who is off reaches a rated-6 model (money spent on the top tier);
* a person's own chat turn (origin human) is exempt — it must not be;
* a run admitted once is admitted again for a different, top-tier model (judged per call);
* a refusal is silent, retryable, or not the plain sentence;
* an unknown answer (memory not loaded) or a raising resolver admits the call;
* a model below the top tier is gated.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai.providers import model_tier_gate as gate
from matrx_ai.providers.unified_client import UnifiedAIClient

ON = "4cf62e4e-2679-484f-b652-034e697418df"
OFF = "0f0e0d0c-0b0a-4908-8706-050403020100"


def _profile(rating: int | None) -> SimpleNamespace:
    return SimpleNamespace(
        vendor="anthropic", model_name="claude-fable-5", model_id="m-fable", endpoint_id="anthropic-test",
        base_url=None, offering_metadata={}, model_cost_rating=rating,
    )


@pytest.fixture
def holders() -> set[str]:
    on: set[str] = {ON}
    gate.set_top_tier_access_resolver(lambda uid: uid in on)
    yield on
    gate.set_top_tier_access_resolver(None)


def _ctx(user_id: str, *, origin_class: str = "human", n: int = 1) -> AppContext:
    return AppContext(
        emitter=SilentEmitter(), user_id=user_id, auth_type="token", is_authenticated=True,
        request_id=f"00000000-0000-4000-8000-{n:012d}", origin_class=origin_class,
    )


async def _paid_call(ctx: AppContext, profile: SimpleNamespace, spent: list[str]) -> BaseException | None:
    token = set_app_context(ctx)
    try:

        async def _provider() -> str:
            spent.append(profile.model_name)
            return "ok"

        await UnifiedAIClient._dispatch_with_billing_net(_provider, profile=profile)
    except BaseException as exc:  # noqa: BLE001
        return exc
    finally:
        clear_app_context(token)
    return None


def test_a_person_who_is_off_is_refused_before_the_provider(holders: set[str]) -> None:
    spent: list[str] = []
    exc = asyncio.run(_paid_call(_ctx(OFF), _profile(6), spent))
    assert isinstance(exc, gate.TopTierModelRefusedError)
    assert spent == []
    assert str(exc).startswith("This model is limited to approved accounts")
    assert exc.is_caller_refusal is True
    assert exc.error_info.is_retryable is False


def test_a_person_who_is_on_runs(holders: set[str]) -> None:
    spent: list[str] = []
    assert asyncio.run(_paid_call(_ctx(ON), _profile(6), spent)) is None
    assert spent == ["claude-fable-5"]


@pytest.mark.parametrize("origin", ["human", "delegated_member", "scheduled", "workflow", "child_agent", "api"])
def test_no_origin_is_exempt(holders: set[str], origin: str) -> None:
    spent: list[str] = []
    exc = asyncio.run(_paid_call(_ctx(OFF, origin_class=origin), _profile(6), spent))
    assert isinstance(exc, gate.TopTierModelRefusedError)
    assert spent == []


def test_each_call_is_judged_on_its_own_model(holders: set[str]) -> None:
    spent: list[str] = []
    ctx = _ctx(OFF, n=7)
    assert asyncio.run(_paid_call(ctx, _profile(5), spent)) is None  # same request, cheaper model
    exc = asyncio.run(_paid_call(ctx, _profile(6), spent))  # same request, top tier
    assert isinstance(exc, gate.TopTierModelRefusedError)
    assert len(spent) == 1


def test_no_person_is_refused(holders: set[str]) -> None:
    spent: list[str] = []
    exc = asyncio.run(_paid_call(_ctx(""), _profile(6), spent))
    assert isinstance(exc, gate.TopTierModelRefusedError)
    assert spent == []


def test_unknown_or_raising_resolver_refuses() -> None:
    spent: list[str] = []
    gate.set_top_tier_access_resolver(lambda uid: None)
    try:
        assert isinstance(asyncio.run(_paid_call(_ctx(ON), _profile(6), spent)), gate.TopTierModelRefusedError)

        def _boom(uid: str) -> bool:
            raise RuntimeError("memory unreadable")

        gate.set_top_tier_access_resolver(_boom)
        assert isinstance(asyncio.run(_paid_call(_ctx(ON), _profile(6), spent)), gate.TopTierModelRefusedError)
    finally:
        gate.set_top_tier_access_resolver(None)
    assert spent == []


@pytest.mark.parametrize("rating", [None, 0, 3, 5])
def test_models_below_the_top_tier_are_never_gated(holders: set[str], rating: int | None) -> None:
    spent: list[str] = []
    assert asyncio.run(_paid_call(_ctx(OFF), _profile(rating), spent)) is None
    assert spent == ["claude-fable-5"]
