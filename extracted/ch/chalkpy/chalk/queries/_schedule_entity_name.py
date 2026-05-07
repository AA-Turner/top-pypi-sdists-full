from __future__ import annotations

import re

_VALID_SCHEDULE_ENTITY_NAME = re.compile(r"^[A-Za-z0-9_ \-().]+$")


def validate_schedule_entity_name(name: str, *, entity_noun: str) -> str | None:
    """Return an error if the name uses characters outside the allowed set."""
    if not name:
        return f"{entity_noun} was instantiated with an empty name. A non-empty name is required."
    if not _VALID_SCHEDULE_ENTITY_NAME.fullmatch(name):
        return (
            f"{entity_noun} '{name}' has an invalid name. "
            "Use only letters, digits, hyphens, underscores, spaces, parentheses, and periods."
        )
    return None
