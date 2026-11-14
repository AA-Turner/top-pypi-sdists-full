"""people on a card: a teammate as name + email (+ user id), and the owner echo a filtered read carries."""

from __future__ import annotations
from typing import Any

#: What a person shows as, in this order: the words a reader knows them by, then the id `owner` takes.
_PERSON_FIELDS = ("name", "email", "user_id")

#: What a read filtered by person or time says about the filter (people and time filters D4, D8):
#: who `owner` matched, how many rows have no known person, and which corpora a person cannot filter; plus
#: `query_note`, the line a name `query` gets when nothing matched or the page is full.
_OWNER_ECHO_FIELDS = ("owner_matched", "unowned_count", "owner_note", "query_note")


def to_person_card(value: Any, *, show_id: bool = True) -> dict | None:
    """`{name, email, user_id}` with empty fields left off; None when nothing names anyone."""
    if not isinstance(value, dict):
        return None
    fields = _PERSON_FIELDS if show_id else _PERSON_FIELDS[:2]
    card = {key: value[key] for key in fields if value.get(key) not in (None, "")}
    return card if card.get("name") or card.get("email") or card.get("user_id") else None


def to_people_cards(values: Any, *, show_id: bool = True) -> list[dict]:
    """Every person in `values` that names someone, in the server's order (a hit's creator first)."""
    if not isinstance(values, list):
        return []
    return [card for value in values if (card := to_person_card(value, show_id=show_id))]


def get_owner_echo(payload: Any) -> dict:
    """The owner echo fields `payload` carries, shaped for a card: `owner_matched` as people with ids
    (the id is what `owner` takes next time), `unowned_count`, `owner_note`. Empty when there are none."""
    if not isinstance(payload, dict):
        return {}
    echo: dict[str, Any] = {}
    matched = to_people_cards(payload.get("owner_matched"))
    if matched:
        echo["owner_matched"] = matched
    unowned = payload.get("unowned_count")
    if isinstance(unowned, int) and not isinstance(unowned, bool) and unowned > 0:
        echo["unowned_count"] = unowned
    for key in ("owner_note", "query_note"):
        note = payload.get(key)
        if isinstance(note, str) and note.strip():
            echo[key] = note.strip()
    return {key: echo[key] for key in _OWNER_ECHO_FIELDS if key in echo}
