"""Tests for agentic_devtools.cli.setup.phase_0._prompt_phase_0_config."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.setup.phase_0 import _prompt_phase_0_config


class TestPromptPhase0ConfigInteractive:
    """Tests for the interactive prompting path."""

    def test_first_run_enable_both(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """First run: y + y → enabled=true, sync_back_on_merge=true."""
        inputs = iter(["y", "y"])
        with patch("agentic_devtools.cli.setup.phase_0.input", side_effect=lambda _: next(inputs)):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value={}):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True) as mock_save:
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config()

        out = capsys.readouterr().out
        assert "Phase 0 configuration saved" in out
        saved_platform = mock_save.call_args[0][1]
        assert saved_platform["phase_0"]["enabled"] is True
        assert saved_platform["phase_0"]["sync_back_on_merge"] is True
        assert saved_platform["phase_0"]["sync_back_fields"] == ["comment"]

    def test_first_run_enable_no_sync(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """First run: y + n → enabled=true, sync_back_on_merge=false."""
        inputs = iter(["y", "n"])
        with patch("agentic_devtools.cli.setup.phase_0.input", side_effect=lambda _: next(inputs)):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value={}):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True) as mock_save:
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config()

        saved_platform = mock_save.call_args[0][1]
        assert saved_platform["phase_0"]["enabled"] is True
        assert saved_platform["phase_0"]["sync_back_on_merge"] is False

    def test_first_run_disable(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """First run: n → only 1 prompt, enabled=false, sync_back_on_merge=false."""
        mock_input = MagicMock(return_value="n")
        with patch("agentic_devtools.cli.setup.phase_0.input", mock_input):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value={}):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True) as mock_save:
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config()

        # Only 1 prompt (enabled), not 2 (no sync_back prompt when disabled)
        assert mock_input.call_count == 1
        saved_platform = mock_save.call_args[0][1]
        assert saved_platform["phase_0"]["enabled"] is False
        assert saved_platform["phase_0"]["sync_back_on_merge"] is False

    def test_first_run_empty_input_uses_defaults(self, tmp_path: Path) -> None:
        """Empty input on both prompts uses defaults (false, false)."""
        inputs = iter(["", ""])
        with patch("agentic_devtools.cli.setup.phase_0.input", side_effect=lambda _: next(inputs)):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value={}):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True) as mock_save:
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config()

        saved_platform = mock_save.call_args[0][1]
        # Default for enabled is False, so only 1 prompt (enabled says no → no sync prompt)
        assert saved_platform["phase_0"]["enabled"] is False
        assert saved_platform["phase_0"]["sync_back_on_merge"] is False

    def test_unrecognised_input_keeps_default(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Unrecognised input 'maybe' keeps default and prints warning."""
        mock_input = MagicMock(return_value="maybe")
        with patch("agentic_devtools.cli.setup.phase_0.input", mock_input):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value={}):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True) as mock_save:
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config()

        err = capsys.readouterr().err
        assert "Unrecognised input" in err
        saved_platform = mock_save.call_args[0][1]
        # Default is False for enabled
        assert saved_platform["phase_0"]["enabled"] is False

    def test_malformed_platform_treated_as_absent(self, tmp_path: Path) -> None:
        """platform='string' treated as absent → prompts shown."""
        mock_input = MagicMock(return_value="n")
        raw_config = {"platform": "not-a-dict"}
        with patch("agentic_devtools.cli.setup.phase_0.input", mock_input):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value=raw_config):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True):
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config()

        # Prompts were shown (input was called)
        mock_input.assert_called()


class TestPromptPhase0ConfigDefaults:
    """Tests for the --defaults path."""

    def test_defaults_no_existing_writes_safe_defaults(self, tmp_path: Path) -> None:
        """use_defaults=True, no phase_0 → safe defaults written, no input()."""
        mock_input = MagicMock()
        with patch("agentic_devtools.cli.setup.phase_0.input", mock_input):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value={}):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True) as mock_save:
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config(use_defaults=True)

        mock_input.assert_not_called()
        saved_platform = mock_save.call_args[0][1]
        assert saved_platform["phase_0"]["enabled"] is False
        assert saved_platform["phase_0"]["sync_back_on_merge"] is False
        assert saved_platform["phase_0"]["sync_back_fields"] == ["comment"]

    def test_defaults_preserves_existing_valid(self, tmp_path: Path) -> None:
        """use_defaults=True, phase_0 exists + valid → preserved, no input()."""
        raw_config = {
            "platform": {
                "phase_0": {"enabled": True, "sync_back_on_merge": True, "sync_back_fields": ["comment", "label"]},
            }
        }
        mock_input = MagicMock()
        with patch("agentic_devtools.cli.setup.phase_0.input", mock_input):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value=raw_config):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True) as mock_save:
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config(use_defaults=True)

        mock_input.assert_not_called()
        saved_platform = mock_save.call_args[0][1]
        assert saved_platform["phase_0"]["enabled"] is True
        assert saved_platform["phase_0"]["sync_back_on_merge"] is True
        assert saved_platform["phase_0"]["sync_back_fields"] == ["comment", "label"]

    def test_defaults_invalid_existing_falls_back(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """use_defaults=True, phase_0 exists with invalid fields → safe defaults, warning."""
        raw_config = {
            "platform": {
                "phase_0": {
                    "enabled": True,
                    "sync_back_on_merge": True,
                    "sync_back_fields": ["invalid_field"],
                },
            }
        }
        mock_input = MagicMock()
        with patch("agentic_devtools.cli.setup.phase_0.input", mock_input):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value=raw_config):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True) as mock_save:
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config(use_defaults=True)

        mock_input.assert_not_called()
        err = capsys.readouterr().err
        assert "invalid" in err.lower() or "safe defaults" in err.lower()
        saved_platform = mock_save.call_args[0][1]
        # Fell back to safe defaults
        assert saved_platform["phase_0"]["enabled"] is False
        assert saved_platform["phase_0"]["sync_back_fields"] == ["comment"]


class TestPromptPhase0ConfigIdempotent:
    """Tests for idempotent re-run behavior."""

    def test_idempotent_rerun_no_prompts(self, tmp_path: Path) -> None:
        """phase_0 present + no force_prompt → zero input() calls, mirrors to project.json."""
        raw_config = {
            "platform": {
                "phase_0": {"enabled": True, "sync_back_on_merge": False, "sync_back_fields": ["comment"]},
            }
        }
        mock_input = MagicMock()
        with patch("agentic_devtools.cli.setup.phase_0.input", mock_input):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value=raw_config):
                    with patch(
                        "agentic_devtools.cli.config.project_config.save_project_config",
                        return_value=tmp_path / "project.json",
                    ) as mock_proj_save:
                        _prompt_phase_0_config()

        mock_input.assert_not_called()
        # Mirrored to project.json
        mock_proj_save.assert_called_once()
        saved = mock_proj_save.call_args[0][0]
        assert saved["phase_0"]["enabled"] is True

    def test_idempotent_rerun_invalid_config_skips(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """phase_0 present but invalid → warning printed, no crash, no mirror."""
        raw_config = {
            "platform": {
                "phase_0": {
                    "enabled": True,
                    "sync_back_on_merge": True,
                    "sync_back_fields": ["bogus_field"],
                },
            }
        }
        mock_input = MagicMock()
        with patch("agentic_devtools.cli.setup.phase_0.input", mock_input):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value=raw_config):
                    with patch(
                        "agentic_devtools.cli.config.project_config.save_project_config",
                        return_value=tmp_path / "project.json",
                    ) as mock_proj_save:
                        _prompt_phase_0_config()

        mock_input.assert_not_called()
        mock_proj_save.assert_not_called()
        err = capsys.readouterr().err
        assert "invalid" in err.lower() or "skipping mirror" in err.lower()


class TestPromptPhase0ConfigReconfigure:
    """Tests for --reconfigure (force_prompt=True)."""

    def test_reconfigure_shows_current_defaults(self, tmp_path: Path) -> None:
        """force_prompt=True, current enabled=true → bracket shows [Y/n]."""
        raw_config = {
            "platform": {
                "phase_0": {"enabled": True, "sync_back_on_merge": True, "sync_back_fields": ["comment"]},
            }
        }
        captured_prompts: list[str] = []

        def mock_input(prompt: str) -> str:
            captured_prompts.append(prompt)
            return ""  # Accept defaults

        with patch("agentic_devtools.cli.setup.phase_0.input", side_effect=mock_input):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value=raw_config):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True) as mock_save:
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config(force_prompt=True)

        # Bracket should show [Y/n] for enabled since currently True
        assert any("[Y/n]" in p for p in captured_prompts)
        # Preserved current values via defaults
        saved_platform = mock_save.call_args[0][1]
        assert saved_platform["phase_0"]["enabled"] is True
        assert saved_platform["phase_0"]["sync_back_on_merge"] is True

    def test_reconfigure_disable_resets_sync_back(self, tmp_path: Path) -> None:
        """force_prompt=True, answer n when currently enabled → resets sync_back_on_merge."""
        raw_config = {
            "platform": {
                "phase_0": {"enabled": True, "sync_back_on_merge": True, "sync_back_fields": ["comment"]},
            }
        }
        inputs = iter(["n"])
        with patch("agentic_devtools.cli.setup.phase_0.input", side_effect=lambda _: next(inputs)):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value=raw_config):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True) as mock_save:
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config(force_prompt=True)

        saved_platform = mock_save.call_args[0][1]
        assert saved_platform["phase_0"]["enabled"] is False
        assert saved_platform["phase_0"]["sync_back_on_merge"] is False

    def test_reconfigure_preserves_existing_sync_back_fields(self, tmp_path: Path) -> None:
        """force_prompt=True with non-default sync_back_fields → fields preserved when accepting defaults."""
        raw_config = {
            "platform": {
                "phase_0": {"enabled": True, "sync_back_on_merge": True, "sync_back_fields": ["comment", "label"]},
            }
        }

        def mock_input(_prompt: str) -> str:
            return ""  # Accept defaults for all prompts

        with patch("agentic_devtools.cli.setup.phase_0.input", side_effect=mock_input):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value=raw_config):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True) as mock_save:
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config(force_prompt=True)

        saved_platform = mock_save.call_args[0][1]
        # Previously configured sync_back_fields must not be silently discarded
        assert saved_platform["phase_0"]["sync_back_fields"] == ["comment", "label"]

    def test_reconfigure_invalid_existing_uses_default_brackets(self, tmp_path: Path) -> None:
        """force_prompt=True with invalid existing config → uses default brackets [y/N]."""
        raw_config = {
            "platform": {
                "phase_0": {
                    "enabled": True,
                    "sync_back_on_merge": True,
                    "sync_back_fields": ["invalid_field"],
                },
            }
        }
        captured_prompts: list[str] = []

        def mock_input(prompt: str) -> str:
            captured_prompts.append(prompt)
            return "n"

        with patch("agentic_devtools.cli.setup.phase_0.input", side_effect=mock_input):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value=raw_config):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True):
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config(force_prompt=True)

        # Falls back to default bracket [y/N] since validation failed
        assert any("[y/N]" in p for p in captured_prompts)

    def test_reconfigure_invalid_sync_back_fields_reset_when_enabling_sync_back(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """force_prompt=True, sync_back_on_merge was false with invalid sync_back_fields.

        When the user enables sync-back, the invalid fields are sanitized to defaults
        so _persist() does not raise ValueError.
        """
        raw_config = {
            "platform": {
                "phase_0": {
                    "enabled": True,
                    "sync_back_on_merge": False,  # gate was off — invalid field was accepted
                    "sync_back_fields": ["bogus_field"],
                },
            }
        }
        inputs = iter(["y", "y"])  # enable=yes, sync_back=yes
        with patch("agentic_devtools.cli.setup.phase_0.input", side_effect=lambda _: next(inputs)):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value=raw_config):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True) as mock_save:
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config(force_prompt=True)

        err = capsys.readouterr().err
        assert "invalid" in err.lower() or "resetting to defaults" in err.lower()
        saved_platform = mock_save.call_args[0][1]
        assert saved_platform["phase_0"]["sync_back_on_merge"] is True
        # Invalid field was reset; config must pass validation
        from agentic_devtools.config import validate_phase_0_config

        validate_phase_0_config(saved_platform["phase_0"])  # must not raise
        assert saved_platform["phase_0"]["sync_back_fields"] == ["comment"]


class TestPromptPhase0ConfigFailures:
    """Tests for save failure handling."""

    def test_save_platform_failure_warns_continues(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """save_platform_config returns False → warning printed, no crash."""
        mock_input = MagicMock(return_value="n")
        with patch("agentic_devtools.cli.setup.phase_0.input", mock_input):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value={}):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=False):
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config()

        captured = capsys.readouterr()
        err = captured.err
        assert "Failed to save Phase 0 to platform config" in err
        assert "Phase 0 configuration saved" not in captured.out

    def test_save_project_config_failure_warns_continues(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """save_project_config raises RuntimeError → warning printed, no crash."""
        mock_input = MagicMock(return_value="n")
        with patch("agentic_devtools.cli.setup.phase_0.input", mock_input):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value={}):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True):
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                side_effect=RuntimeError("no git root"),
                            ):
                                _prompt_phase_0_config()

        captured = capsys.readouterr()
        err = captured.err
        assert "Failed to save Phase 0 to project.json" in err
        assert "Phase 0 configuration saved" not in captured.out

    def test_no_git_root_skips(self, capsys: pytest.CaptureFixture[str]) -> None:
        """No git root → warning and early return."""
        with patch("agentic_devtools.state._get_git_repo_root", return_value=None):
            _prompt_phase_0_config()

        err = capsys.readouterr().err
        assert "Cannot determine git root" in err


class TestPromptPhase0ConfigValidation:
    """Tests verifying all written configs pass validation."""

    @pytest.mark.parametrize(
        "enabled_answer,sync_answer",
        [("y", "y"), ("y", "n"), ("n", ""), ("", ""), ("Y", "N")],
        ids=["both-yes", "enable-no-sync", "disable", "all-defaults", "uppercase"],
    )
    def test_all_combos_pass_validation(self, tmp_path: Path, enabled_answer: str, sync_answer: str) -> None:
        """All input combinations produce configs that pass validate_phase_0_config."""
        from agentic_devtools.config import validate_phase_0_config

        answers = iter([enabled_answer, sync_answer])

        with patch("agentic_devtools.cli.setup.phase_0.input", side_effect=lambda _: next(answers, "")):
            with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
                with patch("agentic_devtools.config.load_repo_config", return_value={}):
                    with patch("agentic_devtools.config.load_platform_config", return_value={}):
                        with patch("agentic_devtools.config.save_platform_config", return_value=True) as mock_save:
                            with patch(
                                "agentic_devtools.cli.config.project_config.save_project_config",
                                return_value=tmp_path / "project.json",
                            ):
                                _prompt_phase_0_config()

        saved_platform = mock_save.call_args[0][1]
        # Should not raise
        result = validate_phase_0_config(saved_platform["phase_0"])
        assert "enabled" in result
        assert "sync_back_on_merge" in result
        assert "sync_back_fields" in result
