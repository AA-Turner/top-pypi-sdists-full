"""Tests for occurrence-aware placeholder boundaries."""

from agentic_devtools.cli.phase0_review.helpers import structural_compare


def test_boundary_uses_occurrence_after_source_collisions():
    snapshot = "{{description}}\n## Next\nend"
    issue = "first\n## Next\nlast\n## Next\nend"
    result = structural_compare(snapshot, issue, {"body": "first\n## Next\nlast"})
    assert result.findings == []
    assert result.captures["description"] == ["first\n## Next\nlast"]


def test_adjacent_placeholder_only_lines_are_malformed():
    result = structural_compare("{{title}}\n{{description}}\n# End", "x\ny\n# End", {})
    assert result.malformed


def test_last_placeholder_consumes_remaining_lines_and_missing_successor_is_reported():
    last = structural_compare("# Start\n{{custom}}", "# Start\none\ntwo", {"properties": {"custom": ["one", "two"]}})
    assert last.captures["custom"] == ["one\ntwo"]

    missing = structural_compare("{{unknown}}\n# End", "value", {})
    assert any("successor structural line is missing" in observed for _, observed in missing.findings)


def test_missing_and_extra_rendered_lines_are_individual_findings():
    missing = structural_compare("# One\n# Two", "# One", {})
    assert missing.findings == [("structural line '# Two' is present", "line is missing")]
    extra = structural_compare("# One", "# One\n# Extra", {})
    assert extra.findings == [("no extra structural line", "found '# Extra'")]


def test_issue_without_frontmatter_uses_whole_document_body():
    result = structural_compare("# {{title}}", "# Example", {"title": "Example"})
    assert result.findings == []
    assert result.captures == {"title": ["Example"]}


def test_property_value_disambiguates_placeholder_boundary():
    snapshot = "{{custom}}\n# End"
    issue = "value\n# End\n# End"
    result = structural_compare(
        snapshot,
        issue,
        {"properties": {"custom": "value\n# End"}},
    )
    assert result.captures["custom"] == ["value\n# End"]
