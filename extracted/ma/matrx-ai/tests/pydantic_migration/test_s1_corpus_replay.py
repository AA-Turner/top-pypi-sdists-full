"""S1 — corpus green. The twins meet every shape production actually stores.

Phase 1b.2. S0 built nine twins; every one was UNREFERENCED, which proves
nothing. The Retirement Ledger's own rule 2 is that retiring beats starting, and
five open rows all sitting at S0 is the accumulate-and-never-advance failure the
ledger exists to prevent. This is the stage that advances them.

WHAT S1 MEANS HERE (CUTOVER.md §3 stage key): "shadow (corpus green)". The live
soak is S2 and needs production traffic this environment cannot see. Corpus
green is achievable now and is the precondition for it.

THE METHOD. For all 60 distinct structural cases in
``fixtures/content_block_shapes.json`` — every (type, kind, key-set,
key-JSON-type) combination in chat.message.content — synthesise a block, push it
through the ONE deserializer, and require the pydantic twin to accept the
dataclass the deserializer produced, field for field. A twin that cannot hold
what the deserializer emits cannot be flipped to, whatever its unit tests say.

WHY SYNTHETIC VALUES AND NOT REAL ONES. The fixture carries key names and JSON
type names, never a value — CORPUS.md §7 forbids committing an unredacted export
of customer conversations, and structural parity does not need values. What is
being tested is that every SHAPE round-trips, and the shape is exactly what the
fixture preserves.
"""

from __future__ import annotations

import dataclasses
import json
import pathlib
from typing import Any

import pytest

from matrx_ai.config.media_config import reconstruct_media_content
from matrx_ai.config.models.media import (
    AudioContentModel,
    DocumentContentModel,
    ImageContentModel,
    VideoContentModel,
    YouTubeVideoContentModel,
)
from matrx_ai.config.models.content import (
    TextContentModel,
    ThinkingContentModel,
    ToolCallContentModel,
    ToolResultContentModel,
)
from matrx_ai.config.unified_content import reconstruct_content

FIXTURE = json.loads(
    (pathlib.Path(__file__).parent / "fixtures" / "content_block_shapes.json").read_text()
)
CASES = FIXTURE["cases"]

TWIN_BY_CLASS = {
    "TextContent": TextContentModel,
    "ThinkingContent": ThinkingContentModel,
    "ToolCallContent": ToolCallContentModel,
    "ToolResultContent": ToolResultContentModel,
    "ImageContent": ImageContentModel,
    "AudioContent": AudioContentModel,
    "VideoContent": VideoContentModel,
    "DocumentContent": DocumentContentModel,
    "YouTubeVideoContent": YouTubeVideoContentModel,
}

# Block types with no twin YET. Listed explicitly, never skipped silently — a
# NEW unmodelled type must show up as a failure, not as a quiet pass.
NOT_YET_MODELLED = {
    "input_notes", "input_table", "input_webpage", "input_task", "input_workbook",
    "web_search",   # WebSearchCallContent — structured-input/extra family, Phase 1b.2 tail
    "quiz",         # aidream AD203 — a frontend EDITOR block, decision-gated
    "image",        # aidream AD203 — one stray pre-unification discriminator
}


def _synthesise(case: dict[str, Any]) -> dict[str, Any]:
    """Build a block with the case's exact keys and JSON types."""
    block: dict[str, Any] = {}
    for key, json_type in case["type_map"].items():
        if key == "type":
            block[key] = case["block_type"]
        elif key == "kind":
            block[key] = case["kind"]
        elif key == "provider":
            block[key] = "anthropic"          # a real member of the Literal
        elif key == "signature_encoding":
            block[key] = None if json_type == "null" else "base64"
        elif key == "signature":
            # When signature_encoding is "base64" the deserializer DECODES this,
            # so the placeholder has to be real base64 or the decode raises.
            # (Noted while writing this: a malformed signature on a row whose
            # encoding says base64 would take the whole rebuild down. Not
            # observed in production — every stored signature decodes — so it is
            # recorded here rather than filed.)
            block[key] = None if json_type == "null" else "eA=="
        elif json_type == "null":
            block[key] = None
        elif json_type == "string":
            block[key] = "x"
        elif json_type == "number":
            block[key] = 1
        elif json_type == "boolean":
            block[key] = True
        elif json_type == "object":
            block[key] = {}
        elif json_type == "array":
            block[key] = []
        else:
            raise AssertionError(f"unhandled JSON type {json_type!r} for {key!r}")
    return block


def _ids(case: dict[str, Any]) -> str:
    k = f".{case['kind']}" if case["kind"] else ""
    return f"{case['block_type']}{k}[{len(case['type_map'])}k×{case['blocks']}]"


@pytest.mark.parametrize("case", CASES, ids=_ids)
def test_every_production_shape_round_trips_into_its_twin(case):
    if case["block_type"] in NOT_YET_MODELLED:
        pytest.skip(f"{case['block_type']} has no twin yet — tracked, not silent")

    block = _synthesise(case)
    rebuilt = (
        reconstruct_media_content(block)
        if case["block_type"] == "media"
        else reconstruct_content(block)
    )
    assert rebuilt is not None, "the ONE deserializer returned nothing for a real stored shape"

    twin_cls = TWIN_BY_CLASS.get(type(rebuilt).__name__)
    assert twin_cls is not None, (
        f"the deserializer produced {type(rebuilt).__name__}, which has no twin"
    )

    values = {f.name: getattr(rebuilt, f.name) for f in dataclasses.fields(rebuilt)}
    twin = twin_cls(**values)

    for name, expected in values.items():
        assert getattr(twin, name) == expected, f"{twin_cls.__name__}.{name}"
        assert type(getattr(twin, name)) is type(expected), (
            f"{twin_cls.__name__}.{name} changed TYPE: "
            f"{type(expected).__name__} -> {type(getattr(twin, name)).__name__}"
        )


def test_the_fixture_covers_what_it_claims():
    assert FIXTURE["_distinct_cases"] == len(CASES) == 60
    assert FIXTURE["_total_blocks"] == sum(c["blocks"] for c in CASES)
    # No values, only type names — the property that makes this committable.
    allowed = {"string", "number", "boolean", "object", "array", "null"}
    for case in CASES:
        assert set(case["type_map"].values()) <= allowed


def test_the_modelled_share_of_production_is_stated_not_assumed():
    """A pass over 60 cases means nothing without knowing how much traffic they
    carry. Nine twins cover the overwhelming majority; the remainder is the
    tail plus AD203."""
    total = sum(c["blocks"] for c in CASES)
    covered = sum(c["blocks"] for c in CASES if c["block_type"] not in NOT_YET_MODELLED)
    share = covered / total
    assert share > 0.999, f"twin coverage fell to {share:.4%} of stored blocks"


def test_unmodelled_types_are_exactly_the_ones_we_named():
    """If a new block type appears in production, it lands here rather than
    slipping through as a skip nobody reads."""
    seen = {c["block_type"] for c in CASES}
    modelled = {"text", "thinking", "tool_call", "tool_result", "media"}
    assert seen - modelled == NOT_YET_MODELLED
