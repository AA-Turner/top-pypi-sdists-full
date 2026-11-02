"""Shared fixtures for the no-change suppressed-triage reaper tests."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import IssueFacts, NoChangePRBrief, PRMetadata, PRTreeState
from agentic_devtools.cli.ci.suppressed_reaper import COPILOT_AGENT_AUTHOR

REVIEW_ID = 4066913338
ISSUE = 1240

SENTINEL = "SUPPRESSED_COMMENTS_EVALUATION_NO_CHANGES_NEEDED"
MARKER = f"<!-- agdt:suppressed-eval:no-changes-needed review-id:{REVIEW_ID} deferred-issue:{ISSUE} -->"

TABLE = "\n".join(
    [
        "| # | Location | Verdict | Justification |",
        "| - | -------- | ------- | ------------- |",
        "| 1 | `specs/spec.md:42` | `valid-no-action` | AS-4 on line 51 already states this. |",
        "| 2 | `stale` | `stale` | `specs/research.md` was deleted before the merge base. |",
    ]
)


def pr_body(*, table: str = TABLE, sentinel: bool = True, marker: bool = True) -> str:
    """Build a shape-B pull request body from its three documented parts."""
    parts = [table]
    if sentinel:
        parts.append(SENTINEL)
    if marker:
        parts.append(MARKER)
    parts.append(f"Closes #{ISSUE}")
    return "\n\n".join(parts)


def brief(**overrides: object) -> NoChangePRBrief:
    """Build an otherwise-eligible candidate brief."""
    defaults: dict = {
        "number": 99,
        "author_login": COPILOT_AGENT_AUTHOR,
        "body": pr_body(),
        "changed_files": 0,
        "additions": 0,
        "deletions": 0,
        "head_branch": "copilot/triage",
        "is_cross_repository": False,
    }
    defaults.update(overrides)
    return NoChangePRBrief(**defaults)  # type: ignore[arg-type]


def issue_body(*, review_id: int = REVIEW_ID, finding_count: int = 2) -> str:
    """Build a deferral issue body carrying the issue-side marker."""
    payload = json.dumps(
        {"pr": 1234, "review_id": review_id, "base_sha": "a" * 40, "finding_count": finding_count},
        separators=(",", ":"),
    )
    return f"<!-- ai-pr-loop:suppressed-comment-deferral {payload} -->\n\n## Deferred suppressed findings\n"


def provider(**overrides: object) -> MagicMock:
    """Build a provider mock whose every call satisfies the close conditions."""
    mock = MagicMock()
    mock.get_issue_facts.return_value = IssueFacts(number=ISSUE, state="open", body=issue_body())
    mock.get_pr_tree_state.return_value = PRTreeState(
        merge_base_sha="b" * 40,
        merge_base_tree_sha="t" * 40,
        head_tree_sha="t" * 40,
        head_sha="h" * 40,
    )
    mock.get_pr_metadata.return_value = PRMetadata(
        number=99,
        title="No changes needed",
        head_branch="copilot/triage",
        head_sha="h" * 40,
        base_branch="main",
    )
    mock.get_file_line_count.return_value = 100
    mock.get_ref_sha.return_value = "h" * 40
    for name, value in overrides.items():
        getattr(mock, name).return_value = value
    return mock
