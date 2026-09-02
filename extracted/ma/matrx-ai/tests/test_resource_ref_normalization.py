"""Regression guard for the 2026-06-15 note-attach loop-to-death incident.

A user attached a note via the smart-input picker. The frontend shipped the
*entire* note object inside `note_ids` (`[{"id": ..., "content": ...}]`) instead
of a bare id list. The notes resolver fed each element straight into
`SELECT * FROM notes WHERE id = $1`, so the whole dict was bound as the UUID and
asyncpg raised `invalid input syntax for type uuid` — a trivial context-injection
step took down the entire request (0-char assistant message, last_request_status
= failed).

The fix introduced a single normalization primitive (`resource_ref`) that every
list-of-resources input uses. It accepts three shapes and reduces each to a
canonical reference:

  - a bare id string                     -> reference (fetch live)
  - an object carrying an id             -> reference (extract id, fetch live)
  - an object with mode="snapshot"+body  -> snapshot (render inline, no DB)

These tests pin every branch so the class of failure stays extinct.
"""

from __future__ import annotations

from matrx_ai.config.resource_ref import (
    ResourceRef,
    normalize_resource_ref,
    normalize_resource_refs,
)


def test_bare_string_is_reference() -> None:
    ref = normalize_resource_ref("0dbd9901-2128-4793-8bf8-b24635701987")
    assert ref == ResourceRef(id="0dbd9901-2128-4793-8bf8-b24635701987", mode="reference")


def test_full_object_extracts_id_as_reference() -> None:
    """The exact shape that caused the incident: a whole note object."""
    entry = {
        "id": "0dbd9901-2128-4793-8bf8-b24635701987",
        "tags": [],
        "label": "1. AGENT SERVICE & MCP",
        "content": "# AGENT SERVICE & MCP\n\n...",
    }
    ref = normalize_resource_ref(entry)
    assert ref is not None
    assert ref.id == "0dbd9901-2128-4793-8bf8-b24635701987"
    assert ref.mode == "reference"  # default — fetch the live note, do NOT snapshot
    assert ref.has_inline_content is True


def test_explicit_snapshot_mode_is_value_attach() -> None:
    entry = {"mode": "snapshot", "id": "x", "content": "frozen body", "label": "L"}
    ref = normalize_resource_ref(entry)
    assert ref is not None
    assert ref.mode == "snapshot"
    assert ref.inline["content"] == "frozen body"


def test_snapshot_without_id_but_with_content() -> None:
    ref = normalize_resource_ref({"mode": "snapshot", "content": "inline only"})
    assert ref is not None
    assert ref.id is None
    assert ref.mode == "snapshot"
    assert ref.has_inline_content is True


def test_object_without_id_or_content_is_dropped() -> None:
    assert normalize_resource_ref({"tags": []}) is None


def test_object_without_id_but_with_content_auto_snapshots() -> None:
    ref = normalize_resource_ref({"content": "just text", "label": "L"})
    assert ref is not None
    assert ref.id is None
    assert ref.mode == "snapshot"


def test_alternate_id_keys() -> None:
    assert normalize_resource_ref({"note_id": "abc"}).id == "abc"
    assert normalize_resource_ref({"task_id": "def"}).id == "def"


def test_empty_and_blank_entries_drop() -> None:
    assert normalize_resource_ref("") is None
    assert normalize_resource_ref("   ") is None
    assert normalize_resource_ref(None) is None


def test_normalize_list_mixed_and_drops_garbage() -> None:
    raw = [
        "id-1",
        {"id": "id-2", "label": "x"},
        {"mode": "snapshot", "content": "c"},
        {"tags": []},  # unresolvable — dropped
    ]
    refs = normalize_resource_refs(raw)
    assert [r.id for r in refs] == ["id-1", "id-2", None]
    assert [r.mode for r in refs] == ["reference", "reference", "snapshot"]


def test_normalize_none_and_empty_lists() -> None:
    assert normalize_resource_refs(None) == []
    assert normalize_resource_refs([]) == []
