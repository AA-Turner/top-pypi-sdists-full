"""``__kind`` marker reduction — the block-shape → wire-shape converter.

THE BUG THESE PIN (2026-08-16): the reduction used to strip only the ROOT
marker. A producer bound to a kind emits the ``injectKind: true`` block export,
which carries a marker on every nested kind object, while the wire schema every
Python validator reads (``emitted_json_schema``) is ``__kind``-free and
``additionalProperties: false`` at every level. The result was that a slot
could not declare its own kind: every CORRECT run became a permanent false
failure. Three live producers were affected (``episode_title_options``,
``media_chapters``, ``video_transcript_research``).

A root-only implementation fails `test_nested_markers_are_removed`. A blind
recursive delete fails `test_marker_the_schema_declares_is_kept`. Both halves
are load-bearing.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.content_ir.markers import strip_kind_markers
from matrx_graph.contract_kinds import check_schema
from matrx_graph.executor.schema_validation import validate_instance

# The real ``episode_title_options`` wire schema, trimmed to what matters: a
# root object whose ``options`` array items are a closed $def with NO __kind.
WIRE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "$defs": {
        "episode_title_option": {
            "type": "object",
            "required": ["title"],
            "properties": {"title": {"type": "string"}, "subtitle": {"type": "string"}},
            "additionalProperties": False,
        }
    },
    "required": ["options"],
    "properties": {
        "working_title": {"type": "string"},
        "options": {"type": "array", "items": {"$ref": "#/$defs/episode_title_option"}},
    },
    "additionalProperties": False,
}

# What the producing agent actually emits (the block export).
BLOCK_ARTIFACT: dict[str, Any] = {
    "__kind": "episode_title_options",
    "working_title": "Old",
    "options": [
        {"__kind": "episode_title_option", "title": "A", "subtitle": "s"},
        {"__kind": "episode_title_option", "title": "B", "subtitle": ""},
    ],
}


def test_nested_markers_are_removed() -> None:
    """A root-only strip leaves the nested markers and the artifact fails."""
    root_only = {k: v for k, v in BLOCK_ARTIFACT.items() if k != "__kind"}
    assert validate_instance(WIRE_SCHEMA, root_only), "regression guard: root-only must fail"

    reduced = strip_kind_markers(BLOCK_ARTIFACT, WIRE_SCHEMA)
    assert validate_instance(WIRE_SCHEMA, reduced) == []
    assert all("__kind" not in option for option in reduced["options"])


def test_marker_the_schema_declares_is_kept() -> None:
    """Some python-owned kinds declare (and REQUIRE) ``__kind`` for real.
    Blind deletion turns those into the mirror-image false failure."""
    schema: dict[str, Any] = {
        "type": "object",
        "required": ["__kind", "title"],
        "properties": {
            "__kind": {"type": "string", "const": "video_transcript_research"},
            "title": {"type": "string"},
            "usage": {
                "type": "object",
                "properties": {"model": {"type": "string"}},
                "additionalProperties": False,
            },
        },
        "additionalProperties": False,
    }
    artifact = {
        "__kind": "video_transcript_research",
        "title": "t",
        # Nested marker the schema does NOT declare — must still go.
        "usage": {"__kind": "transcript_usage", "model": "m"},
    }
    reduced = strip_kind_markers(artifact, schema)
    assert reduced["__kind"] == "video_transcript_research"
    assert "__kind" not in reduced["usage"]
    assert validate_instance(schema, reduced) == []


def test_schema_free_reduction_removes_every_marker() -> None:
    reduced = strip_kind_markers(BLOCK_ARTIFACT)
    assert "__kind" not in reduced
    assert all("__kind" not in option for option in reduced["options"])


def test_reduction_is_idempotent_and_pure() -> None:
    before = repr(BLOCK_ARTIFACT)
    once = strip_kind_markers(BLOCK_ARTIFACT, WIRE_SCHEMA)
    assert strip_kind_markers(once, WIRE_SCHEMA) == once
    assert repr(BLOCK_ARTIFACT) == before, "input must never be mutated"


def test_recursive_root_ref_resolves() -> None:
    """``$ref: "#"`` is the self-reference form the kind exporter emits."""
    schema: dict[str, Any] = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "child": {"$ref": "#"}},
        "additionalProperties": False,
    }
    artifact = {"__kind": "node", "name": "a", "child": {"__kind": "node", "name": "b"}}
    reduced = strip_kind_markers(artifact, schema)
    assert reduced == {"name": "a", "child": {"name": "b"}}
    assert validate_instance(schema, reduced) == []


def test_check_schema_reduces_before_validating() -> None:
    """The chokepoint does the reduction itself — callers hand it the raw
    producer artifact and must not pre-strip."""
    verdict = check_schema(BLOCK_ARTIFACT, WIRE_SCHEMA)
    assert verdict.checked is True
    assert verdict.errors == []


def test_non_containers_pass_through() -> None:
    for value in ("text", 7, True, None, []):
        assert strip_kind_markers(value, WIRE_SCHEMA) == value
