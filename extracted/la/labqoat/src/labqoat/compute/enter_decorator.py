"""Explicit context-first initialization of worker-owned class state."""

from collections.abc import Callable
from typing import ParamSpec, TypeVar, cast

from labqoat.compute.initializer_metadata import InitializerMetadata

P = ParamSpec("P")
R = TypeVar("R")


class EnterDecorator:
    """Mark the class initializer without invoking it during host authoring or publication.

    A class has at most one initializer of each kind. ``snap=True`` marks the one whose result a memory snapshot
    keeps (``Workers(memory_snapshot=True)``): it runs once per snapshot, before it is taken, so it is where models
    load and engines compile. The other runs on every worker, after a restore too, and without snapshots right after
    the first. Do not keep the context or open connections from a ``snap=True`` initializer: a restored worker has
    its own.
    """

    def __init__(self, *, snap: bool = False) -> None:
        """Choose which initializer this marks."""
        if type(snap) is not bool:
            raise TypeError("snap must be a boolean")
        self.snap = snap

    def __call__(self, function: Callable[P, R]) -> Callable[P, R]:
        """Preserve the Python method signature and attach an inert lifecycle marker."""
        marked = cast(InitializerMetadata, function)
        marked.__labqoat_enter__ = True
        marked.__labqoat_snap__ = self.snap
        return function
