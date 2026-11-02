"""Workflow input defaults read from the host's System Context — an injection seam.

A workflow input's default may be a pointer instead of a literal:
``{"$system_context": "preferred_frontier_large_model"}``. The value lives once, in the host's
System Context (an admin changes it there, an organization may set its own), and every workflow
that names it follows the change — no workflow carries a copy of a model id, a company name or a
house rule.

Resolution is host-owned: the host injects one async reader at startup with
``configure_system_context_reader(...)``; the scheduler resolves every pointer among a run's
landed input values before the first step (``resolve_system_context_values``). A run value a person
or caller supplied is a literal and wins as always — only a value that IS a pointer is resolved.

Standalone (no reader configured) a pointer cannot be honored, so the run fails loudly naming the
item: a default that silently became ``None`` or a dict would be worse.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

#: The pointer's one key: ``{"$system_context": "<item key>"}`` and nothing else beside it.
SYSTEM_CONTEXT_REF_KEY = "$system_context"

#: ``(item key, organization id) -> value``; None when the item is missing, inactive or not shareable.
SystemContextReader = Callable[[str, str | None], Awaitable[Any]]

_reader: SystemContextReader | None = None


def configure_system_context_reader(reader: SystemContextReader | None) -> None:
    """Register (or clear) the host's System Context reader. Called once at startup; None clears (tests)."""
    global _reader
    _reader = reader


def is_system_context_ref(value: Any) -> bool:
    """True when ``value`` is a ``{"$system_context": key}`` pointer."""
    return (
        isinstance(value, dict)
        and set(value.keys()) == {SYSTEM_CONTEXT_REF_KEY}
        and isinstance(value[SYSTEM_CONTEXT_REF_KEY], str)
        and bool(value[SYSTEM_CONTEXT_REF_KEY].strip())
    )


def system_context_key(value: Any) -> str | None:
    """The item key a pointer names; None for anything that is not a pointer."""
    return value[SYSTEM_CONTEXT_REF_KEY].strip() if is_system_context_ref(value) else None


async def resolve_system_context_values(
    values: dict[str, Any], *, organization_id: str | None
) -> dict[str, Any]:
    """A copy of ``values`` with every top-level pointer replaced by the item's current value.

    Raises ``UnresolvedInputError`` naming the input and the item when a pointer cannot be read.
    """
    from matrx_graph.errors import UnresolvedInputError

    if not any(is_system_context_ref(v) for v in values.values()):
        return values
    resolved = dict(values)
    for name, value in values.items():
        key = system_context_key(value)
        if key is None:
            continue
        if _reader is None:
            raise UnresolvedInputError(
                f"Input '{name}' defaults to System Context item '{key}', but this host reads no "
                "System Context. Supply a value for it when starting the run."
            )
        item_value = await _reader(key, organization_id)
        if item_value is None or item_value == "":
            raise UnresolvedInputError(
                f"Input '{name}' defaults to System Context item '{key}', which is missing, "
                "inactive, empty or not public. Fix the item, or supply a value when starting the run."
            )
        resolved[name] = item_value
    return resolved


__all__ = [
    "SYSTEM_CONTEXT_REF_KEY",
    "SystemContextReader",
    "configure_system_context_reader",
    "is_system_context_ref",
    "resolve_system_context_values",
    "system_context_key",
]
