"""Read the constants a pi-package TypeScript file copies from Python.

The pi extension cannot import the Python package, so it carries copies of
strings, word lists and patterns, and a parity test compares each copy with
its original. These helpers read the copy out of the `.ts` SOURCE (no node
needed), for the shapes the package writes them in:

    export const NAME = "a" + OTHER + "b";              -> ts_string
    export const NAME = String.raw`...`;                -> ts_raw
    export const NAME: ReadonlySet<string> = new Set([...]);  -> ts_set
    export const NAME = { Key: "value", ... } as const;  -> ts_object

`export` is optional: a module-private copy is pinned the same way.

A shape these do not recognise fails the test loudly (`assert match`), never
reads as an empty value.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

_LITERAL = r'"((?:[^"\\]|\\.)*)"'


def _decode(literal: str) -> str:
    """A TS double-quoted literal's body, unescaped (its escapes are JSON's)."""
    return json.loads(f'"{literal}"')


def _declaration(path: Path, name: str) -> str:
    source = path.read_text(encoding="utf-8")
    match = re.search(rf"^(?:export )?const {name}\b[^=]*=\s*(.*?);\n", source, re.S | re.M)
    assert match, f"{path.name}: no `const {name}` of a shape ts_source reads"
    return match.group(1)


def ts_string(path: Path, name: str) -> str:
    """`"a" + OTHER + "b"`, a bare identifier being another exported string of the same file."""
    parts = re.findall(rf"{_LITERAL}|([A-Za-z_]\w*)", _declaration(path, name))
    assert parts, f"{path.name}: {name} has no string literal"
    return "".join(_decode(literal) if not identifier else ts_string(path, identifier) for literal, identifier in parts)


def ts_raw(path: Path, name: str) -> str:
    """`String.raw` template content, verbatim (a regex pattern's source)."""
    match = re.fullmatch(r"String\.raw`([^`]*)`", _declaration(path, name).strip())
    assert match, f"{path.name}: {name} is not a String.raw template"
    return match.group(1)


def ts_set(path: Path, name: str) -> set[str]:
    """`new Set([...])` of string literals."""
    match = re.fullmatch(r"new Set\(\[(.*)\]\)", _declaration(path, name).strip(), re.S)
    assert match, f"{path.name}: {name} is not a `new Set([...])` of literals"
    return {_decode(literal) for literal in re.findall(_LITERAL, match.group(1))}


def ts_object(path: Path, name: str) -> dict[str, str]:
    """`{ Key: "value", ... } as const`, string values only."""
    match = re.fullmatch(r"\{(.*)\}(?:\s+as const)?", _declaration(path, name).strip(), re.S)
    assert match, f"{path.name}: {name} is not an object literal"
    pairs = re.findall(rf"(\w+):\s*{_LITERAL}", match.group(1))
    assert pairs, f"{path.name}: {name} has no `Key: \"value\"` entries"
    return {key: _decode(value) for key, value in pairs}
