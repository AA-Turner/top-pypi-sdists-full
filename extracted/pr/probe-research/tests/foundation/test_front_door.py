"""A split module's front door behaves like the old single module: live reads, and a patch (and
its undo) on the package lands on every piece bound to the name; a lazy door loads nothing first,
and a deferred one loads whole on its first read."""

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
DEFERRED = (
    "from probe.foundation.front_door.front_door import serve_pieces\n\n"
    f"serve_pieces(__name__, {HOMES}, pieces={PIECES}, is_loaded_on_first_read=True)\n"
)
DOORS = {"eager": EAGER, "lazy": LAZY, "deferred": DEFERRED}


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


@pytest.fixture(params=sorted(DOORS))
def pkg(request, tmp_path, monkeypatch):
    yield _package(tmp_path, monkeypatch, DOORS[request.param])
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


def test_a_deferred_door_loads_nothing_until_read_then_every_piece(tmp_path, monkeypatch) -> None:
    """cli/wizard: a command imports one piece of the folder; the rest load on the first read."""
    try:
        _package(tmp_path, monkeypatch, DEFERRED)
        importlib.import_module("fdpkg.d")
        assert "fdpkg.b" not in sys.modules
        door = sys.modules["fdpkg"]
        assert door.run() == 3
        assert {"fdpkg.a", "fdpkg.b", "fdpkg.d"} <= set(sys.modules)
        with pytest.MonkeyPatch.context() as patch:  # binders as an eager door's: every holder
            patch.setattr(door, "helper", lambda: 7)
            assert door.d.call() == 7 + 3 and door.run() == 7
        assert door.run() == 3
    finally:
        for name in [n for n in sys.modules if n == "fdpkg" or n.startswith("fdpkg.")]:
            del sys.modules[name]


def test_a_deferred_door_read_by_two_threads_at_once_loads_once_in_door_order(tmp_path, monkeypatch) -> None:
    """Two first reads at once: the second waits for the first thread's load. Before, it imported
    its own piece meanwhile, and the two imports handed each other half-run pieces."""
    import threading
    import time

    root = tmp_path / "fdrace"
    root.mkdir()
    (root / "__init__.py").write_text(
        "from probe.foundation.front_door.front_door import serve_pieces\n\n"
        'serve_pieces(__name__, {"LIMIT": "fdrace.a", "helper": "fdrace.a", "run": "fdrace.b"}, '
        'pieces=("fdrace.a", "fdrace.b"), is_loaded_on_first_read=True)\n'
    )
    # a is slow and needs b at its bottom; b needs a at its top (the split's bottom imports).
    (root / "a.py").write_text(
        "import time\n\ntime.sleep(0.3)\nLIMIT = 3\n\n\ndef helper():\n    return LIMIT\n\n\n"
        "from fdrace.b import run  # noqa: E402,F401\n"
    )
    (root / "b.py").write_text("from fdrace.a import helper\n\n\ndef run():\n    return helper()\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    try:
        door = importlib.import_module("fdrace")
        answers, errors = {}, []

        def read(name: str) -> None:
            try:
                answers[name] = getattr(door, name)
            except Exception as exc:  # noqa: BLE001 -- the assertion below names it
                errors.append(exc)

        first = threading.Thread(target=read, args=("LIMIT",))
        first.start()
        deadline = time.monotonic() + 5
        while "fdrace.a" not in sys.modules and time.monotonic() < deadline:
            time.sleep(0.005)  # the first thread is inside a's import
        second = threading.Thread(target=read, args=("run",))
        second.start()
        first.join(10)
        second.join(10)
        assert errors == [] and answers["LIMIT"] == 3 and answers["run"]() == 3
    finally:
        for name in [n for n in sys.modules if n == "fdrace" or n.startswith("fdrace.")]:
            del sys.modules[name]


def test_a_lazy_door_read_by_two_threads_at_once_loads_one_piece_at_a_time(tmp_path, monkeypatch) -> None:
    """cli/imports/folder's shape: a first read loads a piece under an eager sub-door whose pieces
    cycle back to the piece another thread's first read is loading. Unserialized, the threads waited
    on each other's module locks and got half-run modules (ImportError; `_DeadlockError` on the real door)."""
    import threading
    import time

    root = tmp_path / "fdlazy"
    (root / "flow").mkdir(parents=True)
    (root / "__init__.py").write_text(
        "from probe.foundation.front_door.front_door import serve_pieces\n\n"
        'serve_pieces(__name__, {"choose": "fdlazy.flow.choices", "landed": "fdlazy.flow.landed"}, '
        'pieces=("fdlazy.flow.choices", "fdlazy.flow.landed"), is_lazy=True)\n'
    )
    # flow/'s door is eager and slow; its piece needs landed, and landed imports flow/ back.
    (root / "flow" / "__init__.py").write_text("import time\n\ntime.sleep(0.3)\nfrom fdlazy.flow import orch  # noqa: E402,F401\n")
    (root / "flow" / "orch.py").write_text("from fdlazy.flow.landed import landed  # noqa: F401\n")
    (root / "flow" / "landed.py").write_text("import fdlazy.flow  # noqa: F401\n\n\ndef landed():\n    return 1\n")
    (root / "flow" / "choices.py").write_text("def choose():\n    return 2\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    try:
        door = importlib.import_module("fdlazy")
        answers, errors = {}, []

        def read(name: str) -> None:
            try:
                answers[name] = getattr(door, name)()
            except Exception as exc:  # noqa: BLE001 -- the assertion below names it
                errors.append(exc)

        first = threading.Thread(target=read, args=("choose",))
        first.start()
        deadline = time.monotonic() + 5
        while "fdlazy.flow" not in sys.modules and time.monotonic() < deadline:
            time.sleep(0.005)  # the first thread is inside flow/'s door
        second = threading.Thread(target=read, args=("landed",))
        second.start()
        first.join(10)
        second.join(10)
        assert errors == [] and answers == {"choose": 2, "landed": 1}
    finally:
        for name in [n for n in sys.modules if n == "fdlazy" or n.startswith("fdlazy.")]:
            del sys.modules[name]


def test_a_lazy_door_read_past_a_lock_held_too_long_still_answers(tmp_path, monkeypatch) -> None:
    """Another thread holding the door's lock past the wait: the read loads its piece unlocked
    (the fallback that keeps a cross-thread wait from hanging) and leaves the lock as it found it."""
    import threading

    from probe.foundation.front_door import front_door

    root = tmp_path / "fdwait"
    root.mkdir()
    (root / "__init__.py").write_text(
        "from probe.foundation.front_door.front_door import serve_pieces\n\n"
        'serve_pieces(__name__, {"x": "fdwait.a"}, pieces=("fdwait.a",), is_lazy=True)\n'
    )
    (root / "a.py").write_text("x = 7\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    monkeypatch.setattr(front_door, "_LOAD_WAIT_S", 0.2)
    try:
        door = importlib.import_module("fdwait")
        lock, held, done = vars(door)["_load_lock"], threading.Event(), threading.Event()

        def hold() -> None:
            with lock:
                held.set()
                done.wait(5)

        holder = threading.Thread(target=hold)
        holder.start()
        assert held.wait(5)
        assert door.x == 7
        done.set()
        holder.join(5)
        assert lock.acquire(timeout=1)  # not left held by the read
        lock.release()
    finally:
        for name in [n for n in sys.modules if n == "fdwait" or n.startswith("fdwait.")]:
            del sys.modules[name]


MODULE_DOOR = (
    "from probe.foundation.front_door.front_door import serve_pieces\n"
    "from fdmod.a import helper\n"
    "from fdmod.b import run as other_run\n\n\n"
    "def run():  # the door's own function: it reads its own global `helper`\n"
    "    return helper() + 100\n\n\n"
    f"serve_pieces(__name__, {HOMES.replace('fdpkg', 'fdmod')}, pieces={PIECES.replace('fdpkg', 'fdmod')})\n"
)


def test_a_door_that_is_a_module_keeps_its_own_globals_through_a_patch_and_its_undo(tmp_path, monkeypatch) -> None:
    """cli/main.py stays its split's door and its functions read its globals: an undo puts the
    door's own value back (never drops it), and a piece's `run` never hides the door's own."""
    root = tmp_path / "fdmod"
    root.mkdir()
    (root / "__init__.py").write_text("")
    (root / "a.py").write_text(PIECE_A.replace("fdpkg", "fdmod"))
    (root / "b.py").write_text(PIECE_B.replace("fdpkg", "fdmod"))
    (root / "d.py").write_text("from fdmod.a import LIMIT, helper\n")
    (tmp_path / "fddoor.py").write_text(MODULE_DOOR)
    monkeypatch.syspath_prepend(str(tmp_path))
    try:
        door = importlib.import_module("fddoor")
        assert door.run() == 103  # its own run(), not the piece's
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(door, "helper", lambda: 1)
            assert door.run() == 101 and door.other_run() == 1
        assert door.run() == 103 and door.other_run() == 3
        real = door.helper
        door.helper = lambda: 2  # pytest >= 9.2's undo deletes
        del door.helper
        assert door.run() == 103 and door.helper is real
        with pytest.MonkeyPatch.context() as patch:  # a delete, then its undo
            patch.delattr(door, "helper")
            with pytest.raises(NameError):
                door.run()
        assert door.run() == 103 and door.helper is real and door.other_run() == 3
    finally:
        for name in [n for n in sys.modules if n in ("fdmod", "fddoor") or n.startswith("fdmod.")]:
            del sys.modules[name]


def test_an_eager_door_leaves_its_deferred_pieces_until_a_read_or_a_write_needs_them(tmp_path, monkeypatch) -> None:
    """cli/main.py's wizard and harness helpers: not loaded at import; a read of one of their names
    loads that piece; a write loads them all first, so a patch reaches every holder."""
    door_code = (
        "from probe.foundation.front_door.front_door import serve_pieces\n\n"
        f"serve_pieces(__name__, {HOMES}, pieces={PIECES}, deferred=('fdpkg.b', 'fdpkg.d'))\n"
    )
    try:
        door = _package(tmp_path, monkeypatch, door_code)
        assert "fdpkg.a" in sys.modules and "fdpkg.b" not in sys.modules and "fdpkg.d" not in sys.modules
        assert door.run() == 3 and "fdpkg.b" in sys.modules
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(door, "helper", lambda: 7)
            assert "fdpkg.d" in sys.modules
            assert door.run() == 7 and sys.modules["fdpkg.d"].call() == 7 + 3
        assert door.run() == 3 and sys.modules["fdpkg.d"].call() == 3 + 3
    finally:
        for name in [n for n in sys.modules if n == "fdpkg" or n.startswith("fdpkg.")]:
            del sys.modules[name]
