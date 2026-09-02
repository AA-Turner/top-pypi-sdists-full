"""Tests for _check_setup_expectations in the checks pipeline."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.checks.changed_files import DiffUnavailableError
from agentic_devtools.cli.checks.commands import _check_setup_expectations


class TestCheckSetupExpectations:
    """Tests for the setup expectations check integration."""

    def test_skip_when_no_relevant_files(self, tmp_path: Path) -> None:
        """No setup files changed → skip with passing result."""
        with (
            patch(
                "agentic_devtools.cli.checks.commands.get_changed_files",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.checks.commands._build_drift_file_list",
                return_value=([], []),
            ),
        ):
            result = _check_setup_expectations(tmp_path)
        assert result.passed
        assert "skipped" in result.output.lower()

    def test_run_when_setup_files_changed(self) -> None:
        """Setup files changed → run validator, drift gate passes when doc included."""
        repo_root = Path(__file__).resolve().parents[5]  # Navigate to repo root

        def mock_changed_files(**kwargs: object) -> list[str]:
            pattern = kwargs.get("pattern", "")
            if "setup" in str(pattern):
                return ["agentic_devtools/cli/setup/exit_codes.py"]
            return []

        with (
            patch(
                "agentic_devtools.cli.checks.commands.get_changed_files",
                side_effect=mock_changed_files,
            ),
            patch(
                "agentic_devtools.cli.checks.commands._build_drift_file_list",
                return_value=(
                    [
                        "agentic_devtools/cli/setup/exit_codes.py",
                        "docs/setup-expectations/agdt-setup.md",
                    ],
                    [],
                ),
            ),
            patch(
                "agentic_devtools.cli.checks.commands.ensure_placeholder_docs",
            ),
        ):
            result = _check_setup_expectations(repo_root)
        assert result.passed
        assert "consistent" in result.output.lower()

    def test_validator_uses_check_cwd_as_repo_root(self, tmp_path: Path) -> None:
        """Validator should use the check's cwd argument as repo root."""
        from agentic_devtools.cli.setup.expectations_validator import ValidationResult

        def mock_changed_files(**kwargs: object) -> list[str]:
            return ["agentic_devtools/cli/setup/exit_codes.py"]

        with (
            patch(
                "agentic_devtools.cli.checks.commands.get_changed_files",
                side_effect=mock_changed_files,
            ),
            patch(
                "agentic_devtools.cli.checks.commands._build_drift_file_list",
                return_value=(
                    [
                        "agentic_devtools/cli/setup/exit_codes.py",
                        "docs/setup-expectations/README.md",
                    ],
                    [],
                ),
            ),
            patch(
                "agentic_devtools.cli.checks.commands.ensure_placeholder_docs",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_validator.validate_expectations",
                return_value=ValidationResult(True, []),
            ) as mock_validate,
        ):
            result = _check_setup_expectations(tmp_path / "subdir")

        assert result.passed
        mock_validate.assert_called_once_with(repo_root=tmp_path / "subdir")

    def test_fail_on_drift(self, tmp_path: Path) -> None:
        """Validator reports content error → check fails with generic header."""
        from agentic_devtools.cli.setup.expectations_validator import ValidationResult

        def mock_changed_files(**kwargs: object) -> list[str]:
            return ["agentic_devtools/cli/setup/exit_codes.py"]

        with (
            patch(
                "agentic_devtools.cli.checks.commands.get_changed_files",
                side_effect=mock_changed_files,
            ),
            patch(
                "agentic_devtools.cli.checks.commands._build_drift_file_list",
                return_value=(
                    [
                        "agentic_devtools/cli/setup/exit_codes.py",
                        "docs/setup-expectations/README.md",
                    ],
                    [],
                ),
            ),
            patch(
                "agentic_devtools.cli.checks.commands.ensure_placeholder_docs",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_validator.validate_expectations",
                return_value=ValidationResult(False, ["Phase missing"]),
            ),
        ):
            result = _check_setup_expectations(tmp_path)
        assert not result.passed
        assert "check failed" in result.output.lower()

    def test_handles_diff_unavailable(self, tmp_path: Path) -> None:
        """DiffUnavailableError is handled gracefully."""
        with (
            patch(
                "agentic_devtools.cli.checks.commands.get_changed_files",
                side_effect=DiffUnavailableError("no git"),
            ),
            patch(
                "agentic_devtools.cli.checks.commands._build_drift_file_list",
                return_value=([], []),
            ),
        ):
            result = _check_setup_expectations(tmp_path)
        assert result.passed
        assert "skipped" in result.output.lower()

    def test_drift_only_also_runs_content_validation(self, tmp_path: Path) -> None:
        """Drift files changed but no content-relevant files → both drift gate and content validation run."""
        from agentic_devtools.cli.setup.expectations_validator import ValidationResult

        with (
            patch(
                "agentic_devtools.cli.checks.commands.get_changed_files",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.checks.commands._build_drift_file_list",
                return_value=(
                    [
                        "agentic_devtools/skill_injector.py",
                        "docs/setup-expectations/README.md",
                    ],
                    [],
                ),
            ),
            patch(
                "agentic_devtools.cli.checks.commands.ensure_placeholder_docs",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_validator.validate_expectations",
                return_value=ValidationResult(True, []),
            ),
        ):
            result = _check_setup_expectations(tmp_path)
        assert result.passed
        assert "consistent" in result.output.lower()

    def test_deletion_triggers_content_validation(self, tmp_path: Path) -> None:
        """Deleting a setup doc appears in drift_files but not content_relevant; validator must still run."""
        from agentic_devtools.cli.setup.expectations_validator import ValidationResult

        # _build_drift_file_list returns (all_changed_files, deleted_paths).
        # For a pure deletion, the same path appears in both lists: the first list
        # drives the drift check while the second marks the path as deleted so
        # ensure_placeholder_docs won't try to re-create it.
        deleted_doc = "docs/setup-expectations/agdt-setup.md"
        with (
            patch(
                "agentic_devtools.cli.checks.commands.get_changed_files",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.checks.commands._build_drift_file_list",
                return_value=([deleted_doc], [deleted_doc]),
            ),
            patch(
                "agentic_devtools.cli.checks.commands.ensure_placeholder_docs",
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_validator.validate_expectations",
                return_value=ValidationResult(False, ["Phase missing after deletion"]),
            ) as mock_validate,
        ):
            result = _check_setup_expectations(tmp_path)

        # Validator must have been invoked even though content_relevant was empty
        mock_validate.assert_called_once()
        assert not result.passed
        assert "phase missing after deletion" in result.output.lower()

    def test_drift_gate_fails_without_doc(self, tmp_path: Path) -> None:
        """Drift gate detects setup source without doc update → check fails."""
        with (
            patch(
                "agentic_devtools.cli.checks.commands.get_changed_files",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.checks.commands._build_drift_file_list",
                return_value=(
                    ["agentic_devtools/skill_injector.py"],
                    [],
                ),
            ),
            patch(
                "agentic_devtools.cli.checks.commands.ensure_placeholder_docs",
            ),
        ):
            result = _check_setup_expectations(tmp_path)
        assert not result.passed
        assert "drift" in result.output.lower()

    def test_ensure_placeholder_valueerror(self, tmp_path: Path) -> None:
        """ValueError from ensure_placeholder_docs → check fails with message."""
        with (
            patch(
                "agentic_devtools.cli.checks.commands.get_changed_files",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.checks.commands._build_drift_file_list",
                return_value=(
                    [
                        "agentic_devtools/cli/setup/commands.py",
                        "docs/setup-expectations/README.md",
                    ],
                    ["docs/setup-expectations/README.md"],
                ),
            ),
            patch(
                "agentic_devtools.cli.checks.commands.ensure_placeholder_docs",
                side_effect=ValueError("No non-empty tracked placeholder"),
            ),
        ):
            result = _check_setup_expectations(tmp_path)
        assert not result.passed
        assert "placeholder" in result.output.lower()

    def test_ensure_placeholder_oserror(self, tmp_path: Path) -> None:
        """OSError from ensure_placeholder_docs → check fails with message."""
        with (
            patch(
                "agentic_devtools.cli.checks.commands.get_changed_files",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.checks.commands._build_drift_file_list",
                return_value=(
                    [
                        "agentic_devtools/cli/setup/commands.py",
                        "docs/setup-expectations/README.md",
                    ],
                    [],
                ),
            ),
            patch(
                "agentic_devtools.cli.checks.commands.ensure_placeholder_docs",
                side_effect=OSError("Permission denied: /docs/setup-expectations"),
            ),
        ):
            result = _check_setup_expectations(tmp_path)
        assert not result.passed
        assert "permission denied" in result.output.lower()

    def test_content_only_no_drift_files(self, tmp_path: Path) -> None:
        """Content-relevant files changed but no drift files → only content validation runs."""
        from agentic_devtools.cli.setup.expectations_validator import ValidationResult

        def mock_changed_files(**kwargs: object) -> list[str]:
            pattern = kwargs.get("pattern", "")
            if pattern == "agentic_devtools/cli/setup/**":
                return ["agentic_devtools/cli/setup/exit_codes.py"]
            return []

        with (
            patch(
                "agentic_devtools.cli.checks.commands.get_changed_files",
                side_effect=mock_changed_files,
            ),
            patch(
                "agentic_devtools.cli.checks.commands._build_drift_file_list",
                return_value=([], []),
            ),
            patch(
                "agentic_devtools.cli.setup.expectations_validator.validate_expectations",
                return_value=ValidationResult(True, []),
            ),
        ):
            result = _check_setup_expectations(tmp_path)
        assert result.passed
