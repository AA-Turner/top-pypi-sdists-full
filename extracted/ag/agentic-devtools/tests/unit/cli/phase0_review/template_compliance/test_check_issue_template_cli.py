"""Tests for the issue.md compliance command."""

from pathlib import Path

import pytest

from agentic_devtools.cli.phase0_review.template_compliance import check_issue_template_cli


def test_check_issue_template_cli_returns_zero_for_warnings_only(tmp_path: Path, monkeypatch, capsys) -> None:
    issue = tmp_path / "issue.md"
    issue.write_text(
        (
            '---\nid: "1"\ntitle: "Title"\ntype: "task"\nstatus: "open"\n'
            'provider: "github"\nlabels: []\nrendered_at: "now"\n---\n# Title\n\n'
            "## Description\nText\n"
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["agdt-check-issue-template", "--file", str(issue)])

    with pytest.raises(SystemExit) as exc:
        check_issue_template_cli()

    assert exc.value.code == 0
    assert "warning(s)" in capsys.readouterr().err


def test_check_issue_template_cli_returns_one_for_errors(tmp_path: Path, monkeypatch, capsys) -> None:
    issue = tmp_path / "issue.md"
    issue.write_text("", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["agdt-check-issue-template", "--file", str(issue)])

    with pytest.raises(SystemExit) as exc:
        check_issue_template_cli()

    assert exc.value.code == 1
    assert "error(s)" in capsys.readouterr().err
