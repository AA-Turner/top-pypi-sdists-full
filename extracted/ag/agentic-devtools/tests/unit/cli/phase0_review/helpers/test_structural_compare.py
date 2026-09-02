"""Tests for canonical structural comparison."""

from agentic_devtools.cli.phase0_review.helpers import (
    coerce_value,
    encode_table_cell,
    normalize_text,
    resolve_safe_path,
    split_frontmatter,
    structural_compare,
)


def test_structural_compare_ignores_blank_multiplicity_and_reports_deviations():
    snapshot = "# Title  \n\n\nValue: {{title}}\n"
    issue = "# Title\n\nValue: X\n"
    matching = structural_compare(snapshot, issue, {"title": "X"})
    assert matching.findings == []
    assert matching.captures == {"title": ["X"]}

    changed = structural_compare(snapshot, "# Wrong\nValue: X\nExtra", {"title": "X"})
    assert len(changed.findings) == 3


def test_path_and_frontmatter_helper_error_branches(tmp_path):
    absolute, error = resolve_safe_path(str(tmp_path / "x"), tmp_path, require_relative=True)
    assert absolute is None
    assert error == "path must be repository-relative"

    missing_root, error = resolve_safe_path("x", tmp_path / "absent", require_relative=False)
    assert missing_root is None
    assert "outside" in error
    assert split_frontmatter("---\nno close")[2] == "closing YAML frontmatter delimiter is missing"


def test_structural_records_collapse_leading_and_repeated_blank_lines():
    result = structural_compare("# Title\n\nValue", "\n\n# Title\n\n\nValue", {})
    assert result.findings == []


def test_inline_multiline_source_is_malformed():
    result = structural_compare("Value: {{custom}}", "Value: first", {"properties": {"custom": "first\nsecond"}})
    assert result.malformed == [
        (
            "inline placeholder 'custom' resolves to single-line content",
            "source field is multiline-capable",
        )
    ]


def test_normalization_coercion_encoding_and_safe_path_branches(tmp_path):
    assert normalize_text(" \r\nvalue\r ") == "value"
    assert coerce_value(None) == ""
    assert coerce_value([True, 2]) == "True, 2"
    assert coerce_value("x") == "x"
    assert encode_table_cell("a\\b|c\nd") == "a\\\\b\\|c<br>d"

    resolved, error = resolve_safe_path(str(tmp_path / "file"), tmp_path, require_relative=False)
    assert resolved == tmp_path / "file"
    assert error is None
    (tmp_path / ".git").mkdir()
    resolved, error = resolve_safe_path(".git/config", tmp_path, require_relative=False)
    assert resolved is None
    assert ".git subtree" in error


def test_frontmatter_and_table_route_structural_branches():
    snapshot = "---\nid: {{id}}\n---\n| Key | {{custom}} |"
    issue = "---\nid: 1\n---\n| Key | value |"
    result = structural_compare(snapshot, issue, {"properties": {"custom": "value"}})
    assert result.findings == []
    assert result.table_fields == {"custom"}
