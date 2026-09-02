"""Tests for Verdict enum: canonical values, case-insensitive matching."""

from typing import Annotated

import pytest
from pydantic import BaseModel, BeforeValidator, ValidationError

from agentic_devtools.orchestration.schemas._enums import Verdict, normalize_verdict


class _VerdictModel(BaseModel):
    verdict: Annotated[Verdict, BeforeValidator(normalize_verdict)]


class TestVerdict:
    """Tests for Verdict enum normalization."""

    def test_canonical_values(self):
        assert _VerdictModel(verdict="approve").verdict == Verdict.APPROVE
        assert _VerdictModel(verdict="request_changes").verdict == Verdict.REQUEST_CHANGES

    def test_case_insensitive(self):
        assert _VerdictModel(verdict="APPROVE").verdict == Verdict.APPROVE
        assert _VerdictModel(verdict="Request_Changes").verdict == Verdict.REQUEST_CHANGES
        assert _VerdictModel(verdict="REQUEST_CHANGES").verdict == Verdict.REQUEST_CHANGES

    def test_unknown_rejection(self):
        with pytest.raises(ValidationError) as exc_info:
            _VerdictModel(verdict="reject")
        assert "Invalid verdict value" in str(exc_info.value)

    def test_enum_instance_passthrough(self):
        result = _VerdictModel(verdict=Verdict.APPROVE)
        assert result.verdict == Verdict.APPROVE

    def test_non_string_passthrough(self):
        result = normalize_verdict(42)
        assert result == 42
