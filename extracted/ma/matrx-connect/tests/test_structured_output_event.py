"""Tests for the STRUCTURED_OUTPUT event registration + wire shape."""

from __future__ import annotations

import pytest

from matrx_connect.context.events import (
    PAYLOAD_REGISTRY,
    EventType,
    StructuredOutputPayload,
    build_event,
    validate_event_dict,
)


def test_event_type_registered() -> None:
    assert EventType.STRUCTURED_OUTPUT.value == "structured_output"


def test_payload_class_in_registry() -> None:
    assert PAYLOAD_REGISTRY[EventType.STRUCTURED_OUTPUT] is StructuredOutputPayload


def test_payload_roundtrips_through_build_event() -> None:
    payload = StructuredOutputPayload(
        schema_name="test",
        json_schema={"type": "object", "required": ["x"]},
        data={"x": 1},
        success=True,
        reason="",
        match_count=1,
        agent_name="Tester",
        operation_id=None,
        kind="agent_io_agent_1_abcd1234_output",
        kind_version=1,
        kind_checked=True,
        kind_errors=[],
    )
    event = build_event(EventType.STRUCTURED_OUTPUT, payload)
    assert event.event == EventType.STRUCTURED_OUTPUT
    assert event.data["success"] is True
    assert event.data["json_schema"]["type"] == "object"
    assert event.data["kind_checked"] is True

    # Wire format
    jsonl = event.to_jsonl()
    assert jsonl.endswith("\n")
    assert '"event":"structured_output"' in jsonl


def test_failure_payload_is_valid() -> None:
    payload = StructuredOutputPayload(
        json_schema={"type": "array"},
        data=None,
        success=False,
        reason="no JSON candidate matched the supplied schema",
        match_count=0,
    )
    event = build_event(EventType.STRUCTURED_OUTPUT, payload)
    assert event.data["data"] is None
    assert event.data["success"] is False


def test_validate_event_dict_accepts_canonical_payload() -> None:
    data = {
        "schema_name": "x",
        "json_schema": {"type": "object"},
        "data": {"k": "v"},
        "success": True,
        "reason": "",
        "match_count": 1,
        "agent_name": None,
        "operation_id": None,
    }
    event = validate_event_dict("structured_output", data)
    assert event.event == EventType.STRUCTURED_OUTPUT


def test_extra_fields_are_rejected() -> None:
    with pytest.raises(Exception):
        StructuredOutputPayload(
            json_schema={"type": "object"},
            success=True,
            reason="",
            match_count=0,
            unknown_field="should not be allowed",  # type: ignore[call-arg]
        )
