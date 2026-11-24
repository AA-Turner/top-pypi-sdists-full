"""FX18: a value under a key matched ONLY by ``patternProperties`` keeps its ``__kind``.

Live defect (workflow 8e1859b5, kind ``brand_state_read`` v8): ``values.testimony_room_social`` is not a declared
property (rooms added later match ``^testimony_room_[a-z0-9_]+$``); kind validation's marker reducer did not look at
patterns, treated the position as unknown, stripped the section's ``__kind`` and the kind's own ``required: [__kind]``
failed. The schema below has the live kind's shape; the row is a real social testimony row from the failing run.
"""

from matrx_graph.content_ir.markers import strip_kind_markers
from matrx_graph.executor.schema_validation import validate_instance

_SECTION = {
    "anyOf": [
        {"type": "null"},
        {
            "type": "object",
            "required": ["__kind", "section", "items"],
            "properties": {
                "__kind": {"type": "string", "const": "provider_section_list"},
                "section": {"type": "string"},
                "items": {"type": "array", "items": {"type": "object", "properties": {}, "additionalProperties": True}},
            },
            "additionalProperties": False,
        },
    ]
}
_SCHEMA = {
    "type": "object",
    "required": ["values"],
    "properties": {
        "values": {
            "type": "object",
            "properties": {"testimony_room_owner": _SECTION},
            "patternProperties": {"^testimony_room_[a-z0-9_]+$": _SECTION},
            "additionalProperties": False,
        }
    },
    "additionalProperties": False,
}
_SOCIAL_ROW = {
    "id": "d0aa12d2-8e94-4bc9-9fe4-f7976831a171", "room": "social", "topic": "story", "checkable": True,
    "conferred": None, "firsthand": True, "how_to_check": None, "respondent_key": None,
    "quote": "Family owned and operated service you can trust since 1975",
    "statement": "The Facebook bio says it is family owned and operated.",
    "created_at": "2026-11-03 03:43:18.591463+00:00", "source_url": "https://www.facebook.com/MiniMopsInc",
    "updated_by": "8fc0802e-0c2a-41fc-88e3-8aa756501a76", "source_value": "bios: Facebook @MiniMopsInc",
}


def _value(room: str) -> dict:
    return {"values": {f"testimony_room_{room}": {"__kind": "provider_section_list",
                                                  "section": "brand.brand_testimony", "items": [_SOCIAL_ROW]}}}


def test_a_pattern_only_room_keeps_its_marker_and_validates():
    value = _value("social")
    reduced = strip_kind_markers(value, _SCHEMA)
    assert reduced["values"]["testimony_room_social"]["__kind"] == "provider_section_list"
    assert validate_instance(_SCHEMA, reduced) == []


def test_a_declared_room_still_validates():
    assert validate_instance(_SCHEMA, strip_kind_markers(_value("owner"), _SCHEMA)) == []
