"""Shared lexical normalization for refinement path tokens."""

import unicodedata as _unicodedata


def normalize_refinement_path(value: str) -> tuple[str | None, str | None]:
    """Convert separators or return the first ordered lexical error.

    Only backslashes are normalized; all other valid token text is preserved.
    Lexical success does not authorize a path or establish filesystem validity.
    """
    if not value:
        return None, "empty_token"
    if any(_unicodedata.category(character) == "Cc" for character in value):
        return None, "control_character"
    if any(character.isspace() for character in value):
        return None, "whitespace_character"

    normalized = value.replace("\\", "/")
    drive_rooted = (
        len(normalized) >= 3
        and ("A" <= normalized[0] <= "Z" or "a" <= normalized[0] <= "z")
        and normalized[1:3] == ":/"
    )
    if normalized.startswith("/") or drive_rooted:
        return None, "absolute_path"
    if any(segment in {".", ".."} for segment in normalized.split("/")):
        return None, "traversal_segment"
    return normalized, None
