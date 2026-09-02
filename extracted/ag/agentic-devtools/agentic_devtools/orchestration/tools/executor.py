"""Tool executor with cross-cutting concerns (FR-003, FR-004, FR-005, FR-007).

``ToolExecutor`` wraps tool invocations with:
1. Input validation (FR-006)
2. Dry-run enforcement (FR-004)
3. Timeout handling (FR-007)
4. Thread-safety enforcement
5. Audit logging (FR-005)
6. Structured ToolResult wrapping (FR-003)
"""

from __future__ import annotations

import concurrent.futures
import json
import logging
import threading
import time
from collections.abc import Callable
from typing import Any

from .audit import emit_audit_log
from .definition import ToolDefinition
from .registry import ConcreteToolRegistry
from .result import ToolResult
from .validation import validate_inputs

logger = logging.getLogger(__name__)


class ToolExecutor:
    """Executes tools with validation, dry-run, timeout, and audit.

    Immutable after construction (correlation_id, registry ref,
    max_output_summary_length). Internal per-tool locks may mutate
    during execution.

    Args:
        registry: The tool registry containing definitions and functions.
        correlation_id: Links audit entries to a graph execution context.
        max_output_summary_length: Max chars for audit output_summary.

    Notes:
        Uses a single shared ``ThreadPoolExecutor`` per instance for all tool
        executions.  This avoids per-call pool creation and the accumulation of
        background threads when timeouts fire repeatedly.
        ``ThreadPoolExecutor`` cannot preempt a running thread; a timed-out
        tool continues executing until it returns or raises.  Callers that
        require hard-kill semantics should use a subprocess-based executor
        instead.  Call :meth:`shutdown` when the executor is no longer needed.
    """

    _MAX_POOL_WORKERS = 8

    def __init__(
        self,
        registry: ConcreteToolRegistry,
        *,
        correlation_id: str = "",
        max_output_summary_length: int = 500,
        dry_run_fn: Callable[[], bool] | None = None,
        safety_enforcer: Any | None = None,
    ) -> None:
        if dry_run_fn is not None and not callable(dry_run_fn):
            raise TypeError(f"dry_run_fn must be callable, got {type(dry_run_fn).__name__!r}")
        self._registry = registry
        self._correlation_id = correlation_id
        self._max_output_summary_length = max_output_summary_length
        self._dry_run_fn = dry_run_fn
        self._safety_enforcer = safety_enforcer
        self._locks: dict[str, threading.Lock] = {}
        self._locks_lock = threading.Lock()
        # Shared bounded worker pool – created once per instance and reused
        # across all tool invocations to prevent per-call pool proliferation.
        self._pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=self._MAX_POOL_WORKERS,
            thread_name_prefix="tool_exec",
        )

    def shutdown(self, *, wait: bool = True) -> None:
        """Shut down the shared worker pool.

        Call once when this executor is no longer needed (e.g. at the end of a
        LangGraph session) to release pool threads promptly.
        """
        self._pool.shutdown(wait=wait, cancel_futures=not wait)

    def _get_tool_lock(self, tool_name: str) -> threading.Lock:
        """Get or create a per-tool lock."""
        with self._locks_lock:
            if tool_name not in self._locks:
                self._locks[tool_name] = threading.Lock()
            return self._locks[tool_name]

    def _is_dry_run(self) -> bool:
        """Check if dry-run mode is enabled."""
        if self._dry_run_fn is not None:
            return self._dry_run_fn()
        from agentic_devtools.state import is_dry_run

        return is_dry_run()

    def execute(self, tool_name: str, inputs: dict[str, Any] | None = None, *, node_name: str = "") -> ToolResult:
        """Execute a tool with all cross-cutting concerns.

        Steps:
        1. Look up tool definition
        2. Validate inputs against schema
        3. Check dry-run mode for mutating tools
        4. Enforce thread-safety locks
        5. Execute with timeout
        6. Emit audit log
        7. Return structured ToolResult

        Args:
            tool_name: The name of the tool to execute.
            inputs: Tool invocation inputs.
            node_name: The graph node invoking the tool. Passed to the safety
                enforcer so operation log records carry the correct node context
                (FR-006). Required for external-mutation and destructive tools.
        """
        if inputs is None:
            inputs = {}

        start_time = time.time()

        # Step 1: Look up tool
        definition = self._registry.get(tool_name)
        if definition is None:
            duration_ms = (time.time() - start_time) * 1000
            result = ToolResult(
                success=False,
                error_type="not_found",
                error_message=f"Tool not registered: {tool_name!r}",
                duration_ms=duration_ms,
            )
            self._emit_audit(tool_name, inputs, result, "error")
            return result

        # Step 2: Validate inputs
        validation_result = validate_inputs(definition.input_schema, inputs)
        if validation_result is not None:
            duration_ms = (time.time() - start_time) * 1000
            result = ToolResult(
                success=False,
                error_type="validation_error",
                error_message=validation_result.error_message,
                duration_ms=duration_ms,
            )
            self._emit_audit(tool_name, inputs, result, "validation_error")
            return result

        # Step 3: Safety enforcement (replaces legacy dry-run check when enforcer present)
        operation_id: str | None = None
        if self._safety_enforcer is not None:
            try:
                decision = self._safety_enforcer.evaluate(tool_name, inputs, node_name=node_name)
                if decision.action == "simulate":
                    duration_ms = (time.time() - start_time) * 1000
                    from agentic_devtools.orchestration.execution.tracing import redact_sensitive_keys

                    redacted = redact_sensitive_keys(inputs) if isinstance(inputs, dict) else inputs
                    result = ToolResult(
                        success=True,
                        output={"would_execute": tool_name, "inputs": redacted},
                        dry_run=True,
                        duration_ms=duration_ms,
                    )
                    self._emit_audit(tool_name, inputs, result, "dry_run_skipped")
                    return result
                elif decision.action == "skip_duplicate":
                    duration_ms = (time.time() - start_time) * 1000
                    replay_output = decision.replay_record.result_payload if decision.replay_record else None
                    result = ToolResult(
                        success=True,
                        output=replay_output,
                        duration_ms=duration_ms,
                    )
                    self._emit_audit(tool_name, inputs, result, "skipped_duplicate")
                    return result
                elif decision.action == "block":
                    duration_ms = (time.time() - start_time) * 1000
                    result = ToolResult(
                        success=False,
                        error_type="precondition_not_met",
                        error_message=decision.reason,
                        duration_ms=duration_ms,
                    )
                    self._emit_audit(tool_name, inputs, result, "precondition_not_met")
                    return result
                elif decision.action == "execute":
                    # Capture operation_id for lifecycle recording and record
                    # the operation as pending before execution begins.
                    operation_id = decision.operation_id
                    if operation_id is not None:
                        self._safety_enforcer.record_pending(tool_name, inputs, operation_id, node_name=node_name)
                else:
                    # Unknown action — fail closed; a safety gate must never
                    # silently allow an unrecognised decision through.
                    duration_ms = (time.time() - start_time) * 1000
                    result = ToolResult(
                        success=False,
                        error_type="precondition_not_met",
                        error_message=f"Unknown safety decision action: {decision.action!r}",
                        duration_ms=duration_ms,
                    )
                    self._emit_audit(tool_name, inputs, result, "precondition_not_met")
                    return result
            except Exception as exc:  # noqa: BLE001
                duration_ms = (time.time() - start_time) * 1000
                result = ToolResult(
                    success=False,
                    error_type="precondition_not_met",
                    error_message=str(exc),
                    duration_ms=duration_ms,
                )
                self._emit_audit(tool_name, inputs, result, "precondition_not_met")
                return result
        elif self._is_dry_run() and definition.mutating:
            # Legacy dry-run check (backward compatibility when no enforcer)
            duration_ms = (time.time() - start_time) * 1000
            from agentic_devtools.orchestration.execution.tracing import redact_sensitive_keys

            redacted = redact_sensitive_keys(inputs) if isinstance(inputs, dict) else inputs
            result = ToolResult(
                success=True,
                output={"would_execute": tool_name, "inputs": redacted},
                dry_run=True,
                duration_ms=duration_ms,
            )
            self._emit_audit(tool_name, inputs, result, "dry_run_skipped")
            return result

        # Step 4: Thread-safety enforcement
        if not definition.thread_safe:
            lock = self._get_tool_lock(tool_name)
            acquired = lock.acquire(blocking=False)
            if not acquired:
                duration_ms = (time.time() - start_time) * 1000
                result = ToolResult(
                    success=False,
                    error_type="precondition_not_met",
                    error_message="tool_busy",
                    duration_ms=duration_ms,
                )
                self._emit_audit(tool_name, inputs, result, "precondition_not_met")
                if self._safety_enforcer is not None and operation_id is not None:
                    self._safety_enforcer.record_failed(
                        operation_id, tool_name, error_message="tool_busy", node_name=node_name
                    )
                return result
            result = self._execute_with_timeout(
                definition,
                tool_name,
                inputs,
                start_time,
                release_lock=lock.release,
            )
        else:
            result = self._execute_with_timeout(definition, tool_name, inputs, start_time)

        # Record the completed/failed lifecycle entry in the operation log so
        # that idempotency duplicate-skip works correctly on retry/resume.
        # On timeout we intentionally leave the "pending" record intact: the
        # tool's external mutation may still complete in the background, so
        # recording "failed" would allow an unsafe retry.  The "pending" status
        # blocks retries by default (allow_pending_reexecute=True required).
        if self._safety_enforcer is not None and operation_id is not None:
            if result.success:
                self._safety_enforcer.record_completed(
                    operation_id,
                    tool_name,
                    result_summary=str(result.output)[:200] if result.output is not None else "",
                    result_payload=result.output,
                    node_name=node_name,
                )
            elif result.error_type != "timeout":
                self._safety_enforcer.record_failed(
                    operation_id, tool_name, error_message=result.error_message or "", node_name=node_name
                )

        return result

    def _execute_with_timeout(
        self,
        definition: ToolDefinition,
        tool_name: str,
        inputs: dict[str, Any],
        start_time: float,
        release_lock: Callable[[], None] | None = None,
    ) -> ToolResult:
        """Execute the tool function with timeout enforcement.

        Uses the shared ``self._pool`` to avoid per-call pool creation.
        On timeout the future is cancelled, but the worker thread may keep
        running until it finishes (``ThreadPoolExecutor`` cannot preempt
        threads).  For non-thread-safe tools, the per-tool lock is released
        as soon as the future is confirmed done.
        """
        fn = self._registry.get_function(tool_name)
        if fn is None:  # pragma: no cover
            duration_ms = (time.time() - start_time) * 1000
            result = ToolResult(
                success=False,
                error_type="not_found",
                error_message=f"Tool function not found: {tool_name!r}",
                duration_ms=duration_ms,
            )
            self._emit_audit(tool_name, inputs, result, "error")
            return result

        future: concurrent.futures.Future[Any] | None = None
        # Sentinel: set to None inside the timeout branch when lock release is
        # already scheduled via add_done_callback so the finally block skips it.
        pending_release = release_lock

        try:
            future = self._pool.submit(fn, **inputs)
            output = future.result(timeout=definition.timeout_seconds)
            duration_ms = (time.time() - start_time) * 1000
            # Detect domain-level failures encoded as {"success": False, ...}.
            # Tool functions may return such dicts instead of raising (e.g.
            # detached HEAD, missing file).  Treat them as execution failures so
            # callers that branch on ToolResult.success see the correct signal.
            # `is False` is intentional: only an explicit False boolean signals
            # a domain failure; falsy values like None or 0 are not treated as
            # failures so we don't suppress valid outputs that happen to be falsy.
            if isinstance(output, dict) and output.get("success") is False:
                # Probe several keys used by different builtin tool families:
                # "error" / "error_message" — filesystem, ci-checks tools
                # "message" — git tools (detached HEAD, not-a-repo)
                # "stderr"  — testing tools (invalid pattern etc.)
                error_msg = str(
                    output.get("error")
                    or output.get("error_message")
                    or output.get("message")
                    or output.get("stderr")
                    or "tool reported failure"
                )
                result = ToolResult(
                    success=False,
                    output=output,
                    error_type="execution_error",
                    error_message=error_msg,
                    duration_ms=duration_ms,
                )
                self._emit_audit(tool_name, inputs, result, "error")
            else:
                result = ToolResult(
                    success=True,
                    output=output,
                    duration_ms=duration_ms,
                )
                self._emit_audit(tool_name, inputs, result, "success")
            return result

        except concurrent.futures.TimeoutError:
            assert future is not None
            future.cancel()
            if pending_release is not None:
                if future.done():
                    pending_release()
                else:
                    # add_done_callback expects Callable[[Future[T]], None] but
                    # release_lock is Callable[[], None]; the lambda bridges the gap.
                    future.add_done_callback(lambda _: release_lock())  # type: ignore[misc]
                pending_release = None  # prevent finally from releasing again
            duration_ms = (time.time() - start_time) * 1000
            result = ToolResult(
                success=False,
                error_type="timeout",
                error_message=f"Tool '{tool_name}' timed out after {definition.timeout_seconds}s",
                duration_ms=duration_ms,
            )
            self._emit_audit(tool_name, inputs, result, "timeout")
            return result

        except Exception as exc:  # noqa: BLE001
            duration_ms = (time.time() - start_time) * 1000
            result = ToolResult(
                success=False,
                error_type="execution_error",
                error_message=str(exc),
                duration_ms=duration_ms,
            )
            self._emit_audit(tool_name, inputs, result, "error")
            return result

        finally:
            if pending_release is not None:
                pending_release()

    def _emit_audit(
        self,
        tool_name: str,
        inputs: dict[str, Any],
        result: ToolResult,
        status: str,
    ) -> None:
        """Emit audit log entry (best-effort, never raises)."""
        try:
            emit_audit_log(
                tool_name=tool_name,
                inputs=inputs,
                output=result.output,
                duration_ms=result.duration_ms,
                status=status,
                error_type=result.error_type,
                error_message=result.error_message,
                correlation_id=self._correlation_id,
                max_output_summary_length=self._max_output_summary_length,
            )
        except Exception:  # noqa: BLE001
            logger.warning("Failed to emit audit log for tool %r", tool_name, exc_info=True)

    def list_all(self) -> dict[str, ToolDefinition]:
        """Protocol-compatible delegation to the underlying registry.

        Returns a flat mapping of all registered tool definitions.
        """
        return self._registry.list_all()

    def get_categories(self) -> list[str]:
        """Protocol-compatible delegation to the underlying registry.

        Returns a sorted list of all registered category names.
        """
        return self._registry.get_categories()

    def invoke(self, tool_name: str, **kwargs: Any) -> Any:
        """Protocol-compatible invoke facade.

        Returns a JSON-serializable dict (ToolResult envelope).
        Reserved kwarg ``node_name`` is consumed as execution context and is
        not forwarded to the underlying tool inputs.
        """
        definition = self._registry.get(tool_name)
        has_node_name_context = "node_name" in kwargs
        if has_node_name_context and definition is not None:
            properties = definition.input_schema.get("properties")
            if isinstance(properties, dict) and "node_name" in properties:
                result = ToolResult(
                    success=False,
                    error_type="validation_error",
                    error_message=(
                        "Ambiguous invoke argument 'node_name': reserved for execution context and "
                        "also declared as tool input."
                    ),
                )
                return json.loads(result.to_json())
        node_name = kwargs.pop("node_name", "")
        result = self.execute(tool_name, kwargs, node_name=node_name)
        return json.loads(result.to_json())
