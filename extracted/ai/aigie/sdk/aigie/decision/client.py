"""Async gRPC client for ``kytte.decision.v1.DecisionOrchestrator``.

One unary RPC: ``EvaluateSpan``, fired once per finalized span. The SDK
returns the decision when the caller awaits it, but failures stay fail-open:
callers often schedule it with ``asyncio.create_task`` and an escaping exception
would only produce "Task exception was never retrieved" noise.
"""

import asyncio
import logging
from typing import Any  # noqa: TID251 — generated proto types are dynamically typed.

import grpc
from google.protobuf import json_format

from aigie._grpc import (
    _DEFAULT_DECISION_GRPC_PORT,
    grpc_is_unreachable,
    split_host_port,
    unreachable_hint,
)
from aigie.decision._pb.kytte.decision.v1 import decision_pb2 as _decision_pb2
from aigie.decision._pb.kytte.decision.v1 import decision_pb2_grpc as pb_grpc
from aigie.decision._pb.kytte.remediation.v1 import step_pb2 as _step_pb2
from aigie.decision.executor import StepExecutor
from aigie.decision.models import RemediationDecision
from aigie.decision.steps import StepContext, StepOutcome, StepStatus, VerbSpec
from aigie.diagnostics import N010, R007, format_diagnostic
from aigie.rewind.coordinator import RewindCoordinator
from aigie.telemetry import _metric_add, get_meter

pb: Any = _decision_pb2
step_pb: Any = _step_pb2

logger = logging.getLogger(__name__)

# The call is advisory and runs as a detached task, but the deadline must
# outlive the platform's judge pipeline: gRPC cancels the SERVER handler when
# the client deadline expires, which would kill verdict persistence mid-run.
# CPU SLM selector + tier-1 judges currently need 10-40s per span.
_DEFAULT_TIMEOUT_S = 120

# Registration is advisory; keep retries bounded.
_REGISTER_TIMEOUT_S = 10
_REGISTER_MAX_ATTEMPTS = 3
_REGISTER_RETRY_BACKOFF_S = 0.5
_METER_NAME = "kytte.decision"


def _capability_registration_counter() -> Any:
    return get_meter(_METER_NAME).create_counter(
        "kytte.decision.capability_registration",
        description="RegisterCapabilities outcomes (attr: outcome=success|failure)",
        unit="1",
    )


def _tool_catalog_registration_counter() -> Any:
    return get_meter(_METER_NAME).create_counter(
        "kytte.decision.tool_catalog_registration",
        description="RegisterToolCatalog outcomes (attr: outcome=success|failure)",
        unit="1",
    )


def _verb_spec_proto(spec: VerbSpec) -> Any:
    out = step_pb.VerbSpec(name=spec.name, description=spec.description)
    json_format.ParseDict(spec.param_schema, out.param_schema)
    return out


def _tool_proto(tool: dict[str, Any]) -> Any:
    out = step_pb.Tool(name=tool["name"], description=tool.get("description", ""))
    json_format.ParseDict(tool.get("input_schema") or {}, out.input_schema)
    return out


class DecisionClient:
    """Long-lived gRPC client wrapping a single channel + stub.

    Thread-safety: ``grpc.aio.Channel`` is coroutine-safe for concurrent
    unary calls, so we don't add a lock.
    """

    def __init__(
        self,
        endpoint: str,
        api_key: str | None = None,
        *,
        use_tls: bool = False,
        timeout_s: float = _DEFAULT_TIMEOUT_S,
        step_executor: StepExecutor | None = None,
        rewind_coordinator: RewindCoordinator | None = None,
    ) -> None:
        host, port = split_host_port(endpoint)
        self._target = f"{host}:{port or _DEFAULT_DECISION_GRPC_PORT}"
        self._use_tls = use_tls
        self._timeout_s = timeout_s
        self._metadata: tuple[tuple[str, str], ...] = (("x-api-key", api_key),) if api_key else ()
        self._channel: grpc.aio.Channel | None = None
        self._stub: pb_grpc.DecisionOrchestratorStub | None = None
        self._step_executor = step_executor
        self._rewind_coordinator = rewind_coordinator
        # Warn at most once per outage; reset on the next successful call.
        self._unreachable_logged = False

    @property
    def target(self) -> str:
        return self._target

    def _ensure_channel(self) -> pb_grpc.DecisionOrchestratorStub:
        if self._stub is not None:
            return self._stub
        if self._use_tls:
            creds = grpc.ssl_channel_credentials()
            self._channel = grpc.aio.secure_channel(self._target, creds)
        else:
            self._channel = grpc.aio.insecure_channel(self._target)
        self._stub = pb_grpc.DecisionOrchestratorStub(self._channel)
        logger.debug("DecisionClient channel opened: target=%s tls=%s", self._target, self._use_tls)
        return self._stub

    async def evaluate_span(self, span: Any) -> RemediationDecision | None:
        """Evaluate one finalized span; return ``None`` if the RPC fails."""
        try:
            stub = self._ensure_channel()
            response = await stub.EvaluateSpan(
                pb.EvaluateSpanRequest(span=span, trace_id=span.trace_id),
                metadata=self._metadata,
                timeout=self._timeout_s,
            )
            self._unreachable_logged = False
            decision = RemediationDecision.from_response(response)
            self._log_decision(span, decision)
            if decision.apply and decision.execution_id:
                await self._apply_and_report(span, decision, decision.execution_id)
            return decision
        except Exception as e:
            # Fire-and-forget contract: any failure is dropped, not raised. A
            # connectivity failure surfaces once as a warning (so a silently
            # disabled error-evaluation path is visible); everything else, and
            # repeats of the same outage, stay at debug.
            self._swallow_rpc_error(e, f"EvaluateSpan span={span.span_id}")
            return None

    async def _register_with_retry(self, rpc_name: str, request: Any, counter: Any) -> Any | None:
        """Call an advisory registration RPC with bounded retries."""
        for attempt in range(1, _REGISTER_MAX_ATTEMPTS + 1):
            try:
                stub = self._ensure_channel()
                response = await getattr(stub, rpc_name)(
                    request, metadata=self._metadata, timeout=_REGISTER_TIMEOUT_S
                )
                self._unreachable_logged = False
                _metric_add(counter, 1, {"outcome": "success"})
                return response
            except Exception as e:  # noqa: BLE001 — registration must never crash
                if attempt < _REGISTER_MAX_ATTEMPTS:
                    await asyncio.sleep(_REGISTER_RETRY_BACKOFF_S * attempt)
                    continue
                _metric_add(counter, 1, {"outcome": "failure"})
                self._swallow_rpc_error(e, rpc_name)
        return None

    async def register_capabilities(self, *, schema_version: int = 1) -> int | None:
        """Advertise the executor's supported verbs and return the accepted count."""
        if self._step_executor is None:
            return None
        from aigie import __version__ as _sdk_version

        request = pb.RegisterCapabilitiesRequest(
            schema_version=schema_version,
            verbs=[_verb_spec_proto(s) for s in self._step_executor.capabilities()],
            sdk_version=_sdk_version,
        )
        response = await self._register_with_retry(
            "RegisterCapabilities",
            request,
            _capability_registration_counter,
        )
        if response is None:
            return None
        logger.info(
            "[AIGIE] advertised %d remediation verbs to the Decision Orchestrator",
            response.accepted,
        )
        return int(response.accepted)

    async def register_tool_catalog(
        self, tool_registry_hash: str, catalog: list[dict[str, Any]]
    ) -> int | None:
        """Register a run's tool inventory by content hash."""
        if not catalog:
            return None
        request = pb.RegisterToolCatalogRequest(
            tool_registry_hash=tool_registry_hash,
            tools=[_tool_proto(t) for t in catalog],
        )
        response = await self._register_with_retry(
            "RegisterToolCatalog",
            request,
            _tool_catalog_registration_counter,
        )
        if response is None:
            return None
        logger.info(
            "[AIGIE] registered tool catalog (%d tools, hash=%s) with the Decision Orchestrator",
            response.accepted,
            tool_registry_hash[:12],
        )
        return int(response.accepted)

    def _log_decision(self, span: Any, decision: RemediationDecision) -> None:
        level = logging.INFO if decision.action_selected else logging.DEBUG
        logger.log(
            level,
            "[AIGIE] remediation decision span=%s verdict=%s problem=%s steps=%d "
            "apply=%s execution_id=%s",
            span.span_id,
            decision.verdict,
            decision.problem_type,
            len(decision.steps),
            decision.apply,
            decision.execution_id,
        )

    async def _apply_and_report(
        self, span: Any, decision: RemediationDecision, execution_id: str
    ) -> None:
        if self._step_executor is None:
            await self.report_execution_result(
                execution_id, False, "apply requested but no step executor configured"
            )
            return
        ctx = StepContext(
            trace_id=span.trace_id,
            span_id=span.span_id,
            execution_id=execution_id,
            span=span,
            rewind_coordinator=self._rewind_coordinator,
            logger=logger,
        )
        outcomes = await self._step_executor.execute(decision.steps, ctx)
        success = bool(outcomes) and all(o.status == StepStatus.APPLIED for o in outcomes)
        error = "" if success else (_summarize(outcomes) or "no steps to apply")
        await self.report_execution_result(execution_id, success, error, outcomes)

    async def report_execution_result(
        self,
        execution_id: str,
        success: bool,
        error: str,
        outcomes: list[StepOutcome] | None = None,
    ) -> None:
        """Report an autonomous action's aggregate outcome plus the per-step
        rollup; fail-open like evaluate_span."""
        try:
            stub = self._ensure_channel()
            await stub.ReportExecutionResult(
                pb.ReportExecutionResultRequest(
                    execution_id=execution_id,
                    success=success,
                    error=error,
                    step_runs=[_step_run(o) for o in outcomes or []],
                ),
                metadata=self._metadata,
                timeout=self._timeout_s,
            )
            self._unreachable_logged = False
        except Exception as e:  # noqa: BLE001 — reporting must never break evaluate_span
            self._swallow_rpc_error(e, f"ReportExecutionResult exec={execution_id}")

    def _swallow_rpc_error(self, error: Exception, context: str) -> None:
        """Log fail-open RPC errors without raising into callers."""
        if grpc_is_unreachable(error) and not self._unreachable_logged:
            self._log_unreachable(error)
        else:
            logger.debug(format_diagnostic(R007, extra=f"{context}: {error}"))

    def _log_unreachable(self, error: BaseException) -> None:
        """Warn once per outage when the Decision Orchestrator can't be reached."""
        self._unreachable_logged = True
        code = getattr(error, "code", None)
        status = code().name if callable(code) else "UNAVAILABLE"
        logger.warning(
            f"[{N010.code}] Cannot reach the Decision Orchestrator at %s (%s) — error "
            "evaluation is paused; tracing is unaffected. Hint: %s.",
            self._target,
            status,
            unreachable_hint(use_tls=self._use_tls, plaintext_port=_DEFAULT_DECISION_GRPC_PORT),
        )

    async def close(self) -> None:
        if self._channel is not None:
            await self._channel.close()
            self._channel = None
            self._stub = None


def _step_run(outcome: StepOutcome) -> Any:
    """Map a StepOutcome onto the wire StepRun. Cost is not carried — see the
    StepRun proto comment."""
    return step_pb.StepRun(
        step_id=outcome.step_id,
        verb=outcome.verb,
        status=outcome.status.value,
        reason=outcome.reason,
        latency_ms=outcome.latency_ms,
    )


def _summarize(outcomes: list[StepOutcome]) -> str:
    parts = [
        f"{o.verb}:{o.status.value}" + (f"({o.reason})" if o.reason else "")
        for o in outcomes
        if o.status != StepStatus.APPLIED
    ]
    return "; ".join(parts)
