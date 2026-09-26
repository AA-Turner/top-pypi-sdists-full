from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from ._model import Consent


class ConsentParseError(Exception):
    """An error raised if consent parsing/loading fails."""

    def __init__(self, message: str, raw_consent: dict[str, t.Any]) -> None:
        super().__init__(message)
        self.message = message
        self.raw_consent = raw_consent

    def __str__(self) -> str:
        return self.message

    def __reduce__(self) -> tuple[type, tuple[str, dict[str, t.Any]]]:
        return (ConsentParseError, (self.message, self.raw_consent))


class ConsentTreeConstructionError(Exception):
    """An error raised if consent tree construction fails."""

    def __init__(self, message: str, consents: list[Consent]) -> None:
        super().__init__(message)
        self.message = message
        self.consents = consents

    def __str__(self) -> str:
        return self.message

    def __reduce__(self) -> tuple[type, tuple[str, list[Consent]]]:
        return (ConsentTreeConstructionError, (self.message, self.consents))
