"""Anthropic `search_result` wire invariants — the two rules that compound.

  1. A tool_result carrying search_result blocks may carry nothing else
     (live 400, 2026-08-08) — hence the metadata wrapper.
  2. Citations must be enabled on ALL search_result blocks or none
     ("A mixture of enabling and disabling is not supported" — live 400 on
     2026-08-21, request 74ef776d: knowledge_search passages were
     citations-enabled and the metadata wrapper rule 1 forced was not).

Every citable tool result hits BOTH rules at once, so these tests assert the
final wire bytes of every producer plus the translator backstop.
"""

from __future__ import annotations

import json

from matrx_ai.config import (
    SearchResultContent,
    TextContent,
    UnifiedConfig,
    UnifiedMessage,
)
from matrx_ai.config.citations import (
    citable_wire_blocks_from_output,
    enforce_search_result_citation_uniformity,
)
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile

MODEL = "claude-opus-4-5-20250929"


def _profile():
    return make_profile(
        model_name=MODEL,
        wire_format="anthropic_chat",
        capabilities={
            "input": ["text"],
            "output": ["text"],
            "features": ["function_calling", "structured_output"],
            "interaction": "turn",
        },
    )


def _assert_wire_valid(blocks: list[dict]) -> None:
    """Both invariants, exactly as Anthropic enforces them."""
    assert blocks, "expected search_result blocks on the wire"
    assert all(b["type"] == "search_result" for b in blocks), (
        f"invariant 1 violated — mixed block types: {[b['type'] for b in blocks]}"
    )
    postures = {bool((b.get("citations") or {}).get("enabled")) for b in blocks}
    assert len(postures) == 1, (
        "invariant 2 violated — mixture of enabled and disabled citations: "
        f"{[b.get('citations') for b in blocks]}"
    )


def _citable_tool_result() -> ToolResultContent:
    """What a live citable search tool actually hands the wire: passages +
    the trailing metadata TextContent."""
    return ToolResultContent(
        tool_use_id="toolu_live",
        name="knowledge_search",
        content=[
            SearchResultContent(
                texts=["Passage one."],
                title="Handbook — page 3",
                file_id="11111111-1111-1111-1111-111111111111",
                page=3,
            ),
            SearchResultContent(
                texts=["Passage two."],
                title="Handbook — page 9",
                file_id="11111111-1111-1111-1111-111111111111",
                page=9,
            ),
            TextContent(text=json.dumps({"query": "vacation policy", "total_candidates": 2})),
        ],
    )


def test_live_citable_tool_result_is_uniformly_citable():
    """The exact shape that 400'd in production."""
    blocks = _citable_tool_result().to_anthropic()["content"]

    _assert_wire_valid(blocks)
    # And the uniform posture is ENABLED — degrading to all-off would silently
    # destroy the citability the citable-tool path exists to provide.
    assert all(b["citations"] == {"enabled": True} for b in blocks)
    # The metadata JSON still reaches the model, wrapped.
    metadata = [b for b in blocks if b["title"] == "Search metadata"]
    assert len(metadata) == 1
    assert "vacation policy" in metadata[0]["content"][0]["text"]


def test_db_rebuilt_citable_tool_result_is_uniformly_citable():
    """Resend path: provider_content is never persisted, so the wire blocks are
    rebuilt from the stored JSON output — same two invariants."""
    stored = {
        "query": "vacation policy",
        "hits": [
            {
                "snippet": "Passage one.",
                "source_kind": "cld_file",
                "source_id": "11111111-1111-1111-1111-111111111111",
                "page_numbers": [3],
                "metadata": {"title": "Handbook"},
            }
        ],
        "total_candidates": 1,
    }
    blocks = ToolResultContent(
        tool_use_id="toolu_resend", name="knowledge_search", content=stored
    ).to_anthropic()["content"]

    _assert_wire_valid(blocks)
    assert all(b["citations"] == {"enabled": True} for b in blocks)
    assert citable_wire_blocks_from_output("knowledge_search", stored) is not None


def test_translator_repairs_a_rogue_non_uniform_producer():
    """Backstop: a future producer emitting a non-citable search_result block
    must not be able to 400 the whole request."""
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_x",
                    "content": [
                        {
                            "type": "search_result",
                            "source": "matrx://file/abc",
                            "title": "Passage",
                            "content": [{"type": "text", "text": "cite me"}],
                            "citations": {"enabled": True},
                        },
                        {
                            "type": "search_result",
                            "source": "matrx://metadata",
                            "title": "Search metadata",
                            "content": [{"type": "text", "text": "{}"}],
                        },
                    ],
                }
            ],
        }
    ]

    assert enforce_search_result_citation_uniformity(messages) == 1
    _assert_wire_valid(messages[0]["content"][0]["content"])
    # Idempotent: a second pass has nothing left to correct.
    assert enforce_search_result_citation_uniformity(messages) == 0


def test_uniformly_disabled_request_is_left_alone():
    """An all-off request (machine runs strip citations) is already uniform —
    the enforcer must not re-enable anything."""
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_y",
                    "content": [
                        {
                            "type": "search_result",
                            "source": "matrx://file/abc",
                            "title": "Passage",
                            "content": [{"type": "text", "text": "no citations"}],
                        }
                    ],
                }
            ],
        }
    ]
    assert enforce_search_result_citation_uniformity(messages) == 0
    assert "citations" not in messages[0]["content"][0]["content"][0]


def _request_with_citable_result(**config_kwargs) -> dict:
    config = UnifiedConfig(
        model=MODEL,
        messages=[
            UnifiedMessage(role="user", content=[TextContent(text="what is the policy?")]),
            UnifiedMessage(
                role="assistant",
                content=[
                    ToolCallContent(
                        id="toolu_live",
                        name="knowledge_search",
                        arguments={"query": "vacation policy"},
                    )
                ],
            ),
            UnifiedMessage(role="tool", content=[_citable_tool_result()]),
        ],
        **config_kwargs,
    )
    return AnthropicTranslator().to_anthropic(config, _profile())


def test_full_anthropic_request_is_wire_valid():
    request = _request_with_citable_result()
    tool_results = [
        b
        for m in request["messages"]
        for b in m["content"]
        if isinstance(b, dict) and b.get("type") == "tool_result"
    ]
    assert tool_results, "tool result must reach the wire"
    _assert_wire_valid(tool_results[0]["content"])


def test_machine_run_strips_citations_from_every_search_result_block():
    """response_format ⇒ citations off. Uniformly off is legal; a partial strip
    would be the same 400 in the other direction."""
    request = _request_with_citable_result(
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "Answer",
                "schema": {
                    "type": "object",
                    "properties": {"answer": {"type": "string"}},
                    "required": ["answer"],
                    "additionalProperties": False,
                },
            },
        }
    )
    blocks = [
        b
        for m in request["messages"]
        for tr in m["content"]
        if isinstance(tr, dict) and tr.get("type") == "tool_result"
        for b in tr["content"]
    ]
    _assert_wire_valid(blocks)
    assert all("citations" not in b for b in blocks)
