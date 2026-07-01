from __future__ import annotations

from typing import Sequence

from spec_kitty_tracker.models import CanonicalIssue, ExternalRef


class InMemoryIssueStore:
    def __init__(self) -> None:
        self._issues: dict[str, CanonicalIssue] = {}

    async def list_issues(self, *, system: str | None = None) -> Sequence[CanonicalIssue]:
        values = list(self._issues.values())
        if system is not None:
            values = [issue for issue in values if issue.ref.system == system]
        values.sort(key=lambda issue: issue.ref.identity)
        return [issue.clone() for issue in values]

    async def get_issue(self, ref: ExternalRef) -> CanonicalIssue | None:
        issue = self._issues.get(ref.identity)
        return issue.clone() if issue is not None else None

    async def upsert_issue(self, issue: CanonicalIssue) -> None:
        self._issues[issue.ref.identity] = issue.clone()

    async def delete_issue(self, ref: ExternalRef) -> None:
        self._issues.pop(ref.identity, None)
