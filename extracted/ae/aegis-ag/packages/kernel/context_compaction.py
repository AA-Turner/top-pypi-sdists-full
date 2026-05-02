"""Kernel helpers for prompt-projection compaction retries."""

from __future__ import annotations

from typing import Any

from packages.context import estimate_projection_tokens


def looks_like_context_overflow(error: BaseException) -> bool:
    message = str(error).lower()
    return any(
        marker in message
        for marker in (
            "context length",
            "context_length",
            "maximum context",
            "prompt is too long",
            "prompt too long",
            "too many tokens",
            "request payload too large",
            "payload too large",
            "413",
        )
    )


def projection_compaction_detail(result: object) -> str:
    before_tokens = getattr(result, "before_tokens", 0)
    after_tokens = getattr(result, "after_tokens", 0)
    before_lines = getattr(result, "before_line_count", 0)
    after_lines = getattr(result, "after_line_count", 0)
    compacted_lines = getattr(result, "compacted_line_count", 0)
    reason = str(getattr(result, "reason", "") or "preflight")
    tail_count = getattr(result, "protected_tail_count", 0)
    return (
        f"reason={reason} tokens={before_tokens}->{after_tokens} "
        f"lines={before_lines}->{after_lines} compacted_lines={compacted_lines} "
        f"tail={tail_count}"
    )


def latest_compacted_projection(context_capability: object) -> object | None:
    result = getattr(context_capability, "last_projection_compaction", None)
    if result is None or not bool(getattr(result, "compacted", False)):
        return None
    return result


def flush_projection_memory(context_capability: object) -> None:
    flush = getattr(context_capability, "flush_projection_memory", None)
    if callable(flush):
        flush()


def stage_context_usage(
    stage: Any,
    prompt_tokens: int,
    completion_tokens: int,
    total_tokens: int,
) -> None:
    if not callable(stage) or max(prompt_tokens, completion_tokens, total_tokens) <= 0:
        return
    stage(
        "context-usage",
        f"prompt_tokens={prompt_tokens} completion_tokens={completion_tokens} total_tokens={total_tokens}",
    )


def estimate_context_projection_tokens(context: Any) -> int:
    rendered_prompt = str(getattr(context, "rendered_prompt", "") or "").strip()
    if rendered_prompt:
        return estimate_projection_tokens(rendered_prompt)
    envelope = getattr(context, "prompt_envelope", None)
    combined_prompt = getattr(envelope, "combined_prompt", None)
    if callable(combined_prompt):
        return estimate_projection_tokens(combined_prompt())
    return 0


def stage_context_projection(stage: Any, context: Any, *, source: str = "generation") -> None:
    if not callable(stage):
        return
    prompt_tokens = estimate_context_projection_tokens(context)
    token_budget = int(getattr(context, "token_budget", 0) or 0)
    if prompt_tokens <= 0 and token_budget <= 0:
        return
    stage("context-projection", f"prompt_tokens={prompt_tokens} token_budget={token_budget} source={source}")


def compact_context_after_usage(
    *,
    dependencies: Any,
    execution: Any,
    context: Any,
    stage: Any,
    usage_ratio: float = 0.80,
) -> object | None:
    prompt_tokens = int(getattr(execution, "prompt_tokens", 0) or 0)
    context_limit = int(getattr(context, "token_budget", 0) or 0)
    if prompt_tokens <= 0 or context_limit <= 0:
        return None
    if prompt_tokens < max(1, int(context_limit * usage_ratio)):
        return None
    compact = getattr(dependencies.context, "force_projection_compaction", None)
    if not callable(compact):
        return None
    result = compact(reason="usage")
    if result is None or not bool(getattr(result, "compacted", False)):
        return None
    stage("context-compact", projection_compaction_detail(result))
    flush_projection_memory(dependencies.context)
    return result


def retry_context_after_provider_overflow(
    *,
    error: RuntimeError,
    dependencies: Any,
    request: Any,
    profile: Any,
    session: Any,
    intent: Any,
    goals: tuple[Any, ...],
    memories: tuple[Any, ...],
    decision: Any,
    plan: Any,
    continuity: Any,
    clock: Any,
    stage: Any,
    context_for_generation: Any,
    recovery_scope_reason: str,
) -> Any | None:
    if not looks_like_context_overflow(error):
        return None
    compact = getattr(dependencies.context, "force_projection_compaction", None)
    if not callable(compact):
        return None
    result = compact(reason="provider-overflow")
    if result is None or not bool(getattr(result, "compacted", False)):
        return None
    stage("context-compact", projection_compaction_detail(result))
    flush_projection_memory(dependencies.context)
    rebuilt = dependencies.context.assemble(session, goals, memories, intent=intent)
    stage(
        "context",
        f"bundle={rebuilt.bundle_id} budget={rebuilt.token_budget} recovery_scope_reason={recovery_scope_reason}",
    )
    return context_for_generation(
        request=request,
        profile=profile,
        session=session,
        intent=intent,
        goals=goals,
        memories=memories,
        context=rebuilt,
        decision=decision,
        plan=plan,
        continuity=continuity,
        clock=clock,
    )


__all__ = [
    "latest_compacted_projection",
    "compact_context_after_usage",
    "flush_projection_memory",
    "looks_like_context_overflow",
    "projection_compaction_detail",
    "retry_context_after_provider_overflow",
    "stage_context_projection",
    "stage_context_usage",
]
