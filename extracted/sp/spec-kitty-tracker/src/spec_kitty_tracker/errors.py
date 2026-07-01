from __future__ import annotations

from enum import StrEnum


class SpecKittyTrackerError(Exception):
    """Base exception for spec-kitty-tracker."""


class ConnectorConfigError(SpecKittyTrackerError):
    """Raised when connector configuration is invalid."""


class CapabilityNotSupportedError(SpecKittyTrackerError):
    """Raised when invoking an unsupported connector feature."""


class IssueNotFoundError(SpecKittyTrackerError):
    """Raised when the requested issue cannot be found."""


class SyncConflictError(SpecKittyTrackerError):
    """Raised when strict sync conflict handling blocks execution."""


class DiscoveryContractError(SpecKittyTrackerError):
    """Raised when a provider adapter returns discovery data that violates
    the hybrid metadata contract.

    This is a contract failure, not a transport, authentication, or parse
    failure. Hosts and contract tests can catch it independently of
    ConnectorRequestError to distinguish "the provider returned malformed
    discovery data" from ordinary request errors.

    Attributes:
        provider: Provider slug ("linear", "jira", "github", "gitlab") or None.
        kind: One of "workspace", "resource", "result" — what kind of object
            the violation was found on.
        field_path: Dotted path to the offending field, e.g.
            "provider_context.workspace_handle" or "items[3].stable_ref".
        reason: Short rule code from contracts/discovery-contract.md §4
            (e.g. "WS-008", "RS-011", "DR-002").
    """

    def __init__(
        self,
        message: str,
        *,
        provider: str | None = None,
        kind: str | None = None,
        field_path: str | None = None,
        reason: str | None = None,
    ) -> None:
        super().__init__(message)
        self.provider = provider
        self.kind = kind
        self.field_path = field_path
        self.reason = reason


class FailureClass(StrEnum):
    """Canonical failure classification used by retry orchestration."""

    TRANSIENT = "transient"
    RATE_LIMIT = "rate_limit"
    AUTHENTICATION = "authentication"
    PERMISSION = "permission"
    NOT_FOUND = "not_found"
    VALIDATION = "validation"
    NON_RETRYABLE = "non_retryable"


def classify_http_status(status_code: int) -> FailureClass:
    """Map HTTP status codes to deterministic retry classes."""

    if status_code == 429:
        return FailureClass.RATE_LIMIT
    if status_code in {408, 425, 500, 502, 503, 504}:
        return FailureClass.TRANSIENT
    if status_code == 401:
        return FailureClass.AUTHENTICATION
    if status_code == 403:
        return FailureClass.PERMISSION
    if status_code == 404:
        return FailureClass.NOT_FOUND
    if status_code in {400, 409, 422}:
        return FailureClass.VALIDATION
    return FailureClass.NON_RETRYABLE


class ConnectorRequestError(SpecKittyTrackerError):
    """Raised when upstream tracker API request fails."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        failure_class: FailureClass | None = None,
        retry_after_seconds: int | None = None,
        provider: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.failure_class = (
            failure_class
            if failure_class is not None
            else (
                classify_http_status(status_code)
                if status_code is not None
                else FailureClass.NON_RETRYABLE
            )
        )
        self.retry_after_seconds = retry_after_seconds
        self.provider = provider

    @property
    def is_retryable(self) -> bool:
        return self.failure_class in {FailureClass.TRANSIENT, FailureClass.RATE_LIMIT}
