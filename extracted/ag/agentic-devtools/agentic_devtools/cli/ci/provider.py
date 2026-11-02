"""CI platform provider abstraction and stable public imports."""

from __future__ import annotations

from agentic_devtools.cli.ci.provider_audit import _ProviderAuditMixin
from agentic_devtools.cli.ci.provider_audit_dispatch import _ProviderAuditDispatchMixin
from agentic_devtools.cli.ci.provider_comments import _ProviderCommentsMixin
from agentic_devtools.cli.ci.provider_deferrals import _ProviderDeferralsMixin
from agentic_devtools.cli.ci.provider_diff import _ProviderDiffMixin
from agentic_devtools.cli.ci.provider_events import _ProviderEventsMixin
from agentic_devtools.cli.ci.provider_issue_inventory import _ProviderIssueInventoryMixin
from agentic_devtools.cli.ci.provider_issue_mutations import _ProviderIssueMutationsMixin
from agentic_devtools.cli.ci.provider_pr_lifecycle import _ProviderPrLifecycleMixin
from agentic_devtools.cli.ci.provider_repair_dispatch import _ProviderRepairDispatchMixin
from agentic_devtools.cli.ci.provider_repository import _ProviderRepositoryMixin
from agentic_devtools.cli.ci.provider_reviews import _ProviderReviewsMixin
from agentic_devtools.cli.ci.provider_scheduler import _ProviderSchedulerMixin
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class RepairDispatchNotAttemptedError(RuntimeError):
    """A repair dispatch failure known to have occurred before any creation request."""


class RepairDispatchBookkeepingRateLimitError(ProviderRateLimitError):
    """A bookkeeping quota pause after confirmed repair creation, retaining its receipt."""

    def __init__(self, receipt: int | str, error: ProviderRateLimitError) -> None:
        super().__init__(
            retry_after_seconds=error.retry_after_seconds,
            reset_timestamp=error.reset_timestamp,
            remaining=error.remaining,
            provider=error.provider,
            credential_identity=error.credential_identity,
            source=error.source,
            is_rate_limit=error.is_rate_limit,
        )
        self.receipt = receipt


class CIPlatformProvider(
    _ProviderEventsMixin,
    _ProviderCommentsMixin,
    _ProviderPrLifecycleMixin,
    _ProviderRepairDispatchMixin,
    _ProviderReviewsMixin,
    _ProviderDiffMixin,
    _ProviderRepositoryMixin,
    _ProviderSchedulerMixin,
    _ProviderAuditMixin,
    _ProviderAuditDispatchMixin,
    _ProviderDeferralsMixin,
    _ProviderIssueInventoryMixin,
    _ProviderIssueMutationsMixin,
):
    """Abstract base class for CI platform providers.

    Concrete implementations translate platform-specific APIs into a
    unified interface consumed by the orchestrator and guard modules.
    """


def trusted_loop_comment_logins(provider: CIPlatformProvider) -> set[str]:
    """Resolve trusted comment authors, retaining compatibility with older providers."""
    getter = getattr(provider, "get_trusted_loop_comment_logins", None)
    if callable(getter):
        logins = getter()
        if isinstance(logins, (set, frozenset)) and all(isinstance(login, str) for login in logins):
            return {login.casefold() for login in logins if login.strip()}
    login = provider.get_pr_token_login()
    return {login.casefold()} if isinstance(login, str) and login.strip() else set()
