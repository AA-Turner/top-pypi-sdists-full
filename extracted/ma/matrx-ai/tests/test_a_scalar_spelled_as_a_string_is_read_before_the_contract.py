"""A scalar the model spelled as a string is read before the tool and the Content IR contract see it.

Live 2026-11-18 (``tool_input_contract_drift`` x3, ``data``): the model sent ``limit: "3"``,
``content_max_chars: "1"``, ``descending: "true"``. The tool's lax input model read them as 3, 1, True
and ran; the contract (the schema the model was shown) refused the strings, so each call was filed
as contract drift. ``decode_stringified_by_schema`` now reads plain scalar literals by the published
type, so both judge the same value. Anything that is not an exact literal is left for the refusal.
"""

from __future__ import annotations

from matrx_graph.contract_kinds import check_schema

from matrx_ai.tools._dispatch_util import decode_stringified_by_schema

SCHEMA = {
    "type": "object",
    "properties": {
        "action": {"type": "string"},
        "limit": {"type": "integer"},
        "content_max_chars": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
        "descending": {"type": "boolean"},
        "ratio": {"type": "number"},
        "label": {"type": "string"},
        "id_or_count": {"type": ["string", "integer"]},
    },
}


def test_the_live_call_reads_as_the_tool_reads_it_and_the_contract_agrees() -> None:
    sent = {"action": "list", "limit": "3", "content_max_chars": "1", "descending": "true"}
    assert check_schema(sent, SCHEMA).errors, "the live call is refused by the contract as sent"
    decoded = decode_stringified_by_schema(sent, SCHEMA)
    assert decoded is not None
    arguments, fields = decoded
    assert arguments == {"action": "list", "limit": 3, "content_max_chars": 1, "descending": True}
    assert fields == ["content_max_chars", "descending", "limit"]
    assert not check_schema(arguments, SCHEMA).errors


def test_numbers_read_exactly() -> None:
    arguments, _ = decode_stringified_by_schema({"ratio": " 0.25 ", "limit": "-2"}, SCHEMA) or ({}, [])
    assert arguments == {"ratio": 0.25, "limit": -2}


def test_only_exact_literals_are_read() -> None:
    sent = {
        "limit": "3 items",
        "descending": "yes",
        "ratio": "nan",
        "label": "42",
        "id_or_count": "7",
    }
    # Not literals of the declared type, or a string is lawful: left as sent for the tool to judge.
    assert decode_stringified_by_schema(sent, SCHEMA) is None
    assert decode_stringified_by_schema({"limit": "3.5"}, SCHEMA) is None
    assert decode_stringified_by_schema({"descending": "1"}, SCHEMA) is None
