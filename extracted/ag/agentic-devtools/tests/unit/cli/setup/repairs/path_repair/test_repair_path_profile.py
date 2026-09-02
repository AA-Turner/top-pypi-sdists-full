"""Tests for repair_path_profile."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.repairs.path_repair import repair_path_profile


class TestRepairPathProfileApplied:
    """repair_path_profile appends entry when missing."""

    def test_appends_entry_when_missing(self, tmp_path: Path) -> None:
        """When PATH entry is missing, persist_path_entry writes it and returns True."""
        profile = tmp_path / ".bashrc"
        profile.write_text("# empty\n", encoding="utf-8")
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_type",
                return_value="bash",
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_profile",
                return_value=profile,
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.persist_path_entry",
                return_value=True,
            ),
        ):
            result = repair_path_profile(dep)

        assert result is True
        assert dep.found is True


class TestRepairPathProfileNoop:
    """repair_path_profile returns False when entry already present."""

    def test_returns_false_when_already_present(self, tmp_path: Path) -> None:
        """When PATH entry already exists, returns False (no-op)."""
        profile = tmp_path / ".bashrc"
        path_entry = str(Path.home() / ".agdt" / "bin")
        profile.write_text(f'export PATH="{path_entry}:$PATH"\n', encoding="utf-8")
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_type",
                return_value="bash",
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_profile",
                return_value=profile,
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.persist_path_entry",
                return_value=False,
            ),
        ):
            result = repair_path_profile(dep)

        assert result is False
        assert dep.found is True


class TestRepairPathProfileFailure:
    """repair_path_profile raises on write failure."""

    def test_raises_on_write_failure(self, tmp_path: Path) -> None:
        """When persist_path_entry returns False and entry not in file, raises."""
        profile = tmp_path / ".bashrc"
        profile.write_text("# no path entry\n", encoding="utf-8")
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_type",
                return_value="bash",
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_profile",
                return_value=profile,
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.persist_path_entry",
                return_value=False,
            ),
        ):
            with pytest.raises(RuntimeError, match="Failed to persist PATH entry"):
                repair_path_profile(dep)

    def test_raises_when_only_superstring_path_is_present(self, tmp_path: Path) -> None:
        """A superstring PATH component is not treated as a successful no-op."""
        profile = tmp_path / ".bashrc"
        path_entry = str(Path.home() / ".agdt" / "bin")
        profile.write_text(
            f'export PATH="{path_entry}-tools:$PATH"\n',
            encoding="utf-8",
        )
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_type",
                return_value="bash",
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_profile",
                return_value=profile,
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.persist_path_entry",
                return_value=False,
            ),
        ):
            with pytest.raises(RuntimeError, match="Failed to persist PATH entry"):
                repair_path_profile(dep)


class TestRepairPathProfileUnknownShell:
    """repair_path_profile raises when profile path is None."""

    def test_raises_on_unknown_shell(self) -> None:
        """When detect_shell_profile returns None, raises RuntimeError."""
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_type",
                return_value="unknown",
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_profile",
                return_value=None,
            ),
        ):
            with pytest.raises(RuntimeError, match="unsupported shell type"):
                repair_path_profile(dep)


class TestRepairPathProfilePowershell:
    """repair_path_profile handles PowerShell shell type."""

    def test_noop_powershell_entry_present(self, tmp_path: Path) -> None:
        """When entry present in PowerShell PATH assignment, returns False."""
        profile = tmp_path / "profile.ps1"
        path_entry = str(Path.home() / ".agdt" / "bin")
        profile.write_text(f'$env:PATH = "{path_entry};$env:PATH"\n', encoding="utf-8")
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_type",
                return_value="powershell",
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_profile",
                return_value=profile,
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.persist_path_entry",
                return_value=False,
            ),
        ):
            result = repair_path_profile(dep)

        assert result is False
        assert dep.found is True


class TestRepairPathProfileMissingProfile:
    """repair_path_profile raises when profile file doesn't exist after write."""

    def test_raises_when_profile_not_exists(self, tmp_path: Path) -> None:
        """When profile doesn't exist and persist returns False, raises."""
        profile = tmp_path / ".bashrc"  # NOT created
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_type",
                return_value="bash",
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_profile",
                return_value=profile,
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.persist_path_entry",
                return_value=False,
            ),
        ):
            with pytest.raises(RuntimeError, match="Failed to persist PATH entry"):
                repair_path_profile(dep)

    def test_raises_when_profile_read_fails(self, tmp_path: Path) -> None:
        """When profile read fails after a false write result, raises RuntimeError."""
        profile = tmp_path / ".bashrc"
        profile.write_text("# existing profile\n", encoding="utf-8")
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_type",
                return_value="bash",
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.detect_shell_profile",
                return_value=profile,
            ),
            patch(
                "agentic_devtools.cli.setup.repairs.path_repair.persist_path_entry",
                return_value=False,
            ),
            patch(
                "pathlib.Path.read_text",
                side_effect=PermissionError("permission denied"),
            ),
        ):
            with pytest.raises(RuntimeError, match="Failed to persist PATH entry"):
                repair_path_profile(dep)
