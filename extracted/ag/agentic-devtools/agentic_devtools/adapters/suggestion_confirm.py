"""Provider-neutral adapters for confirming addressed pull-request suggestions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from agentic_devtools.adapters.base import PullRequestThreadReplyRequest, is_valid_github_repository
from agentic_devtools.adapters.exceptions import AdapterValidationError
from agentic_devtools.adapters.pull_request_threads import _GITHUB_THREAD_ID
from agentic_devtools.cli.azure_devops.auth import get_auth_headers, get_pat
from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.helpers import get_repository_id, require_requests, resolve_thread_by_id


@dataclass(frozen=True)
class SuggestionConfirmationRequest:
    """Validated request to reply to and resolve one review suggestion."""

    provider: Literal["azure_devops", "github"]
    repository: str
    pull_request_id: int
    discussion_id: int | str
    commit_hash: str
    review_thread_id: str | None = None
    dry_run: bool = False
    organization: str | None = None
    project: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.provider, str) or self.provider not in ("azure_devops", "github"):
            raise AdapterValidationError("provider must be 'azure_devops' or 'github'")
        if not isinstance(self.repository, str) or not self.repository.strip():
            raise AdapterValidationError("repository is required")
        if (
            not isinstance(self.pull_request_id, int)
            or isinstance(self.pull_request_id, bool)
            or self.pull_request_id <= 0
        ):
            raise AdapterValidationError("pull_request_id must be a positive integer")
        if not isinstance(self.commit_hash, str) or not self.commit_hash.strip():
            raise AdapterValidationError("commit_hash is required")
        object.__setattr__(self, "commit_hash", self.commit_hash.strip())
        if (
            isinstance(self.discussion_id, bool)
            or not str(self.discussion_id).isdigit()
            or int(self.discussion_id) <= 0
        ):
            raise AdapterValidationError("discussion_id must be a positive integer")
        if self.provider == "github":
            if not is_valid_github_repository(self.repository):
                raise AdapterValidationError("GitHub repository must be in owner/repo form")
            if not isinstance(self.review_thread_id, str) or not self.review_thread_id.strip():
                raise AdapterValidationError("review_thread_id is required for GitHub")
            if not _GITHUB_THREAD_ID.fullmatch(self.review_thread_id):
                raise AdapterValidationError("review_thread_id must be an opaque PRRT_ GraphQL node ID")
        if not isinstance(self.dry_run, bool):
            raise AdapterValidationError("dry_run must be a boolean")
        for name in ("organization", "project"):
            value = getattr(self, name)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise AdapterValidationError(f"{name} must be a non-empty string when provided")
        if self.provider == "azure_devops" and ((self.organization is None) != (self.project is None)):
            raise AdapterValidationError("organization and project must be provided together for Azure DevOps")


@dataclass(frozen=True)
class SuggestionConfirmationResult:
    """Normalized result of a suggestion confirmation."""

    success: bool
    provider: str
    status: str
    reply_id: int | str | None = None
    diagnostics: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-serializable result."""
        return {
            "success": self.success,
            "provider": self.provider,
            "status": self.status,
            "reply_id": self.reply_id,
            "diagnostics": list(self.diagnostics),
        }


class SuggestionConfirmationAdapter:
    """Confirm a suggestion using the selected code-hosting provider."""

    def __init__(
        self,
        *,
        requests_module: Any | None = None,
        azure_config: AzureDevOpsConfig | None = None,
        pat: str | None = None,
    ) -> None:
        self._requests = requests_module
        self._azure_config = azure_config
        self._pat = pat

    def _sanitize_diagnostic(self, message: object) -> str:
        from agentic_devtools.cli.pull_request_thread import _sanitize_diagnostic

        diagnostic = _sanitize_diagnostic(message)
        diagnostic = diagnostic.replace(self._pat, "[redacted]") if self._pat else diagnostic
        return diagnostic[:1000]

    def confirm(self, request: SuggestionConfirmationRequest) -> SuggestionConfirmationResult:
        """Post the confirmation reply and resolve the review discussion."""
        if request.dry_run:
            return SuggestionConfirmationResult(True, request.provider, "dry_run")
        try:
            if request.provider == "github":
                from agentic_devtools.cli.pull_request_thread import reply_to_pull_request_thread

                reply_request = PullRequestThreadReplyRequest(
                    provider="github",
                    repository=request.repository,
                    pull_request_number=request.pull_request_id,
                    discussion_id=request.discussion_id,
                    body=f"✅ Suggestion addressed in commit `{request.commit_hash[:7]}`.",
                    resolve=True,
                    review_thread_id=request.review_thread_id,
                    dry_run=False,
                )
                result = reply_to_pull_request_thread(reply_request)
                if not result.mutation_status == "replied_and_resolved":
                    return SuggestionConfirmationResult(
                        False, request.provider, result.mutation_status, result.reply_id, result.diagnostics
                    )
                return SuggestionConfirmationResult(True, request.provider, result.mutation_status, result.reply_id)

            if self._azure_config is not None:
                config = AzureDevOpsConfig(
                    organization=self._azure_config.organization,
                    project=self._azure_config.project,
                    repository=request.repository,
                )
            elif request.organization and request.project:
                config = AzureDevOpsConfig(
                    organization=request.organization,
                    project=request.project,
                    repository=request.repository,
                )
            else:
                state_config = AzureDevOpsConfig.from_state()
                config = AzureDevOpsConfig(
                    organization=state_config.organization,
                    project=state_config.project,
                    repository=request.repository,
                )
            requests_module = self._requests or require_requests()
            pat = self._pat if self._pat is not None else get_pat()
            headers = get_auth_headers(pat)
            repo_id = get_repository_id(
                config.organization,
                config.project,
                config.repository,
                requests_module=requests_module,
                pat=pat,
            )
            url = config.build_api_url(
                repo_id, "pullRequests", request.pull_request_id, "threads", int(request.discussion_id), "comments"
            )
            response = requests_module.post(
                url,
                headers=headers,
                json={
                    "content": f"✅ Suggestion addressed in commit `{request.commit_hash[:7]}`.",
                    "commentType": "text",
                },
                timeout=30,
            )
            response.raise_for_status()
            try:
                payload = response.json()
            except ValueError as exc:
                return SuggestionConfirmationResult(
                    False,
                    request.provider,
                    "partial_success",
                    None,
                    diagnostics=(
                        self._sanitize_diagnostic(f"Reply posted but response payload was not valid JSON: {exc}"),
                    ),
                )
            reply_id = payload.get("id") if isinstance(payload, dict) else None
            if isinstance(reply_id, bool) or not isinstance(reply_id, int) or reply_id <= 0:
                return SuggestionConfirmationResult(
                    False,
                    request.provider,
                    "partial_success",
                    None,
                    diagnostics=("Reply posted but response did not include a valid positive integer id",),
                )
            try:
                resolve_thread_by_id(
                    requests_module,
                    headers,
                    config,
                    repo_id,
                    request.pull_request_id,
                    int(request.discussion_id),
                    status="closed",
                )
            except Exception as exc:
                return SuggestionConfirmationResult(
                    False,
                    request.provider,
                    "partial_success",
                    reply_id,
                    diagnostics=(self._sanitize_diagnostic(f"Reply posted but resolution failed: {exc}"),),
                )
            return SuggestionConfirmationResult(True, request.provider, "replied_and_resolved", reply_id)
        except Exception as exc:
            return SuggestionConfirmationResult(
                False, request.provider, "failed", diagnostics=(self._sanitize_diagnostic(exc),)
            )


__all__ = ["SuggestionConfirmationAdapter", "SuggestionConfirmationRequest", "SuggestionConfirmationResult"]
