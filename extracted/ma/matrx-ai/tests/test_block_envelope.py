"""Canonical ``metadata.__ir`` envelope emission — the ``py-block-detector`` engine.

Guards the wire contract with matrx-frontend
(``/Users/armanisadeghi/code/common-docs/systems/content-ir-system/PYTHON_ENVELOPE_CONTRACT.md``):

* the fingerprint is byte-identical to the TypeScript implementation — asserted
  against the SHARED, TS-generated vectors, never a mock;
* the envelope's shape matches ``CanonicalBlockIR`` exactly (the FE gate
  ``sanitizeInboundEnvelopeMetadata`` strips anything malformed and screams);
* a streaming/partial block NEVER carries an envelope (a premature stamp poisons
  the FE's fingerprint-keyed envelope cache);
* an unregistered kind and a schema-invalid value both produce NO envelope.

The kind CATALOG is mocked (no DB in unit tests) but the SCHEMAS are the real
``emitted_json_schema`` rows, snapshotted in ``fixtures/kind_schemas_sample.json``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from matrx_ai.processing.blocks import envelope as envelope_mod
from matrx_ai.processing.blocks.envelope import (
    IR_ENGINE,
    IR_ENVELOPE_KEY,
    IR_VERSION,
    adapt_block_data,
    build_canonical_envelope,
    envelope_for_block,
    reset_kind_catalog_snapshot,
)
from matrx_ai.processing.blocks.fingerprint import fingerprint_text
from matrx_ai.processing.blocks.stream_processor import StreamBlockProcessor

_FIXTURES = Path(__file__).parent / "fixtures"

# The exact top-level / root keys of CanonicalBlockIR (core/ir-types.ts).
_ENVELOPE_KEYS = {"v", "engine", "fingerprint", "root"}
_ROOT_KEYS = {
    "role",
    "kind",
    "kindState",
    "discriminator",
    "path",
    "status",
    "value",
    "residue",
}
_RESIDUE_KEYS = {"extra", "optionalMissing", "notices"}


def _load_kind_schemas() -> dict[str, dict[str, Any]]:
    with (_FIXTURES / "kind_schemas_sample.json").open(encoding="utf-8") as f:
        return json.load(f)["schemas"]


def _load_fingerprint_vectors() -> list[dict[str, str]]:
    with (_FIXTURES / "fingerprint_vectors.json").open(encoding="utf-8") as f:
        return json.load(f)["vectors"]


_KIND_SCHEMAS = _load_kind_schemas()


@pytest.fixture(autouse=True)
def _mock_kind_catalog(monkeypatch: pytest.MonkeyPatch):
    """Seed the sync snapshot with REAL schemas; no DB, no async catalog."""
    reset_kind_catalog_snapshot()
    monkeypatch.setattr(envelope_mod, "_schema_snapshot", dict(_KIND_SCHEMAS))
    yield
    reset_kind_catalog_snapshot()


def _seed(monkeypatch: pytest.MonkeyPatch, snapshot: dict[str, Any]) -> None:
    monkeypatch.setattr(envelope_mod, "_schema_snapshot", snapshot)


# ---------------------------------------------------------------------------
# (a) fingerprint parity — the hard gate, against the TS-generated vectors
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("vector", _load_fingerprint_vectors(), ids=lambda v: v["name"])
def test_envelope_fingerprint_matches_shared_ts_vector(vector: dict[str, str]) -> None:
    """The envelope's fingerprint IS fingerprint_text(source) — the FE reuse key.

    `reuseEnvelopeIfCurrent` compares `candidate.fingerprint === fingerprintText(source)`.
    Any drift here silently degrades every server envelope to a client re-parse.
    """
    built = build_canonical_envelope(
        {"segments": []},
        "transcript",
        source_text=vector["input"],
        discriminator={"format": "fence", "language": "transcript"},
    )
    assert built["fingerprint"] == vector["fingerprint"]


def test_stamped_envelope_fingerprints_the_exact_block_content() -> None:
    """End-to-end: the stamped fingerprint hashes the emitted `content` string."""
    processor = StreamBlockProcessor()
    processor.process_chunk("```transcript\n[00:01] Ada: Hello\n[00:05] Bob: Hi\n```\n")
    events = processor.finalize()

    block = next(e for e in events if e.type == "transcript")
    ir = block.metadata[IR_ENVELOPE_KEY]
    assert block.content is not None
    assert ir["fingerprint"] == fingerprint_text(block.content)


# ---------------------------------------------------------------------------
# (b) envelope shape — exact keys, for two different kinds
# ---------------------------------------------------------------------------


def _assert_contract_shape(ir: dict[str, Any], kind: str) -> None:
    assert set(ir) <= _ENVELOPE_KEYS | {"nodeIndex"}
    assert _ENVELOPE_KEYS <= set(ir)

    # The four fields the FE gate `isCanonicalBlockIR` actually checks.
    assert ir["v"] == IR_VERSION == 1
    assert ir["engine"] == IR_ENGINE == "py-block-detector"
    assert isinstance(ir["fingerprint"], str) and ir["fingerprint"]
    assert ir["root"]["role"] == "structured"

    root = ir["root"]
    assert set(root) == _ROOT_KEYS
    assert root["kind"] == kind
    assert root["kindState"] == "resolved"
    assert root["status"] == "complete"
    assert root["path"] == []
    assert isinstance(root["value"], dict)
    # Law 3: value carries schema fields + __kind ONLY.
    assert root["value"]["__kind"] == kind

    if root["residue"] is not None:
        assert set(root["residue"]) == _RESIDUE_KEYS

    for path_key, node in ir.get("nodeIndex", {}).items():
        assert "." in path_key or path_key.isidentifier()
        assert set(node) == {"kind", "kindState", "status", "residue"}
        assert node["status"] == "complete"
        assert set(node["residue"]) == _RESIDUE_KEYS


def test_envelope_shape_transcript_fence_block() -> None:
    ir = envelope_for_block(
        "transcript",
        {"segments": [{"timecode": "00:01", "seconds": 1.0, "text": "Hi", "speaker": None}]},
        source_text="[00:01] Hi",
    )
    assert ir is not None
    _assert_contract_shape(ir, "transcript")
    assert ir["root"]["discriminator"] == {"format": "fence", "language": "transcript"}


def test_envelope_shape_decision_tree_json_block() -> None:
    """Real `DecisionNode` vocabulary: question / action / yes / no (+ id, type)."""
    data = {
        "title": "Deploy?",
        "description": None,
        "root": {
            "id": "root",
            "type": "decision",
            "question": "Tests green?",
            "yes": {"id": "n2", "type": "action", "action": "Ship it"},
        },
    }
    ir = envelope_for_block("decision_tree", data, source_text=json.dumps(data))
    assert ir is not None
    _assert_contract_shape(ir, "decision_tree")
    assert ir["root"]["discriminator"] == {"format": "json", "key": "__kind"}

    # `description: None` is an unset optional the schema types as string —
    # dropped from value, recorded in optionalMissing (never silently lost).
    assert "description" not in ir["root"]["value"]
    assert "description" in ir["root"]["residue"]["optionalMissing"]

    # Schema fields survive in value; the recursive `yes` child is partitioned too.
    assert ir["root"]["value"]["root"]["question"] == "Tests green?"
    assert ir["root"]["value"]["root"]["yes"] == {"action": "Ship it"}

    # Zero data loss: the parser's `id`/`type` keys are unknown to decision_node,
    # so they ride in each node's residue rather than being dropped or merged.
    node = ir["nodeIndex"]["root"]
    assert node["kind"] == "decision_node"
    assert node["residue"]["extra"] == {"id": "root", "type": "decision"}
    assert "id" not in ir["root"]["value"]["root"]
    assert ir["nodeIndex"]["root.yes"]["residue"]["extra"] == {"id": "n2", "type": "action"}


def test_envelope_value_never_holds_unknown_keys() -> None:
    """Unknown root keys land in residue.extra, verbatim — never merged into value."""
    ir = envelope_for_block(
        "transcript",
        {"segments": [], "isComplete": True, "vendorField": {"a": 1}},
        source_text="x",
    )
    assert ir is not None
    assert set(ir["root"]["value"]) == {"segments", "__kind"}
    assert ir["root"]["residue"]["extra"] == {"isComplete": True, "vendorField": {"a": 1}}


# ---------------------------------------------------------------------------
# (c) complete-only — a streaming block NEVER carries an envelope
# ---------------------------------------------------------------------------


def test_streaming_blocks_get_no_envelope_but_finalize_does() -> None:
    """The law: no envelope until the block's own completion signal fires.

    `transcript` is a PARTIAL_UPDATE type — its parser runs on every chunk and
    `block.data` is populated mid-stream. Only `status == COMPLETE` may stamp.
    """
    processor = StreamBlockProcessor()

    streaming_events = []
    for chunk in ("```transcript\n", "[00:01] Ada: Hel", "lo\n", "[00:05] Bob: Hi\n"):
        streaming_events.extend(processor.process_chunk(chunk))

    transcript_streaming = [e for e in streaming_events if e.type == "transcript"]
    assert transcript_streaming, "expected the transcript block to stream"
    for event in transcript_streaming:
        assert event.status.value == "streaming"
        assert IR_ENVELOPE_KEY not in event.metadata

    # At least one streaming event already had parsed data — proving the guard
    # is the status, not the absence of a payload.
    assert any(e.data for e in transcript_streaming)

    final = [e for e in processor.finalize() if e.type == "transcript"]
    assert final and final[-1].status.value == "complete"
    assert IR_ENVELOPE_KEY in final[-1].metadata
    assert final[-1].metadata[IR_ENVELOPE_KEY]["root"]["status"] == "complete"


def test_incomplete_block_state_is_not_stamped_directly() -> None:
    processor = StreamBlockProcessor()
    events = processor.process_chunk("```transcript\n[00:01] Ada: Hello\n")
    assert all(IR_ENVELOPE_KEY not in e.metadata for e in events)


# ---------------------------------------------------------------------------
# (d) unregistered / unmapped kind -> no envelope
# ---------------------------------------------------------------------------


def test_unknown_block_type_gets_no_envelope() -> None:
    assert "not_a_block" not in envelope_mod.BLOCK_KIND_MAP
    assert envelope_for_block("not_a_block", {"value": 1}, source_text="{}") is None


def test_quiz_adapter_is_lossless_and_canonical() -> None:
    source = {
        "quizTitle": "Safety",
        "category": "Ops",
        "multipleChoice": [
            {
                "id": "q1",
                "question": "Deploy?",
                "options": ["No", "Yes"],
                "correctAnswer": 1,
                "explanation": "Checks passed",
            }
        ],
    }
    adapted = adapt_block_data("quiz", source)
    assert source["multipleChoice"][0]["correctAnswer"] == 1
    assert adapted["title"] == "Safety"
    assert adapted["questions"][0]["correct_answer"] == "Yes"
    assert adapted["multipleChoice"] == source["multipleChoice"]


def test_legacy_block_adapters_cover_all_known_vocabulary_gaps() -> None:
    cases = {
        "flashcards": ({"cards": []}, "title"),
        "mermaid": ({"source": "graph TD"}, "code"),
        "progress_tracker": ({"title": "T", "categories": []}, "phases"),
        "resources": ({"title": "R", "categories": []}, "categories"),
        "math_problem": ({"math_problem": {"title": "M"}}, "title"),
        "questionnaire": ({"sections": []}, "questions"),
    }
    for block_type, (value, required_key) in cases.items():
        assert required_key in adapt_block_data(block_type, value)


def test_unregistered_kind_gets_no_envelope(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kind mapped but absent from content_ir.kind_definition -> never stamp."""
    _seed(monkeypatch, {"transcript": None})
    assert envelope_for_block("transcript", {"segments": []}, source_text="x") is None


def test_cold_catalog_gets_no_envelope(monkeypatch: pytest.MonkeyPatch) -> None:
    """A cold snapshot in a sync context degrades to no-stamp, never a crash."""
    _seed(monkeypatch, {})
    assert envelope_for_block("transcript", {"segments": []}, source_text="x") is None


# ---------------------------------------------------------------------------
# (e) schema-invalid value -> no envelope (never emit what the FE would reject)
# ---------------------------------------------------------------------------


def test_schema_invalid_value_gets_no_envelope() -> None:
    """`segments` is required and must be an array — a wrong type must not stamp."""
    assert envelope_for_block("transcript", {"segments": "nope"}, source_text="x") is None


def test_missing_required_field_gets_no_envelope() -> None:
    """decision_tree requires `root` + `title`; residue can never invent them."""
    assert envelope_for_block("decision_tree", {"title": "T"}, source_text="{}") is None


def test_nested_schema_violation_gets_no_envelope() -> None:
    """Validation is recursive: a KNOWN child field of the wrong type kills it.

    `task_item.checked` is declared `boolean`, so a string must not stamp — even
    though the violation is two levels down inside an array.
    """
    data = {"items": [{"title": "t", "checked": "not-a-bool"}]}
    assert envelope_for_block("tasks", data, source_text="x") is None


def test_nested_enum_violation_gets_no_envelope() -> None:
    data = {"items": [{"title": "t", "item_type": "not-a-member"}]}
    assert envelope_for_block("tasks", data, source_text="x") is None


def test_unknown_nested_key_survives_as_residue_not_a_rejection() -> None:
    """The mirror of the above: an UNKNOWN child key is residue, not a violation.

    The task parser emits `id` and `type`, neither of which task_item declares.
    They must ride in nodeIndex residue — the envelope stays valid, nothing is
    dropped, and `value` still satisfies `additionalProperties: false`.
    """
    data = {"items": [{"title": "t", "checked": True, "id": "t-1", "type": "task"}]}
    ir = envelope_for_block("tasks", data, source_text="x")
    assert ir is not None
    assert set(ir["root"]["value"]["items"][0]) == {"title", "checked"}
    assert ir["nodeIndex"]["items.0"]["residue"]["extra"] == {"id": "t-1", "type": "task"}
    assert ir["nodeIndex"]["items.0"]["kind"] == "task_item"


def test_empty_or_absent_data_gets_no_envelope() -> None:
    assert envelope_for_block("transcript", None, source_text="x") is None
    assert envelope_for_block("transcript", {}, source_text="x") is None
    assert envelope_for_block("transcript", {"segments": []}, source_text="") is None


# ---------------------------------------------------------------------------
# Vocabulary collapse — "schema-valid but renders empty" must never ship
# ---------------------------------------------------------------------------


def test_vocabulary_collapse_gets_no_envelope() -> None:
    """A node whose every key is unknown to the schema must not stamp.

    `decision_node` declares question/action/yes/no/... — not id/type. A node
    carrying ONLY id+type keeps nothing, so `value.root` would be `{}`: still
    schema-valid (decision_node has no required fields) and still lossless via
    residue, but the FE renders `root.value` and would draw an EMPTY tree.
    """
    data = {"title": "T", "root": {"id": "n1", "type": "question"}}
    assert envelope_for_block("decision_tree", data, source_text="{}") is None


def test_all_optional_unset_object_is_not_a_collapse() -> None:
    """The mirror: known fields that are merely unset render `{}` legitimately."""
    data = {"title": "T", "root": {"question": None, "action": None}}
    ir = envelope_for_block("decision_tree", data, source_text="{}")
    assert ir is not None
    assert ir["root"]["value"]["root"] == {}
    assert ir["nodeIndex"]["root"]["residue"]["extra"] is None
    assert "question" in ir["nodeIndex"]["root"]["residue"]["optionalMissing"]


# ---------------------------------------------------------------------------
# The pure assembler mirrors the TS `envelopeFromCompleteValue` when schema-less
# ---------------------------------------------------------------------------


def test_pure_assembler_without_schema_wraps_value_verbatim() -> None:
    value = {"segments": [], "anything": 1}
    ir = build_canonical_envelope(
        value,
        "transcript",
        source_text="src",
        discriminator={"format": "fence", "language": "transcript"},
    )
    assert set(ir) == _ENVELOPE_KEYS  # no nodeIndex
    assert ir["root"]["residue"] is None
    assert ir["root"]["value"] == {"segments": [], "anything": 1, "__kind": "transcript"}
    assert ir["fingerprint"] == fingerprint_text("src")
