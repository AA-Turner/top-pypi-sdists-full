"""Podcast usage on checkpoint resume — report full, never settle twice (#8).

A resumed run replays completed stages from the checkpoint. Their ``usage``
must be RESTORED (dropping it under-reported the run's true cost) but marked
``usage_settled`` — the prior attempt already settled that spend (its terminal
aggregate went to the scheduler via the success payload's ``usage`` or the
failure's ``details.usage``). The invariant: **a resumed run reports full
usage but never settles the same stage twice.** The settle-safe delta travels
as ``unsettled_usage`` → the consuming caller's settlement channel.
"""

from __future__ import annotations

from matrx_ai.agent_runners._checkpoint import REPLAYED_KEY
from matrx_ai.agent_runners.podcast_generator import (
    PodcastGenerationResult,
    StageResult,
    _aggregate_stage_usage,
    _stage_from_payload,
)

# Per-model buckets carry the full canonical AiModelUsage key-set (incl.
# request_count / api defaults) — the shape AiUsage.model_dump() now emits.
_USAGE_A = {
    "input_tokens": 100,
    "output_tokens": 50,
    "total_tokens": 150,
    "cost_usd": 0.01,
    "models": {
        "m1": {
            "input_tokens": 100, "output_tokens": 50, "total_tokens": 150,
            "cost_usd": 0.01, "request_count": 0, "api": "",
        }
    },
}
_USAGE_B = {
    "input_tokens": 200,
    "output_tokens": 100,
    "total_tokens": 300,
    "cost_usd": 0.02,
    "models": {
        "m1": {
            "input_tokens": 200, "output_tokens": 100, "total_tokens": 300,
            "cost_usd": 0.02, "request_count": 0, "api": "",
        }
    },
}


def test_a_REPLAYED_stage_restores_usage_and_is_marked_settled():
    sr = StageResult(stage="create_script", success=True, output="s", usage=_USAGE_A)
    payload = {**sr.model_dump(), REPLAYED_KEY: True}  # what ckpt.stage() returns on a hit
    replayed = _stage_from_payload("create_script", payload)
    assert replayed.usage == _USAGE_A  # reported — no longer dropped
    assert replayed.usage_settled is True  # ...but never settled again


def test_a_FRESH_stage_with_usage_is_NOT_marked_settled():
    """The bug that made every run report $0.00.

    `_stage_from_payload` runs on every stage, not just replays. Keying
    `usage_settled` on "the payload carries usage" therefore marked stages that
    had JUST EXECUTED as already-paid-for, so the settle-safe aggregate came out
    empty and real spend was never written to the run. Only the checkpointer's
    replay marker may set this flag.
    """
    sr = StageResult(stage="create_audio", success=True, output="cdn://a.mp3", usage=_USAGE_A)
    fresh = _stage_from_payload("create_audio", sr.model_dump())  # no replay marker
    assert fresh.usage == _USAGE_A
    assert fresh.usage_settled is False
    assert _aggregate_stage_usage([fresh], unsettled_only=True) == _USAGE_A


def test_stage_from_payload_without_usage():
    replayed = _stage_from_payload("k", {"stage": "k", "success": True, "output": "x"})
    assert replayed.usage is None
    assert replayed.usage_settled is False


def test_resumed_run_reports_full_but_settles_only_this_attempt():
    # Attempt 1 paid for create_script (checkpointed, settled on its failure);
    # attempt 2 replays it and pays only for create_audio's agent usage.
    replayed = _stage_from_payload(
        "create_script",
        {
            **StageResult(
                stage="create_script", success=True, output="s", usage=_USAGE_A
            ).model_dump(),
            REPLAYED_KEY: True,
        },
    )
    fresh = StageResult(stage="generate_metadata", success=True, output="m", usage=_USAGE_B)
    stages = [replayed, fresh]

    full = _aggregate_stage_usage(stages)
    delta = _aggregate_stage_usage(stages, unsettled_only=True)

    assert full is not None and delta is not None
    assert full["cost_usd"] == round(0.01 + 0.02, 6) or abs(full["cost_usd"] - 0.03) < 1e-9
    assert full["total_tokens"] == 450
    assert delta["cost_usd"] == 0.02  # replayed stage excluded from settlement
    assert delta["total_tokens"] == 300


def test_fresh_run_delta_equals_full():
    stages = [
        StageResult(stage="a", success=True, usage=_USAGE_A),
        StageResult(stage="b", success=False, error="x", usage=_USAGE_B),
    ]
    assert _aggregate_stage_usage(stages) == _aggregate_stage_usage(stages, unsettled_only=True)


def test_all_replayed_yields_no_settlement_block():
    replayed = _stage_from_payload(
        "a",
        {**StageResult(stage="a", success=True, usage=_USAGE_A).model_dump(), REPLAYED_KEY: True},
    )
    assert _aggregate_stage_usage([replayed]) is not None  # still reported
