"""Shared helpers for PR snapshot collection."""

from __future__ import annotations

from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.retry import ProviderRateLimitError


def _raise_if_rate_limit(exc: Exception) -> None:
    """Re-raise actual provider rate limits so caller can return paused exit."""
    if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
        raise


def _supports_diff_fingerprint(provider: object) -> bool:
    """Return whether ``provider`` implements diff fingerprinting."""
    method = getattr(provider, "compute_diff_hash", None)
    if not callable(method):
        return False
    provider_method = getattr(method, "__func__", None)
    if provider_method is None:
        return True
    return provider_method is not CIPlatformProvider.compute_diff_hash
