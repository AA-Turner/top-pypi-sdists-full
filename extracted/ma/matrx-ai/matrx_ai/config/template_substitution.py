"""THE ONE ``{{variable}}`` substitution rule.

THIS IS HOW WE DO IT:
1. Only DECLARED variables are filled: the exact text ``{{name}}`` for each name given.
2. Filled ONCE, on the first turn. A second fill (a forced re-apply, a clone) restarts from the
   authored template — never from filled text — and a part changed since refuses loudly.
3. A declared variable with no value becomes ``""``.
4. Every other ``{{...}}`` is left exactly as written. The server never searches text for
   braces, never reports them, never removes them.
5. One pass: text a value brings in is never filled.
6. The one escape: ``{{!name}}`` in the author's text becomes ``{{name}}``, in the same pass
   (also ``{{!#name}}``, ``{{!^name}}``, ``{{!/name}}`` and ``{{!<name>}}``), for ANY name — the
   escape exists for names that are NOT variables (an example token in a prompt that teaches
   prompts), so it never depends on what is declared (Arman, 2026-10-25). A name is one run of
   characters with no space and no brace (a DECLARED name is also matched verbatim, spaces and all).
   ``{{! a comment }}`` (a space after ``!``), ``{{!-- note --}}`` and ``{{!}}`` are not escapes and are
   left as written. The model sees ``{{name}}`` either way: an undeclared
   ``{{name}}`` is left as written (rule 4), so escaping it changes nothing the model reads.
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
9. A platform value (``PlatformValue`` / ``PlatformList`` / ``PlatformDict``: an undeclared
   ``vsc_*`` or ``__name__`` key a door passes through for its own use) is never filled and never
   forms a section, whatever its type.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from typing import Any

ESCAPE_OPEN = "{{!"


class VariableRefillError(RuntimeError):
    """A second fill could not restart a part from its authored template.

    Every fill starts again from each part's authored template, so a value's own braces are
    never filled. A part whose text changed after its fill (or that the fill removed) cannot
    restart honestly; the refill refuses instead of being silently ignored."""

    def __init__(self, part: str, reason: str) -> None:
        super().__init__(
            f"Cannot fill variables again: {part} {reason}. Fill a fresh copy of the agent's "
            "authored definition instead."
        )
        self.part = part
        self.reason = reason


class VariablesAlreadyAppliedError(RuntimeError):
    """New values were given to an agent whose variables were already applied.

    Variables are filled once. New values on an applied agent were silently stored and never
    reached the prompt; they now refuse loudly (owner ruling 2026-10-16) and are recorded."""

    def __init__(self, names: list[str]) -> None:
        super().__init__(
            f"Variables were already applied to this agent; the new values for "
            f"{', '.join(names)} would never reach its prompt. Fill a fresh copy instead "
            "(agent.clone().with_variables(...)), or refill deliberately with "
            "set_variable(...) then apply_variables(force=True)."
        )
        self.names = names


#: Set on a part by its fill: the text the fill produced. A later fill restarts from the authored
#: template only when the part still holds exactly this text.
FILLED_ATTR = "_filled_text"


def restart_point(part: Any, current: Any, label: str) -> None:
    """Refuse a refill of ``part`` when its text changed since its last fill (``current`` != the
    text that fill produced). A part never filled passes."""
    filled = getattr(part, FILLED_ATTR, None)
    if filled is not None and current != filled:
        raise VariableRefillError(label, "was changed after its variables were filled")


#: Any NAME for rule 6: one run with no whitespace, brace or angle bracket, not starting with a marker
#: or ``-`` (so a Handlebars-style ``{{!-- note --}}`` is never read as an escape).
_ANY_ESCAPE_NAME = r"[^\s{}<>!#^/\-][^\s{}<>]*"


def escape_pattern(declared: Any = ()) -> str:
    """Rule 6, exactly: ``{{!`` + optional ``#``/``^``/``/`` + NAME + ``}}``, or ``{{!<`` + NAME +
    ``>}}`` — NAME is any space-free name, or a ``declared`` name verbatim (a declared name may hold
    a space: ``{{!first name}}``)."""
    names = sorted({str(n) for n in declared if str(n)}, key=len, reverse=True)
    name = "(?:" + "|".join([*(re.escape(n) for n in names), _ANY_ESCAPE_NAME]) + ")"
    return r"\{\{!(?P<e>[#^/]?" + name + r"|<" + name + r">)\}\}"


#: The person's typed content, marked the moment it joins a message: never filled, escaped or
#: section-evaluated, however many times a pass runs (THE USER-INPUT LAW).
_DATA_ATTR = "_variable_data"
#: Typed text glued onto the end of an AUTHORED text block: that tail is data, the head is the
#: authored template.
_DATA_TAIL_ATTR = "_variable_data_tail"


def mark_as_data(content: Any) -> None:
    """Mark a content block as data: no pass ever fills it."""
    try:
        setattr(content, _DATA_ATTR, True)
    except (AttributeError, TypeError):
        pass


def is_data(content: Any) -> bool:
    return bool(getattr(content, _DATA_ATTR, False))


def add_data_tail(content: Any, tail: str) -> None:
    """Record ``tail`` (already appended to ``content.text``) as data glued to an authored block."""
    try:
        setattr(content, _DATA_TAIL_ATTR, getattr(content, _DATA_TAIL_ATTR, "") + tail)
    except (AttributeError, TypeError):
        pass


def data_tail(content: Any) -> str:
    return getattr(content, _DATA_TAIL_ATTR, "") or ""


class OffValue(str):
    """A toggle's off label (``toggleValues[0]``, default "No"): fills its slot with its text, but a
    ``{{#name}}`` section treats it as empty. Composition (``agents.variables``) marks it."""


class PlatformValue(str):
    """A value a door passes through for its own use (an undeclared ``vsc_*`` or ``__name__`` key):
    kept in the run's values, never filled into text and never a section (rule 9). Composition
    (``agents.variables``) marks it."""


class PlatformList(list):
    """``PlatformValue`` for a list (``__agent_user_input__`` as content parts, ``vsc_open_files``)."""


class PlatformDict(dict):
    """``PlatformValue`` for a dict."""


def as_platform_value(value: Any) -> Any:
    """Mark a door's own value so substitution never fills it (rule 9), whatever its type: a list
    or dict keeps its shape; anything else (text, a number, ``None``) becomes ``PlatformValue``
    text."""
    if is_platform_value(value):
        return value
    if isinstance(value, list):
        return PlatformList(value)
    if isinstance(value, dict):
        return PlatformDict(value)
    return PlatformValue("" if value is None else value)


def is_platform_value(value: Any) -> bool:
    return isinstance(value, (PlatformValue, PlatformList, PlatformDict))


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


def declared_values_given(
    template: str, variables: Mapping[str, Any], render: Callable[[Any], str]
) -> bool:
    """True when a DECLARED variable the template names was given a non-empty value.

    The variable rule's own answer to "did the run put anything in this turn?": it reads the
    declared values, never the text (no search for braces). A turn whose every declared slot
    was filled with nothing is the author's sentence with holes in it, not run context.
    """
    for name, value in variables.items():
        if is_platform_value(value):
            continue
        if any(token in template for token in (f"{{{{{name}}}}}", f"{{{{#{name}}}}}", f"{{{{<{name}>}}}}")):
            if is_filled(value, render):
                return True
    return False


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

    ``unescape`` also turns an escape ``{{!name}}`` into ``{{name}}`` (rule 6) — only while ``text`` is still the
    untouched authored template, so a value's text is never changed. ``sections`` (default: same as
    ``unescape``) evaluates the ``{{#name}}`` / ``{{^name}}`` sections first, on that same text.
    ``blocks`` maps each DECLARED prompt block name to its resolved text (rule 8)."""
    if any(is_platform_value(v) for v in variables.values()):
        variables = {k: v for k, v in variables.items() if not is_platform_value(v)}
    if (unescape if sections is None else sections) and text == template:
        text = template = apply_sections(template, variables, render)
    names = authored_names(template, variables)
    block_names = [n for n in (blocks or {}) if block_token(n) in template]
    escape = (
        escape_pattern([*variables, *(blocks or {})])
        if unescape and text == template and ESCAPE_OPEN in text
        else None
    )
    strip = escape is not None and re.search(escape, text) is not None
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
        alternatives.append(escape)
    rendered = {name: render(variables[name]) for name in names}
    wrapped = {name: wrap_block(name, str((blocks or {})[name] or "")) for name in block_names}
    pattern = re.compile("|".join(alternatives))

    def replace(m: re.Match[str]) -> str:
        groups = m.groupdict()
        if groups.get("v") is not None:
            return rendered[groups["v"]]
        if groups.get("b") is not None:
            return wrapped[groups["b"]]
        return "{{" + groups["e"] + "}}"

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
    messages are authored; nothing is inferred from text. ``UnifiedConfig.from_dict`` lifts the
    authored system/developer messages into the system instruction and the config builder drops
    every blank message (``message_config.is_blank_message``), keeping the rest in order, so the
    authored ones are the first K config messages, K = the non-system, non-blank messages among
    the first N wire messages — counted with the builder's own blank test, so a blank authored
    message can never shift the selection onto history or the typed turn. Capture the result by
    identity right after the config is built and pass it as
    ``replace_variables(..., template_messages=...)``. ``None``/0 (an older client) = nothing is
    filled: typed text and history are never filled.
    """
    count = template_message_count or 0
    if count <= 0:
        return []
    from matrx_ai.config.message_config import UnifiedMessage, is_blank_message

    def _role(m: Any) -> str:
        role = m.get("role") if isinstance(m, Mapping) else getattr(m, "role", None)
        return str(getattr(role, "value", role))

    def _kept(m: Any) -> bool:
        if isinstance(m, UnifiedMessage):
            message = m
        elif isinstance(m, Mapping):
            message = UnifiedMessage.from_dict(dict(m))
        elif hasattr(m, "model_dump"):
            message = UnifiedMessage.from_dict(m.model_dump(exclude_none=True))
        else:
            return True  # not a wire shape the builder reads; counted as before
        return not is_blank_message(message)

    authored = sum(
        1 for m in list(wire_messages)[:count] if _role(m) not in _SYSTEM_ROLES and _kept(m)
    )
    return list(config_messages)[:authored]


def fold_typed_turn_into_template(config_messages: Any, template_messages: list[Any]) -> bool:  # api-any-ok: the config's MessageList
    """Join the typed turn onto the authored template's trailing user message, as its own block.

    THE AGENT DOOR'S SHAPE, on every door. A saved agent's run appends the person's words to its
    authored user message (``append_or_extend_user_text(own_block=True)``): ONE user message whose
    ``content`` is template block(s) + typed block and whose ``user_content`` is only what she
    typed. A client-carried door (``/ai/manual``, the Builder's Test run) sends the template and
    the typed turn as two messages; the turn's trigger is the typed one, so only it was stored and
    turn 2 reloaded a history without the filled template (PB-03, 2026-10-16: "Order name:
    Benedita Raposo" gone, reply NOT PROVIDED). Folded here, the stored turn equals the agent
    door's and the provider receives the same single user message.

    Folds only when the last authored message is a user message and the very next message is the
    new typed user turn (no DB id/position) and is the last one. Returns whether it folded."""
    if not template_messages:
        return False
    from matrx_ai.config.message_config import Role

    items = list(config_messages)
    last_authored = template_messages[-1]
    try:
        index = next(i for i, m in enumerate(items) if m is last_authored)
    except StopIteration:
        return False
    if index != len(items) - 2:
        return False
    typed = items[-1]
    if last_authored.role != Role.USER or typed.role != Role.USER:
        return False
    if getattr(typed, "id", None) is not None and getattr(typed, "position", None) is not None:
        return False
    typed_blocks = list(typed.content or [])
    if not typed_blocks:
        return False
    last_authored.content = list(last_authored.content or []) + typed_blocks
    said = typed.user_content if typed.user_content is not None else typed_blocks
    last_authored.user_content = list(said)
    config_messages.pop(len(items) - 1)
    return True
