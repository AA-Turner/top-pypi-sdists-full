"""Tests for discover_templates and bundled issue-template preset invariants."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from agentic_devtools.cli.issue_template.discovery import discover_templates
from agentic_devtools.cli.issue_template.exceptions import PresetLoadError


def _resolve_repo_root(start: Path) -> Path:
    """Resolve repository root by searching parents for the bundled preset path."""
    for candidate in (start, *start.parents):
        if (candidate / ".specify" / "presets" / "agdt-templates").is_dir():
            return candidate
    raise RuntimeError(f"Could not resolve repository root from {start}")


# Path to the real preset directory (used by template-content validation tests)
_REPO_ROOT = _resolve_repo_root(Path(__file__).resolve())
_PRESET_DIR = _REPO_ROOT / ".specify" / "presets" / "agdt-templates"
_TEMPLATE_PATH = _PRESET_DIR / "templates" / "issue-template.md"
_PRESET_YML_PATH = _PRESET_DIR / "preset.yml"


def _create_preset(
    tmp_path: Path,
    templates_list: list[str],
    *,
    create_files: list[str] | None = None,
) -> Path:
    """Create a preset directory with preset.yml and optional template files."""
    preset_dir = tmp_path / "preset"
    preset_dir.mkdir()
    templates_dir = preset_dir / "templates"
    templates_dir.mkdir()

    yml_content = "name: test-preset\ntemplates:\n"
    for t in templates_list:
        yml_content += f"  - {t}\n"

    (preset_dir / "preset.yml").write_text(yml_content, encoding="utf-8")

    files_to_create = create_files if create_files is not None else templates_list
    for f in files_to_create:
        (templates_dir / f).write_text(f"# {f}", encoding="utf-8")

    return preset_dir


class TestDiscoverTemplates:
    """Tests for the discover_templates function."""

    def test_registered_templates_found(self, tmp_path: Path) -> None:
        """Registered type-specific templates are discovered."""
        preset_dir = _create_preset(
            tmp_path,
            ["issue-template-bug.md", "issue-template-story.md", "issue-template.md"],
        )
        type_map, default = discover_templates(preset_dir)

        assert "bug" in type_map
        assert "story" in type_map
        assert type_map["bug"].name == "issue-template-bug.md"
        assert type_map["story"].name == "issue-template-story.md"

    def test_default_template_returned_separately(self, tmp_path: Path) -> None:
        """Default template is returned as second tuple element."""
        preset_dir = _create_preset(
            tmp_path,
            ["issue-template.md", "issue-template-bug.md"],
        )
        type_map, default = discover_templates(preset_dir)

        assert default is not None
        assert default.name == "issue-template.md"
        assert "bug" in type_map
        # Default is NOT in the type map
        assert "template" not in type_map

    def test_unregistered_file_ignored(self, tmp_path: Path) -> None:
        """Template file on disk but not in preset.yml is ignored."""
        preset_dir = _create_preset(
            tmp_path,
            ["issue-template-bug.md"],
            create_files=["issue-template-bug.md", "issue-template-story.md"],
        )
        type_map, _ = discover_templates(preset_dir)

        assert "bug" in type_map
        assert "story" not in type_map

    def test_duplicate_type_first_match_wins(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Duplicate type entries: first match wins with stderr warning."""
        preset_dir = _create_preset(
            tmp_path,
            ["issue-template-bug.md", "issue-template-bug.md"],
        )
        type_map, _ = discover_templates(preset_dir)
        captured = capsys.readouterr()

        assert "bug" in type_map
        assert "Duplicate" in captured.err

    def test_filename_convention_parsing(self, tmp_path: Path) -> None:
        """issue-template-{type_slug}.md convention is parsed correctly."""
        preset_dir = _create_preset(
            tmp_path,
            ["issue-template-user-story.md", "issue-template-feature.md"],
        )
        type_map, _ = discover_templates(preset_dir)

        assert "user-story" in type_map
        assert "feature" in type_map

    def test_non_issue_templates_ignored(self, tmp_path: Path) -> None:
        """Non-issue templates (e.g., spec-template.md) are ignored."""
        preset_dir = _create_preset(
            tmp_path,
            ["spec-template.md", "plan-template.md", "issue-template-bug.md"],
        )
        type_map, default = discover_templates(preset_dir)

        assert len(type_map) == 1
        assert "bug" in type_map
        assert default is None

    def test_missing_preset_yml_raises(self, tmp_path: Path) -> None:
        """Missing preset.yml raises PresetLoadError (FR-006)."""
        preset_dir = tmp_path / "empty-preset"
        preset_dir.mkdir()
        with pytest.raises(PresetLoadError, match="preset.yml not found"):
            discover_templates(preset_dir)

    def test_malformed_preset_yml_raises(self, tmp_path: Path) -> None:
        """Unparseable preset.yml raises PresetLoadError (FR-006)."""
        preset_dir = tmp_path / "preset"
        preset_dir.mkdir()
        # Invalid YAML: unbalanced brackets cause a parser error.
        (preset_dir / "preset.yml").write_text("templates: [unclosed\n", encoding="utf-8")
        with pytest.raises(PresetLoadError, match="Could not parse preset.yml"):
            discover_templates(preset_dir)

    def test_missing_template_file_on_disk(self, tmp_path: Path) -> None:
        """Registered template that doesn't exist on disk is not included."""
        preset_dir = _create_preset(
            tmp_path,
            ["issue-template-bug.md", "issue-template-story.md"],
            create_files=["issue-template-bug.md"],  # story file not created
        )
        type_map, _ = discover_templates(preset_dir)

        assert "bug" in type_map
        assert "story" not in type_map

    def test_non_dict_preset_data(self, tmp_path: Path) -> None:
        """Non-dict preset data returns empty results."""
        preset_dir = tmp_path / "preset"
        preset_dir.mkdir()
        (preset_dir / "preset.yml").write_text("just a string", encoding="utf-8")
        type_map, default = discover_templates(preset_dir)
        assert type_map == {}
        assert default is None

    def test_non_list_templates_value(self, tmp_path: Path) -> None:
        """Non-list templates value returns empty results."""
        preset_dir = tmp_path / "preset"
        preset_dir.mkdir()
        (preset_dir / "preset.yml").write_text("name: test\ntemplates: not-a-list\n", encoding="utf-8")
        type_map, default = discover_templates(preset_dir)
        assert type_map == {}
        assert default is None

    def test_non_string_entry_ignored(self, tmp_path: Path) -> None:
        """Non-string entries in templates list are ignored."""
        preset_dir = tmp_path / "preset"
        preset_dir.mkdir()
        templates_dir = preset_dir / "templates"
        templates_dir.mkdir()
        (templates_dir / "issue-template-bug.md").write_text("# Bug", encoding="utf-8")
        (preset_dir / "preset.yml").write_text(
            "name: test\ntemplates:\n  - 123\n  - issue-template-bug.md\n",
            encoding="utf-8",
        )
        type_map, _ = discover_templates(preset_dir)
        assert "bug" in type_map

    def test_default_template_not_on_disk(self, tmp_path: Path) -> None:
        """Default template registered but not on disk returns None."""
        preset_dir = tmp_path / "preset"
        preset_dir.mkdir()
        templates_dir = preset_dir / "templates"
        templates_dir.mkdir()
        # Register issue-template.md but don't create the file
        (preset_dir / "preset.yml").write_text(
            "name: test\ntemplates:\n  - issue-template.md\n",
            encoding="utf-8",
        )
        _, default = discover_templates(preset_dir)
        assert default is None

    def test_path_traversal_entry_ignored(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Entry with POSIX path separator (e.g. '../evil.md') is rejected."""
        preset_dir = tmp_path / "preset"
        preset_dir.mkdir()
        templates_dir = preset_dir / "templates"
        templates_dir.mkdir()

        # Create a legitimate template alongside the malicious entry
        (templates_dir / "issue-template-bug.md").write_text("# Bug", encoding="utf-8")
        (preset_dir / "preset.yml").write_text(
            "name: test\ntemplates:\n  - ../issue-template-evil.md\n  - issue-template-bug.md\n",
            encoding="utf-8",
        )

        type_map, _ = discover_templates(preset_dir)
        captured = capsys.readouterr()

        # Traversal entry must be rejected; legitimate entry must be found
        assert "bug" in type_map
        assert len(type_map) == 1
        assert "Warning" in captured.err
        assert "../issue-template-evil.md" in captured.err

    def test_path_traversal_windows_style_entry_ignored(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Entry with Windows path separator (e.g. '..\\evil.md') is rejected."""
        preset_dir = tmp_path / "preset"
        preset_dir.mkdir()
        templates_dir = preset_dir / "templates"
        templates_dir.mkdir()

        (templates_dir / "issue-template-bug.md").write_text("# Bug", encoding="utf-8")
        # The Python string literal `'..\\\\issue-template-evil.md'` contains four
        # backslashes, which write two literal backslashes to the file.  YAML then
        # parses the single-quoted value as the string `..\\issue-template-evil.md`
        # (two backslashes collapsed to one by YAML), which contains a `\\` separator.
        (preset_dir / "preset.yml").write_text(
            "name: test\ntemplates:\n  - '..\\\\issue-template-evil.md'\n  - issue-template-bug.md\n",
            encoding="utf-8",
        )

        type_map, _ = discover_templates(preset_dir)
        captured = capsys.readouterr()

        # Traversal entry must be rejected; legitimate entry must be found
        assert "bug" in type_map
        assert len(type_map) == 1
        assert "Warning" in captured.err

    def test_dot_segment_current_dir_entry_ignored(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """A bare '.' entry (current-directory dot-segment) is rejected (FR-007)."""
        preset_dir = tmp_path / "preset"
        preset_dir.mkdir()
        templates_dir = preset_dir / "templates"
        templates_dir.mkdir()
        (templates_dir / "issue-template-bug.md").write_text("# Bug", encoding="utf-8")
        (preset_dir / "preset.yml").write_text(
            "name: test\ntemplates:\n  - '.'\n  - issue-template-bug.md\n",
            encoding="utf-8",
        )

        type_map, _ = discover_templates(preset_dir)
        captured = capsys.readouterr()

        assert "bug" in type_map
        assert len(type_map) == 1
        assert "dot-segments" in captured.err

    def test_dot_dot_entry_escaping_templates_dir_ignored(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A bare '..' entry whose resolved path escapes templates/ is rejected (FR-007)."""
        preset_dir = tmp_path / "preset"
        preset_dir.mkdir()
        templates_dir = preset_dir / "templates"
        templates_dir.mkdir()
        (templates_dir / "issue-template-bug.md").write_text("# Bug", encoding="utf-8")
        (preset_dir / "preset.yml").write_text(
            "name: test\ntemplates:\n  - '..'\n  - issue-template-bug.md\n",
            encoding="utf-8",
        )

        type_map, _ = discover_templates(preset_dir)
        captured = capsys.readouterr()

        assert "bug" in type_map
        assert len(type_map) == 1
        assert "path escapes the templates directory" in captured.err

    def test_directory_named_like_template_excluded(self, tmp_path: Path) -> None:
        """A directory whose name matches issue-template-{slug}.md is not registered."""
        preset_dir = tmp_path / "preset"
        preset_dir.mkdir()
        templates_dir = preset_dir / "templates"
        templates_dir.mkdir()

        # Create a directory that looks like a template file
        dir_entry = templates_dir / "issue-template-bug.md"
        dir_entry.mkdir()

        (preset_dir / "preset.yml").write_text(
            "name: test\ntemplates:\n  - issue-template-bug.md\n",
            encoding="utf-8",
        )

        type_map, _ = discover_templates(preset_dir)

        # The directory must not appear in the type map
        assert "bug" not in type_map
        assert type_map == {}

    def test_directory_named_like_default_template_excluded(self, tmp_path: Path) -> None:
        """A directory named issue-template.md is not registered as the default."""
        preset_dir = tmp_path / "preset"
        preset_dir.mkdir()
        templates_dir = preset_dir / "templates"
        templates_dir.mkdir()

        # Create a directory that looks like the default template file
        dir_entry = templates_dir / "issue-template.md"
        dir_entry.mkdir()

        (preset_dir / "preset.yml").write_text(
            "name: test\ntemplates:\n  - issue-template.md\n",
            encoding="utf-8",
        )

        _, default = discover_templates(preset_dir)

        # The directory must not be registered as the default template
        assert default is None


_PLACEHOLDER_RE = re.compile(r"\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}")

_REQUIRED_PLACEHOLDERS = frozenset(
    {
        "id",
        "title",
        "type",
        "status",
        "provider",
        "labels",
        "description",
        "priority",
        "assignees",
        "created_at",
        "updated_at",
        "milestone",
        "component",
    }
)


class TestIssueTemplateFileExists:
    """Validate the issue-template.md file exists and meets basic constraints."""

    def test_file_exists(self) -> None:
        """Template file exists at the expected preset path."""
        assert _TEMPLATE_PATH.exists()

    def test_non_empty(self) -> None:
        """Template file is non-empty."""
        assert _TEMPLATE_PATH.stat().st_size > 0

    def test_valid_utf8(self) -> None:
        """Template file is valid UTF-8."""
        _TEMPLATE_PATH.read_text(encoding="utf-8")

    def test_under_5120_bytes(self) -> None:
        """Template file is under 5120 bytes."""
        assert _TEMPLATE_PATH.stat().st_size < 5120


class TestIssueTemplatePlaceholders:
    """Validate placeholder syntax and required placeholder set."""

    def test_at_least_13_distinct_placeholders(self) -> None:
        """Template contains at least 13 distinct placeholders."""
        content = _TEMPLATE_PATH.read_text(encoding="utf-8")
        names = set(_PLACEHOLDER_RE.findall(content))
        assert len(names) >= 13

    def test_all_required_placeholders_present(self) -> None:
        """All 13 required placeholder names are present."""
        content = _TEMPLATE_PATH.read_text(encoding="utf-8")
        names = set(_PLACEHOLDER_RE.findall(content))
        missing = _REQUIRED_PLACEHOLDERS - names
        assert not missing, f"Missing placeholders: {missing}"

    def test_no_jinja2_or_mustache_constructs(self) -> None:
        """Template uses only {{placeholder}} syntax, no Jinja2/Mustache."""
        content = _TEMPLATE_PATH.read_text(encoding="utf-8")
        assert "{%" not in content
        assert "%}" not in content
        assert "{{{" not in content
        assert "}}}" not in content


class TestIssueTemplateNoFrontmatter:
    """Validate that the template has no YAML frontmatter."""

    def test_no_leading_frontmatter(self) -> None:
        """First non-whitespace/non-comment content is not ---."""
        content = _TEMPLATE_PATH.read_text(encoding="utf-8")
        # Strip HTML comments and whitespace from the start
        stripped = re.sub(r"^\s*<!--.*?-->\s*", "", content, flags=re.DOTALL)
        assert not stripped.startswith("---")


class TestIssueTemplateSections:
    """Validate that all 4 required section headings are present."""

    def test_all_section_headings_present(self) -> None:
        """Template contains ## Metadata, ## Description, ## Properties, ## Provenance."""
        content = _TEMPLATE_PATH.read_text(encoding="utf-8")
        assert "## Metadata" in content
        assert "## Description" in content
        assert "## Properties" in content
        assert "## Provenance" in content


class TestIssueTemplateTableFormat:
    """Validate markdown table format in table sections."""

    @pytest.mark.parametrize("section", ["## Metadata", "## Properties", "## Provenance"])
    def test_section_has_markdown_table(self, section: str) -> None:
        """Each table section contains a pipe-delimited table with separator row."""
        content = _TEMPLATE_PATH.read_text(encoding="utf-8")
        # Extract section content (up to next ## heading or end)
        pattern = re.escape(section) + r"\n(.*?)(?=\n## |\Z)"
        match = re.search(pattern, content, re.DOTALL)
        assert match, f"Section {section} not found"
        section_content = match.group(1)
        # Check for pipe-delimited rows and separator
        assert "| --- | --- |" in section_content


class TestIssueTemplateNoRenderedAt:
    """Validate that {{rendered_at}} does not appear in template."""

    def test_no_rendered_at_placeholder(self) -> None:
        """{{rendered_at}} is NOT in the template body."""
        content = _TEMPLATE_PATH.read_text(encoding="utf-8")
        assert "{{rendered_at}}" not in content


class TestPresetYmlRegistration:
    """Validate preset.yml registers issue-template.md correctly."""

    def test_issue_template_in_templates_list(self) -> None:
        """issue-template.md is listed in preset.yml templates."""
        data = yaml.safe_load(_PRESET_YML_PATH.read_text(encoding="utf-8"))
        assert "issue-template.md" in data["templates"]

    def test_manifest_fields_present(self) -> None:
        """Manifest contains required fields: name, version, description, author, license, repository, assets."""
        data = yaml.safe_load(_PRESET_YML_PATH.read_text(encoding="utf-8"))
        for field in ("name", "version", "description", "author", "license", "repository", "assets"):
            assert field in data, f"Missing field: {field}"

    def test_original_templates_preserved(self) -> None:
        """All original template entries are preserved."""
        data = yaml.safe_load(_PRESET_YML_PATH.read_text(encoding="utf-8"))
        templates = data["templates"]
        for expected in (
            "agent-file-template.md",
            "checklist-template.md",
            "plan-template.md",
            "spec-template.md",
            "tasks-template.md",
        ):
            assert expected in templates
