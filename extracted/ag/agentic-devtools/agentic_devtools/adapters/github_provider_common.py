"""Shared GitHub provider state and CLI helpers."""

from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Callable
from typing import Any

from agentic_devtools.adapters.issue_provider import ProviderIssueResult
from agentic_devtools.adapters.retry import TransientError, detect_transient_status_code

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


class _GitHubProviderCommonMixin:
    _owner_repo: str
    _run: Callable[..., subprocess.CompletedProcess[str]]
    _dry_run_issues: list[dict[str, Any]]
    _dry_run_deps: list[dict[str, Any]]
    _idempotency_cache: dict[str, ProviderIssueResult]

    @property
    def owner_repo(self) -> str:
        """Return the configured repository slug."""
        return self._owner_repo

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
