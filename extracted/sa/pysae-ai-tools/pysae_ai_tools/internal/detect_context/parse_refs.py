"""Parse GitLab references from free-text arguments.

Handles: !IID, #IID, MR/issue/job/pipeline URLs, branch names (prefix/IID-slug).
"""

import re
from dataclasses import dataclass


@dataclass
class ParsedRef:
    """Parsed GitLab reference from user input."""

    mr_iid: str = ""
    issue_iid: str = ""
    job_id: str = ""
    pipeline_id: str = ""
    project_path: str = ""  # extracted from URL, may differ from current repo

    @property
    def has_any(self) -> bool:
        return bool(self.mr_iid or self.issue_iid or self.job_id or self.pipeline_id)


# URL patterns — order matters: more specific first
_URL_PATTERNS: list[tuple[re.Pattern[str], list[str]]] = [
    (
        re.compile(r"https?://gitlab\.com/([\w./-]+?)/-/merge_requests/(\d+)"),
        ["project_path", "mr_iid"],
    ),
    (
        re.compile(r"https?://gitlab\.com/([\w./-]+?)/-/(?:issues|work_items)/(\d+)"),
        ["project_path", "issue_iid"],
    ),
    (
        re.compile(r"https?://gitlab\.com/([\w./-]+?)/-/jobs/(\d+)"),
        ["project_path", "job_id"],
    ),
    (
        re.compile(r"https?://gitlab\.com/([\w./-]+?)/-/pipelines/(\d+)"),
        ["project_path", "pipeline_id"],
    ),
]

# Short ref patterns
_MR_SHORT = re.compile(r"!(\d+)")
_ISSUE_SHORT = re.compile(r"#(\d+)")

# Branch name pattern: prefix/IID-slug
_BRANCH_PATTERN = re.compile(r"^[\w]+/(\d+)-[\w-]+$")


def parse_gitlab_refs(text: str) -> ParsedRef:
    """Parse GitLab references from a free-text string.

    Supports:
    - URLs: MR, issue, work_item, job, pipeline (with project_path extraction)
    - Short refs: !IID (MR), #IID (issue)
    - Branch names: feat/123-add-login → issue_iid=123

    Returns the first URL match if any, otherwise combines short refs.
    """
    ref = ParsedRef()

    # Try URL patterns first (most specific)
    for pattern, fields in _URL_PATTERNS:
        match = pattern.search(text)
        if match:
            for i, field in enumerate(fields):
                setattr(ref, field, match.group(i + 1))
            return ref

    # Short refs
    mr_match = _MR_SHORT.search(text)
    if mr_match:
        ref.mr_iid = mr_match.group(1)

    issue_match = _ISSUE_SHORT.search(text)
    if issue_match:
        ref.issue_iid = issue_match.group(1)

    if ref.has_any:
        return ref

    # Branch name fallback
    branch_match = _BRANCH_PATTERN.search(text.strip())
    if branch_match:
        ref.issue_iid = branch_match.group(1)

    return ref
