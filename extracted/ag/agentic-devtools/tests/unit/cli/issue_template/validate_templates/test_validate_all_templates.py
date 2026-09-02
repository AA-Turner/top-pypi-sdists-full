"""Tests for validate_all_templates() (FR-004, E002, E003, W003)."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_devtools.cli.issue_template.validate_templates import validate_all_templates


def _write_preset(preset_dir: Path, templates: list[str], files: dict[str, str]) -> None:
    """Create a preset.yml listing *templates* and write *files* under templates/."""
    preset_dir.mkdir(parents=True, exist_ok=True)
    templates_dir = preset_dir / "templates"
    templates_dir.mkdir(exist_ok=True)
    (preset_dir / "preset.yml").write_text(
        "templates:\n" + "".join(f"  - {name}\n" for name in templates),
        encoding="utf-8",
    )
    for name, content in files.items():
        (templates_dir / name).write_text(content, encoding="utf-8")


class TestValidateAllTemplates:
    """Tests for the directory-scanning orchestrator."""

    def test_none_preset_dir_emits_e003(self) -> None:
        """A None preset directory yields a command-level E003 diagnostic."""
        summary = validate_all_templates(None)
        assert summary.templates_checked == 0
        assert [d.code for d in summary.command_diagnostics] == ["E003"]

    def test_missing_preset_yml_emits_e003(self, tmp_path: Path) -> None:
        """A preset directory without preset.yml yields E003."""
        summary = validate_all_templates(tmp_path)
        assert [d.code for d in summary.command_diagnostics] == ["E003"]

    def test_happy_path_all_valid(self, tmp_path: Path, monkeypatch) -> None:
        """A directory of valid templates yields per-file pass results."""
        monkeypatch.chdir(tmp_path)
        preset = tmp_path / "presets"
        _write_preset(
            preset,
            ["issue-template.md"],
            {"issue-template.md": "{{title}}\n{{description}}\n"},
        )
        summary = validate_all_templates(preset, git_root=tmp_path)
        assert summary.templates_checked == 1
        assert summary.error_count == 0
        assert summary.results[0].status == "pass"

    def test_missing_registered_file_emits_e002(self, tmp_path: Path) -> None:
        """A registered template with no file on disk yields E002."""
        preset = tmp_path / "presets"
        _write_preset(preset, ["issue-template-bug.md"], {})
        summary = validate_all_templates(preset, git_root=tmp_path)
        assert summary.templates_checked == 1
        codes = [d.code for d in summary.results[0].diagnostics]
        assert codes == ["E002"]
        assert summary.results[0].status == "fail"

    def test_registered_directory_emits_e002(self, tmp_path: Path) -> None:
        """A registered template path that is a directory yields E002."""
        preset = tmp_path / "presets"
        _write_preset(preset, ["issue-template.md"], {})
        (preset / "templates" / "issue-template.md").mkdir()
        summary = validate_all_templates(preset, git_root=tmp_path)
        assert [d.code for d in summary.results[0].diagnostics] == ["E002"]

    def test_registered_invalid_utf8_emits_e002(self, tmp_path: Path) -> None:
        """A registered template with invalid UTF-8 content yields E002."""
        preset = tmp_path / "presets"
        _write_preset(preset, ["issue-template.md"], {})
        (preset / "templates" / "issue-template.md").write_bytes(b"\xff")
        summary = validate_all_templates(preset, git_root=tmp_path)
        assert [d.code for d in summary.results[0].diagnostics] == ["E002"]

    def test_empty_template_emits_w003(self, tmp_path: Path) -> None:
        """An empty registered template yields a W003 warning."""
        preset = tmp_path / "presets"
        _write_preset(preset, ["issue-template.md"], {"issue-template.md": "   "})
        summary = validate_all_templates(preset, git_root=tmp_path)
        assert [d.code for d in summary.results[0].diagnostics] == ["W003"]

    def test_type_filter_narrows_templates(self, tmp_path: Path) -> None:
        """A type filter only validates the matching type template."""
        preset = tmp_path / "presets"
        _write_preset(
            preset,
            ["issue-template.md", "issue-template-bug.md"],
            {
                "issue-template.md": "{{title}} {{description}}",
                "issue-template-bug.md": "{{title}} {{description}}",
            },
        )
        summary = validate_all_templates(preset, "bug", git_root=tmp_path)
        assert summary.templates_checked == 1
        assert summary.results[0].template_path.endswith("issue-template-bug.md")

    def test_type_filter_no_match_emits_e003(self, tmp_path: Path) -> None:
        """A type filter matching no registered template yields E003."""
        preset = tmp_path / "presets"
        _write_preset(
            preset,
            ["issue-template.md", "issue-template-bug.md"],
            {
                "issue-template.md": "{{title}} {{description}}",
                "issue-template-bug.md": "{{title}} {{description}}",
            },
        )
        summary = validate_all_templates(preset, "buug", git_root=tmp_path)
        assert summary.templates_checked == 0
        assert [d.code for d in summary.command_diagnostics] == ["E003"]

    def test_type_schema_from_project_json(self, tmp_path: Path) -> None:
        """Type-specific property names from project.json become known/required."""
        preset = tmp_path / "presets"
        _write_preset(
            preset,
            ["issue-template-bug.md"],
            {"issue-template-bug.md": "{{title}} {{description}} {{severity}}"},
        )
        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True)
        (config_dir / "project.json").write_text(
            json.dumps(
                {
                    "issue_types_metadata": {
                        "PROJ": {
                            "lastDiscovered": "2026-01-01T00:00:00+00:00",
                            "lastRefreshed": "2026-01-01T00:00:00+00:00",
                            "provider": "jira",
                            "issue_types": [
                                {
                                    "id": "1",
                                    "name": "Bug",
                                    "description": "",
                                    "is_subtask": False,
                                    "properties": [
                                        {
                                            "name": "severity",
                                            "display_name": "Severity",
                                            "type": "string",
                                            "required": True,
                                            "allowed_values": None,
                                            "included_in_template": True,
                                        }
                                    ],
                                }
                            ],
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        summary = validate_all_templates(preset, git_root=tmp_path)
        # severity is now a known placeholder and a covered required property.
        assert summary.error_count == 0
        assert summary.warning_count == 0
