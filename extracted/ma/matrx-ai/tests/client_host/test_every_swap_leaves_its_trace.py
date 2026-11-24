"""EVERY STAND-IN LEAVES ITS TRACE ON THE REQUEST ROW (CGU-10 AND-IMG12 #3, 2026-11-11).

Live (AND-V IMG11): a guest picked Opus, Haiku answered, the chat kept Opus — and ``chat.request.metadata``
held no ``original_model`` and no reason; only the stream's ``model_swapped`` notice said it happened.
Every stand-in runs through ONE door (``UnifiedConfig.model_this_turn_only``), which now takes the reason
and keeps a turn-only trace; the provider seam stamps it on the call's usage and the request row carries it.

Through the REAL executor (the in-repo mock provider, no network), one test per kind: the dispatch
gates (free tier, HIPAA), the overload reroute (a fallback model; a billing refusal), and a host's early
hop before the run (aidream's auth-tier and minor-safety swaps call ``swap_model_this_turn_only``). What
each is FOR: drop the stamp in ``_stamp_offering_usage`` or the lift in ``CompletedRequest.to_storage_dict``
→ all red; a gate that stops naming its reason → its own test red. A turn with no swap carries nothing.
"""

from __future__ import annotations

from typing import Any

import pytest

pytestmark = pytest.mark.usefixtures("client_host_sandbox")

from test_a_turn_only_change_is_never_stored import (  # noqa: E402
    FALLBACK,
    _configure,
    _persons_config,
    _pin_resolves_as_the_models_own_route,  # noqa: F401 — fixture
    _scripted_model,
    execute_ai_request_quiet,
)
from test_the_iteration_ceiling_ends_with_an_answer import _set_context, probe_tool  # noqa: E402,F401


def _rows(completed: Any) -> list[dict[str, Any]]:
    return completed.to_storage_dict()["requests"]


def _assert_traced(completed: Any, reason: str) -> None:
    rows = _rows(completed)
    assert rows, "the run stored no request row"
    meta = rows[-1].get("metadata") or {}
    assert meta.get("original_model") == "mock-model", f"no original model on the row: {meta}"
    assert meta.get("model_swap_reason") == reason, f"wrong or missing swap reason on the row: {meta}"
    assert meta.get("model_swaps") and meta["model_swaps"][-1]["to"] == FALLBACK, meta
    # The trace is the turn's, never the chat's: the stored config carries none of it.
    stored = completed.request.config.to_storage_dict()
    assert "model_swaps_this_turn" not in (stored.get("config") or {}), "the swap trace was stored with the chat"


@pytest.mark.asyncio
async def test_a_turn_with_no_swap_carries_no_trace(monkeypatch, probe_tool, _pin_resolves_as_the_models_own_route) -> None:  # noqa: F811
    _configure()
    _set_context(sub_agent=False)
    _scripted_model(monkeypatch, [])
    completed = await execute_ai_request_quiet(_persons_config())
    for row in _rows(completed):
        assert "original_model" not in (row.get("metadata") or {}), row


@pytest.mark.asyncio
async def test_a_free_tier_swap_is_traced(monkeypatch, probe_tool, _pin_resolves_as_the_models_own_route) -> None:  # noqa: F811
    from matrx_ai.providers import free_tier_models as ftm

    _configure()
    _set_context(sub_agent=False)
    seen = _scripted_model(monkeypatch, [])
    monkeypatch.setattr(ftm, "_resolver", lambda ctx: ftm.FreeTierPolicy(tier="guest", max_cost_rating=2))

    async def _target(original: str, policy: Any, **_kw: Any) -> Any:
        return (FALLBACK, "") if original == "mock-model" else None

    async def _quiet(*_a: Any, **_k: Any) -> None:
        return None

    monkeypatch.setattr(ftm, "free_tier_target", _target)
    monkeypatch.setattr(ftm, "tell_model_swapped", _quiet)
    monkeypatch.setattr(ftm, "admit_free_tier_model", _quiet)

    completed = await execute_ai_request_quiet(_persons_config())
    assert seen and seen[0][0] == FALLBACK
    _assert_traced(completed, "free_tier")


@pytest.mark.asyncio
async def test_a_host_ceiling_decision_that_is_not_a_swap_rides_the_row(monkeypatch, probe_tool, _pin_resolves_as_the_models_own_route) -> None:  # noqa: F811
    """A host that EXEMPTS a person (aidream: an exempt account class) or could not resolve the tier records the
    decision on the request context; the person's model runs and the request row says why (``model_ceiling``)."""
    from matrx_ai.providers import free_tier_models as ftm

    _configure()
    _set_context(sub_agent=False)
    seen = _scripted_model(monkeypatch, [])
    decision = {"decision": "exempt", "account_class": "friends_family", "tier": "free"}

    def _exempting(ctx: Any) -> None:
        ctx.metadata["model_ceiling"] = decision  # ftm.MODEL_CEILING_KEY: the row contract's key
        return None

    monkeypatch.setattr(ftm, "_resolver", _exempting)
    completed = await execute_ai_request_quiet(_persons_config())
    assert seen and seen[0][0] == "mock-model", "an exempt person's own model must run"
    meta = _rows(completed)[-1].get("metadata") or {}
    assert meta.get("model_ceiling") == decision, f"the exemption is not on the request row: {meta}"
    assert "original_model" not in meta, meta


@pytest.mark.asyncio
async def test_a_hipaa_swap_is_traced(monkeypatch, probe_tool, _pin_resolves_as_the_models_own_route) -> None:  # noqa: F811
    from types import SimpleNamespace

    from matrx_ai.providers import baa_gate

    _configure()
    _set_context(sub_agent=False)
    seen = _scripted_model(monkeypatch, [])
    policy = SimpleNamespace(covers=lambda vendor, interaction: False, chat_standin_model=FALLBACK)

    async def _policy(*_a: Any, **_k: Any) -> Any:
        return policy

    async def _quiet(*_a: Any, **_k: Any) -> Any:
        return []

    monkeypatch.setattr(baa_gate, "baa_policy", _policy)
    monkeypatch.setattr(baa_gate, "baa_interaction", lambda profile: "chat")
    for name in ("_refuse_above_free_tier", "_tell_once", "admit_baa", "apply_baa_features", "_label"):
        monkeypatch.setattr(baa_gate, name, _quiet)

    completed = await execute_ai_request_quiet(_persons_config())
    assert seen and seen[0][0] == FALLBACK
    _assert_traced(completed, "hipaa")


@pytest.mark.asyncio
@pytest.mark.parametrize("reason", ["minor_safety", "free_tier"])
async def test_a_hosts_early_hop_is_traced(monkeypatch, probe_tool, _pin_resolves_as_the_models_own_route, reason: str) -> None:  # noqa: F811
    """aidream's minor-safety and auth-tier hops swap the config before the run, through the same door."""
    from matrx_ai.config.unified_config import swap_model_this_turn_only

    _configure()
    _set_context(sub_agent=False)
    seen = _scripted_model(monkeypatch, [])
    config = _persons_config()
    swap_model_this_turn_only(config, FALLBACK, swap_reason=reason)
    completed = await execute_ai_request_quiet(config)
    assert seen and seen[0][0] == FALLBACK
    _assert_traced(completed, reason)


@pytest.mark.asyncio
@pytest.mark.parametrize(("error_type", "reason"), [("provider_overloaded", "overload"), ("billing_error", "billing")])
async def test_an_overload_reroute_is_traced(monkeypatch, error_type: str, reason: str) -> None:
    from test_the_iteration_ceiling_ends_with_an_answer import _config

    from matrx_ai.catalog import resolve as catalog_resolve
    from matrx_ai.orchestrator import executor as executor_mod
    from matrx_ai.orchestrator import overload_reroute
    from matrx_ai.orchestrator.overload_reroute import OverloadPolicy, RerouteDecision, RerouteNote
    from matrx_ai.providers.errors import RetryableError
    from matrx_ai.providers.mock.mock_api import MockChat

    _configure()
    _set_context(sub_agent=False)
    sent: list[str] = []
    original_raw_spec = MockChat._raw_spec

    def _raw_spec(unified_config: Any) -> dict[str, Any]:
        raw = dict(original_raw_spec(unified_config) or {})
        sent.append(str(unified_config.model))
        raw["tool_calls"] = []
        if len(sent) == 1:
            raw["fail"] = True
            raw["error_message"] = "overloaded_error: the provider is overloaded"
        return raw

    monkeypatch.setattr(MockChat, "_raw_spec", staticmethod(_raw_spec))
    monkeypatch.setattr(
        executor_mod,
        "classify_provider_error",
        lambda _p, exc: RetryableError(error_type=error_type, message=str(exc), status_code=529, is_retryable=True),
    )

    async def _policy(*_a: Any, **_k: Any) -> OverloadPolicy:
        return OverloadPolicy(retry_max_attempts=0, fallback_ref=FALLBACK)

    async def _no_ladder(*_a: Any, **_k: Any) -> None:
        return None

    def _decide(**kw: Any) -> RerouteDecision:
        if kw["current_model"] == FALLBACK:
            return RerouteDecision(action="give_up", reason="already on the fallback")
        note = RerouteNote(
            from_model=kw["current_model"], to_model=FALLBACK, attempts_on_model=kw["attempts_on_model"],
            error_type=error_type, reason="overloaded",
        )
        return RerouteDecision(action="reroute", to_model=FALLBACK, reason="overloaded", note=note)

    monkeypatch.setattr(overload_reroute, "load_overload_policy", _policy)
    monkeypatch.setattr(overload_reroute, "load_offering_ladder", _no_ladder)
    monkeypatch.setattr(overload_reroute, "decide_overload_action", _decide)
    real_resolve = catalog_resolve.resolve_call_profile

    async def _resolve(model_ref: str, endpoint_hint: str | None = None, **kw: Any) -> Any:
        kw["offering_id"] = None
        return await real_resolve(model_ref, endpoint_hint, **kw)

    monkeypatch.setattr(catalog_resolve, "resolve_call_profile", _resolve)
    config = _config()
    config.tools = []
    completed = await execute_ai_request_quiet(config)
    assert sent[:2] == ["mock-model", FALLBACK], sent
    _assert_traced(completed, reason)


def test_a_swap_with_no_reason_is_refused() -> None:
    config = _persons_config()
    with pytest.raises(TypeError):
        config.model_this_turn_only(FALLBACK)  # type: ignore[call-arg]
    with pytest.raises(ValueError, match="swap reason"):
        config.model_this_turn_only(FALLBACK, swap_reason="because")
    config.model_this_turn_only(FALLBACK, swap_reason="free_tier")
    assert config.end_model_this_turn_only() and config.model_swaps_this_turn is None


@pytest.mark.asyncio
async def test_a_pick_sent_as_an_id_is_traced_by_its_name(monkeypatch, probe_tool, _pin_resolves_as_the_models_own_route) -> None:  # noqa: F811
    """Live (AND-IMG12): a guest's ``/ai/chat`` sends ``ai_model_id``, so the config holds the model's id and
    the row said ``original_model: <uuid>``. The dispatch gate resolved the name; the row carries it."""
    from test_execute_with_store import _MOCK_MODEL

    from matrx_ai.providers import free_tier_models as ftm

    _configure()
    _set_context(sub_agent=False)
    _scripted_model(monkeypatch, [])
    monkeypatch.setattr(ftm, "_resolver", lambda ctx: ftm.FreeTierPolicy(tier="guest", max_cost_rating=2))

    async def _target(original: str, policy: Any, **_kw: Any) -> Any:
        return (FALLBACK, "") if original == "mock-model" else None

    async def _quiet(*_a: Any, **_k: Any) -> None:
        return None

    monkeypatch.setattr(ftm, "free_tier_target", _target)
    monkeypatch.setattr(ftm, "tell_model_swapped", _quiet)
    monkeypatch.setattr(ftm, "admit_free_tier_model", _quiet)
    config = _persons_config()
    config.adopt_model_for_conversation(str(_MOCK_MODEL["id"]))
    completed = await execute_ai_request_quiet(config)
    _assert_traced(completed, "free_tier")


@pytest.mark.parametrize("reason", sorted(__import__("matrx_ai.config.unified_config", fromlist=["x"]).SWAP_REASONS))
def test_every_swap_site_records_names_through_the_one_door(monkeypatch, _pin_resolves_as_the_models_own_route, reason: str) -> None:  # noqa: F811
    """CGU-10 AND-IMG13 #5: only 2 of 6 sites passed a resolved name, so the auth-tier hop, minor safety and
    the overload / billing / offering reroutes recorded ``config.model`` — an id when the pick arrived as one.
    THE door names both ends, for all six reasons (``SWAP_REASONS`` is the list, so a seventh is covered)."""
    from test_execute_with_store import _MOCK_MODEL

    from matrx_ai.catalog.manager import ai_catalog_manager
    from matrx_ai.config.unified_config import swap_model_this_turn_only

    _configure()
    model_id = str(_MOCK_MODEL["id"])
    # The server holds the catalog in memory (``ai_catalog_manager``): the id routes to the row named mock-model.
    monkeypatch.setattr(ai_catalog_manager, "_model_ids", frozenset({model_id}))
    monkeypatch.setattr(ai_catalog_manager, "_model_names", {"mock-model": model_id})
    monkeypatch.setattr(ai_catalog_manager, "_model_state", {model_id: {"id": model_id, "name": "mock-model"}})
    config = _persons_config()
    config.adopt_model_for_conversation(model_id)
    assert config.model == model_id, "the config must hold the id for this test to mean anything"
    swap_model_this_turn_only(config, model_id, swap_reason=reason)
    step = config.model_swaps_this_turn[-1]
    assert step == {"from": "mock-model", "to": "mock-model", "reason": reason}, step
