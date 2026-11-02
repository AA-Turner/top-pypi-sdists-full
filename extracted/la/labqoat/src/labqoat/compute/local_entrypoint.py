"""Explicitly host-side launcher with an injected, caller-owned Client."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Concatenate, Generic, ParamSpec, TypeVar

if TYPE_CHECKING:
    from labqoat.client import Client

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class LocalEntrypoint(Generic[P, R]):
    """Retain launcher code separately from managed functions and remote credentials."""

    local: Callable[Concatenate["Client", P], R]
    app_name: str = ""

    def __call__(self, client: "Client", *args: P.args, **kwargs: P.kwargs) -> R:
        """Invoke on the current host with explicit client ownership."""
        return self.local(client, *args, **kwargs)
