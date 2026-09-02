"""Tests for map_suggestion."""

import pytest

from agentic_devtools.cli.azure_devops.pr_review_submit_mapper import MapperError, map_suggestion


class TestMapSuggestion:
    def test_maps_basic_line_suggestion(self):
        mapped = map_suggestion({"line": 42, "severity": "high", "content": "Guard null."}, "diff")
        assert mapped == {
            "line": 42,
            "end_line": 42,
            "severity": "high",
            "content": "Guard null.",
            "out_of_scope": False,
        }

    def test_uses_explicit_end_line(self):
        mapped = map_suggestion({"line": 10, "endLine": 14, "severity": "low", "content": "x"}, "diff")
        assert mapped["end_line"] == 14

    def test_includes_link_text_when_present(self):
        mapped = map_suggestion(
            {"line": 1, "severity": "low", "content": "x", "link_text": "see here"},
            "diff",
        )
        assert mapped["link_text"] == "see here"

    def test_blank_link_text_is_skipped(self):
        mapped = map_suggestion(
            {"line": 1, "severity": "low", "content": "x", "link_text": "   "},
            "diff",
        )
        assert "link_text" not in mapped

    def test_non_string_link_text_raises(self):
        with pytest.raises(MapperError):
            map_suggestion({"line": 1, "severity": "low", "content": "x", "link_text": 5}, "diff")

    def test_applies_replacement_code_fence(self):
        mapped = map_suggestion(
            {"line": 1, "severity": "high", "content": "Fix", "replacement_code": "return 1;"},
            "diff",
        )
        assert mapped["content"] == "Fix\n\n```suggestion\nreturn 1;\n```"

    def test_out_of_scope_without_line_is_skipped(self):
        assert map_suggestion({"out_of_scope": True, "severity": "low", "content": "x"}, "diff") is None

    def test_missing_line_without_out_of_scope_raises(self):
        with pytest.raises(MapperError):
            map_suggestion({"severity": "low", "content": "x"}, "diff")

    def test_line_anchored_on_forbidden_mode_raises(self):
        with pytest.raises(MapperError):
            map_suggestion({"line": 3, "severity": "high", "content": "x"}, "binary")

    def test_out_of_scope_with_line_allowed_on_forbidden_mode(self):
        mapped = map_suggestion(
            {"line": 3, "severity": "high", "content": "x", "out_of_scope": True},
            "deleted",
        )
        assert mapped["out_of_scope"] is True
        assert mapped["line"] == 3
