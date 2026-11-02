"""Tests for _get_imported_module_names."""

from __future__ import annotations

from agentic_devtools.cli.checks.changed_files import _get_imported_module_names


def test_resolves_absolute_and_relative_imports(tmp_path) -> None:
    """Resolves local modules while ignoring imports outside the repository."""
    source = tmp_path / "tests" / "unit" / "test_imports.py"
    source.parent.mkdir(parents=True)
    source.write_text(
        "import agentic_devtools.app\nfrom agentic_devtools import app\nfrom .. import helpers\nimport json\n",
        encoding="utf-8",
    )
    module_paths = {
        "agentic_devtools": tmp_path / "agentic_devtools" / "__init__.py",
        "agentic_devtools.app": tmp_path / "agentic_devtools" / "app.py",
        "tests.helpers": tmp_path / "tests" / "helpers.py",
    }

    assert _get_imported_module_names("tests.unit.test_imports", source, module_paths) == {
        "agentic_devtools",
        "agentic_devtools.app",
        "tests.helpers",
    }


def test_invalid_relative_import_and_unparseable_file_are_ignored(tmp_path) -> None:
    """Returns no dependency for an invalid relative path or malformed source."""
    invalid_relative = tmp_path / "tests" / "test_invalid.py"
    invalid_relative.parent.mkdir(parents=True)
    invalid_relative.write_text("from .. import missing\n", encoding="utf-8")
    malformed = tmp_path / "tests" / "test_malformed.py"
    malformed.write_text("from (", encoding="utf-8")
    module_paths = {"tests.missing": tmp_path / "tests" / "missing.py"}

    assert _get_imported_module_names("tests.test_invalid", invalid_relative, module_paths) == set()
    assert _get_imported_module_names("tests.test_malformed", malformed, module_paths) == set()
