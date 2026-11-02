"""Workflow-side Content IR envelope producer (matrx_graph.content_ir.envelope).

Covers the pure assembler (full form vs wire-elided form) and the
VALUE-LEVEL fingerprint parity boundary — ``fingerprint_text`` itself is
vector-pinned against the TS twin (matrx-ai ``test_fingerprint_parity.py``,
shared string vectors), but that only proves parity for PRE-SERIALIZED
strings. The workflow producer serializes the value itself
(``compact_json`` = ``json.dumps(v, ensure_ascii=False,
separators=(",", ":"), default=str)`` vs the twin's
``JSON.stringify(value)``), so this file pins that serialization boundary.

The TS-side expected fingerprints below were generated from the REAL twin
implementation (``apps/shared/content-ir-core/core/fingerprint.ts``) via::

    pnpm dlx tsx  # script: JSON.stringify(value) -> fingerprintText(...)

on 2026-07-15. Regenerate the same way if compact_json or the twin changes.

KNOWN, DOCUMENTED DIVERGENCES (pinned as such, not claimed as parity):
Python's float repr differs from JS number formatting for
- whole-number floats: ``1.0`` -> ``"1.0"`` (JS: ``"1"``)
- small exponents:   ``5e-7`` -> ``"5e-07"`` (JS: ``"5e-7"``)
The fingerprint is a cache/idempotence KEY, never a validation gate:
consumers receive the envelope by reference on the event, and a mismatched
fingerprint at worst degrades a fingerprint-keyed cache hit to a re-parse
(the contract's stated failure mode). Strings, ints, unicode (incl. astral
pairs), nesting/key order, null/true/false, fractional floats, and large
exponents are byte-identical and pinned below.
"""

from __future__ import annotations

import json

from matrx_graph.content_ir.envelope import (
    IR_ENVELOPE_KEY,
    VALUE_REF_OUTPUT,
    compact_json,
    elide_envelope_value,
    envelope_for_verified_output,
    ir_metadata_for_verified_output,
)
from matrx_graph.content_ir.fingerprint import fingerprint_text

# ---------------------------------------------------------------- assembler


def test_full_envelope_wraps_value_verbatim():
    value = {"status": 200, "body": "ok"}
    env = envelope_for_verified_output(value, "http_response")
    assert env["v"] == 1
    assert env["engine"] == "py-block-detector"
    root = env["root"]
    assert root["role"] == "structured"
    assert root["kind"] == "http_response"
    assert root["kindState"] == "resolved"
    assert root["status"] == "complete"
    assert root["residue"] is None
    # Out-of-band posture: the value BY REFERENCE, unmutated, no __kind.
    assert root["value"] is value
    assert "__kind" not in value
    assert "value_ref" not in root  # the full form carries no elision marker
    assert env["fingerprint"] == fingerprint_text(compact_json(value))


def test_elide_envelope_value_is_pure_and_marked():
    value = {"status": 200}
    full = envelope_for_verified_output(value, "http_response")
    elided = elide_envelope_value(full)
    # Marked elision — never mistakable for a legitimate null value.
    assert elided["root"]["value"] is None
    assert elided["root"]["value_ref"] == VALUE_REF_OUTPUT
    # Everything else preserved, incl. the FULL-value fingerprint.
    assert elided["fingerprint"] == full["fingerprint"]
    assert elided["root"]["kind"] == "http_response"
    # Non-mutating: the full envelope still holds the value.
    assert full["root"]["value"] is value
    assert "value_ref" not in full["root"]


def test_ir_metadata_ships_the_elided_wire_form():
    value = {"result": "ok"}
    metadata = ir_metadata_for_verified_output(value, "test_result")
    env = metadata[IR_ENVELOPE_KEY]
    assert env["root"]["value"] is None
    assert env["root"]["value_ref"] == VALUE_REF_OUTPUT
    # The payload appears NOWHERE in the serialized metadata (no double
    # serialization per event / per wf_node_events row).
    assert '"result"' not in json.dumps(metadata)
    assert env["fingerprint"] == fingerprint_text(compact_json(value))


# ------------------------------------------------- value-level fingerprints

# (value, TS JSON.stringify output, TS fingerprintText output) — generated
# from the real twin; see module docstring.
_TS_PARITY_VECTORS: list[tuple[dict, str, str]] = [
    (
        {"topic": "photosynthesis"},
        '{"topic":"photosynthesis"}',
        "q-6ky0c1gsnpsq",
    ),
    (
        {"emoji": "\U0001f680", "text": "café", "mixed": "日本語 + emoji 🎉"},
        '{"emoji":"🚀","text":"café","mixed":"日本語 + emoji 🎉"}',
        "1h-kozormngpq1o",
    ),
    (
        {"n": 42, "arr": [1, 2, 3], "nested": {"b": 1, "a": 2}, "s": None, "t": True},
        '{"n":42,"arr":[1,2,3],"nested":{"b":1,"a":2},"s":null,"t":true}',
        "1r-16qhf6713t9rkt",
    ),
    (
        {"f": 1.5, "g": -0.25, "h": 3.14159},
        '{"f":1.5,"g":-0.25,"h":3.14159}',
        "v-13x306d8cjbff",
    ),
]


def test_value_level_fingerprint_parity_with_ts_twin():
    """compact_json(value) is byte-identical to JSON.stringify(value) — and
    therefore fingerprints match — for strings, unicode/astral, ints,
    insertion-order keys, null/true, and fractional floats."""
    for value, ts_json, ts_fingerprint in _TS_PARITY_VECTORS:
        py_json = compact_json(value)
        assert py_json == ts_json, f"serialization drift for {value!r}"
        assert fingerprint_text(py_json) == ts_fingerprint


# TS-side truth for the documented divergence classes (same generation run).
_TS_DIVERGENT_VECTORS: list[tuple[dict, str, str, str]] = [
    # (value, TS json, TS fingerprint, python json)
    ({"f": 1.0}, '{"f":1}', "7-1q6m0rcp1t7a6", '{"f":1.0}'),
    (
        {"big": 1e21, "tiny": 5e-7},
        '{"big":1e+21,"tiny":5e-7}',
        "p-anaphd1omy2tz",
        '{"big":1e+21,"tiny":5e-07}',
    ),
]


def test_value_level_fingerprint_known_float_divergences():
    """Whole-number floats and small exponents serialize differently in
    Python vs JS — a DOCUMENTED divergence (see module docstring), pinned
    here so any accidental 'fix' or regression is visible. Acceptable
    because the fingerprint is only a cache key; the envelope travels by
    reference and a mismatch degrades to a re-parse, never an error."""
    for value, ts_json, ts_fingerprint, py_json_expected in _TS_DIVERGENT_VECTORS:
        py_json = compact_json(value)
        assert py_json == py_json_expected  # pin the Python side too
        assert py_json != ts_json
        assert fingerprint_text(py_json) != ts_fingerprint
        # Same STRING still hashes identically — the divergence is purely
        # the serialization, not the hash (string-level parity is pinned in
        # matrx-ai test_fingerprint_parity.py).
        assert fingerprint_text(ts_json) == ts_fingerprint
