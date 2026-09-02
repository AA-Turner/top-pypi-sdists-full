"""Defense-in-depth guards against duplicate ``tool_result`` blocks.

The 2026-06-22 incident (conversation ``bcc588b6-...``): two ``tool_result``
blocks with the same ``tool_use_id`` reached Anthropic and 400'd the WHOLE
request ("each tool_use must have a single result"), which then failed every
subsequent turn. The root cause lives in conversation rebuild (covered by
``test_conversation_rebuild_hydration.py``); THIS file covers the two
independent guards that must catch the duplicate even if the root fix is
bypassed (the live-loop ``dataclasses.replace`` and cache-hit ``deepcopy`` paths
both skip ``MessageList.sanitize``):

1. ``MessageList.sanitize`` — provider-agnostic assembly guard.
2. The Anthropic translator — the final provider-payload boundary (last line
   before the wire), which runs on EVERY call.
"""

from __future__ import annotations

from matrx_ai.config import UnifiedConfig
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.tool_result_guard import (
    dedupe_tool_result_dicts,
    result_block_is_empty,
)
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_content import TextContent
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile

# ---------------------------------------------------------------------------
# The reusable dedup primitive (the heart of the translator's last line).
# ---------------------------------------------------------------------------


def test_dedupe_keeps_exactly_one_and_reports() -> None:
    content = [
        {"type": "tool_result", "tool_use_id": "X", "content": "a"},
        {"type": "tool_result", "tool_use_id": "X", "content": "a"},
        {"type": "text", "text": "hi"},
    ]
    out, dups = dedupe_tool_result_dicts(content)
    assert sum(1 for b in out if b.get("type") == "tool_result") == 1
    assert dups == [{"tool_use_id": "X", "name": None, "count": 2, "dropped": 1}]
    # Non-tool_result blocks are untouched.
    assert any(b.get("type") == "text" for b in out)


def test_dedupe_prefers_the_non_empty_block() -> None:
    """An empty pointer stub must never win over a block that carries output."""
    content = [
        {"type": "tool_result", "tool_use_id": "X", "content": ""},
        {"type": "tool_result", "tool_use_id": "X", "content": "the real result"},
    ]
    out, _ = dedupe_tool_result_dicts(content)
    kept = [b for b in out if b.get("type") == "tool_result"]
    assert len(kept) == 1
    assert kept[0]["content"] == "the real result"


def test_dedupe_preserves_distinct_ids() -> None:
    content = [
        {"type": "tool_result", "tool_use_id": "X", "content": "a"},
        {"type": "tool_result", "tool_use_id": "Y", "content": "b"},
    ]
    out, dups = dedupe_tool_result_dicts(content)
    assert dups == []
    assert len([b for b in out if b.get("type") == "tool_result"]) == 2


def test_dedupe_matches_on_call_id_fallback() -> None:
    """OpenAI-shaped blocks key on call_id, not tool_use_id."""
    content = [
        {"type": "tool_result", "call_id": "C", "content": "a"},
        {"type": "tool_result", "call_id": "C", "content": "a"},
    ]
    out, dups = dedupe_tool_result_dicts(content)
    assert len([b for b in out if b.get("type") == "tool_result"]) == 1
    assert dups[0]["count"] == 2


def test_result_block_is_empty() -> None:
    assert result_block_is_empty(None)
    assert result_block_is_empty("")
    assert result_block_is_empty("   ")
    assert result_block_is_empty([])
    assert result_block_is_empty({})
    assert not result_block_is_empty("x")
    assert not result_block_is_empty([{"type": "text"}])


# ---------------------------------------------------------------------------
# Layer 2 — MessageList.sanitize (provider-agnostic assembly guard).
# ---------------------------------------------------------------------------


def _result_count(ml: MessageList, rid: str) -> int:
    n = 0
    for m in ml._messages:
        for c in m.content:
            if isinstance(c, ToolResultContent) and (c.tool_use_id or c.call_id) == rid:
                n += 1
    return n


def test_sanitize_drops_duplicate_tool_result_across_messages() -> None:
    """Two role='tool' messages each carrying a tool_result for the same id —
    the exact shape rebuild produced (a synthesised one + a persisted one).
    sanitize must collapse them to exactly one and keep the matching tool_use."""
    ml = MessageList(
        _messages=[
            UnifiedMessage(
                role="assistant",
                content=[ToolCallContent(id="X", name="research_web", arguments={})],
            ),
            UnifiedMessage(
                role="tool",
                content=[
                    ToolResultContent(
                        tool_use_id="X", call_id="X", name="research_web",
                        content="the real result",
                    )
                ],
            ),
            UnifiedMessage(
                role="tool",
                content=[
                    ToolResultContent(
                        tool_use_id="X", call_id="X", name="research_web",
                        content="",  # empty stub duplicate
                    )
                ],
            ),
        ]
    )
    ml.sanitize()
    assert _result_count(ml, "X") == 1, "duplicate tool_result must be removed"
    # The surviving block is the non-empty one.
    survivors = [
        c
        for m in ml._messages
        for c in m.content
        if isinstance(c, ToolResultContent)
    ]
    assert survivors[0].content == "the real result"
    # The matching tool_use is still present (not treated as an orphan).
    assert any(
        isinstance(c, ToolCallContent) and c.id == "X"
        for m in ml._messages
        for c in m.content
    )


def test_sanitize_preserves_reused_call_id_with_matching_tool_uses() -> None:
    """Gemini reuses deterministic call_ids ACROSS turns — each tool_use has its
    OWN legitimate result. With 2 tool_uses and 2 results for one id, NOTHING is
    a duplicate; the count-aware rule must keep BOTH (lossless, provider-safe)."""
    ml = MessageList(
        _messages=[
            UnifiedMessage(
                role="assistant",
                content=[ToolCallContent(id="gemini_-1", name="search", arguments={})],
            ),
            UnifiedMessage(
                role="tool",
                content=[ToolResultContent(tool_use_id="gemini_-1", call_id="gemini_-1", name="search", content="r1")],
            ),
            UnifiedMessage(
                role="assistant",
                content=[ToolCallContent(id="gemini_-1", name="search", arguments={})],
            ),
            UnifiedMessage(
                role="tool",
                content=[ToolResultContent(tool_use_id="gemini_-1", call_id="gemini_-1", name="search", content="r2")],
            ),
        ]
    )
    ml.sanitize()
    assert _result_count(ml, "gemini_-1") == 2, (
        "reused-id results that each pair with a tool_use must NOT be dropped — "
        "that would silently lose a Gemini tool result"
    )
    contents = sorted(
        c.content
        for m in ml._messages
        for c in m.content
        if isinstance(c, ToolResultContent)
    )
    assert contents == ["r1", "r2"]


def test_sanitize_drops_only_the_excess_for_reused_id() -> None:
    """3 results but only 2 tool_uses for one id → exactly ONE excess is dropped
    (the empty stub), the two real results survive."""
    ml = MessageList(
        _messages=[
            UnifiedMessage(role="assistant", content=[ToolCallContent(id="g1", name="s", arguments={})]),
            UnifiedMessage(role="assistant", content=[ToolCallContent(id="g1", name="s", arguments={})]),
            UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="g1", call_id="g1", name="s", content="real-a")]),
            UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="g1", call_id="g1", name="s", content="")]),
            UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="g1", call_id="g1", name="s", content="real-b")]),
        ]
    )
    ml.sanitize()
    assert _result_count(ml, "g1") == 2
    survivors = sorted(
        c.content for m in ml._messages for c in m.content if isinstance(c, ToolResultContent)
    )
    assert survivors == ["real-a", "real-b"], "the empty stub is the excess that gets dropped"


def test_sanitize_leaves_single_results_untouched() -> None:
    ml = MessageList(
        _messages=[
            UnifiedMessage(
                role="assistant",
                content=[ToolCallContent(id="X", name="t", arguments={})],
            ),
            UnifiedMessage(
                role="tool",
                content=[ToolResultContent(tool_use_id="X", call_id="X", name="t", content="r")],
            ),
        ]
    )
    ml.sanitize()
    assert _result_count(ml, "X") == 1


# ---------------------------------------------------------------------------
# Layer 1 — Anthropic translator (final provider-payload boundary).
# ---------------------------------------------------------------------------


def _anthropic_tool_results(payload: dict, tid: str) -> list[dict]:
    return [
        b
        for m in payload["messages"]
        for b in m["content"]
        if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("tool_use_id") == tid
    ]


def test_translator_dedups_even_when_sanitize_was_bypassed() -> None:
    """The true last line: a duplicate injected AFTER construction (simulating
    the replace/deepcopy paths that never re-run sanitize) must still be stripped
    before the bytes hit the wire."""
    config = UnifiedConfig(
        model="claude-opus-4-8",
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[ToolCallContent(id="X", name="research_web", arguments={})],
            ),
            UnifiedMessage(
                role="tool",
                content=[
                    ToolResultContent(
                        tool_use_id="X", call_id="X", name="research_web",
                        content="the real result",
                    )
                ],
            ),
        ],
    )
    # __post_init__ already ran sanitize (kept tool_use + one result). Now mimic
    # a post-sanitize append (the live-loop / cache-hit shape) by adding a
    # duplicate tool message directly to the underlying list.
    config.messages._messages.append(
        UnifiedMessage(
            role="tool",
            content=[
                ToolResultContent(
                    tool_use_id="X", call_id="X", name="research_web",
                    content="the real result",
                )
            ],
        )
    )

    payload = AnthropicTranslator().to_anthropic(config, make_profile(model_name='m', wire_format='anthropic_chat'))
    assert len(_anthropic_tool_results(payload, "X")) == 1, (
        "translator must emit exactly one tool_result per id even when sanitize "
        "was bypassed — this is the last line before the Anthropic 400"
    )


def test_translator_preserves_distinct_results() -> None:
    config = UnifiedConfig(
        model="claude-opus-4-8",
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[
                    ToolCallContent(id="X", name="t", arguments={}),
                    ToolCallContent(id="Y", name="t", arguments={}),
                ],
            ),
            UnifiedMessage(
                role="tool",
                content=[
                    ToolResultContent(tool_use_id="X", call_id="X", name="t", content="rx"),
                    ToolResultContent(tool_use_id="Y", call_id="Y", name="t", content="ry"),
                ],
            ),
        ],
    )
    payload = AnthropicTranslator().to_anthropic(config, make_profile(model_name='m', wire_format='anthropic_chat'))
    assert len(_anthropic_tool_results(payload, "X")) == 1
    assert len(_anthropic_tool_results(payload, "Y")) == 1


def _windowed_pairing_ok(ml) -> bool:
    """Provider-faithful invariant: after the translator merges the consecutive
    tool/user run following an assistant, every tool_use must be answered there."""
    msgs = ml._messages

    def _is_asst(m) -> bool:
        r = getattr(m, "role", None)
        return r == "assistant" or getattr(r, "value", None) == "assistant"

    n = len(msgs)
    for i, m in enumerate(msgs):
        uses = [c.id for c in m.content if isinstance(c, ToolCallContent)]
        if not uses:
            continue
        acc: set = set()
        j = i + 1
        while j < n and not _is_asst(msgs[j]):
            acc |= {
                (c.tool_use_id or c.call_id)
                for c in msgs[j].content
                if isinstance(c, ToolResultContent)
            }
            j += 1
        if any(u not in acc for u in uses):
            return False
    return True


def test_sanitize_fixes_nonadjacent_duplicate_tool_uses_bcc588b6():
    """Conversation bcc588b6 (2nd incident): the assistant at position 13 carried
    SIX tool_uses, but the next tool message answered only THREE — the other
    three ids were re-emitted (adjacently paired) in LATER assistant turns. The
    old 'a result exists somewhere' check passed them straight to Anthropic →
    'tool_use ids were found without tool_result blocks' 400. Adjacency-aware
    sanitize must collapse it to a VALID payload with NO data loss."""

    def asst(*ids):
        return UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id=i, name="context_patch", arguments={}) for i in ids],
        )

    def tool(*ids):
        return UnifiedMessage(
            role="tool",
            content=[
                ToolResultContent(tool_use_id=i, call_id=i, name="context_patch", content=f"r-{i}")
                for i in ids
            ],
        )

    ml = MessageList(
        _messages=[
            asst("A", "B", "C", "D", "E", "F"),  # pos13 — 6 uses; D/E/F belong to later turns
            tool("A", "B", "C"),                  # pos14 — only 3 results
            asst("D"), tool("D"),                 # pos15/16
            asst("E", "F"), tool("E", "F"),       # pos17/18
        ]
    )
    ml.sanitize()

    assert _windowed_pairing_ok(ml), "every tool_use must be answered in its following tool-run"
    # The corrupted first message keeps ONLY its adjacently-paired uses.
    first_uses = sorted(c.id for c in ml._messages[0].content if isinstance(c, ToolCallContent))
    assert first_uses == ["A", "B", "C"]
    # No data lost: D, E, F survive via their later adjacent turns.
    all_uses = sorted(
        c.id for m in ml._messages for c in m.content if isinstance(c, ToolCallContent)
    )
    assert all_uses == ["A", "B", "C", "D", "E", "F"]
    # No orphan results either.
    all_results = sorted(
        (c.tool_use_id or c.call_id)
        for m in ml._messages
        for c in m.content
        if isinstance(c, ToolResultContent)
    )
    assert all_results == ["A", "B", "C", "D", "E", "F"]


def test_sanitize_drops_true_orphan_tool_use_no_result_anywhere():
    """A tool_use with NO result anywhere (delegated timeout) is a true orphan —
    dropped quietly, never a loud duplicate alarm."""
    ml = MessageList(
        _messages=[
            UnifiedMessage(role="assistant", content=[ToolCallContent(id="ORPH", name="t", arguments={})]),
            UnifiedMessage(role="user", content=[TextContent(text="continue")]),
        ]
    )
    ml.sanitize()
    assert _windowed_pairing_ok(ml)
    assert all(
        not isinstance(c, ToolCallContent)
        for m in ml._messages
        for c in m.content
    ), "the orphan tool_use must be gone"
