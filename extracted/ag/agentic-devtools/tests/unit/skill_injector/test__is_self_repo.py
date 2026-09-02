"""Tests for agentic_devtools.skill_injector._is_self_repo."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.skill_injector import _is_self_repo

_SELF_PYPROJECT = '[build-system]\nrequires = ["hatchling"]\n\n[project]\nname = "agentic-devtools"\n'


def _make_self_checkout(root: Path, pyproject: str = _SELF_PYPROJECT) -> None:
    """Create the marker files that identify an agentic-devtools checkout."""
    package = root / "agentic_devtools"
    package.mkdir(parents=True, exist_ok=True)
    (package / "skill_injector.py").write_text("", encoding="utf-8")
    (root / "pyproject.toml").write_text(pyproject, encoding="utf-8")


class TestIsSelfRepo:
    """Tests for the _is_self_repo function."""

    def test_true_for_wheel_install_marker_files(self, tmp_path) -> None:
        """Package source + [project] name = agentic-devtools → self repo."""
        _make_self_checkout(tmp_path)
        assert _is_self_repo(tmp_path) is True

    def test_true_for_editable_install_same_repo_root(self, tmp_path) -> None:
        """The running package's own repo root is always the self repo."""
        module_path = tmp_path / "agentic_devtools" / "skill_injector.py"
        module_path.parent.mkdir(parents=True)
        module_path.write_text("", encoding="utf-8")
        with patch("agentic_devtools.skill_injector.__file__", str(module_path)):
            # No pyproject.toml at all — the path signal alone must suffice.
            assert _is_self_repo(tmp_path) is True

    def test_false_for_unrelated_repo(self, tmp_path) -> None:
        """A plain target repo is not the self repo."""
        (tmp_path / ".github").mkdir()
        assert _is_self_repo(tmp_path) is False

    def test_false_when_pyproject_declares_other_project(self, tmp_path) -> None:
        """Package-shaped directory but a different project name → not self."""
        _make_self_checkout(tmp_path, '[project]\nname = "some-other-tool"\n')
        assert _is_self_repo(tmp_path) is False

    def test_false_when_name_outside_project_table(self, tmp_path) -> None:
        """A matching name in another table must not be mistaken for [project]."""
        _make_self_checkout(
            tmp_path,
            '[tool.example]\nname = "agentic-devtools"\n\n[project]\nname = "other"\n',
        )
        assert _is_self_repo(tmp_path) is False

    def test_false_when_pyproject_missing(self, tmp_path) -> None:
        """Package source without a readable pyproject.toml → not self."""
        package = tmp_path / "agentic_devtools"
        package.mkdir()
        (package / "skill_injector.py").write_text("", encoding="utf-8")
        assert _is_self_repo(tmp_path) is False

    def test_false_when_pyproject_is_not_utf8(self, tmp_path) -> None:
        """Undecodable pyproject.toml is treated as 'not the self repo'."""
        _make_self_checkout(tmp_path)
        (tmp_path / "pyproject.toml").write_bytes(b"\xff\xfe\x00name")
        assert _is_self_repo(tmp_path) is False

    def test_true_when_name_has_inline_comment(self, tmp_path) -> None:
        """name = "agentic-devtools" # comment is valid TOML and must match."""
        _make_self_checkout(
            tmp_path,
            '[project]\nname = "agentic-devtools" # package name\n',
        )
        assert _is_self_repo(tmp_path) is True

    def test_false_when_resolve_raises_oserror(self, tmp_path) -> None:
        """An unresolvable path is treated as 'not the self repo'."""
        with patch.object(Path, "resolve", side_effect=OSError("boom")):
            assert _is_self_repo(tmp_path) is False
