"""Tests for SchemaValidationError exception class."""

from agentic_devtools.orchestration.schemas._validation import SchemaValidationError


class TestSchemaValidationError:
    """Tests for SchemaValidationError diagnostics."""

    def test_basic_construction(self):
        error = SchemaValidationError(
            model_name="FileReviewResult",
            raw_input='{"invalid": true}',
            errors=[{"loc": ("field",), "msg": "field required", "type": "missing"}],
        )
        assert error.model_name == "FileReviewResult"
        assert "FileReviewResult" in str(error)
        assert "field required" in str(error)

    def test_truncated_preview_under_200_bytes(self):
        short_input = '{"short": true}'
        error = SchemaValidationError(
            model_name="Test",
            raw_input=short_input,
            errors=[],
        )
        assert error.raw_input_preview == short_input

    def test_truncated_preview_over_200_bytes(self):
        long_input = "x" * 300
        error = SchemaValidationError(
            model_name="Test",
            raw_input=long_input,
            errors=[],
        )
        assert len(error.raw_input_preview.encode("utf-8")) <= 200
        assert error.raw_input_preview.endswith("...")

    def test_sha256_digest(self):
        import hashlib

        raw = "test input"
        error = SchemaValidationError(
            model_name="Test",
            raw_input=raw,
            errors=[],
        )
        expected = hashlib.sha256(raw.encode()).hexdigest()
        assert error.raw_input_digest == expected

    def test_field_path_errors(self):
        errors = [
            {"loc": ("findings", 0, "severity"), "msg": "invalid value", "type": "value_error"},
            {"loc": ("summary",), "msg": "field required", "type": "missing"},
        ]
        error = SchemaValidationError(
            model_name="FileReviewResult",
            raw_input="{}",
            errors=errors,
        )
        assert "findings.0.severity" in str(error)
        assert "summary" in str(error)

    def test_opt_in_raw_input(self):
        raw = "full raw content"
        error = SchemaValidationError(
            model_name="Test",
            raw_input=raw,
            errors=[],
            include_raw=True,
        )
        assert error.full_raw_input == raw

    def test_no_raw_input_by_default(self):
        error = SchemaValidationError(
            model_name="Test",
            raw_input="sensitive content",
            errors=[],
        )
        assert error.full_raw_input is None

    def test_loc_as_non_iterable(self):
        """Branch coverage for loc that is not a list/tuple."""
        errors = [{"loc": "single_string_loc", "msg": "some error", "type": "value_error"}]
        error = SchemaValidationError(
            model_name="Test",
            raw_input="{}",
            errors=errors,
        )
        assert "single_string_loc" in str(error)
