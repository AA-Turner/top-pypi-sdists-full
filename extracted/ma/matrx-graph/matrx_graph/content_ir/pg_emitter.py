"""What a Postgres function EMITS, as a model ``contract_drift`` can hand to a kind.

WHY THIS EXISTS. ``contract_drift`` (``matrx_graph.content_ir.sample``) asks the
runtime's question — does the consumer's validator accept what the emitter
emits? — but it needs the emitter as a model. A node has one (its
``output_schema``). A tool that passes a database function's JSON straight
through has none in Python: the emitter is the function, and the shape lives
in ``pg_proc``. That is exactly where ``topical_map`` drifted (2026-09-22,
``RESULT_KIND_MISMATCH action='create_map'``): ``seo.upsert_map_topics`` gained
five keys, ``topical_map_result`` never followed, and no guard could see it
because the only record of the shape was the function body.

THE RULE: THE SHAPE IS READ FROM ``pg_proc``, NEVER GUESSED.

* ``RETURNS TABLE (...)`` / ``OUT`` arguments → one field per column, required.
* ``RETURNS text`` / a scalar → the caller wraps it under a key; the function
  contributes no keys of its own.
* ``RETURNS json[b]`` → every ``RETURN jsonb_build_object(...)`` in the body is
  read for its literal keys. A key present in EVERY such ``RETURN`` is
  required; one present in only some is optional. Values are UNTYPED (``Any``,
  which ``contract_drift`` synthesizes as ``None``) — ``pg_proc`` states which keys
  a function returns, not their JSON types, and this module does not pretend to.
  So the check is exact about keys (``extra_forbidden``, a missing required key)
  and silent about value types, which the runtime check in the tool still owns.

A ``RETURN`` may also be a ``||`` of literal objects and variables each assigned
exactly once from another function (``v := seo.upsert_map_topics(...)``) — that
function's keys are read from ITS ``pg_proc`` row through the caller's resolver.
Anything else — ``RETURN v_result`` built up in a loop, a non-literal key, a
variable of unknown origin — raises
``UngradeableEmitter`` naming why. It is never read as "no keys": a checker that
quietly stops checking is the failure mode ``sample.py`` was written to end.

Pure text processing, no database: the host reads ``pg_proc`` and passes the
columns in, so this stays importable on a bare interpreter.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ConfigDict, create_model

__all__ = [
    "PgFunction",
    "UngradeableEmitter",
    "json_return_keys",
    "emitter_model",
]


class UngradeableEmitter(ValueError):
    """``pg_proc`` does not state this function's result shape precisely enough."""


@dataclass(frozen=True)
class PgFunction:
    """The ``pg_proc`` facts about one function's result."""

    qualified_name: str
    #: ``pg_get_function_result(oid)`` — e.g. ``jsonb``, ``text``, ``TABLE(id uuid, …)``.
    result: str
    #: ``prosrc`` — the body.
    body: str
    #: OUT / TABLE column names in order (``proargnames`` where the mode is o/b/t).
    out_columns: tuple[str, ...] = ()




def _strip_comments(body: str) -> str:
    """Drop comments without touching string literals (``--`` inside quotes stays)."""
    out: list[str] = []
    i, n = 0, len(body)
    while i < n:
        ch = body[i]
        if ch == "'":
            j = i + 1
            while j < n:
                if body[j] == "'" and j + 1 < n and body[j + 1] == "'":
                    j += 2
                    continue
                if body[j] == "'":
                    break
                j += 1
            out.append(body[i : j + 1])
            i = j + 1
            continue
        if body.startswith("--", i):
            j = body.find("\n", i)
            i = n if j == -1 else j
            continue
        if body.startswith("/*", i):
            j = body.find("*/", i + 2)
            i = n if j == -1 else j + 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _split_args(body: str, start: int) -> tuple[list[str], int]:
    """Top-level comma-split of the call whose ``(`` is at ``start - 1``.

    Returns the argument texts and the index just past the closing ``)``.
    Respects nested parens/brackets and single-quoted literals (``''`` escapes).
    """
    args: list[str] = []
    depth = 0
    i = start
    current = start
    n = len(body)
    while i < n:
        ch = body[i]
        if ch == "'":
            i += 1
            while i < n:
                if body[i] == "'" and i + 1 < n and body[i + 1] == "'":
                    i += 2
                    continue
                if body[i] == "'":
                    break
                i += 1
        elif ch in "([":
            depth += 1
        elif ch in ")]":
            if depth == 0:
                args.append(body[current:i].strip())
                return args, i + 1
            depth -= 1
        elif ch == "," and depth == 0:
            args.append(body[current:i].strip())
            current = i + 1
        i += 1
    raise UngradeableEmitter("unbalanced parentheses in a RETURN jsonb_build_object(...)")


_LITERAL_KEY = re.compile(r"^'((?:[^']|'')*)'(?:::text)?$")
_IDENT = r"[A-Za-z_][A-Za-z0-9_]*"
_RETURN_STMT = re.compile(r"\bRETURN\b(?!\s+(?:QUERY|NEXT)\b)", re.IGNORECASE)
_BUILD = re.compile(r"(jsonb?_build_object)\s*\(", re.IGNORECASE)


def _statement(body: str, start: int) -> tuple[str, int]:
    """The text from ``start`` to the next top-level ``;`` (quotes/parens respected)."""
    depth, i, n = 0, start, len(body)
    while i < n:
        ch = body[i]
        if ch == "'":
            i += 1
            while i < n and not (body[i] == "'" and not body.startswith("''", i)):
                i += 2 if body.startswith("''", i) else 1
        elif ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        elif ch == ";" and depth == 0:
            return body[start:i], i + 1
        i += 1
    raise UngradeableEmitter("a RETURN statement with no terminating ';'")


def _split_concat(expr: str) -> list[str]:
    """Top-level ``||`` operands of ``expr``."""
    parts: list[str] = []
    depth, i, current, n = 0, 0, 0, len(expr)
    while i < n:
        ch = expr[i]
        if ch == "'":
            i += 1
            while i < n and not (expr[i] == "'" and not expr.startswith("''", i)):
                i += 2 if expr.startswith("''", i) else 1
        elif ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        elif depth == 0 and expr.startswith("||", i):
            parts.append(expr[current:i].strip())
            current = i + 2
            i += 1
        i += 1
    parts.append(expr[current:].strip())
    return parts


Resolver = Callable[[str], "PgFunction | None"]


def _object_keys(fn: PgFunction, operand: str, body: str, resolve: Resolver | None, seen: frozenset[str]) -> set[str]:
    """Keys of ONE ``||`` operand: a literal object, or a variable assigned once
    from another function's result (read from that function's own ``pg_proc``)."""
    built = _BUILD.match(operand)
    if built:
        args, end = _split_args(operand, built.end())
        if operand[end:].strip():
            raise UngradeableEmitter(f"{fn.qualified_name}: trailing text after {built.group(1)}(...)")
        if len(args) % 2:
            raise UngradeableEmitter(f"{fn.qualified_name}: odd argument count in {built.group(1)}")
        keys: set[str] = set()
        for key_text in args[0::2]:
            literal = _LITERAL_KEY.match(key_text)
            if literal is None:
                raise UngradeableEmitter(
                    f"{fn.qualified_name}: a non-literal key {key_text[:40]!r} in the returned object"
                )
            keys.add(literal.group(1).replace("''", "'"))
        return keys
    if re.fullmatch(_IDENT, operand) and resolve is not None:
        assigned = re.findall(
            rf"\b{operand}\s*:=\s*({_IDENT}\.{_IDENT})\s*\(", body, flags=re.IGNORECASE
        )
        others = re.findall(rf"\b{operand}\s*:=", body, flags=re.IGNORECASE)
        if len(assigned) == 1 and len(others) == 1:
            callee = resolve(assigned[0])
            if callee is None:
                raise UngradeableEmitter(
                    f"{fn.qualified_name}: {operand} comes from {assigned[0]}, which pg_proc does not hold"
                )
            if callee.qualified_name in seen:
                raise UngradeableEmitter(f"{fn.qualified_name}: recursive composition via {operand}")
            inner = json_return_keys(callee, resolve=resolve, _seen=seen | {fn.qualified_name})
            return {k for k, required in inner.items() if required} | {
                f"?{k}" for k, required in inner.items() if not required
            }
    raise UngradeableEmitter(
        f"{fn.qualified_name}: RETURN operand {operand[:60]!r} is not a literal object or a "
        "variable assigned once from another function — its keys are not stated in pg_proc"
    )


def json_return_keys(
    fn: PgFunction, *, resolve: Resolver | None = None, _seen: frozenset[str] = frozenset()
) -> dict[str, bool]:
    """``{key: required}`` over every ``RETURN`` in the body.

    Each ``RETURN`` must be a literal ``jsonb_build_object(...)``, or a ``||``
    of those and variables each assigned exactly once from another function
    (``v := seo.upsert_map_topics(...)``) whose own keys are read from ITS
    ``pg_proc`` row via ``resolve``. A key in every ``RETURN`` is required.
    """
    body = _strip_comments(fn.body)
    key_sets: list[tuple[set[str], set[str]]] = []
    for m in _RETURN_STMT.finditer(body):
        expr, _ = _statement(body, m.end())
        expr = expr.strip()
        if not expr or expr.upper() == "NULL":
            continue  # a NULL result — contributes no keys
        required: set[str] = set()
        optional: set[str] = set()
        for operand in _split_concat(expr):
            for key in _object_keys(fn, operand, body, resolve, _seen):
                (optional if key.startswith("?") else required).add(key.lstrip("?"))
        key_sets.append((required, optional - required))
    if not key_sets:
        raise UngradeableEmitter(
            f"{fn.qualified_name} returns {fn.result} but no RETURN builds an object, so "
            "pg_proc does not say which keys it emits"
        )
    every = set.intersection(*(req for req, _ in key_sets))
    union = set.union(*(req | opt for req, opt in key_sets))
    return {key: key in every for key in sorted(union)}


def _is_json(result: str) -> bool:
    return result.strip().lower() in {"json", "jsonb"}


def emitter_model(
    fn: PgFunction,
    *,
    name: str,
    under_key: str | None = None,
    envelope: dict[str, tuple[Any, Any]] | None = None,
    renames: dict[str, str] | None = None,
    resolve: Resolver | None = None,
) -> type[BaseModel]:
    """The model of what a caller that passes ``fn``'s result through emits.

    ``under_key`` — the caller puts the whole result under this key (a text
    outline, a list of hits): the function contributes that one key.
    Otherwise a JSON object result is SPREAD at the top level, key for key.
    ``envelope`` — fields the caller adds itself (``{name: (type, default)}``),
    in pydantic ``create_model`` form. ``renames`` — keys the caller renames on
    the way through (``topic`` → ``slug``).
    """
    fields: dict[str, tuple[Any, Any]] = dict(envelope or {})
    if under_key is not None:
        fields[under_key] = (Any, ...)
    elif fn.out_columns:
        for column in fn.out_columns:
            fields[(renames or {}).get(column, column)] = (Any, ...)
    elif _is_json(fn.result):
        for key, required in json_return_keys(fn, resolve=resolve).items():
            target = (renames or {}).get(key, key)
            if target in fields:
                continue  # the caller's own envelope wins (it strips e.g. map_id)
            fields[target] = (Any, ...) if required else (Any, None)
    else:
        raise UngradeableEmitter(
            f"{fn.qualified_name} returns {fn.result}; a scalar result must be passed "
            "through under a key"
        )
    # Field definitions are ``(annotation, default)`` pairs; typed as ``Any`` so
    # they cannot bind to create_model's own ``__doc__``/``__module__`` keywords.
    field_definitions: dict[str, Any] = fields
    return create_model(name, __config__=ConfigDict(extra="forbid"), **field_definitions)
