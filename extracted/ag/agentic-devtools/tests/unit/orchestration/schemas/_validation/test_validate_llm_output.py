"""Tests for validate_llm_output() function."""

import json

import pytest

from agentic_devtools.orchestration.schemas._validation import (
    SchemaValidationError,
    validate_llm_output,
)
from agentic_devtools.orchestration.schemas.shared.stop_condition import StopCondition


class TestValidateLlmOutputValid:
    """Tests for validate_llm_output with valid input."""

    def test_valid_json_returns_model(self):
        raw = json.dumps({"reason": "Budget exceeded", "is_recoverable": True, "details": "Over limit"})
        result = validate_llm_output(StopCondition, raw)
        assert isinstance(result, StopCondition)
        assert result.reason == "Budget exceeded"
        assert result.is_recoverable is True

    def test_valid_json_with_defaults(self):
        raw = json.dumps({"reason": "Budget exceeded"})
        result = validate_llm_output(StopCondition, raw)
        assert result.is_recoverable is False
        assert result.details == ""

    def test_reversed_argument_order_raw_then_model(self):
        """Both (ModelClass, raw) and (raw, ModelClass) are supported."""
        raw = json.dumps({"reason": "Budget exceeded", "is_recoverable": True, "details": "Over limit"})
        result = validate_llm_output(raw, StopCondition)  # type: ignore[arg-type]
        assert isinstance(result, StopCondition)
        assert result.reason == "Budget exceeded"
        assert result.is_recoverable is True

    def test_reversed_argument_order_invalid_raises_error(self):
        """Error handling works correctly when using (raw, ModelClass) order."""
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_llm_output("not valid json", StopCondition)  # type: ignore[arg-type]
        assert exc_info.value.model_name == "StopCondition"

    def test_both_args_non_model_raises_type_error(self):
        """If neither argument is a BaseModel subclass, raises TypeError."""
        with pytest.raises(TypeError, match="Pydantic BaseModel subclass"):
            validate_llm_output("raw_text", "not_a_model")  # type: ignore[arg-type]


class TestValidateLlmOutputInvalid:
    """Tests for validate_llm_output with invalid input."""

    def test_unparseable_raises_error(self):
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_llm_output(StopCondition, "This is just prose with no JSON at all.")
        assert exc_info.value.model_name == "StopCondition"

    def test_missing_required_field(self):
        raw = json.dumps({"is_recoverable": True})
        with pytest.raises(SchemaValidationError):
            validate_llm_output(StopCondition, raw)

    def test_include_raw_on_error(self):
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_llm_output(StopCondition, "bad", include_raw_on_error=True)
        assert exc_info.value.full_raw_input == "bad"

    def test_invalid_json_gives_json_invalid_error(self):
        """Lines 113-114: ValueError branch when JSON parsing fails with non-ValidationError."""
        from unittest.mock import patch

        # Mock model_validate_json to raise plain ValueError (not ValidationError)
        # to cover the except ValueError branch in error collection
        call_count = 0

        def mock_validate_json(raw):
            nonlocal call_count
            call_count += 1
            if call_count <= 1:
                # First call (direct parse attempt) - raise ValueError
                raise ValueError("Not valid JSON")
            # Second call (error collection) - raise ValueError again
            raise ValueError("Still not valid JSON")

        with patch.object(StopCondition, "model_validate_json", side_effect=mock_validate_json):
            with pytest.raises(SchemaValidationError) as exc_info:
                validate_llm_output(StopCondition, "not json at all")
        assert exc_info.value.model_name == "StopCondition"
        assert any("Invalid JSON" in str(e.get("msg", "")) for e in exc_info.value.errors)
        assert all("input" not in error for error in exc_info.value.errors)

    def test_validation_error_input_key_stripped_by_default(self):
        """ValidationError path: 'input' key must not appear in errors by default.

        Pydantic's error dicts include an ``input`` key containing the offending
        value.  When ``include_raw_on_error=False`` (the default), that key must
        be stripped to prevent accidental leakage of the raw LLM response.
        """
        # Valid JSON but missing the required 'reason' field → triggers ValidationError
        raw = json.dumps({"is_recoverable": True})
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_llm_output(StopCondition, raw)
        assert all("input" not in err for err in exc_info.value.errors)

    def test_validation_error_input_key_preserved_when_include_raw_on_error_true(self):
        """ValidationError path: 'input' key is preserved when ``include_raw_on_error=True``."""
        raw = json.dumps({"is_recoverable": True})
        with pytest.raises(SchemaValidationError) as exc_info:
            validate_llm_output(StopCondition, raw, include_raw_on_error=True)
        assert any("input" in err for err in exc_info.value.errors)


class TestValidateLlmOutputFallback:
    """Tests for validate_llm_output with fallback strategies."""

    def test_code_fence_extraction(self):
        raw = "Here's the result:\n```json\n" + json.dumps({"reason": "Done"}) + "\n```\nEnd."
        result = validate_llm_output(StopCondition, raw)
        assert result.reason == "Done"

    def test_bom_stripping(self):
        raw = "\ufeff" + json.dumps({"reason": "BOM test"})
        result = validate_llm_output(StopCondition, raw)
        assert result.reason == "BOM test"

    def test_trailing_comma_removal(self):
        raw = '{"reason": "trailing comma test",}'
        result = validate_llm_output(StopCondition, raw)
        assert result.reason == "trailing comma test"
