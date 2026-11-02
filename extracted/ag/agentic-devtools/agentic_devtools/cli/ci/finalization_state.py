"""Durable finalization state for review-level thread resolution."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from agentic_devtools.cli.ci.comment_format import normalize_ai_pr_loop_comment
from agentic_devtools.cli.ci.provider import trusted_loop_comment_logins

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)

_FINALIZED_REVIEW_MARKER = re.compile(
    r"<!--\s*ai-pr-loop:finalized-review\s+(.+?)\s*-->",
    re.DOTALL,
)

FINALIZED_REVIEW_TRACKING_SENTINEL = "<!-- agdt:ai-pr-loop-tracking -->"
FINALIZED_REVIEW_TRACKING_HEADER = (
    "### 🤖 AI PR Loop State & Finalized Reviews\nAutomated review finalization and loop state tracking."
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
        self._tracking_comment_cache: dict[int, tuple[int, str]] = {}

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
            trusted_authors = trusted_loop_comment_logins(self._provider)
        except Exception as exc:
            logger.warning(
                "Failed to resolve finalized-review author for PR #%d review %d: %s",
                key.pr_number,
                key.review_id,
                exc,
            )
            return False
        if not trusted_authors:
            return False

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
            if comment.author.casefold() not in trusted_authors:
                continue
            body = comment.body or ""
            normalized_body = normalize_ai_pr_loop_comment(body)
            if normalized_body is None:
                if FINALIZED_REVIEW_TRACKING_SENTINEL in body or _FINALIZED_REVIEW_MARKER.search(body):
                    raise ValueError("Trusted finalized-review state has a malformed terminal label")
                continue
            for marker_match in _FINALIZED_REVIEW_MARKER.finditer(normalized_body):
                parsed = _parse_finalized_review_payload(marker_match.group(1))
                if parsed is not None:
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
        marker = f"<!-- ai-pr-loop:finalized-review {json.dumps(payload, sort_keys=True)} -->"

        existing_comment: tuple[int, str] | None = None
        try:
            trusted_authors = trusted_loop_comment_logins(self._provider)
            comments = self._provider.list_issue_comments(key.pr_number)
        except Exception as exc:
            logger.warning(
                "Failed to find tracking comment for PR #%d: %s",
                key.pr_number,
                exc,
            )
            trusted_authors = set()
            comments = []

        for c in reversed(comments):
            if getattr(c, "author", "").casefold() not in trusted_authors:
                continue
            c_body = getattr(c, "body", "") or ""
            normalized_body = normalize_ai_pr_loop_comment(c_body)
            if normalized_body is None:
                if FINALIZED_REVIEW_TRACKING_SENTINEL in c_body or _FINALIZED_REVIEW_MARKER.search(c_body):
                    raise ValueError("Trusted finalized-review state has a malformed terminal label")
                continue
            if FINALIZED_REVIEW_TRACKING_SENTINEL in normalized_body or _FINALIZED_REVIEW_MARKER.search(
                normalized_body
            ):
                existing_comment = (c.id, normalized_body)
                break

        cached_tracking_comment = self._tracking_comment_cache.get(key.pr_number)
        if cached_tracking_comment is not None and (
            existing_comment is None or cached_tracking_comment[0] > existing_comment[0]
        ):
            existing_comment = cached_tracking_comment

        try:
            update_comment = getattr(self._provider, "update_comment", None)
            if existing_comment is not None and callable(update_comment):
                existing_comment_id, existing_body = existing_comment
                updated_body = f"{existing_body}\n{marker}"
                if FINALIZED_REVIEW_TRACKING_SENTINEL not in updated_body and not updated_body.startswith("#"):
                    updated_body = (
                        f"{FINALIZED_REVIEW_TRACKING_HEADER}\n{FINALIZED_REVIEW_TRACKING_SENTINEL}\n\n{updated_body}"
                    )
                migrated_comment_id = update_comment(existing_comment_id, updated_body)
                self._tracking_comment_cache[key.pr_number] = (
                    migrated_comment_id
                    if type(migrated_comment_id) is int and migrated_comment_id > 0
                    else existing_comment_id,
                    updated_body,
                )
            else:
                new_body = f"{FINALIZED_REVIEW_TRACKING_HEADER}\n{FINALIZED_REVIEW_TRACKING_SENTINEL}\n\n{marker}"
                new_comment_id = self._provider.post_comment(key.pr_number, new_body)
                if type(new_comment_id) is int and new_comment_id > 0:
                    self._tracking_comment_cache[key.pr_number] = (new_comment_id, new_body)
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


def _parse_finalized_review_payload(raw_json: str) -> FinalizedReviewKey | None:
    try:
        data = json.loads(raw_json)
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


def _parse_finalized_review_marker(body: str) -> FinalizedReviewKey | None:
    """Parse one finalized-review marker body into a validated key."""
    if not isinstance(body, str):
        return None
    normalized_body = normalize_ai_pr_loop_comment(body)
    if normalized_body is None:
        return None
    match = _FINALIZED_REVIEW_MARKER.search(normalized_body)
    if match is None:
        return None
    return _parse_finalized_review_payload(match.group(1))
