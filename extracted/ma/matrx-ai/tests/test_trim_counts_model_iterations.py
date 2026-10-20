"""Trim distance is counted in MODEL ITERATIONS, and nothing is trimmed before
the model has acted on it (2026-10-17).

Conversation e9c0d599 (Google AI Model Sync, Opus 5.5): a parallel batch of tool
calls appended one message per result, so a provider-settings read and a DB
structure read were 12-14 raw messages back after only one or two model
iterations, and were cleared before the agent had used them. One iteration is
now ONE assistant message plus all its results (2 positions), and a block with
no assistant message after it is never trimmed, whatever the tiers say.
"""

from __future__ import annotations

from matrx_ai.config import ToolCallContent, ToolResultContent, UnifiedMessage
from matrx_ai.config.context_trim import TrimPolicy, trim_messages_context


def _calls(n: int, tag: str) -> UnifiedMessage:
    return UnifiedMessage(
        role="assistant",
        content=[
            ToolCallContent(id=f"{tag}-{i}", name="sql", arguments={"q": f"{tag}-{i}"})
            for i in range(n)
        ],
    )


def _result(tag: str, chars: int = 13_500) -> UnifiedMessage:
    return UnifiedMessage(
        role="tool",
        content=[
            ToolResultContent(tool_use_id=tag, call_id=tag, name="sql", content="x" * chars, output_chars=chars)
        ],
    )


def _batch(n: int, tag: str) -> list[UnifiedMessage]:
    return [_calls(n, tag)] + [_result(f"{tag}-{i}") for i in range(n)]


def test_a_fourteen_result_parallel_batch_is_not_trimmed_before_the_model_reads_it() -> None:
    # Raw distance puts the first two results 13 and 12 messages back (tier 1);
    # the model has not had a single turn since they arrived.
    messages = _batch(14, "batch")
    report = trim_messages_context(messages)
    assert report.blocks_rewritten == 0
    assert all("cleared" not in str(m.content[0].content) for m in messages[1:])


def test_one_iteration_after_a_batch_its_results_are_two_positions_back() -> None:
    messages = _batch(14, "batch") + _batch(1, "next")
    report = trim_messages_context(messages)
    assert report.blocks_rewritten == 0  # 2 positions back, tier 1 needs 12


def test_never_unacted_even_when_an_org_sets_the_tier_to_zero() -> None:
    policy = TrimPolicy(tier_1_min_positions_back=0, tier_1_min_output_chars=1_000)
    messages = _batch(3, "old") + _batch(3, "fresh")
    report = trim_messages_context(messages, policy=policy)
    trimmed = {b["call_id"] for b in report.rewritten_blocks}
    # The acted-on batch goes; the batch the model has not seen yet stays whole.
    assert trimmed == {"old-0", "old-1", "old-2"}
    assert all(b["iterations_back"] == 1 for b in report.rewritten_blocks)
    assert all("cleared" not in str(m.content[0].content) for m in messages[5:])


def test_parallel_results_age_by_iterations_not_by_message_count() -> None:
    # Five 14-wide batches: the first batch is 4 iterations (8 positions) back,
    # under tier 1 — raw counting had it 50+ messages back, past tier 2.
    messages: list[UnifiedMessage] = []
    for b in range(5):
        messages += _batch(14, f"b{b}")
    report = trim_messages_context(messages)
    assert report.blocks_rewritten == 0

    # Two more iterations put the first batch 6 iterations (12 positions) back.
    messages += _batch(1, "c0") + _batch(1, "c1")
    report = trim_messages_context(messages)
    assert {b["call_id"].split("-")[0] for b in report.rewritten_blocks} == {"b0"}
    assert report.blocks_rewritten == 14
    assert {b["positions_back"] for b in report.rewritten_blocks} == {12}


def test_one_response_split_into_two_assistant_messages_counts_once() -> None:
    """Adversarial review M2 (2026-10-18): a translator may store ONE provider
    response as two consecutive assistant messages (text, then the tool calls).
    Counting both aged every older result one extra iteration per split, so
    results were trimmed ~2x sooner than the tiers say."""
    from matrx_ai.config import TextContent
    from matrx_ai.config.context_trim import _iteration_distances

    def split_iteration(tag: str) -> list[UnifiedMessage]:
        return [
            UnifiedMessage(role="assistant", content=[TextContent(text=f"thinking {tag}")]),
            _calls(1, tag),
            _result(f"{tag}-0"),
        ]

    plain = _batch(1, "old") + _batch(1, "a") + _batch(1, "b")
    split = _batch(1, "old") + split_iteration("a") + split_iteration("b")
    # The old result has two model iterations after it either way.
    assert _iteration_distances(plain)[1] == (4, 2)
    assert _iteration_distances(split)[1] == (4, 2), _iteration_distances(split)
    # Both halves of one response sit at the same distance.
    distances = _iteration_distances(split)
    assert distances[2][1] == distances[3][1]
