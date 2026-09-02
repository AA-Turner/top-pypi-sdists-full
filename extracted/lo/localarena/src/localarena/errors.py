"""Exception hierarchy for explicit live-provider operations."""

from __future__ import annotations


class LocalArenaError(Exception):
    """Base class for LocalArena errors outside the deterministic core."""


class ProviderError(LocalArenaError):
    """Base class for sanitized provider failures."""

    def __init__(
        self,
        message: str,
        *,
        provider: str,
        status_code: int | None = None,
        retryable: bool = False,
        attempts: int = 1,
    ) -> None:
        self.provider = provider
        self.status_code = status_code
        self.retryable = retryable
        self.attempts = attempts
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.provider}: {self.args[0]}"


class ProviderConfigurationError(ProviderError):
    """A provider could not be configured safely."""


class ProviderConnectionError(ProviderError):
    """The configured provider could not be reached."""


class ProviderTimeoutError(ProviderConnectionError):
    """The configured provider did not respond within the timeout."""


class ProviderAuthError(ProviderError):
    """The provider rejected the configured credentials."""


class ProviderRateLimitError(ProviderError):
    """The provider rejected a request due to rate limiting."""


class ProviderResponseError(ProviderError):
    """The provider returned an invalid or unsuccessful response."""


class JudgeParseError(LocalArenaError):
    """A judge response could not be reduced to a valid arena result."""
