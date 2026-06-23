"""Async gRPC client for ``kytte.decision.v1.DecisionOrchestrator``.

One unary RPC: ``EvaluateSpan``, fired once per finalized span,
**fire-and-forget** — the SDK never blocks on or consumes the verdict
(Determine Error MVP). ``evaluate_span`` therefore swallows every exception:
callers schedule it with ``asyncio.create_task`` and an escaping exception
would only produce "Task exception was never retrieved" noise.
"""

import logging
from typing import Any  # noqa: TID251 — generated proto types are dynamically typed.

import grpc

from aigie._grpc import (
    _DEFAULT_DECISION_GRPC_PORT,
    grpc_is_unreachable,
    split_host_port,
    unreachable_hint,
)
from aigie.decision._pb.kytte.decision.v1 import decision_pb2 as _decision_pb2
from aigie.decision._pb.kytte.decision.v1 import decision_pb2_grpc as pb_grpc

pb: Any = _decision_pb2

logger = logging.getLogger(__name__)

# The call is advisory and runs as a detached task, but the deadline must
# outlive the platform's judge pipeline: gRPC cancels the SERVER handler when
# the client deadline expires, which would kill verdict persistence mid-run.
# CPU SLM selector + tier-1 judges currently need 10-40s per span.
_DEFAULT_TIMEOUT_S = 120


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
    ) -> None:
        host, port = split_host_port(endpoint)
        self._target = f"{host}:{port or _DEFAULT_DECISION_GRPC_PORT}"
        self._use_tls = use_tls
        self._timeout_s = timeout_s
        self._metadata: tuple[tuple[str, str], ...] = (("x-api-key", api_key),) if api_key else ()
        self._channel: grpc.aio.Channel | None = None
        self._stub: pb_grpc.DecisionOrchestratorStub | None = None
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

    async def evaluate_span(self, span: Any) -> None:
        """Fire one EvaluateSpan for a finalized span. Never raises."""
        try:
            stub = self._ensure_channel()
            await stub.EvaluateSpan(
                pb.EvaluateSpanRequest(span=span, trace_id=span.trace_id),
                metadata=self._metadata,
                timeout=self._timeout_s,
            )
            self._unreachable_logged = False
        except Exception as e:
            # Fire-and-forget contract: any failure is dropped, not raised. A
            # connectivity failure surfaces once as a warning (so a silently
            # disabled error-evaluation path is visible); everything else, and
            # repeats of the same outage, stay at debug.
            if grpc_is_unreachable(e) and not self._unreachable_logged:
                self._log_unreachable(e)
            else:
                logger.debug("[AIGIE] EvaluateSpan dropped for span=%s: %s", span.span_id, e)

    def _log_unreachable(self, error: BaseException) -> None:
        """Warn once per outage when the Decision Orchestrator can't be reached."""
        self._unreachable_logged = True
        code = getattr(error, "code", None)
        status = code().name if callable(code) else "UNAVAILABLE"
        logger.warning(
            "[AIGIE] Cannot reach the Decision Orchestrator at %s (%s) — error "
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
