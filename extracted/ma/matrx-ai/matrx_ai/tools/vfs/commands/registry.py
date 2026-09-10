from __future__ import annotations

import contextlib
from collections.abc import Callable, Iterator

from matrx_ai.tools.vfs.commands.base import Command

_COMMANDS: dict[str, Command] = {}

# ``register`` fires at command-module IMPORT time, so once those modules are in
# ``sys.modules`` a second ``import_module`` is a no-op. That makes ``clear()`` a
# ONE-WAY DOOR for the rest of the process unless someone reloads the modules —
# and the registry is a process global, so one caller's cleanup disarms every
# virtual command for everybody. Measured 2026-09-09: a single test fixture's
# teardown ``clear()`` took 557 later tests with it the moment collection order
# put it first (green in one order, red in another, with no code change).
# ``load_all()`` reads this flag and RELOADS instead of re-importing.
_CLEARED = False


def register(*names: str) -> Callable[[Command], Command]:
    def decorator(fn: Command) -> Command:
        for name in names:
            _COMMANDS[name] = fn
        return fn

    return decorator


def get(name: str) -> Command | None:
    return _COMMANDS.get(name)


def all_names() -> list[str]:
    return sorted(_COMMANDS.keys())


def is_registered(name: str) -> bool:
    return name in _COMMANDS


def clear() -> None:
    """Empty the registry. ``load_all()`` can always refill it afterwards."""
    global _CLEARED

    _COMMANDS.clear()
    _CLEARED = True


def take_cleared() -> bool:
    """True once after a ``clear()`` — consumed by ``load_all()``."""
    global _CLEARED

    was_cleared, _CLEARED = _CLEARED, False
    return was_cleared


@contextlib.contextmanager
def isolated() -> Iterator[None]:
    """Run a block against an EMPTY registry, then put the real one back.

    The registry is a process global, so a caller that empties it and walks away
    disarms every virtual command for every consumer that runs afterwards — with
    no error anywhere, just commands that quietly stop existing. Use this instead
    of a bare ``clear()`` whenever the emptiness is temporary (a test asserting
    on registration itself, a host swapping in its own command set).
    """
    saved = dict(_COMMANDS)
    _COMMANDS.clear()
    try:
        yield
    finally:
        _COMMANDS.clear()
        _COMMANDS.update(saved)
