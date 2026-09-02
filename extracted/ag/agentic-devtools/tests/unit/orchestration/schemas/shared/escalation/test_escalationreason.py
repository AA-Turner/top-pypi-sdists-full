"""Tests for EscalationReason model."""

import json

from agentic_devtools.orchestration.schemas._enums import EscalationCategory
from agentic_devtools.orchestration.schemas.shared.escalation import EscalationReason


class TestEscalationReason:
    """Tests for EscalationReason construction and serialization."""

    def test_construction(self):
        reason = EscalationReason(
            category="ambiguous_requirements",
            description="Requirements are unclear",
        )
        assert reason.category == EscalationCategory.AMBIGUOUS_REQUIREMENTS
        assert reason.description == "Requirements are unclear"

    def test_optional_fields_default(self):
        reason = EscalationReason(
            category="security_concern",
            description="Potential SQL injection",
        )
        assert reason.context == ""
        assert reason.suggested_action == ""

    def test_model_dump(self):
        reason = EscalationReason(
            category="policy_violation",
            description="Exceeds line count",
            context="file.py:500",
            suggested_action="Split the file",
        )
        data = reason.model_dump()
        assert data["category"] == "policy_violation"
        assert data["description"] == "Exceeds line count"
        assert data["context"] == "file.py:500"

    def test_model_validate_json(self):
        raw = json.dumps(
            {
                "category": "budget_exceeded",
                "description": "Token limit reached",
            }
        )
        reason = EscalationReason.model_validate_json(raw)
        assert reason.category == EscalationCategory.BUDGET_EXCEEDED

    def test_case_insensitive_category(self):
        reason = EscalationReason(
            category="SECURITY_CONCERN",
            description="test",
        )
        assert reason.category == EscalationCategory.SECURITY_CONCERN
