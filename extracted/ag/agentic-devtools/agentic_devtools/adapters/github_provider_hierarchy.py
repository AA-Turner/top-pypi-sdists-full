"""GitHub issue hierarchy and parent-link operations."""

from __future__ import annotations

import json

from agentic_devtools.adapters.exceptions import AdapterValidationError, HierarchyLinkError
from agentic_devtools.adapters.github_provider_common import (
    _NOT_FOUND_RE,
    _detect_transient,
    _GitHubProviderCommonMixin,
)
from agentic_devtools.adapters.github_provider_issue_types import _ISSUE_TYPE_LABELS, _UNSUPPORTED_TYPES
from agentic_devtools.adapters.issue_provider import ProviderIssueResult, ProviderLinkResult, check_hierarchy_pair
from agentic_devtools.adapters.retry import retry_on_transient


# The facade composes sibling mixins supplying the intentionally ignored members below.
class GitHubProviderCreationHierarchyMixin(_GitHubProviderCommonMixin):
    def _link_created_issue(
        self,
        issue_result: ProviderIssueResult,
        parent_id: str | None,
        *,
        newly_created: bool,
        error_result: ProviderIssueResult | None = None,
    ) -> ProviderIssueResult:
        """Link an issue to a parent and preserve the partial-creation error contract."""
        if parent_id is None:
            return issue_result
        try:
            link_result = self.link_subissue(  # type: ignore[attr-defined]
                parent_id, issue_result.identifier, dry_run=False
            )
        except Exception as link_exc:
            outcome = "was created" if newly_created else "already exists"
            raise HierarchyLinkError(
                f"Issue #{issue_result.identifier} {outcome} at {issue_result.url} but "
                f"sub-issue linking to parent #{parent_id} failed "
                "(see chained exception for details)",
                created_result=error_result if error_result is not None else issue_result,
                stage="link_subissue",
                cause=link_exc,
            ) from link_exc
        return ProviderIssueResult(
            identifier=issue_result.identifier,
            url=issue_result.url,
            status=issue_result.status,
            metadata=issue_result.metadata,
            hierarchy_link_result=link_result,
        )


class GitHubProviderHierarchyMixin(_GitHubProviderCommonMixin):
    @retry_on_transient
    def link_subissue(
        self,
        parent_id: str,
        child_id: str,
        *,
        dry_run: bool = False,
    ) -> ProviderLinkResult:
        """Link a child issue to a parent using the GitHub Sub-Issues API.

        ``parent_id`` and ``child_id`` are GitHub issue *numbers*.  The child
        number is resolved to its integer database ID before calling
        ``POST /repos/{owner}/{repo}/issues/{number}/sub_issues`` with
        ``sub_issue_id``.  The returned ``target_id`` is the child issue number
        (the domain identifier), not the internal database ID.

        Idempotent: returns ``status="already-linked"`` when the child is
        already listed as a sub-issue of the parent without issuing a POST.
        """
        parent_id = self._normalize_issue_number(parent_id, "parent_id")
        child_id = self._normalize_issue_number(child_id, "child_id")

        if dry_run:
            entry = {
                "source": parent_id,
                "target": child_id,
                "type": "sub-issue",
                "operation": f"POST /repos/{self._owner_repo}/issues/{parent_id}/sub_issues",
                "status": "dry-run",
            }
            self._dry_run_deps.append(entry)
            return ProviderLinkResult(
                source_id=parent_id,
                target_id=child_id,
                status="dry-run",
            )

        # Resolve the child issue number to its integer database ID, which the
        # sub-issues API requires as ``sub_issue_id``.  Call the inner helper
        # directly (no retry decorator) so this retry-decorated method does not
        # amplify retries across nested layers.  Raises ``ValueError`` on 404
        # (translated inside _resolve_identifier_inner).
        resolved = self._resolve_identifier_inner(child_id)  # type: ignore[attr-defined]
        sub_issue_id = resolved.metadata["database_id"]  # validated positive int by _resolve_identifier_inner

        # Idempotency check: GET the parent's existing sub-issues and return
        # early if the child is already linked.  Raises ``ValueError`` when the
        # parent issue is not found (translated inside _find_existing_sub_issue).
        existing = self._find_existing_sub_issue(parent_id, sub_issue_id)
        if existing:
            return ProviderLinkResult(
                source_id=parent_id,
                target_id=child_id,
                status="already-linked",
            )

        payload = {"sub_issue_id": sub_issue_id}
        args = [
            "gh",
            "api",
            f"/repos/{self._owner_repo}/issues/{parent_id}/sub_issues",
            "--method",
            "POST",
            "--input",
            "-",
        ]
        result = self._run(
            args,
            capture_output=True,
            text=True,
            shell=False,
            input=json.dumps(payload),
        )
        if result.returncode != 0:
            stderr = result.stderr or ""
            if "404" in stderr or "422" in stderr:
                raise RuntimeError(
                    f"Sub-issues API not available or invalid request for "
                    f"{self._owner_repo}: {stderr}. "
                    f"Ensure the repository has sub-issues enabled."
                )
            _detect_transient(stderr)
            raise RuntimeError(f"Failed to link sub-issue: {stderr}")

        return ProviderLinkResult(
            source_id=parent_id,
            target_id=child_id,
            status="linked",
        )

    def _find_existing_sub_issue(self, parent_id: str, child_db_id: int) -> bool:
        """Return whether the child's database ID is already linked to the parent.

        Propagates malformed responses and non-404 failures rather than failing
        open, which could create a duplicate relationship; translates 404 to
        ``ValueError`` for the consistent :meth:`link_subissue` contract.
        """
        args = [
            "gh",
            "api",
            f"/repos/{self._owner_repo}/issues/{parent_id}/sub_issues",
            "--method",
            "GET",
            "-f",
            "per_page=100",
        ]
        try:
            result = self._exec_gh(args)
        except RuntimeError as exc:
            if _NOT_FOUND_RE.search(str(exc)):
                raise ValueError(f"Parent issue {parent_id!r} not found") from exc
            raise
        items = self._parse_json(result.stdout)
        if not isinstance(items, list):
            raise RuntimeError("Expected sub-issues list response from GitHub sub_issues endpoint.")
        for item in items:
            if isinstance(item, dict) and item.get("id") == child_db_id:
                return True
        return False

    def validate_issue_type(self, issue_type: str) -> None:
        """Validate an issue type against GitHub's label mapping.

        Rejects unmapped types and the non-canonical ``sub-task`` spelling that
        GitHub cannot represent, raising a shared adapter-layer validation
        exception rather than a provider-specific one.

        Raises:
            AdapterValidationError: If the type has no GitHub label mapping.
        """
        if not isinstance(issue_type, str) or not issue_type.strip():
            raise AdapterValidationError("issue_type must be a non-empty string")
        type_lower = issue_type.lower().strip()
        if type_lower in _UNSUPPORTED_TYPES or type_lower not in _ISSUE_TYPE_LABELS:
            raise AdapterValidationError(
                f"Issue type '{issue_type}' has no GitHub label mapping. "
                f"Supported types: {list(_ISSUE_TYPE_LABELS.keys())}"
            )

    def validate_hierarchy_pair(self, child_type: str, parent_type: str) -> None:
        """Validate a parent-child issue-type pair for GitHub.

        Raises:
            AdapterValidationError: If either type is unsupported or the pair is
                not a permitted parent-above-child combination.
        """
        self.validate_issue_type(child_type)
        self.validate_issue_type(parent_type)
        check_hierarchy_pair(child_type, parent_type)
