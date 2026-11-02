"""Signature-preserving host entrypoint registration."""

from collections.abc import Callable
from typing import TYPE_CHECKING, Concatenate, ParamSpec, TypeVar

from labqoat.compute.local_entrypoint import LocalEntrypoint

if TYPE_CHECKING:
    from labqoat.client import Client

P = ParamSpec("P")
R = TypeVar("R")


class LocalEntrypointDecorator:
    """Mark host code while retaining its explicit Client and authored parameters."""

    def __init__(self, app_name: str = "") -> None:
        """Remember which app the launcher belongs to, so what it launches can be named after it."""
        self.app_name = app_name

    def __call__(self, function: Callable[Concatenate["Client", P], R]) -> LocalEntrypoint[P, R]:
        """Create a local launcher with no publication or remote side effects."""
        return LocalEntrypoint(function, self.app_name)
