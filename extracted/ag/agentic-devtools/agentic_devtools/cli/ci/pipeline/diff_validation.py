"""Validation for preserving a pull request diff across branch mutations."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class DiffValidationResult:
    """Result of comparing a pre- and post-mutation pull request diff."""

    valid: bool
    missing_files: tuple[str, ...] = ()
    reason: str = ""


def validate_diff_preservation(
    pre_files: list[str],
    post_files: list[str],
    *,
    pre_hash: str = "",
    post_hash: str = "",
    pre_hash_available: bool = True,
    post_hash_available: bool = True,
    fingerprint_supported: bool = False,
    intentional_noop: bool = False,
    allow_file_removal: bool = False,
    allowed_removed_files: Sequence[str] | None = None,
) -> DiffValidationResult:
    """Ensure a mutation did not remove intended files or change its patch."""
    if not pre_files:
        if intentional_noop and not post_files:
            return DiffValidationResult(True)
        return DiffValidationResult(False, (), "pre-mutation diff is empty without explicit no-op intent")
    missing_files = tuple(sorted(set(pre_files) - set(post_files)))
    allowed_removed = set(allowed_removed_files or ())
    if not post_files:
        return DiffValidationResult(False, missing_files, "post-mutation diff is empty")
    if missing_files and not allow_file_removal and not set(missing_files).issubset(allowed_removed):
        return DiffValidationResult(False, missing_files, "post-mutation diff is missing intended files")
    if fingerprint_supported and (not pre_hash_available or not post_hash_available):
        return DiffValidationResult(False, (), "post-mutation patch fingerprint unavailable")
    if fingerprint_supported and (not pre_hash or not post_hash):
        return DiffValidationResult(False, (), "post-mutation patch fingerprint unavailable")
    if fingerprint_supported and pre_hash != post_hash:
        return DiffValidationResult(False, (), "post-mutation patch fingerprint changed")
    return DiffValidationResult(True)
