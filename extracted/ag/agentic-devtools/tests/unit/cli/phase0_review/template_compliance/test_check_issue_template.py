"""Tests for rendered issue.md template compliance."""

from pathlib import Path

from agentic_devtools.cli.phase0_review.template_compliance import check_issue_template


def _write_issue(path: Path, frontmatter: str, body: str) -> None:
    path.write_text(f"---\n{frontmatter}\n---\n{body}", encoding="utf-8")


def test_check_issue_template_reports_clean_required_structure(tmp_path: Path) -> None:
    issue = tmp_path / "issue.md"
    _write_issue(
        issue,
        (
            'id: "1"\ntitle: "Title"\ntype: "task"\nstatus: "open"\n'
            'provider: "github"\nlabels: []\nrendered_at: "2026-01-01T00:00:00+00:00"'
        ),
        (
            "# Title\n\n## Description\n\nText\n\n## Dependencies\n\nNone\n\n"
            "## Constraints\n\nNone\n\n## Properties\n\nNone\n\n## Provenance\n\nNone\n"
        ),
    )

    assert check_issue_template(issue) == []


def test_check_issue_template_distinguishes_warnings_from_errors(tmp_path: Path) -> None:
    issue = tmp_path / "issue.md"
    _write_issue(
        issue,
        (
            'id: "1"\ntitle: "Title"\ntype: "task"\nstatus: "open"\n'
            'provider: "github"\nlabels: []\nrendered_at: "2026-01-01T00:00:00+00:00"'
        ),
        "# Title\n\n## Description\n\nText\n",
    )

    diagnostics = check_issue_template(issue)

    assert diagnostics
    assert all(item["level"] == "warning" for item in diagnostics)
    assert any("optional section" in item["message"] for item in diagnostics)


def test_check_issue_template_reports_all_schema_and_heading_errors(tmp_path: Path) -> None:
    issue = tmp_path / "issue.md"
    issue.write_text(
        "---\ntitle: [\nunknown: true\nlabels: bad\n---\n### Wrong\n",
        encoding="utf-8",
    )

    diagnostics = check_issue_template(issue, expected_sections=("Description", "Missing"))
    messages = {item["message"] for item in diagnostics}

    assert any(item["level"] == "error" for item in diagnostics)
    assert "missing required section '## Description'" in messages
    assert "missing required section '## Missing'" in messages
    assert any("not valid YAML" in message for message in messages)
    assert any("optional section" in message for message in messages)
    assert any("level-one title" in message for message in messages)


def test_check_issue_template_reports_unreadable_and_delimiter_errors(tmp_path: Path) -> None:
    missing = check_issue_template(tmp_path / "missing.md")
    assert missing[0]["level"] == "error"

    issue = tmp_path / "issue.md"
    issue.write_text("no frontmatter", encoding="utf-8")
    diagnostics = check_issue_template(issue)
    assert any("opening frontmatter" in item["message"] for item in diagnostics)
    assert any("cannot be validated" in item["message"] for item in diagnostics)


def test_check_issue_template_reports_schema_types_and_formatting_drift(tmp_path: Path) -> None:
    issue = tmp_path / "issue.md"
    issue.write_text(
        "---\n"
        "id: 1\n"
        "title: Title\n"
        "type: task\n"
        "status: open\n"
        "provider: github\n"
        "labels: [1]\n"
        "rendered_at: 1\n"
        "---\n"
        "# Title\n"
        "### Description\n"
        "## Description\n"
        "#Title\n",
        encoding="utf-8",
    )

    diagnostics = check_issue_template(issue)

    assert any("must be a string" in item["message"] for item in diagnostics)
    assert any("list of strings" in item["message"] for item in diagnostics)
    assert any("level-two" in item["message"] for item in diagnostics)
    assert any("duplicates" in item["message"] for item in diagnostics)


def test_check_issue_template_reports_non_mapping_and_missing_closing_delimiter(tmp_path: Path) -> None:
    non_mapping = tmp_path / "non-mapping.md"
    non_mapping.write_text("---\n[]\n---\n# Title\n", encoding="utf-8")
    assert any("must be a mapping" in item["message"] for item in check_issue_template(non_mapping))

    missing_closing = tmp_path / "missing-closing.md"
    missing_closing.write_text("---\nid: 1\n", encoding="utf-8")
    diagnostics = check_issue_template(missing_closing)
    assert any("closing frontmatter" in item["message"] for item in diagnostics)

    missing_field = tmp_path / "missing-field.md"
    missing_field.write_text("---\nid: '1'\n---\n# Title\n## Description\n", encoding="utf-8")
    assert any("missing required frontmatter field" in item["message"] for item in check_issue_template(missing_field))
