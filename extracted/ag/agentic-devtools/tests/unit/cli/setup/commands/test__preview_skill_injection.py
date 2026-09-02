"""Tests for agentic_devtools.cli.setup.commands._preview_skill_injection."""

from __future__ import annotations

import builtins
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.commands import _preview_skill_injection


class TestPreviewSkillInjection:
    """Tests for the dry-run skill-injection preview."""

    def test_invokes_injector_with_saved_axes(self, tmp_path: Path, capsys) -> None:
        """The injector uses saved axes for dry-run preview when authoritative config exists."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir(parents=True)
        (config_dir / "agdt-config.json").write_text(
            '{"platform":{"issue_adapter":"github","code_hosting":"github","issue_adapter_resolved":true}}',
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector.inject_skills_with_summary") as mock_inject:
            mock_inject.return_value = (True, None)
            _preview_skill_injection(tmp_path)

        kwargs = mock_inject.call_args.kwargs
        assert kwargs.get("dry_run") is True
        assert kwargs.get("issue_adapter") == "github"
        assert kwargs.get("code_hosting") == "github"
        out = capsys.readouterr().out
        assert "would inject agent/prompt/skill files" in out
        assert "issue_adapter=github" in out
        assert "code_hosting=github" in out

    def test_invokes_injector_with_unrestricted_axes_without_authoritative_config(self, tmp_path: Path, capsys) -> None:
        """Legacy markerless default adapter keeps issue-adapter axis unrestricted."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir(parents=True)
        (config_dir / "agdt-config.json").write_text(
            '{"platform":{"issue_adapter":"jira","code_hosting":"github"}}',
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector.inject_skills_with_summary") as mock_inject:
            mock_inject.return_value = (True, None)
            _preview_skill_injection(tmp_path)

        kwargs = mock_inject.call_args.kwargs
        assert kwargs.get("dry_run") is True
        assert kwargs.get("issue_adapter") is None
        assert kwargs.get("code_hosting") == "github"
        out = capsys.readouterr().out
        assert "issue_adapter=unrestricted" in out
        assert "code_hosting=github" in out

    def test_injector_failure_emits_warning(self, tmp_path: Path, capsys) -> None:
        """A False success return from the injector is surfaced as a stderr warning."""
        with patch("agentic_devtools.skill_injector.inject_skills_with_summary") as mock_inject:
            mock_inject.return_value = (False, None)
            _preview_skill_injection(tmp_path)

        captured = capsys.readouterr()
        assert "manifest diff may be incomplete" in captured.err

    def test_import_failure_degrades_to_warning(self, tmp_path: Path, capsys) -> None:
        """An unimportable injector warns instead of failing the dry run."""
        real_import = builtins.__import__

        def _raising_import(name, *args, **kwargs):
            if name == "agentic_devtools.skill_injector":
                raise ImportError("boom")
            return real_import(name, *args, **kwargs)

        with patch.object(builtins, "__import__", _raising_import):
            _preview_skill_injection(tmp_path)

        captured = capsys.readouterr()
        assert "would inject agent/prompt/skill files" in captured.out
        assert "manifest diff unavailable" in captured.err
