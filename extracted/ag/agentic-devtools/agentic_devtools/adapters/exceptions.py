"""Exception hierarchy for issue adapters.

Provides a minimal exception tree for adapter-level errors:

- :class:`AdapterError` — base class for all adapter exceptions.
- :class:`AdapterValidationError` — raised when identity field validation
  fails during :class:`~agentic_devtools.adapters.types.NormalizedIssue`
  construction, or when a provider rejects an unsupported issue type or
  parent-child hierarchy pair.
- :class:`HierarchyLinkError` — raised when an issue is confirmed but a
  subsequent hierarchy-link step failed, leaving a partial result.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agentic_devtools.adapters.issue_provider import ProviderIssueResult


class AdapterError(Exception):
    """Base exception for all issue adapter errors."""


class AdapterValidationError(AdapterError):
    """Raised when adapter identity field validation fails.

    Typically triggered during :class:`NormalizedIssue` construction when
    required identity fields (``issue_id``, ``title``, ``url``, ``provider``)
    are ``None``, empty, or whitespace-only.  Also raised by the
    ``HierarchyValidationProvider`` companion capability when a provider is
    asked to validate an unsupported issue type or an impermissible
    parent-child hierarchy pair.
    """


class HierarchyLinkError(AdapterError):
    """Raised when an issue is confirmed but required hierarchy linkage fails.

    Signals a partial operation: the provider confirmed the child issue exists,
    but a subsequent create-time or recovery hierarchy-link call failed.
    Callers can capture the ``created_result`` before failing closed.

    This applies both when a provider creates the issue before linking and when
    it recovers a confirmed issue whose parent link must be reconciled.

    Attributes:
        created_result: The :class:`ProviderIssueResult` for the issue that was
            successfully created before the link step failed.
        stage: A short machine-readable label for the failing stage (for
            example ``"link_subissue"``).
        cause: The underlying exception that caused the link failure.
    """

    def __init__(
        self,
        message: str,
        *,
        created_result: ProviderIssueResult,
        stage: str,
        cause: Exception,
    ) -> None:
        super().__init__(message)
        self.created_result: ProviderIssueResult = created_result
        self.stage: str = stage
        self.cause: Exception = cause
