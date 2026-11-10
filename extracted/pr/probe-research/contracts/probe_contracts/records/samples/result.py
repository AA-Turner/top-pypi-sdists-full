"""SampleResult: what happened in one attempt (passed, failed or error), derived by the server, and why it broke."""

from __future__ import annotations

import math

from ...compat import StrEnum

#: The full reward when the plan names none: a 0/1 verifier's pass mark.
DEFAULT_REWARD_MAX = 1.0


class SampleResult(StrEnum):
    """Pytest's words for one rollout. Never `status`: the SQL tool joins samples to runs (DESIGN.md)."""

    PASSED = "passed"  # a valid reward at or above the full reward
    FAILED = "failed"  # a valid reward below it (a wrong answer, or graded after a timeout)
    ERROR = "error"  # no valid reward because something broke


class SampleErrorReason(StrEnum):
    """Why an attempt broke. Each adapter maps its framework's exceptions onto these once."""

    ENGINE_ABORT = "engine_abort"  # inference engine abort or preemption
    SANDBOX = "sandbox"  # sandbox start or exec failure
    VERIFIER = "verifier"  # verifier crash, or Harbor `reward_valid = false`
    REWARD_FUNCTION = "reward_fn"  # a reward function raised
    TIMEOUT = "timeout"
    OOM = "oom"
    NETWORK = "network"
    TOOL_BACKEND = "tool_backend"  # a lost tool backend
    CANCELED = "canceled"  # someone asked (a live sample's cancel command): the attempt ended `canceled`
    PROBE_PROXY = "probe_proxy"  # the Probe rollout proxy its model calls went through stopped under it
    #: A sibling was aborted (a cancel), so the framework drops the whole group (Miles' filter): this one ended dropped.
    GROUP_HAS_ABORTED = "group_has_aborted"
    UNKNOWN = "unknown"


def derive_result(reward: float | None, *, reward_max: float = DEFAULT_REWARD_MAX,
                  error_reason: SampleErrorReason | None = None) -> SampleResult | None:
    """The red line is "was it graded": a valid reward is green or orange whatever broke around it.

    None = nothing graded it and nothing broke (an SFT example, an attempt still in flight).
    """
    if reward is not None and math.isfinite(reward):
        return SampleResult.PASSED if reward >= reward_max else SampleResult.FAILED
    if error_reason is not None or reward is not None:
        return SampleResult.ERROR
    return None
