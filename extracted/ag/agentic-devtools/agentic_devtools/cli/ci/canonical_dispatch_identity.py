"""Canonical immutable identity for a repair dispatch."""

from __future__ import annotations

import re
from dataclasses import dataclass

_REPO_SEGMENT_RE = re.compile(r"[a-z0-9_.][a-z0-9_.-]*")
_HEAD_SHA_RE = re.compile(r"[0-9a-f]{40}")
_WORK_DIGEST_RE = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True)
class CanonicalDispatchIdentity:
    """Six-field repair identity; review ID zero is reserved for check-only work.

    This context-free model accepts zero as the check-only sentinel. A later
    identity builder must ensure that zero is used only for check-only work.
    """

    repo: str
    pull_request_id: int
    head_sha: str
    review_id: int
    work_digest: str
    ordinal: int

    def __post_init__(self) -> None:
        if not isinstance(self.repo, str):
            raise ValueError("repo must be a canonical lowercase owner/name")
        segments = self.repo.split("/")
        if len(segments) != 2:
            raise ValueError("repo must be a canonical lowercase owner/name")
        owner, name = segments
        if not _REPO_SEGMENT_RE.fullmatch(owner) or owner in {".", ".."}:
            raise ValueError("repo must contain valid lowercase owner and repository slugs")
        if not _REPO_SEGMENT_RE.fullmatch(name) or name in {".", ".."}:
            raise ValueError("repo must contain valid lowercase owner and repository slugs")
        if (
            isinstance(self.pull_request_id, bool)
            or not isinstance(self.pull_request_id, int)
            or self.pull_request_id <= 0
        ):
            raise ValueError("pull_request_id must be a positive integer")
        if isinstance(self.review_id, bool) or not isinstance(self.review_id, int) or self.review_id < 0:
            raise ValueError("review_id must be a nonnegative integer")
        if not isinstance(self.head_sha, str) or not _HEAD_SHA_RE.fullmatch(self.head_sha):
            raise ValueError("head_sha must be 40 lowercase hexadecimal characters")
        if not isinstance(self.work_digest, str) or not _WORK_DIGEST_RE.fullmatch(self.work_digest):
            raise ValueError("work_digest must be 64 lowercase hexadecimal characters")
        if isinstance(self.ordinal, bool) or not isinstance(self.ordinal, int) or self.ordinal <= 0:
            raise ValueError("ordinal must be a positive integer")

    @property
    def key(self) -> str:
        """Return the canonical six-field key."""
        return f"{self.repo}:{self.pull_request_id}:{self.head_sha}:{self.review_id}:{self.work_digest}:{self.ordinal}"

    @property
    def retry_key(self) -> tuple[str, int, str, int, str]:
        """Return the five identity fields that determine retry equivalence."""
        return (self.repo, self.pull_request_id, self.head_sha, self.review_id, self.work_digest)
