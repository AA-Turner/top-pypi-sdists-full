"""RetryIntervention — the first real CallIntervention.

Reads retry knobs from `directive.action_params` (with sane defaults) and
produces a `PostCallResult.retry(...)`. The chain's retry loop performs the
re-invocation; this class does not loop.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from aigie.autonomous.interventions.base import CallIntervention
from aigie.autonomous.reasons import AUTONOMOUS_RETRY
from aigie.interceptor.protocols import PostCallResult

if TYPE_CHECKING:
    from aigie.interceptor.protocols import InterceptionContext


class RetryIntervention(CallIntervention):
    """In-step retry — Directive view exposing the chain's retry knobs."""

    @property
    def max_attempts(self) -> int:
        return int(self.action_params.get("max_attempts", 3))

    @property
    def backoff_ms_initial(self) -> int:
        return int(self.action_params.get("backoff_ms_initial", 100))

    @property
    def backoff_multiplier(self) -> float:
        return float(self.action_params.get("backoff_multiplier", 2.0))

    @property
    def backoff_max_ms(self) -> int:
        return int(self.action_params.get("backoff_max_ms", 5000))

    def to_post_call_result(self, ctx: InterceptionContext) -> PostCallResult:
        """Translate the directive into the chain's retry primitive.

        The chain (`InterceptorChain.post_call`) consumes `should_retry`/`retry_kwargs`
        and performs the re-invocation. Backoff multiplier / max are carried in
        retry_kwargs metadata for the retry loop to consult.
        """
        return PostCallResult.retry(
            reason=AUTONOMOUS_RETRY,
            retry_kwargs={
                "max_attempts": self.max_attempts,
                "backoff_ms_initial": self.backoff_ms_initial,
                "backoff_multiplier": self.backoff_multiplier,
                "backoff_max_ms": self.backoff_max_ms,
            },
            hook_name=AUTONOMOUS_RETRY,
        )
