"""Tests for _build_static_import_graph."""

from __future__ import annotations

from agentic_devtools.cli.checks.changed_files import _build_static_import_graph


def test_indexes_local_modules_and_reverse_imports(tmp_path) -> None:
    """Maps repository modules to their importers."""
    source = tmp_path / "agentic_devtools" / "app.py"
    source.parent.mkdir(parents=True)
    source.write_text("VALUE = 1\n", encoding="utf-8")
    test = tmp_path / "tests" / "test_app.py"
    test.parent.mkdir(parents=True)
    test.write_text("from agentic_devtools.app import VALUE\n", encoding="utf-8")

    module_paths, path_modules, reverse_imports = _build_static_import_graph(tmp_path)

    assert module_paths["agentic_devtools.app"] == source
    assert path_modules["tests/test_app.py"] == "tests.test_app"
    assert reverse_imports["agentic_devtools.app"] == {"tests.test_app"}


def test_skips_missing_module_roots(tmp_path) -> None:
    """Returns empty indexes if neither repository Python root exists."""
    assert _build_static_import_graph(tmp_path) == ({}, {}, {})
