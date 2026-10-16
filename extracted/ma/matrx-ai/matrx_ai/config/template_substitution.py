"""THE ONE ``{{variable}}`` substitution rule.

THIS IS HOW WE DO IT:
1. Only DECLARED variables are filled: the exact text ``{{name}}`` for each name given.
2. Filled ONCE, on the first turn. Never again.
3. A declared variable with no value becomes ``""``.
4. Every other ``{{...}}`` is left exactly as written. The server never searches text for
   braces, never reports them, never removes them.
5. One pass: text a value brings in is never filled.
6. The one escape: ``{{!name}}`` in the author's text becomes ``{{name}}``, in the same pass.
   Nothing else.
7. Sections (Mustache), authored text only, same pass, evaluated before the slots are filled:
   ``{{#name}}...{{/name}}`` stays only when declared ``name`` has a value that is not empty or
   whitespace-only; ``{{^name}}...{{/name}}`` stays only when it is empty. Empty is decided once,
   here (``is_filled``): None, blank text, ``False``, an empty list/dict, or a toggle's off label
   (``OffValue``). Any other value, including the text "false" or "No", is filled. Only declared names form
   sections; any other ``{{#x}}`` is left as written. A section tag alone on its line removes that
   whole line. An unclosed or unmatched tag is left as written. ``{{!#name}}`` is the escape.
8. Prompt blocks: ``{{<name>}}`` for each DECLARED block becomes ``<name>\n{text}\n</name>`` (the
   wrapper is part of the form); empty text becomes ``""``. Block text is a value: never filled,
   never section-evaluated, never unescaped. An undeclared ``{{<x>}}`` is left as written.
   ``{{!<name>}}`` is the escape (rule 6).
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from typing import Any

ESCAPE_OPEN = "{{!"


class OffValue(str):
    """A toggle's off label (``toggleValues[0]``, default "No"): fills its slot with its text, but a
    ``{{#name}}`` section treats it as empty. Composition (``agents.variables``) marks it."""


def is_empty_value(value: Any) -> bool:
    """A value that means "nothing was given" for the run's precedence ladder: None, blank text, or
    an empty list/dict. ``False`` and ``0`` are given values here (they only empty a section)."""
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    return isinstance(value, (list, tuple, set, frozenset, dict)) and not value


def authored_names(template: str, variables: Mapping[str, Any]) -> list[str]:
    """Variable names whose exact ``{{name}}`` appears in ``template``."""
    return [name for name in variables if f"{{{{{name}}}}}" in template]


def is_filled(value: Any, render: Callable[[Any], str]) -> bool:
    """A value fills a section unless it is None, ``False``, an empty container, blank text or a
    toggle's off label (``OffValue``)."""
    if value is None or value is False or isinstance(value, OffValue):
        return False
    if isinstance(value, (list, tuple, set, frozenset, dict)) and not value:
        return False
    return bool(render(value).strip())


def _whitespace(chunk: str) -> bool:
    return chunk.strip(" \t\r") == ""


def apply_sections(
    template: str, variables: Mapping[str, Any], render: Callable[[Any], str]
) -> str:
    """Keep or drop the ``{{#name}}`` / ``{{^name}}`` sections of ``template`` (declared names only)."""
    if not variables or ("{{#" not in template and "{{^" not in template):
        return template
    names = sorted(variables, key=len, reverse=True)
    tag = re.compile(r"\{\{([#^/])(" + "|".join(re.escape(str(n)) for n in names) + r")\}\}")
    tokens = [(m.start(), m.end(), m.group(1), m.group(2)) for m in tag.finditer(template)]
    if not tokens:
        return template

    # Pair each close with the nearest open of the same name; the rest stay literal.
    stack: list[int] = []
    close_of: dict[int, int] = {}
    for i, (_, _, kind, name) in enumerate(tokens):
        if kind in "#^":
            stack.append(i)
        else:
            for depth in range(len(stack) - 1, -1, -1):
                if tokens[stack[depth]][3] == name:
                    close_of[stack[depth]] = i
                    del stack[depth:]
                    break
    if not close_of:
        return template

    def span(index: int) -> tuple[int, int, bool]:
        """The text a tag takes with it: its whole line when it stands alone on it."""
        start, end, _, _ = tokens[index]
        line_start = template.rfind("\n", 0, start) + 1
        line_end = template.find("\n", end)
        stop = len(template) if line_end == -1 else line_end
        if _whitespace(template[line_start:start]) and _whitespace(template[end:stop]):
            return line_start, (stop if line_end == -1 else stop + 1), True
        return start, end, False

    acc: list[str] = []

    def write(chunk: str, after_line_tag: bool) -> None:
        """Append ``chunk``; right after a removed tag line, a blank line already written is not doubled."""
        if after_line_tag:
            written = "".join(acc[-2:]) if acc else ""
            if written == "" or written.replace("\r", "").endswith("\n\n"):
                chunk = chunk.lstrip("\r\n")
        if chunk:
            acc.append(chunk)

    def emit(first: int, last: int, begin: int, finish: int, lead_line: bool) -> None:
        cursor = begin
        pending = lead_line
        i = first
        while i < last:
            if i not in close_of:
                i += 1
                continue
            j = close_of[i]
            open_from, open_to, open_line = span(i)
            close_from, close_to, close_line = span(j)
            filled = is_filled(variables[tokens[i][3]], render)
            keep = filled == (tokens[i][2] == "#")
            if not keep:
                # A removed section that leaves its line(s) empty takes the line(s) with it.
                head = template.rfind("\n", 0, open_from) + 1
                tail_end = template.find("\n", close_to)
                tail = len(template) if tail_end == -1 else tail_end
                if _whitespace(template[head:open_from]) and _whitespace(template[close_to:tail]):
                    write(template[cursor:head], pending)
                    cursor = tail if tail_end == -1 else tail + 1
                    pending = True
                    i = j + 1
                    continue
            write(template[cursor:open_from], pending)
            if keep:
                emit(i + 1, j, open_to, close_from, open_line)
                pending = close_line
            else:
                pending = open_line or close_line
            cursor = close_to
            i = j + 1
        write(template[cursor:finish], pending)

    emit(0, len(tokens), 0, len(template), False)
    return "".join(acc)


def block_token(name: str) -> str:
    """The exact authored text of a prompt block: ``{{<name>}}``."""
    return "{{<" + name + ">}}"


def wrap_block(name: str, text: str) -> str:
    """What a declared ``{{<name>}}`` becomes: the text wrapped in a tag of its name."""
    return f"<{name}>\n{text}\n</{name}>" if text.strip() else ""


def substitute_authored(
    text: str,
    template: str,
    variables: Mapping[str, Any],
    render: Callable[[Any], str],
    *,
    unescape: bool = False,
    sections: bool | None = None,
    blocks: Mapping[str, str] | None = None,
) -> str:
    """Fill the declared slots of ``template`` in ``text`` in one pass.

    ``unescape`` also turns ``{{!`` into ``{{`` — only while ``text`` is still the
    untouched authored template, so a value's text is never changed. ``sections`` (default: same as
    ``unescape``) evaluates the ``{{#name}}`` / ``{{^name}}`` sections first, on that same text.
    ``blocks`` maps each DECLARED prompt block name to its resolved text (rule 8)."""
    if (unescape if sections is None else sections) and text == template:
        text = template = apply_sections(template, variables, render)
    names = authored_names(template, variables)
    block_names = [n for n in (blocks or {}) if block_token(n) in template]
    strip = unescape and text == template and ESCAPE_OPEN in text
    if not names and not strip and not block_names:
        return text
    alternatives = []
    if names:
        names.sort(key=len, reverse=True)
        alternatives.append(r"\{\{(?P<v>" + "|".join(re.escape(n) for n in names) + r")\}\}")
    if block_names:
        block_names.sort(key=len, reverse=True)
        alternatives.append(r"\{\{<(?P<b>" + "|".join(re.escape(n) for n in block_names) + r")>\}\}")
    if strip:
        alternatives.append(re.escape(ESCAPE_OPEN))
    rendered = {name: render(variables[name]) for name in names}
    wrapped = {name: wrap_block(name, str((blocks or {})[name] or "")) for name in block_names}
    pattern = re.compile("|".join(alternatives))

    def replace(m: re.Match[str]) -> str:
        groups = m.groupdict()
        if groups.get("v") is not None:
            return rendered[groups["v"]]
        if groups.get("b") is not None:
            return wrapped[groups["b"]]
        return "{{"

    return pattern.sub(replace, text)


_SYSTEM_ROLES = frozenset({"system", "developer"})


def authored_template_messages(
    wire_messages: Any,  # api-any-ok: wire messages are dicts (local) or models (server)
    template_message_count: int | None,
    config_messages: Any,  # api-any-ok: the config's message list, sliced by identity
) -> list[Any]:
    """The config messages that are the AUTHORED template — the only ones filled.

    ONE implementation for every host that takes a client-carried ``messages[]`` (aidream
    ``/ai/manual`` + ``/ai/chat``, matrx-local's engine). The client says how many leading wire
    messages are authored; nothing is inferred from text. ``build_unified_config`` lifts
    system/developer messages into the system instruction and keeps every other message in
    order, so the authored ones are the first K config messages, K = the non-system messages
    among the first N wire messages. Capture the result by identity right after the config is
    built and pass it as ``replace_variables(..., template_messages=...)``. ``None``/0 (an older
    client) = nothing is filled: typed text and history are never filled.
    """
    count = template_message_count or 0
    if count <= 0:
        return []

    def _role(m: Any) -> str:
        role = m.get("role") if isinstance(m, Mapping) else getattr(m, "role", None)
        return str(getattr(role, "value", role))

    authored = sum(1 for m in list(wire_messages)[:count] if _role(m) not in _SYSTEM_ROLES)
    return list(config_messages)[:authored]
