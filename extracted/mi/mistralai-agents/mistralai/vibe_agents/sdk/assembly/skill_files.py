"""Shared file representation for local and Registry skills."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from dataclasses import dataclass, field

from temporalio.exceptions import ApplicationError

_NON_SLUG_CHARS = re.compile(r"[^a-z0-9]+")
_MAX_SLUG_LENGTH = 64
SKILL_DIGEST_LENGTH = 12


class SkillProvisioningError(ApplicationError):
    """A declared skill cannot be turned into a folder the sandbox can serve.

    A retry gives the same result unless the cause is transient, so the sandbox write that
    raises it is not retried by default.
    """

    def __init__(self, message: str, *, non_retryable: bool = True) -> None:
        super().__init__(message, type=type(self).__name__, non_retryable=non_retryable)


@dataclass(frozen=True, slots=True)
class SkillFiles:
    """One skill resolved to the files of its folder, keyed by POSIX path relative to the folder."""

    name: str
    description: str
    files: Mapping[str, bytes]
    executable: frozenset[str] = frozenset()
    digest: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        digest = hashlib.sha256()
        for path in sorted(self.files):
            for value in (path.encode(), self.files[path], b"x" if path in self.executable else b"-"):
                digest.update(len(value).to_bytes(8, "big"))
                digest.update(value)
        object.__setattr__(self, "digest", digest.hexdigest())

    @property
    def directory(self) -> str:
        """Folder name under the root: content-addressed, so a changed skill gets a new path."""

        slug = _NON_SLUG_CHARS.sub("-", self.name.lower()).strip("-")[:_MAX_SLUG_LENGTH].rstrip("-")
        return f"{slug or 'skill'}-{self.digest[:SKILL_DIGEST_LENGTH]}"


__all__ = ["SKILL_DIGEST_LENGTH", "SkillFiles", "SkillProvisioningError"]
