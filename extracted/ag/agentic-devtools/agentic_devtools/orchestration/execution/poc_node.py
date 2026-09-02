"""Proof-of-concept node demonstrating the execution model.

``create_analysis_node()`` is a node factory that accepts an
``ExecutionContext`` and returns a LangGraph-compatible callable
(``ExecutionState → NodeUpdateAlias``).  It demonstrates:

1. LLM reasoning via ``ReasoningProvider``
2. Tool invocation via ``ToolRegistry``
3. Retry with context accumulation via ``with_retry()``
4. Trace event emission via ``TraceEmitter``
"""

from __future__ import annotations

import json
import sys
import time
from collections.abc import Callable
from typing import cast

from .context import ExecutionContext
from .exceptions import ReasoningTimeoutError
from .retry import RetryContext, with_retry
from .state import ExecutionState, NodeUpdateAlias
from .tracing import TraceEvent, make_trace_event
from .types import JSONValue

NODE_NAME = "analysis_poc"
"""Default node name used in trace events."""


def _emit_best_effort(tracer, event: TraceEvent) -> None:  # noqa: ANN001
    """Emit *event* via *tracer*, swallowing any exception to stderr.

    Tracing is non-critical: a faulty tracer must never interrupt node
    execution or change its return value.
    """
    try:
        tracer.emit(event)
    except Exception as exc:  # noqa: BLE001
        print(
            f"[TraceEmitter] emit failed for node={event.node_name} op={event.operation_type}: {type(exc).__name__}",
            file=sys.stderr,
        )


def create_analysis_node(
    ctx: ExecutionContext,
    *,
    model: str | None = None,
    max_retries: int = 2,
) -> Callable[[ExecutionState], NodeUpdateAlias]:
    """Create a PoC analysis node demonstrating the execution model.

    The returned callable:

    1. Reads issue context from state via the ``ToolRegistry``.
    2. Invokes ``ReasoningProvider`` with a prompt and optional model.
    3. Validates the structured response.
    4. Returns a state update with the analysis result.

    Args:
        ctx: Injected execution context (providers + config).
        model: Optional model identifier override.
        max_retries: Maximum retry attempts for reasoning failures.

    Returns:
        A LangGraph-compatible node callable.
    """
    if ctx.reasoning is None:  # type: ignore[comparison-overlap]
        raise ValueError("ExecutionContext.reasoning provider is not configured")
    if max_retries < 0:
        raise ValueError(f"max_retries must be >= 0, got {max_retries}")

    default_model_raw = ctx.config.get("default_model", "")
    if not isinstance(default_model_raw, str):
        raise ValueError(
            f"ExecutionContext.config 'default_model' must be a string, got {type(default_model_raw).__name__!r}"
        )
    effective_model = model or default_model_raw

    def _node(state: ExecutionState) -> NodeUpdateAlias:
        # ------------------------------------------------------------------
        # Step 1: Read context via ToolRegistry
        # ------------------------------------------------------------------
        issue_context: JSONValue = ""
        tool_start = time.time()
        try:
            raw_result = ctx.tools.invoke("get_issue_context", node_name=NODE_NAME, state=cast(JSONValue, state))
            tool_duration = (time.time() - tool_start) * 1000

            # Unwrap ToolResult envelope if present
            if isinstance(raw_result, dict) and "success" in raw_result:
                if not raw_result.get("success"):
                    error_type = raw_result.get("error_type", "unknown")
                    error_msg = str(
                        raw_result.get("error_message")
                        or raw_result.get("error")
                        or raw_result.get("message")
                        or raw_result.get("stderr")
                        or "Tool invocation failed"
                    )
                    _emit_best_effort(
                        ctx.tracer,
                        make_trace_event(
                            node_name=NODE_NAME,
                            operation_type="tool_invocation",
                            tool_name="get_issue_context",
                            input_summary="state",
                            output_summary=f"error_type={error_type}",
                            duration_ms=tool_duration,
                            success=False,
                        ),
                    )
                    return {
                        "status": "failed",
                        "error": f"Tool invocation failed: tool=get_issue_context error_type={error_type}: {error_msg}",
                    }
                issue_context = raw_result.get("output", raw_result)
            else:
                issue_context = raw_result

            _emit_best_effort(
                ctx.tracer,
                make_trace_event(
                    node_name=NODE_NAME,
                    operation_type="tool_invocation",
                    tool_name="get_issue_context",
                    input_summary="state",
                    output_summary=_summarize_json_value(issue_context),
                    duration_ms=tool_duration,
                    success=True,
                ),
            )
        except Exception as exc:  # noqa: BLE001  # catch all registry failures — different implementations may raise different types
            tool_duration = (time.time() - tool_start) * 1000
            _emit_best_effort(
                ctx.tracer,
                make_trace_event(
                    node_name=NODE_NAME,
                    operation_type="tool_invocation",
                    tool_name="get_issue_context",
                    input_summary="state",
                    output_summary=f"error_type={type(exc).__name__}",
                    duration_ms=tool_duration,
                    success=False,
                ),
            )
            return {
                "status": "failed",
                "error": f"Tool invocation failed: tool=get_issue_context error_type={type(exc).__name__}",
            }

        # ------------------------------------------------------------------
        # Step 2: Invoke LLM reasoning with retry
        # ------------------------------------------------------------------
        prompt = f"Analyze the following issue context and produce a structured plan:\n\n{issue_context}"

        def _reason(retry_ctx: RetryContext) -> NodeUpdateAlias:
            if retry_ctx.attempt > 0:
                augmented_prompt = (
                    prompt + f"\n\nThis is retry attempt {retry_ctx.attempt}."
                    f" {retry_ctx.attempt} previous attempt(s) failed."
                    " Adjust your approach."
                )
            else:
                augmented_prompt = prompt

            # Tracks whether a failure trace was already emitted within THIS
            # retry attempt (e.g., by the parse-failure path).  Reset to False
            # on every new attempt because _reason() is re-invoked from scratch
            # by with_retry() on each iteration.
            _failure_already_traced = False
            reasoning_start = time.time()
            try:
                response = ctx.reasoning.invoke(
                    augmented_prompt,
                    model=effective_model or None,
                )
                reasoning_duration = (time.time() - reasoning_start) * 1000

                usage_dict: dict[str, JSONValue] = {}
                if response.usage is not None:
                    usage_dict = {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                    }

                # Validate structured output BEFORE emitting the success trace so
                # that a parse failure produces only a failure trace — not a
                # misleading success trace followed by a failure trace.
                parsed = response.parsed_output
                if parsed is None:
                    # Try parsing raw_text as JSON
                    try:
                        parsed = json.loads(response.raw_text)
                    except (json.JSONDecodeError, TypeError) as parse_exc:
                        _failure_already_traced = True
                        _emit_best_effort(
                            ctx.tracer,
                            make_trace_event(
                                node_name=NODE_NAME,
                                operation_type="reasoning",
                                model_id=effective_model,
                                input_summary=_summarize_reasoning_input(augmented_prompt),
                                output_summary=f"parse_error_type={type(parse_exc).__name__}",
                                duration_ms=reasoning_duration,
                                success=False,
                            ),
                        )
                        raise ValueError("Malformed LLM response") from parse_exc

                # Emit the success trace only after validation has passed.
                _emit_best_effort(
                    ctx.tracer,
                    make_trace_event(
                        node_name=NODE_NAME,
                        operation_type="reasoning",
                        model_id=effective_model,
                        input_summary=_summarize_reasoning_input(augmented_prompt),
                        output_summary=_summarize_reasoning_output(
                            response.raw_text,
                            parsed_output=parsed,
                        ),
                        duration_ms=reasoning_duration,
                        success=True,
                        usage=usage_dict,
                    ),
                )

                return {
                    "status": "completed",
                    "error": None,
                    "analysis_result": parsed,
                }

            except ReasoningTimeoutError:
                reasoning_duration = (time.time() - reasoning_start) * 1000
                _emit_best_effort(
                    ctx.tracer,
                    make_trace_event(
                        node_name=NODE_NAME,
                        operation_type="reasoning",
                        model_id=effective_model,
                        input_summary=_summarize_reasoning_input(augmented_prompt),
                        output_summary="timeout",
                        duration_ms=reasoning_duration,
                        success=False,
                    ),
                )
                raise
            except Exception as exc:
                # Emit a failure trace for any unexpected provider exception
                # (e.g., network errors, schema errors).  Skip emission when the
                # parse-failure path already traced the event to avoid
                # double-emission.
                if not _failure_already_traced:
                    reasoning_duration = (time.time() - reasoning_start) * 1000
                    _emit_best_effort(
                        ctx.tracer,
                        make_trace_event(
                            node_name=NODE_NAME,
                            operation_type="reasoning",
                            model_id=effective_model,
                            input_summary=_summarize_reasoning_input(augmented_prompt),
                            output_summary=f"error_type={type(exc).__name__}",
                            duration_ms=reasoning_duration,
                            success=False,
                        ),
                    )
                raise

        try:
            return with_retry(_reason, max_retries=max_retries)
        except Exception as exc:  # noqa: BLE001
            return {
                "status": "failed",
                "error": f"Reasoning failed after {max_retries + 1} attempts: error_type={type(exc).__name__}",
                "retry_count": max_retries + 1,
            }

    return _node


def _summarize_json_value(value: JSONValue) -> str:
    """Return non-sensitive metadata for a JSON-like value."""
    if isinstance(value, dict):
        return f"dict(keys={len(value)})"
    if isinstance(value, list):
        return f"list(items={len(value)})"
    if isinstance(value, str):
        return f"str(chars={len(value)})"
    return type(value).__name__


def _summarize_reasoning_input(prompt: str) -> str:
    """Return prompt metadata without logging prompt content."""
    return f"prompt_chars={len(prompt)}"


def _summarize_reasoning_output(raw_text: str, *, parsed_output: JSONValue | None) -> str:
    """Return model-output metadata without logging raw model text."""
    return f"raw_text_chars={len(raw_text)} parsed_type={type(parsed_output).__name__}"
