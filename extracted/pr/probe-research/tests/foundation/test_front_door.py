"""A split module's front door behaves like the old single module: live reads, and a patch (and
its undo) on the package lands on every piece bound to the name; a lazy door loads nothing first."""

from __future__ import annotations

import importlib
import sys
from unittest import mock

import pytest

PIECE_A = "import json\n\nLIMIT = 3\n\n\ndef helper():\n    return LIMIT\n"
PIECE_B = "from fdpkg.a import helper\n\n\ndef run():\n    return helper()\n"
HOMES = '{"LIMIT": "fdpkg.a", "helper": "fdpkg.a", "run": "fdpkg.b", "json": "fdpkg.a"}'
#: The old module's pieces: `d` holds no old name, only a copy one; `c` is a separate module.
PIECES = '("fdpkg.a", "fdpkg.b", "fdpkg.d")'
EAGER = (
    "from probe.foundation.front_door.front_door import serve_pieces\n\nfrom . import a, b, d  # noqa: F401\n\n"
    f"serve_pieces(__name__, {HOMES}, pieces={PIECES})\n"
)
LAZY = (
    "from probe.foundation.front_door.front_door import serve_pieces\n\n"
    f"serve_pieces(__name__, {HOMES}, pieces={PIECES}, is_lazy=True)\n"
)


def _package(tmp_path, monkeypatch, door: str):
    root = tmp_path / "fdpkg"
    root.mkdir()
    (root / "__init__.py").write_text(door)
    (root / "a.py").write_text(PIECE_A)
    (root / "b.py").write_text(PIECE_B)
    (root / "c.py").write_text("import json\n\nVALUE = 1\n")
    # A piece that only imports a name: no old name lives here, yet a patch must reach its copy.
    (root / "d.py").write_text("from fdpkg.a import LIMIT, helper\n\n\ndef call():\n    return helper() + LIMIT\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    return importlib.import_module("fdpkg")


@pytest.fixture(params=["eager", "lazy"])
def pkg(request, tmp_path, monkeypatch):
    yield _package(tmp_path, monkeypatch, EAGER if request.param == "eager" else LAZY)
    for name in [n for n in sys.modules if n == "fdpkg" or n.startswith("fdpkg.")]:
        del sys.modules[name]


def test_names_and_imported_names_are_served_live(pkg) -> None:
    assert pkg.run() == 3 and pkg.LIMIT == 3
    assert pkg.json is sys.modules["json"]  # an imported name the old module exposed
    pkg.a.LIMIT = 5
    assert pkg.LIMIT == 5 and pkg.run() == 5
    with pytest.raises(AttributeError):
        _ = pkg.nothing_here


def test_a_patch_reaches_every_piece_bound_to_the_name_and_undoes_cleanly(pkg) -> None:
    real = pkg.helper
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(pkg, "helper", lambda: 99)
        assert pkg.run() == 99 and pkg.a.helper() == 99 and pkg.b.helper() == 99
    assert pkg.a.helper is real and pkg.b.helper is real and pkg.run() == 3
    assert "helper" not in vars(pkg)


def test_an_undo_that_deletes_puts_the_pieces_back(pkg) -> None:
    """pytest >= 9.2 records the package's own dict entry (absent) and undoes with delattr."""
    real = pkg.helper
    pkg.helper = lambda: 1
    pkg.helper = lambda: 2  # nested: the inner write keeps the first override's originals
    del pkg.helper
    assert pkg.a.helper is real and pkg.b.helper is real and pkg.run() == 3
    assert "helper" not in vars(pkg)


def test_nested_patches_unwind_in_order(pkg) -> None:
    real = pkg.helper
    with pytest.MonkeyPatch.context() as outer:
        outer.setattr(pkg, "helper", lambda: 1)
        with pytest.MonkeyPatch.context() as inner:
            inner.setattr(pkg, "helper", lambda: 2)
            assert pkg.run() == 2
        assert pkg.run() == 1
    assert pkg.a.helper is real and pkg.b.helper is real and "helper" not in vars(pkg)


def test_mock_patch_enters_and_exits_through_the_door(pkg) -> None:
    with mock.patch.object(pkg, "LIMIT", 42):
        assert pkg.a.helper() == 42
    assert pkg.a.helper() == 3 and "LIMIT" not in vars(pkg)


def test_a_plain_write_never_hides_a_later_rebinding_in_the_piece(pkg) -> None:
    """A reset by plain assignment (the conftest's `fluent._exit_status = ...`) keeps no stale copy."""
    pkg.LIMIT = 5
    assert pkg.a.LIMIT == 5
    pkg.a.LIMIT = 7  # the piece's own code rebinds its global
    assert pkg.LIMIT == 7 and pkg.run() == 7
    del pkg.LIMIT


def test_patching_a_name_to_the_value_it_holds_undoes_cleanly(pkg) -> None:
    real = pkg.helper
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(pkg, "helper", real)
    assert pkg.a.helper is real and pkg.b.helper is real and pkg.run() == 3
    with mock.patch.object(pkg, "LIMIT", 3):
        assert pkg.LIMIT == 3
    assert pkg.a.LIMIT == 3 and "LIMIT" not in vars(pkg)


def test_a_patch_after_a_plain_write_restores_the_live_value(pkg) -> None:
    pkg.LIMIT = 5  # a reset by plain assignment, never undone
    pkg.a.LIMIT = 7  # then the piece rebinds it itself
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(pkg, "LIMIT", 9)
        assert pkg.run() == 9
    assert pkg.LIMIT == 7 and pkg.a.LIMIT == 7
    del pkg.LIMIT


def test_a_patch_reaches_a_piece_that_only_imports_the_name(pkg) -> None:
    importlib.import_module("fdpkg.d")
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(pkg, "helper", lambda: 100)
        assert pkg.d.call() == 103
    assert pkg.d.call() == 6


def test_a_patch_never_reaches_a_module_that_is_not_a_piece(pkg) -> None:
    importlib.import_module("fdpkg.c")
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(pkg, "json", "not json")
        assert pkg.a.json == "not json"
        assert pkg.c.json is sys.modules["json"]


def test_undoing_a_delete_puts_the_name_back_and_a_second_delete_raises(pkg) -> None:
    with pytest.MonkeyPatch.context() as patch:
        patch.delattr(pkg, "LIMIT")
        assert not hasattr(pkg.a, "LIMIT")
        with pytest.raises(AttributeError):
            del pkg.LIMIT
    assert pkg.a.LIMIT == 3 and pkg.LIMIT == 3 and pkg.run() == 3


def test_a_submodule_imported_later_stays_a_package_attribute(pkg) -> None:
    importlib.import_module("fdpkg.c")
    assert pkg.c.VALUE == 1 and "c" in vars(pkg)


def test_a_lazy_door_loads_only_the_piece_a_read_needs(tmp_path, monkeypatch) -> None:
    pkg = _package(tmp_path, monkeypatch, LAZY)
    try:
        assert "fdpkg.a" not in sys.modules and "fdpkg.b" not in sys.modules
        assert pkg.LIMIT == 3
        assert "fdpkg.a" in sys.modules and "fdpkg.b" not in sys.modules
        from fdpkg import run  # `from door import name` goes through the door too

        assert run() == 3
    finally:
        for name in [n for n in sys.modules if n == "fdpkg" or n.startswith("fdpkg.")]:
            del sys.modules[name]
