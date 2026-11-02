"""Workflow-side ``metadata.__ir`` envelope producer (workflow node outputs).

The scheduler validates every kind-declaring node's output against the kind's
registered ``emitted_json_schema`` (``check_against_kind``). When — and ONLY
when — that check ran and PASSED, this module wraps the output in a canonical
``CanonicalBlockIR`` envelope so the Studio (and any other consumer of
``node_completed`` events) renders it through the twin's trusted-envelope path
(``readEnvelope`` / ``sanitizeInboundEnvelopeMetadata``) without re-parsing or
re-classifying. Wire contract: matrx-frontend
``/Users/armanisadeghi/code/common-docs/systems/architecture/content-ir/FEATURE.md``; TS shape reference:
``core/normalize.ts#envelopeFromCompleteValue`` (the zero-reprocessing wrap
this mirrors field-for-field).

THE LAWS (workflow flavor of the chat producer's three laws — see
``matrx_ai.processing.blocks.envelope``):

1. **Verified-only.** No envelope without a real ``checked=True`` PASS from
   the kind catalog. A drifting output, a degraded (loud-skip) check, or a
   kind-less node gets NO envelope — the verdict fields on the event
   (``output_kind_ok`` / ``output_kind_degraded``) already carry that truth,
   and consumers fall back to their own honest classification. A skipped
   check is never a pass, and an envelope IS a rendered pass.
2. **Out-of-band, zero mutation.** Workflow edges are a framed protocol —
   kind identity travels BESIDE the value (``output_kind`` on the event, the
   envelope on ``metadata``), never inside it. ``root.value`` is the node's
   output dict verbatim: no ``__kind`` injection, no partition, no copy. A
   verified pass against an ``additionalProperties: false`` schema means the
   value is already schema-clean, so ``residue`` is ``null`` by construction
   — exactly like the TS ``envelopeFromCompleteValue``.
3. **Never load-bearing.** Envelope assembly can never fail a run. The
   scheduler wraps the call in a loud fail-open (mirrors the kind catalog's
   posture): a stamping bug logs at error level and the event ships without
   an envelope.

The fingerprint hashes the compact JSON serialization of the output value
(``json.dumps(value, ensure_ascii=False, separators=(",", ":"))``) — the
Python analogue of the TS twin's ``fingerprintText(JSON.stringify(value))``
in ``envelopeFromCompleteValue``. It is a cache/idempotence key, not a
validation gate: consumers receive the envelope by reference on the event and
never need to recompute it.
"""

from __future__ import annotations

import json
from typing import Any

from matrx_graph.content_ir.fingerprint import fingerprint_text

# Mirrors matrx-frontend core/ir-types.ts + core/kind-schema.types.ts, and the
# chat-side producer matrx_ai.processing.blocks.envelope (which imports these).
IR_VERSION = 1
IR_ENVELOPE_KEY = "__ir"
KIND_KEY = "__kind"

# Engine tag for Python-built envelopes. The contract's TS type pins
# ``engine`` to the closed union "fe-kind-parser" | "py-block-detector"
# (twin ``core/ir-types.ts``; PYTHON_ENVELOPE_CONTRACT: Python producers
# MUST send "py-block-detector") — so the workflow producer sends the same
# value as the chat pipeline. Workflow provenance is carried by the FRAME
# (the ``node_completed`` event the envelope rides), not the engine string.
IR_ENGINE = "py-block-detector"

# The ENGINE-PLANE keys the platform stamps INTO a payload dict. They are
# metadata about the payload, never one of the author's data args — routing
# and merging must treat them as engine namespace (ENGINE_SPEC §3.7: two
# edges delivering ``__kind`` is a metadata coincidence, not a multi-writer
# collision the author can even fix). One set, so the exclusion never
# degenerates into scattered ``"__kind"`` literals at each site.
RESERVED_MARKER_KEYS: frozenset[str] = frozenset({KIND_KEY, IR_ENVELOPE_KEY})


def compact_json(value: Any) -> str:
    """Compact JSON — the fingerprint source (TS ``JSON.stringify`` analogue)."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def envelope_for_verified_output(value: dict[str, Any], kind: str) -> dict[str, Any]:
    """Assemble a complete, resolved CanonicalBlockIR for a VERIFIED output.

    Pure — no IO, no logging, no mutation of ``value`` (held by reference;
    the envelope rides the same frozen event as the output itself).

    The caller MUST have already established that the output validated
    against ``kind``'s registered schema (``check_against_kind`` →
    ``checked=True`` with no errors); this function cannot know that, and
    stamping an unverified value would be a contract violation (law 1).
    """
    return {
        "v": IR_VERSION,
        "engine": IR_ENGINE,
        "fingerprint": fingerprint_text(compact_json(value)),
        "root": {
            "role": "structured",
            "kind": kind,
            "kindState": "resolved",
            # Framed-protocol provenance: the kind arrived out of band (the
            # node's compiled output_kind), not from an in-band __kind key.
            # ``{format: "json", key: "__kind"}`` is the contract's only JSON
            # discriminator shape (same documented gap as the chat producer's
            # legacy-wrapper-key blocks — see its ``discriminator_for_block``).
            "discriminator": {"format": "json", "key": KIND_KEY},
            "path": [],
            "status": "complete",
            "value": value,
            "residue": None,
        },
    }


# Marker for a wire-elided envelope: ``root.value`` was dropped because the
# SAME dict already rides the frame beside it (NodeCompletedEvent.output) —
# inlining it would serialize every verified payload twice per streamed event
# and per persisted wf_node_events row. ``value_ref`` names the sibling frame
# field holding the value; its PRESENCE (never a bare ``value: null``, which
# could be a legitimate value) is what marks the elision. The consumer's
# single ingest gate rehydrates ``root.value`` from that field BEFORE the twin
# contract ever sees the envelope (Studio: ``inbound-envelope.ts``).
VALUE_REF_OUTPUT = "output"


def elide_envelope_value(envelope: dict[str, Any]) -> dict[str, Any]:
    """Wire/persistence form: drop the inline ``root.value``, mark the source.

    Pure and non-mutating (shallow copies); everything else — fingerprint
    (hashed over the FULL value at stamp time), kind, discriminator, status —
    is untouched. ``envelope_for_verified_output`` stays the standalone
    full-envelope assembler for consumers without a value-bearing frame.
    """
    root = {**envelope["root"], "value": None, "value_ref": VALUE_REF_OUTPUT}
    return {**envelope, "root": root}


def ir_metadata_for_verified_output(value: dict[str, Any], kind: str) -> dict[str, Any]:
    """The ``metadata`` dict carrying the WIRE-ELIDED envelope at ``__ir``.

    Built for the ``node_completed`` frame, whose ``output`` field carries
    ``value`` verbatim — so the envelope ships without the duplicate inline
    copy (see ``elide_envelope_value``).
    """
    return {IR_ENVELOPE_KEY: elide_envelope_value(envelope_for_verified_output(value, kind))}


def stamp_kind_marker(dump: Any, kind: str | None) -> Any:
    """STATION 1 — SETTLEMENT STAMPING. Make a node's dumped payload SAY what
    it is, using the kind the node is registered to produce.

    THE ``__kind`` MARKER LAW (KINDS_EVERYWHERE_PLAN §4.2a) applies to every
    value that crosses a named boundary — and a node's output crosses several
    that the scheduler is not standing on: the isolated node-test result and
    its ``last_test_output`` sample slot, and an inner action's payload nested
    inside ``tool.call``'s envelope. A payload model that IS a ``KindModel``
    carries the marker as declared data and arrives here already stamped; the
    46-of-89 registered nodes whose payload predates ``KindModel`` (measured
    2026-09-09) carry NOTHING, so the identity has to come from the node's
    registered/compiled ``output_kind``. Live defect this closes: "Text to
    Data" (``data.parse_json``) declares the ``value`` archetype kind and its
    Test Step sample failed the Studio's structural check with *(root) must
    have required property '__kind'* — the step worked, the verdict was red,
    because the emitter never said what it emitted.

    THE ONE PLACE. Every path that dumps a node payload calls THIS — the
    scheduler's settlement, the node-test path, ``tool.call``'s inner
    dispatch. A per-node fix is banned: an emitter is not where identity is
    decided, and 46 copies of the same four lines is 46 chances to forget one.

    Rules, all three load-bearing:

    - **Never overwrite.** A dump that already carries ``__kind`` said it
      itself (a ``KindModel``, or an upstream stamp) and that answer wins.
    - **Never touch anything but the root.** Nested markers are the nested
      values' own identity — a parsed ``directive_v1_create_task`` sitting
      inside a ``value`` wrapper keeps ITS marker untouched, at every depth.
      This function stamps one key on one dict and recurses into nothing.
    - **``json`` is a format word, never an identity** (round-1 F7) — a node
      declaring it gets no stamp, exactly as the specs no longer declare it.

    Callers holding a VERDICT must not stamp a payload that measurably FAILED
    its kind check (stamping would make the data lie) — that gate belongs to
    the caller, which is the only one that has the verdict.

    Mutates ``dump`` in place and returns it (the scheduler hands the same
    dict to routing, broadcast and ``last_outputs``); a non-dict payload is
    returned untouched, since a scalar has nowhere to carry a marker.
    """
    if isinstance(dump, dict) and kind and kind != "json" and KIND_KEY not in dump:
        dump[KIND_KEY] = kind
    return dump
