"""Paid output, stored separately — a storage failure never re-buys the output.

Every media-producing provider call has two phases:

1. **The paid call.** The vendor bills us the moment it answers.
2. **Storage.** We write the bytes to our file store (S3, thumbnails, the
   files row).

Before 2026-09-22 the two were one ``execute()``: an S3/thumbnail failure in
phase 2 was classified as a provider error, the executor retried the whole
``execute()``, and ElevenLabs billed three times for one run. The rule now:

* :func:`store_paid_output` runs phase 2 with the provider's result HELD in
  memory and retries STORAGE ONLY, once. When the retry fails too it raises
  :class:`PaidOutputStorageError` — non-retryable, honest about what failed,
  carrying the billed usage so the executor records the spend exactly once.
* :func:`mark_failed_after_paid_call` is for every other failure that happens
  after the paid call returned (alignment, event emission, metadata mapping):
  it forces a non-retryable classification and attaches the billed usage.

Both are provider-agnostic; every audio, image, and video adapter uses them.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

from matrx_ai.providers.errors import RetryableError, attach_billed_usage

if TYPE_CHECKING:  # pragma: no cover
    from matrx_ai.config import TokenUsage

STORAGE_FAILED = "media_storage_failed"
POST_PROVIDER_FAILURE = "post_provider_failure"

__all__ = [
    "POST_PROVIDER_FAILURE",
    "STORAGE_FAILED",
    "PaidOutputStorageError",
    "mark_failed_after_paid_call",
    "non_retryable_after_paid_call",
    "store_paid_output",
]


class PaidOutputStorageError(RuntimeError):
    """The provider delivered (and billed) the output; saving it failed twice."""

    def __init__(
        self,
        *,
        provider: str,
        modality: str,
        cause: BaseException,
        usage: TokenUsage | None = None,
        first_error: BaseException | None = None,
    ) -> None:
        cause_text = f"{type(cause).__name__}: {cause}".strip()
        message = (
            f"{provider} generated the {modality}, but saving it failed after one "
            f"storage retry ({cause_text}). The provider was not called again."
        )
        super().__init__(message)
        self.provider = provider
        self.modality = modality
        self.error_info = RetryableError(
            error_type=STORAGE_FAILED,
            message=message,
            is_retryable=False,
            user_message=(
                f"The {modality} was generated, but saving the file failed. You were "
                "charged once for the generation; run it again to get a saved copy."
            ),
            details={
                "provider": provider,
                "modality": modality,
                "suppressed_retry": True,
                "reason": "storage_failed_after_paid_call",
                "storage_attempts": 2,
                "cause_type": type(cause).__name__,
                "first_error": (
                    f"{type(first_error).__name__}: {first_error}" if first_error else None
                ),
            },
        )
        attach_billed_usage(self, usage)


async def store_paid_output[T](
    store: Callable[[], Awaitable[T]],
    *,
    provider: str,
    modality: str,
    usage: TokenUsage | None = None,
) -> T:
    """Run the storage phase for a paid output: one storage-only retry, then
    an honest non-retryable failure. ``store`` must close over the bytes the
    provider already returned — it is called at most twice and never reaches
    the provider."""
    try:
        return await store()
    except asyncio.CancelledError:
        raise
    except Exception as first:  # noqa: BLE001 — classified below, never swallowed
        vcprint(
            f"[paid output] {provider} {modality}: storage failed "
            f"({type(first).__name__}: {first}); retrying STORAGE ONLY — the provider "
            "is not called again.",
            color="yellow",
        )
        try:
            return await store()
        except asyncio.CancelledError:
            raise
        except Exception as second:  # noqa: BLE001
            vcprint(
                f"[paid output] {provider} {modality}: storage failed again "
                f"({type(second).__name__}: {second}); failing the run non-retryably.",
                color="red",
            )
            raise PaidOutputStorageError(
                provider=provider,
                modality=modality,
                cause=second,
                usage=usage,
                first_error=first,
            ) from second


def non_retryable_after_paid_call(
    error_info: Any,
    exc: BaseException,
    *,
    provider: str,
    modality: str,
) -> RetryableError:
    """Force a non-retryable classification once the paid provider call finished.

    The provider already billed the output. Retrying the whole ``execute()``
    would buy it again for a local failure — the loop that burned duplicate
    Replicate video runs (a missing partition misread as HTTP 429) and triple
    ElevenLabs renders (an S3 failure read as a provider error).
    """
    message = str(exc).strip() or type(exc).__name__
    details: dict[str, object] = {
        "suppressed_retry": True,
        "reason": "paid_provider_call_already_completed",
        "provider": provider,
        "modality": modality,
    }
    if isinstance(error_info, RetryableError):
        if not error_info.is_retryable:
            error_info.details.update({**details, **(error_info.details or {})})
            return error_info
        details.update(error_info.details or {})
        generic = error_info.error_type in {"rate_limit", "unknown_error", "overloaded"}
        return RetryableError(
            error_type=POST_PROVIDER_FAILURE if generic else error_info.error_type,
            message=error_info.message or message,
            status_code=error_info.status_code,
            is_retryable=False,
            user_message=(
                f"{modality.title()} generation finished at {provider}, but "
                "processing the result failed. It has been recorded — please try again."
                if generic
                else error_info.user_message
            ),
            details=details,
        )
    return RetryableError(
        error_type=POST_PROVIDER_FAILURE,
        message=message,
        is_retryable=False,
        user_message=(
            f"{modality.title()} generation finished at {provider}, but "
            "processing the result failed. It has been recorded — please try again."
        ),
        details=details,
    )


def mark_failed_after_paid_call(
    exc: BaseException,
    *,
    provider: str,
    modality: str,
    classified: Any = None,
    usage: TokenUsage | None = None,
) -> None:
    """Stamp a failure raised AFTER the paid call returned: non-retryable
    classification (an already-attached one wins when it is non-retryable) and
    the billed usage, so the executor records the spend once and never re-buys."""
    attached = getattr(exc, "error_info", None)
    base = attached if attached is not None else classified
    try:
        exc.error_info = non_retryable_after_paid_call(  # type: ignore[attr-defined]
            base, exc, provider=provider, modality=modality
        )
    except Exception:  # noqa: BLE001 — a builtin that rejects attributes keeps its own
        pass
    attach_billed_usage(exc, usage)
