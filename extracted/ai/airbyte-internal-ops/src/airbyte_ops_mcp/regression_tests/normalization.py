# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""How a stream is identified, and how a protocol object becomes plain data.

Both the execution model and the comparators need these: `models.py` keys the
state it extracts by stream identity, and `regression/comparators.py` keys the
discovered catalog the same way and turns both into the labels a reviewer reads.
They live here rather than in either of those so neither has to import the
other's internals -- a leaf module both sides depend on, instead of the
execution model reaching into the comparison layer.

Keeping them in one place is also what makes the surfaces agree: a stream named
one thing in the catalog table and another in the state table would read as two
different streams.
"""

from __future__ import annotations

from typing import Any


def to_stream_id(namespace: Any, name: Any) -> tuple[str | None, str]:
    """What identifies a stream: its namespace and its name, as a pair.

    A pair rather than the `namespace.name` string it displays as, so a stream
    literally called `public.users` is not the same key as `users` in the
    `public` namespace.

    A falsy namespace normalises to `None`, which is what makes `("", name)`
    unreachable here -- the state comparison uses that for the two states which
    belong to no stream, so no connector-declared stream can collide with them.
    """
    return (str(namespace) if namespace else None, str(name))


def stream_label(namespace: Any, name: Any) -> str:
    """How a stream is named in everything a reviewer reads.

    Shared by the catalog and state comparisons, so the discovered catalog and
    the emitted state agree on what a stream is called.
    """
    return f"{namespace}.{name}" if namespace else str(name)


def unique_label(label: str, taken: dict[str, Any]) -> str:
    """`label`, or a qualified form of it when another stream got there first.

    Two distinct streams can render the same label -- `public.users` the name
    beside `users` in the `public` namespace -- and a shared label must not
    collapse them into one result.
    """
    if label not in taken:
        return label

    qualified = f"{label} (2)"
    suffix = 2
    while qualified in taken:
        suffix += 1
        qualified = f"{label} ({suffix})"

    return qualified


def to_plain_dict(value: Any, *, exclude_none: bool = True) -> dict[str, Any] | None:
    """Normalise a protocol object to plain JSON-compatible data.

    Accepts the pydantic models an `ExecutionResult` yields as well as the plain
    dicts saved artifacts and tests carry, so a comparator never depends on
    which of the two it was handed.

    `exclude_none` drops keys whose value is `None`, which is what the spec and
    catalog comparisons want: a protocol optional nobody set is noise, not
    something the connector declared. Pass `False` for a state blob, where a
    `null` is the connector's own data -- a cursor one version emits as `null`
    and the other omits is a change to what the next sync resumes from, and
    dropping the key would report the two states as identical.
    """
    if value is None:
        return None

    if isinstance(value, dict):
        return value

    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        return model_dump(mode="json", exclude_none=exclude_none)

    raise TypeError(f"Cannot compare a {type(value).__name__} as JSON data")
