"""GitHub push attribution: scan commits since a persisted watermark."""

from __future__ import annotations

import json
import logging
from typing import Any

from agentic_devtools.cli.ci.github_provider import _gh_api
from agentic_devtools.cli.ci.reconciliation import config

logger = logging.getLogger(__name__)

MAX_PAGES = config.MAX_PAGINATION_PAGES_PER_RUN


def list_commits_since_watermark(
    repo: str,
    watermark: str,
    *,
    pr_number: int | None = None,
    head_ref: str | None = None,
    per_page: int = 30,
    max_pages: int = MAX_PAGES,
    scan_state: dict[str, bool] | None = None,
) -> list[dict[str, Any]]:
    """Return commits newer than *watermark*, oldest first.

    When ``pr_number`` or ``head_ref`` is provided, the history is scoped to
    that pull-request head instead of the repository's default branch.
    """
    if per_page < 1 or per_page > 100:
        raise ValueError(f"per_page must be between 1 and 100, got {per_page}")
    if max_pages < 1:
        raise ValueError(f"max_pages must be >= 1, got {max_pages}")

    commits: list[dict[str, Any]] = []
    watermark_reached = False
    history_exhausted = False
    pull_request_history = pr_number is not None
    for page in range(1, max_pages + 1):
        if pull_request_history:
            assert pr_number is not None
            if isinstance(pr_number, bool) or pr_number < 1:
                raise ValueError("pr_number must be a positive integer")
            endpoint = f"/repos/{repo}/pulls/{pr_number}/commits?per_page={per_page}&page={page}"
        else:
            ref_query = f"&sha={head_ref}" if head_ref else ""
            endpoint = f"/repos/{repo}/commits?per_page={per_page}&page={page}{ref_query}"
        response = _gh_api(endpoint)
        page_commits = json.loads(response)
        if not isinstance(page_commits, list):
            raise ValueError(f"GitHub commits response must be a list, got {type(page_commits).__name__}")
        if not page_commits:
            history_exhausted = True
            break

        if pull_request_history:
            page_items: list[dict[str, Any]] = []
            for commit in page_commits:
                if not isinstance(commit, dict):
                    raise ValueError(f"GitHub commits response must contain objects, got {type(commit).__name__}")
                page_items.append(commit)
            if watermark:
                if not watermark_reached:
                    watermark_index = next(
                        (index for index, commit in enumerate(page_items) if commit.get("sha", "") == watermark),
                        None,
                    )
                    if watermark_index is not None:
                        watermark_reached = True
                        commits.extend(page_items[watermark_index + 1 :])
                else:
                    commits.extend(page_items)
            else:
                commits.extend(page_items)
        else:
            for commit in page_commits:
                if not isinstance(commit, dict):
                    raise ValueError(f"GitHub commits response must contain objects, got {type(commit).__name__}")
                sha = commit.get("sha", "")
                if sha == watermark:
                    watermark_reached = True
                    break
                commits.append(commit)

        if len(page_commits) < per_page:
            history_exhausted = True
        if (not pull_request_history and watermark_reached) or len(page_commits) < per_page:
            break

    watermark_found = not watermark or watermark_reached
    scan_complete = history_exhausted or watermark_found
    if watermark and not watermark_found:
        logger.warning(
            "Commit watermark %r was not found after scanning up to %d page(s) for %s",
            watermark,
            max_pages,
            repo,
        )
    if scan_state is not None:
        scan_state.update(
            {
                "watermark_found": watermark_found,
                "scan_complete": scan_complete,
            }
        )

    if not pull_request_history:
        commits.reverse()
    logger.debug("Loaded %d commits since watermark %r for %s", len(commits), watermark, repo)
    return commits
