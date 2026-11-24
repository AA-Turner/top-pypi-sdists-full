"""A follow-up turn on another worker sends the tools array with the SAME bytes as the turn before.

Live finding (static seal check, 2026-11-12): turn 1 sent each ``input_schema`` in Python key order
(type, properties, required, additionalProperties). The ledger's record rides ``cx_conversation.config``
(jsonb), which reorders object keys (shorter first). A worker without the ledger in memory hydrated the
jsonb-ordered copy and sent it as-is: the ``tools`` bytes changed and the provider's cached prefix broke,
while the ledger's sort-keys digest saw nothing. The record now keeps each declaration's JSON text.
"""

from __future__ import annotations

import json
from typing import Any

from matrx_ai.tools import declaration_ledger as ledger

CONV = "22222222-3333-4444-5555-666666666666"


def _declarations() -> list[dict[str, Any]]:
    return [
        {
            "name": "lookup_record",
            "description": "Look a record up.",
            "input_schema": {
                "type": "object",
                "properties": {"record_id": {"type": "string", "description": "The id."}},
                "required": ["record_id"],
                "additionalProperties": False,
            },
        }
    ]


def _as_jsonb(value: Any) -> Any:
    """What Postgres jsonb hands back: object keys ordered shorter first, then bytewise."""
    if isinstance(value, dict):
        return {k: _as_jsonb(value[k]) for k in sorted(value, key=lambda k: (len(k.encode()), k.encode()))}
    if isinstance(value, list):
        return [_as_jsonb(v) for v in value]
    return value


def _send() -> str:
    result = ledger.stabilize_declarations(
        "anthropic", _declarations(), name_of=lambda d: d.get("name"), conversation_id=CONV
    )
    return json.dumps(result.declarations)


def test_turn_two_hydrated_from_jsonb_sends_turn_one_bytes() -> None:
    ledger.reset_for_tests()
    try:
        turn_one = _send()
        stored = _as_jsonb(json.loads(json.dumps(ledger.export_record(CONV))))  # the row, as read back
        ledger.reset_for_tests()  # another worker: no ledger in memory
        assert ledger.hydrate_from_record(CONV, stored)
        assert _send() == turn_one
    finally:
        ledger.reset_for_tests()


def test_a_record_written_before_the_wire_text_still_hydrates() -> None:
    ledger.reset_for_tests()
    try:
        _send()
        record = ledger.export_record(CONV) or {}
        for entry in record.values():
            for item in entry["tools"]:
                # The first stored shape: the object only (jsonb order), no wire text.
                item["declaration"] = json.loads(item.pop(ledger.WIRE_KEY))
        ledger.reset_for_tests()
        assert ledger.hydrate_from_record(CONV, record)
    finally:
        ledger.reset_for_tests()


def test_each_tool_is_stored_once_as_its_wire_text() -> None:
    """The record carries each declaration ONCE (the wire text), never also as an object: the
    object copy doubled every write of the record (audit 2026-11-13). Records written before (both
    keys) still hydrate to the same bytes."""
    ledger.reset_for_tests()
    try:
        first = _send()
        record = ledger.export_record(CONV) or {}
        items = [item for entry in record.values() for item in entry["tools"]]
        assert items and all(ledger.WIRE_KEY in item and "declaration" not in item for item in items)
        both = json.loads(json.dumps(record))
        for entry in both.values():
            for item in entry["tools"]:
                item["declaration"] = json.loads(item[ledger.WIRE_KEY])
        ledger.reset_for_tests()
        assert ledger.hydrate_from_record(CONV, both)
        assert json.dumps(_send(), ensure_ascii=False) == json.dumps(first, ensure_ascii=False)
    finally:
        ledger.reset_for_tests()
