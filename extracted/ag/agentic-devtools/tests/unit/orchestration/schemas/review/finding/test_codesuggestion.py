"""Tests for CodeSuggestion model."""

from agentic_devtools.orchestration.schemas.review.finding import CodeSuggestion


class TestCodeSuggestion:
    """Tests for CodeSuggestion construction and serialization."""

    def test_construction(self):
        suggestion = CodeSuggestion(
            file_path="src/main.py",
            start_line=10,
            end_line=12,
            original_code="x = None",
            replacement_code="x = default_value",
        )
        assert suggestion.file_path == "src/main.py"
        assert suggestion.start_line == 10
        assert suggestion.end_line == 12

    def test_optional_explanation(self):
        suggestion = CodeSuggestion(
            file_path="f.py",
            start_line=1,
            end_line=1,
            original_code="a",
            replacement_code="b",
        )
        assert suggestion.explanation == ""

    def test_model_dump(self):
        suggestion = CodeSuggestion(
            file_path="f.py",
            start_line=1,
            end_line=2,
            original_code="old",
            replacement_code="new",
            explanation="Better naming",
        )
        data = suggestion.model_dump()
        assert data["file_path"] == "f.py"
        assert data["explanation"] == "Better naming"

    def test_round_trip(self):
        original = CodeSuggestion(
            file_path="f.py",
            start_line=1,
            end_line=1,
            original_code="a",
            replacement_code="b",
        )
        raw = original.model_dump_json()
        restored = CodeSuggestion.model_validate_json(raw)
        assert original == restored


class TestCodeSuggestionOptionalReplacement:
    """Tests for the optional replacement_code field (FR-014)."""

    def test_replacement_code_defaults_to_none(self):
        suggestion = CodeSuggestion(
            file_path="f.py",
            start_line=1,
            end_line=2,
            original_code="a",
        )
        assert suggestion.replacement_code is None

    def test_replacement_code_present(self):
        suggestion = CodeSuggestion(
            file_path="f.py",
            start_line=1,
            end_line=2,
            original_code="a",
            replacement_code="b",
        )
        assert suggestion.replacement_code == "b"

    def test_round_trip_without_replacement(self):
        original = CodeSuggestion(
            file_path="f.py",
            start_line=1,
            end_line=1,
            original_code="a",
        )
        restored = CodeSuggestion.model_validate_json(original.model_dump_json())
        assert original == restored
        assert restored.replacement_code is None
