"""Per-iteration trim audit lands on the cx_request row it compacted.

Before 2026-09-08 the executor's send-boundary trim overwrote the resolver's
``last_trim_report`` and persistence only ever attached that key to iteration
1 — so every in-loop trim (the ones that make an agent re-fetch data it
already had) was audited into nowhere: 0 of ~1,400 iteration≥2 rows carried a
trim_summary while agents were seeing "[tool result cleared]".
"""

from __future__ import annotations

from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_ai.db.persistence import _latest_trim_summary
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest


def _completed(iterations: int) -> CompletedRequest:
    config = UnifiedConfig(model="gpt-oss-120b", messages=[{"role": "user", "content": "hi"}])
    req = AIMatrixRequest(
        conversation_id="c1",
        config=config,
        usage_history=[
            TokenUsage(
                input_tokens=10, output_tokens=5, matrx_model_name="gpt-oss-120b", api="together"
            )
            for _ in range(iterations)
        ],
    )
    return CompletedRequest(request=req, iterations=iterations, final_response=None)


def test_in_loop_trim_lands_on_its_own_iteration_row() -> None:
    ctx = AppContext(emitter=None, user_id="u1")
    ctx.metadata["last_trim_report"] = {"blocks_rewritten": 0, "freed_chars": 0}
    ctx.metadata["trim_reports_by_iteration"] = {
        3: {"blocks_rewritten": 2, "freed_chars": 180_000},
        5: {"blocks_rewritten": 1, "freed_chars": 14_000},
    }
    token = set_app_context(ctx)
    try:
        rows = _completed(5).to_storage_dict()["requests"]
    finally:
        clear_app_context(token)

    by_iter = {r["iteration"]: r.get("trim_summary") for r in rows}
    assert by_iter[1] == {"blocks_rewritten": 0, "freed_chars": 0}
    assert by_iter[2] is None
    assert by_iter[3]["freed_chars"] == 180_000
    assert by_iter[4] is None
    assert by_iter[5]["freed_chars"] == 14_000
    assert _latest_trim_summary(rows)["freed_chars"] == 14_000


def test_latest_trim_summary_skips_rows_without_one() -> None:
    rows = [{"iteration": 1, "trim_summary": {"blocks_rewritten": 1}}, {"iteration": 2}]
    assert _latest_trim_summary(rows) == {"blocks_rewritten": 1}
    assert _latest_trim_summary([]) is None
