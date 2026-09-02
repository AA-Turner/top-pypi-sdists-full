"""Tests for _check_path_profile."""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from unittest.mock import patch

from agentic_devtools.cli.setup.dependency_checker import _check_path_profile


class TestCheckPathProfileFound:
    """_check_path_profile returns found=True when entry present."""

    def test_entry_in_path_assignment_line(self, tmp_path: Path) -> None:
        """Entry present in an export PATH= line → found=True."""
        profile = tmp_path / ".bashrc"
        # POSIX-style bin dir: a Windows drive letter would collide with the
        # ':' separator that bash PATH assignments are split on.
        bin_dir = PurePosixPath("/home/dev/.agdt/bin")
        profile.write_text(f'export PATH="{bin_dir}:$PATH"\n', encoding="utf-8")

        with (
            patch(
                "agentic_devtools.cli.setup.dependency_checker._MANAGED_BIN_DIR",
                bin_dir,
            ),
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_type",
                return_value="bash",
            ),
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_profile",
                return_value=profile,
            ),
        ):
            status = _check_path_profile()

        assert status.found is True
        assert status.name == "path-profile"
        assert status.required is True


class TestCheckPathProfileMissing:
    """_check_path_profile returns found=False when entry missing."""

    def test_entry_not_in_profile(self, tmp_path: Path) -> None:
        """Profile exists but no PATH line with entry → found=False."""
        profile = tmp_path / ".bashrc"
        profile.write_text('export PATH="/usr/bin:$PATH"\n', encoding="utf-8")

        with (
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_type",
                return_value="bash",
            ),
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_profile",
                return_value=profile,
            ),
        ):
            status = _check_path_profile()

        assert status.found is False
        assert status.required is True

    def test_entry_in_comment_line(self, tmp_path: Path) -> None:
        """Entry present only in a comment, not in a PATH= line → found=False."""
        profile = tmp_path / ".bashrc"
        path_entry = str(Path.home() / ".agdt" / "bin")
        profile.write_text(f"# {path_entry}\n", encoding="utf-8")

        with (
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_type",
                return_value="bash",
            ),
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_profile",
                return_value=profile,
            ),
        ):
            status = _check_path_profile()

        assert status.found is False

    def test_superstring_path_component_not_treated_as_match(self, tmp_path: Path) -> None:
        """A superstring PATH component does not satisfy the managed entry check."""
        profile = tmp_path / ".bashrc"
        path_entry = str(Path.home() / ".agdt" / "bin")
        profile.write_text(
            f'export PATH="{path_entry}-tools:$PATH"\n',
            encoding="utf-8",
        )

        with (
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_type",
                return_value="bash",
            ),
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_profile",
                return_value=profile,
            ),
        ):
            status = _check_path_profile()

        assert status.found is False

    def test_profile_file_missing(self, tmp_path: Path) -> None:
        """Profile path points to nonexistent file → found=False."""
        profile = tmp_path / ".bashrc"  # Not created

        with (
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_type",
                return_value="bash",
            ),
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_profile",
                return_value=profile,
            ),
        ):
            status = _check_path_profile()

        assert status.found is False

    def test_profile_none_unknown_shell(self) -> None:
        """detect_shell_profile returns None for unknown shell → found=False, required=False."""
        with (
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_type",
                return_value="unknown",
            ),
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_profile",
                return_value=None,
            ),
        ):
            status = _check_path_profile()

        assert status.found is False
        assert status.required is False
        assert status.category == "Optional — unknown shell"

    def test_profile_none_known_shell(self) -> None:
        """detect_shell_profile returns None for a known shell → found=False, required=True."""
        with (
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_type",
                return_value="bash",
            ),
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_profile",
                return_value=None,
            ),
        ):
            status = _check_path_profile()

        assert status.found is False
        assert status.required is True

    def test_profile_read_error(self, tmp_path: Path) -> None:
        """Unreadable profile file is treated as missing instead of crashing."""
        profile = tmp_path / ".bashrc"
        profile.write_text("", encoding="utf-8")

        with (
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_type",
                return_value="bash",
            ),
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_profile",
                return_value=profile,
            ),
            patch.object(Path, "read_text", side_effect=PermissionError("denied")),
        ):
            status = _check_path_profile()

        assert status.found is False
        assert status.required is True
        assert status.install_hint == "run: agdt-setup (or agdt-setup-check --fix)"
        assert status.category == "Required"


class TestCheckPathProfilePowershell:
    """_check_path_profile handles PowerShell profiles."""

    def test_powershell_entry_found(self, tmp_path: Path) -> None:
        """PowerShell $env:PATH line with entry → found=True."""
        profile = tmp_path / "profile.ps1"
        path_entry = str(Path.home() / ".agdt" / "bin")
        profile.write_text(f'$env:PATH = "{path_entry};$env:PATH"\n', encoding="utf-8")

        with (
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_type",
                return_value="powershell",
            ),
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_profile",
                return_value=profile,
            ),
        ):
            status = _check_path_profile()

        assert status.found is True
        assert status.name == "path-profile"

    def test_powershell_entry_missing(self, tmp_path: Path) -> None:
        """PowerShell profile without the entry → found=False."""
        profile = tmp_path / "profile.ps1"
        profile.write_text('$env:PATH = "C:\\bin;$env:PATH"\n', encoding="utf-8")

        with (
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_type",
                return_value="powershell",
            ),
            patch(
                "agentic_devtools.cli.setup.shell_profile.detect_shell_profile",
                return_value=profile,
            ),
        ):
            status = _check_path_profile()

        assert status.found is False
