# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest

from omnibase_compat.models.event_envelope import EventEnvelopeV1Minimal


@pytest.mark.unit
@pytest.mark.timeout(30)
class TestEventEnvelopeProvenance:
    def test_default_provenance_is_none(self) -> None:
        envelope = EventEnvelopeV1Minimal(event_id="id", event_type="type", payload={})
        assert envelope.data_provenance is None

    def test_set_provenance(self) -> None:
        envelope = EventEnvelopeV1Minimal(
            event_id="id", event_type="type", payload={}, data_provenance="measured"
        )
        assert envelope.data_provenance == "measured"

    def test_backwards_compatible_without_provenance(self) -> None:
        data = {"event_id": "id", "event_type": "type", "payload": {}}
        envelope = EventEnvelopeV1Minimal.model_validate(data)
        assert envelope.data_provenance is None

    def test_accepts_expected_provenance_values(self) -> None:
        for value in ("demo_seeded", "demo_projected_shortcut", "measured", "estimated", "unknown"):
            envelope = EventEnvelopeV1Minimal(
                event_id="id", event_type="type", payload={}, data_provenance=value
            )
            assert envelope.data_provenance == value
