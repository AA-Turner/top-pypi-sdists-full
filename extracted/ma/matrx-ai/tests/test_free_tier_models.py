"""The free-tier model ceiling: guests and free accounts never run a premium model.

Forcing tests for FREE-ALLOWANCE.md attack A1 (premium model through /ai/chat or /ai/manual by a
guest): the swap must happen at the ONE place every chat/media call resolves its model
(``UnifiedAIClient._execute_dispatch``), keyed on the request's tier — never on the client's
choice — and the paid-call seam must refuse a premium model that has no stand-in.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.providers import free_tier_models as ftm

ROWS: dict[str, SimpleNamespace] = {}


def _row(name: str, rating: int | None, *, guest: str | None = None, mid: str | None = None,
         premium: bool = False, metadata: dict[str, Any] | None = None) -> SimpleNamespace:
    row = SimpleNamespace(
        id=f"id-{name}", name=name, common_name=name.title(), cost_rating=rating,
        guest_fallback_id=f"id-{guest}" if guest else None,
        mid_fallback_id=f"id-{mid}" if mid else None,
        is_premium=premium, metadata=metadata or {},
    )
    ROWS[name] = row
    ROWS[row.id] = row
    return row


_row("haiku", 1)
_row("flash", 3)
_row("flash-lite", 1)
_row("sonnet", 5, guest="haiku", mid="haiku")
_row("opus", 4, guest="haiku", mid="sonnet", premium=True)
_row("opus-max", 6, guest="haiku", mid="sonnet")
_row("image-premium", 5)
_row("local-unrated", None)
_row("allowed-anyway", 5, metadata={"free_tier": "allow"})

GUEST = ftm.FreeTierPolicy(tier="guest", max_cost_rating=3, default_model="flash-lite")
FREE = ftm.FreeTierPolicy(tier="free", max_cost_rating=4, default_model="flash")


@pytest.fixture(autouse=True)
def _catalog(monkeypatch: pytest.MonkeyPatch):
    async def _load(name_or_id: str):
        return ROWS.get(name_or_id)

    monkeypatch.setattr(ftm, "_load", _load)
    ftm._told.clear()
    yield
    ftm.set_free_tier_policy_resolver(None)


class _Emitter:
    def __init__(self) -> None:
        self.infos: list[Any] = []

    async def send_info(self, payload: Any) -> None:
        self.infos.append(payload)


def _ctx(policy: ftm.FreeTierPolicy | None, **kw: Any) -> SimpleNamespace:
    ctx = SimpleNamespace(user_id="u-1", request_id=kw.get("request_id", "r-1"), emitter=_Emitter(),
                          policy=policy)
    ftm.set_free_tier_policy_resolver(lambda c: c.policy)
    return ctx


@pytest.mark.asyncio
async def test_guest_premium_swaps_to_its_guest_fallback():
    assert await ftm.free_tier_target("sonnet", GUEST) == ("haiku", "")


@pytest.mark.asyncio
async def test_free_account_fallback_above_ceiling_goes_to_the_default():
    # opus-max's mid fallback is sonnet (5) — still premium for free (4) → the default model.
    assert await ftm.free_tier_target("opus-max", FREE) == ("flash", "")


@pytest.mark.asyncio
async def test_premium_flag_counts_even_within_the_rating():
    assert await ftm.free_tier_target("opus", FREE) == ("flash", "")  # mid=sonnet is premium too
    assert await ftm.free_tier_target("opus", GUEST) == ("haiku", "")


@pytest.mark.asyncio
async def test_within_ceiling_and_overrides_run_as_asked():
    assert await ftm.free_tier_target("flash", GUEST) is None
    assert await ftm.free_tier_target("allowed-anyway", GUEST) is None


@pytest.mark.asyncio
async def test_unrated_chat_model_is_premium_but_unrated_media_is_not():
    assert await ftm.free_tier_target("local-unrated", GUEST) == ("flash-lite", "")
    assert await ftm.free_tier_target("local-unrated", GUEST, interaction="single") is None


@pytest.mark.asyncio
async def test_premium_media_model_with_no_stand_in_is_never_answered_by_a_chat_model():
    target = await ftm.free_tier_target("image-premium", GUEST, interaction="single")
    assert target is not None and target[0] == ""


@pytest.mark.asyncio
async def test_swap_rewrites_config_drops_the_offering_pin_and_says_so_once(monkeypatch):
    ctx = _ctx(GUEST)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    config = SimpleNamespace(model="sonnet", offering_id="off-1", runtime_offering_id=None, metadata={})
    profile = SimpleNamespace(model_name="sonnet", capabilities=SimpleNamespace(interaction="turn"))
    assert await ftm.swap_for_free_tier(config, profile) is True
    assert config.model == "haiku" and config.offering_id is None
    assert config.metadata["original_model"] == "sonnet"
    config2 = SimpleNamespace(model="sonnet", offering_id=None, runtime_offering_id=None, metadata={})
    assert await ftm.swap_for_free_tier(config2, profile) is True  # a later turn of the same request
    assert len(ctx.emitter.infos) == 1
    info = ctx.emitter.infos[0]
    assert info.code == ftm.MODEL_SWAPPED_INFO_CODE
    assert info.user_message == "Ran on Haiku. Sign up free for Sonnet."


@pytest.mark.asyncio
async def test_paid_person_is_never_swapped(monkeypatch):
    ctx = _ctx(None)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    config = SimpleNamespace(model="opus-max", metadata={})
    profile = SimpleNamespace(model_name="opus-max", capabilities=SimpleNamespace(interaction="turn"))
    assert await ftm.swap_for_free_tier(config, profile) is False
    assert config.model == "opus-max"


@pytest.mark.asyncio
async def test_seam_backstop_refuses_premium_without_stand_in(monkeypatch):
    ctx = _ctx(GUEST)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    profile = SimpleNamespace(model_name="image-premium", model_id="id-image-premium",
                              model_cost_rating=5, capabilities=SimpleNamespace(interaction="single"))
    with pytest.raises(ftm.FreeTierModelRefusedError) as err:
        await ftm.admit_free_tier_model(profile)
    assert err.value.is_caller_refusal and err.value.fix_action == "sign_up"
    ok = SimpleNamespace(model_name="haiku", model_id="id-haiku", model_cost_rating=1,
                         capabilities=SimpleNamespace(interaction="turn"))
    await ftm.admit_free_tier_model(ok)


@pytest.mark.asyncio
async def test_execute_dispatch_swaps_before_anything_runs(monkeypatch):
    """The class guard: the client's model (``ai_model_id`` on /ai/chat and /ai/manual) reaches
    ``_execute_dispatch`` unswapped; the dispatch must re-resolve onto the stand-in. Red before the
    swap was wired there (the profile was resolved once, on the client's model)."""
    import matrx_ai.catalog.resolve as resolve_mod
    from matrx_ai.providers.unified_client import UnifiedAIClient

    ctx = _ctx(GUEST)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    asked: list[str] = []

    class _Stop(Exception):
        pass

    async def _resolve(model: str, *_a: Any, **_k: Any):
        asked.append(model)
        if len(asked) > 1:
            raise _Stop
        return SimpleNamespace(model_name=model, model_cost_rating=ROWS[model].cost_rating,
                               capabilities=SimpleNamespace(interaction="turn"))

    monkeypatch.setattr(resolve_mod, "resolve_tts_call_profile", _resolve)
    config = SimpleNamespace(model="sonnet", offering_id=None, runtime_offering_id=None,
                             routing_offering_id=None, tts_quality=None, metadata={})
    request = SimpleNamespace(config=config, debug=False)
    client = UnifiedAIClient.__new__(UnifiedAIClient)
    with pytest.raises(_Stop):
        await client._execute_dispatch(request)  # type: ignore[arg-type]
    assert asked == ["sonnet", "haiku"]


@pytest.mark.asyncio
async def test_seam_backstop_admits_a_device_served_run(monkeypatch):
    """A run on the person's own computer (route_kind "device") costs 0.0 and spends nobody's
    money, so the free-tier ceiling never refuses it — whatever the model's cost rating."""
    ctx = _ctx(GUEST)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    premium = dict(model_name="image-premium", model_id="id-image-premium", model_cost_rating=5,
                   capabilities=SimpleNamespace(interaction="turn"))
    with pytest.raises(ftm.FreeTierModelRefusedError):  # the same model in the cloud is refused
        await ftm.admit_free_tier_model(SimpleNamespace(**premium))
    device = SimpleNamespace(**premium, route_kind="device", served_via=object())
    await ftm.admit_free_tier_model(device)
