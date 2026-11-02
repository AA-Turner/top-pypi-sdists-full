"""Mutual-exclusion lock between refresh and submit (v2 PR review, P3).

``agdt-pr-review-refresh-comment`` and ``agdt-pr-review-submit`` are the two
single-writer fan-in operations. They must never run concurrently: a refresh
re-renders the consolidated comment from the ledger while a submit mutates
terminal review state and PATCHes the same comment. This module provides one
exclusive sidecar lock both operations acquire at their outermost scope so they
are serialized (plan §3, §15.3).

The lock is intentionally **separate** from the ``review-state.json`` data lock
so the submit worker can hold this pipeline lock while its per-file processor
still takes the data lock for each ``read_modify_write_review_state`` call.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator
from pathlib import Path
from typing import IO

from ...file_locking import locked_file
from .review_state import get_review_state_file_path

PIPELINE_LOCK_FILENAME = "pull-request-review-pipeline"

#: Default timeout (seconds) for acquiring the pipeline lock. A short timeout
#: surfaces a clear "already in progress" failure rather than blocking forever.
DEFAULT_PIPELINE_LOCK_TIMEOUT_SECONDS = 10.0


def pipeline_lock_path(pull_request_id: int) -> Path:
    """Return the PR-scoped pipeline lock path, beside ``review-state.json``.

    Args:
        pull_request_id: PR ID (forwarded to ``get_review_state_file_path``).

    Returns:
        The sidecar lock file path in the ``reviews/`` directory, scoped by
        pull request ID so different PRs in the same worktree do not contend.
    """
    filename = f"{PIPELINE_LOCK_FILENAME}.{pull_request_id}.lock"
    return get_review_state_file_path(pull_request_id).parent / filename


@contextlib.contextmanager
def pipeline_lock(
    pull_request_id: int,
    timeout: float = DEFAULT_PIPELINE_LOCK_TIMEOUT_SECONDS,
) -> Iterator[IO]:
    """Acquire the exclusive refresh/submit pipeline lock for a PR.

    Args:
        pull_request_id: The PR whose pipeline to lock.
        timeout: Maximum seconds to wait for the lock.

    Yields:
        The locked file handle.

    Raises:
        FileLockError: When the lock cannot be acquired within *timeout*
            (i.e. a refresh or submit is already running for this PR).
    """
    with locked_file(pipeline_lock_path(pull_request_id), mode="r+", exclusive=True, timeout=timeout) as handle:
        yield handle
