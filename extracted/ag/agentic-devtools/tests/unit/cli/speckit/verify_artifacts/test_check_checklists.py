"""Tests for ``check_checklists()``."""

from pathlib import Path

from agentic_devtools.cli.speckit.verify_artifacts import CHECK_CHECKLIST, check_checklists

_VALID = """# Requirements Checklist

- [ ] CHK001 Requirement one is testable.
- [ ] CHK002 Requirement two is testable.
- [ ] CHK003 Requirement three is testable.
- [ ] CHK004 Requirement four is testable.
"""

_PROSE_ONLY = """# Requirements Checklist

This document explains the approach in prose without any checkbox items at all.
"""


class TestCheckChecklists:
    """Generated checklists must contain real checkbox items."""

    def test_no_violation_for_a_valid_checklist(self, tmp_path: Path) -> None:
        checklists = tmp_path / "checklists"
        checklists.mkdir()
        (checklists / "requirements.md").write_text(_VALID, encoding="utf-8")

        assert check_checklists(tmp_path) == []

    def test_flags_a_prose_only_checklist(self, tmp_path: Path) -> None:
        checklists = tmp_path / "checklists"
        checklists.mkdir()
        (checklists / "requirements.md").write_text(_PROSE_ONLY, encoding="utf-8")

        violations = check_checklists(tmp_path)

        assert len(violations) == 1
        assert violations[0].check == CHECK_CHECKLIST
        assert violations[0].artifact == "checklists/requirements.md"
        assert violations[0].detail

    def test_flags_a_deficient_checklist(self, tmp_path: Path) -> None:
        checklists = tmp_path / "checklists"
        checklists.mkdir()
        (checklists / "requirements.md").write_text("# Checklist\n\n- [ ] CHK001 Only one item.\n", encoding="utf-8")

        violations = check_checklists(tmp_path)

        assert len(violations) == 1
        assert violations[0].artifact == "checklists/requirements.md"

    def test_returns_empty_when_checklist_directory_is_absent(self, tmp_path: Path) -> None:
        assert check_checklists(tmp_path) == []

    def test_returns_empty_when_checklist_directory_is_empty(self, tmp_path: Path) -> None:
        (tmp_path / "checklists").mkdir()

        assert check_checklists(tmp_path) == []

    def test_ignores_non_markdown_files(self, tmp_path: Path) -> None:
        checklists = tmp_path / "checklists"
        checklists.mkdir()
        (checklists / "notes.txt").write_text("not a checklist", encoding="utf-8")

        assert check_checklists(tmp_path) == []

    def test_reports_each_deficient_file(self, tmp_path: Path) -> None:
        checklists = tmp_path / "checklists"
        checklists.mkdir()
        (checklists / "a.md").write_text(_PROSE_ONLY, encoding="utf-8")
        (checklists / "b.md").write_text(_PROSE_ONLY, encoding="utf-8")
        (checklists / "c.md").write_text(_VALID, encoding="utf-8")

        violations = check_checklists(tmp_path)

        assert {v.artifact for v in violations} == {"checklists/a.md", "checklists/b.md"}
