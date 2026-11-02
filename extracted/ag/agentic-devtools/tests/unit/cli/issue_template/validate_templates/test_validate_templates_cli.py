"""Tests for validate_templates_cli() (FR-005, FR-006, FR-007, NFR-002)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentic_devtools.cli.issue_template import validate_templates as vt
from agentic_devtools.cli.issue_template.validate_templates import validate_templates_cli


def _make_preset(tmp_path: Path, files: dict[str, str]) -> Path:
    preset = tmp_path / "presets"
    templates = preset / "templates"
    templates.mkdir(parents=True)
    (preset / "preset.yml").write_text(
        "templates:\n" + "".join(f"  - {name}\n" for name in files),
        encoding="utf-8",
    )
    for name, content in files.items():
        (templates / name).write_text(content, encoding="utf-8")
    return preset


class TestValidateTemplatesCli:
    """Tests for the argparse CLI entry point."""

    def test_preset_dir_human_output_to_stderr_exit_zero(self, tmp_path: Path, monkeypatch, capsys) -> None:
        """Human-readable output goes to stderr and exits 0 when clean."""
        preset = _make_preset(tmp_path, {"issue-template.md": "{{title}} {{description}}"})
        monkeypatch.setattr("sys.argv", ["agdt-validate-templates", "--preset-dir", str(preset)])
        with pytest.raises(SystemExit) as exc:
            validate_templates_cli()
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "Checked 1 template(s)" in captured.err

    def test_json_output_to_stdout(self, tmp_path: Path, monkeypatch, capsys) -> None:
        """JSON output goes to stdout and is parseable."""
        preset = _make_preset(tmp_path, {"issue-template.md": "{{title}} {{description}}"})
        monkeypatch.setattr(
            "sys.argv",
            ["agdt-validate-templates", "--preset-dir", str(preset), "--json"],
        )
        with pytest.raises(SystemExit) as exc:
            validate_templates_cli()
        assert exc.value.code == 0
        parsed = json.loads(capsys.readouterr().out)
        assert parsed["summary"]["templates_checked"] == 1

    def test_error_exits_one(self, tmp_path: Path, monkeypatch, capsys) -> None:
        """A syntax error yields exit code 1."""
        preset = _make_preset(tmp_path, {"issue-template.md": "{{title}} {{bad"})
        monkeypatch.setattr("sys.argv", ["agdt-validate-templates", "--preset-dir", str(preset)])
        with pytest.raises(SystemExit) as exc:
            validate_templates_cli()
        assert exc.value.code == 1

    def test_strict_promotes_warnings_to_exit_one(self, tmp_path: Path, monkeypatch, capsys) -> None:
        """--strict makes warning-only results exit 1."""
        preset = _make_preset(tmp_path, {"issue-template.md": "{{title}} {{description}} {{oops}}"})
        monkeypatch.setattr(
            "sys.argv",
            ["agdt-validate-templates", "--preset-dir", str(preset), "--strict"],
        )
        with pytest.raises(SystemExit) as exc:
            validate_templates_cli()
        assert exc.value.code == 1

    def test_file_mode(self, tmp_path: Path, monkeypatch, capsys) -> None:
        """--file validates a single template file."""
        template = tmp_path / "t.md"
        template.write_text("{{title}} {{description}}", encoding="utf-8")
        monkeypatch.setattr("sys.argv", ["agdt-validate-templates", "--file", str(template)])
        with pytest.raises(SystemExit) as exc:
            validate_templates_cli()
        assert exc.value.code == 0
        assert "Checked 1 template(s)" in capsys.readouterr().err

    def test_file_mode_with_type(self, tmp_path: Path, monkeypatch, capsys) -> None:
        """--file with --type uses the type-specific schema branch."""
        template = tmp_path / "issue-template-bug.md"
        template.write_text("{{title}} {{description}}", encoding="utf-8")
        monkeypatch.setattr(
            "sys.argv",
            ["agdt-validate-templates", "--file", str(template), "--type", "bug"],
        )
        with pytest.raises(SystemExit) as exc:
            validate_templates_cli()
        assert exc.value.code == 0

    def test_file_mode_json_directory_path_exits_one_with_e002(self, tmp_path: Path, monkeypatch, capsys) -> None:
        """--file --json with a directory returns structured E002 output."""
        template_dir = tmp_path / "t.md"
        template_dir.mkdir()
        monkeypatch.setattr(
            "sys.argv",
            ["agdt-validate-templates", "--file", str(template_dir), "--json"],
        )
        with pytest.raises(SystemExit) as exc:
            validate_templates_cli()
        assert exc.value.code == 1
        parsed = json.loads(capsys.readouterr().out)
        assert parsed["summary"]["errors"] == 1
        assert parsed["results"][0]["diagnostics"][0]["code"] == "E002"

    def test_no_preset_dir_arg_uses_resolver(self, tmp_path: Path, monkeypatch, capsys) -> None:
        """Without --preset-dir the resolver is used (returns None -> E003, exit 1)."""
        monkeypatch.setattr(vt, "resolve_preset_dir", lambda arg: None)
        monkeypatch.setattr("sys.argv", ["agdt-validate-templates"])
        with pytest.raises(SystemExit) as exc:
            validate_templates_cli()
        assert exc.value.code == 1
        assert "E003" in capsys.readouterr().err

    def test_json_mode_malformed_preset_yml_exits_one_with_e003(self, tmp_path: Path, monkeypatch, capsys) -> None:
        """Malformed preset.yml in JSON mode returns structured E003 output."""
        preset = tmp_path / "presets"
        preset.mkdir(parents=True)
        (preset / "preset.yml").write_text("templates:\n  - issue-template.md\n  - [\n", encoding="utf-8")
        monkeypatch.setattr(
            "sys.argv",
            ["agdt-validate-templates", "--preset-dir", str(preset), "--json"],
        )
        with pytest.raises(SystemExit) as exc:
            validate_templates_cli()
        assert exc.value.code == 1
        parsed = json.loads(capsys.readouterr().out)
        assert parsed["summary"]["errors"] == 1
        assert parsed["diagnostics"][0]["code"] == "E003"
