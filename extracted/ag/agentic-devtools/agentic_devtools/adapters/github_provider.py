"""GitHub IssueProvider implementation.

Uses the ``gh`` CLI for REST API calls.  All mutating calls pass
``shell=False`` to prevent ``%VAR%`` expansion on Windows when user-controlled
text is present in arguments.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Callable
from typing import Any

from agentic_devtools.adapters.dry_run_manifest import build_dry_run_manifest
from agentic_devtools.adapters.exceptions import AdapterValidationError, HierarchyLinkError
from agentic_devtools.adapters.issue_provider import (
    IssueTypeMappingError,
    ProviderIssueResult,
    ProviderLinkResult,
    check_hierarchy_pair,
)
from agentic_devtools.adapters.orchestration_key import embed_orchestration_key, extract_orchestration_key
from agentic_devtools.adapters.retry import TransientError, detect_transient_status_code, retry_on_transient
from agentic_devtools.cli.subprocess_utils import run_safe

# Issue type → GitHub label mapping.  Must align with ``VALID_ISSUE_TYPES`` in
# ``issue_provider.py`` (the ``sub-task`` non-canonical spelling is unsupported
# and handled separately by ``_UNSUPPORTED_TYPES``; ``subtask`` maps to a label).
_ISSUE_TYPE_LABELS: dict[str, str] = {
    "epic": "epic",
    "feature": "feature",
    "subtask": "subtask",
    "task": "task",
    "bug": "bug",
}

# Types that cannot be mapped to GitHub labels (non-canonical spellings only)
_UNSUPPORTED_TYPES: frozenset[str] = frozenset({"sub-task"})

# Matches a GitHub ``HTTP 404`` not-found token as a whole token (case
# insensitive). Anchoring on the ``HTTP`` prefix avoids false positives from
# unrelated numeric substrings such as issue URLs (``.../issues/4040``) or
# issue numbers (``1404``) that merely contain the digits ``404``.
_NOT_FOUND_RE = re.compile(r"\bhttp 404\b", re.IGNORECASE)


def _detect_transient(stderr: str) -> None:
    """Raise TransientError if *stderr* contains a transient HTTP status code.

    Delegates to the shared :func:`detect_transient_status_code` matcher so
    provider-level detection stays aligned with :func:`is_transient_error`.
    Precise matching means strings like ``"1429"``, ``"HTTP 50200"``, or
    ``"processed 429 rows"`` do **not** trigger a false positive, while
    bare provider stderr such as ``"503 service unavailable"`` still does.
    """
    code = detect_transient_status_code(stderr)
    if code is not None:
        raise TransientError(f"GitHub API returned {code}: {stderr}", status_code=code)


class GitHubProvider:
    """GitHub IssueProvider using the ``gh`` CLI for API calls.

    Args:
        owner_repo: Repository slug in ``owner/repo`` format.
        run_command: Optional callable for executing subprocess commands
            (for testing injection).
    """

    def __init__(
        self,
        owner_repo: str,
        run_command: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    ) -> None:
        normalized_owner_repo = owner_repo.strip()
        owner, sep, repo = normalized_owner_repo.partition("/")
        if not sep or not owner or not repo or "/" in repo:
            raise ValueError("owner_repo must be in 'owner/repo' format")

        self._owner_repo = normalized_owner_repo
        self._run: Callable[..., subprocess.CompletedProcess[str]] = run_command or run_safe
        self._dry_run_issues: list[dict[str, Any]] = []
        self._dry_run_deps: list[dict[str, Any]] = []
        # Per-instance cache for idempotency key → result: avoids duplicate
        # creation when GitHub search indexing lags after a fresh POST.
        self._idempotency_cache: dict[str, ProviderIssueResult] = {}

    @property
    def owner_repo(self) -> str:
        """Return the configured repository slug."""
        return self._owner_repo

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _exec_gh(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        """Execute a gh CLI command, raising on transient errors."""
        result = self._run(args, capture_output=True, text=True, shell=False)
        if result.returncode != 0:
            stderr = result.stderr or ""
            _detect_transient(stderr)
            raise RuntimeError(f"gh command failed (exit {result.returncode}): {stderr}")
        return result

    def _parse_json(self, stdout: str) -> Any:
        """Parse JSON from stdout."""
        try:
            return json.loads(stdout)
        except (json.JSONDecodeError, TypeError) as exc:
            raise RuntimeError(f"Failed to parse gh output: {exc}") from exc

    def _fetch_issue_label_names(self, identifier: str) -> set[str]:
        """Fetch all issue label names across all pages.

        Raises ``ValueError`` if the issue is not found (GitHub HTTP 404) so
        callers such as :meth:`set_issue_type` and :meth:`apply_labels` expose
        a consistent not-found contract matching the rest of the provider.
        """
        endpoint = f"/repos/{self._owner_repo}/issues/{identifier}/labels"
        page = 1
        labels: set[str] = set()
        while True:
            args = [
                "gh",
                "api",
                endpoint,
                "--method",
                "GET",
                "-f",
                "per_page=100",
                "-f",
                f"page={page}",
            ]
            try:
                result = self._exec_gh(args)
            except RuntimeError as exc:
                if _NOT_FOUND_RE.search(str(exc)):
                    raise ValueError(f"GitHub issue {identifier!r} not found") from exc
                raise
            page_items = self._parse_json(result.stdout)
            if not isinstance(page_items, list):
                raise RuntimeError("Expected label list response from GitHub issue labels endpoint.")
            for item in page_items:
                if not isinstance(item, dict):
                    continue
                name = item.get("name")
                if isinstance(name, str) and name:
                    labels.add(name)
            if len(page_items) < 100:
                return labels
            page += 1
        return labels

    # ------------------------------------------------------------------
    # IssueProvider protocol methods
    # ------------------------------------------------------------------

    @retry_on_transient
    def create_issue(
        self,
        title: str,
        body: str,
        issue_type: str,
        *,
        parent_id: str | None = None,
        labels: list[str] | None = None,
        idempotency_key: str | None = None,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Create a GitHub issue via ``gh api``.

        Returns the integer database ID (``id`` field) and GraphQL ``node_id``
        in metadata for follow-up link operations.  When ``idempotency_key`` is
        provided the key is embedded in the body and a find-before-create search
        returns any existing match with ``status="existing"``.
        """
        operation = f"POST /repos/{self._owner_repo}/issues"

        if not title or not title.strip():
            raise ValueError("title must be a non-empty string")
        # Fully validate and normalize parent_id *before* creating the issue so
        # that a malformed value (e.g. "1/comments") fails fast rather than
        # creating an orphaned issue that link_subissue only rejects afterwards.
        normalized_parent_id: str | None = None
        if parent_id is not None:
            normalized_parent_id = self._normalize_issue_number(parent_id, "parent_id")

        # Validate issue_type before creating.
        if not issue_type or not issue_type.strip():
            raise ValueError("issue_type must be a non-empty string")

        type_lower = issue_type.lower()
        if type_lower in _UNSUPPORTED_TYPES:
            raise IssueTypeMappingError(
                f"Issue type '{issue_type}' cannot be mapped to a GitHub label. "
                f"GitHub does not support native sub-task types. "
                f"Supported types: {list(_ISSUE_TYPE_LABELS.keys())}"
            )
        if type_lower not in _ISSUE_TYPE_LABELS:
            raise IssueTypeMappingError(
                f"Issue type '{issue_type}' has no GitHub label mapping. "
                f"Supported types: {list(_ISSUE_TYPE_LABELS.keys())}"
            )
        type_label = _ISSUE_TYPE_LABELS[type_lower]

        # Embed the idempotency key into the body so future find-before-create
        # searches can locate this issue.
        if idempotency_key:
            body = embed_orchestration_key(body, idempotency_key)

        if dry_run:
            entry = {
                "title": title,
                "issue_type": issue_type,
                "operation": operation,
                "status": "dry-run",
                "parent_id": normalized_parent_id,
            }
            self._dry_run_issues.append(entry)
            return ProviderIssueResult(
                identifier="",
                url="",
                status="dry-run",
                metadata={"operation": operation, "title": title},
            )

        # Idempotency: consult instance cache first (avoids a search-API call
        # and guards against GitHub search-indexing lag after a fresh POST),
        # then fall back to a remote search.
        orch_key = idempotency_key or extract_orchestration_key(body)
        if orch_key:
            if orch_key in self._idempotency_cache:
                return self._idempotency_cache[orch_key]
            existing = self._find_by_orchestration_key(orch_key)
            if existing:
                # Reconcile parent link: if the caller specified a parent_id but
                # the existing issue was found via remote search (not the local
                # cache), the parent link may not be established yet (e.g. first
                # run crashed after create but before link_subissue).  Re-attempt
                # the link so the caller's invariant is satisfied on every run.
                if normalized_parent_id is not None:
                    try:
                        self.link_subissue(normalized_parent_id, existing.identifier, dry_run=False)
                    except Exception as link_exc:
                        raise RuntimeError(
                            f"Issue #{existing.identifier} already exists at "
                            f"{existing.url} but sub-issue linking to parent "
                            f"#{normalized_parent_id} failed"
                            " (see chained exception for details)"
                        ) from link_exc
                self._idempotency_cache[orch_key] = existing
                return existing

        # Compose the label set: issue-type label plus any caller-provided
        # labels, trimmed and de-duplicated case-insensitively so that values
        # like " Task " or "TASK" alongside the derived "task" label do not
        # produce duplicate or incorrect label payloads.
        payload_labels: list[str] = [type_label]
        seen_lower: set[str] = {type_label.lower()}
        for lbl in labels or []:
            lbl = lbl.strip()
            if lbl and lbl.lower() not in seen_lower:
                payload_labels.append(lbl)
                seen_lower.add(lbl.lower())

        # Create the issue via gh api
        payload: dict[str, Any] = {"title": title, "body": body, "labels": payload_labels}

        args = [
            "gh",
            "api",
            f"/repos/{self._owner_repo}/issues",
            "--method",
            "POST",
            "--input",
            "-",
        ]
        # Use stdin for the payload to avoid shell escaping issues
        result = self._run(
            args,
            capture_output=True,
            text=True,
            shell=False,
            input=json.dumps(payload),
        )
        if result.returncode != 0:
            stderr = result.stderr or ""
            _detect_transient(stderr)
            raise RuntimeError(f"Failed to create issue: {stderr}")

        data = self._parse_json(result.stdout)
        if not isinstance(data, dict):
            raise ValueError(f"Unexpected response type from GitHub API: {type(data).__name__}")
        number = data.get("number")
        if not isinstance(number, int) or number <= 0:
            raise ValueError(f"GitHub API response did not include a valid issue number: {data!r}")
        issue_number = str(number)
        url = data.get("html_url", "")
        database_id = data.get("id", 0)
        node_id = data.get("node_id", "")

        issue_result = ProviderIssueResult(
            identifier=issue_number,
            url=url,
            status="created",
            metadata={
                "database_id": database_id,
                "node_id": node_id,
                "labels": sorted(payload_labels),
            },
        )

        # Link to parent if requested.  TransientError from the link step is
        # re-raised as HierarchyLinkError to prevent the outer
        # @retry_on_transient wrapper from re-running the whole create_issue
        # (which could produce a duplicate if the idempotency cache is cold on
        # the next attempt) and to signal that the issue *was* created but the
        # subsequent hierarchy-link stage failed (partial creation).
        if normalized_parent_id is not None:
            try:
                self.link_subissue(normalized_parent_id, issue_number, dry_run=False)
            except Exception as link_exc:
                raise HierarchyLinkError(
                    f"Issue #{issue_number} was created at {url} but "
                    f"sub-issue linking to parent #{normalized_parent_id} failed"
                    " (see chained exception for details)",
                    created_result=issue_result,
                    stage="link_subissue",
                    cause=link_exc,
                ) from link_exc

        # Populate the instance idempotency cache only after the full operation
        # (including parent linking) succeeds, so a same-key retry does not
        # return status="existing" when linking had previously failed.
        # Cache with status="existing" so idempotent repeat calls correctly
        # signal that the issue already existed rather than that it was created.
        if orch_key:
            self._idempotency_cache[orch_key] = ProviderIssueResult(
                identifier=issue_result.identifier,
                url=issue_result.url,
                status="existing",
                metadata=issue_result.metadata,
            )

        return issue_result

    @retry_on_transient
    def set_issue_type(
        self,
        identifier: str,
        issue_type: str,
        *,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Set the issue-type label by replacing any existing type label.

        Raises:
            ValueError: If ``identifier`` is empty or whitespace-only.
            IssueTypeMappingError: If ``issue_type`` has no GitHub label mapping.
        """
        identifier_normalized = self._normalize_issue_number(identifier, "identifier")
        type_lower = issue_type.lower()

        if type_lower in _UNSUPPORTED_TYPES:
            raise IssueTypeMappingError(
                f"Issue type '{issue_type}' cannot be mapped to a GitHub label. "
                f"GitHub does not support native sub-task types. "
                f"Supported types: {list(_ISSUE_TYPE_LABELS.keys())}"
            )

        if type_lower not in _ISSUE_TYPE_LABELS:
            raise IssueTypeMappingError(
                f"Issue type '{issue_type}' has no GitHub label mapping. "
                f"Supported types: {list(_ISSUE_TYPE_LABELS.keys())}"
            )

        if dry_run:
            return ProviderIssueResult(
                identifier=identifier_normalized,
                url="",
                status="dry-run",
                metadata={"label": _ISSUE_TYPE_LABELS[type_lower], "issue_type": type_lower},
            )

        label = _ISSUE_TYPE_LABELS[type_lower]
        url = f"https://github.com/{self._owner_repo}/issues/{identifier_normalized}"

        # Read current labels (all pages) and replace any existing issue-type
        # label with the requested one while preserving unrelated labels.
        existing_set = self._fetch_issue_label_names(identifier_normalized)

        # Use casefold comparison so "Bug" is treated the same as "bug"
        # (GitHub labels are case-insensitive; the repository may store the
        # canonical label name with any casing).
        type_labels_lower = {t.casefold() for t in _ISSUE_TYPE_LABELS.values()}
        non_type_labels = {lbl for lbl in existing_set if lbl.casefold() not in type_labels_lower}
        next_labels = non_type_labels | {label}
        # No-op when the resulting label set is case-insensitively identical to
        # the existing set (handles "Bug" == "bug" with no PATCH needed).
        if {lbl.casefold() for lbl in next_labels} == {lbl.casefold() for lbl in existing_set}:
            return ProviderIssueResult(
                identifier=identifier_normalized,
                url=url,
                status="no-op",
                metadata={"label": label, "issue_type": type_lower},
            )

        payload = {"labels": sorted(next_labels)}
        args = [
            "gh",
            "api",
            f"/repos/{self._owner_repo}/issues/{identifier_normalized}",
            "--method",
            "PATCH",
            "--input",
            "-",
        ]
        patch_result = self._run(
            args,
            capture_output=True,
            text=True,
            shell=False,
            input=json.dumps(payload),
        )
        if patch_result.returncode != 0:
            stderr = patch_result.stderr or ""
            _detect_transient(stderr)
            raise RuntimeError(f"Failed to set issue type label {label!r}: {stderr}")

        return ProviderIssueResult(
            identifier=identifier_normalized,
            url=url,
            status="updated",
            metadata={"label": label, "issue_type": type_lower},
        )

    def _resolve_identifier_inner(self, identifier_normalized: str) -> ProviderIssueResult:
        """Perform the actual identifier → database-ID lookup without a retry decorator.

        Callers that need retry behaviour should use the public
        :meth:`resolve_identifier` method.  Callers that are themselves
        already retry-decorated (``link_subissue``, ``_to_db_id``) call this
        helper directly so that a persistent transient failure does not trigger
        nested retry amplification (``4 × 4 = 16`` attempts).

        Raises ``ValueError`` when the issue is not found (GitHub HTTP 404),
        matching the :class:`IssueProvider` contract so that every caller
        (``link_subissue``, ``_to_db_id``, ``resolve_identifier``) gets
        consistent not-found behaviour without needing individual wrappers.

        Validates that the resolved ``database_id`` is a positive integer
        before returning ``status="resolved"``, so callers see a clear error
        instead of a truthy ``"0"`` string that would silently fail later.
        """
        args = [
            "gh",
            "api",
            f"/repos/{self._owner_repo}/issues/{identifier_normalized}",
        ]
        try:
            result = self._exec_gh(args)
        except RuntimeError as exc:
            if _NOT_FOUND_RE.search(str(exc)):
                raise ValueError(f"GitHub issue {identifier_normalized!r} not found") from exc
            raise
        data = self._parse_json(result.stdout)

        if not isinstance(data, dict):
            raise RuntimeError(f"Expected a JSON object from GitHub issues endpoint, got {type(data).__name__}")

        raw_id = data.get("id")
        if not isinstance(raw_id, int) or isinstance(raw_id, bool) or raw_id <= 0:
            raise RuntimeError(
                f"GitHub issue {identifier_normalized!r} did not return a valid positive integer "
                f"database ID; got: {raw_id!r}"
            )

        url = data.get("html_url", "")
        node_id = data.get("node_id", "")

        return ProviderIssueResult(
            identifier=identifier_normalized,
            url=url,
            status="resolved",
            metadata={
                "database_id": raw_id,
                "node_id": node_id,
                "internal_id": str(raw_id),
            },
        )

    @retry_on_transient
    def resolve_identifier(
        self,
        identifier: str,
        *,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Resolve an existing GitHub issue number to its database ID.

        Raises ``ValueError`` when the issue does not exist (GitHub returns
        ``HTTP 404``), matching the :class:`IssueProvider` contract and the
        Jira/InMemory adapters, so protocol consumers can handle not-found
        consistently.  The 404→ValueError translation is performed inside
        :meth:`_resolve_identifier_inner`; other provider failures propagate
        unchanged.
        """
        identifier_normalized = self._normalize_issue_number(identifier, "identifier")

        if dry_run:
            return ProviderIssueResult(
                identifier=identifier_normalized,
                url="",
                status="dry-run",
            )

        return self._resolve_identifier_inner(identifier_normalized)

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
        resolved = self._resolve_identifier_inner(child_id)
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
        """Return ``True`` if *child_db_id* is already a sub-issue of *parent_id*.

        GETs ``/repos/{owner}/{repo}/issues/{parent_id}/sub_issues`` and checks
        whether any item's ``id`` (integer database ID) matches *child_db_id*.
        A failed GET or a malformed (non-list) response is propagated as an
        error rather than treated as "not found", since silently returning
        ``False`` could duplicate an existing sub-issue relationship.

        Raises ``ValueError`` when the parent issue is not found (GitHub HTTP
        404) so :meth:`link_subissue` exposes a consistent not-found contract.
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

    @retry_on_transient
    def add_blocked_by(
        self,
        issue_id: str,
        blocked_by_id: str,
        *,
        dry_run: bool = False,
    ) -> ProviderLinkResult:
        """Declare a blocking dependency via the GitHub REST Dependencies API.

        Both ``issue_id`` and ``blocked_by_id`` must be numeric GitHub issue
        numbers.  ``blocked_by_id`` is resolved to its integer database ID
        before calling
        ``POST /repos/{owner}/{repo}/issues/{issue_id}/dependencies/blocked_by``
        with ``{"issue_id": <int>}``.

        Idempotent: returns ``status="already-linked"`` when the REST API
        reports that the dependency already exists (non-zero exit code with
        an "already exists" message in the response body or stderr).
        """
        issue_id_normalized = issue_id.strip()
        blocked_by_id_normalized = blocked_by_id.strip()
        if not issue_id_normalized:
            raise ValueError("issue_id must be non-empty")
        if not issue_id_normalized.isdigit():
            raise ValueError(f"issue_id must be a numeric GitHub issue number, got: {issue_id!r}")
        if not blocked_by_id_normalized:
            raise ValueError("blocked_by_id must be non-empty")
        if not blocked_by_id_normalized.isdigit():
            raise ValueError(f"blocked_by_id must be a numeric GitHub issue number, got: {blocked_by_id!r}")
        if issue_id_normalized == blocked_by_id_normalized:
            raise ValueError("an issue cannot block itself")

        if dry_run:
            entry = {
                "source": blocked_by_id_normalized,
                "target": issue_id_normalized,
                "type": "blocks",
                "operation": (f"POST /repos/{self._owner_repo}/issues/{issue_id_normalized}/dependencies/blocked_by"),
                "status": "dry-run",
            }
            self._dry_run_deps.append(entry)
            return ProviderLinkResult(
                source_id=blocked_by_id_normalized,
                target_id=issue_id_normalized,
                status="dry-run",
            )

        # Resolve blocked_by_id to its integer database ID for the request body.
        # _to_db_id calls _resolve_identifier_inner, which raises ``ValueError``
        # when the blocker issue is not found (HTTP 404).
        blocked_by_db_id = self._to_db_id(blocked_by_id_normalized)

        payload = {"issue_id": blocked_by_db_id}
        args = [
            "gh",
            "api",
            f"/repos/{self._owner_repo}/issues/{issue_id_normalized}/dependencies/blocked_by",
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
            stdout = result.stdout or ""
            combined = stderr + stdout
            # Idempotent: return "already-linked" when the dependency already exists.
            if "already exists" in combined.lower():
                return ProviderLinkResult(
                    source_id=blocked_by_id_normalized,
                    target_id=issue_id_normalized,
                    status="already-linked",
                )
            _detect_transient(stderr)
            if "HTTP 404" in combined or "HTTP 422" in combined:
                raise ValueError(
                    f"Invalid or non-existent identifier in blocked_by dependency (HTTP 404/422): {stderr}"
                )
            raise RuntimeError(f"Failed to add blocked_by dependency: {stderr}")

        return ProviderLinkResult(
            source_id=blocked_by_id_normalized,
            target_id=issue_id_normalized,
            status="linked",
        )

    def _to_db_id(self, identifier: str) -> int:
        """Return the integer database ID for a numeric issue number.

        Resolves ``identifier`` (a GitHub issue number as a digit string) to
        its internal integer database ID via :meth:`_resolve_identifier_inner`.
        Calls the inner helper directly (no retry decorator) so that callers
        which are already retry-decorated (``add_blocked_by``) do not amplify
        retries across nested layers.  Raises ``RuntimeError`` when the
        identifier is not numeric or the resolved metadata does not include a
        valid positive integer ``database_id``.  Raises ``ValueError`` when
        the issue is not found (HTTP 404), propagated from
        :meth:`_resolve_identifier_inner`.
        """
        identifier = identifier.strip()
        if not identifier:
            raise RuntimeError("GitHub issue identifier must not be empty.")
        if not identifier.isdigit():
            raise RuntimeError(
                f"Expected a numeric GitHub issue number, got {identifier!r}. "
                "Provide the issue number (not a node ID) for dependency linking."
            )
        resolved = self._resolve_identifier_inner(identifier)
        return resolved.metadata["database_id"]  # validated positive int by _resolve_identifier_inner

    @retry_on_transient
    def apply_labels(
        self,
        identifier: str,
        labels: list[str],
        *,
        dry_run: bool = False,
    ) -> ProviderIssueResult:
        """Apply labels to a GitHub issue (idempotent, additive).

        Returns ``status="no-op"`` for an empty list or when all requested
        labels are already present, ``status="updated"`` when at least one new
        label is applied, or ``status="dry-run"`` in dry-run mode.  For
        all modes, ``identifier`` must be a numeric GitHub issue number (a
        single leading ``#`` is accepted and stripped).
        For
        non-dry-run results ``metadata["labels"]`` reflects the full
        post-operation label set (sorted); in dry-run mode no API call is made,
        and ``metadata["labels"]`` is a sorted preview of the requested labels
        only.
        """
        identifier = self._normalize_issue_number(identifier, "identifier")

        # Trim whitespace and deduplicate case-insensitively (preserve
        # first-seen casing).  GitHub labels are case-insensitive, so
        # ["Bug", " bug ", "BUG"] are all the same label.
        seen_lower: set[str] = set()
        requested_labels: list[str] = []
        for lbl in labels:
            stripped = lbl.strip() if lbl else ""
            if stripped and stripped.lower() not in seen_lower:
                requested_labels.append(stripped)
                seen_lower.add(stripped.lower())
        issue_url = f"https://github.com/{self._owner_repo}/issues/{identifier}"

        if dry_run:
            entry = {
                "source": identifier,
                "target": ",".join(requested_labels),
                "type": "label",
                "operation": f"POST /repos/{self._owner_repo}/issues/{identifier}/labels",
                "status": "dry-run",
            }
            self._dry_run_deps.append(entry)
            return ProviderIssueResult(
                identifier=identifier,
                url="",
                status="dry-run",
                metadata={"labels": sorted(set(requested_labels))},
            )

        # Fetch existing labels across all pages on the issue.
        existing_set = self._fetch_issue_label_names(identifier)
        # Use case-insensitive comparison: GitHub treats "Bug" and "bug" as the
        # same label, so avoid a redundant POST when casing differs.
        existing_lower = {lbl.lower() for lbl in existing_set}

        new_labels = [lbl for lbl in requested_labels if lbl.lower() not in existing_lower]

        if not new_labels:
            return ProviderIssueResult(
                identifier=identifier,
                url=issue_url,
                status="no-op",
                metadata={"labels": sorted(existing_set)},
            )

        # Add the new labels in a single request.
        payload = {"labels": new_labels}
        args = [
            "gh",
            "api",
            f"/repos/{self._owner_repo}/issues/{identifier}/labels",
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
            _detect_transient(stderr)
            raise RuntimeError(f"Failed to apply labels {new_labels!r}: {stderr}")

        return ProviderIssueResult(
            identifier=identifier,
            url=issue_url,
            status="updated",
            metadata={"labels": sorted(existing_set | set(new_labels))},
        )

    def _normalize_issue_number(self, identifier: str, field_name: str) -> str:
        """Return a stripped numeric issue number for a user-supplied identifier."""
        if not identifier or not identifier.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        normalized = identifier.strip().removeprefix("#")
        if not normalized.isdigit():
            raise ValueError(f"{field_name} must be a numeric GitHub issue number, got: {identifier!r}")
        return normalized

    def normalize_identifier(self, identifier: str) -> str:
        """Normalize a GitHub issue identifier (strips a leading ``#``).

        Pure string transformation with no side effects.  Raises
        ``ValueError`` for empty/whitespace-only identifiers.
        """
        if not identifier or not identifier.strip():
            raise ValueError("identifier must be a non-empty string")
        stripped = identifier.strip().removeprefix("#")
        if not stripped:
            raise ValueError("identifier must be a non-empty string after normalization")
        return stripped

    def format_identifier(self, identifier: str) -> str:
        """Format a GitHub issue identifier for display (ensures a leading ``#``).

        Raises ``ValueError`` for empty/whitespace-only identifiers.
        """
        if not identifier or not identifier.strip():
            raise ValueError("identifier must be a non-empty string")
        cleaned = identifier.strip()
        return cleaned if cleaned.startswith("#") else f"#{cleaned}"

    # ------------------------------------------------------------------
    # Hierarchy-validation capability (HierarchyValidationProvider)
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Idempotency helpers
    # ------------------------------------------------------------------

    def _find_by_orchestration_key(self, orch_key: str) -> ProviderIssueResult | None:
        """Search for an existing issue with the given orchestration key.

        Returns a result with ``status="existing"`` when a match is found, or
        ``None`` when the search succeeds but returns no results.  Any search
        failure (authentication errors, malformed responses, transient errors,
        or a match lacking a valid positive issue ``number``) is propagated to
        the caller rather than silently treated as "not found", which would
        cause duplicate issues to be created on re-runs.
        """
        query = f'repo:{self._owner_repo} "agdt-orch-key:{orch_key}" in:body is:issue'
        args = [
            "gh",
            "api",
            "/search/issues",
            "--method",
            "GET",
            "-f",
            f"q={query}",
        ]
        result = self._exec_gh(args)
        data = self._parse_json(result.stdout)
        if not isinstance(data, dict):
            raise RuntimeError("Expected search response object from GitHub issue search.")
        if data.get("incomplete_results") is True:
            raise RuntimeError(
                "GitHub issue search timed out and returned incomplete results; "
                "cannot safely determine idempotent-create status."
            )
        items = data.get("items", [])
        if not isinstance(items, list):
            raise RuntimeError("Expected search response items to be a list.")
        if len(items) > 1:
            raise RuntimeError(
                f"Ambiguous idempotency-key search: {len(items)} issues matched "
                f"orchestration key {orch_key!r}. Cannot safely determine which "
                "issue to treat as the existing one."
            )
        if items:
            item = items[0]
            if not isinstance(item, dict):
                raise RuntimeError("Expected first search result item to be an object.")
            number = item.get("number")
            if not isinstance(number, int) or isinstance(number, bool) or number <= 0:
                raise RuntimeError("GitHub issue search result did not include a valid positive issue number.")
            return ProviderIssueResult(
                identifier=str(number),
                url=item.get("html_url", ""),
                status="existing",
                metadata={
                    "database_id": item.get("id", 0),
                    "node_id": item.get("node_id", ""),
                },
            )
        return None

    # ------------------------------------------------------------------
    # Dry-run manifest
    # ------------------------------------------------------------------

    def get_dry_run_manifest(self) -> dict[str, Any]:
        """Return the accumulated dry-run manifest."""
        return build_dry_run_manifest(
            issues=self._dry_run_issues,
            dependencies=self._dry_run_deps,
        )
