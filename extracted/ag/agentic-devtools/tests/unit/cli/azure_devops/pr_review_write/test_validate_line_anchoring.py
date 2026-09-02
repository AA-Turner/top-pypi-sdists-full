"""Tests for validate_line_anchoring."""

from agentic_devtools.cli.azure_devops.pr_review_write import validate_line_anchoring


class TestValidateLineAnchoring:
    def test_non_dict(self):
        assert validate_line_anchoring("nope") == []

    def test_anchorable_mode_allows_lines(self):
        answer = {"reviewMode": "diff", "suggestions": [{"line": 5, "severity": "low", "content": "x"}]}
        assert validate_line_anchoring(answer) == []

    def test_suggestions_not_list(self):
        assert validate_line_anchoring({"reviewMode": "binary", "suggestions": "nope"}) == []

    def test_binary_rejects_line_suggestion(self):
        answer = {"reviewMode": "binary", "suggestions": [{"line": 5, "severity": "low", "content": "x"}]}
        errors = validate_line_anchoring(answer)
        assert any("not allowed for reviewMode 'binary'" in e for e in errors)

    def test_deleted_rejects_line_suggestion(self):
        answer = {"reviewMode": "deleted", "suggestions": [{"line": 1, "severity": "low", "content": "x"}]}
        assert validate_line_anchoring(answer)

    def test_out_of_scope_exempt(self):
        answer = {
            "reviewMode": "metadata-only",
            "suggestions": [{"out_of_scope": True, "severity": "low", "content": "x"}],
        }
        assert validate_line_anchoring(answer) == []

    def test_non_dict_suggestion_skipped(self):
        assert validate_line_anchoring({"reviewMode": "binary", "suggestions": ["nope"]}) == []

    def test_no_line_allowed(self):
        answer = {
            "reviewMode": "binary",
            "suggestions": [{"out_of_scope": False, "severity": "low", "content": "x"}],
        }
        assert validate_line_anchoring(answer) == []
