"""Tests for validate_file() (FR-007, --file mode)."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_devtools.cli.issue_template.validate_templates import validate_file


class TestValidateFile:
    """Tests for single-file validation."""

    def test_missing_file_emits_e002(self, tmp_path: Path) -> None:
        """A non-existent file yields an E002 error."""
        summary = validate_file(tmp_path / "nope.md")
        assert summary.templates_checked == 1
        assert [d.code for d in summary.results[0].diagnostics] == ["E002"]
        assert summary.error_count == 1

    def test_directory_path_emits_e002(self, tmp_path: Path) -> None:
        """A directory path yields E002 instead of raising."""
        template_dir = tmp_path / "template-dir.md"
        template_dir.mkdir()
        summary = validate_file(template_dir)
        assert [d.code for d in summary.results[0].diagnostics] == ["E002"]
        assert summary.error_count == 1

    def test_invalid_utf8_file_emits_e002(self, tmp_path: Path) -> None:
        """A non-UTF-8 file yields E002 instead of raising."""
        template = tmp_path / "t.md"
        template.write_bytes(b"\xff")
        summary = validate_file(template)
        assert [d.code for d in summary.results[0].diagnostics] == ["E002"]
        assert summary.error_count == 1

    def test_base_schema_without_type(self, tmp_path: Path) -> None:
        """Without --type, coverage uses base required properties (title, description)."""
        template = tmp_path / "t.md"
        template.write_text("{{title}}", encoding="utf-8")
        summary = validate_file(template)
        codes = [d.code for d in summary.results[0].diagnostics]
        # description is required in the base schema but missing -> W002.
        assert "W002" in codes
        assert all(c != "E001" for c in codes)

    def test_valid_file_passes(self, tmp_path: Path) -> None:
        """A file covering the base required set has no diagnostics."""
        template = tmp_path / "t.md"
        template.write_text("{{title}} {{description}}", encoding="utf-8")
        summary = validate_file(template)
        assert summary.results[0].diagnostics == []

    def test_type_schema_from_project_json(self, tmp_path: Path) -> None:
        """With --type, type-specific schema properties become known/required."""
        template = tmp_path / "issue-template-bug.md"
        template.write_text("{{title}} {{description}} {{severity}}", encoding="utf-8")
        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True)
        (config_dir / "project.json").write_text(
            json.dumps(
                {
                    "issue_types_metadata": {
                        "PROJ": {
                            "issue_types": [
                                {
                                    "name": "Bug",
                                    "properties": [{"name": "severity", "required": True}],
                                }
                            ]
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        summary = validate_file(template, "bug", git_root=tmp_path)
        assert summary.warning_count == 0
        assert summary.error_count == 0
