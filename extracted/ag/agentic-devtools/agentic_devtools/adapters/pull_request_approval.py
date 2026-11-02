"""Provider-neutral pull-request approval adapters."""

from __future__ import annotations

import inspect
import os
import re
from dataclasses import dataclass
from typing import Any, Literal, Protocol

Provider = Literal["azure_devops", "github"]
_SHA40_RE = re.compile(r"[0-9a-f]{40}\Z")
_APPROVER_TOKEN_ENV = "AGDT_PR_APPROVER_PAT"
_SECRET_ENV_VARS = (
    _APPROVER_TOKEN_ENV,
    "GH_TOKEN",
    "GITHUB_TOKEN",
    "AZURE_DEV_OPS_COPILOT_PAT",
    "AZURE_DEVOPS_EXT_PAT",
)


def _sanitize_diagnostic(error: object) -> str:
    """Return a provider-raised diagnostic with credentials removed.

    Mirrors ``agentic_devtools.adapters.pull_request_comments._sanitize_error``:
    redacts any configured credential env-var value found verbatim in the
    message, plus ``Authorization:`` header values, before truncating.
    """
    message = str(error)
    for secret_name in _SECRET_ENV_VARS:
        value = os.environ.get(secret_name, "").strip()
        if value:
            message = message.replace(value, "[REDACTED]")
    message = re.sub(r"(?i)(Authorization:\s*\S+\s+)\S+", r"\1[REDACTED]", message)
    message = re.sub(r"(?i)(['\"]authorization['\"]\s*:\s*['\"]\S+\s+)\S+(['\"])", r"\1[REDACTED]\2", message)
    return message[:1000]


@dataclass(frozen=True)
class PullRequestApprovalRequest:
    """Validated approval request shared by Azure DevOps and GitHub."""

    provider: Provider
    repository: str
    pull_request_id: int
    content: str
    expected_head: str | None = None
    dry_run: bool = False
    organization: str | None = None
    project: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.provider, str) or self.provider not in {"azure_devops", "github"}:
            raise ValueError("provider must be 'azure_devops' or 'github'")
        if not isinstance(self.repository, str) or not self.repository.strip():
            raise ValueError("repository is required")
        object.__setattr__(self, "repository", self.repository.strip())
        if self.provider == "github" and (
            self.repository.count("/") != 1
            or any(not part.strip() or any(char.isspace() for char in part) for part in self.repository.split("/"))
        ):
            raise ValueError("GitHub repository must use owner/repo form")
        if (
            not isinstance(self.pull_request_id, int)
            or isinstance(self.pull_request_id, bool)
            or self.pull_request_id <= 0
        ):
            raise ValueError("pull_request_id must be a positive integer")
        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("content is required")
        if self.provider == "github" and (
            not isinstance(self.expected_head, str) or _SHA40_RE.fullmatch(self.expected_head) is None
        ):
            raise ValueError("expected_head must be a full 40-character lowercase hexadecimal SHA")
        if self.provider == "azure_devops" and self.expected_head is not None:
            raise ValueError(
                "expected_head is not supported for provider 'azure_devops': the Azure "
                "DevOps adapter does not validate the pull-request head before approval, "
                "so a head-pinned approval cannot be guaranteed. Omit expected_head."
            )
        if self.organization is not None and (not isinstance(self.organization, str) or not self.organization.strip()):
            raise ValueError("organization must be a non-empty string or None")
        if self.organization is not None:
            object.__setattr__(self, "organization", self.organization.strip())
        if self.project is not None and (not isinstance(self.project, str) or not self.project.strip()):
            raise ValueError("project must be a non-empty string or None")
        if self.project is not None:
            object.__setattr__(self, "project", self.project.strip())
        if not isinstance(self.dry_run, bool):
            raise ValueError("dry_run must be a boolean")


@dataclass(frozen=True)
class PullRequestApprovalResult:
    """Normalized result of a pull-request approval.

    ``organization``, ``project``, ``repository``, ``pull_request_id``, and
    ``expected_head`` mirror the request's immutable target identity so the
    JSON emitted by concurrent background approvals can be matched back to the
    provider namespace and PR/head it describes, even when multiple approvals
    complete around the same time.
    """

    success: bool
    provider: str
    status: str
    error: str = ""
    verified: bool = False
    external_id: int | None = None
    repository: str = ""
    pull_request_id: int = 0
    expected_head: str | None = None
    operation_kind: str | None = None
    organization: str | None = None
    project: str | None = None

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-serializable result."""
        return {
            "success": self.success,
            "provider": self.provider,
            "status": self.status,
            "error": self.error,
            "verified": self.verified,
            "external_id": self.external_id,
            "repository": self.repository,
            "pull_request_id": self.pull_request_id,
            "expected_head": self.expected_head,
            "operation_kind": self.operation_kind,
            "organization": self.organization,
            "project": self.project,
        }

    @classmethod
    def for_request(
        cls,
        request: PullRequestApprovalRequest,
        success: bool,
        status: str,
        error: str = "",
        verified: bool = False,
        external_id: int | None = None,
        operation_kind: str | None = None,
    ) -> PullRequestApprovalResult:
        """Build a result carrying *request*'s immutable target identity."""
        return cls(
            success,
            request.provider,
            status,
            error,
            verified,
            external_id,
            repository=request.repository,
            pull_request_id=request.pull_request_id,
            expected_head=request.expected_head,
            operation_kind=operation_kind,
            organization=request.organization,
            project=request.project,
        )


class PullRequestApprovalAdapter(Protocol):
    """Transport protocol for provider-specific pull-request approval."""

    def approve(self, request: PullRequestApprovalRequest) -> PullRequestApprovalResult:
        """Approve a pull request."""


class AzureDevOpsPullRequestApprovalAdapter:
    """Delegate approval to the existing Azure DevOps command."""

    provider: Provider = "azure_devops"

    def __init__(self, approve_fn: Any) -> None:
        self._approve_fn = approve_fn

    def approve(self, request: PullRequestApprovalRequest) -> PullRequestApprovalResult:
        if request.provider != self.provider:
            return PullRequestApprovalResult.for_request(request, False, "provider_mismatch")
        if request.dry_run:
            return PullRequestApprovalResult.for_request(request, True, "dry_run")
        try:
            signature = inspect.signature(self._approve_fn)
            params = signature.parameters.values()
            accepts_request = any(
                param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
                for param in params
            ) or any(param.kind is inspect.Parameter.VAR_POSITIONAL for param in params)
            if accepts_request:
                outcome = self._approve_fn(request)
            else:
                outcome = self._approve_fn()
        except Exception as exc:
            return PullRequestApprovalResult.for_request(request, False, "approval_failed", _sanitize_diagnostic(exc))
        # `outcome` is an `AzureApprovalOutcome` when the delegate reports the
        # narrative-vs-fallback distinction; legacy/test doubles that return
        # `None` are treated as a fully resolved narrative update so existing
        # callers keep reporting a plain "approved" result.
        resolved = getattr(outcome, "resolved", True)
        thread_id = getattr(outcome, "thread_id", None)
        operation_kind = getattr(outcome, "operation_kind", None)
        if not resolved:
            # The fallback comment was posted but could not be marked resolved:
            # the documented "resolved approval comment" state was not reached,
            # so this must not be reported as a successful background task.
            return PullRequestApprovalResult.for_request(
                request,
                False,
                "approved_unresolved_thread",
                error="Fallback approval comment was posted but the thread could not be resolved.",
                external_id=thread_id,
                operation_kind=operation_kind,
            )
        return PullRequestApprovalResult.for_request(
            request,
            True,
            "approved",
            verified=True,
            external_id=thread_id,
            operation_kind=operation_kind,
        )


class GitHubPullRequestApprovalAdapter:
    """Delegate approval to the verified, head-pinned GitHub implementation.

    When the default GitHub implementation is used (no ``approve_fn`` override),
    the adapter requires the dedicated ``AGDT_PR_APPROVER_PAT`` identity, because
    GitHub forbids a pull-request author from approving their own pull request.
    The token is passed as ``GH_TOKEN`` in the delegated subprocess environment,
    so the ``gh`` CLI authenticates as the approver identity rather than the ambient
    login without mutating process-wide environment variables.
    """

    provider: Provider = "github"

    def __init__(self, approve_fn: Any | None = None) -> None:
        self._uses_default_approve_fn = approve_fn is None
        if approve_fn is None:
            from agentic_devtools.cli.github.pr_approve import approve_pr

            approve_fn = approve_pr
        self._approve_fn = approve_fn

    def approve(self, request: PullRequestApprovalRequest) -> PullRequestApprovalResult:
        if request.provider != self.provider:
            return PullRequestApprovalResult.for_request(request, False, "provider_mismatch")
        if request.dry_run:
            return PullRequestApprovalResult.for_request(request, True, "dry_run")

        approval_env: dict[str, str] | None = None
        if self._uses_default_approve_fn:
            approver_token = os.environ.get(_APPROVER_TOKEN_ENV, "").strip()
            if not approver_token:
                return PullRequestApprovalResult.for_request(
                    request,
                    False,
                    "missing_approver_identity",
                    f"{_APPROVER_TOKEN_ENV} is not configured. A dedicated approver "
                    "identity is required because GitHub forbids a pull-request author "
                    "from approving their own pull request.",
                )
            approval_env = os.environ.copy()
            approval_env["GH_TOKEN"] = approver_token
            approval_env.pop("GITHUB_TOKEN", None)

        try:
            if self._uses_default_approve_fn:
                result = self._approve_fn(
                    request.pull_request_id,
                    request.repository,
                    request.content,
                    request.expected_head,
                    persist_state=False,
                    env=approval_env,
                )
            else:
                result = self._approve_fn(
                    request.pull_request_id,
                    request.repository,
                    request.content,
                    request.expected_head,
                )
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else 1
            return PullRequestApprovalResult.for_request(
                request,
                False,
                "readiness_failed",
                _sanitize_diagnostic(
                    f"GitHub CLI readiness check failed (exit code {code}); ensure 'gh' is "
                    "installed and authenticated as the approver identity."
                ),
            )
        except Exception as exc:
            return PullRequestApprovalResult.for_request(request, False, "approval_failed", _sanitize_diagnostic(exc))

        if not isinstance(result, dict):
            return PullRequestApprovalResult.for_request(
                request, False, "approval_failed", "GitHub approval returned an invalid result"
            )
        if result.get("approved") is not True:
            raw_status = result.get("error")
            error = _sanitize_diagnostic(result.get("message") or raw_status or "")
            status = (
                raw_status
                if isinstance(raw_status, str)
                and raw_status in {"approval_failed", "head_check_failed", "lookup_failed", "stale_head"}
                else "approval_failed"
            )
            return PullRequestApprovalResult.for_request(request, False, status, error)
        verified = result.get("verified") is True
        # The delegate reports "status": "already_approved" when an existing
        # APPROVED review for this PR/head/identity was found and reused
        # instead of submitting a duplicate review, so retries and reruns
        # stay idempotent (see #4025).
        status = (
            "already_approved"
            if verified and result.get("status") == "already_approved"
            else "approved"
            if verified
            else "submitted_unverified"
        )
        review_id = result.get("reviewId")
        external_id = (
            review_id if isinstance(review_id, int) and not isinstance(review_id, bool) and review_id > 0 else None
        )
        # An inconclusive verification must not be reported as a verified success:
        # the review was submitted, but we cannot confirm it registered against the
        # intended PR/head/identity, so callers must not treat this as approved.
        return PullRequestApprovalResult.for_request(
            request,
            verified,
            status,
            error="" if verified else "GitHub approval was submitted but could not be verified.",
            verified=verified,
            external_id=external_id,
        )
