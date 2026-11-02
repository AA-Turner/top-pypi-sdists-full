"""Tests for validate_suggestion."""

from agentic_devtools.cli.azure_devops.pr_review_write import validate_suggestion


class TestValidateSuggestion:
    def test_valid_full_suggestion(self):
        suggestion = {
            "line": 42,
            "severity": "high",
            "content": "Guard against null.",
            "replacement_code": "if (x == null) return;",
            "lineSide": "right",
            "endLine": 44,
            "out_of_scope": False,
        }
        assert validate_suggestion(suggestion, 0) == []

    def test_minimal_valid_suggestion(self):
        assert validate_suggestion({"line": 5, "severity": "low", "content": "x"}, 0) == []

    def test_non_dict(self):
        assert validate_suggestion("nope", 1) == ["suggestions[1]: must be an object"]

    def test_invalid_severity(self):
        errors = validate_suggestion({"line": 1, "severity": "critical", "content": "x"}, 0)
        assert any("severity" in e for e in errors)

    def test_empty_content(self):
        errors = validate_suggestion({"line": 1, "severity": "low", "content": "   "}, 0)
        assert any("content" in e for e in errors)

    def test_out_of_scope_non_bool(self):
        errors = validate_suggestion({"severity": "low", "content": "x", "out_of_scope": "yes"}, 0)
        assert any("out_of_scope" in e for e in errors)

    def test_line_required_when_not_out_of_scope(self):
        errors = validate_suggestion({"severity": "low", "content": "x"}, 0)
        assert any("line is required" in e for e in errors)

    def test_line_optional_when_out_of_scope(self):
        assert validate_suggestion({"severity": "low", "content": "x", "out_of_scope": True}, 0) == []

    def test_line_non_int(self):
        errors = validate_suggestion({"line": "5", "severity": "low", "content": "x"}, 0)
        assert any("line must be an integer" in e for e in errors)

    def test_line_bool_rejected(self):
        errors = validate_suggestion({"line": True, "severity": "low", "content": "x"}, 0)
        assert any("line must be an integer" in e for e in errors)

    def test_line_below_one_rejected(self):
        errors = validate_suggestion({"line": 0, "severity": "low", "content": "x"}, 0)
        assert any("line must be >= 1" in e for e in errors)

    def test_end_line_below_one_rejected(self):
        errors = validate_suggestion({"line": 1, "severity": "low", "content": "x", "endLine": 0}, 0)
        assert any("endLine must be >= 1" in e for e in errors)

    def test_end_line_non_int(self):
        errors = validate_suggestion({"line": 5, "severity": "low", "content": "x", "endLine": "9"}, 0)
        assert any("endLine must be an integer" in e for e in errors)

    def test_end_line_less_than_line(self):
        errors = validate_suggestion({"line": 9, "severity": "low", "content": "x", "endLine": 5}, 0)
        assert any("endLine must be >= line" in e for e in errors)

    def test_end_line_ignored_when_line_non_int(self):
        errors = validate_suggestion({"line": "x", "severity": "low", "content": "x", "endLine": 5}, 0)
        assert all("endLine must be >= line" not in e for e in errors)

    def test_invalid_line_side(self):
        errors = validate_suggestion({"line": 1, "severity": "low", "content": "x", "lineSide": "middle"}, 0)
        assert any("lineSide" in e for e in errors)

    def test_end_line_without_line_rejected(self):
        errors = validate_suggestion({"severity": "low", "content": "x", "out_of_scope": True, "endLine": 5}, 0)
        assert any("endLine is only valid when line is provided" in e for e in errors)

    def test_line_side_without_line_rejected(self):
        errors = validate_suggestion({"severity": "low", "content": "x", "out_of_scope": True, "lineSide": "right"}, 0)
        assert any("lineSide is only valid when line is provided" in e for e in errors)

    def test_replacement_code_non_str(self):
        errors = validate_suggestion({"line": 1, "severity": "low", "content": "x", "replacement_code": 5}, 0)
        assert any("replacement_code" in e for e in errors)
