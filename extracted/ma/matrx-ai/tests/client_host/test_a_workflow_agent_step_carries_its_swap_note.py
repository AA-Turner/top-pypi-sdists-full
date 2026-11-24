"""A WORKFLOW AGENT STEP CARRIES THE SWAP IT TOLD THE PERSON ABOUT (research-as-workflow lane F2b, 2026-11-19).

A free-tier or HIPAA stand-in tells the person on the stream (``info:model_swapped``), but inside a workflow that
notice rides the agent step's own emitter, which the workflow's caller never hears: the code engine's research
report said "Ran on Sonnet. Upgrade for Opus." and the workflow said nothing. The step's result now carries the
swap (``metadata.model_swapped``: the sentence, the model picked, the model that ran, why), so any workflow can say
it on its own line. Through the REAL executor (the in-repo mock provider), then the agent steps' ONE normalizer
(``graph_nodes.shared.normalize_completed``). Red when the normalizer stops reading the swap, or reads a reroute
(provenance, never a notice) as one.
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

from matrx_ai.graph_nodes.shared import MODEL_SWAPPED_KEY, normalize_completed  # noqa: E402


@pytest.mark.asyncio
async def test_a_free_tier_swap_rides_the_steps_result_with_the_sentence_the_person_read(
    monkeypatch, probe_tool, _pin_resolves_as_the_models_own_route  # noqa: F811
) -> None:
    from matrx_ai.context.app_context import try_get_app_context
    from matrx_ai.providers import free_tier_models as ftm

    _configure()
    _set_context(sub_agent=False)
    seen = _scripted_model(monkeypatch, [])
    monkeypatch.setattr(ftm, "_resolver", lambda ctx: ftm.FreeTierPolicy(tier="free", max_cost_rating=2))

    async def _target(original: str, policy: Any, **_kw: Any) -> Any:
        return (FALLBACK, "") if original == "mock-model" else None

    async def _tell(ctx: Any, original: str, new: str, policy: Any, *, person_picked: bool = False) -> None:
        # What the real notice writes on the request context (its labels need the catalog); like the real one,
        # it speaks only when the person picked the model.
        if not person_picked:
            return
        ctx.metadata[ftm.MODEL_SWAP_NOTE_KEY] = f"Ran on {new}. Upgrade for {original}."

    async def _quiet(*_a: Any, **_k: Any) -> None:
        return None

    monkeypatch.setattr(ftm, "free_tier_target", _target)
    monkeypatch.setattr(ftm, "tell_model_swapped", _tell)
    monkeypatch.setattr(ftm, "admit_free_tier_model", _quiet)

    config = _persons_config()
    config.model_picked_by_person = True  # the notice is spoken only for a model the person picked
    completed = await execute_ai_request_quiet(config)
    assert seen and seen[0][0] == FALLBACK
    assert try_get_app_context() is not None
    swapped = normalize_completed(completed).metadata.get(MODEL_SWAPPED_KEY)
    assert swapped == {
        "message": f"Ran on {FALLBACK}. Upgrade for mock-model.",
        "original_model": "mock-model",
        "model": FALLBACK,
        "reason": "free_tier",
    }, swapped


@pytest.mark.asyncio
async def test_a_hipaa_swap_rides_the_steps_result(monkeypatch, probe_tool, _pin_resolves_as_the_models_own_route) -> None:  # noqa: F811
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
    swapped = normalize_completed(completed).metadata.get(MODEL_SWAPPED_KEY)
    assert swapped == {"message": baa_gate.HIPAA_SWAP_SENTENCE, "original_model": "mock-model", "model": FALLBACK,
                       "reason": "hipaa"}, swapped


@pytest.mark.asyncio
async def test_a_turn_with_no_told_swap_carries_none(monkeypatch, probe_tool, _pin_resolves_as_the_models_own_route) -> None:  # noqa: F811
    """No swap, and a host hop the person is not told about (minor safety: a trace, no notice), carry nothing."""
    from matrx_ai.config.unified_config import swap_model_this_turn_only

    _configure()
    _set_context(sub_agent=False)
    _scripted_model(monkeypatch, [])
    completed = await execute_ai_request_quiet(_persons_config())
    assert MODEL_SWAPPED_KEY not in normalize_completed(completed).metadata

    config = _persons_config()
    swap_model_this_turn_only(config, FALLBACK, swap_reason="minor_safety")
    completed = await execute_ai_request_quiet(config)
    assert MODEL_SWAPPED_KEY not in normalize_completed(completed).metadata
