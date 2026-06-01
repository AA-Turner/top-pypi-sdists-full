# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Utility functions for repository operations.

This module provides helper functions for parsing PR information and resolving
git diff ranges for connector change detection.
"""

from __future__ import annotations

import os
import re


def parse_pr_info(pr_num_or_url: str) -> tuple[int | None, str | None, str | None]:
    """Parse PR number, owner, and repo from string or URL.

    Args:
        pr_num_or_url: PR number (e.g., "123") or URL (e.g., "https://github.com/airbytehq/airbyte/pull/123")

    Returns:
        Tuple of (pr_number, pr_owner, pr_repo)
    """
    # If it's all digits, just return PR number
    if pr_num_or_url.isdigit():
        return int(pr_num_or_url), None, None

    # Parse URL: https://github.com/airbytehq/airbyte-enterprise/pull/123
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)", pr_num_or_url)
    if m:
        pr_owner = m.group(1)
        pr_repo = m.group(2)
        pr_number = int(m.group(3))
        return pr_number, pr_owner, pr_repo

    return None, None, None


def detect_env_pr_info() -> tuple[int | None, str | None, str | None]:
    """Detect PR number, owner, and repo from GitHub Actions environment variables.

    Returns:
        Tuple of (pr_number, pr_owner, pr_repo)
    """
    # Try to extract PR number from GITHUB_REF (e.g., "refs/pull/123/merge")
    github_ref = os.getenv("GITHUB_REF", "")
    m = re.match(r"refs/pull/(\d+)/", github_ref)
    pr_number = int(m.group(1)) if m else None

    # Try to extract owner and repo from GITHUB_REPOSITORY (e.g., "airbytehq/airbyte")
    pr_owner = None
    pr_repo = None
    github_repo = os.getenv("GITHUB_REPOSITORY", "")
    if github_repo and "/" in github_repo:
        parts = github_repo.split("/", 1)
        pr_owner = parts[0]
        pr_repo = parts[1]

    return pr_number, pr_owner, pr_repo


def resolve_diff_range(
    pr_num_or_url: str | None,
) -> tuple[str, str, int | None, str | None, str | None]:
    """Resolve PR info to base_ref and head_ref for git diff.

    Args:
        pr_num_or_url: PR number, URL, or None to auto-detect from environment

    Returns:
        Tuple of (base_ref, head_ref, pr_number, pr_owner, pr_repo)
    """
    pr_number = None
    pr_owner = None
    pr_repo = None

    # Try to get PR info from parameter or environment
    if pr_num_or_url:
        pr_number, pr_owner, pr_repo = parse_pr_info(pr_num_or_url)
    else:
        pr_number, pr_owner, pr_repo = detect_env_pr_info()

    # Backfill owner/repo from GITHUB_REPOSITORY when only PR number is known
    # (e.g. --pr 75600 without a full URL, running inside GitHub Actions)
    if pr_number is not None and (pr_owner is None or pr_repo is None):
        _env_number, env_owner, env_repo = detect_env_pr_info()
        if env_owner and env_repo:
            pr_owner = pr_owner or env_owner
            pr_repo = pr_repo or env_repo

    # Determine base_ref and head_ref based on PR detection
    if pr_number is not None:
        # PR detected - use origin/{base_branch} vs HEAD (assumes CI checked out the PR)
        # Use GITHUB_BASE_REF if available (set by GitHub Actions for PRs)
        # This handles repos with different default branches (main, master, etc.)
        base_branch = os.getenv("GITHUB_BASE_REF") or "master"
        base_ref = f"origin/{base_branch}"
        head_ref = "HEAD"
    else:
        # No PR detected - fallback to HEAD~1 vs HEAD (post-merge use case)
        base_ref = "HEAD~1"
        head_ref = "HEAD"

    return base_ref, head_ref, pr_number, pr_owner, pr_repo
