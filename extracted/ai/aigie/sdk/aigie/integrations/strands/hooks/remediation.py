"""Real-time remediation + post-tool intercepts; called from on_after_tool_call."""

from __future__ import annotations

import contextlib
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from strands.hooks import AfterToolCallEvent

    from ....realtime.remediation_engine import RemediationResult
    from ..handler import StrandsHandler

logger = logging.getLogger(__name__)


async def _try_programmatic_fix(
    handler: StrandsHandler,
    rem_result: RemediationResult,
    tool_name: str,
    error_msg: str,
    event: AfterToolCallEvent,
) -> bool:
    """Apply a structured fix via AutoFixApplicator. Returns True on success."""
    engine = handler._remediation_engine
    if not rem_result.action_type or engine is None:
        return False
    try:
        fix_action = engine.to_fix_action(rem_result)
        if not fix_action:
            return False
        from ....interceptor.protocols import InterceptionContext
        from ....realtime.auto_fix import AutoFixApplicator

        applicator = AutoFixApplicator()
        applicator.set_retry_executor(_make_strands_retry_executor(event))

        ctx = InterceptionContext(
            provider="strands",
            model="",
            messages=[],
            response_content=error_msg,
        )
        fix_result = await applicator.apply_fixes(ctx, [fix_action])
        if not fix_result.success:
            return False
        logger.warning(
            f"[AIGIE] Programmatic fix applied: {rem_result.action_type} on {tool_name} "
            f"(strategy={fix_result.strategy.value}, latency={fix_result.latency_ms:.0f}ms)"
        )
        if fix_result.modified_response:
            modified = str(fix_result.modified_response.get("content", ""))
            inject_guidance(event, modified)
            rem_result.fixed_output = modified
        return True
    except Exception as fix_err:
        logger.debug(f"[AIGIE] Programmatic fix failed, falling back to guidance: {fix_err}")
        return False


def _make_strands_retry_executor(event: AfterToolCallEvent):
    """Closure that flips event.retry=True (Strands' built-in re-execution flag)."""

    async def _strands_retry_executor(**retry_kwargs):
        if hasattr(event, "retry"):
            event.retry = True
            return {"retried": True, "kwargs": retry_kwargs}
        return retry_kwargs

    return _strands_retry_executor


async def _maybe_remediate(
    handler: StrandsHandler,
    is_error: bool,
    error_msg: str | None,
    tool_name: str,
    span_id: str,
    tool_data: dict,
    result_str: str,
    event: AfterToolCallEvent,
) -> None:
    """Real-time remediation: query for a fix and inject guidance into the event."""
    if not (is_error and error_msg and handler._remediation_engine):
        return
    try:
        rem_result = await handler._remediation_engine.evaluate(
            error_msg,
            tool_name,
            span_id,
            handler.trace_id or "",
            mode=handler.config.remediation_mode,
        )
        if not rem_result:
            return
        rem_result.original_input = str(tool_data.get("tool_input", ""))
        rem_result.original_output = result_str
        if handler.config.remediation_mode == "autonomous":
            await _apply_remediation_autonomous(handler, rem_result, tool_name, error_msg, event)
        else:
            logger.info(
                f"[AIGIE] Remediation available for {rem_result.error_type} on {tool_name}: "
                f"strategy={rem_result.strategy}, rate={rem_result.success_rate:.0%} "
                f"(mode=recommendation, not applied)"
            )
        await report_remediation(handler, span_id, rem_result)
    except Exception as rem_err:
        logger.debug(f"[AIGIE] Remediation failed (non-fatal): {rem_err}")


async def _apply_remediation_autonomous(
    handler: StrandsHandler,
    rem_result: RemediationResult,
    tool_name: str,
    error_msg: str,
    event: AfterToolCallEvent,
) -> None:
    applied_programmatic = await _try_programmatic_fix(
        handler, rem_result, tool_name, error_msg, event
    )
    if not applied_programmatic:
        inject_guidance(event, rem_result.guidance_text)
        rem_result.fixed_output = rem_result.guidance_text
    engine = handler._remediation_engine
    if engine is not None:
        engine.mark_applied(rem_result)
    logger.warning(
        f"[AIGIE] Real-time correction applied: {rem_result.error_type} on {tool_name} "
        f"(strategy={rem_result.strategy}, rate={rem_result.success_rate:.0%}, "
        f"query={rem_result.query_ms:.0f}ms, programmatic={applied_programmatic})"
    )


async def _maybe_post_tool_intercept(
    handler: StrandsHandler,
    is_error: bool,
    error_msg: str | None,
    tool_name: str,
    span_id: str,
    duration_ms: float,
    event: AfterToolCallEvent,
) -> None:
    """Consult backend for post-tool fix signals; inject guidance if requested."""
    aigie = handler._get_aigie()
    if not (aigie and aigie._initialized and is_error):
        return
    try:
        post = await aigie.intercept_after_tool(
            tool_name=tool_name,
            result=event.result,
            error=error_msg,
            error_type=type(event.exception).__name__
            if event.exception
            else ("ToolError" if is_error else None),
            trace_id=handler.trace_id,
            span_id=span_id,
            duration_ms=duration_ms,
        )
        if not (post.get("fixes") and handler.config.remediation_mode == "autonomous"):
            return
        for fix in post["fixes"]:
            if fix.get("confidence", 0) < 0.7:
                continue
            guidance = fix.get("reason") or fix.get("parameters", {}).get("guidance")
            if guidance:
                inject_guidance(event, guidance)
                logger.info(
                    f"[AIGIE] Backend fix applied: {fix.get('action_type')} "
                    f"(confidence={fix.get('confidence'):.0%})"
                )
                break
    except Exception as pie:
        logger.debug(f"[AIGIE] Post-tool intercept error (non-fatal): {pie}")


def _apply_push_intervention(
    handler: StrandsHandler, tool_data: dict, event: AfterToolCallEvent
) -> None:
    """Apply a push intervention payload (inject_correction / break_loop / redirect)."""
    if handler.config.remediation_mode != "autonomous":
        return
    pending = tool_data.get("_pending_intervention")
    if not pending:
        return
    try:
        if pending.intervention_type == "inject_correction":
            inject_guidance(event, pending.payload.get("guidance", pending.reason))
        elif pending.intervention_type == "break_loop":
            inject_guidance(event, f"[Aigie: Stop] {pending.reason}. Do not retry this action.")
        elif pending.intervention_type == "redirect":
            alt = pending.payload.get("alternative_tool", "")
            inject_guidance(event, f"[Aigie: Use {alt} instead] {pending.reason}")
        logger.info(f"[AIGIE] Push intervention applied: type={pending.intervention_type}")
    except Exception as int_err:
        logger.debug(f"[AIGIE] Intervention injection failed (non-fatal): {int_err}")


def inject_guidance(event: AfterToolCallEvent, guidance_text: str) -> None:
    """Append corrective guidance into a Strands ToolResult dict."""
    try:
        result = event.result
        if isinstance(result, dict):
            content = result.get("content", [])
            if isinstance(content, list):
                content.append({"text": guidance_text})
            else:
                result["content"] = [{"text": str(content)}, {"text": guidance_text}]
            event.result = result
    except Exception as e:
        logger.warning(f"[AIGIE] Failed to apply remediation to event.result: {e}")


async def report_remediation(
    handler: StrandsHandler, span_id: str, result: RemediationResult
) -> None:
    """Publish a remediation result to span metadata + the platform."""
    with contextlib.suppress(Exception):
        from ....buffer import EventType

        aigie = handler._get_aigie()
        if not aigie or not aigie._initialized:
            return
        if aigie._buffer:
            await aigie._buffer.add(
                EventType.SPAN_UPDATE,
                {
                    "id": span_id,
                    "trace_id": handler.trace_id,
                    "metadata": {"realtime_remediation": result.to_dict()},
                },
            )
        if handler._remediation_engine:
            await handler._remediation_engine.report_result(result, handler.trace_id)
