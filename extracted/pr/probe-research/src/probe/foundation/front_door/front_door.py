"""A split module's package served like the old module: live reads, and a write lands on every piece
bound to the name. Twin of app/core/front_door, plus a lazy door that loads a piece on first use."""

from __future__ import annotations

import importlib
import pkgutil
import sys
import threading
import types
from collections.abc import Mapping, Sequence

_MISSING = object()
#: How long a first read waits for another thread's load through the door (s). Past it (a piece
#: that read the door while it loads, in another thread) the read loads the name's piece itself.
_LOAD_WAIT_S = 10.0


class FrontDoor(types.ModuleType):
    """A package serving its pieces' names; `_homes` maps a name to the piece that holds it and
    `_binders` (filled at once, or on a lazy door's first write) to every piece that binds it.

    A write is an override: it lands on every binder (every loaded piece holding that object) and
    remembers what they held. It also sits in the package's own dict, which pytest >= 9.2 reads as
    the old value to undo nested patches, so each read refreshes that copy from the piece. Deleting
    it (how pytest >= 9.2 and mock.patch undo a patch) puts the pieces back; writing the original
    back later clears it too. A plain write never undone keeps the one value it replaced. Not
    covered: mock.patch reads the dict copy without a read through the door, so after a piece
    rebinds a global itself it can restore the copy (patch the piece; first-party code does)."""

    _homes: dict[str, str]
    _binders: dict[str, tuple[types.ModuleType, ...]]
    _saved: dict[str, tuple[object, ...]]

    def __getattribute__(self, name: str):
        # A served name is always read from its piece: the door's own copy is only pytest's
        # bookkeeping for an override, and goes stale once the piece rebinds the name itself.
        if not name.startswith("__"):
            own = object.__getattribute__(self, "__dict__")
            binders = own.get("_binders", {}).get(name)
            if binders:
                value = getattr(binders[0], name)
                if name in own and own[name] is not value:
                    own[name] = value  # keep pytest's copy current (it undoes by restoring it)
                return value
        return super().__getattribute__(name)

    def __getattr__(self, name: str):
        own = vars(self)
        binders = own["_binders"].get(name)
        if binders:
            return getattr(binders[0], name)
        home = own["_homes"].get(name)
        if own.get("_is_loaded_on_first_read"):  # a deferred door: load it whole, then answer
            if home is None and name.startswith("__"):  # the import system's probes load nothing
                raise AttributeError(f"module {self.__name__!r} has no attribute {name!r}")
            _load_whole(self)
            if not own.get("_is_loaded_on_first_read"):
                return getattr(self, name)
        if home is None:
            raise AttributeError(f"module {self.__name__!r} has no attribute {name!r}")
        return getattr(_import_piece(self, home), name)

    def __setattr__(self, name: str, value) -> None:
        if isinstance(value, types.ModuleType) and value.__name__ == f"{self.__name__}.{name}":
            super().__setattr__(name, value)  # the import system attaching a submodule
            return
        binders = self._get_binders(name)
        if not binders:
            super().__setattr__(name, value)
            return
        saved = vars(self)["_saved"]
        first = name not in saved
        if first and not all(name in vars(piece) for piece in binders):
            for piece in binders:  # writing back a deleted name (an undo of delattr): no override
                setattr(piece, name, value)
            vars(self)["_deleted"].pop(name, None)
            if vars(self)["_deleted_own"].pop(name, _MISSING) is not _MISSING:
                vars(self)[name] = value  # a module door's functions read it as their global
            return
        if first:
            saved[name] = tuple((piece, vars(piece)[name]) for piece in binders)
            # A door that is a module of its own (cli/main.py) reads its globals: keep its value.
            vars(self)["_own_saved"][name] = vars(self).get(name, _MISSING)
        for piece in binders:
            setattr(piece, name, value)
        vars(self)["_deleted"].pop(name, None)
        # The original written back (a pytest < 9.2 undo): no override left. Never on the first
        # write, or patching a name to the value it holds would forget the override at once.
        if not first and value is saved[name][0][1]:
            del saved[name]
            self._restore_own(name)
        else:
            vars(self)[name] = value

    def __delattr__(self, name: str) -> None:
        binders = self._get_binders(name)
        if not binders:
            super().__delattr__(name)
            return
        saved = vars(self)["_saved"].pop(name, None)
        if saved is None:  # no override: delete the name itself, as on the old module
            holding = [piece for piece in binders if name in vars(piece)]
            if not holding:
                raise AttributeError(f"module {self.__name__!r} has no attribute {name!r}")
            own_value = vars(self).pop(name, _MISSING)
            if own_value is not _MISSING:  # a later write (an undo) puts the door's own back too
                vars(self)["_deleted_own"][name] = own_value
            for piece in holding:
                delattr(piece, name)
            vars(self)["_deleted"][name] = tuple(holding)  # a later write (an undo) puts it back here
            return
        self._restore_own(name)
        originals = dict(saved)
        for piece in {**dict.fromkeys(binders), **originals}:  # and a piece that took the override since
            setattr(piece, name, originals.get(piece, saved[0][1]))

    def _restore_own(self, name: str) -> None:
        own = vars(self)
        before = own["_own_saved"].pop(name, _MISSING)
        if before is _MISSING:
            own.pop(name, None)
        else:
            own[name] = before

    def __dir__(self) -> list[str]:
        return sorted(set(vars(self)) | set(vars(self)["_homes"]))

    def _get_binders(self, name: str) -> tuple[types.ModuleType, ...] | None:
        """Every loaded piece holding the object `name` is bound to, found afresh at each write."""
        own = vars(self)
        homes, known = own.get("_homes", {}), own.get("_binders", {}).get(name)
        if name in homes:
            if own.get("_is_loaded_on_first_read"):  # a deferred door: whole, in door order
                _load_whole(self)
            for piece in own["_pieces"]:  # a lazy door loads its pieces at a first write
                _import_piece(self, piece)
            first = sys.modules[homes[name]]
        elif known:
            first = known[0]
        else:
            return None
        if name not in vars(first):  # deleted: an undo writes it back where it was
            return own["_deleted"].get(name) or (first,)
        binders = own["_binders"][name] = _find_binders(name, first, _loaded(own["_pieces"]))
        return binders


def serve_pieces(
    package: str, homes: Mapping[str, str], *, pieces: tuple[str, ...] = (), is_lazy: bool = False,
    is_loaded_on_first_read: bool = False, deferred: tuple[str, ...] = (),
) -> None:
    """Make `package` a FrontDoor over `homes` (name -> piece module holding it).

    Eager (the default) loads every piece now, as importing the old module ran all of it, and
    serves the names the pieces import too. Lazy loads nothing: a read imports the name's piece,
    so a light piece (a leaf a lower layer imports) never drags in the rest; `homes` must then
    list every name to serve. A name bound to the same object in several pieces (one imports it
    from another) is written to each, so a patch reaches every caller as it did when they shared
    one module's globals.

    `is_loaded_on_first_read` defers the eager load: importing a piece of the folder runs this
    door at no cost, and the first read through it of a name or a submodule loads every piece
    in `pieces` order, as an eager door would have (cli/wizard: every command loads pieces of
    that folder, which the old module never imported).

    `deferred` names pieces an eager door leaves for later: a read of a name they hold imports
    its piece, and the first write through the door loads them all first, so a patch still
    reaches every holder (cli/main.py's wizard and harness helpers, which only some commands
    call)."""
    door = sys.modules[package]
    own = vars(door)
    own["_homes"] = dict(homes)
    # The old module's pieces, and only them: a write never reaches a module that was always separate.
    own["_pieces"] = tuple(dict.fromkeys([*pieces, *homes.values()]))
    own["_binders"] = {}
    own["_saved"] = {}
    own["_deleted"] = {}
    own["_deleted_own"] = {}
    own["_own_saved"] = {}
    own["_is_loaded_on_first_read"] = is_loaded_on_first_read
    own["_loading"] = False
    own["_load_lock"] = threading.RLock()
    own["_deferred"] = frozenset(deferred)
    if not is_lazy and not is_loaded_on_first_read:
        _bind_pieces(door)
    door.__class__ = FrontDoor


def _import_piece(door: types.ModuleType, piece: str) -> types.ModuleType:
    """A piece the door reads, loaded by one thread at a time. Two first reads at once, through
    pieces that import each other, deadlocked the import system (`_DeadlockError`, cli/imports/folder)."""
    module = sys.modules.get(piece)
    if module is not None and not getattr(getattr(module, "__spec__", None), "_initializing", False):
        return module  # loaded: no lock
    lock = vars(door)["_load_lock"]
    is_held = lock.acquire(timeout=_LOAD_WAIT_S)
    try:
        return importlib.import_module(piece)
    finally:
        if is_held:
            lock.release()


def _load_whole(door: types.ModuleType) -> None:
    """A deferred door's first read: every piece, in load order, then the eager door's binders.

    One thread loads and the others wait: two loading at once handed each other half-run pieces
    (`cannot import name ... from partially initialized module`). The door counts as loaded only
    once bound; a read inside the load (a piece reading the door) answers from its piece."""
    own = vars(door)
    if not own["_load_lock"].acquire(timeout=_LOAD_WAIT_S):
        return
    try:
        if own["_is_loaded_on_first_read"] and not own["_loading"]:
            own["_loading"] = True
            try:
                _bind_pieces(door)
                own["_is_loaded_on_first_read"] = False
            finally:
                own["_loading"] = False
    finally:
        own["_load_lock"].release()


def _bind_pieces(door: types.ModuleType) -> None:
    own = vars(door)
    package, homes = door.__name__, own["_homes"]
    for piece in own["_pieces"]:
        if piece not in own["_deferred"]:
            importlib.import_module(piece)
    loaded = _loaded(own["_pieces"])
    # Submodule attributes belong to the import system; a write to one is never forwarded. A
    # module of the folder not imported yet is one too: a piece's same-named import never hides it.
    submodules = {n for n, v in vars(door).items() if isinstance(v, types.ModuleType)
                  and v.__name__.startswith(package + ".")}
    if hasattr(door, "__path__"):
        submodules |= {info.name for info in pkgutil.iter_modules(door.__path__)}
    binders = own["_binders"]
    # What the door defines itself (cli/main.py's root callback, main()): never a piece's name.
    door_own = {n: v for n, v in own.items() if not n.startswith("__")}
    # Each name's holders, in load order, found in one pass: a door over ~100 pieces
    # (cli/main.py) scanned every piece for each of its ~750 names, ~11 ms per command.
    holders: dict[str, list[types.ModuleType]] = {}
    for piece in loaded:
        for name in vars(piece):
            holders.setdefault(name, []).append(piece)
    def is_door_own(name: str, piece: types.ModuleType) -> bool:
        return name in door_own and door_own[name] is not vars(piece)[name]

    for name, home in homes.items():
        # A piece still loading (this load began inside another import) lacks its later names:
        # a read of one goes through __getattr__ to the piece, once it has it.
        if home in sys.modules and name in vars(sys.modules[home]) and not is_door_own(name, sys.modules[home]):
            # (a deferred piece not loaded yet is read through __getattr__)
            binders[name] = _find_binders(name, sys.modules[home], holders.get(name, ()))
    for piece in loaded:
        for name in vars(piece):
            if not name.startswith("__") and name not in binders and name not in submodules \
                    and not is_door_own(name, piece):
                binders[name] = _find_binders(name, piece, holders[name])
    for name in submodules:
        binders.pop(name, None)


def _find_binders(name: str, first: types.ModuleType, pieces: Sequence[types.ModuleType]) -> tuple[types.ModuleType, ...]:
    value = vars(first)[name]
    return (first, *(p for p in pieces if p is not first and vars(p).get(name, _MISSING) is value))


def _loaded(pieces: tuple[str, ...]) -> list[types.ModuleType]:
    return [sys.modules[m] for m in pieces if isinstance(sys.modules.get(m), types.ModuleType)]
