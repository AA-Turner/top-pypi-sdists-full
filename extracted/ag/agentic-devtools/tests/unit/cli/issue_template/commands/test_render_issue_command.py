"""Tests for agentic_devtools.cli.issue_template.commands.render_issue_command."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import yaml

from agentic_devtools.adapters.types import NormalizedIssue
from agentic_devtools.cli.issue_template.commands import render_issue_command


def _make_issue(**kwargs: object) -> NormalizedIssue:
    """Create a NormalizedIssue with sensible defaults."""
    defaults: dict[str, object] = {
        "issue_id": "TEST-42",
        "title": "Test Issue Title",
        "url": "https://example.com/issues/42",
        "provider": "jira",
        "description": "Issue description text.",
        "status": "open",
        "labels": ["feature"],
        "raw": {"issue_type": "story"},
    }
    defaults.update(kwargs)
    return NormalizedIssue(**defaults)  # type: ignore[arg-type]


def _setup_preset_dir(tmp_path: Path) -> Path:
    """Create a minimal preset directory with templates."""
    preset_dir = tmp_path / ".specify" / "presets" / "agdt-templates"
    templates_dir = preset_dir / "templates"
    templates_dir.mkdir(parents=True)

    # Create preset.yml
    (preset_dir / "preset.yml").write_text(
        "name: test\ntemplates:\n  - issue-template.md\n  - issue-template-story.md\n",
        encoding="utf-8",
    )

    # Create template files
    (templates_dir / "issue-template.md").write_text(
        "## Description\n\n{{description}}",
        encoding="utf-8",
    )
    (templates_dir / "issue-template-story.md").write_text(
        "## Description\n\nSTORY-TEMPLATE-MARKER {{description}}\n\n## Acceptance Criteria\n\n{{acceptance_criteria}}",
        encoding="utf-8",
    )

    return tmp_path


class TestRenderIssueCommand:
    """Tests for the render_issue_command function."""

    def test_happy_path_full_orchestration(self, tmp_path: Path) -> None:
        """Full synchronous orchestration produces correct issue.md."""
        repo_root = _setup_preset_dir(tmp_path)
        state_dir = tmp_path / "state"
        state_dir.mkdir()

        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {"mock": "detail"}
        mock_adapter.normalize.return_value = issue

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_state_dir",
                return_value=state_dir,
            ),
        ):
            render_issue_command()

        output_file = state_dir / "issue.md"
        assert output_file.exists()

        content = output_file.read_text(encoding="utf-8")
        parts = content.split("---\n")
        frontmatter = yaml.safe_load(parts[1])

        assert frontmatter["id"] == "TEST-42"
        assert frontmatter["title"] == "Test Issue Title"
        assert frontmatter["type"] == "story"
        assert frontmatter["provider"] == "jira"
        assert "rendered_at" in frontmatter
        assert "## Description" in content
        assert "Issue description text." in content
        # T011/FR-001: the type-specific story template must be selected, not the
        # default template. A regression to the default would drop this marker.
        assert "STORY-TEMPLATE-MARKER" in content

    def test_overwrite_behavior(self, tmp_path: Path) -> None:
        """Repeated invocations overwrite the existing issue.md."""
        repo_root = _setup_preset_dir(tmp_path)
        state_dir = tmp_path / "state"
        state_dir.mkdir()

        # Write initial content
        (state_dir / "issue.md").write_text("old content", encoding="utf-8")

        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_state_dir",
                return_value=state_dir,
            ),
        ):
            render_issue_command()

        content = (state_dir / "issue.md").read_text(encoding="utf-8")
        assert "old content" not in content
        assert "Issue description text." in content

    def test_template_override_bypasses_selection(self, tmp_path: Path) -> None:
        """--template override uses specified file, bypasses selection."""
        repo_root = _setup_preset_dir(tmp_path)
        state_dir = tmp_path / "state"
        state_dir.mkdir()

        custom_template = tmp_path / "custom.md"
        custom_template.write_text(
            "## Custom\n\n{{description}}",
            encoding="utf-8",
        )

        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": str(custom_template),
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_state_dir",
                return_value=state_dir,
            ),
        ):
            render_issue_command()

        content = (state_dir / "issue.md").read_text(encoding="utf-8")
        assert "## Custom" in content

    def test_missing_issue_key_exits(self) -> None:
        """Missing issue_key exits with non-zero code."""
        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                return_value=None,
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1

    def test_not_in_git_repo_exits(self, tmp_path: Path) -> None:
        """Not in a git repository exits with non-zero code."""
        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=None,
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1

    def test_adapter_error_exits(self, tmp_path: Path) -> None:
        """Error from adapter.get_issue exits with non-zero code."""
        repo_root = _setup_preset_dir(tmp_path)

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                side_effect=RuntimeError("no adapter"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1

    def test_template_override_not_found_exits(self, tmp_path: Path) -> None:
        """Template override file not found exits with non-zero code."""
        repo_root = _setup_preset_dir(tmp_path)
        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": "/nonexistent/template.md",
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1

    def test_template_override_is_directory_exits(self, tmp_path: Path) -> None:
        """Template override path is a directory, not a file — exits with code 1."""
        repo_root = _setup_preset_dir(tmp_path)
        dir_path = tmp_path / "a-directory"
        dir_path.mkdir()

        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": str(dir_path),
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1

    def test_template_read_error_exits(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """OSError reading template file exits with code 1."""
        repo_root = _setup_preset_dir(tmp_path)
        state_dir = tmp_path / "state"
        state_dir.mkdir()

        custom_template = tmp_path / "locked.md"
        custom_template.write_text("# template", encoding="utf-8")

        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue

        # Patch only the specific template path to raise OSError; all other
        # Path.read_text calls (e.g., preset.yml loading) fall through to the
        # real implementation so the rest of the command runs normally.
        _real_read_text = Path.read_text

        def _selective_oserror(self: Path, *args: object, **kwargs: object) -> str:
            if self == custom_template:
                raise OSError("permission denied")
            return _real_read_text(self, *args, **kwargs)  # type: ignore[arg-type,return-value]

        monkeypatch.setattr(Path, "read_text", _selective_oserror)

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": str(custom_template),
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1

    def test_template_not_found_error_exits(self, tmp_path: Path) -> None:
        """TemplateNotFoundError from select_template exits with non-zero code."""
        repo_root = _setup_preset_dir(tmp_path)
        issue = _make_issue(raw={"issue_type": "exotic-type"})
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue

        # Remove the default template so select_template fails
        (repo_root / ".specify" / "presets" / "agdt-templates" / "templates" / "issue-template.md").unlink()
        # Update preset.yml to not list issue-template.md
        (repo_root / ".specify" / "presets" / "agdt-templates" / "preset.yml").write_text(
            "name: test\ntemplates:\n  - issue-template-story.md\n",
            encoding="utf-8",
        )

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1

    def test_jira_issue_key_fallback(self, tmp_path: Path) -> None:
        """Falls back to jira.issue_key when issue_key is not set."""
        repo_root = _setup_preset_dir(tmp_path)
        state_dir = tmp_path / "state"
        state_dir.mkdir()

        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": None,
                    "jira.issue_key": "JIRA-99",
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_state_dir",
                return_value=state_dir,
            ),
        ):
            render_issue_command()

        assert (state_dir / "issue.md").exists()

    def test_rendered_at_in_frontmatter(self, tmp_path: Path) -> None:
        """rendered_at field is present in frontmatter."""
        repo_root = _setup_preset_dir(tmp_path)
        state_dir = tmp_path / "state"
        state_dir.mkdir()

        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_state_dir",
                return_value=state_dir,
            ),
        ):
            render_issue_command()

        content = (state_dir / "issue.md").read_text(encoding="utf-8")
        parts = content.split("---\n")
        frontmatter = yaml.safe_load(parts[1])
        assert "rendered_at" in frontmatter
        assert frontmatter["rendered_at"]  # Not empty

    def test_validation_error_exits(self, tmp_path: Path) -> None:
        """TemplateValidationError from validate_required_properties exits with code 1."""
        from agentic_devtools.cli.issue_template.exceptions import TemplateValidationError

        repo_root = _setup_preset_dir(tmp_path)
        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue
        mock_adapter.get_type_properties.return_value = []

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.validate_required_properties",
                side_effect=TemplateValidationError("Missing required properties: 'severity'"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1

    def test_validation_provider_error_exits(self, tmp_path: Path) -> None:
        """Unexpected provider validation errors exit with code 1."""
        repo_root = _setup_preset_dir(tmp_path)
        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue
        mock_adapter.get_type_properties.side_effect = RuntimeError("provider validation failed")

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1

    def test_validation_provider_value_error_exits(self, tmp_path: Path) -> None:
        """ValueError from provider type properties exits with code 1."""
        repo_root = _setup_preset_dir(tmp_path)
        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue
        mock_adapter.get_type_properties.side_effect = ValueError("invalid type config")

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1

    def test_validation_skipped_when_not_implemented(self, tmp_path: Path) -> None:
        """NotImplementedError from get_type_properties skips validation."""
        repo_root = _setup_preset_dir(tmp_path)
        state_dir = tmp_path / "state"
        state_dir.mkdir()

        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue
        mock_adapter.get_type_properties.side_effect = NotImplementedError("not implemented")

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_state_dir",
                return_value=state_dir,
            ),
        ):
            render_issue_command()

        assert (state_dir / "issue.md").exists()

    def test_output_write_error_exits(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """OSError writing issue.md exits with code 1."""
        repo_root = _setup_preset_dir(tmp_path)
        state_dir = tmp_path / "state"
        state_dir.mkdir()

        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue

        output_file = state_dir / "issue.md"
        _real_write_text = Path.write_text

        def _selective_write_os_error(
            self: Path,
            *args: Any,
            **kwargs: Any,
        ) -> int:
            if self == output_file:
                raise OSError("disk full")
            return _real_write_text(self, *args, **kwargs)

        monkeypatch.setattr(Path, "write_text", _selective_write_os_error)

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_state_dir",
                return_value=state_dir,
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1

    def test_preset_load_error_exits(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """A malformed preset.yml surfaces a distinct stderr message and non-zero exit (FR-006)."""
        repo_root = tmp_path
        preset_dir = repo_root / ".specify" / "presets" / "agdt-templates"
        preset_dir.mkdir(parents=True)
        # preset.yml is missing entirely -> discover_templates raises PresetLoadError.

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error loading preset" in captured.err

    def test_get_type_properties_receives_native_type_name_not_slug(self, tmp_path: Path) -> None:
        """get_type_properties is called with the original provider-native type name.

        For multi-word type names like "Customer Request", the adapter expects the
        original string for case-insensitive matching — not the slug "customer-request",
        which would fail to match.
        """
        repo_root = _setup_preset_dir(tmp_path)
        state_dir = tmp_path / "state"
        state_dir.mkdir()

        # Multi-word type name: slug would be "customer-request"
        issue = _make_issue(raw={"issue_type": "Customer Request"})
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue
        mock_adapter.get_type_properties.return_value = []

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_state_dir",
                return_value=state_dir,
            ),
        ):
            render_issue_command()

        # Adapter must receive the original name, not a slug
        mock_adapter.get_type_properties.assert_called_once_with("Customer Request")

    def test_get_type_properties_falls_back_to_slug_when_no_raw_type(self, tmp_path: Path) -> None:
        """When issue_type is absent from raw, slug is used for get_type_properties.

        This covers the label-based and default-fallback resolution paths where
        no provider-native type name is available.
        """
        repo_root = _setup_preset_dir(tmp_path)
        state_dir = tmp_path / "state"
        state_dir.mkdir()

        # No issue_type in raw — resolver falls back to label "story" (in known_types)
        issue = _make_issue(raw={}, labels=["story"])
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue
        mock_adapter.get_type_properties.return_value = []

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_state_dir",
                return_value=state_dir,
            ),
        ):
            render_issue_command()

        # Adapter receives the slug as fallback when no raw issue_type is present
        mock_adapter.get_type_properties.assert_called_once_with("story")

    def test_get_type_properties_ignores_raw_type_when_it_slugifies_empty(self, tmp_path: Path) -> None:
        """Punctuation-only raw issue_type falls back to the resolved slug."""
        repo_root = _setup_preset_dir(tmp_path)
        state_dir = tmp_path / "state"
        state_dir.mkdir()

        issue = _make_issue(raw={"issue_type": "!!!"}, labels=["story"])
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue
        mock_adapter.get_type_properties.return_value = []

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_state_dir",
                return_value=state_dir,
            ),
        ):
            render_issue_command()

        mock_adapter.get_type_properties.assert_called_once_with("story")

    def test_invalid_project_mapping_exits(self, tmp_path: Path) -> None:
        """A TemplateValidationError from mapping resolution exits with code 1."""
        from agentic_devtools.cli.issue_template.exceptions import TemplateValidationError

        repo_root = _setup_preset_dir(tmp_path)
        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.mapping_resolver.resolve_effective_mapping",
                side_effect=TemplateValidationError("bad mapping"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1

    def test_template_mapping_conflict_exits(self, tmp_path: Path) -> None:
        """A TemplateValidationError raised by render_issue exits with code 1."""
        from agentic_devtools.cli.issue_template.exceptions import TemplateValidationError

        repo_root = _setup_preset_dir(tmp_path)
        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.mapping_resolver.resolve_effective_mapping",
                return_value={"description": "omit"},
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.render_issue",
                side_effect=TemplateValidationError("template conflict"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1

    def test_invalid_config_mode_exits(self, tmp_path: Path) -> None:
        """A ValueError from resolve_effective_mapping (e.g. invalid config_mode) exits with code 1."""
        repo_root = _setup_preset_dir(tmp_path)
        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue

        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "TEST-42",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.mapping_resolver.resolve_effective_mapping",
                side_effect=ValueError("invalid config_mode: 'bogus'"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            render_issue_command()
        assert exc_info.value.code == 1
