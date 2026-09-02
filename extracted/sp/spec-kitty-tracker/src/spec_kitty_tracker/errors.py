from __future__ import annotations

from enum import StrEnum
from typing import Final


class SpecKittyTrackerError(Exception):
    """Base exception for spec-kitty-tracker."""


class ConnectorConfigError(SpecKittyTrackerError):
    """Raised when connector configuration is invalid."""


class CapabilityNotSupportedError(SpecKittyTrackerError):
    """Raised when invoking an unsupported connector feature.

    ``capability`` optionally names the specific capability that was refused
    (e.g. ``"status"`` for a Jira status-transition refusal) so orchestration
    can distinguish it from unrelated capability gaps. Defaults to ``None`` so
    existing raisers are unaffected.
    """

    def __init__(self, message: str, *, capability: str | None = None) -> None:
        super().__init__(message)
        self.capability = capability


STATUS_TRANSITION_CAPABILITY: Final = "status"


def is_status_transition_refusal(exc: CapabilityNotSupportedError) -> bool:
    """True iff ``exc`` is a Jira status-transition refusal (vs. any other capability gap)."""
    return exc.capability == STATUS_TRANSITION_CAPABILITY


class IssueNotFoundError(SpecKittyTrackerError):
    """Raised when the requested issue cannot be found."""


class SyncConflictError(SpecKittyTrackerError):
    """Raised when strict sync conflict handling blocks execution."""


class TrackerContractError(SpecKittyTrackerError):
    """Raised when a tracker payload violates a typed public contract.

    This is a contract failure, not a transport, authentication, or
    not-found failure — hosts and contract tests can catch it independently
    of ConnectorRequestError to distinguish "the payload violates the
    tracker's contract" from ordinary request errors. It is the common base
    for every contract-violation subclass (TRK-M1-01 draft A7).

    Attributes:
        provider: Provider slug (e.g. "linear", "beads") or None.
        kind: What kind of object the violation was found on (e.g.
            "workspace", "resource", "result", "issue", "patch").
        field_path: Dotted/bracketed path to the offending field, e.g.
            "provider_context.workspace_handle" or "decision_refs[0].decision_id".
        reason: Short rule code identifying the exact violated rule (e.g.
            "WS-008", "PK-001", "BD-003", "DR-002").
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


class DiscoveryContractError(TrackerContractError):
    """Raised when a provider adapter returns discovery data that violates
    the hybrid metadata contract.

    Re-parented under :class:`TrackerContractError` (TRK-M1-01 draft A7);
    this changes no attribute, no raise site, and no reason-code vocabulary.
    Every pre-existing ``isinstance(exc, SpecKittyTrackerError)`` check keeps
    passing via the MRO (DiscoveryContractError -> TrackerContractError ->
    SpecKittyTrackerError).

    See :class:`TrackerContractError` for the attribute contract
    (``provider``, ``kind``, ``field_path``, ``reason``). Reason codes come
    from contracts/discovery-contract.md §4 (e.g. "WS-008", "RS-011",
    "DR-002").
    """


class IssuePayloadContractError(TrackerContractError):
    """Raised when a canonical issue/patch payload violates its contract.

    Covers, e.g., unknown patch keys (reason "PK-*") and malformed
    provider-native issue payloads (reason "BD-*"). Production raise sites
    across connectors/engine egress paths are TRK-M1-03 (A6, A8); this type
    is owned by TRK-M1-02.
    """


class DecisionReferenceContractError(TrackerContractError):
    """Raised when a mission decision-reference payload violates its contract.

    Covers malformed ``custom_fields.decision_refs`` entries (reason
    "DR-001"/"DR-002") during strict parsing. Production raise sites are
    TRK-M1-03 (A13); this type is owned by TRK-M1-02.
    """


class ScopeViolationError(SpecKittyTrackerError):
    """Raised when a local/native connector call crosses its declared scope.

    Not a :class:`TrackerContractError` — a cross-scope call is a trust/
    authorization failure, not a payload-shape violation. Production raise
    sites are host territory (TRK-M1-04/05; TRK-M1-06 N7).

    Attributes:
        expected_scope: The scope (e.g. repository name) the caller's
            context declared.
        actual_scope: The scope the call actually resolved against.
    """

    def __init__(
        self,
        message: str,
        *,
        expected_scope: str | None = None,
        actual_scope: str | None = None,
    ) -> None:
        super().__init__(message)
        self.expected_scope = expected_scope
        self.actual_scope = actual_scope


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


class HostedAuthRequiredError(ConnectorRequestError):
    """Raised when a hosted connector call fails because hosted auth is missing.

    Mission ``tracker-readiness-alignment-01KS7PZ7`` (WS5, issue
    ``Priivacy-ai/spec-kitty-tracker#18``).

    This is a typed subclass of :class:`ConnectorRequestError` so the CLI
    can pattern-match on type (``except HostedAuthRequiredError as exc:``)
    and route the failure through the shared readiness language without
    having to inspect ``failure_class`` or rely on string matching.

    ``failure_class`` is forced to :attr:`FailureClass.AUTHENTICATION`
    regardless of the supplied ``status_code`` so the typed envelope is
    self-consistent.  ``status_code`` defaults to ``401`` because that is
    the canonical HTTP value for missing/invalid hosted auth, but callers
    MAY override (e.g. when the SaaS control plane returns ``403`` for an
    auth token that is present but lacks the team membership scope).

    Consumers SHOULD NOT instantiate this error for non-hosted (local)
    connectors.  Local connectors handle their own credential prompts;
    raising this from a local code path would mislead the CLI into
    rendering the hosted-auth remediation.
    """

    def __init__(
        self,
        message: str = "Hosted tracker authentication is required.",
        *,
        status_code: int | None = 401,
        retry_after_seconds: int | None = None,
        provider: str | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=status_code,
            failure_class=FailureClass.AUTHENTICATION,
            retry_after_seconds=retry_after_seconds,
            provider=provider,
        )
