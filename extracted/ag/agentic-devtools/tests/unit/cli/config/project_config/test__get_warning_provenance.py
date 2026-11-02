"""Tests for ``_get_warning_provenance``."""

from agentic_devtools.cli.config.project_config import _get_warning_provenance


class TestGetWarningProvenance:
    """Tests for warning provenance selection."""

    def test_returns_provenance_field_when_present(self):
        assert _get_warning_provenance({"provenance": "curated-catalog"}) == "curated-catalog"

    def test_falls_back_to_source_metadata_source(self):
        assert _get_warning_provenance({"sourceMetadata": {"source": "acp-cache"}}) == "acp-cache"

    def test_returns_unknown_for_non_mapping_or_blank_source(self):
        assert _get_warning_provenance(None) == "unknown"
        assert _get_warning_provenance({"sourceMetadata": {"source": "   "}}) == "unknown"
