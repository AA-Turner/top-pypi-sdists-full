"""A split module's package served like the old module: live reads, and a write lands on every piece
bound to the name. Twin of app/core/front_door, plus a lazy door that loads a piece on first use."""

from __future__ import annotations

import importlib
import sys
import types
from collections.abc import Mapping

_MISSING = object()


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
        if home is None:
            raise AttributeError(f"module {self.__name__!r} has no attribute {name!r}")
        return getattr(importlib.import_module(home), name)

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
            return
        if first:
            saved[name] = tuple((piece, vars(piece)[name]) for piece in binders)
        for piece in binders:
            setattr(piece, name, value)
        vars(self)["_deleted"].pop(name, None)
        # The original written back (a pytest < 9.2 undo): no override left. Never on the first
        # write, or patching a name to the value it holds would forget the override at once.
        if not first and value is saved[name][0][1]:
            del saved[name]
            vars(self).pop(name, None)
        else:
            vars(self)[name] = value

    def __delattr__(self, name: str) -> None:
        binders = self._get_binders(name)
        if not binders:
            super().__delattr__(name)
            return
        saved = vars(self)["_saved"].pop(name, None)
        vars(self).pop(name, None)
        if saved is None:  # no override: delete the name itself, as on the old module
            holding = [piece for piece in binders if name in vars(piece)]
            if not holding:
                raise AttributeError(f"module {self.__name__!r} has no attribute {name!r}")
            for piece in holding:
                delattr(piece, name)
            vars(self)["_deleted"][name] = tuple(holding)  # a later write (an undo) puts it back here
            return
        originals = dict(saved)
        for piece in {**dict.fromkeys(binders), **originals}:  # and a piece that took the override since
            setattr(piece, name, originals.get(piece, saved[0][1]))

    def __dir__(self) -> list[str]:
        return sorted(set(vars(self)) | set(vars(self)["_homes"]))

    def _get_binders(self, name: str) -> tuple[types.ModuleType, ...] | None:
        """Every loaded piece holding the object `name` is bound to, found afresh at each write."""
        own = vars(self)
        homes, known = own.get("_homes", {}), own.get("_binders", {}).get(name)
        if name in homes:
            for piece in own["_pieces"]:  # a lazy door loads its pieces at a first write
                importlib.import_module(piece)
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
    package: str, homes: Mapping[str, str], *, pieces: tuple[str, ...] = (), is_lazy: bool = False
) -> None:
    """Make `package` a FrontDoor over `homes` (name -> piece module holding it).

    Eager (the default) loads every piece now, as importing the old module ran all of it, and
    serves the names the pieces import too. Lazy loads nothing: a read imports the name's piece,
    so a light piece (a leaf a lower layer imports) never drags in the rest; `homes` must then
    list every name to serve. A name bound to the same object in several pieces (one imports it
    from another) is written to each, so a patch reaches every caller as it did when they shared
    one module's globals."""
    door = sys.modules[package]
    own = vars(door)
    own["_homes"] = dict(homes)
    # The old module's pieces, and only them: a write never reaches a module that was always separate.
    own["_pieces"] = tuple(dict.fromkeys([*pieces, *homes.values()]))
    own["_binders"] = {}
    own["_saved"] = {}
    own["_deleted"] = {}
    if not is_lazy:
        for piece in own["_pieces"]:
            importlib.import_module(piece)
        loaded = _loaded(own["_pieces"])
        # Submodule attributes belong to the import system; a write to one is never forwarded.
        submodules = {n for n, v in vars(door).items() if isinstance(v, types.ModuleType)
                      and v.__name__.startswith(package + ".")}
        binders = own["_binders"]
        for name, home in homes.items():
            binders[name] = _find_binders(name, sys.modules[home], loaded)
        for piece in loaded:
            for name in vars(piece):
                if not name.startswith("__") and name not in binders and name not in submodules:
                    binders[name] = _find_binders(name, piece, loaded)
        for name in submodules:
            binders.pop(name, None)
    door.__class__ = FrontDoor


def _find_binders(name: str, first: types.ModuleType, pieces: list[types.ModuleType]) -> tuple[types.ModuleType, ...]:
    value = vars(first)[name]
    return (first, *(p for p in pieces if p is not first and vars(p).get(name, _MISSING) is value))


def _loaded(pieces: tuple[str, ...]) -> list[types.ModuleType]:
    return [sys.modules[m] for m in pieces if isinstance(sys.modules.get(m), types.ModuleType)]
