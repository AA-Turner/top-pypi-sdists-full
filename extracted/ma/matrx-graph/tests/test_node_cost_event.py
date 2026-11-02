"""node_cost_from_output — per-model cost key + primary-model selection.

Regression for the review finding: producers write per-model ``cost_usd``
(AiUsage buckets) but ``_model_cost`` read ``cost`` — per-model cost ranked
as 0.0 and the primary model label was arbitrary.
"""

from __future__ import annotations

from matrx_graph.types.events import node_cost_from_output

_IDS = dict(run_id="run-1234567890", step=1, node_id="n1", spec_type="ai.agent", attempt=1)


def _usage(models: dict) -> dict:
    return {
        "usage": {
            "cost_usd": 0.5,
            "input_tokens": 100,
            "output_tokens": 50,
            "total_tokens": 150,
            "models": models,
        }
    }


def test_primary_model_picked_by_cost_usd():
    event = node_cost_from_output(
        _usage(
            {
                "cheap-model": {"cost_usd": 0.01},
                "expensive-model": {"cost_usd": 0.49},
            }
        ),
        **_IDS,
    )
    assert event is not None
    assert event.model == "expensive-model"
    assert set(event.models) == {"cheap-model", "expensive-model"}


def test_primary_model_accepts_legacy_cost_key():
    event = node_cost_from_output(
        _usage(
            {
                "old-cheap": {"cost": 0.02},
                "old-expensive": {"cost": 0.48},
            }
        ),
        **_IDS,
    )
    assert event is not None
    assert event.model == "old-expensive"


def test_cost_usd_wins_over_legacy_cost_in_same_entry():
    event = node_cost_from_output(
        _usage(
            {
                "a": {"cost_usd": 0.4, "cost": 0.0},
                "b": {"cost_usd": 0.1, "cost": 99.0},
            }
        ),
        **_IDS,
    )
    assert event is not None
    assert event.model == "a"


def test_no_usage_returns_none():
    assert node_cost_from_output({}, **_IDS) is None
    assert node_cost_from_output({"usage": {"cost_usd": 0.0}}, **_IDS) is None


def test_cost_event_preserves_fanout_invocation_identity():
    event = node_cost_from_output(
        _usage({"model": {"cost_usd": 0.5}}),
        **_IDS,
        dispatch_id="dispatch-a",
        item_index=4,
    )
    assert event is not None
    assert event.dispatch_id == "dispatch-a"
    assert event.item_index == 4


def test_cached_tokens_ride_the_cost_event():
    """The usage block's prompt-cache tokens reach the event (they were dropped: only input/output/total did)."""
    payload = _usage({"m": {"cost_usd": 0.5}})
    payload["usage"].update(cached_input_tokens=800, cache_write_tokens=120)
    event = node_cost_from_output(payload, **_IDS)
    assert event is not None
    assert (event.cached_input_tokens, event.cache_write_tokens) == (800, 120)
    assert event.model_dump()["cached_input_tokens"] == 800  # persists into the node_cost payload


def test_cached_tokens_default_to_zero_when_the_producer_does_not_report_them():
    event = node_cost_from_output(_usage({"m": {"cost_usd": 0.5}}), **_IDS)
    assert event is not None
    assert (event.cached_input_tokens, event.cache_write_tokens) == (0, 0)
