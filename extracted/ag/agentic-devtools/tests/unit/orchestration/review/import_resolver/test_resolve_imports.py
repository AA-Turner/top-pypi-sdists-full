"""Tests for resolve_imports function."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.orchestration.review.import_resolver import resolve_imports


class TestResolveImports:
    """Tests for the full resolve_imports function."""

    def test_resolves_first_party_imports(self, tmp_path: Path) -> None:
        """Resolves first-party imports to file paths."""
        source = "from agentic_devtools.state import get_value\n"
        # Create the target file
        target = tmp_path / "agentic_devtools" / "state.py"
        target.parent.mkdir(parents=True)
        target.write_text("def get_value(): pass")

        result = resolve_imports(source, "/src/app.py", repo_root=tmp_path)
        assert "agentic_devtools/state.py" in result

    def test_ignores_third_party(self) -> None:
        """Third-party imports are not resolved."""
        source = "import requests\nfrom os import path\n"
        result = resolve_imports(source, "/src/app.py")
        assert result == []

    def test_cycle_prevention(self, tmp_path: Path) -> None:
        """Visited set prevents infinite loops."""
        source = "from agentic_devtools.state import get_value\n"
        target = tmp_path / "agentic_devtools" / "state.py"
        target.parent.mkdir(parents=True)
        target.write_text("")

        # Pass the same file as visited
        result = resolve_imports(
            source, "agentic_devtools/state.py", visited={"agentic_devtools/state.py"}, repo_root=tmp_path
        )
        # The import itself points to state.py which is in visited
        assert "agentic_devtools/state.py" not in result

    def test_max_depth_zero_raises_value_error(self) -> None:
        """max_depth=0 raises ValueError (invalid depth)."""
        source = "from agentic_devtools.state import get_value\n"
        with pytest.raises(ValueError, match="max_depth must be a positive integer"):
            resolve_imports(source, "/src/app.py", max_depth=0)

    def test_max_depth_negative_raises_value_error(self) -> None:
        """Negative max_depth raises ValueError."""
        source = "from agentic_devtools.state import get_value\n"
        with pytest.raises(ValueError, match="max_depth must be a positive integer"):
            resolve_imports(source, "/src/app.py", max_depth=-1)

    def test_no_imports_returns_empty(self) -> None:
        """Source with no imports returns empty."""
        source = "x = 1\ny = 2\n"
        result = resolve_imports(source, "/src/app.py")
        assert result == []

    def test_package_init_fallback(self, tmp_path: Path) -> None:
        """Falls back to __init__.py when module file doesn't exist."""
        pkg_dir = tmp_path / "agentic_devtools" / "cli"
        pkg_dir.mkdir(parents=True)
        (pkg_dir / "__init__.py").write_text("")

        source = "from agentic_devtools.cli import something\n"
        result = resolve_imports(source, "/src/app.py", repo_root=tmp_path)
        assert "agentic_devtools/cli/__init__.py" in result

    def test_no_repo_root_skips_file_check(self) -> None:
        """When repo_root is None, includes without file existence check."""
        source = "from agentic_devtools.state import get_value\n"
        result = resolve_imports(source, "/src/app.py", repo_root=None)
        assert "agentic_devtools/state.py" in result

    def test_no_repo_root_includes_package_init_candidate(self) -> None:
        """When repo_root is None, both module-file and package __init__ candidates are returned.

        Without filesystem access we cannot distinguish ``agentic_devtools/cli.py`` from
        ``agentic_devtools/cli/__init__.py``, so both are returned for the upstream fetcher
        to attempt.
        """
        source = "from agentic_devtools.cli import something\n"
        result = resolve_imports(source, "/src/app.py", repo_root=None)
        assert "agentic_devtools/cli.py" in result
        assert "agentic_devtools/cli/__init__.py" in result

    def test_no_repo_root_skips_already_visited_init_candidate(self) -> None:
        """When repo_root is None and __init__.py candidate is already visited, only module file returned."""
        source = "from agentic_devtools.cli import something\n"
        result = resolve_imports(
            source,
            "/src/app.py",
            repo_root=None,
            visited={"agentic_devtools/cli/__init__.py"},
        )
        assert "agentic_devtools/cli.py" in result
        assert "agentic_devtools/cli/__init__.py" not in result

    def test_file_not_found_skipped(self, tmp_path: Path) -> None:
        """Non-existent file with repo_root is skipped."""
        (tmp_path / "agentic_devtools").mkdir(parents=True)
        source = "from agentic_devtools.nonexistent import foo\n"
        result = resolve_imports(source, "/src/app.py", repo_root=tmp_path)
        assert result == []

    def test_affected_import_filtering(self, tmp_path: Path) -> None:
        """Only imports affected by diff lines are included."""
        source = (
            "from agentic_devtools.state import get_value\nfrom agentic_devtools.config import load\nx = get_value()\n"
        )
        (tmp_path / "agentic_devtools").mkdir(parents=True)
        (tmp_path / "agentic_devtools" / "state.py").write_text("")
        (tmp_path / "agentic_devtools" / "config.py").write_text("")

        # Only line 3 changed, which references get_value
        result = resolve_imports(source, "/src/app.py", diff_lines=[3], repo_root=tmp_path)
        assert "agentic_devtools/state.py" in result
        # config's load is not referenced in the diff line
        assert "agentic_devtools/config.py" not in result


class TestResolveImportsUnaffected:
    """Tests for imports already visited (cycle at import level)."""

    def test_resolved_import_already_visited(self) -> None:
        """Resolved import path already in visited set is skipped."""
        source = "from agentic_devtools.state import get_value\n"
        # visited contains the resolved path → continue
        result = resolve_imports(
            source,
            "src/app.py",
            visited={"agentic_devtools/state.py"},
        )
        assert result == []


class TestResolveImportsRelative:
    """Tests for relative import qualification."""

    def test_single_dot_relative_import_is_qualified(self, tmp_path: Path) -> None:
        """from .config import X is resolved relative to the current file's package."""
        source = "from .config import SomeClass\nx = SomeClass()\n"
        pkg = tmp_path / "agentic_devtools" / "cli" / "git"
        pkg.mkdir(parents=True)
        (pkg / "config.py").write_text("")

        result = resolve_imports(
            source,
            "agentic_devtools/cli/git/core.py",
            repo_root=tmp_path,
        )
        assert "agentic_devtools/cli/git/config.py" in result

    def test_double_dot_relative_import_is_qualified(self, tmp_path: Path) -> None:
        """from ..state import get_value is resolved two levels up."""
        source = "from ..state import get_value\nx = get_value()\n"
        pkg = tmp_path / "agentic_devtools" / "cli"
        pkg.mkdir(parents=True)
        (pkg / "state.py").write_text("")

        result = resolve_imports(
            source,
            "agentic_devtools/cli/git/core.py",
            repo_root=tmp_path,
        )
        assert "agentic_devtools/cli/state.py" in result

    def test_relative_import_level_exceeds_depth_is_skipped(self) -> None:
        """Relative import going above the root is skipped gracefully."""
        source = "from ...external import something\nx = something()\n"
        result = resolve_imports(source, "agentic_devtools/state.py")
        assert result == []

    def test_relative_import_third_party_package_excluded(self, tmp_path: Path) -> None:
        """Relative imports that resolve outside agentic_devtools are excluded."""
        source = "from .helpers import util\nx = util()\n"
        # File is in a non-first-party package, so resolved path will not start
        # with agentic_devtools/ and _resolve_module_to_path returns None.
        result = resolve_imports(source, "third_party/module.py", repo_root=tmp_path)
        assert result == []

    def test_module_less_relative_import_resolved(self, tmp_path: Path) -> None:
        """from . import state is resolved as a sibling module."""
        source = "from . import state\nx = state.get_value()\n"
        pkg = tmp_path / "agentic_devtools" / "cli" / "git"
        pkg.mkdir(parents=True)
        (pkg / "state.py").write_text("")

        result = resolve_imports(
            source,
            "agentic_devtools/cli/git/core.py",
            repo_root=tmp_path,
        )
        assert "agentic_devtools/cli/git/state.py" in result
