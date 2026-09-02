"""Tests for EscalationCategory enum."""

from typing import Annotated

import pytest
from pydantic import BaseModel, BeforeValidator, ValidationError

from agentic_devtools.orchestration.schemas._enums import (
    EscalationCategory,
    normalize_escalation_category,
)


class _Model(BaseModel):
    category: Annotated[EscalationCategory, BeforeValidator(normalize_escalation_category)]


class TestEscalationCategory:
    """Tests for EscalationCategory enum normalization."""

    def test_canonical_values(self):
        for value in (
            "ambiguous_requirements",
            "security_concern",
            "architecture_decision",
            "policy_violation",
            "external_dependency",
            "budget_exceeded",
        ):
            result = _Model(category=value)
            assert result.category == EscalationCategory(value)

    def test_case_insensitive(self):
        assert _Model(category="AMBIGUOUS_REQUIREMENTS").category == EscalationCategory.AMBIGUOUS_REQUIREMENTS
        assert _Model(category="Security_Concern").category == EscalationCategory.SECURITY_CONCERN

    def test_unknown_rejection(self):
        with pytest.raises(ValidationError):
            _Model(category="unknown_category")

    def test_enum_instance_passthrough(self):
        result = _Model(category=EscalationCategory.SECURITY_CONCERN)
        assert result.category == EscalationCategory.SECURITY_CONCERN

    def test_non_string_passthrough(self):
        result = normalize_escalation_category(42)
        assert result == 42
