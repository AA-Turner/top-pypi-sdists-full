"""Selection and type identity for one authored CLI entrypoint."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import ModuleType
from typing import cast

import click

from labqoat.compute.function import Function
from labqoat.compute.local_entrypoint import LocalEntrypoint


@dataclass(frozen=True)
class AuthoredTarget:
    """Select decorated functions without treating ordinary Python helpers as remote work."""

    name: str
    declaration: Function[..., object] | LocalEntrypoint[..., object]

    @property
    def function(self) -> Callable[..., object]:
        """Expose the original signature with its injected first parameter."""
        return self.declaration.local

    @classmethod
    def select(cls, module: ModuleType, name: str) -> "AuthoredTarget":
        """Prefer a sole local entrypoint, then explicit main, then a sole remote function."""
        candidates = {
            key: value for key, value in vars(module).items() if isinstance(value, (Function, LocalEntrypoint))
        }
        if name:
            return cls._named(candidates, name)
        local = {key: value for key, value in candidates.items() if isinstance(value, LocalEntrypoint)}
        selected = local or candidates
        if "main" in selected:
            return cls._named(selected, "main")
        if len(selected) == 1:
            return cls._named(selected, next(iter(selected)))
        choices = ", ".join(sorted(candidates)) or "none"
        raise click.UsageError(f"Select an entrypoint with FILE.py::NAME. Available targets: {choices}")

    @classmethod
    def _named(cls, candidates: Mapping[str, object], name: str) -> "AuthoredTarget":
        """Reject absent or undecorated attributes with an actionable usage error."""
        value = candidates.get(name)
        if not isinstance(value, (Function, LocalEntrypoint)):
            raise click.UsageError(f"{name!r} is not a decorated function or local entrypoint.")
        return cls(name, cast(Function[..., object] | LocalEntrypoint[..., object], value))
