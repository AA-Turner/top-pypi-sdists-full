"""A cleared tool result says it was cleared AND names the exact call that reads it again.

Live (conversation d1e4226e, 2026-11-12): a 26 KB ``sql`` lookup of ``company.legal_document_type``
(ids included) was cleared six iterations later by the context trimmer. The stub said only
"[tool result cleared] Replaced with keys and chars -- Fetch again when necessary"; the agent
wrote document_type_id values from memory, they were wrong, and an FK refusal caught it. Every
clearing path (``trim_messages_context``, the history token budget, and its warm-cache replay)
now writes a ``refetch`` naming the tool and its arguments, built from the call as it ran.
"""

from __future__ import annotations

import json

from matrx_ai.config import ToolCallContent, ToolResultContent, UnifiedMessage
from matrx_ai.config.context_trim import REFETCH_ARGUMENTS_MAX_CHARS, trim_messages_context
from matrx_ai.config.history_budget import clear_tool_results, trim_history_to_token_budget

LOOKUP_ARGS = {"table": "company.legal_document_type", "action": "query"}


def _loop(first_args: dict, iterations: int = 9) -> list[UnifiedMessage]:
    messages: list[UnifiedMessage] = [
        UnifiedMessage(role="assistant", content=[ToolCallContent(id="call-lookup", name="sql", arguments=first_args)]),
        UnifiedMessage(
            role="tool",
            content=[
                ToolResultContent(
                    tool_use_id="call-lookup",
                    name="sql",
                    content="x" * 26_000,
                    output_chars=26_000,
                    output_preview={"keys": ["__kind", "rows", "count"], "chars": 26_000},
                )
            ],
        ),
    ]
    for i in range(iterations):
        messages.append(
            UnifiedMessage(role="assistant", content=[ToolCallContent(id=f"c{i}", name="sql", arguments={"i": i})])
        )
        messages.append(
            UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id=f"c{i}", name="sql", content="ok")])
        )
    return messages


def _stub(messages: list[UnifiedMessage]) -> dict:
    content = messages[1].content[0].content
    assert isinstance(content, str) and content.startswith('{"result": "[tool result cleared]'), content
    return json.loads(content)


def test_the_trimmer_names_the_exact_call() -> None:
    messages = _loop(LOOKUP_ARGS)
    report = trim_messages_context(messages)
    assert report.blocks_rewritten == 1
    stub = _stub(messages)
    assert stub["refetch"] == {"tool": "sql", "arguments": LOOKUP_ARGS}
    assert "never write them from memory" in stub["result"]
    assert stub["chars"] == 26_000  # the preview still rides along


def test_long_arguments_are_not_repeated() -> None:
    long_args = {"table": "t", "action": "query", "filter": "y" * (REFETCH_ARGUMENTS_MAX_CHARS + 50)}
    messages = _loop(long_args)
    trim_messages_context(messages)
    stub = _stub(messages)
    assert stub["refetch"]["tool"] == "sql"
    assert "arguments" not in stub["refetch"]
    assert "y" * 100 not in json.dumps(stub)


def test_the_argument_cap_is_measured_as_written() -> None:
    """Non-ASCII arguments are escaped in the stub; the cap counts the escaped size."""
    args = {"table": "t", "action": "query", "q": "é" * (REFETCH_ARGUMENTS_MAX_CHARS // 2)}
    messages = _loop(args)
    trim_messages_context(messages)
    assert "arguments" not in _stub(messages)["refetch"]


def test_a_write_is_never_offered_as_the_refetch() -> None:
    insert = {"table": "company.legal_entity_document", "action": "insert", "data": [{"title": "x"}]}
    messages = _loop(insert)
    trim_messages_context(messages)
    refetch = _stub(messages)["refetch"]
    assert refetch["tool"] == "sql"
    assert "arguments" not in refetch
    assert "never re-run" in refetch["how"]


def test_an_unclassified_tool_gets_no_arguments() -> None:
    messages = _loop({"to": "someone@example.com"})
    messages[0].content[0].name = "send_email"
    messages[1].content[0].name = "send_email"
    trim_messages_context(messages)
    refetch = _stub(messages)["refetch"]
    assert refetch["tool"] == "send_email" and "arguments" not in refetch


def test_trimmed_arguments_say_query_again() -> None:
    from matrx_ai.config.context_trim import TRIMMED_ARGUMENT_MARKER

    messages = _loop({"action": "query", "table": "t", "filter": f"abc…[9 more chars {TRIMMED_ARGUMENT_MARKER}]"})
    trim_messages_context(messages)
    refetch = _stub(messages)["refetch"]
    assert "arguments" not in refetch
    assert "query again" in refetch["how"]
    assert TRIMMED_ARGUMENT_MARKER not in json.dumps(refetch)


def test_live_and_rebuilt_names_give_the_same_bytes() -> None:
    """A live call carries the wire name, a DB-rebuilt one the internal name."""
    live, rebuilt = _loop(LOOKUP_ARGS), _loop(LOOKUP_ARGS)
    for messages, name in ((live, "db__read"), (rebuilt, "db:read")):
        messages[0].content[0].name = name
        messages[1].content[0].name = name
    trim_messages_context(live)
    trim_messages_context(rebuilt)
    assert live[1].content[0].content == rebuilt[1].content[0].content
    assert _stub(live)["refetch"]["tool"] == "db__read"


def test_a_stub_never_replaces_something_smaller() -> None:
    """10 small sql results over a tiny budget: clearing must never GROW the history."""
    messages: list[UnifiedMessage] = []
    for i in range(10):
        messages.append(
            UnifiedMessage(role="assistant", content=[ToolCallContent(id=f"s{i}", name="sql", arguments=LOOKUP_ARGS)])
        )
        messages.append(
            UnifiedMessage(
                role="tool",
                content=[ToolResultContent(tool_use_id=f"s{i}", name="sql", content="r" * 300, output_chars=300)],
            )
        )
    report = trim_history_to_token_budget(messages, budget_tokens=500)
    assert report.tokens_after <= report.tokens_before
    assert report.blocks_cleared == 0
    assert all(m.content[0].content == "r" * 300 for m in messages[1::2])
    # The replay of a recorded cut decides the same way.
    assert clear_tool_results(messages, {f"s{i}" for i in range(10)}) == 0


def test_the_trimmer_never_grows_a_result() -> None:
    from matrx_ai.config.context_trim import TrimPolicy

    messages = _loop(LOOKUP_ARGS)
    messages[1].content[0].content = "x" * 200
    messages[1].content[0].output_chars = 20_000  # a stale size claim must not force a growing stub
    report = trim_messages_context(messages, TrimPolicy(tier_1_min_output_chars=10, tier_2_min_output_chars=10))
    assert report.blocks_rewritten - report.arguments_rewritten == 0  # no RESULT was rewritten
    assert messages[1].content[0].content == "x" * 200


def test_the_history_budget_and_its_replay_name_the_same_call() -> None:
    budgeted = _loop(LOOKUP_ARGS, iterations=1)
    report = trim_history_to_token_budget(budgeted, budget_tokens=1_000)
    assert report.blocks_cleared == 1
    replayed = _loop(LOOKUP_ARGS, iterations=1)
    assert clear_tool_results(replayed, set(report.cleared_ids)) == 1
    # The warm-cache replay rebuilds the cut byte for byte.
    assert budgeted[1].content[0].content == replayed[1].content[0].content
    assert _stub(budgeted)["refetch"] == {"tool": "sql", "arguments": LOOKUP_ARGS}


def test_the_stub_is_stable_across_sends() -> None:
    first, second = _loop(LOOKUP_ARGS), _loop(LOOKUP_ARGS)
    trim_messages_context(first)
    trim_messages_context(second)
    assert first[1].content[0].content == second[1].content[0].content
    # Re-running the trim on the already-trimmed list changes nothing.
    before = first[1].content[0].content
    trim_messages_context(first)
    assert first[1].content[0].content == before
