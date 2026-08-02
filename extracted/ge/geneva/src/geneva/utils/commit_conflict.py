# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Classify Lance commit-version conflicts.

Lance raises a plain ``OSError`` for a retryable commit conflict -- it exposes no
typed exception for it -- and the message wording has varied: "Commit conflict for
version ..." (legacy) and "Retryable commit conflict for version ..." (current).
Match the common case-insensitive substring so both are caught, in one place, for
every committer (carry-forward and sparse). If Lance ever exposes a typed or
error-coded conflict, this is the single spot to switch to it.
"""

from __future__ import annotations


def is_retryable_commit_conflict(exc: BaseException) -> bool:
    """True if ``exc`` is a Lance retryable commit-version conflict."""
    return "commit conflict for version" in str(exc).lower()
