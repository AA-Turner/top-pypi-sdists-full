"""Per-family envelope parity fixtures — every Shape-backed render block.

One end-to-end case per ``BLOCK_KIND_MAP`` family (mermaid, since LEGACY-5):
realistic inline wire source -> ``StreamBlockProcessor`` -> finalize ->
the stamped ``metadata.__ir`` envelope must:

* carry the canonical kind slug for the family;
* hold a ``root.value`` that VALIDATES against the kind's LIVE
  ``emitted_json_schema`` (snapshotted by ``fixtures/refresh_kind_schemas.py``
  — real rows, never hand-written);
* fingerprint the exact emitted ``content`` string;
* pass the FE inbound gate shape (``sanitizeInboundEnvelopeMetadata``).

Cross-language scope, stated honestly: these assertions prove PYTHON
self-consistency (envelope fingerprint == ``fingerprint_text(content)``).
Byte-parity of ``fingerprint_text`` itself with the TS kernel is a SEPARATE,
transitive guarantee — ``test_fingerprint_parity.py`` pins the algorithm
against the TS-generated shared vectors, which do NOT include these family
content strings. If the algorithms ever diverged on an input class the vectors
miss, this suite alone would not catch it; extend the TS-generated vector set
(never by hand) to close that class.

A family whose sample fails to stamp is parser/kind CONTRACT DRIFT — the
exact defect class this suite exists to catch. Fix the adapter in
``processing/blocks/envelope.py``; never loosen the assertion.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from matrx_ai.processing.blocks import envelope as envelope_mod
from matrx_ai.processing.blocks.envelope import (
    BLOCK_KIND_MAP,
    IR_ENGINE,
    IR_ENVELOPE_KEY,
    IR_VERSION,
    KIND_KEY,
    NON_ENVELOPE_BLOCK_TYPES,
    envelope_for_block,
    reset_kind_catalog_snapshot,
)
from matrx_ai.processing.blocks.fingerprint import fingerprint_text
from matrx_ai.processing.blocks.stream_processor import StreamBlockProcessor
from matrx_graph.executor.schema_validation import validate_instance

_FIXTURES = Path(__file__).parent / "fixtures"
with (_FIXTURES / "kind_schemas_sample.json").open(encoding="utf-8") as f:
    _KIND_SCHEMAS: dict[str, dict[str, Any]] = json.load(f)["schemas"]


# Each mapped family gets a realistic inline wire source, written in the exact
# syntax agents emit today (parsers unchanged — law).
_INLINE_SOURCES: dict[str, str] = {
    "mermaid": (
        "```mermaid\n"
        "graph TD\n"
        "    A[Client] -->|HTTPS| B[API Gateway]\n"
        "    B --> C[Auth Service]\n"
        "    B --> D[Streaming Service]\n"
        "```\n"
    ),
}

# block type -> where its realistic sample comes from ("corpus" or inline).
# The 18 pre-kind families left with their readers in legacy-shapes step 5 (LEGACY-5);
# a kind now arrives as a ``__kind`` instance (the ``kind`` block, covered by
# test_registered_kinds_are_kind_blocks.py).
_FAMILY_SOURCES: dict[str, str] = dict(_INLINE_SOURCES)

_ENVELOPE_KEYS = {"v", "engine", "fingerprint", "root", "nodeIndex"}
_ROOT_KEYS = {"role", "kind", "kindState", "discriminator", "path", "status", "value", "residue"}


@pytest.fixture(autouse=True)
def _mock_kind_catalog(monkeypatch: pytest.MonkeyPatch):
    """Seed the sync snapshot with the REAL live schemas; no DB in tests."""
    reset_kind_catalog_snapshot()
    monkeypatch.setattr(envelope_mod, "_schema_snapshot", dict(_KIND_SCHEMAS))
    yield
    reset_kind_catalog_snapshot()


def test_every_mapped_family_has_a_fixture_and_a_live_schema() -> None:
    """The suite can never silently cover a subset of BLOCK_KIND_MAP."""
    assert set(_FAMILY_SOURCES) == set(BLOCK_KIND_MAP), (
        "BLOCK_KIND_MAP and the family fixture table drifted — add a realistic "
        "source for every mapped block type."
    )
    missing = [slug for slug in BLOCK_KIND_MAP.values() if slug not in _KIND_SCHEMAS]
    assert not missing, (
        f"kind_schemas_sample.json is missing live schemas for {missing} — rerun "
        "fixtures/refresh_kind_schemas.py"
    )


def test_every_block_type_is_classified_mapped_or_reviewed_bypass() -> None:
    """No silent envelope bypasses: every emittable type is in exactly one table."""
    from matrx_ai.processing.blocks.block_detector import (
        ATTRIBUTE_XML_BLOCKS,
        SPECIAL_CODE_LANGUAGES,
        SPLITTER_ONLY_BLOCK_TYPES,
        XML_TAG_BLOCKS,
    )
    from matrx_ai.processing.blocks.block_registry import BlockRegistry

    emittable = (
        set(BlockRegistry().type_keys())
        | set(XML_TAG_BLOCKS)
        | set(SPECIAL_CODE_LANGUAGES)
        | set(ATTRIBUTE_XML_BLOCKS)
        | set(SPLITTER_ONLY_BLOCK_TYPES)
        | {"matrx"}
    )
    mapped = set(BLOCK_KIND_MAP)
    bypassed = set(NON_ENVELOPE_BLOCK_TYPES)
    assert not (mapped & bypassed), f"types in BOTH tables: {sorted(mapped & bypassed)}"
    unclassified = emittable - mapped - bypassed
    assert not unclassified, (
        f"UNCLASSIFIED envelope bypass: {sorted(unclassified)} — map each to a "
        "registered kind in BLOCK_KIND_MAP or record the reviewed reason in "
        "NON_ENVELOPE_BLOCK_TYPES (processing/blocks/envelope.py)."
    )


def test_unclassified_block_type_screams_and_does_not_stamp(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level("ERROR", logger="matrx_ai.processing.blocks.envelope"):
        assert envelope_for_block("made_up_type", {"x": 1}, source_text="x") is None
    assert any("UNCLASSIFIED" in r.message for r in caplog.records)


@pytest.mark.parametrize("block_type", sorted(_FAMILY_SOURCES), ids=str)
def test_family_emits_canonical_envelope(block_type: str) -> None:
    kind = BLOCK_KIND_MAP[block_type]
    schema = _KIND_SCHEMAS[kind]

    processor = StreamBlockProcessor()
    processor.process_chunk(_FAMILY_SOURCES[block_type])
    events = processor.finalize()

    blocks = [e for e in events if e.type == block_type]
    assert blocks, (
        f"detector never produced a '{block_type}' block from its own sample — "
        f"got types {sorted({e.type for e in events})}"
    )
    stamped = [b for b in blocks if IR_ENVELOPE_KEY in (b.metadata or {})]
    assert stamped, (
        f"'{block_type}' completed WITHOUT a __ir envelope — parser/kind contract "
        f"drift against '{kind}' (see the loud envelope log for the cause)"
    )

    block = stamped[-1]
    ir = block.metadata[IR_ENVELOPE_KEY]

    # FE inbound gate shape (sanitizeInboundEnvelopeMetadata).
    assert set(ir) <= _ENVELOPE_KEYS and {"v", "engine", "fingerprint", "root"} <= set(ir)
    assert ir["v"] == IR_VERSION
    assert ir["engine"] == IR_ENGINE
    assert set(ir["root"]) == _ROOT_KEYS
    assert ir["root"]["role"] == "structured"
    assert ir["root"]["kind"] == kind
    assert ir["root"]["kindState"] == "resolved"
    assert ir["root"]["status"] == "complete"
    assert ir["root"]["path"] == []

    # The reuse key: fingerprint of the EXACT emitted content string.
    assert block.content
    assert ir["fingerprint"] == fingerprint_text(block.content)

    # value = schema fields + __kind, and it validates against the LIVE schema.
    value = dict(ir["root"]["value"])
    assert value.pop(KIND_KEY) == kind
    errors = validate_instance(schema, value)
    assert not errors, f"'{block_type}' envelope value fails kind '{kind}' schema: {errors[:5]}"


# ---------------------------------------------------------------------------
# Open objects (`additionalProperties: true`) — the collapse-suppression bug.
# ---------------------------------------------------------------------------


def test_open_object_keys_stay_in_value_and_do_not_suppress_the_envelope(monkeypatch: pytest.MonkeyPatch) -> None:
    """A node that DECLARES it accepts unnamed keys knows those keys.

    Routing them to residue empties the node, which trips the vocabulary-collapse
    guard and suppresses the WHOLE envelope. That is what silently killed every
    `item_presentation` stamp: its `additionalDetails` is
    `additionalProperties: true`, so every caller-supplied detail counted as
    unknown. Measured against the LIVE schema, never a hand-written one.
    """
    # The partition is generic; item_presentation is the live schema with an open node.
    # Its legacy block type left BLOCK_KIND_MAP in LEGACY-5, so the test maps it here.
    monkeypatch.setitem(envelope_mod.BLOCK_KIND_MAP, "item_presentation", "item_presentation")
    schema = _KIND_SCHEMAS["item_presentation"]
    additional = schema["properties"]["additionalDetails"]
    assert additional.get("additionalProperties") is True, (
        "fixture drifted — this test only means something while additionalDetails "
        "is an OPEN object in the live schema"
    )

    envelope = envelope_for_block(
        "item_presentation",
        {"type": "agent", "id": "agent-1", "additionalDetails": {"label": "Helper"}},
        source_text='{"item_presentation": {"type": "agent"}}',
    )

    assert envelope is not None, (
        "no envelope stamped — an open object's keys were treated as unknown, "
        "collapsing the node (the exact suppression this test exists to stop)"
    )
    details = envelope["root"]["value"]["additionalDetails"]
    assert details == {"label": "Helper"}, (
        f"open-object keys did not survive into value: {details!r}"
    )
    # ...and they are NOT ALSO duplicated into residue (that would double-carry).
    node = envelope.get("nodeIndex", {}).get("additionalDetails")
    extra = (node or {}).get("residue", {}).get("extra")
    assert not extra, f"open-object keys leaked into residue.extra as well: {extra!r}"


def test_closed_object_still_routes_unknown_keys_to_residue(monkeypatch: pytest.MonkeyPatch) -> None:
    """The open-object rule must not weaken the CLOSED case (law 3)."""
    monkeypatch.setitem(envelope_mod.BLOCK_KIND_MAP, "item_presentation", "item_presentation")
    envelope = envelope_for_block(
        "item_presentation",
        {"type": "agent", "id": "agent-1", "not_a_schema_field": "x"},
        source_text='{"item_presentation": {"type": "agent"}}',
    )
    assert envelope is not None
    assert "not_a_schema_field" not in envelope["root"]["value"]
    assert envelope["root"]["residue"]["extra"] == {"not_a_schema_field": "x"}
