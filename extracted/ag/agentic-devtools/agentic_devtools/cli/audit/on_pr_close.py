"""PR close trigger for the audit workflow.

Checks whether the threshold of unaudited closed PRs has been met
and dispatches the audit workflow if so.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys

from agentic_devtools.cli.audit.config import (
    LABEL_AUDITED,
    LABEL_IN_PROGRESS,
    resolve_threshold,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.github.repo_resolution import resolve_github_repo

logger = logging.getLogger(__name__)


def check_threshold_and_dispatch(
    provider: CIPlatformProvider,
    threshold: int | None,
    repo_path: str,
) -> bool:
    """Check if the unaudited PR threshold is met and signal dispatch.

    Args:
        provider: CI platform provider instance.
        threshold: Explicit threshold (None to resolve from config).
        repo_path: Path to the repository root.

    Returns:
        True if threshold is met (audit should run), False otherwise.

    Raises:
        NotImplementedError: If the provider does not support threshold counting.
        Exception: On provider/API errors.
    """
    resolved_threshold = resolve_threshold(threshold, repo_path)

    unaudited_count = provider.count_prs_without_labels(
        exclude_labels=[LABEL_AUDITED, LABEL_IN_PROGRESS],
        state="closed",
    )

    logger.info(
        "Unaudited closed PRs: %d (threshold: %d)",
        unaudited_count,
        resolved_threshold,
    )

    if unaudited_count >= resolved_threshold:
        logger.info("Threshold met — audit should be dispatched")
        return True

    logger.info("Threshold not met — no audit needed")
    return False


def on_pr_close_command() -> None:
    """CLI entry point for agdt-audit-on-pr-close.

    Checks unaudited PR count against threshold and exits with
    appropriate code to signal whether audit should be dispatched.

    Exit codes:
        0: Threshold met — audit should run
        1: Error occurred (provider/API failure)
        2: Threshold not met — no action needed
    """
    parser = argparse.ArgumentParser(description="Check audit threshold on PR close")
    parser.add_argument("--threshold", type=int, default=None, help="Override threshold count")
    parser.add_argument("--repo", type=str, default=None, help="Repository (owner/repo)")
    args = parser.parse_args()

    from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

    repo = resolve_github_repo(args.repo or os.environ.get("GITHUB_REPOSITORY"))
    provider = GitHubActionsProvider(repo=repo)
    repo_path = os.environ.get("GITHUB_WORKSPACE", os.getcwd())

    try:
        should_dispatch = check_threshold_and_dispatch(provider, args.threshold, repo_path)
    except Exception:
        logger.error("Error checking audit threshold", exc_info=True)
        print("AUDIT_THRESHOLD_MET=error")
        sys.exit(1)

    if should_dispatch:
        print("AUDIT_THRESHOLD_MET=true")
        sys.exit(0)
    else:
        print("AUDIT_THRESHOLD_MET=false")
        sys.exit(2)
