"""ONE FIXED ORDER FOR EVERY PLATFORM-BUILT LIST THAT REACHES A PROVIDER (static seal P0.2, D16).

Arman, 2026-11-12: "by default, our platform uses some system for ordering that guarantees it will
always be the same. For example, if it was alphabetical ... that can never change." A provider caches a
prompt by its exact bytes, so a list whose order depends on how it was built (insertion order, a DB row
order, set iteration, a jsonb round trip) re-writes the cache the first time two paths disagree. Live
2026-11-12: tool declarations reloaded from the jsonb ledger came back with different key order on
turn 2 and the whole conversation was re-written.

The rules, applied at the producer AND enforced at the boundary every request passes:

* **A list of named things is sorted by its name** (code-point order, never locale): tool
  declarations, per-turn context slots. ``sorted_by_name``.
* **A JSON object's keys sit in ONE canonical order**: the structural keys in
  ``CANONICAL_KEY_ORDER``, then every other key in code-point order. ``canonical_json``.
* **Two things are NEVER reordered, because the model reads their order:**
  - the MEMBERS of a name map (``properties``, ``$defs``, ``definitions``, ``patternProperties``):
    a constrained decoder writes arguments / fields in ``properties`` order
    (``schema.rules.restore_generation_order`` measured an answer collapse from a storage order). The
    author's / registry's order is frozen at its source instead (the tool ledger keeps the sent JSON
    text, ``propertyOrdering`` records it through jsonb); this module only orders the KEYWORDS around it.
  - DATA values (``const``, ``enum``, ``default``, ``examples``, ``example``) and every array: arrays keep their
    order (jsonb keeps arrays), and a data object is the author's literal value.

Idempotent: ``canonical_json(canonical_json(x)) == canonical_json(x)``. The input is never mutated.
``canonical_bytes`` is the byte form the fingerprints and the order guards compare.
"""

from __future__ import annotations

import copy
import json
from collections.abc import Callable, Iterable
from typing import Any, TypeVar

T = TypeVar("T")

#: Structural keys first, in this order; every other key follows in code-point order. Covers both tool
#: declaration wrappers (Anthropic ``name/description/input_schema``, OpenAI ``type/function`` and
#: Responses ``type/name/description/parameters/strict``, Gemini ``name/description/parameters``) and
#: the JSON-Schema keywords inside them. Changing this tuple changes the bytes of every tools array:
#: a one-time prompt-cache reset, accepted for the first ship (D16).
CANONICAL_KEY_ORDER: tuple[str, ...] = (
    "type",
    "name",
    "title",
    "description",
    "function",
    "parameters",
    "input_schema",
    "strict",
    "const",
    "enum",
    "format",
    "default",
    "properties",
    "required",
    "items",
    "prefixItems",
    "additionalProperties",
    "anyOf",
    "oneOf",
    "allOf",
    "$ref",
    "$defs",
    "definitions",
)

#: Keys whose value is a map from an AUTHOR'S name to a schema: member order is kept, each member's
#: schema is canonicalized. Same set as ``schema.rules._SCHEMA_NAME_MAP_KEYS`` plus ``patternProperties``.
NAME_MAP_KEYS: frozenset[str] = frozenset({"properties", "$defs", "definitions", "patternProperties"})

#: Keys whose value is the author's literal data, kept byte for byte.
DATA_KEYS: frozenset[str] = frozenset({"const", "enum", "default", "examples", "example"})

_RANK = {key: i for i, key in enumerate(CANONICAL_KEY_ORDER)}


def canonical_key(key: str) -> tuple[int, str]:
    """Sort key for one object key: its structural rank, else after all of them by code point."""
    return (_RANK.get(key, len(_RANK)), key)


def _data_copy(member: Any) -> Any:
    """The author's literal value, copied without reordering. A JSON round trip (tuples become
    lists, exactly as the wire sees them); a value JSON cannot hold (a set, an object) is never
    turned into its ``str``: it is kept as it was, copied — unchanged, as before canonicalization."""
    if not isinstance(member, dict | list | tuple):
        return member
    try:
        return json.loads(json.dumps(member, allow_nan=True))
    except (TypeError, ValueError, RecursionError):
        try:
            return copy.deepcopy(member)
        except Exception:  # noqa: BLE001 — an uncopyable value is passed through untouched
            return member


def canonical_json(value: Any) -> Any:
    """A deep copy of ``value`` with every object's keys in the canonical order (see module doc)."""
    if isinstance(value, list | tuple):
        return [canonical_json(item) for item in value]
    if not isinstance(value, dict):
        return value
    out: dict[str, Any] = {}
    for key in sorted(value, key=lambda k: canonical_key(str(k))):
        member = value[key]
        if key in DATA_KEYS:
            out[key] = _data_copy(member)
        elif key in NAME_MAP_KEYS and isinstance(member, dict):
            out[key] = {name: canonical_json(sub) for name, sub in member.items()}
        else:
            out[key] = canonical_json(member)
    return out


def canonical_bytes(value: Any) -> bytes:
    """The canonical JSON bytes of ``value`` (what the fingerprints and order guards compare)."""
    return json.dumps(
        canonical_json(value), ensure_ascii=False, separators=(",", ":"), default=str
    ).encode("utf-8", "replace")


def sorted_by_name(items: Iterable[T], name_of: Callable[[T], str | None]) -> list[T]:
    """``items`` sorted by name in code-point order; ties (and nameless items, named ``""``) are
    broken by their canonical bytes so the result never depends on the input order."""
    return sorted(items, key=lambda item: (name_of(item) or "", canonical_bytes(item)))


def is_name_sorted(names: Iterable[str]) -> bool:
    """Whether ``names`` already sit in the platform's one order."""
    listed = list(names)
    return listed == sorted(listed)


__all__ = [
    "CANONICAL_KEY_ORDER",
    "DATA_KEYS",
    "NAME_MAP_KEYS",
    "canonical_bytes",
    "canonical_json",
    "canonical_key",
    "is_name_sorted",
    "sorted_by_name",
]
