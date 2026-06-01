"""RewriteArgsIntervention — CallIntervention for IN_STEP_REWRITE_ARGS.

Flow actions ``modify_prompt`` and ``reduce_context`` resolve to this
intervention (see actions.py). The flow step's ``parameters`` dict is
passed through verbatim as ``args_overrides``; the chain's retry loop is
responsible for merging those into the next call kwargs (this class does
not interpret the keys — that's per-provider/per-call-shape concern).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aigie.autonomous.interventions.base import CallIntervention
from aigie.autonomous.reasons import AUTONOMOUS_REWRITE_ARGS
from aigie.interceptor.protocols import PostCallResult

if TYPE_CHECKING:
    from aigie.interceptor.protocols import InterceptionContext


class RewriteArgsIntervention(CallIntervention):
    """In-step rewrite of the next call's kwargs.

    Reads ``args_overrides`` from the directive params and forwards it on
    the retry result so the chain's retry primitive picks up the new
    kwargs on re-invocation.
    """

    @property
    def args_overrides(self) -> dict[str, Any]:
        raw = self.action_params.get("args_overrides", {})
        return dict(raw) if isinstance(raw, dict) else {}

    def to_post_call_result(self, ctx: InterceptionContext) -> PostCallResult:
        return PostCallResult.retry(
            reason=AUTONOMOUS_REWRITE_ARGS,
            retry_kwargs={"args_overrides": self.args_overrides},
            hook_name=AUTONOMOUS_REWRITE_ARGS,
        )
