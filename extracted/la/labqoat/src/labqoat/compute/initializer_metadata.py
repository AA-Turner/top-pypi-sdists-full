"""Typed marker attached to a worker initializer's authored function."""

from typing import Protocol


class InitializerMetadata(Protocol):
    """Describe the inert lifecycle markers installed by the enter decorator."""

    __labqoat_enter__: bool
    __labqoat_snap__: bool
