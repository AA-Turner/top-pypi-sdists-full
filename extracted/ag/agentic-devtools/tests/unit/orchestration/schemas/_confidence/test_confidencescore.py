"""Tests for ConfidenceScore annotated type."""

import pytest
from pydantic import BaseModel, ValidationError

from agentic_devtools.orchestration.schemas._confidence import ConfidenceScore


class _Model(BaseModel):
    score: ConfidenceScore


class TestConfidenceScore:
    """Tests for ConfidenceScore type validation."""

    def test_valid_float_values(self):
        assert _Model(score=0.0).score == 0.0
        assert _Model(score=0.5).score == 0.5
        assert _Model(score=1.0).score == 1.0
        assert _Model(score=0.87).score == 0.87

    def test_int_coercion(self):
        assert _Model(score=0).score == 0.0
        assert _Model(score=1).score == 1.0

    def test_out_of_range_rejection(self):
        with pytest.raises(ValidationError) as exc_info:
            _Model(score=-0.1)
        assert "between 0.0 and 1.0" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            _Model(score=1.1)
        assert "between 0.0 and 1.0" in str(exc_info.value)

    def test_non_finite_rejection(self):
        with pytest.raises(ValidationError) as exc_info:
            _Model(score=float("nan"))
        assert "finite" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            _Model(score=float("inf"))
        assert "finite" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            _Model(score=float("-inf"))
        assert "finite" in str(exc_info.value)

    def test_boundary_values(self):
        assert _Model(score=0.0).score == 0.0
        assert _Model(score=1.0).score == 1.0
