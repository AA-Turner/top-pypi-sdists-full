"""Durable repair reservations; uncertain dispatches consume their attempt.

The companion marker deliberately does not match the global ``repair-dispatch:``
prefix: the global guard owns and rewrites that separate per-HEAD counter.
Callers must serialize PR processing; comment writes are not CAS.
"""

from __future__ import annotations

import json
import logging
import re

from agentic_devtools.cli.ci.comment_format import normalize_ai_pr_loop_comment
from agentic_devtools.cli.ci.guards import AGENT_FAILED_LABEL
from agentic_devtools.cli.ci.models import ReviewCommentInfo
from agentic_devtools.cli.ci.provider import CIPlatformProvider, trusted_loop_comment_logins

#: Raised when workflow identity cannot be resolved to trust/reject a marker.
#: Distinct from envelope and marker-identity validation errors.
_IDENTITY_ERROR = "Cannot establish the authenticated workflow identity for repair attempt markers"
_ATTEMPT_KEY_PATTERN = r"(root|review):[1-9]\d*|synthetic:[1-9]\d*:-[1-9]\d*|critique:[1-9]\d*:[12]|ci"

logger = logging.getLogger(__name__)


class RepairAttemptTracker:
    """Track one attempt per finding/HEAD and one human escalation per finding."""

    def __init__(self, provider: CIPlatformProvider, pr_number: int, head_sha: str) -> None:
        if type(pr_number) is not int or pr_number <= 0:
            raise ValueError("Invalid repair PR number")
        if not isinstance(head_sha, str) or not re.fullmatch(r"[A-Za-z0-9._-]+", head_sha):
            raise ValueError("Invalid repair HEAD")
        self.provider = provider
        self.pr_number = pr_number
        self.head_sha = head_sha
        self.prefix = f"<!-- repair-dispatch-findings:{pr_number}:{head_sha}:"
        self.marker = self.prefix + "v1 -->"
        self.attempted: set[str] = set()
        self.comment_id: int | None = None
        existing = self._find_trusted_comment(self.prefix)
        if existing is not None:
            if not (
                isinstance(existing, tuple)
                and len(existing) == 2
                and type(existing[0]) is int
                and existing[0] > 0
                and isinstance(existing[1], str)
                and existing[1].startswith(self.marker + "\n")
            ):
                raise ValueError("Malformed repair attempt marker")
            normalized_body = normalize_ai_pr_loop_comment(existing[1])
            if normalized_body is None:
                raise ValueError("Malformed repair attempt marker")
            self.comment_id = existing[0]
            data = json.loads(normalized_body[len(self.marker) + 1 :])
            if (
                not isinstance(data, dict)
                or set(data) != {"attempted"}
                or not isinstance(data["attempted"], list)
                or any(
                    not isinstance(key, str) or not re.fullmatch(_ATTEMPT_KEY_PATTERN, key) for key in data["attempted"]
                )
            ):
                raise ValueError("Malformed repair attempt identities")
            self.attempted = set(data["attempted"])

    def _find_trusted_comment(self, needle: str) -> tuple[int, str] | None:
        """Find the newest comment containing ``needle``, trusting only the workflow-token author.

        ``provider.find_comment`` matches by marker text alone, so any PR commenter
        could post a comment containing the marker and spoof a reservation or
        escalation. A candidate comment is trusted only when it was posted by the
        authenticated workflow-token identity (mirrors the deferral-marker trust
        model in ``pipeline/deferral.py``); comments from any other author are
        ignored, as if they did not exist, so a forged marker cannot suppress or
        falsely escalate genuine repair work.
        """
        candidates = [
            comment
            for comment in self.provider.list_issue_comments(self.pr_number)
            if isinstance(comment.body, str) and needle in comment.body
        ]
        if not candidates:
            return None
        trusted_logins = trusted_loop_comment_logins(self.provider)
        if not trusted_logins:
            raise ValueError(_IDENTITY_ERROR)
        matching = [
            comment
            for comment in candidates
            if isinstance(comment.author, str) and comment.author.casefold() in trusted_logins
        ]
        if not matching:
            return None
        newest = max(matching, key=lambda c: c.id)
        return newest.id, newest.body

    @staticmethod
    def finding_key(review_id: int, comment: ReviewCommentInfo) -> str | None:
        """Native roots persist across reviews; negative IDs are review-local."""
        if type(review_id) is not int or review_id <= 0:
            raise ValueError("Invalid repair review ID")
        if type(comment.id) is not int or comment.id == 0:
            raise ValueError("Invalid repair finding ID")
        if comment.in_reply_to_id is not None and (
            type(comment.in_reply_to_id) is not int or comment.in_reply_to_id <= 0
        ):
            raise ValueError("Invalid repair parent finding ID")
        if comment.id < 0:
            return f"synthetic:{review_id}:{comment.id}"
        if comment.in_reply_to_id is None:
            return f"root:{comment.id}"
        return None

    def filter_review(
        self,
        review_id: int,
        comments: list[ReviewCommentInfo],
        resolved_ids: set[int],
    ) -> list[ReviewCommentInfo]:
        """Escalate attempted unresolved roots, even those with agent replies."""
        if not isinstance(comments, list) or any(not isinstance(c, ReviewCommentInfo) for c in comments):
            raise ValueError("Malformed repair review comments")
        remaining: list[ReviewCommentInfo] = []
        for comment in comments:
            key = self.finding_key(review_id, comment)
            if comment.id > 0 and comment.id in resolved_ids:
                continue
            if key in self.attempted:
                assert key is not None
                self.escalate(key)
                continue
            if comment.in_reply_to_id is not None and f"root:{comment.in_reply_to_id}" in self.attempted:
                continue
            remaining.append(comment)
        return remaining

    def resolved_ids(self) -> set[int]:
        """Require a successful, well-formed thread read; propagate rate limits."""
        states = self.provider.list_review_thread_states(self.pr_number)
        if not isinstance(states, dict) or any(
            type(key) is not int
            or key <= 0
            or not isinstance(value, tuple)
            or len(value) != 2
            or any(type(flag) is not bool for flag in value)
            for key, value in states.items()
        ):
            raise ValueError("Malformed required repair thread state")
        return {key for key, value in states.items() if value[0]}

    def escalate(self, key: str, *, reason: str | None = None) -> None:
        """Notify humans once; labels are best-effort, without assigning anybody."""
        explanation = reason or (
            "the repair attempt is exhausted and the finding remains unresolved. No automatic retry will be dispatched."
        )
        marker = f"<!-- repair-dispatch-escalation:v1:{self.pr_number}:{self.head_sha}:{key} -->"
        existing = self._find_trusted_comment(marker)
        # Labels are idempotent and may need restoring after a partial failure.
        # A label failure (even a label endpoint rate limit) must not block the
        # human notification or unrelated findings. Required marker/state reads
        # and notification writes still propagate failures, including cooldowns.
        try:
            self.provider.add_label(self.pr_number, AGENT_FAILED_LABEL)
        except Exception as exc:
            logger.warning(
                "PR #%d: Failed to add %s for finding %s; continuing human escalation: %s",
                self.pr_number,
                AGENT_FAILED_LABEL,
                key,
                exc,
            )
        if existing is not None:
            if not (
                isinstance(existing, tuple)
                and len(existing) == 2
                and type(existing[0]) is int
                and existing[0] > 0
                and isinstance(existing[1], str)
                and existing[1].startswith(marker + "\n")
            ):
                raise ValueError("Malformed repair escalation marker")
            return
        comment_id = self.provider.post_comment(
            self.pr_number,
            f"{marker}\nHuman intervention required for PR #{self.pr_number}, "
            f"HEAD `{self.head_sha}`, finding `{key}`: {explanation}",
        )
        if type(comment_id) is not int or comment_id <= 0:
            raise ValueError("Repair escalation was not persisted")

    def reserve(self, keys: set[str]) -> None:
        """Persist before dispatch; never release a failed/uncertain attempt."""
        if not keys or keys & self.attempted:
            raise ValueError("Repair attempt already reserved or empty")
        body = self.marker + "\n" + json.dumps({"attempted": sorted(self.attempted | keys)})
        if self.comment_id is None:
            comment_id = self.provider.post_comment(self.pr_number, body)
            if type(comment_id) is not int or comment_id <= 0:
                raise ValueError("Repair reservation was not persisted")
            self.comment_id = comment_id
        else:
            migrated_comment_id = self.provider.update_comment(self.comment_id, body)
            if migrated_comment_id is not None:
                if type(migrated_comment_id) is not int or migrated_comment_id <= 0:
                    raise ValueError("Repair reservation migration returned an invalid comment ID")
                self.comment_id = migrated_comment_id
        confirmed = self.provider.find_comment(self.pr_number, self.prefix)
        if not isinstance(confirmed, tuple) or confirmed != (self.comment_id, body) or type(confirmed[0]) is not int:
            raise ValueError("Repair reservation could not be confirmed")
        self.attempted.update(keys)

    def release(self, keys: set[str]) -> None:
        """Remove reservations only after the provider confirms no creation was attempted."""
        if not keys or not keys <= self.attempted:
            raise ValueError("Repair reservation is not active")
        if self.comment_id is None:
            raise ValueError("Repair reservation was not persisted")
        remaining = self.attempted - keys
        body = self.marker + "\n" + json.dumps({"attempted": sorted(remaining)})
        self.provider.update_comment(self.comment_id, body)
        confirmed = self.provider.find_comment(self.pr_number, self.prefix)
        if not isinstance(confirmed, tuple) or confirmed != (self.comment_id, body) or type(confirmed[0]) is not int:
            raise ValueError("Repair reservation release could not be confirmed")
        self.attempted = remaining
