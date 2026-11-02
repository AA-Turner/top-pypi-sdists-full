"""Tests for StageEvent in speckit/phase0/observability.py (FR-001)."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.observability import StageEvent


class TestStageEvent:
    """Tests for the StageEvent dataclass."""

    def test_to_dict_uses_exact_fr001_key_names(self) -> None:
        event = StageEvent(
            sequence=1,
            stage="validation",
            status="succeeded",
            timestamp="2026-01-01T00:00:00Z",
            message="ok",
        )
        assert event.to_dict() == {
            "sequence": 1,
            "stage": "validation",
            "status": "succeeded",
            "timestamp": "2026-01-01T00:00:00Z",
            "diagnosticCode": None,
            "message": "ok",
            "capturedProperties": [],
            "excludedProperties": [],
            "missingProperties": [],
            "diagnosticUrl": None,
        }

    def test_optional_fields_default_to_empty_or_none(self) -> None:
        event = StageEvent(sequence=2, stage="commit", status="failed", timestamp="t", message="m")
        assert event.diagnostic_code is None
        assert event.captured_properties == []
        assert event.excluded_properties == []
        assert event.missing_properties == []
        assert event.diagnostic_url is None
