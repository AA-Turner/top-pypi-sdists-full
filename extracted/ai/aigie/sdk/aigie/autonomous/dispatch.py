"""Route InterceptionContext → PostCallResult.

Call-domain interventions enact inline; workflow-domain delegates to
``DirectiveApplier.apply`` via the runtime's bounded executor so sync and
async arrivals share one path.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aigie.autonomous import adapters as adapter_registry
from aigie.autonomous.adapters import SpanContext
from aigie.autonomous.interventions import CallIntervention, resolve
from aigie.autonomous.outcome import Status
from aigie.autonomous.reasons import NO_ADAPTER, UNKNOWN_ACTION_TYPE
from aigie.interceptor.protocols import PostCallResult

if TYPE_CHECKING:
    from aigie.autonomous.runtime import AutonomousRuntime
    from aigie.interceptor.protocols import InterceptionContext

logger = logging.getLogger(__name__)


def _framework_for(ctx: InterceptionContext) -> str:
    fw = getattr(ctx, "framework", None)
    if fw:
        return str(fw)
    meta = getattr(ctx, "metadata", None) or {}
    meta_fw = meta.get("framework") if isinstance(meta, dict) else None
    return str(meta_fw or getattr(ctx, "provider", "") or "")


def dispatch(ctx: InterceptionContext, runtime: AutonomousRuntime) -> PostCallResult:
    """Route a post-call context through the autonomous pipeline."""
    if getattr(ctx, "error", None) is None:
        return PostCallResult.allow()
    directive = runtime.evaluate_inline(ctx)
    if directive is None:
        return PostCallResult.allow()
    intervention = resolve(directive)
    if intervention is None:
        reason = UNKNOWN_ACTION_TYPE.format(action_type=int(directive.action_type))
        runtime.report_outcome(directive, Status.FAILED, reason)
        return PostCallResult.allow()
    framework = _framework_for(ctx)
    adapter = adapter_registry.get(framework) if framework else None
    if adapter is None or directive.action_type not in adapter.capabilities():
        runtime.report_outcome(directive, Status.FAILED, NO_ADAPTER.format(framework=framework))
        return PostCallResult.allow()
    if isinstance(intervention, CallIntervention):
        result = intervention.to_post_call_result(ctx)
        runtime.report_outcome(directive, Status.APPLIED, result.hook_name or "applied")
        return result
    span_ctx = SpanContext(
        trace_id=getattr(ctx, "trace_id", None) or "",
        span_id=getattr(ctx, "span_id", None) or "",
        framework=framework,
        framework_handle=getattr(ctx, "framework_handle", None),
        logger=logger,
        attrs=dict(getattr(ctx, "metadata", {}) or {}),
    )

    def _run() -> None:
        runtime.outcome_reporter.report(runtime.applier.apply(directive, framework, span_ctx))

    executor = getattr(runtime, "_apply_executor", None)
    if executor is None:
        _run()
    else:
        try:
            executor.submit(_run)
        except Exception as exc:  # noqa: BLE001
            logger.warning("apply executor submit failed: %s", exc)
    return PostCallResult.allow()


def make_chain_hook(runtime: AutonomousRuntime):
    """Return an async PostCallHook-compatible callable wrapping `dispatch`."""

    async def _autonomous_post_call_hook(ctx: InterceptionContext) -> PostCallResult:
        return dispatch(ctx, runtime)

    _autonomous_post_call_hook.name = "autonomous_dispatch"  # type: ignore[attr-defined]
    _autonomous_post_call_hook.priority = 10  # type: ignore[attr-defined]
    return _autonomous_post_call_hook
