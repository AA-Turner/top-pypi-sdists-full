"""Ranked command-palette suggestions for bare-slash REPL entry (#1429)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .commands import (
    ALL_COMMAND_NAMES,
    COMMAND_ARGUMENT_HINTS,
    COMMAND_DESCRIPTIONS,
    COMMAND_INTENT_LABELS,
    COMMAND_INTENTS,
    COMMAND_SEARCH_TERMS,
    SUBCOMMAND_COMPLETIONS,
)

_WORD_RE = re.compile(r"[^a-z0-9]+")

_INTENT_ORDER: dict[str, int] = {
    "conversation": 0,
    "workspace": 1,
    "inspect": 2,
    "workflow": 3,
    "session": 4,
}

_PREFERRED_ORDER: tuple[str, ...] = (
    "new",
    "search",
    "resume",
    "last",
    "list",
    "clear",
    "space",
    "tools",
    "model",
    "help",
    "upload",
    "plan",
    "task",
    "pack",
    "artifact",
    "usage",
)
_PREFERRED_INDEX = {name: idx for idx, name in enumerate(_PREFERRED_ORDER)}
_ALL_COMMAND_INDEX = {name: idx for idx, name in enumerate(ALL_COMMAND_NAMES)}


@dataclass(frozen=True)
class CommandPaletteSuggestion:
    """A ranked command suggestion rendered in the REPL completion menu."""

    command: str
    insert_text: str
    display_text: str
    description: str
    intent: str
    intent_label: str
    meta_text: str


def should_open_command_palette(text: str) -> bool:
    """Return True when the buffer should behave like a slash-command palette."""

    stripped = text.lstrip()
    if not stripped.startswith("/"):
        return False
    if "\n" in stripped:
        return False
    return " " not in stripped


def get_command_palette_suggestions(query: str, *, limit: int = 12) -> tuple[CommandPaletteSuggestion, ...]:
    """Return ranked slash-command suggestions for the current query."""

    normalized_query = _normalize(query)
    ranked: list[tuple[int, tuple[int, int, int], CommandPaletteSuggestion]] = []

    for command in ALL_COMMAND_NAMES:
        suggestion = _build_suggestion(command)
        score = _score_suggestion(suggestion, normalized_query)
        if normalized_query and score is None:
            continue
        ranked.append((score or 0, _sort_key(suggestion), suggestion))

    ranked.sort(key=lambda item: (-item[0], *item[1]))
    return tuple(suggestion for _, _, suggestion in ranked[:limit])


def _build_suggestion(command: str) -> CommandPaletteSuggestion:
    hint = COMMAND_ARGUMENT_HINTS.get(command)
    display_text = f"/{command} {hint}" if hint else f"/{command}"
    insert_text = f"/{command} " if hint else f"/{command}"
    intent = COMMAND_INTENTS.get(command, "inspect")
    intent_label = COMMAND_INTENT_LABELS.get(intent, "Inspect")
    description = COMMAND_DESCRIPTIONS[command]
    meta_text = f"{intent_label} · {description}"
    return CommandPaletteSuggestion(
        command=command,
        insert_text=insert_text,
        display_text=display_text,
        description=description,
        intent=intent,
        intent_label=intent_label,
        meta_text=meta_text,
    )


def _score_suggestion(suggestion: CommandPaletteSuggestion, query: str) -> int | None:
    if not query:
        return 0

    tokens = tuple(token for token in query.split() if token)
    if not tokens:
        return 0

    terms = _search_terms(suggestion)
    name = suggestion.command
    exact_terms = _exact_match_terms(suggestion)
    prefix_terms = _prefix_match_terms(suggestion)
    blob = " ".join(terms)
    total = 0

    for token in tokens:
        if token == name:
            total += 400
            continue
        if token in exact_terms:
            total += 300
            continue
        if name.startswith(token):
            total += 320 - min(len(name) - len(token), 40)
            continue
        prefixed = next((term for term in prefix_terms if term.startswith(token)), None)
        if prefixed is not None:
            total += 260 - min(len(prefixed) - len(token), 30)
            continue
        if token in blob:
            total += 120
            continue
        return None

    if query == name:
        total += 120
    if any(term == query for term in terms):
        total += 90
    return total


def _search_terms(suggestion: CommandPaletteSuggestion) -> tuple[str, ...]:
    command = suggestion.command
    extras = COMMAND_SEARCH_TERMS.get(command, ())
    subcommands = tuple(SUBCOMMAND_COMPLETIONS.get(command, ()))
    normalized_subcommands = tuple(_normalize(part) for part in subcommands)
    terms = (
        command,
        _normalize(suggestion.display_text),
        _normalize(suggestion.description),
        _normalize(suggestion.intent_label),
        *extras,
        *normalized_subcommands,
    )
    return tuple(part for part in terms if part)


def _exact_match_terms(suggestion: CommandPaletteSuggestion) -> frozenset[str]:
    return frozenset(
        term
        for term in (
            *COMMAND_SEARCH_TERMS.get(suggestion.command, ()),
            *(_normalize(part) for part in SUBCOMMAND_COMPLETIONS.get(suggestion.command, ())),
        )
        if term
    )


def _prefix_match_terms(suggestion: CommandPaletteSuggestion) -> tuple[str, ...]:
    return (
        *COMMAND_SEARCH_TERMS.get(suggestion.command, ()),
        *(_normalize(part) for part in SUBCOMMAND_COMPLETIONS.get(suggestion.command, ())),
        _normalize(suggestion.display_text),
        _normalize(suggestion.description),
        _normalize(suggestion.intent_label),
    )


def _sort_key(suggestion: CommandPaletteSuggestion) -> tuple[int, int, int]:
    intent_order = _INTENT_ORDER.get(suggestion.intent, 99)
    preferred = _PREFERRED_INDEX.get(suggestion.command, len(_PREFERRED_INDEX))
    natural = _ALL_COMMAND_INDEX[suggestion.command]
    return (intent_order, preferred, natural)


def _normalize(value: str) -> str:
    return " ".join(part for part in _WORD_RE.sub(" ", value.lower()).split() if part)
