"""Tests for YAML frontmatter validation."""

from unittest.mock import patch

from agentic_devtools.cli.phase0_review import helpers
from agentic_devtools.cli.phase0_review.helpers import frontmatter_validate


def test_frontmatter_validates_delimiters_yaml_fields_and_order():
    snapshot = "---\nid: {{id}}\ntitle: {{title}}\n---\n# Body"
    good = '---\nid: "1"\ntitle: "T"\n---\n# Body'
    findings, parsed = frontmatter_validate(snapshot, good)
    assert findings == []
    assert parsed == {"id": "1", "title": "T"}

    findings, _ = frontmatter_validate(snapshot, "# no frontmatter")
    assert "delimiter" in findings[0][1]

    bad = "---\ntitle: [\nid: 1\n---\n"
    findings, _ = frontmatter_validate(snapshot, bad)
    assert len(findings) >= 2

    findings, parsed = frontmatter_validate("", "---\n[]\n---\n")
    assert parsed == {}
    assert any("mapping" in expected for expected, _ in findings)

    findings, _ = frontmatter_validate("---\n---\n", "---\nid: 1\nextra: x\n---\n")
    assert any("field order" in expected for expected, _ in findings)
    assert any("unexpected" in expected for expected, _ in findings)

    duplicate = "---\nid: 1\nid: 2\ntitle: T\n---\n"
    findings, _ = frontmatter_validate(snapshot, duplicate)
    assert any("occurs once" in expected for expected, _ in findings)

    with patch.object(helpers, "split_frontmatter", return_value=(None, "", None)):
        findings, _ = frontmatter_validate(snapshot, good)
    assert findings == [("valid YAML frontmatter delimiters", "frontmatter was not extracted")]
