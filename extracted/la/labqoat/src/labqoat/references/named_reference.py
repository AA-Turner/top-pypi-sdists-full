"""Validation shared by authored family and revision selectors."""

import re


class NamedReference:
    """Validate fully qualified family names and explicit revision selectors."""

    @staticmethod
    def validate(name: str, revision: str) -> None:
        """Require a qualified name and an unambiguous revision."""
        if re.fullmatch(r"[a-z][a-z0-9-]*(?:/[a-z][a-z0-9-]*)+", name) is None:
            raise ValueError("Expected a qualified lowercase family name")
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", revision) is None:
            raise ValueError("Expected a revision selector")

    @staticmethod
    def parse(value: str) -> tuple[str, str]:
        """Split a named reference, defaulting omitted selectors to latest."""
        name, separator, revision = value.partition("@")
        selected = revision if separator else "latest"
        NamedReference.validate(name, selected)
        return name, selected
