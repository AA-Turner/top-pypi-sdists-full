#!/usr/bin/env python3
"""Cleanup redundant collapsed summary comments on pull requests.

Finds and deletes comments containing the sentinel:
``<!-- agdt:ai-pr-loop-summary-collapsed -->``
on specified pull requests.

Usage:
    python scripts/cleanup_pr_summary_comments.py --repo swai-factory/agentic-devtools 4182 4162 4137
    python scripts/cleanup_pr_summary_comments.py --dry-run 4182
"""

from __future__ import annotations

import argparse
import logging
import os
import sys

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.pipeline.summary import SUMMARY_COLLAPSED_SENTINEL
from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)


def cleanup_collapsed_summaries(
    provider: CIPlatformProvider,
    pr_number: int,
    *,
    dry_run: bool = False,
) -> int:
    """Find and delete collapsed AI PR loop summary comments on a PR.

    Args:
        provider: CI platform provider instance.
        pr_number: Pull request number.
        dry_run: If True, log comment IDs without deleting them.

    Returns:
        Number of collapsed comments deleted (or identified for deletion in dry-run).
    """
    list_issue_comments = getattr(provider, "list_issue_comments", None)
    if not callable(list_issue_comments):
        logger.error("PR #%d: Provider does not support list_issue_comments", pr_number)
        return 0

    comments = list_issue_comments(pr_number)
    collapsed_comments = [c for c in comments if SUMMARY_COLLAPSED_SENTINEL in (c.body or "")]

    logger.info("PR #%d: Found %d collapsed summary comment(s)", pr_number, len(collapsed_comments))
    deleted_count = 0
    for comment in collapsed_comments:
        if dry_run:
            logger.info("PR #%d: [DRY-RUN] Would delete comment %d", pr_number, comment.id)
            deleted_count += 1
        else:
            try:
                provider.delete_comment(comment.id)
                logger.info("PR #%d: Deleted comment %d", pr_number, comment.id)
                deleted_count += 1
            except Exception as exc:
                logger.warning("PR #%d: Failed to delete comment %d: %s", pr_number, comment.id, exc)

    return deleted_count


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Delete redundant collapsed summary comments from specified PRs.")
    parser.add_argument(
        "prs",
        nargs="*",
        type=int,
        help="PR numbers to clean up (e.g. 4182 4162 4137).",
    )
    parser.add_argument(
        "--repo",
        default=os.environ.get("GITHUB_REPOSITORY", ""),
        help="Repository in 'owner/repo' format (defaults to GITHUB_REPOSITORY).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only list comments that would be deleted without deleting them.",
    )
    return parser.parse_args(args)


def main(args: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    parsed = parse_args(args)
    prs = parsed.prs
    if not prs:
        prs = [4182, 4162, 4137]
        logger.info("No PR numbers specified; using default targets: %s", prs)

    provider = GitHubActionsProvider(repo=parsed.repo)
    total_deleted = 0
    for pr_number in prs:
        deleted = cleanup_collapsed_summaries(provider, pr_number, dry_run=parsed.dry_run)
        total_deleted += deleted

    mode_str = "identified for deletion (dry-run)" if parsed.dry_run else "deleted"
    logger.info("Total collapsed comments %s across %d PR(s): %d", mode_str, len(prs), total_deleted)
    return 0


if __name__ == "__main__":
    sys.exit(main())
