"""Pydantic twins for the four dominant content blocks (Phase 1b.2).

Shadowed, not swapped. Retirement Ledger row 4.

WHY THESE FOUR FIRST. `chat.message.content` holds 136,730 blocks and these four
are 99.15% of them — text 82,908, thinking 24,571, tool_call 14,768,
tool_result 13,322. They are also already the four routed through the ONE
deserializer (`unified_content.reconstruct_content`) rather than `_filter`, so
they have a single well-defined rebuild path to be faithful to. Full census:
FIELD_TRUTH.md §4b.

🚨 THE THIRD DECLARED-TYPE LIE, AND THE WORST ONE BY VOLUME.
`ToolResultContent.content` is declared `list[dict[str, Any]]`. The ONE
deserializer assigns a **str** to it on EVERY tool_result rebuild —
`content = block.get("content", "")`, and the Anthropic empty-error safeguard
synthesises an f-string. A literal port of that annotation rejects the pointer
block (99.7% of production) AND the error path — i.e. every tool result in the
system, 13,338 blocks. Construction sites pass str, list AND dict, so the honest
type is `Any` until someone decides what it should be. Verified by execution,
not by reading.

That makes it three for three: `UnifiedMessage.timestamp`, `UnifiedResponse.raw_response`,
and now this. **A declared type in this package is a hypothesis, never an input.**

WHAT THE CORPUS ALSO SAID:

  * `thinking` stores REAL EXPLICIT JSON NULLS — `signature` null ×243,
    `signature_encoding` null ×1,992. Every earlier shape had zero, which is why
    FIELD_TRUTH §2's "absence, never null" now carries a scope warning. These two
    fields must accept a null that is actually on the wire, not merely be optional.
  * `text.text` is POLYMORPHIC — string ×82,934, array ×1. One row, but a
    `str`-only annotation raises on it and it is a real stored message.
  * `thinking.provider`'s 9-member Literal is SAFE — all 8 observed values are
    inside it. A declared type that is actually correct; asserted so a 10th
    provider fails loudly here instead of at flip.
  * `citations` (text) and `call_id` (tool_call) are STORED keys with no matching
    field — the deserializer folds them into `metadata` / `id`. Not modelled here;
    they belong to the deserializer's contract, not the block's.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# extra="forbid" matches the dataclasses, which raise TypeError on an unknown
# keyword. reconstruct_content builds all four with explicit kwargs, so nothing
# splats stored data in — the one site that splats (executor.py:1045) already
# hits that TypeError today.
_BLOCK = ConfigDict(extra="forbid", validate_assignment=False, arbitrary_types_allowed=True)


class TextContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["text"] = "text"
    # str ×82,934, list ×1. The array is one real stored message; `str` alone
    # raises on it.
    text: str | list[Any] = ""
    id: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class ThinkingContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["thinking"] = "thinking"
    text: str = ""
    id: str = ""
    summary: list[dict[str, Any]] = Field(default_factory=list)
    # Verified against the corpus: 8 distinct values, all inside this Literal.
    provider: (
        Literal[
            "openai", "anthropic", "google", "cerebras", "moonshot",
            "together", "groq", "xai", "generic_openai",
        ]
        | None
    ) = None
    # bytes is the IN-MEMORY form (Gemini's decoded thoughtSignature); JSON only
    # ever carries str or an explicit null.
    signature: str | bytes | None = None
    signature_encoding: Literal["base64"] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ToolCallContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["tool_call", "function_call"] = "tool_call"
    id: str = ""
    name: str = ""
    arguments: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ToolResultContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["tool_result"] = "tool_result"
    tool_use_id: str = ""
    call_id: str = ""
    name: str = ""
    # 🚨 DELIBERATELY Any — see the module docstring. Declared list[dict] in the
    # dataclass; the deserializer always assigns str; construction sites pass
    # str, list and dict. Narrowing this is its own decision with its own
    # evidence, and it is NOT a cleanup.
    content: Any = Field(default_factory=list)
    is_error: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)
    output_chars: int = 0
    output_preview: dict[str, Any] | None = None
    approved_max_chars: int | None = None
