"""``SendPrep.fit`` is recorded on the request row the way the trim audit is.

``prepare_for_send`` measured and shrank a call to fit (``input_fit``) and kept the record only on
the in-memory ``SendPrep`` — gone when the pass ended, so a shrunk call could not be told from an
untouched one afterwards. The trim audit was already landed on AppContext and persisted on its
iteration's ``cx_request`` row; the fit record now rides the same road, as
``cx_request.metadata["input_fit"]``, and only when a fit was recorded (``fit`` not ``None``).
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from test_input_fit import (  # noqa: F401
    CONVERSATION_ID,
    REQUEST_ID,
    _budget,
    _clean,  # noqa: F401  (the autouse fixture that frees the budget seams)
    _long_tool_loop,
)

from matrx_ai.config import input_fit
from matrx_ai.config.context_preflight import estimate_prompt_tokens
from matrx_ai.config.send_boundary import (
    STAGE_LOOP,
    STAGE_RESOLVE,
    prepare_for_send,
)
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest


def _rows(ctx: AppContext, iterations: int) -> list[dict]:
    config = UnifiedConfig(model="gpt-oss-120b", messages=[{"role": "user", "content": "hi"}])
    request = AIMatrixRequest(
        conversation_id="c1",
        config=config,
        usage_history=[
            TokenUsage(
                input_tokens=10, output_tokens=5, matrx_model_name="gpt-oss-120b", api="together"
            )
            for _ in range(iterations)
        ],
    )
    done = CompletedRequest(request=request, iterations=iterations, final_response=None)
    token = set_app_context(ctx)
    try:
        return done.to_storage_dict()["requests"]
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", [STAGE_LOOP, STAGE_RESOLVE])
async def test_a_fit_pass_is_recorded_on_the_context_and_lands_on_its_row(stage: str) -> None:
    ctx = AppContext(emitter=None, user_id="u1")
    token = set_app_context(ctx)
    try:
        config = _long_tool_loop()
        _budget(estimate_prompt_tokens(config) // 3)
        prep = await prepare_for_send(
            config,
            stage=stage,
            conversation_id=CONVERSATION_ID,
            request_id=REQUEST_ID,
            iteration=2 if stage == STAGE_LOOP else None,
        )
    finally:
        clear_app_context(token)
    assert prep.fit and prep.fit["fits"] is True

    rows = _rows(ctx, 3)
    by_iter = {r["iteration"]: (r.get("metadata") or {}).get("input_fit") for r in rows}
    landed_on = 2 if stage == STAGE_LOOP else 1
    assert by_iter[landed_on] == prep.fit
    assert all(v is None for i, v in by_iter.items() if i != landed_on)


@pytest.mark.asyncio
async def test_a_pass_with_no_fit_record_leaves_no_trace(monkeypatch) -> None:
    ctx = AppContext(emitter=None, user_id="u1")
    token = set_app_context(ctx)
    try:
        config = SimpleNamespace(
            model="claude-opus-5-5",
            matrx_model_name="claude-opus-5-5",
            messages=[{"role": "user", "content": "hi"}],
            system_instruction=None,
            tools=[],
            prompt_cache_key=None,
        )

        async def _no_limit_known(*_a, **_kw):
            return None

        monkeypatch.setattr(input_fit, "ensure_fits", _no_limit_known)
        prep = await prepare_for_send(
            config,
            stage=STAGE_LOOP,
            conversation_id=CONVERSATION_ID,
            request_id=REQUEST_ID,
            iteration=1,
        )
    finally:
        clear_app_context(token)
    assert prep.fit is None
    assert "fit_by_iteration" not in ctx.metadata and "last_fit" not in ctx.metadata
    assert all("input_fit" not in (r.get("metadata") or {}) for r in _rows(ctx, 1))
