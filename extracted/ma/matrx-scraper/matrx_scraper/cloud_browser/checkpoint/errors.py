"""Exceptions and the frozen failure-code vocabulary (S3 §5.5).

The failure codes are literal strings consumed by three repos; they must never be
guessed or spelled differently. ``FAILURE_CODES`` is the closed set.
"""

from __future__ import annotations

from typing import Final

FAILURE_CODES: Final[frozenset[str]] = frozenset(
    {
        # closure
        "close_not_completed",
        "chromium_still_running",
        "open_file_descriptors",
        "singleton_lock_held",
        "sqlite_unsettled",
        # capture
        "archive_failed",
        "encrypt_failed",
        "dek_wrap_failed",
        "upload_failed",
        # verification
        "upload_hash_mismatch",
        "wrap_context_mismatch",
        "dek_unwrap_failed",
        "auth_tag_invalid",
        "plaintext_hash_mismatch",
        "archive_unreadable",
        "profile_probe_failed",
        # restore / manifest
        "manifest_row_mismatch",
        "manifest_missing",
        "manifest_version_unsupported",
        "archive_format_unsupported",
        "profile_format_too_new",
        "chromium_downgrade_refused",
        "owner_mismatch",
        "wrap_alg_not_permitted",
        "object_missing",
        "object_version_mismatch",
        # D-5 cookie scheme portability
        "cookie_scheme_mismatch",
    }
)


class CheckpointError(Exception):
    """Base for every checkpoint-engine error. Carries a frozen failure ``code``."""

    code: str = "checkpoint_error"

    def __init__(self, message: str, *, code: str | None = None) -> None:
        if code is not None:
            if code not in FAILURE_CODES:
                raise ValueError(f"unknown checkpoint failure code: {code!r}")
            self.code = code
        super().__init__(message)


class ClosureError(CheckpointError):
    """The profile could not be proven closed; no archive is produced (S3 §4)."""


class CaptureError(CheckpointError):
    """Archive / encrypt / wrap / upload failed during capture (S3 §3)."""


class VerificationError(CheckpointError):
    """A checkpoint failed the verification gate (S3 §5)."""


class RestoreError(CheckpointError):
    """A restore pre-launch check failed (S3 §6)."""


class NoRestorableRevisionError(CheckpointError):
    """Every fallback candidate failed; NO blank profile is created (S3 §7.4)."""

    code = "checkpoint_error"

    def __init__(self, message: str, *, attempts: list[dict[str, object]]) -> None:
        self.attempts = attempts
        super().__init__(message)


class DeletionError(CheckpointError):
    """Cryptographic deletion could not complete (S3 §8)."""


class CheckpointKmsNotConfiguredError(CheckpointError):
    """The KMS wrap provider has no key id. Loud, never a silent local fallback.

    Mirrors ``EscrowNotConfiguredError`` / ``BrokerNotConfigured`` — a real
    deployment must configure ``MATRX_BROWSER_PROFILE_KMS_KEY_ID``.
    """


class LocalDevProviderRefusedError(CheckpointError):
    """The local-dev key-wrap provider was constructed outside local/test (S3 §9.3)."""
