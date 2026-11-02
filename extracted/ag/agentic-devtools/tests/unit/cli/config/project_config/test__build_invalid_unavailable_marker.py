"""Tests for ``_build_invalid_unavailable_marker``."""

from agentic_devtools.cli.config.project_config import (
    _build_invalid_unavailable_marker,
    validate_model_metadata,
)


class TestBuildInvalidUnavailableMarker:
    """Tests for canonical invalid-row marker construction."""

    def test_builds_default_valid_marker_for_non_mapping_entry(self):
        marker = _build_invalid_unavailable_marker("claude-opus-4.8", None)

        validate_model_metadata(marker)

        assert marker["modelId"] == "claude-opus-4.8"
        assert marker["surfaces"]["copilot"] == {"modelId": "claude-opus-4.8"}
        assert marker["surfaces"]["vscode"]["displayName"] == "Claude Opus 4.8"
        assert marker["surfaces"]["docs"]["displayName"] == "Claude Opus 4.8"
        assert marker["pricingStatus"] == "unavailable"
        assert marker["priceCategory"] is None
        assert marker["provenance"] == "unknown"
        assert marker["unavailableReason"] == "invalid"
        assert "sourceMetadata" not in marker
        assert "observedAt" not in marker

    def test_uses_source_metadata_when_provenance_is_missing(self):
        marker = _build_invalid_unavailable_marker(
            "future-model",
            {
                "surfaces": {
                    "vscode": {"displayName": "Future VS Code"},
                    "docs": {"displayName": "Future Docs"},
                },
                "sourceMetadata": {"source": "acp-cache", "acp": {"copilotPriceCategory": "low"}},
                "priceCategory": "low",
                "observedAt": "2026-08-31T00:00:00+00:00",
            },
        )

        validate_model_metadata(marker)

        assert marker["surfaces"]["vscode"]["displayName"] == "Future VS Code"
        assert marker["surfaces"]["docs"]["displayName"] == "Future Docs"
        assert marker["provenance"] == "acp-cache"
        assert marker["sourceMetadata"] == {"source": "acp-cache", "acp": {"copilotPriceCategory": "low"}}
        assert marker["priceCategory"] == "low"
        assert marker["observedAt"] == "2026-08-31T00:00:00+00:00"

    def test_ignores_invalid_optional_fields_and_falls_back_to_default_surface_names(self):
        marker = _build_invalid_unavailable_marker(
            "future-model",
            {
                "provenance": "project-config",
                "surfaces": {
                    "vscode": {"displayName": "   "},
                    "docs": {"displayName": 7},
                },
                "sourceMetadata": "bad",
                "priceCategory": "   ",
                "observedAt": "not-a-timestamp",
            },
        )

        validate_model_metadata(marker)

        assert marker["surfaces"]["vscode"]["displayName"] == "future-model"
        assert marker["surfaces"]["docs"]["displayName"] == "future-model"
        assert marker["provenance"] == "project-config"
        assert marker["priceCategory"] is None
        assert "sourceMetadata" not in marker
        assert "observedAt" not in marker
