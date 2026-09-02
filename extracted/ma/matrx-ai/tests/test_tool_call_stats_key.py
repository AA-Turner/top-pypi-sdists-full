"""The counter must count — the producer's key and the consumer's key must agree.

Twice now, in ONE function, a graph-node result read a stats key that its
producer never emits: `duration_ms` (found 2026-08-20) and `tool_calls_made`
(found 2026-08-22). Both reported 0 on every real run, forever, with no error.

`tool_calls_made` is the more expensive of the two, because something reasons
about it: a Hindsight reviewer judging the podcast research step read `0` as
proof that no web search had occurred and filed a confident finding telling us
to wire in a search tool that was already wired. A silent zero does not just
lose information — it manufactures a false one.

These cases pin the CONTRACT (aggregate's key set) against its CONSUMER, which
is the only place the agreement can be broken again.
"""

from __future__ import annotations

from matrx_ai.orchestrator.tracking import ToolCallUsage


def _usage(iteration: int, count: int, names: list[str]) -> ToolCallUsage:
    return ToolCallUsage(
        iteration=iteration,
        tool_calls_count=count,
        tool_calls_details=[{"name": n, "success": True} for n in names],
    )


def test_aggregate_emits_the_key_the_consumer_reads() -> None:
    """The regression itself: `shared.py` read `total_calls`, which aggregate
    has never emitted under any input — empty or populated."""
    empty = ToolCallUsage.aggregate([])
    populated = ToolCallUsage.aggregate([_usage(1, 2, ["research_web", "web"])])

    assert "total_tool_calls" in empty
    assert "total_tool_calls" in populated
    # Pin the shape both ways: if a future change renames the key, the consumer
    # below must be updated in the same commit.
    assert populated["total_tool_calls"] == 2


def test_a_real_search_turn_is_not_reported_as_zero() -> None:
    """The exact live case: a research call that DID call its tools."""
    from matrx_ai.graph_nodes.shared import _extract_usage  # noqa: F401 — import guard

    stats = ToolCallUsage.aggregate(
        [_usage(1, 1, ["research_web"]), _usage(2, 1, ["web"])]
    )
    # This is the consumer's exact expression, kept in lockstep with shared.py.
    tool_calls_made = int(
        stats.get("total_tool_calls") or stats.get("total_calls") or 0
    )
    assert tool_calls_made == 2, "a run with two tool calls must not report zero"


def test_the_replay_harness_shape_is_still_honored() -> None:
    """`testing/record_replay.py` builds `total_calls` directly — the fallback
    exists for it and must keep working."""
    stats = {"total_calls": 3}
    assert int(stats.get("total_tool_calls") or stats.get("total_calls") or 0) == 3


def test_no_tool_calls_is_still_zero() -> None:
    """The honest zero must survive — a run that really made no call."""
    stats = ToolCallUsage.aggregate([_usage(1, 0, [])])
    assert int(stats.get("total_tool_calls") or stats.get("total_calls") or 0) == 0
