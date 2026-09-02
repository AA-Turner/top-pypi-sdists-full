"""Audit data models.

Dataclasses and enums for the PR review audit workflow. These models
are provider-agnostic — they work with any ``CIPlatformProvider``
implementation (GitHub, Azure DevOps, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ClaimResult(Enum):
    """Result of attempting to claim a PR for audit.

    Used by ``CIPlatformProvider.claim_pr_for_audit()`` to indicate whether
    the claim was newly established or the PR was already claimed by another
    concurrent audit run.

    Azure DevOps equivalent: Tag-based claim with optimistic concurrency
    (check tag existence → add tag; retry on conflict).
    """

    CLAIMED = "claimed"
    ALREADY_CLAIMED = "already_claimed"


@dataclass(frozen=True)
class ClosedPRInfo:
    """Minimal metadata for a closed pull request eligible for audit.

    Attributes:
        number: PR number.
        title: PR title.
        url: Direct URL to the PR.
        state: PR state (e.g., "closed", "merged").
        closed_at: ISO 8601 timestamp when the PR was closed.
        merged: Whether the PR was merged (True) or closed without merge (False).

    Azure DevOps equivalent: Uses ``GitPullRequest`` with ``status=completed``
    or ``status=abandoned`` and ``closedDate`` field.
    """

    number: int
    title: str
    url: str
    state: str
    closed_at: str
    merged: bool


@dataclass(frozen=True)
class ReviewObservation:
    """A single review observation extracted from a PR comment.

    Represents one categorized piece of feedback from a reviewer.

    Attributes:
        file_path: File path the comment references (empty for PR-level).
        line: Line number (None for file-level or PR-level comments).
        body: Full comment body text.
        diff_hunk: Diff context around the commented line.
        resolved: Whether the comment thread was resolved.
        reviewer: Login of the reviewer who posted the comment.
        primary_category: Primary feedback category from the taxonomy.
        secondary_category: Optional secondary category (empty if none).
        is_stale: Whether the observation references deleted/refactored code.

    Azure DevOps equivalent: Maps to ``GitPullRequestCommentThread`` with
    ``threadContext`` for file/line and ``status`` for resolution state.
    """

    file_path: str
    line: int | None
    body: str
    diff_hunk: str
    resolved: bool
    reviewer: str
    primary_category: str
    secondary_category: str = ""
    is_stale: bool = False
    pr_number: int = 0


@dataclass
class AuditBatch:
    """Represents a batch of PRs being audited together.

    Attributes:
        batch_id: Unique identifier for this batch (UUID4 hex).
        pr_numbers: List of PR numbers included in this batch.
        created_at: ISO 8601 timestamp when the batch was created.
        status: Batch processing status (e.g., "preparing", "ready", "applied").
        output_dir: Absolute path to the batch output directory.

    Azure DevOps equivalent: Same structure; PR numbers are integer IDs.
    """

    batch_id: str
    pr_numbers: list[int] = field(default_factory=list)
    created_at: str = ""
    status: str = "preparing"
    output_dir: str = ""


@dataclass
class InstructionFile:
    """A preloaded instruction file with its content and metadata.

    Attributes:
        path: Repo-relative path (e.g., ".github/copilot-instructions.md").
        exists: Whether the file currently exists on disk.
        can_update: Whether the evaluation agent may edit this file directly.
        content: File content (empty string if file does not exist).
    """

    path: str
    exists: bool
    can_update: bool = True
    content: str = ""


@dataclass
class BatchOutput:
    """Complete structured output of the preparation phase.

    Attributes:
        batch_id: Unique batch identifier.
        prs: List of closed PR info for all PRs in the batch.
        observations: All review observations across all PRs.
        instruction_files: Preloaded instruction files relevant to the batch.
    """

    batch_id: str
    prs: list[ClosedPRInfo] = field(default_factory=list)
    observations: list[ReviewObservation] = field(default_factory=list)
    instruction_files: list[InstructionFile] = field(default_factory=list)
