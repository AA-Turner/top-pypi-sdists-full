"""Exact diff fingerprinting for pipeline diff-preservation checks."""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence

from agentic_devtools.cli.ci.pipeline import runner_diff_parser
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)


def get_exact_diff_fingerprint(
    provider: CIPlatformProvider,
    *,
    base_sha: str,
    head_sha: str,
    expected_files: Sequence[str],
    pr_number: int,
) -> str:
    """Fetch and validate one exact patch against its pinned base."""
    if not base_sha or not expected_files:
        return ""
    get_commit_range_diff_bytes = getattr(provider, "get_commit_range_diff_bytes", None)
    get_change_counts = getattr(provider, "get_commit_range_diff_change_counts", None)
    if (
        not callable(get_commit_range_diff_bytes)
        or getattr(get_commit_range_diff_bytes, "__func__", None) is CIPlatformProvider.get_commit_range_diff_bytes
        or not callable(get_change_counts)
        or getattr(get_change_counts, "__func__", None) is CIPlatformProvider.get_commit_range_diff_change_counts
    ):
        return ""
    try:
        exact_diff_bytes = get_commit_range_diff_bytes(base_sha, head_sha)
        change_counts = get_change_counts(base_sha, head_sha)
    except Exception as exc:
        if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
            raise
        logger.warning(
            "PR #%d: Failed to compute exact diff for %s: %s",
            pr_number,
            head_sha[:8],
            str(exc)[:200],
        )
        return ""
    if not isinstance(exact_diff_bytes, bytes):
        return ""
    if not isinstance(change_counts, Mapping):
        return ""
    try:
        exact_diff = exact_diff_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return ""
    return runner_diff_parser.validated_exact_diff_fingerprint(exact_diff, expected_files, change_counts)
