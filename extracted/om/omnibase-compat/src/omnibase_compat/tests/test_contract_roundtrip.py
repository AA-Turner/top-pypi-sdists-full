# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from omnibase_compat.models.event_envelope import EventEnvelopeV1Minimal


@pytest.mark.unit
def test_event_envelope_roundtrip() -> None:
    envelope = EventEnvelopeV1Minimal(
        event_id="evt-001",
        event_type="node.executed.v1",
        payload={"result": "ok"},
    )
    serialized = envelope.model_dump_json()
    restored = EventEnvelopeV1Minimal.model_validate_json(serialized)
    assert restored.event_id == envelope.event_id
    assert restored.event_type == envelope.event_type
    assert restored.payload == envelope.payload


@pytest.mark.unit
def test_event_envelope_is_frozen() -> None:
    envelope = EventEnvelopeV1Minimal(
        event_id="evt-002",
        event_type="node.executed.v1",
        payload={},
    )
    with pytest.raises((ValidationError, TypeError)):
        envelope.event_id = "mutated"  # type: ignore[misc]


@pytest.mark.unit
def test_event_envelope_schema_export() -> None:
    schema = EventEnvelopeV1Minimal.model_json_schema()
    assert set(schema["properties"].keys()) == {
        "event_id",
        "event_type",
        "payload",
        "schema_version",
        "data_provenance",
    }
