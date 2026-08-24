"""Real-time interception hooks for the OpenAI wrapper.

Interception can deliberately stop a call (a block) or ask for it to be run
again (a retry). Everything else that goes wrong in here is our bug, and the
rule is absolute: an SDK-internal interception failure must never prevent or
destroy the customer's LLM call. So each entry point below re-raises the two
intentional signals and swallows everything else.

Only OpenAI has these hooks today. The sync path has no awaitable chain, so it
can consult the local rules engine and nothing more.
"""

from __future__ import annotations

import logging
from typing import Any

from aigie.context_manager import RunContext

logger = logging.getLogger(__name__)

# Interception failures are contained, but a hook that fails on every call is a
# misconfiguration only the customer can fix. Warning every time floods the log;
# staying at debug hides it entirely. So the first occurrence of each kind is
# visible and the rest are not.
_WARNED_ONCE: set[str] = set()


def _log_contained(kind: str, template: str, error: Exception) -> None:
    """Warn once per process for `kind`, then debug for every later occurrence."""
    if kind in _WARNED_ONCE:
        logger.debug(template, error)
        return

    _WARNED_ONCE.add(kind)
    logger.warning(template + " (further occurrences logged at debug)", error)


def _reraise_if_intentional(error: Exception, class_name: str) -> None:
    """Re-raise `error` if it is the named interception signal, else return.

    A missing protocols module or signal class means nothing can be
    intentional, so the error falls through to the fail-open path.
    """
    try:
        from aigie.interceptor import protocols

        signal_type = getattr(protocols, class_name)
    except (ImportError, AttributeError):
        return

    if isinstance(error, signal_type):
        raise error


def _raise_if_blocked(ctx: Any) -> None:
    from aigie.interceptor.protocols import InterceptionBlockedError, InterceptionDecision

    if ctx.decision == InterceptionDecision.BLOCK:
        raise InterceptionBlockedError(
            reason=ctx.block_reason or "Request blocked by interception",
            hook_name="pre_call",
        )


def _apply_pre_call_modifications(ctx: Any, messages: list, model: str, kwargs: dict) -> tuple:
    """Fold any interception edits back into the outgoing request."""
    if ctx.modified_messages:
        kwargs["messages"] = ctx.modified_messages
        messages = ctx.modified_messages
    if ctx.modified_kwargs:
        kwargs.update(ctx.modified_kwargs)
        model = kwargs.get("model", model)
    return messages, model


async def run_pre_call(
    aigie: Any,
    *,
    model: str,
    messages: list,
    kwargs: dict,
    trace_id: str | None,
    span_id: str,
) -> tuple:
    """Run the pre-call chain.

    Returns `(interception_ctx, messages, model)`, with `kwargs` updated in
    place. On any non-block failure the context comes back as None and the
    original request proceeds untouched.
    """
    try:
        ctx = await aigie.intercept_pre_call(
            provider="openai",
            model=model,
            messages=messages,
            trace_id=trace_id,
            span_id=span_id,
            **{k: v for k, v in kwargs.items() if k not in ["messages", "model"]},
        )
        _raise_if_blocked(ctx)
        messages, model = _apply_pre_call_modifications(ctx, messages, model, kwargs)
        return ctx, messages, model

    except Exception as intercept_error:
        _reraise_if_intentional(intercept_error, "InterceptionBlockedError")
        _log_contained(
            "pre_call",
            "[wrapper] Pre-call interception failed (%s); proceeding with original request",
            intercept_error,
        )
        return None, messages, model


def _stamp_actuals(ctx: Any, run_ctx: RunContext, output_content: str) -> None:
    """Give the interceptor what the call actually cost."""
    if "cost" in run_ctx.metadata:
        ctx.actual_cost = run_ctx.metadata["cost"].get("total_cost", 0)
    if "usage" in run_ctx.metadata:
        ctx.actual_input_tokens = run_ctx.metadata["usage"].get("prompt_tokens", 0)
        ctx.actual_output_tokens = run_ctx.metadata["usage"].get("completion_tokens", 0)
    ctx.response_content = output_content


def _raise_if_retry_requested(ctx: Any, kwargs: dict) -> None:
    from aigie.interceptor.protocols import InterceptionDecision, InterceptionRetryError

    if ctx.decision == InterceptionDecision.MODIFY and ctx.should_retry:
        raise InterceptionRetryError(
            reason="Post-call interception requested retry",
            retry_kwargs=ctx.retry_kwargs or kwargs,
        )


def _apply_response_modification(ctx: Any, run_ctx: RunContext, output_content: str) -> None:
    if not ctx.modified_response:
        return

    logger.debug("[wrapper] Applying post-call response modification")
    # The provider's response object can't be rewritten in place, so only our
    # record of it changes; the caller still receives the original object.
    run_ctx.metadata["output"] = {"content": ctx.modified_response.get("content", output_content)}
    run_ctx.metadata["interception_modified"] = True


async def run_post_call(
    aigie: Any,
    ctx: Any,
    *,
    run_ctx: RunContext,
    response: Any,
    output_content: str,
    kwargs: dict,
) -> Any:
    """Run the post-call chain for a successful call.

    Returns the (possibly replaced) interception context. A retry request
    propagates; anything else is logged and the original response stands.
    """
    try:
        _stamp_actuals(ctx, run_ctx, output_content)
        ctx = await aigie.intercept_post_call(ctx=ctx, response=response, error=None)
        _raise_if_retry_requested(ctx, kwargs)
        _apply_response_modification(ctx, run_ctx, output_content)
        return ctx

    except Exception as intercept_error:
        _reraise_if_intentional(intercept_error, "InterceptionRetryError")
        _log_contained(
            "post_call",
            "[wrapper] Post-call interception failed (%s); returning original response",
            intercept_error,
        )
        return ctx


async def run_error_post_call(aigie: Any, ctx: Any, error: Exception) -> dict | None:
    """Run the post-call chain for a failed call.

    Returns retry kwargs if an auto-fix wants the call run again, else None.
    """
    try:
        ctx = await aigie.intercept_post_call(ctx=ctx, response=None, error=error)
        if ctx.should_retry and ctx.retry_kwargs:
            logger.debug("[wrapper] Auto-fix retry after error")
            fix_kwargs: dict = ctx.retry_kwargs
            return fix_kwargs
    except Exception as intercept_error:
        logger.debug("[wrapper] Post-call error interception failed: %s", intercept_error)

    return None


def retry_kwargs_from(error: Exception) -> dict | None:
    """Retry kwargs carried by an interception retry signal, if this is one."""
    try:
        from aigie.interceptor.protocols import InterceptionRetryError

        if isinstance(error, InterceptionRetryError) and error.retry_kwargs:
            retry_kwargs: dict = error.retry_kwargs
            return retry_kwargs
    except ImportError:
        pass

    return None


def run_sync_pre_call(
    aigie: Any,
    *,
    model: str,
    messages: list,
    kwargs: dict,
    trace_id: str | None,
    span_id: str,
) -> None:
    """Consult the local rules engine before a sync call.

    The full chain is async, so a sync call can only be blocked by a local
    rule. A block propagates; every other failure is logged and ignored.
    """
    try:
        from aigie.interceptor.protocols import (
            InterceptionBlockedError,
            InterceptionContext,
            InterceptionDecision,
        )

        ctx = InterceptionContext(
            provider="openai",
            model=model,
            messages=messages,
            trace_id=trace_id,
            span_id=span_id,
            request_kwargs=kwargs,
        )

        try:
            from aigie.utils.safe import schedule_async

            result = schedule_async(aigie._rules_engine.evaluate(ctx))
            if result is not None and result.decision == InterceptionDecision.BLOCK:
                raise InterceptionBlockedError(
                    reason=result.reason or "Request blocked by rules",
                    hook_name="rules_engine",
                )
        except Exception as rule_error:
            if isinstance(rule_error, InterceptionBlockedError):
                raise
            logger.debug("[wrapper] Sync rules evaluation failed: %s", rule_error)

    except ImportError:
        pass
