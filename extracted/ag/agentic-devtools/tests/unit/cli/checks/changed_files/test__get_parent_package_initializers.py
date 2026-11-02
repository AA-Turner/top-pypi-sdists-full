"""Tests for _get_parent_package_initializers."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.checks.changed_files import _get_parent_package_initializers


def test_returns_only_indexed_parent_package_initializers(tmp_path: Path) -> None:
    """Returns indexed parent packages but excludes module parents."""
    module_paths = {
        "agentic_devtools": tmp_path / "agentic_devtools" / "__init__.py",
        "agentic_devtools.feature": tmp_path / "agentic_devtools" / "feature" / "__init__.py",
        "agentic_devtools.feature.worker": tmp_path / "agentic_devtools" / "feature" / "worker.py",
    }

    assert _get_parent_package_initializers("agentic_devtools.feature.worker", module_paths) == {
        "agentic_devtools",
        "agentic_devtools.feature",
    }


def test_returns_empty_without_indexed_package_parents(tmp_path: Path) -> None:
    """Does not treat regular modules or external paths as package initializers."""
    module_paths = {"external": tmp_path / "external.py"}

    assert _get_parent_package_initializers("external.child", module_paths) == set()
