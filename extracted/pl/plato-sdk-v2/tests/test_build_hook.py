"""Tests for the WorldSchemaHook build hook utilities.

The hook itself requires hatchling (a build-only dep), so we test the
static helper methods by importing them after mocking the hatchling base class.
"""

from __future__ import annotations

import sys
import types

import pytest


@pytest.fixture(autouse=True)
def _mock_hatchling():
    """Stub out hatchling so we can import build_hook without it installed."""
    fake_interface = types.ModuleType("hatchling.builders.hooks.plugin.interface")
    fake_interface.BuildHookInterface = type("BuildHookInterface", (), {})

    originals = {}
    for mod_name in [
        "hatchling",
        "hatchling.builders",
        "hatchling.builders.hooks",
        "hatchling.builders.hooks.plugin",
        "hatchling.builders.hooks.plugin.interface",
    ]:
        originals[mod_name] = sys.modules.get(mod_name)
        sys.modules[mod_name] = fake_interface

    yield

    for mod_name, orig in originals.items():
        if orig is None:
            sys.modules.pop(mod_name, None)
        else:
            sys.modules[mod_name] = orig
    # Force re-import on next use
    sys.modules.pop("plato.worlds.build_hook", None)


def _get_hook_class():
    from plato.worlds.build_hook import WorldSchemaHook

    return WorldSchemaHook


# ---------------------------------------------------------------------------
# _find_world_file
# ---------------------------------------------------------------------------


class TestFindWorldFile:
    def test_finds_file_with_register_world(self, tmp_path):
        pkg = tmp_path / "my_world"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("from .world import MyWorld\n")
        (pkg / "world.py").write_text('@register_world("my-world")\nclass MyWorld: pass\n')
        (pkg / "utils.py").write_text("# no decorator here\n")

        cls = _get_hook_class()
        result = cls._find_world_file(pkg)
        assert result is not None
        assert result.name == "world.py"

    def test_skips_init_py(self, tmp_path):
        pkg = tmp_path / "my_world"
        pkg.mkdir()
        (pkg / "__init__.py").write_text('@register_world("x")\nclass X: pass\n')

        cls = _get_hook_class()
        result = cls._find_world_file(pkg)
        assert result is None

    def test_returns_none_when_no_decorator(self, tmp_path):
        pkg = tmp_path / "my_world"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("")
        (pkg / "world.py").write_text("class MyWorld: pass\n")

        cls = _get_hook_class()
        result = cls._find_world_file(pkg)
        assert result is None

    def test_returns_none_for_missing_dir(self, tmp_path):
        cls = _get_hook_class()
        result = cls._find_world_file(tmp_path / "nonexistent")
        assert result is None


# ---------------------------------------------------------------------------
# _import_file
# ---------------------------------------------------------------------------


class TestImportFile:
    def test_imports_module_without_init(self, tmp_path):
        pkg = tmp_path / "test_pkg"
        pkg.mkdir()
        (pkg / "world.py").write_text("VALUE = 42\n")

        cls = _get_hook_class()
        sys.path.insert(0, str(tmp_path))
        try:
            cls._import_file("test_pkg", pkg / "world.py")

            assert "test_pkg" in sys.modules
            assert "test_pkg.world" in sys.modules
            assert sys.modules["test_pkg.world"].VALUE == 42
        finally:
            sys.path.remove(str(tmp_path))
            sys.modules.pop("test_pkg", None)
            sys.modules.pop("test_pkg.world", None)

    def test_registers_package_stub(self, tmp_path):
        pkg = tmp_path / "stub_pkg"
        pkg.mkdir()
        (pkg / "mod.py").write_text("X = 1\n")

        cls = _get_hook_class()
        sys.path.insert(0, str(tmp_path))
        try:
            cls._import_file("stub_pkg", pkg / "mod.py")

            stub = sys.modules["stub_pkg"]
            assert hasattr(stub, "__path__")
            assert stub.__package__ == "stub_pkg"
        finally:
            sys.path.remove(str(tmp_path))
            sys.modules.pop("stub_pkg", None)
            sys.modules.pop("stub_pkg.mod", None)

    def test_does_not_clobber_existing_package(self, tmp_path):
        pkg = tmp_path / "existing_pkg"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("INIT_VAR = 'original'\n")
        (pkg / "world.py").write_text("WORLD_VAR = 'loaded'\n")

        cls = _get_hook_class()
        sys.path.insert(0, str(tmp_path))
        try:
            # Pre-populate sys.modules with the real package
            import importlib

            real_pkg = importlib.import_module("existing_pkg")
            assert real_pkg.INIT_VAR == "original"

            # _import_file should not clobber the existing package
            cls._import_file("existing_pkg", pkg / "world.py")

            assert sys.modules["existing_pkg"].INIT_VAR == "original"
            assert sys.modules["existing_pkg.world"].WORLD_VAR == "loaded"
        finally:
            sys.path.remove(str(tmp_path))
            sys.modules.pop("existing_pkg", None)
            sys.modules.pop("existing_pkg.world", None)
