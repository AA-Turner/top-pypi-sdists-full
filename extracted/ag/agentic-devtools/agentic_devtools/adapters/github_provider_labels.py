"""GitHub issue label operations."""

from __future__ import annotations

import json

from agentic_devtools.adapters.github_provider_common import _detect_transient, _GitHubProviderCommonMixin
from agentic_devtools.adapters.issue_provider import ProviderIssueResult
from agentic_devtools.adapters.retry import retry_on_transient


class GitHubProviderLabelsMixin(_GitHubProviderCommonMixin):
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
