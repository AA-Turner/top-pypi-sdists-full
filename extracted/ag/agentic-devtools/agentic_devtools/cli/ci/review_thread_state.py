"""Capability-aware review-thread-state lookup with a degraded signal.

Reporting review-thread resolution state is an *optional* provider capability:
``CIPlatformProvider.list_review_thread_states()`` is non-abstract and its
default raises ``NotImplementedError``, and ``AzureDevOpsProvider`` does not
override it. Callers must therefore distinguish "thread state says nothing is
unresolved" from "thread state is unavailable" — treating the latter as zero
unresolved threads would silently loosen the merge gate for any provider that
simply lacks the capability.

:func:`fetch_review_thread_states` performs that detection once and returns a
:class:`ReviewThreadStates` result whose ``degraded`` flag tells the caller that
the mapping carries no information and the gate must fail closed.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from agentic_devtools.cli.ci.provider import CIPlatformProvider

_MAX_REASON_LENGTH = 200


@dataclass(frozen=True)
class ReviewThreadStates:
    """Outcome of a capability-aware review-thread-state lookup.

    Attributes:
        states: Mapping of review comment id to ``(is_resolved, has_reply)``.
            Always empty when ``degraded`` is True — a degraded lookup carries
            no thread information at all.
        degraded: True when the provider could not report thread state (the
            capability is missing, unimplemented, failed, or returned a value
            that is not a mapping). Callers must fail closed rather than treat
            the empty mapping as "nothing unresolved".
        reason: Human-readable explanation of why the lookup is degraded.
            Empty string when ``degraded`` is False.
    """

    states: dict[int, tuple[bool, bool]] = field(default_factory=dict)
    degraded: bool = False
    reason: str = ""


def fetch_review_thread_states(provider: CIPlatformProvider, pr_number: int) -> ReviewThreadStates:
    """Fetch review-thread state from ``provider``, degrading instead of raising.

    The provider method is resolved dynamically so that providers which do not
    derive from :class:`CIPlatformProvider` (or which explicitly drop the
    attribute) are handled the same way as one whose default implementation
    raises ``NotImplementedError``.

    Args:
        provider: CI platform provider to query.
        pr_number: Pull request number.

    Returns:
        A :class:`ReviewThreadStates` result. ``degraded`` is True whenever the
        state could not be determined; the caller must then never report a
        count of zero unresolved threads.
    """
    list_thread_states = getattr(provider, "list_review_thread_states", None)
    if not callable(list_thread_states):
        return ReviewThreadStates(degraded=True, reason="provider does not expose list_review_thread_states()")

    try:
        states = list_thread_states(pr_number)
    except NotImplementedError:
        return ReviewThreadStates(degraded=True, reason="provider does not implement list_review_thread_states()")
    except Exception as exc:
        detail = str(exc)[:_MAX_REASON_LENGTH]
        return ReviewThreadStates(degraded=True, reason=f"list_review_thread_states() failed: {detail}")

    if not isinstance(states, dict):
        return ReviewThreadStates(
            degraded=True,
            reason=f"list_review_thread_states() returned {type(states).__name__}, expected a mapping",
        )

    if any(
        type(comment_id) is not int
        or not isinstance(state, tuple)
        or len(state) != 2
        or any(type(flag) is not bool for flag in state)
        for comment_id, state in states.items()
    ):
        return ReviewThreadStates(
            degraded=True,
            reason="list_review_thread_states() returned an invalid state mapping",
        )

    return ReviewThreadStates(states=states)
