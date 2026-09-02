"""Exception hierarchy for issue adapters.

Provides a minimal exception tree for adapter-level errors:

- :class:`AdapterError` — base class for all adapter exceptions.
- :class:`AdapterValidationError` — raised when identity field validation
  fails during :class:`~agentic_devtools.adapters.types.NormalizedIssue`
  construction, or when a provider rejects an unsupported issue type or
  parent-child hierarchy pair.
- :class:`HierarchyLinkError` — raised when an issue was created successfully
  but a subsequent hierarchy-link step failed, leaving a partially-created
  result.
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
    """Raised when issue creation succeeded but hierarchy linkage failed.

    Signals a *partial* creation: the provider confirmed the child issue was
    created, but a subsequent post-create hierarchy-link call (for example
    GitHub's ``POST .../sub_issues``) failed.  Callers can capture the
    ``created_result`` as a ``partial-created`` descriptor before failing
    closed.

    Only providers that establish hierarchy links in a *separate* step after
    creation (currently GitHub) raise this error.  Providers that embed the
    parent in the creation request itself (Jira) propagate their ordinary
    creation exception instead, because no partial creation can be confirmed.

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
