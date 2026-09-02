"""Tests for _cleanup_partial_retro_spec in retro_spec/commands.py."""

from __future__ import annotations

from inspect import signature
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.retro_spec.commands import _cleanup_partial_retro_spec

_MOD = "agentic_devtools.cli.speckit.retro_spec.commands"


class TestCleanupPartialRetroSpec:
    """Tests for the _cleanup_partial_retro_spec function."""

    def test_cleanup_signature_includes_hierarchy_restore_params(self) -> None:
        """Cleanup includes hierarchy rollback parameters for atomic hierarchy registration."""
        parameters = signature(_cleanup_partial_retro_spec).parameters
        assert "hierarchy_path" in parameters
        assert "hierarchy_existed" in parameters
        assert "original_hierarchy_content" in parameters

    def test_skips_optional_cleanup_steps_when_paths_are_absent(self, tmp_path: Path) -> None:
        """Test that cleanup tolerates a missing generated spec file."""
        target_dir = tmp_path / "42"
        target_dir.mkdir()

        with patch(
            f"{_MOD}.subprocess.run",
            return_value=SimpleNamespace(returncode=0, stderr="", stdout=""),
        ):
            _cleanup_partial_retro_spec(
                spec_file=target_dir / "spec.md",
                target_dir=target_dir,
                target_dir_existed=True,
                specs_root=tmp_path,
            )

    def test_skips_git_reset_when_reset_index_is_false(self, tmp_path: Path) -> None:
        """Test that non-commit cleanup does not touch the git index."""
        target_dir = tmp_path / "42"
        target_dir.mkdir()

        with patch(f"{_MOD}.subprocess.run") as mock_run:
            _cleanup_partial_retro_spec(
                spec_file=target_dir / "spec.md",
                target_dir=target_dir,
                target_dir_existed=True,
                specs_root=tmp_path,
                reset_index=False,
            )

        mock_run.assert_not_called()

    def test_warns_when_reset_and_file_cleanup_fail(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that cleanup logs warnings when reset or file restoration fails."""
        git_root = tmp_path
        spec_file = tmp_path / "42" / "spec.md"
        spec_file.parent.mkdir(parents=True)
        spec_file.write_text("spec", encoding="utf-8")

        def _failing_unlink(path: Path, missing_ok: bool = False) -> None:
            if path == spec_file:
                raise OSError("spec fail")
            raise AssertionError(f"Unexpected unlink for {path}")

        with (
            patch(f"{_MOD}._get_git_root", return_value=git_root),
            patch(
                f"{_MOD}.subprocess.run",
                return_value=SimpleNamespace(returncode=1, stderr="reset failed"),
            ),
            patch.object(Path, "unlink", autospec=True, side_effect=_failing_unlink),
        ):
            _cleanup_partial_retro_spec(
                spec_file=spec_file,
                target_dir=spec_file.parent,
                target_dir_existed=True,
                specs_root=tmp_path,
            )

        err = capsys.readouterr().err
        assert "could not reset git index" in err
        assert "spec fail" in err

    def test_warns_when_reset_command_raises_oserror(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that git restore OSError is warned and cleanup continues."""
        git_root = tmp_path
        target_dir = tmp_path / "42"
        target_dir.mkdir()
        spec_file = target_dir / "spec.md"
        spec_file.write_text("generated", encoding="utf-8")

        with (
            patch(f"{_MOD}._get_git_root", return_value=git_root),
            patch(
                f"{_MOD}.subprocess.run",
                side_effect=OSError("git not found"),
            ),
        ):
            _cleanup_partial_retro_spec(
                spec_file=spec_file,
                target_dir=target_dir,
                target_dir_existed=True,
                specs_root=tmp_path,
            )

        assert not spec_file.exists()
        assert "could not reset git index" in capsys.readouterr().err

    def test_prunes_empty_dirs_when_target_did_not_exist(self, tmp_path: Path) -> None:
        """Test that newly-created target dir is pruned when cleanup runs."""
        target_dir = tmp_path / "specs" / "100" / "42"
        target_dir.mkdir(parents=True)
        specs_root = tmp_path / "specs"

        with patch(
            f"{_MOD}.subprocess.run",
            return_value=SimpleNamespace(returncode=0, stderr="", stdout=""),
        ):
            _cleanup_partial_retro_spec(
                spec_file=target_dir / "spec.md",
                target_dir=target_dir,
                target_dir_existed=False,
                specs_root=specs_root,
            )

        # Empty dirs should be pruned up to specs_root
        assert not target_dir.exists()

    def test_prunes_only_target_when_output_outside_specs_root(self, tmp_path: Path) -> None:
        """Test that pruning stops at target's parent when it is outside specs_root."""
        specs_root = tmp_path / "specs"
        specs_root.mkdir()
        # target_dir is outside specs_root (e.g. from a custom --output path)
        outside_parent = tmp_path / "custom"
        outside_parent.mkdir()
        target_dir = outside_parent / "out"
        target_dir.mkdir()

        with patch(
            f"{_MOD}.subprocess.run",
            return_value=SimpleNamespace(returncode=0, stderr="", stdout=""),
        ):
            _cleanup_partial_retro_spec(
                spec_file=target_dir / "my-spec.md",
                target_dir=target_dir,
                target_dir_existed=False,
                specs_root=specs_root,
            )

        # Only the created target dir is pruned; its parent is preserved.
        assert not target_dir.exists()
        assert outside_parent.exists()

    def test_uses_scoped_restore_when_git_root_is_available(
        self,
        tmp_path: Path,
    ) -> None:
        """Cleanup unstages only the generated spec file, not the whole index."""
        git_root = tmp_path
        spec_file = git_root / "specs" / "42" / "spec.md"
        spec_file.parent.mkdir(parents=True)
        spec_file.write_text("generated", encoding="utf-8")
        expected_rel = "specs/42/spec.md"

        with (
            patch(f"{_MOD}._get_git_root", return_value=git_root),
            patch(
                f"{_MOD}.subprocess.run",
                return_value=SimpleNamespace(returncode=0, stderr="", stdout=""),
            ) as mock_run,
        ):
            _cleanup_partial_retro_spec(
                spec_file=spec_file,
                target_dir=spec_file.parent,
                target_dir_existed=True,
                specs_root=git_root / "specs",
            )

        # Must use scoped restore, NOT bare reset
        run_calls = [list(c.args[0]) for c in mock_run.call_args_list if c.args]
        assert any(args == ["git", "restore", "--staged", "--", expected_rel] for args in run_calls), (
            f"Expected scoped restore call not found in: {run_calls}"
        )
        assert not any(args == ["git", "reset", "--quiet"] for args in run_calls), (
            "Bare git reset must not be used when relative path is available"
        )

    def test_falls_back_to_warning_when_git_root_unavailable(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Cleanup emits a warning and skips git index mutation when root is unavailable."""
        spec_file = tmp_path / "42" / "spec.md"
        spec_file.parent.mkdir()
        spec_file.write_text("generated", encoding="utf-8")

        with (
            patch(f"{_MOD}._get_git_root", return_value=None),
            patch(
                f"{_MOD}.subprocess.run",
                return_value=SimpleNamespace(returncode=0, stderr="", stdout=""),
            ) as mock_run,
        ):
            _cleanup_partial_retro_spec(
                spec_file=spec_file,
                target_dir=spec_file.parent,
                target_dir_existed=True,
                specs_root=tmp_path,
            )

        # No git commands must be issued — bare reset could clobber unrelated staged files.
        run_calls = [list(c.args[0]) for c in mock_run.call_args_list if c.args]
        assert not any(args[:2] == ["git", "reset"] for args in run_calls), (
            "Bare git reset must not be issued when git root is unavailable"
        )
        assert not any(args[:2] == ["git", "restore"] for args in run_calls), (
            "git restore must not be issued when relative spec path cannot be determined"
        )
        err = capsys.readouterr().err
        assert "git index was not modified" in err, "A warning about skipped index mutation must be emitted"

    def test_hierarchy_rollback_deletes_new_file_when_it_did_not_exist(self, tmp_path: Path) -> None:
        """Cleanup deletes a newly created hierarchy.yml when hierarchy_existed is False."""
        spec_file = tmp_path / "42" / "spec.md"
        spec_file.parent.mkdir()
        spec_file.write_text("generated", encoding="utf-8")
        hierarchy_file = tmp_path / "hierarchy.yml"
        hierarchy_file.write_text("newly created content", encoding="utf-8")

        with patch(f"{_MOD}._get_git_root", return_value=None):
            _cleanup_partial_retro_spec(
                spec_file=spec_file,
                target_dir=spec_file.parent,
                target_dir_existed=True,
                specs_root=tmp_path,
                hierarchy_path=hierarchy_file,
                hierarchy_existed=False,
            )

        assert not hierarchy_file.exists(), "Newly created hierarchy.yml must be deleted on rollback"

    def test_hierarchy_rollback_restores_original_content_when_file_existed(self, tmp_path: Path) -> None:
        """Cleanup restores the original hierarchy.yml content when hierarchy_existed is True."""
        original = "title: 'parent'\nlevel: epic\nchildren: []\n"
        spec_file = tmp_path / "42" / "spec.md"
        spec_file.parent.mkdir()
        spec_file.write_text("generated", encoding="utf-8")
        hierarchy_file = tmp_path / "hierarchy.yml"
        # Simulate the file having been modified by the write phase.
        hierarchy_file.write_text("mutated content with child entry", encoding="utf-8")

        with patch(f"{_MOD}._get_git_root", return_value=None):
            _cleanup_partial_retro_spec(
                spec_file=spec_file,
                target_dir=spec_file.parent,
                target_dir_existed=True,
                specs_root=tmp_path,
                hierarchy_path=hierarchy_file,
                hierarchy_existed=True,
                original_hierarchy_content=original,
            )

        assert hierarchy_file.read_text(encoding="utf-8") == original

    def test_hierarchy_rollback_skips_unlink_when_file_already_gone(self, tmp_path: Path) -> None:
        """Cleanup silently skips unlink when hierarchy_existed is False and file is already absent."""
        spec_file = tmp_path / "42" / "spec.md"
        spec_file.parent.mkdir()
        hierarchy_file = tmp_path / "hierarchy.yml"
        # hierarchy_file does NOT exist — simulates it never being written or already cleaned up.

        with patch(f"{_MOD}._get_git_root", return_value=None):
            _cleanup_partial_retro_spec(
                spec_file=spec_file,
                target_dir=spec_file.parent,
                target_dir_existed=True,
                specs_root=tmp_path,
                hierarchy_path=hierarchy_file,
                hierarchy_existed=False,
            )

        assert not hierarchy_file.exists()

    def test_hierarchy_rollback_warns_on_os_error(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Cleanup prints a warning and continues when the hierarchy file cannot be removed."""
        from unittest.mock import MagicMock

        spec_file = tmp_path / "42" / "spec.md"
        spec_file.parent.mkdir()
        # Use a mock for hierarchy_path so we can inject an OSError from unlink().
        hierarchy_mock = MagicMock(spec=Path)
        hierarchy_mock.exists.return_value = True
        hierarchy_mock.unlink.side_effect = OSError("permission denied")

        with patch(f"{_MOD}._get_git_root", return_value=None):
            _cleanup_partial_retro_spec(
                spec_file=spec_file,
                target_dir=spec_file.parent,
                target_dir_existed=True,
                specs_root=tmp_path,
                hierarchy_path=hierarchy_mock,
                hierarchy_existed=False,
            )

        err = capsys.readouterr().err
        assert "could not roll back hierarchy file" in err

    def test_cleanup_also_unstages_hierarchy_when_git_root_available(self, tmp_path: Path) -> None:
        """Cleanup unstages both spec and hierarchy files when hierarchy_path is provided."""
        git_root = tmp_path
        spec_file = git_root / "specs" / "42" / "spec.md"
        spec_file.parent.mkdir(parents=True)
        spec_file.write_text("generated", encoding="utf-8")
        hierarchy_file = git_root / "specs" / "100" / "hierarchy.yml"
        hierarchy_file.parent.mkdir(parents=True)
        hierarchy_file.write_text("hierarchy", encoding="utf-8")

        with (
            patch(f"{_MOD}._get_git_root", return_value=git_root),
            patch(
                f"{_MOD}.subprocess.run",
                return_value=SimpleNamespace(returncode=0, stderr="", stdout=""),
            ) as mock_run,
        ):
            _cleanup_partial_retro_spec(
                spec_file=spec_file,
                target_dir=spec_file.parent,
                target_dir_existed=True,
                specs_root=git_root / "specs",
                hierarchy_path=hierarchy_file,
                hierarchy_existed=False,
            )

        run_calls = [list(c.args[0]) for c in mock_run.call_args_list if c.args]
        assert any("specs/42/spec.md" in args and "specs/100/hierarchy.yml" in args for args in run_calls), (
            f"Expected both files in restore call, got: {run_calls}"
        )

    def test_hierarchy_outside_git_root_skips_hierarchy_unstage(self, tmp_path: Path) -> None:
        """Cleanup silently skips hierarchy unstage when hierarchy path is outside the git root."""
        git_root = tmp_path / "repo"
        git_root.mkdir()
        spec_file = git_root / "specs" / "42" / "spec.md"
        spec_file.parent.mkdir(parents=True)
        spec_file.write_text("generated", encoding="utf-8")
        # hierarchy file lives outside the git root → relative_to raises ValueError
        outside_hierarchy = tmp_path / "outside" / "hierarchy.yml"
        outside_hierarchy.parent.mkdir()
        outside_hierarchy.write_text("content", encoding="utf-8")

        with (
            patch(f"{_MOD}._get_git_root", return_value=git_root),
            patch(
                f"{_MOD}.subprocess.run",
                return_value=SimpleNamespace(returncode=0, stderr="", stdout=""),
            ) as mock_run,
        ):
            _cleanup_partial_retro_spec(
                spec_file=spec_file,
                target_dir=spec_file.parent,
                target_dir_existed=True,
                specs_root=git_root / "specs",
                hierarchy_path=outside_hierarchy,
                hierarchy_existed=False,
            )

        # Only the spec should be in the restore call — hierarchy outside root is silently skipped.
        run_calls = [list(c.args[0]) for c in mock_run.call_args_list if c.args]
        restore_args = next(
            (args for args in run_calls if "restore" in args),
            None,
        )
        assert restore_args is not None, "A git restore call must be issued for the spec"
        assert str(outside_hierarchy) not in " ".join(str(a) for a in restore_args), (
            "Hierarchy path outside git root must not appear in the restore call"
        )


class TestIsRelativeTo:
    """Tests for the _is_relative_to helper."""

    def test_returns_true_when_nested(self, tmp_path: Path) -> None:
        """Nested path returns True."""
        from agentic_devtools.cli.speckit.retro_spec.commands import _is_relative_to

        assert _is_relative_to(tmp_path / "a" / "b", tmp_path) is True

    def test_returns_false_when_not_nested(self, tmp_path: Path) -> None:
        """Unrelated path returns False."""
        from agentic_devtools.cli.speckit.retro_spec.commands import _is_relative_to

        assert _is_relative_to(tmp_path / "a", tmp_path / "b") is False
