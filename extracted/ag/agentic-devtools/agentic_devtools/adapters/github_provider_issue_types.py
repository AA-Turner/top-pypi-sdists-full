"""GitHub issue-type label operations."""

from __future__ import annotations

import json

from agentic_devtools.adapters.github_provider_common import _detect_transient, _GitHubProviderCommonMixin
from agentic_devtools.adapters.issue_provider import IssueTypeMappingError, ProviderIssueResult
from agentic_devtools.adapters.retry import retry_on_transient

_ISSUE_TYPE_LABELS: dict[str, str] = {
    "epic": "epic",
    "feature": "feature",
    "subtask": "subtask",
    "task": "task",
    "bug": "bug",
}
_UNSUPPORTED_TYPES: frozenset[str] = frozenset({"sub-task"})


class GitHubProviderIssueTypesMixin(_GitHubProviderCommonMixin):
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
