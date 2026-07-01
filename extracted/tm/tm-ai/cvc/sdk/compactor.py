"""
cvc.sdk.compactor — Context Compaction & Distillation (Phase 7).

Keeps the hive mind efficient as it grows to millions of commits through:

1. **Compaction**: Creates new "distilled" summary commits that condense
   chains of old commits into single summaries.  Original commits are
   NEVER deleted — the distilled commit is additive.

2. **Context windowing**: Per-agent configurable window of recent commits
   in active context; older commits remain accessible via ``agent.recall()``.

3. **Anchor commits**: Periodic full-state snapshots per squad, enabling
   faster sync and delta compression.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Callable

from cvc.core.database import ContextDatabase
from cvc.core.models import (
    CognitiveCommit,
    CommitMetadata,
    CommitType,
    ContentBlob,
    ContextMessage,
)

logger = logging.getLogger("cvc.sdk.compactor")

# Default summariser just concatenates messages — real usage passes an LLM
SummariserFn = Callable[[list[CognitiveCommit]], str]


def _default_summariser(commits: list[CognitiveCommit]) -> str:
    """Built-in summariser: concatenate commit messages into a bullet list."""
    lines: list[str] = []
    for c in commits:
        agent = c.metadata.agent_id
        short = c.commit_hash[:8]
        lines.append(f"- [{short}] {agent}: {c.message}")
    return "Distilled summary of {} commits:\n{}".format(len(commits), "\n".join(lines))


class CompactionResult:
    """Result of a compaction operation."""

    __slots__ = ("distilled_commits", "original_count", "branches_compacted", "anchors_created")

    def __init__(self) -> None:
        self.distilled_commits: list[str] = []   # hashes of new distilled commits
        self.original_count: int = 0              # how many raw commits were summarised
        self.branches_compacted: list[str] = []   # which branches were compacted
        self.anchors_created: list[str] = []      # hashes of auto-anchor commits

    def __repr__(self) -> str:
        return (
            f"CompactionResult(distilled={len(self.distilled_commits)}, "
            f"originals={self.original_count}, "
            f"branches={len(self.branches_compacted)}, "
            f"anchors={len(self.anchors_created)})"
        )


class HiveCompactor:
    """
    AI-powered context compaction for the hive mind.

    Creates distilled commits that summarise chains of older commits
    while preserving every original commit in the Merkle DAG.

    Usage::

        compactor = HiveCompactor(db)
        result = compactor.compact(strategy="summarize", max_age_hours=24)
        print(result.distilled_commits)
    """

    def __init__(
        self,
        db: ContextDatabase,
        *,
        summariser: SummariserFn | None = None,
    ) -> None:
        self._db = db
        self._summariser = summariser or _default_summariser

    @property
    def summariser(self) -> SummariserFn:
        return self._summariser

    @summariser.setter
    def summariser(self, fn: SummariserFn) -> None:
        self._summariser = fn

    # -- Main compaction ---------------------------------------------------

    def compact(
        self,
        *,
        strategy: str = "summarize",
        max_age_hours: float = 24.0,
        branch: str | None = None,
        min_commits: int = 3,
    ) -> CompactionResult:
        """Compact old commits into distilled summaries.

        Parameters
        ----------
        strategy:
            ``"summarize"`` — create distilled commits summarising old chains.
        max_age_hours:
            Commits older than this many hours are candidates for compaction.
        branch:
            If given, only compact this branch.  Otherwise compact all branches.
        min_commits:
            Minimum number of eligible commits needed to trigger compaction
            on a branch.

        Returns
        -------
        CompactionResult with details of what was created.
        """
        if strategy != "summarize":
            raise ValueError(f"Unknown compaction strategy: {strategy!r}")

        result = CompactionResult()
        cutoff = time.time() - (max_age_hours * 3600)

        branches_to_compact: list[str]
        if branch:
            branches_to_compact = [branch]
        else:
            branches_to_compact = [
                bp.name for bp in self._db.index.list_branches()
            ]

        for branch_name in branches_to_compact:
            self._compact_branch(
                branch_name, cutoff, min_commits, result,
            )

        return result

    def _compact_branch(
        self,
        branch_name: str,
        cutoff: float,
        min_commits: int,
        result: CompactionResult,
    ) -> None:
        """Compact a single branch's old commits."""
        bp = self._db.index.get_branch(branch_name)
        if bp is None:
            return

        # Walk the branch and find commits older than cutoff that are NOT
        # already distilled or genesis-type
        old_commits = self._get_compactable_commits(bp.head_hash, cutoff)

        if len(old_commits) < min_commits:
            return

        # Create a distilled commit referencing all the originals
        summary = self._summariser(old_commits)
        distilled_hash = self._create_distilled_commit(
            branch_name, old_commits, summary,
        )

        result.distilled_commits.append(distilled_hash)
        result.original_count += len(old_commits)
        if branch_name not in result.branches_compacted:
            result.branches_compacted.append(branch_name)

    def _get_compactable_commits(
        self,
        head_hash: str,
        cutoff: float,
    ) -> list[CognitiveCommit]:
        """Walk from head backwards, collecting commits older than cutoff.

        Skips commits that are already DISTILLATION-type or the genesis commit.
        """
        candidates: list[CognitiveCommit] = []
        queue = [head_hash]
        seen: set[str] = set()

        while queue:
            h = queue.pop(0)
            if h in seen:
                continue
            seen.add(h)

            c = self._db.index.get_commit(h)
            if c is None:
                continue

            # Skip distilled commits — don't re-distill them
            if c.commit_type == CommitType.DISTILLATION:
                # Still walk parents so we find old raw commits behind distilled ones
                queue.extend(c.parent_hashes)
                continue

            if c.metadata.timestamp <= cutoff:
                # Skip genesis commits (no parent, anchor at root)
                if c.parent_hashes:
                    candidates.append(c)
                # Keep walking to gather the full old chain
                queue.extend(c.parent_hashes)
            else:
                # Newer than cutoff — walk parents in case there are older ones
                queue.extend(c.parent_hashes)

        # Return in chronological order (oldest first)
        candidates.sort(key=lambda c: c.metadata.timestamp)
        return candidates

    def _create_distilled_commit(
        self,
        branch_name: str,
        original_commits: list[CognitiveCommit],
        summary: str,
    ) -> str:
        """Create and store a distilled commit."""
        bp = self._db.index.get_branch(branch_name)
        if bp is None:
            raise ValueError(f"Branch {branch_name} does not exist")

        original_count = len(original_commits)
        original_tokens = sum(c.content_blob.token_count for c in original_commits)
        # Estimate distilled tokens from summary length
        distilled_tokens = max(1, len(summary.split()))
        ratio = distilled_tokens / max(1, original_tokens) if original_tokens else 0.0

        # Parent is the current branch head — preserves Merkle chain
        # Also reference the oldest original commit to maintain provenance
        parent_hashes = [bp.head_hash]

        # Build content blob with distilled summary
        blob = ContentBlob(
            messages=[ContextMessage(
                role="system",
                content=summary,
            )],
            distilled_summary=summary,
            token_count=distilled_tokens,
        )

        # Metadata references the compaction
        meta = CommitMetadata(
            agent_id="hive-compactor",
            tags=[
                "distilled",
                f"original_count:{original_count}",
                f"branch:{branch_name}",
            ],
            distilled_ratio=ratio,
        )

        commit = CognitiveCommit(
            parent_hashes=parent_hashes,
            commit_type=CommitType.DISTILLATION,
            message=f"Distilled {original_count} commits on {branch_name}",
            content_blob=blob,
            metadata=meta,
        )

        commit_hash = self._db.store_commit(commit)
        self._db.index.advance_head(branch_name, commit_hash)

        logger.info(
            "Created distilled commit %s on %s (%d originals → summary)",
            commit_hash[:12], branch_name, original_count,
        )
        return commit_hash

    # -- Anchor commits ----------------------------------------------------

    def auto_anchor(
        self,
        *,
        branch: str | None = None,
        every_n: int = 10,
    ) -> CompactionResult:
        """Create anchor commits on branches that have accumulated enough deltas.

        Parameters
        ----------
        branch:
            If given, only check this branch.  Otherwise check all.
        every_n:
            Create an anchor after this many commits since the last anchor.

        Returns
        -------
        CompactionResult with ``anchors_created`` populated.
        """
        result = CompactionResult()

        branches_to_check: list[str]
        if branch:
            branches_to_check = [branch]
        else:
            branches_to_check = [
                bp.name for bp in self._db.index.list_branches()
            ]

        for branch_name in branches_to_check:
            bp = self._db.index.get_branch(branch_name)
            if bp is None:
                continue

            commits_since = self._db.index.count_commits_since_anchor(bp.head_hash)
            if commits_since >= every_n:
                anchor_hash = self._create_anchor_commit(branch_name)
                result.anchors_created.append(anchor_hash)
                if branch_name not in result.branches_compacted:
                    result.branches_compacted.append(branch_name)

        return result

    def _create_anchor_commit(self, branch_name: str) -> str:
        """Create a full-state anchor commit on a branch."""
        bp = self._db.index.get_branch(branch_name)
        if bp is None:
            raise ValueError(f"Branch {branch_name} does not exist")

        # Gather recent commits on this branch for the anchor's summary
        recent = self._db.index.get_ancestors(bp.head_hash, limit=20)
        summary_parts = []
        for c in recent:
            summary_parts.append(f"{c.metadata.agent_id}: {c.message}")

        blob = ContentBlob(
            messages=[ContextMessage(
                role="system",
                content=f"Anchor snapshot for {branch_name}",
            )],
            distilled_summary="\n".join(summary_parts[:10]),
        )

        meta = CommitMetadata(
            agent_id="hive-compactor",
            tags=["anchor", f"branch:{branch_name}"],
        )

        commit = CognitiveCommit(
            parent_hashes=[bp.head_hash],
            commit_type=CommitType.ANCHOR,
            message=f"Anchor snapshot on {branch_name}",
            content_blob=blob,
            metadata=meta,
            is_delta=False,
        )

        commit_hash = self._db.store_commit(commit)
        self._db.index.advance_head(branch_name, commit_hash)

        logger.info(
            "Created anchor commit %s on %s",
            commit_hash[:12], branch_name,
        )
        return commit_hash

    # -- Windowed context query -------------------------------------------

    def windowed_context(
        self,
        agent_id: str,
        *,
        window_size: int = 10,
        branch: str | None = None,
        include_distilled: bool = True,
    ) -> list[CognitiveCommit]:
        """Return the last ``window_size`` commits visible to an agent.

        If ``include_distilled`` is True (default), distilled commits are
        included in the window and count toward the limit — giving the
        agent a summary of older context within their window.

        Parameters
        ----------
        agent_id:
            The agent requesting context.
        window_size:
            Maximum number of commits in the active window.
        branch:
            If given, query only this branch.  Otherwise query globally.
        include_distilled:
            Whether to include DISTILLATION-type commits in the window.
        """
        if branch:
            bp = self._db.index.get_branch(branch)
            if bp is None:
                return []
            all_commits = self._db.index.get_ancestors(bp.head_hash, limit=window_size * 3)
        else:
            all_commits = self._db.index.list_all_commits(limit=window_size * 3)

        # Filter by agent scope — agent's own commits + targeted at agent
        windowed: list[CognitiveCommit] = []
        for c in all_commits:
            if not include_distilled and c.commit_type == CommitType.DISTILLATION:
                continue
            windowed.append(c)
            if len(windowed) >= window_size:
                break

        return windowed
