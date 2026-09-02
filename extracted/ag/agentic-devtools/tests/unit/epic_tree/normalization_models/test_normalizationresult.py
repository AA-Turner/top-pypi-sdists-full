"""Tests for NormalizationResult dataclass."""

from agentic_devtools.epic_tree.normalization_models import NormalizationResult, NormalizationWarning


class TestNormalizationResult:
    """Tests for NormalizationResult construction and field access."""

    def test_construction_with_defaults(self):
        """NormalizationResult can be constructed with just a document."""
        result = NormalizationResult(document={"epic": {}})
        assert result.document == {"epic": {}}
        assert result.warnings == []

    def test_construction_with_warnings(self):
        """NormalizationResult can carry warnings."""
        warning = NormalizationWarning(
            ref="f1", depth=1, field="issueType", actual_value="epic", expected_value="feature"
        )
        result = NormalizationResult(document={"epic": {}}, warnings=[warning])
        assert len(result.warnings) == 1
        assert result.warnings[0].ref == "f1"

    def test_document_field_access(self):
        """Document field provides the normalized document."""
        doc = {"schemaVersion": "1.0", "epic": {"ref": "e1"}}
        result = NormalizationResult(document=doc)
        assert result.document["schemaVersion"] == "1.0"
