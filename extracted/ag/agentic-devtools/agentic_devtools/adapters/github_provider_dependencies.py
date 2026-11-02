"""GitHub blocked-by dependency operations."""

from __future__ import annotations

import json

from agentic_devtools.adapters.github_provider_common import _detect_transient, _GitHubProviderCommonMixin
from agentic_devtools.adapters.issue_provider import ProviderLinkResult
from agentic_devtools.adapters.retry import retry_on_transient


# The facade composes sibling mixins supplying the intentionally ignored members below.
class GitHubProviderDependenciesMixin(_GitHubProviderCommonMixin):
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
        resolved = self._resolve_identifier_inner(identifier)  # type: ignore[attr-defined]
        return resolved.metadata["database_id"]  # validated positive int by _resolve_identifier_inner
