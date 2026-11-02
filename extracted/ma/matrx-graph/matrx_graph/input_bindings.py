"""A run input filled from table data at run start — the host injection seam.

A Collect Inputs field (``io.user_input``) may carry a ``binding``: the SAME merge-field
declaration an agent variable carries when its author picks "From my data"
(``{"kind": "merge_field", "source": "record", "semantic_type": …, "table_id": …}``). At run
start the field's value is read from that table instead of being asked for.

This package never reads a table. The host owns the one merge-field resolver (aidream:
``conversation_context.merge_field_bindings.resolve_merge_field_bindings``, the function every
agent run and the agent builder's preview call), and injects it here once at startup.
Unconfigured, a bound field refuses BY NAME — never an empty success.

MISSING IS NEVER BLANK. A binding that resolves to nothing comes back ``present=False`` with
the resolver's named absence as its text and one plain sentence; the node delivers that text
as the value AND says the sentence in the run (a progress line), so a downstream step never
receives a silent empty. ``missing: "block"`` raises :class:`InputBindingBlocked` and the run
parks on the input step with the sentence.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from typing import Any

__all__ = [
    "BoundInput",
    "InputBindingBlocked",
    "InputBindingResolver",
    "configure_input_binding_resolver",
    "get_input_binding_resolver",
]


@dataclass(frozen=True, slots=True)
class BoundInput:
    """One bound field after resolution."""

    #: What the field receives — the rendered data, or the named absence.
    text: str
    present: bool
    #: When absent: one plain sentence saying why, for the run's own record.
    absent_sentence: str | None = None
    #: The client-sent value may not replace this one (the binding's override policy).
    locks_client: bool = True


class InputBindingBlocked(Exception):
    """A ``missing: "block"`` binding had no value — the run must not go on."""

    def __init__(self, user_message: str, *, key: str) -> None:
        super().__init__(user_message)
        self.user_message = user_message
        self.key = key


#: ``(bindings by field key, user_id, organization_id) -> BoundInput by field key``.
InputBindingResolver = Callable[
    [Mapping[str, dict[str, Any]], str | None, str | None],
    Awaitable[dict[str, BoundInput]],
]

_resolver: InputBindingResolver | None = None


def configure_input_binding_resolver(resolver: InputBindingResolver | None) -> None:
    """Install (or clear, with ``None``) the host's merge-field resolver."""
    global _resolver
    _resolver = resolver


def get_input_binding_resolver() -> InputBindingResolver | None:
    return _resolver
