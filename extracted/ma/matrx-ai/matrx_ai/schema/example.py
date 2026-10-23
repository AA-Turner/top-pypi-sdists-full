"""An answer example generated FROM a structured-output schema's wire form.

Why this exists (2026-10-22, the Brand Curator): an agent's instructions showed its
answer shape hand-written by the instructions writer, and that shape left ``__kind`` off
the nested ``entries[]`` / ``word_signals[]`` objects. Every provider translator runs
:func:`matrx_ai.schema.lint.make_portable` first, which lists EVERY property in
``required`` — so on the wire those nested ``__kind`` keys are required, and Groq's strict
check refused 4 answers in 6 (``'/entries/0' … missing properties: '__kind'``).

A shape a model is shown must therefore come from the schema the provider enforces, never
from a person's or a writer's reading of it. :func:`answer_example` is that shape: one
instance that validates against the wire schema, ``__kind`` present at every level that
declares it, each pinned value (``const`` / one-member ``enum``) spelled out. Never strip
``__kind`` from a schema to make a provider happy (content-ir FEATURE.md §4.2a); show it.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from typing import Any

KIND_KEY = "__kind"
_MAX_DEPTH = 12
_ARRAY_DEPTH = 6
_FORMAT_SAMPLES = {
    "date-time": "2026-01-01T00:00:00Z",
    "date": "2026-01-01",
    "time": "00:00:00",
    "uri": "https://example.com",
    "url": "https://example.com",
    "email": "name@example.com",
    "uuid": "00000000-0000-0000-0000-000000000000",
}


def wire_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """The schema every provider translator starts from (``make_portable``)."""
    from matrx_ai.schema.lint import make_portable

    return make_portable(schema)


def _resolve(node: Any, root: dict[str, Any]) -> Any:
    seen: set[str] = set()
    while isinstance(node, dict) and isinstance(node.get("$ref"), str):
        ref = node["$ref"]
        if ref in seen or not ref.startswith("#/"):
            return {}
        seen.add(ref)
        target: Any = root
        for part in ref[2:].split("/"):
            target = target.get(part) if isinstance(target, dict) else None
        node = target if isinstance(target, dict) else {}
    return node


def _types(node: dict[str, Any]) -> list[str]:
    t = node.get("type")
    if isinstance(t, list):
        return [str(x) for x in t]
    return [str(t)] if isinstance(t, str) else []


def _sample(node: Any, root: dict[str, Any], *, key: str | None, depth: int) -> Any:
    node = _resolve(node, root)
    if not isinstance(node, dict):
        return None
    if "const" in node:
        return node["const"]
    enum = node.get("enum")
    if isinstance(enum, list) and enum:
        non_null = [v for v in enum if v is not None]
        return non_null[0] if non_null else enum[0]
    if key == KIND_KEY:
        # A sub-structure's marker is declared, optional on the author's side and REQUIRED on the
        # wire: it is present, and empty says "no kind of its own" (KindSubModel's default).
        default = node.get("default")
        return default if isinstance(default, str) else ""
    if "default" in node and isinstance(node["default"], (str, int, float, bool)):
        # A scalar default is a real value; an empty list/object default would hide the nested shape.
        return node["default"]
    for comb in ("anyOf", "oneOf"):
        branches = node.get(comb)
        if isinstance(branches, list) and branches:
            resolved = [_resolve(b, root) for b in branches]
            real = [b for b in resolved if isinstance(b, dict) and _types(b) != ["null"]]
            return _sample(real[0] if real else resolved[0], root, key=key, depth=depth)
    all_of = node.get("allOf")
    if isinstance(all_of, list) and all_of:
        return _sample(all_of[0], root, key=key, depth=depth)
    types = [t for t in _types(node) if t != "null"] or _types(node)
    t = types[0] if types else ("object" if "properties" in node else "")
    if depth > _MAX_DEPTH:
        return None if "null" in _types(node) else ({} if t == "object" else [] if t == "array" else None)
    if t == "object" or "properties" in node:
        props = node.get("properties") if isinstance(node.get("properties"), dict) else {}
        return {name: _sample(sub, root, key=name, depth=depth + 1) for name, sub in props.items()}
    if t == "array":
        if node.get("maxItems") == 0 or (depth >= _ARRAY_DEPTH and not node.get("minItems")):
            return []  # a recursive shape (a tree) stops at an empty list, which every such array admits
        count = max(int(node.get("minItems") or 1), 1)
        prefix = node.get("prefixItems")
        if isinstance(prefix, list) and prefix:
            return [_sample(i, root, key=None, depth=depth + 1) for i in prefix]
        items = node.get("items")
        if isinstance(items, list):
            return [_sample(i, root, key=None, depth=depth + 1) for i in items]
        return [_sample(items or {}, root, key=None, depth=depth + 1) for _ in range(count)]
    if t == "string":
        fmt = node.get("format")
        if isinstance(fmt, str) and fmt in _FORMAT_SAMPLES:
            return _FORMAT_SAMPLES[fmt]
        text = "..."
        min_len = node.get("minLength")
        if isinstance(min_len, int) and min_len > len(text):
            text = "." * min_len
        max_len = node.get("maxLength")
        if isinstance(max_len, int) and max_len < len(text):
            text = text[:max_len]
        pattern = node.get("pattern")
        if isinstance(pattern, str):
            for candidate in (text, *_FORMAT_SAMPLES.values(), "a", "A", "0", "a-a", "#000000", "+15555550100"):
                try:
                    if re.search(pattern, candidate):
                        return candidate
                except re.error:
                    break
        return text
    if t in ("integer", "number"):
        low = node.get("minimum")
        if low is None and isinstance(node.get("exclusiveMinimum"), (int, float)):
            low = node["exclusiveMinimum"] + 1
        value = low if isinstance(low, (int, float)) else 0
        return int(value) if t == "integer" else value
    if t == "boolean":
        return False
    if t == "null":
        return None
    return None


def answer_example(schema: dict[str, Any]) -> Any:
    """One instance of ``schema``'s WIRE form (:func:`wire_schema`): every key the provider
    requires, ``__kind`` at every level that declares it, pinned values spelled out."""
    wire = wire_schema(schema)
    return _sample(wire, wire, key=None, depth=0)


def object_shapes(schema: dict[str, Any]) -> tuple[list[frozenset[str]], list[frozenset[str]]]:
    """The property sets of every object in the wire schema, ``__kind`` excluded: (objects that declare
    ``__kind`` — each requires it on the wire —, objects that do not)."""
    wire = wire_schema(schema)
    marked: list[frozenset[str]] = []
    plain: list[frozenset[str]] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            props = node.get("properties")
            if isinstance(props, dict):
                keys = frozenset(k for k in props if k != KIND_KEY)
                bucket = marked if KIND_KEY in props else plain
                if keys and keys not in bucket:
                    bucket.append(keys)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(wire)
    return marked, plain


def kind_marked_shapes(schema: dict[str, Any]) -> list[frozenset[str]]:
    """The property sets of every wire-schema object that declares (so requires) ``__kind``."""
    return object_shapes(schema)[0]


_KEY = re.compile(r"""["'`]?([A-Za-z_][A-Za-z0-9_]*)["'`]?\s*:""")


def _brace_spans(text: str) -> Iterator[str]:
    """Every balanced ``{…}`` span in ``text`` (nested spans included)."""
    stack: list[int] = []
    for i, ch in enumerate(text):
        if ch == "{":
            stack.append(i)
        elif ch == "}" and stack:
            start = stack.pop()
            yield text[start + 1 : i]


def _top_level_keys(body: str) -> set[str]:
    depth = 0
    flat: list[str] = []
    for ch in body:
        if ch in "{[":
            depth += 1
            flat.append(" ")
        elif ch in "}]":
            depth -= 1
            flat.append(" ")
        else:
            flat.append(ch if depth == 0 else " ")
    return set(_KEY.findall("".join(flat)))


def shapes_missing_kind(text: str, schema: dict[str, Any]) -> list[list[str]]:
    """Answer shapes written in ``text`` that show an object of ``schema`` WITHOUT ``__kind``.

    A ``{…}`` span is a shape of a marked object when it has at least two keys and every key is that
    object's property — and it fits no object that declares no marker. Returns each such span's keys,
    sorted; empty when every written shape carries its marker."""
    marked, plain = object_shapes(schema)
    return spans_missing_kind(text, marked, plain)


def spans_missing_kind(
    text: str, marked: list[frozenset[str]], plain: list[frozenset[str]] = ()  # type: ignore[assignment]
) -> list[list[str]]:
    """:func:`shapes_missing_kind` over precomputed :func:`object_shapes`."""
    found: list[list[str]] = []
    for body in _brace_spans(text):
        keys = _top_level_keys(body)
        if KIND_KEY in keys or len(keys) < 2:
            continue
        if any(keys <= props for props in marked) and not any(keys <= props for props in plain):
            found.append(sorted(keys))
    return found


__all__ = [
    "answer_example", "kind_marked_shapes", "object_shapes", "shapes_missing_kind", "spans_missing_kind", "wire_schema",
]
