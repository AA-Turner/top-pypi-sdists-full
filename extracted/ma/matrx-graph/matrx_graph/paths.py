"""THE ONE source-path resolver — dotted + indexed field selection.

One notation, one resolver, everywhere a definition points at a field inside
an upstream payload:

* edge mappings (``{"entries": "structured_output.entries"}``) — the scheduler's
  ``_map_edge_payload`` and the dry-run's sample mirror,
* display steps (``output.to_frontend``'s ``payload_key``),
* the ``text.json_path`` node.

Grammar (the union of what the three call sites historically each accepted —
they now all accept all of it):

    ``a.b.c``                 — walk dicts by key
    ``a.0.b`` / ``a[0].b``    — index into lists (both spellings, negatives ok)
    ``a[-1]``                 — last element
    ``a\\.b``                 — backslash-escape a literal dot inside a key
    ``a[*].b`` / ``a.*.b``    — EACH element of a list: the rest of the path is
                                read from every element and the answers come back
                                as a list (an element that lacks it, or holds null,
                                is left out). A second ``*`` flattens one level:
                                ``values[*].socials[*]`` is every social of every
                                value in one list. A dict with a literal ``"*"`` key
                                still reads that key.

A SOURCE (what an edge mapping, a display step or ``text.json_path`` names) is a
path plus three connection powers — so a step never exists only to move data:

    ``a ?? b ?? "none"``      — EITHER-OR / DEFAULT: the first alternative that reads
                                a non-null value wins. An alternative after ``??``
                                may be a JSON literal (``""``, ``[]``, ``{}``, ``0``,
                                ``true``, ``"text"``) and then always answers.
    ``a[0:3]`` / ``a[3:]``    — SLICE a list (Python slice rules, negatives ok).
    ``a[*].{id: page_id, title, why: reason ?? ""}``
                              — PICK + RENAME: build a record from each element (or
                                from one record: ``plan.{title, keywords}``; on a
                                list, ``[*]`` may be left out). A field
                                is ``name: source``, a bare ``name`` or a fixed value
                                (``error: null``, ``kind: "search"``); a field whose
                                source reads nothing is left out of the record (one
                                that reads null stays null: ``age ?? null``).
    ``a[*].{keyword: @}``     — ``@`` is the element itself; ``{n: #}`` its position
                                in the list (0-based).
    ``trim(a)`` / ``lower(a)`` / ``upper(a)`` / ``casefold(a)``
                              — tidy a text, or each text of a list (non-text
                                values pass through). ``trim`` also collapses runs
                                of spaces inside, like ``text.case``.

The notation is JMESPath's (AWS CLI, Ansible) with JavaScript's ``??``.

A miss NEVER raises here: the resolver returns ``(False, None)`` and each call
site decides what a miss means (an edge mapping raises EdgeRoutingError, a
display step renders nothing, ``text.json_path`` returns its default).
"""

from __future__ import annotations

import json
from typing import Any

__all__ = [
    "WILDCARD",
    "first_segment",
    "parse_path",
    "path_syntax_problem",
    "resolve_path",
    "source_paths",
]


ALTERNATIVE = "??"
CURRENT = "@"


def _matching(text: str, start: int, opening: str, closing: str) -> int:
    """Index of the bracket closing ``text[start]``, skipping nested brackets and quoted
    strings; -1 when it never closes."""
    depth = 0
    quote = ""
    i = start
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
        elif ch == opening:
            depth += 1
        elif ch == closing:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _split_top(text: str, sep: str) -> list[str]:
    """Split ``text`` on ``sep`` outside brackets, braces and quoted strings."""
    parts: list[str] = []
    depth = 0
    quote = ""
    last = 0
    i = 0
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
        elif ch in "[{(":
            depth += 1
        elif ch in "]})":
            depth -= 1
        elif depth == 0 and text.startswith(sep, i):
            parts.append(text[last:i])
            i += len(sep)
            last = i
            continue
        i += 1
    parts.append(text[last:])
    return parts


def _alternatives(source: str) -> list[str]:
    return [part.strip() for part in _split_top(source, ALTERNATIVE)]


def _tidy_trim(text: str) -> str:
    return " ".join(text.split())


#: Text tidy-ups a source may wrap a value in — the ones live text.case steps did.
TEXT_FUNCTIONS: dict[str, Any] = {
    "trim": _tidy_trim,
    "lower": str.lower,
    "upper": str.upper,
    "casefold": str.casefold,
}


def _function(alt: str) -> tuple[str, str] | None:
    """``trim(answer)`` → ``("trim", "answer")``; None when ``alt`` is not a call."""
    paren = alt.find("(")
    if paren <= 0 or not alt.endswith(")") or alt[:paren] not in TEXT_FUNCTIONS:
        return None
    if _matching(alt, paren, "(", ")") != len(alt) - 1:
        return None
    return alt[:paren], alt[paren + 1 : -1].strip()


def _apply(name: str, value: Any) -> Any:
    fn = TEXT_FUNCTIONS[name]
    if isinstance(value, str):
        return fn(value)
    if isinstance(value, list):
        return [fn(v) if isinstance(v, str) else v for v in value]
    return value


def _literal(text: str, position: int) -> tuple[bool, Any]:
    """``(True, value)`` when an alternative is a literal, not a path.

    A quoted string and the empty ``[]`` / ``{}`` are literals anywhere; after the first
    ``??`` anything JSON reads (``0``, ``true``, ``null``, ``[1, 2]``) is too. The first
    alternative is otherwise always a path, so a key named ``true`` still reads."""
    t = text.strip()
    if t == "[]":
        return True, []
    if t == "{}":
        return True, {}
    if len(t) >= 2 and t[0] == t[-1] == "'":
        return True, t[1:-1]
    if t[:1] == '"' or position > 0:
        try:
            return True, json.loads(t)
        except ValueError:
            return False, None
    return False, None


def _fields(inner: str) -> list[tuple[str, str]]:
    """``{id: page_id, title}`` → ``[("id", "page_id"), ("title", "title")]``."""
    out: list[tuple[str, str]] = []
    for raw in _split_top(inner, ","):
        if not raw.strip():
            continue
        pieces = _split_top(raw, ":")
        name = pieces[0].strip().strip("\"'")
        source = ":".join(pieces[1:]).strip() if len(pieces) > 1 else name
        out.append((name, source))
    return out


def _slice(inner: str) -> tuple[int | None, int | None] | None:
    parts = inner.split(":")
    if len(parts) != 2:
        return None
    bounds: list[int | None] = []
    for part in parts:
        part = part.strip()
        if not part:
            bounds.append(None)
            continue
        try:
            bounds.append(int(part))
        except ValueError:
            return None
    return bounds[0], bounds[1]


def _tokens(path: str) -> list[tuple[str, Any]]:
    """Every token of one path: ``k`` key, ``i`` index, ``s`` slice, ``p`` pick, ``@``."""
    tokens: list[tuple[str, Any]] = []
    buf: list[str] = []
    i = 0
    n = len(path)

    def flush() -> None:
        if buf:
            word = "".join(buf)
            tokens.append(("@", None) if word == CURRENT else ("k", word))
            buf.clear()

    while i < n:
        ch = path[i]
        if ch == "\\" and i + 1 < n and path[i + 1] == ".":
            buf.append(".")
            i += 2
            continue
        if ch == ".":
            flush()
            i += 1
            continue
        if ch == "{" and not buf:
            end = _matching(path, i, "{", "}")
            if end == -1:
                buf.append(path[i:])
                break
            tokens.append(("p", _fields(path[i + 1 : end])))
            i = end + 1
            continue
        if ch == "[":
            flush()
            end = path.find("]", i)
            if end == -1:
                # Unclosed bracket — treat the remainder as a literal key.
                buf.append(path[i:])
                break
            index_str = path[i + 1 : end].strip()
            bounds = _slice(index_str) if ":" in index_str else None
            if bounds is not None:
                tokens.append(("s", bounds))
            else:
                try:
                    tokens.append(("i", int(index_str)))
                except ValueError:
                    tokens.append(("k", index_str))
            i = end + 1
            continue
        buf.append(ch)
        i += 1
    flush()
    return tokens


def parse_path(path: str) -> list[tuple[str, str | int]]:
    """The leading plain run of keys and indexes of a source's first path — what a declared
    schema can be walked with. Stops at a slice, a pick or ``@`` (beyond them the schema
    probes stay quiet). kind ∈ {'k', 'i'}."""
    first = next(iter(source_paths(path)), "")
    plain: list[tuple[str, str | int]] = []
    for kind, key in _tokens(first):
        if kind not in ("k", "i"):
            break
        plain.append((kind, key))
    return plain


def _unwrap(alt: str) -> str:
    call = _function(alt)
    while call is not None:
        alt = call[1]
        call = _function(alt)
    return alt


def source_paths(source: str) -> list[str]:
    """The path alternatives of a source (literals left out, text functions unwrapped),
    for schema checks."""
    out: list[str] = []
    for pos, alt in enumerate(_alternatives(source)):
        if _literal(alt, pos)[0]:
            continue
        inner = _unwrap(alt)
        if inner != alt:
            out.extend(source_paths(inner))
        else:
            out.append(alt)
    return out


def path_syntax_problem(path: str) -> str | None:
    """Why ``path`` is not a source this grammar can read — or None when it is.

    The resolver never refuses: an empty ``[]`` becomes a key named ``""``, an
    unclosed ``[`` a literal key, ``a..b`` silently loses a segment. Each of those
    resolves to NOTHING at run time, so the step quietly receives no value. Live
    defect 2026-10-27: ``items[].page_id`` (meant ``items[*].page_id``) validated
    "valid" and the step got nothing. The definition validator calls this.
    """
    if not isinstance(path, str) or not path.strip():
        return "the path is empty"
    if path != path.strip():
        return "the path has leading or trailing spaces"
    alternatives = _alternatives(path)
    for pos, alt in enumerate(alternatives):
        if not alt:
            return "'??' needs a value on both sides"
        if _literal(alt, pos)[0]:
            continue
        call = _function(alt)
        if call is not None:
            inner = path_syntax_problem(call[1]) if call[1] else "it reads nothing"
            if inner is not None:
                return f"in {call[0]}(…): {inner}"
            continue
        if alt[:1] in "\"'":
            return f"{alt} opens a quoted value that never closes"
        problem = _plain_path_problem(alt)
        if problem is not None:
            return problem if len(alternatives) == 1 else f"in '{alt}': {problem}"
    return None


def _plain_path_problem(path: str) -> str | None:
    i = 0
    n = len(path)
    while i < n:
        ch = path[i]
        if ch == "\\" and i + 1 < n and path[i + 1] == ".":
            i += 2
            continue
        if ch == "{":
            if i > 0 and path[i - 1] != ".":
                return f"'{{' at position {i} must start a segment (write 'a.{{...}}')"
            end = _matching(path, i, "{", "}")
            if end == -1:
                return f"'{{' at position {i} is never closed"
            fields = _fields(path[i + 1 : end])
            if not fields:
                return f"'{{}}' at position {i} picks nothing — name at least one field"
            for name, source in fields:
                if not name:
                    return f"a field in the pick at position {i} has no name"
                inner = path_syntax_problem(source)
                if inner is not None:
                    return f"field '{name}': {inner}"
            i = end + 1
            if i < n and path[i] not in ".[":
                return f"'{path[i]}' follows '}}' at position {i - 1} — expected '.' or '['"
            continue
        if ch == "}":
            return f"'}}' at position {i} has no matching '{{'"
        if ch == "[":
            end = path.find("]", i)
            if end == -1:
                return f"'[' at position {i} is never closed"
            inner = path[i + 1 : end].strip()
            if not inner:
                return (
                    f"'[]' at position {i} is not path syntax — write '[*]' for each "
                    "element of a list, or '[0]' for one element"
                )
            if "[" in inner:
                return f"'[' at position {i} opens again before it closes"
            if ":" in inner and _slice(inner) is None:
                return f"'[{inner}]' at position {i} is not a slice — write '[0:3]', '[3:]' or '[:-1]'"
            i = end + 1
            if i < n and path[i] not in ".[":
                return f"'{path[i]}' follows ']' at position {i - 1} — expected '.' or '['"
            continue
        if ch == "]":
            return f"']' at position {i} has no matching '['"
        if ch == "." and (i == 0 or i == n - 1 or path[i + 1] == "."):
            return f"empty segment at position {i} ('.' with nothing on one side)"
        i += 1
    return None


def _as_index(key: str | int) -> int | None:
    if isinstance(key, int):
        return key
    try:
        return int(key)
    except (TypeError, ValueError):
        return None


WILDCARD = "*"


def resolve_path(value: Any, path: str) -> tuple[bool, Any]:
    """Resolve the source ``path`` against ``value``. Returns ``(found, resolved)``.

    A dict key wins over an index reading: ``{"0": x}`` resolves ``a.0`` to
    ``x`` when ``a`` is that dict, and to ``a[0]`` when ``a`` is a list.
    ``*`` on a list reads the rest of the path from each element; ``??``, slices
    and picks as in the module doc.
    """
    alternatives = _alternatives(path)
    last: tuple[bool, Any] = (False, None)
    for pos, alt in enumerate(alternatives):
        is_literal, literal = _literal(alt, pos)
        if is_literal:
            return True, literal
        call = _function(alt)
        if call is not None:
            found, val = resolve_path(value, call[1])
            last = (found, _apply(call[0], val) if found else val)
        else:
            last = _resolve(value, _tokens(alt))
        if len(alternatives) == 1 or (last[0] and last[1] is not None):
            return last
    return last


POSITION = "#"


def _pick(value: Any, fields: list[tuple[str, str]], position: int | None = None) -> dict[str, Any]:
    record: dict[str, Any] = {}
    for name, source in fields:
        if source == POSITION:
            if position is not None:
                record[name] = position
            continue
        # A field may be a fixed value: ``{error: null, kind: "search", n: 0}``.
        is_literal, literal = _literal(source, 1)
        if is_literal:
            record[name] = literal
            continue
        found, val = resolve_path(value, source)
        if found:
            record[name] = val
    return record


def _resolve(value: Any, tokens: list[tuple[str, Any]]) -> tuple[bool, Any]:
    current = value
    for pos, (kind, key) in enumerate(tokens):
        if kind == "@":
            continue
        if kind == "p":
            if current is None:
                return False, None
            # A pick on a list picks from each element (``pages.{id: page_id}``).
            current = (
                [_pick(el, key, i) for i, el in enumerate(current) if el is not None]
                if isinstance(current, list)
                else _pick(current, key)
            )
            continue
        if kind == "s":
            if not isinstance(current, list):
                return False, None
            current = current[key[0] : key[1]]
            continue
        if isinstance(current, dict):
            if kind == "k" and key in current:
                current = current[key]
                continue
            return False, None
        if isinstance(current, list):
            if key == WILDCARD:
                rest = tokens[pos + 1 :]
                flatten = any(k == WILDCARD for _, k in rest)
                picked: list[Any] = []
                for position, element in enumerate(current):
                    if element is None:
                        continue
                    if rest and rest[0][0] == "p":
                        found, val = _resolve(_pick(element, rest[0][1], position), rest[1:])
                    else:
                        found, val = _resolve(element, rest)
                    if not found or val is None:
                        continue
                    if flatten and isinstance(val, list):
                        picked.extend(val)
                    else:
                        picked.append(val)
                return True, picked
            idx = _as_index(key)
            if idx is None:
                return False, None
            try:
                current = current[idx]
            except IndexError:
                return False, None
            continue
        return False, None
    return True, current


def first_segment(path: str) -> str:
    """The leading KEY segment of the source's first path — what a declared
    output schema's top-level properties are checked against. ``""`` when the path
    opens with an index (``[0].x``) or a pick, which no top-level schema property can name."""
    tokens = parse_path(path)
    if tokens and tokens[0][0] == "k":
        return str(tokens[0][1])
    return ""
