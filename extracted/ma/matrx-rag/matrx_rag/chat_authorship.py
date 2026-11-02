"""Whose words a chat holds — the ONE rule for "the person typed this conversation" (``field_id="typed"``).

A conversation row says, in its own columns, who started it and why: ``conversation_type``
(``standard`` is a person's chat; ``subagent``, ``auto``, ``workflow``, ``scheduled``,
``system_process``, ``research``, ``podcast`` … are runs a machine started), ``origin_class``
(``human`` / ``client_auto`` / ``unknown`` vs ``child_agent`` / ``workflow`` / ``scheduled`` /
``system`` / ``api``), ``source_app`` (``code-plugin`` = a coding-session bridge mirror),
``source_feature`` (``mandate:<key>`` = a declared platform job), ``parent_conversation_id``
(a fork / sub-agent) and ``exclude_from_kg``. Measured on one heavy account (2026-10-25): of
44,956 conversations, ~25,000 are coding-session mirrors and ~9,000 more are agent, workflow,
scheduled or mandate runs — their titles ("researcher subagent", "page summary", "user message")
were the top "topics" of a person who never typed them.

:func:`conversation_skip_reason` answers for one row; every reader that asks "is this chat the
person's own words" — the typed resolver here and the host's inventories — calls it, so the rule
lives once. The thresholds are the host's (:class:`TypedChatPolicy`, injected through
``configure(typed_chat_policy=...)``); there is no package default, because a guessed default
would decide whose words are indexed.

:func:`typed_parts` builds the typed text itself: what the person typed (the authorship
projection, D327) plus the variable values they entered, minus a value equal to the agent's
declared default and minus any line repeated verbatim across ``template_repeat_runs`` runs of the
same agent (a template, a pasted shortcut). Never an assistant reply, a system prompt, or context.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TypedChatPolicy:
    """The host's thresholds for whose words a chat holds (every field is a host knob)."""

    #: ``conversation_type`` values a person's own chat carries.
    person_conversation_types: frozenset[str]
    #: ``origin_class`` values a person's own chat carries (``unknown`` = pre-stamp rows).
    person_origin_classes: frozenset[str]
    #: ``source_app`` values that are mirrors of another tool's session (coding-session bridge).
    mirror_source_apps: frozenset[str]
    #: ``source_feature`` prefixes / exact values a machine job stamps (``mandate:`` …).
    machine_source_features: tuple[str, ...]
    #: Title prefixes a platform automation stamps (``Automation:``, ``<heartbeat>``).
    automation_title_markers: tuple[str, ...]
    #: A line repeated verbatim in at least this many runs of one agent is a template.
    template_repeat_runs: int
    #: How many of the same agent's other runs are read to find templates.
    template_scan_runs: int


#: The columns :func:`conversation_skip_reason` reads (select exactly these).
CONVERSATION_AUTHORSHIP_COLUMNS: tuple[str, ...] = (
    "id",
    "title",
    "conversation_type",
    "origin_class",
    "source_app",
    "source_feature",
    "parent_conversation_id",
    "exclude_from_kg",
)


def _s(value: Any) -> str:
    return str(getattr(value, "value", value) or "").strip()


def conversation_skip_reason(row: Mapping[str, Any], policy: TypedChatPolicy) -> str | None:
    """``None`` when the conversation is the person's own chat, else the first reason it is not.

    Reasons (stable words, reported per kind by every caller): ``excluded_from_kg``,
    ``sub_agent_fork``, ``machine_type:<type>``, ``machine_origin:<class>``,
    ``coding_session_mirror``, ``machine_feature``, ``automation_title``."""
    if row.get("exclude_from_kg"):
        return "excluded_from_kg"
    if row.get("parent_conversation_id"):
        return "sub_agent_fork"
    ctype = _s(row.get("conversation_type")) or "standard"
    if ctype not in policy.person_conversation_types:
        return f"machine_type:{ctype}"
    origin = _s(row.get("origin_class")) or "unknown"
    if origin not in policy.person_origin_classes:
        return f"machine_origin:{origin}"
    if _s(row.get("source_app")) in policy.mirror_source_apps:
        return "coding_session_mirror"
    feature = _s(row.get("source_feature"))
    if feature and any(feature == m or (m.endswith(":") and feature.startswith(m)) for m in policy.machine_source_features):
        return "machine_feature"
    title = _s(row.get("title"))
    if any(title.startswith(m) for m in policy.automation_title_markers if m):
        return "automation_title"
    return None


def variable_values(variables: Any) -> list[tuple[str, str]]:
    """``[(name, text)]`` for every non-empty string a ``chat.conversation.variables`` object holds
    (lists and nested objects flattened, in order; numbers and booleans are settings, not words)."""
    out: list[tuple[str, str]] = []

    def walk(name: str, value: Any) -> None:
        if isinstance(value, str):
            text = value.strip()
            if text:
                out.append((name, text))
        elif isinstance(value, Mapping):
            for k, v in value.items():
                walk(name, v)
        elif isinstance(value, (list, tuple)):
            for v in value:
                walk(name, v)

    if isinstance(variables, Mapping):
        for name, value in variables.items():
            walk(str(name), value)
    return out


def declared_defaults(variable_definitions: Any) -> dict[str, str]:
    """``{name: default text}`` from an agent's ``variable_definitions`` (``defaultValue``)."""
    out: dict[str, str] = {}
    if isinstance(variable_definitions, list):
        for d in variable_definitions:
            if isinstance(d, Mapping) and d.get("name"):
                default = d.get("defaultValue")
                if isinstance(default, str) and default.strip():
                    out[str(d["name"])] = default.strip()
    return out


def lines_of(text: str) -> list[str]:
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def typed_parts(
    *,
    turns: Iterable[str],
    variables: Any,
    defaults: Mapping[str, str],
    other_runs: Iterable[set[str]],
    repeat_runs: int,
) -> tuple[list[str], dict[str, int]]:
    """The person's typed text for one conversation, as lines, plus what was dropped and why.

    ``turns`` are the person's own messages (already projected to their words); ``other_runs`` is
    one set of lines per OTHER run of the same agent. A line present in ``repeat_runs`` runs
    (this one included) is a template and dropped; so is a variable value equal to its default."""
    dropped = {"default_value": 0, "template_line": 0}
    candidates: list[str] = []
    for name, value in variable_values(variables):
        if defaults.get(name) == value:
            dropped["default_value"] += 1
            continue
        candidates.extend(lines_of(value))
    for turn in turns:
        candidates.extend(lines_of(turn))
    seen_in: dict[str, int] = {}
    for run in other_runs:
        for ln in run:
            seen_in[ln] = seen_in.get(ln, 0) + 1
    kept: list[str] = []
    for ln in candidates:
        if repeat_runs > 0 and 1 + seen_in.get(ln, 0) >= repeat_runs:
            dropped["template_line"] += 1
            continue
        kept.append(ln)
    return kept, dropped
