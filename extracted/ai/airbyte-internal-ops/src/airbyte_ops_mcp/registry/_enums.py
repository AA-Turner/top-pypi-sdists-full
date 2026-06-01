# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Shared StrEnum types for registry filtering and metadata.

These enums provide strongly typed values for connector properties used
across registry operations, CLI commands, and MCP tools.
"""

from __future__ import annotations

from enum import StrEnum


class SupportLevel(StrEnum):
    """Connector support levels ordered by precedence."""

    ARCHIVED = "archived"
    COMMUNITY = "community"
    CERTIFIED = "certified"

    @property
    def precedence(self) -> int:
        """Numeric precedence for ordering comparisons.

        Higher values indicate higher support commitment.
        """
        return _SUPPORT_LEVEL_PRECEDENCE[self]

    @classmethod
    def from_precedence(cls, precedence: int) -> SupportLevel:
        """Look up a `SupportLevel` by its numeric precedence value.

        Raises `ValueError` when the precedence is not recognised.
        """
        for member in cls:
            if _SUPPORT_LEVEL_PRECEDENCE[member] == precedence:
                return member
        valid = ", ".join(f"`{_SUPPORT_LEVEL_PRECEDENCE[m]}`" for m in cls)
        raise ValueError(
            f"Unrecognized support-level precedence: {precedence!r}. "
            f"Expected one of: {valid}."
        ) from None

    @classmethod
    def parse(cls, value: str) -> SupportLevel:
        """Parse a string into a `SupportLevel`.

        Accepts a keyword (`archived`, `community`, `certified`)
        or a legacy integer string (`100`, `200`, `300`).

        Raises `ValueError` when the value is not recognised.
        """
        try:
            return cls(value)
        except ValueError:
            pass
        # Fallback: try interpreting as an integer precedence value.
        try:
            return cls.from_precedence(int(value))
        except (ValueError, KeyError):
            pass
        valid_kw = ", ".join(f"`{m.value}`" for m in cls)
        valid_int = ", ".join(f"`{_SUPPORT_LEVEL_PRECEDENCE[m]}`" for m in cls)
        raise ValueError(
            f"Unrecognized support level: {value!r}. "
            f"Expected keyword ({valid_kw}) or integer ({valid_int})."
        ) from None


class ConnectorType(StrEnum):
    """Connector type: source or destination."""

    SOURCE = "source"
    DESTINATION = "destination"

    @classmethod
    def parse(cls, value: str) -> ConnectorType:
        """Parse a string into a `ConnectorType`, raising `ValueError` on mismatch."""
        try:
            return cls(value)
        except ValueError:
            valid = ", ".join(f"`{m.value}`" for m in cls)
            raise ValueError(
                f"Unrecognized connector type: {value!r}. Expected one of: {valid}."
            ) from None


class ConnectorLanguage(StrEnum):
    """Connector implementation languages."""

    PYTHON = "python"
    JAVA = "java"
    LOW_CODE = "low-code"
    MANIFEST_ONLY = "manifest-only"

    @classmethod
    def parse(cls, value: str) -> ConnectorLanguage:
        """Parse a string into a `ConnectorLanguage`, raising `ValueError` on mismatch."""
        try:
            return cls(value)
        except ValueError:
            valid = ", ".join(f"`{m.value}`" for m in cls)
            raise ValueError(
                f"Unrecognized language: {value!r}. Expected one of: {valid}."
            ) from None


# Internal precedence mapping (kept private; access via SupportLevel.precedence).
_SUPPORT_LEVEL_PRECEDENCE: dict[SupportLevel, int] = {
    SupportLevel.ARCHIVED: 100,
    SupportLevel.COMMUNITY: 200,
    SupportLevel.CERTIFIED: 300,
}
