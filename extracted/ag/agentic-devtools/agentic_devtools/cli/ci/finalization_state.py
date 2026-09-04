"""Durable finalization state for review-level thread resolution."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)

_FINALIZED_REVIEW_MARKER = re.compile(
    r"<!--\s*ai-pr-loop:finalized-review\s+(.+?)\s*-->",
    re.DOTALL,
)


@dataclass(frozen=True)
class FinalizedReviewKey:
    """Logical key for one finalized review."""

    repository: str
    pr_number: int
    review_id: int


class PRCommentFinalizationStateStore:
    """Repository-backed finalization state using PR issue comments."""

    def __init__(self, provider: CIPlatformProvider) -> None:
        self._provider = provider
        self._cache_attr = "_finalized_review_keys_cache"

    def _get_cached_terminal_keys(self, pr_number: int) -> set[FinalizedReviewKey] | None:
        """Return cached terminal keys for a PR when available."""
        cache = getattr(self._provider, self._cache_attr, None)
        if not isinstance(cache, dict):
            return None
        terminal_keys = cache.get(pr_number)
        if not isinstance(terminal_keys, set):
            return None
        return terminal_keys

    def _set_cached_terminal_keys(self, pr_number: int, terminal_keys: set[FinalizedReviewKey]) -> None:
        """Cache terminal keys for a PR on the provider instance."""
        cache = getattr(self._provider, self._cache_attr, None)
        if not isinstance(cache, dict):
            cache = {}
            setattr(self._provider, self._cache_attr, cache)
        cache[pr_number] = terminal_keys

    def is_terminal(self, *, key: FinalizedReviewKey) -> bool:
        """Return whether this review was previously finalized."""
        cached_keys = self._get_cached_terminal_keys(key.pr_number)
        if cached_keys is not None:
            return key in cached_keys

        try:
            pr_token_login = self._provider.get_pr_token_login()
        except Exception as exc:
            logger.warning(
                "Failed to resolve finalized-review author for PR #%d review %d: %s",
                key.pr_number,
                key.review_id,
                exc,
            )
            return False
        if not isinstance(pr_token_login, str) or not pr_token_login:
            return False
        trusted_author = pr_token_login.casefold()

        try:
            comments = self._provider.list_issue_comments(key.pr_number)
        except Exception as exc:
            logger.warning(
                "Failed to read finalized-review state for PR #%d review %d: %s",
                key.pr_number,
                key.review_id,
                exc,
            )
            return False

        terminal_keys: set[FinalizedReviewKey] = set()
        for comment in reversed(comments):
            if trusted_author and comment.author.casefold() != trusted_author:
                continue
            parsed = _parse_finalized_review_marker(comment.body)
            if parsed is None:
                continue
            terminal_keys.add(parsed)
        self._set_cached_terminal_keys(key.pr_number, terminal_keys)
        return key in terminal_keys

    def mark_terminal(self, *, key: FinalizedReviewKey, reason: str) -> None:
        """Persist terminal finalization state for one review."""
        payload = {
            "repo": key.repository,
            "pr": key.pr_number,
            "review_id": key.review_id,
            "reason": reason,
        }
        body = f"<!-- ai-pr-loop:finalized-review {json.dumps(payload, sort_keys=True)} -->"
        try:
            self._provider.post_comment_as_pr_token(key.pr_number, body)
        except Exception as exc:
            logger.warning(
                "Failed to persist finalized-review state for PR #%d review %d: %s",
                key.pr_number,
                key.review_id,
                exc,
            )
            return
        terminal_keys = self._get_cached_terminal_keys(key.pr_number)
        if terminal_keys is None:
            terminal_keys = set()
        terminal_keys.add(key)
        self._set_cached_terminal_keys(key.pr_number, terminal_keys)


def _parse_finalized_review_marker(body: str) -> FinalizedReviewKey | None:
    """Parse one finalized-review marker body into a validated key."""
    if not isinstance(body, str):
        return None
    match = _FINALIZED_REVIEW_MARKER.search(body)
    if match is None:
        return None
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None

    repo = data.get("repo")
    pr = data.get("pr")
    review_id = data.get("review_id")
    if (
        not isinstance(repo, str)
        or not repo
        or type(pr) is not int
        or pr <= 0
        or type(review_id) is not int
        or review_id <= 0
    ):
        return None
    return FinalizedReviewKey(repository=repo, pr_number=pr, review_id=review_id)
