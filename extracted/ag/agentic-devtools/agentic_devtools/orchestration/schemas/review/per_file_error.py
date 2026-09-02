"""PerFileReviewError model for resumable per-file review failures.

Records a terminal-for-this-run per-file failure so resume logic can
distinguish retryable pending files from operator-blocked files.  A reviewed
PR file persists either one terminal ``FileReviewResult`` or one
``PerFileReviewError`` for the current outcome, never both simultaneously.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ErrorKind = Literal[
    "malformed_output",
    "rate_limit",
    "transient_provider",
    "unsupported_configuration",
    "unknown",
]

# ``retryable`` is a fixed function of ``error_kind`` (FR-005/FR-012): only
# transient/malformed failures are retried on the next invocation; configuration
# and unknown failures block the file until an operator intervenes.
_RETRYABLE_KINDS: frozenset[str] = frozenset({"malformed_output", "rate_limit", "transient_provider"})


class PerFileReviewError(BaseModel):
    """A resumable per-file review failure record."""

    model_config = ConfigDict(validate_assignment=True)

    file_path: str = Field(description="Repository-relative path of the file that failed review")
    request_id: str | None = Field(default=None, description="Identifier of the request/chunk that failed")
    chunk_id: str | None = Field(default=None, description="Identifier of the diff chunk that failed, when chunked")
    model_id: str = Field(default="", description="Identifier of the model used for the attempt")
    attempt_count: int = Field(default=0, ge=0, description="Number of attempts made before failing")
    error_kind: ErrorKind = Field(description="Closed-domain classification of the failure")
    retryable: bool = Field(
        default=False,
        description="Whether the file is retried on the next invocation (derived from error_kind)",
    )
    message: str = Field(default="", description="Sanitized human-readable failure description")

    @model_validator(mode="after")
    def _derive_retryable(self) -> PerFileReviewError:
        """Force ``retryable`` to the fixed mapping for ``error_kind``."""
        object.__setattr__(self, "retryable", self.error_kind in _RETRYABLE_KINDS)
        return self
