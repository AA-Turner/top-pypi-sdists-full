"""Tests for shared.confidence re-export of ConfidenceScore."""

from pydantic import BaseModel

from agentic_devtools.orchestration.schemas.shared.confidence import ConfidenceScore


class _Model(BaseModel):
    score: ConfidenceScore


class TestConfidenceScoreReExport:
    """Tests that ConfidenceScore re-exported from shared.confidence works correctly."""

    def test_valid_value_via_shared_import(self):
        result = _Model(score=0.75)
        assert result.score == 0.75

    def test_all_exported(self):
        from agentic_devtools.orchestration.schemas.shared import confidence

        assert hasattr(confidence, "ConfidenceScore")
        assert "ConfidenceScore" in confidence.__all__
