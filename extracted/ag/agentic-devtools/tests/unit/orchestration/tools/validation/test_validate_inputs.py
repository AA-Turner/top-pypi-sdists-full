"""Tests for input validation."""

from unittest.mock import patch

from agentic_devtools.orchestration.tools.validation import validate_inputs


class TestValidateInputs:
    """Tests for validate_inputs function."""

    def test_valid_inputs(self):
        """Returns None for valid inputs."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "count": {"type": "integer"},
            },
            "required": ["name"],
        }
        result = validate_inputs(schema, {"name": "test", "count": 5})
        assert result is None

    def test_missing_required_field(self):
        """Returns ToolResult with validation_error for missing field."""
        schema = {
            "type": "object",
            "properties": {
                "issue_key": {"type": "string"},
                "comment": {"type": "string"},
            },
            "required": ["issue_key", "comment"],
        }
        result = validate_inputs(schema, {"issue_key": "PROJ-123"})
        assert result is not None
        assert result.success is False
        assert result.error_type == "validation_error"
        assert "comment" in result.error_message

    def test_wrong_type(self):
        """Returns ToolResult with validation_error for type mismatch."""
        schema = {
            "type": "object",
            "properties": {
                "count": {"type": "integer"},
            },
        }
        result = validate_inputs(schema, {"count": "not_a_number"})
        assert result is not None
        assert result.success is False
        assert result.error_type == "validation_error"

    def test_empty_schema_accepts_anything(self):
        """Empty object schema accepts any object."""
        schema = {"type": "object"}
        result = validate_inputs(schema, {"any": "thing"})
        assert result is None

    def test_invalid_schema(self):
        """Returns error for invalid schema definition."""
        schema = {"type": "invalid_type_xyz"}
        result = validate_inputs(schema, {})
        assert result is not None
        assert result.success is False
        assert result.error_type == "validation_error"

    def test_non_json_serializable_schema(self):
        """Returns validation_error when schema cannot be JSON-serialized."""
        schema = {
            "type": "object",
            "properties": {
                "mode": {"enum": {"fast", "safe"}},
            },
        }
        result = validate_inputs(schema, {"mode": "fast"})
        assert result is not None
        assert result.success is False
        assert result.error_type == "validation_error"
        assert "not JSON serializable" in str(result.error_message)

    def test_stops_after_first_validation_error(self):
        """Stops consuming validation errors after the first one."""
        schema = {"type": "object"}
        first_error = type(
            "ValidationErrorStub",
            (),
            {"message": "first error", "absolute_path": ["field"]},
        )()

        def iter_errors(_inputs):
            yield first_error
            raise AssertionError("validate_inputs consumed extra errors")

        with patch("agentic_devtools.orchestration.tools.validation._get_validator") as mock_get_validator:
            mock_get_validator.return_value.iter_errors.side_effect = iter_errors

            result = validate_inputs(schema, {})

        assert result is not None
        assert result.success is False
        assert result.error_type == "validation_error"
        assert result.error_message == "first error (field: field)"
