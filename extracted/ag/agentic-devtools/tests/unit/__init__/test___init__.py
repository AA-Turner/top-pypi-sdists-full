"""Tests for the agentic_devtools package initializer."""

import builtins
import importlib
import sys
from types import ModuleType
from unittest.mock import Mock

import pytest

_MISSING = object()


@pytest.fixture
def package_import_state(monkeypatch):
    """Restore package imports and module state after each reload test."""
    package = importlib.import_module("agentic_devtools")
    original_import = builtins.__import__
    package_state = package.__dict__.copy()
    package_module = sys.modules["agentic_devtools"]
    version_module = sys.modules.get("agentic_devtools._version", _MISSING)

    try:
        yield package, original_import
    finally:
        monkeypatch.setattr(builtins, "__import__", original_import)
        sys.modules["agentic_devtools"] = package_module
        if version_module is _MISSING:
            sys.modules.pop("agentic_devtools._version", None)
        else:
            sys.modules["agentic_devtools._version"] = version_module
        package.__dict__.clear()
        package.__dict__.update(package_state)


def _missing_version_import(original_import, error=None):
    if error is None:
        error = ModuleNotFoundError(
            "No module named 'agentic_devtools._version'",
            name="agentic_devtools._version",
        )

    def import_hook(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "agentic_devtools._version":
            raise error
        return original_import(name, globals, locals, fromlist, level)

    return import_hook


class TestPackageVersion:
    """Tests for the package version export."""

    def test_uses_generated_version_when_available(self, package_import_state, monkeypatch):
        package, original_import = package_import_state
        generated_version = ModuleType("agentic_devtools._version")
        generated_version.__version__ = "1.2.3"
        sys.modules["agentic_devtools._version"] = generated_version
        version_lookup = Mock(side_effect=AssertionError("metadata lookup should not run"))
        monkeypatch.setattr(importlib.metadata, "version", version_lookup)

        reloaded_package = importlib.reload(package)

        assert reloaded_package.__version__ == "1.2.3"
        version_lookup.assert_not_called()
        assert builtins.__import__ is original_import

    def test_uses_distribution_version_when_generated_module_is_missing(self, package_import_state, monkeypatch):
        package, original_import = package_import_state
        monkeypatch.setattr(
            builtins,
            "__import__",
            _missing_version_import(original_import),
        )
        version_lookup = Mock(return_value="4.5.6")
        monkeypatch.setattr(importlib.metadata, "version", version_lookup)

        reloaded_package = importlib.reload(package)

        assert reloaded_package.__version__ == "4.5.6"
        version_lookup.assert_called_once_with("agentic-devtools")

    def test_uses_unknown_version_when_distribution_metadata_is_absent(self, package_import_state, monkeypatch):
        package, original_import = package_import_state
        monkeypatch.setattr(
            builtins,
            "__import__",
            _missing_version_import(original_import),
        )
        version_lookup = Mock(side_effect=importlib.metadata.PackageNotFoundError)
        monkeypatch.setattr(importlib.metadata, "version", version_lookup)

        reloaded_package = importlib.reload(package)

        assert reloaded_package.__version__ == "0+unknown"
        version_lookup.assert_called_once_with("agentic-devtools")

    def test_propagates_unrelated_missing_import(self, package_import_state, monkeypatch):
        package, original_import = package_import_state
        missing_dependency = ModuleNotFoundError(
            "No module named 'unrelated_dependency'",
            name="unrelated_dependency",
        )
        monkeypatch.setattr(
            builtins,
            "__import__",
            _missing_version_import(original_import, missing_dependency),
        )
        version_lookup = Mock(side_effect=AssertionError("metadata lookup should not run"))
        monkeypatch.setattr(importlib.metadata, "version", version_lookup)

        with pytest.raises(ModuleNotFoundError) as exc_info:
            importlib.reload(package)

        assert exc_info.value is missing_dependency
        version_lookup.assert_not_called()
