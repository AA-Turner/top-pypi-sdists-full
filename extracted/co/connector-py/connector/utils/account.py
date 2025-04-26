"""Account related utility functions."""


def full_name(given_name: str | None, family_name: str | None) -> str:
    """Get full name."""
    return " ".join(filter(None, (given_name, family_name))).strip()
