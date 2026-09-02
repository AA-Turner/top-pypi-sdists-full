from __future__ import annotations

from collections.abc import Callable

from matrx_ai.tools.vfs.commands.base import Command

_COMMANDS: dict[str, Command] = {}


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
    _COMMANDS.clear()
