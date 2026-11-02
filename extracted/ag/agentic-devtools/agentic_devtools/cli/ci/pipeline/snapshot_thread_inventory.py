"""Validate provider-supplied review-thread inventories."""

from __future__ import annotations

import logging
from typing import cast

from agentic_devtools.cli.ci.pipeline.snapshot_utils import _raise_if_rate_limit
from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)
ThreadState = tuple[bool, tuple[int, ...]]


def _load_thread_states(provider: CIPlatformProvider, pr_number: int) -> dict[str, ThreadState] | None:
    """Fetch thread state, returning ``None`` when the provider cannot supply it."""
    lookup = getattr(provider, "list_review_threads_by_thread_id", None)
    if not callable(lookup):
        logger.warning(
            "PR #%d: review-thread state unavailable (provider does not expose list_review_threads_by_thread_id())"
            " — failing closed with an unknown-thread count",
            pr_number,
        )
        return None
    try:
        thread_states = lookup(pr_number)
    except NotImplementedError:
        logger.warning(
            "PR #%d: review-thread state unavailable (provider does not implement list_review_threads_by_thread_id())"
            " — failing closed with an unknown-thread count",
            pr_number,
        )
        return None
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.warning(
            "PR #%d: review-thread state unavailable (%s) — failing closed with an unknown-thread count",
            pr_number,
            str(exc)[:200],
        )
        return None
    if not isinstance(thread_states, dict):
        logger.warning(
            "PR #%d: review-thread state unavailable "
            "(list_review_threads_by_thread_id() returned %s, expected a mapping)"
            " — failing closed with an unknown-thread count",
            pr_number,
            type(thread_states).__name__,
        )
        return None
    return cast(dict[str, ThreadState], thread_states)


def _thread_comment_ids(
    thread_key: object,
    state: object,
    pr_number: int,
) -> tuple[bool, tuple[int, ...] | None]:
    """Validate one thread key/state pair and return its comment IDs."""
    if not isinstance(thread_key, str) or not thread_key:
        logger.warning(
            "PR #%d: review-thread state unavailable "
            "(list_review_threads_by_thread_id() returned an invalid thread key: thread_key=%r)"
            " — failing closed with an unknown-thread count",
            pr_number,
            thread_key,
        )
        return False, None
    if not isinstance(state, tuple) or len(state) != 2 or type(state[0]) is not bool:
        logger.warning(
            "PR #%d: review-thread state unavailable "
            "(list_review_threads_by_thread_id() returned an invalid state mapping: "
            "thread=%r state=%r) — failing closed with an unknown-thread count",
            pr_number,
            thread_key,
            state,
        )
        return False, None
    comment_ids = state[1]
    if not isinstance(comment_ids, tuple):
        logger.warning(
            "PR #%d: review-thread state unavailable "
            "(list_review_threads_by_thread_id() returned an invalid state mapping)"
            " — failing closed with an unknown-thread count",
            pr_number,
        )
        return False, None
    if any(type(comment_id) is not int for comment_id in comment_ids):
        invalid_id = next(comment_id for comment_id in comment_ids if type(comment_id) is not int)
        logger.warning(
            "PR #%d: review-thread state unavailable "
            "(list_review_threads_by_thread_id() returned an invalid state mapping: "
            "thread=%r comment_id=%r) — failing closed with an unknown-thread count",
            pr_number,
            thread_key,
            invalid_id,
        )
        return False, None
    return True, comment_ids


def _index_thread_comments(thread_states: dict[str, ThreadState], pr_number: int) -> dict[int, str] | None:
    """Map each validated comment ID to exactly one provider thread."""
    comment_to_thread: dict[int, str] = {}
    for thread_key, state in thread_states.items():
        valid, comment_ids = _thread_comment_ids(thread_key, state, pr_number)
        if not valid or comment_ids is None:
            return None
        for comment_id in comment_ids:
            mapped_thread = comment_to_thread.get(comment_id)
            if mapped_thread is not None and mapped_thread != thread_key:
                logger.warning(
                    "PR #%d: review-thread state unavailable "
                    "(list_review_thread_states() returned conflicting thread mappings: "
                    "comment_id=%r thread=%r conflicting_thread=%r)"
                    " — failing closed with an unknown-thread count",
                    pr_number,
                    comment_id,
                    mapped_thread,
                    thread_key,
                )
                return None
            comment_to_thread[comment_id] = thread_key
    return comment_to_thread
