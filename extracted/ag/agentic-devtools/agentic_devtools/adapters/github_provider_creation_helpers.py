"""Shared preparation and result helpers for GitHub issue creation."""

from __future__ import annotations

from dataclasses import dataclass

from agentic_devtools.adapters.github_provider_common import _GitHubProviderCommonMixin
from agentic_devtools.adapters.github_provider_issue_types import _ISSUE_TYPE_LABELS, _UNSUPPORTED_TYPES
from agentic_devtools.adapters.issue_provider import DefinitiveCreationFailure, PreCreateLookup, ProviderIssueResult
from agentic_devtools.adapters.orchestration_key import (
    embed_orchestration_key,
    extract_orchestration_key,
    normalize_orchestration_key,
)


@dataclass(frozen=True)
class _IssueCreationContext:
    title: str
    body: str
    issue_type: str
    operation: str
    parent_id: str | None
    type_label: str
    orchestration_key: str | None
    lookup_key: str
    precreate_lookup: PreCreateLookup | None


# The facade composes sibling mixins supplying the intentionally ignored members below.
class _GitHubProviderCreationHelpersMixin(_GitHubProviderCommonMixin):
    def _prepare_creation_context(
        self,
        title: str,
        body: str,
        issue_type: str,
        parent_id: str | None,
        idempotency_key: str | None,
        precreate_lookup: PreCreateLookup | None,
    ) -> _IssueCreationContext:
        operation = f"POST /repos/{self._owner_repo}/issues"
        lookup_orchestration_key = idempotency_key
        self._validate_precreate_lookup(precreate_lookup, idempotency_key)  # type: ignore[attr-defined]
        self._validate_creation_title(title)
        normalized_parent_id = self._normalize_creation_parent(parent_id)
        type_label = self._resolve_creation_type(issue_type)
        body, idempotency_key = self._embed_creation_key(body, idempotency_key)
        orchestration_key = idempotency_key or extract_orchestration_key(body)
        lookup_key = lookup_orchestration_key or orchestration_key or ""
        return _IssueCreationContext(
            title=title,
            body=body,
            issue_type=issue_type,
            operation=operation,
            parent_id=normalized_parent_id,
            type_label=type_label,
            orchestration_key=orchestration_key,
            lookup_key=lookup_key,
            precreate_lookup=precreate_lookup,
        )

    @staticmethod
    def _validate_creation_title(title: str) -> None:
        if not isinstance(title, str) or not title.strip():
            raise DefinitiveCreationFailure("title must be a non-empty string")

    def _normalize_creation_parent(self, parent_id: str | None) -> str | None:
        if parent_id is None:
            return None
        try:
            return self._normalize_issue_number(parent_id, "parent_id")
        except (ValueError, AttributeError, TypeError) as exc:
            raise DefinitiveCreationFailure(str(exc)) from exc

    @staticmethod
    def _resolve_creation_type(issue_type: str) -> str:
        if not isinstance(issue_type, str) or not issue_type.strip():
            raise DefinitiveCreationFailure("issue_type must be a non-empty string")
        type_lower = issue_type.lower()
        if type_lower in _UNSUPPORTED_TYPES:
            raise DefinitiveCreationFailure(
                f"Issue type '{issue_type}' cannot be mapped to a GitHub label. "
                f"GitHub does not support native sub-task types. "
                f"Supported types: {list(_ISSUE_TYPE_LABELS.keys())}"
            )
        if type_lower not in _ISSUE_TYPE_LABELS:
            raise DefinitiveCreationFailure(
                f"Issue type '{issue_type}' has no GitHub label mapping. "
                f"Supported types: {list(_ISSUE_TYPE_LABELS.keys())}"
            )
        return _ISSUE_TYPE_LABELS[type_lower]

    @staticmethod
    def _embed_creation_key(body: str, idempotency_key: str | None) -> tuple[str, str | None]:
        if not idempotency_key:
            return body, idempotency_key
        normalized_key = normalize_orchestration_key(idempotency_key)
        body = embed_orchestration_key(body, normalized_key)
        return body, extract_orchestration_key(body)

    def _dry_run_creation_result(self, context: _IssueCreationContext) -> ProviderIssueResult:
        self._dry_run_issues.append(
            {
                "title": context.title,
                "issue_type": context.issue_type,
                "operation": context.operation,
                "status": "dry-run",
                "parent_id": context.parent_id,
            }
        )
        return ProviderIssueResult(
            identifier="",
            url="",
            status="dry-run",
            metadata={"operation": context.operation, "title": context.title},
        )

    def _find_existing_creation(self, context: _IssueCreationContext) -> ProviderIssueResult | None:
        if not context.orchestration_key:
            return None
        return self._lookup_existing_for_creation(  # type: ignore[attr-defined]
            context.orchestration_key,
            context.lookup_key,
            context.parent_id,
            context.precreate_lookup,
        )

    @staticmethod
    def _creation_labels(type_label: str, labels: list[str] | None) -> list[str]:
        payload_labels = [type_label]
        seen_lower = {type_label.lower()}
        for label in labels or []:
            label = label.strip()
            if label and label.lower() not in seen_lower:
                payload_labels.append(label)
                seen_lower.add(label.lower())
        return payload_labels

    def _recovered_creation_result(
        self,
        recovered: ProviderIssueResult,
        context: _IssueCreationContext,
    ) -> ProviderIssueResult:
        result = ProviderIssueResult(
            identifier=recovered.identifier,
            url=recovered.url,
            status="existing",
            metadata=recovered.metadata,
        )
        result = self._link_created_issue(  # type: ignore[attr-defined]
            result, context.parent_id, newly_created=False
        )
        assert context.orchestration_key is not None
        self._idempotency_cache[context.orchestration_key] = result
        return result

    def _created_issue_result(self, stdout: str, payload_labels: list[str]) -> ProviderIssueResult:
        data = self._parse_json(stdout)
        if not isinstance(data, dict):
            raise ValueError(f"Unexpected response type from GitHub API: {type(data).__name__}")
        number = data.get("number")
        if not isinstance(number, int) or number <= 0:
            raise ValueError(f"GitHub API response did not include a valid issue number: {data!r}")
        return ProviderIssueResult(
            identifier=str(number),
            url=data.get("html_url", ""),
            status="created",
            metadata={
                "database_id": data.get("id", 0),
                "node_id": data.get("node_id", ""),
                "labels": sorted(payload_labels),
            },
        )

    def _cache_created_issue(self, issue: ProviderIssueResult, orchestration_key: str | None) -> None:
        if not orchestration_key:
            return
        self._idempotency_cache[orchestration_key] = ProviderIssueResult(
            identifier=issue.identifier,
            url=issue.url,
            status="existing",
            metadata=issue.metadata,
            hierarchy_link_result=issue.hierarchy_link_result,
        )
