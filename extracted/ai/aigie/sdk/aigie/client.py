"""
Aigie Client - Main SDK class for integrating Aigie monitoring.
"""

import asyncio
import logging
import os
import signal
import time
from collections import OrderedDict
from collections.abc import Callable, Coroutine, Iterable
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Optional, TypeVar

import grpc
import httpx

from aigie.buffer import BufferedEvent, EventBuffer
from aigie.config import Config
from aigie.diagnostics import (
    C002,
    C003,
    I004,
    R001,
    R002,
    R006,
    format_diagnostic,
)
from aigie.ingest import span_to_proto as _span_to_proto
from aigie.rewind.coordinator import RewindCoordinator
from aigie.trace import TraceContext
from aigie.tracing.trace_state import drain_open_spans_as_interrupted
from aigie.tracing.types import JUDGE_SKIP_STATUSES

if TYPE_CHECKING:
    from aigie.diagnostics import DoctorResult
    from aigie.drift import DriftMonitor
    from aigie.interceptor import InterceptionContext, InterceptorChain, PostCallHook, PreCallHook
    from aigie.rules import LocalRulesEngine, Rule

logger = logging.getLogger(__name__)

# ── Hardcoded behavior constants (formerly Config knobs) ────────────────────
# Buffering
_BATCH_SIZE: int = 100
_FLUSH_INTERVAL: float = 5.0  # seconds
# Cap the per-trace tool_registry_hash registry so a long-lived process can't
# grow it unbounded; traces are short-lived, so oldest-out is safe.
_TOOL_HASH_TRACE_CAP: int = 4096
# Bounded hash -> catalog retention for local remediation validation.
_TOOL_CATALOG_CAP: int = 64
# Retries
_MAX_RETRIES: int = 3
_RETRY_DELAY: float = 1.0  # base delay in seconds
# HTTP
_TIMEOUT: float = 30.0
_CONNECT_TIMEOUT: float = 5.0  # TCP connect timeout — fail fast on unreachable backends
_MAX_CONNECTIONS: int = 10
# Circuit breaker
_CIRCUIT_BREAKER_THRESHOLD: int = 5  # failures before opening
_CIRCUIT_BREAKER_TIMEOUT: float = 60.0  # seconds before retry
# Sampling — always send everything
_SAMPLING_RATE: float = 1.0

# Global singleton instance
_global_aigie: Optional["Aigie"] = None
_instrumentation_enabled: bool = False
import threading

_global_lock = threading.Lock()

_V = TypeVar("_V")


def _lru_put(registry: OrderedDict[str, _V], key: str, value: _V, cap: int) -> None:
    """Insert into a bounded most-recently-used registry, evicting oldest first."""
    registry[key] = value
    registry.move_to_end(key)
    while len(registry) > cap:
        registry.popitem(last=False)


class Aigie:
    """
    Main Aigie client for monitoring AI agent workflows.

    Usage:
        aigie = Aigie()
        await aigie.initialize()

        async with aigie.trace("My Workflow") as trace:
            # Your code here
            pass

    With debug mode:
        aigie = Aigie(debug=True)  # or AIGIE_DEBUG=true
    """

    def __init__(
        self,
        kytte_url: str | None = None,  # Primary: Kytte platform URL
        kytte_token: str | None = None,  # Primary: Kytte authentication token
        *,
        config: Config | None = None,
        log_level: str | None = None,
        agent_name: str | None = None,
    ):
        """
        Initialize Aigie client.

        Args:
            kytte_url: Kytte platform URL (defaults to KYTTE_URL env var)
            kytte_token: Kytte authentication token (REQUIRED for data to be sent)
            config: Optional Config object (if provided, overrides other params)
            log_level: Control logging verbosity (DEBUG, INFO, WARNING, ERROR,
                CRITICAL). Pass "DEBUG" for the former debug=True behavior.
            agent_name: Agent/deployment name for identification
        """
        # ── URL / token resolution: explicit param > KYTTE_* env vars
        effective_url = kytte_url or os.getenv("KYTTE_URL", "")
        effective_token = kytte_token or os.getenv("KYTTE_TOKEN")

        # Use config if provided, otherwise create from params/env
        if config:
            self.config = config
            self._aigie_url = config.aigie_url
            # Use the effective token from constructor if provided, otherwise from config
            self._auth_token = effective_token or config.get_auth_token()
        else:
            self.config = Config(
                aigie_url=effective_url,
                aigie_token=effective_token,
                log_level=log_level or os.getenv("AIGIE_LOG_LEVEL", "WARNING"),
            )
            self._aigie_url = self.config.aigie_url
            self._auth_token = self.config.get_auth_token()

        # Agent identification metadata
        self._agent_name = agent_name or os.getenv("AIGIE_AGENT_NAME")

        # Configure logging level
        # Priority: log_level parameter > AIGIE_LOG_LEVEL env var > default WARNING
        level_str = (
            log_level or self.config.log_level or os.getenv("AIGIE_LOG_LEVEL", "WARNING")
        ).upper()
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        effective_log_level = level_map.get(level_str, logging.WARNING)

        # Configure all AIGIE-related loggers
        self._configure_logging(effective_log_level)

        self._debug = effective_log_level == logging.DEBUG
        if self._debug:
            from aigie import decorators_v3

            decorators_v3.set_debug_mode(True)
            logger.debug("Aigie client initialized in debug mode")

        self._rewind_coordinator = RewindCoordinator()
        self.client: httpx.AsyncClient | None = None
        self._initialized: bool = False
        self._init_status: str = "pending"  # "pending", "ok", "partial", "failed"
        self._init_errors: list[str] = []
        # Auth retry state (replaces permanent _auth_failed kill-switch)
        self._auth_suspended: bool = False  # True while backing off after 401
        self._auth_retry_count: int = 0
        self._auth_max_retries: int = 5
        self._auth_backoff_base: float = 2.0  # seconds, doubles each retry
        self._auth_periodic_retry_interval: float = 300.0  # 5 min after max retries
        self._auth_next_retry_at: float = 0.0  # time.monotonic() timestamp
        self._closing: bool = False
        self._buffer: EventBuffer | None = None

        # Real-time interception components
        self._interceptor_chain: InterceptorChain | None = None
        self._rules_engine: LocalRulesEngine | None = None
        self._drift_monitor: DriftMonitor | None = None

        # Callback handlers (LiteLLM-style)
        self._callbacks: list[Any] = []

        # Backend health / signals
        self._signal_reporter: Any | None = None
        self._health_monitor: Any | None = None

        # Judge LLM client (closed at shutdown if set externally)
        self._judge_llm_client: Any | None = None

    def _configure_logging(self, level: int) -> None:
        """Configure logging for AIGIE and related libraries to reduce noise.

        By default, sets all AIGIE-related loggers to WARNING level to provide
        a clean customer experience. Only errors and critical issues are shown.

        Args:
            level: Logging level (logging.DEBUG, logging.INFO, etc.)
        """
        # Configure AIGIE and all sub-package loggers
        aigie_modules = [
            "aigie",
            "aigie.auto_instrument",
            "aigie.integrations",
            "aigie.client",
            "claude_agent_sdk",
            "langchain",
            "langchain_core",
        ]

        for module_name in aigie_modules:
            module_logger = logging.getLogger(module_name)
            module_logger.setLevel(level)

        # Note: We intentionally do NOT set the root logger level here.
        # Enterprise apps need their own debug/info logging alongside Aigie.

    @property
    def aigie_url(self) -> str:
        """Get the Aigie API URL."""
        return self._aigie_url

    async def initialize(self) -> None:
        """Initialize the HTTP client, event buffer, and interception components.

        This method also:
        - Sets this instance as the global Aigie instance (for get_aigie())
        - Enables auto-instrumentation for LangChain, LangGraph, and LLM clients

        Initialization is split into phases:
        - Phase 1: Core setup (must happen first, fast)
        - Phase 2: Optional subsystems in parallel (all non-fatal)
        - Phase 3: Wiring + pattern cache
        - Phase 4: Auto-instrumentation (sync, idempotent)
        """
        if not self._initialized:
            # ── Phase 1: Core setup (fast, <200ms) ──────────────────────
            # Set this instance as the global instance so get_aigie() returns it
            global _global_aigie
            with _global_lock:
                if _global_aigie is None:
                    _global_aigie = self

            headers = {"Content-Type": "application/json"}
            if self._auth_token:
                headers["X-API-Key"] = self._auth_token
            # Include SDK version in headers so the platform can detect it
            try:
                from aigie import __version__ as _ver

                headers["X-SDK-Version"] = str(_ver)
            except Exception:
                pass
            self.client = httpx.AsyncClient(
                timeout=httpx.Timeout(
                    connect=_CONNECT_TIMEOUT,
                    read=_TIMEOUT,
                    write=_TIMEOUT,
                    pool=_CONNECT_TIMEOUT,
                ),
                limits=httpx.Limits(max_connections=_MAX_CONNECTIONS),
                headers=headers,
            )

            if self.config.internal_telemetry.enabled:
                from aigie import telemetry as _internal_telemetry

                _internal_telemetry.initialize(self.config.internal_telemetry)

            # When kytte_grpc_url is configured, finalized spans (SPAN_UPDATE)
            # are routed to IngestService.IngestSpans instead of HTTP.
            self._ingest_client = None
            if self.config.kytte_grpc_url:
                from aigie.ingest import IngestClient as _IngestClient

                self._ingest_client = _IngestClient(
                    self.config.kytte_grpc_url,
                    api_key=self._auth_token,
                    use_tls=self.config.kytte_grpc_use_tls,
                )
                logger.info(
                    "[AIGIE] gRPC ingest enabled: target=%s tls=%s",
                    self._ingest_client.target,
                    self.config.kytte_grpc_use_tls,
                )

            self._decision_client = None
            self._decision_tasks: set = set()
            self._tool_catalog_hashes: set[str] = set()
            self._tool_catalog_by_hash: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
            # trace_id -> tool_registry_hash for the run; ToolHashStamper folds
            # it onto every span of the trace (bounded to cap process memory).
            self._tool_hash_by_trace: OrderedDict[str, str] = OrderedDict()

            if self.config.kytte_decision_grpc_url:
                from aigie.decision import DecisionClient as _DecisionClient
                from aigie.decision.executor import StepExecutor

                self._decision_client = _DecisionClient(
                    self.config.kytte_decision_grpc_url,
                    api_key=self._auth_token,
                    use_tls=self.config.kytte_grpc_use_tls,
                    step_executor=StepExecutor(),
                    rewind_coordinator=self._rewind_coordinator,
                )
                logger.info(
                    "[AIGIE] gRPC determine enabled: target=%s tls=%s",
                    self._decision_client.target,
                    self.config.kytte_grpc_use_tls,
                )
                # Advertise executable verbs without blocking startup.
                self._track_decision_task(self._decision_client.register_capabilities())

            # Initialize event buffer (always on)
            self._buffer = EventBuffer(
                max_size=_BATCH_SIZE,
                flush_interval=_FLUSH_INTERVAL,
                max_retries=_MAX_RETRIES,
                retry_delay=_RETRY_DELAY,
                enable_circuit_breaker=True,
                circuit_breaker_threshold=_CIRCUIT_BREAKER_THRESHOLD,
                circuit_breaker_timeout=_CIRCUIT_BREAKER_TIMEOUT,
            )
            self._buffer.set_flusher(self._flush_events)
            await self._buffer.start_background_flusher()

            # Validate configuration for self-hosted deployments
            self.config.validate_and_warn()

            # Set _initialized EARLY so traces can flow immediately
            self._initialized = True

            # ── Phase 2: Optional subsystems in parallel (all non-fatal) ─
            async def _safe_init(name: str, coro, timeout: float) -> tuple[str, bool, str | None]:
                """Run a subsystem init with timeout. Never raises."""
                try:
                    await asyncio.wait_for(coro, timeout=timeout)
                    return (name, True, None)
                except asyncio.TimeoutError:
                    reason = f"timed out after {timeout}s"
                    logger.warning(f"[AIGIE] {name} init {reason} (non-fatal)")
                    return (name, False, reason)
                except Exception as e:
                    reason = str(e)
                    logger.warning(f"[AIGIE] {name} init failed (non-fatal): {reason}")
                    return (name, False, reason)

            parallel_tasks = []

            # Platform connectivity check
            if self._aigie_url:
                parallel_tasks.append(_safe_init("platform", self._check_platform_health(), 5.0))

            if parallel_tasks:
                results = await asyncio.gather(*parallel_tasks)
            else:
                results = []

            # ── Init summary ─────────────────────────────────────────────
            failed = [(name, reason) for name, ok, reason in results if not ok]
            if not failed:
                self._init_status = "ok"
                self._init_errors = []
                logger.info("[AIGIE] Init OK — all subsystems operational")
            else:
                self._init_status = "partial"
                self._init_errors = [f"{name}: {reason}" for name, reason in failed]
                failed_summary = ", ".join(name for name, _ in failed)
                logger.warning(f"[AIGIE] Init partial — failed: {failed_summary}")

            # ── Phase 3: Wiring ─────────────────────────────────────────
            self._wire_components()

            # ── Phase 4: Auto-instrumentation (always on, sync, idempotent)
            try:
                from aigie.integrations.install import install_framework_adapters

                install_framework_adapters(aigie=self)
            except Exception as e:
                logger.debug("Framework adapter install failed (non-fatal): %s", e)
            _enable_auto_instrumentation()
            logger.info("Auto-instrumentation enabled - LLM calls will be automatically traced")

            # ── Phase 5: Startup diagnostics banner ────────────────────────
            try:
                from aigie.diagnostics import format_startup_banner

                diag = self._collect_diagnostics()
                banner = format_startup_banner(diag)
                logger.info(f"\n{banner}")
            except Exception:
                pass  # Never let diagnostics break init

    def _collect_diagnostics(self) -> dict:
        """Collect current subsystem states for the startup banner."""
        import os

        # Version
        try:
            from aigie import __version__ as ver

            version = str(ver) if ver else "unknown"
        except Exception:
            version = "unknown"

        # Auth status
        if not self._auth_token:
            auth = ("error", "no token [AIGIE-C002]")
        elif not self._aigie_url:
            auth = ("error", "no platform URL configured [AIGIE-C001]")
        elif any(err.startswith("platform:") for err in self._init_errors):
            auth = ("error", "token set, platform unreachable")
        else:
            auth = ("ok", "connected")

        # Interception
        if self._interceptor_chain is not None:
            rule_count = len(self._rules_engine.list_rules()) if self._rules_engine else 0
            interception = ("ok", f"enabled (local-only, {rule_count} rules)")
        else:
            interception = ("skip", "disabled")

        # Auto-instrument
        frameworks = []
        if _instrumentation_enabled:
            for name in ["langchain", "langgraph", "openai", "anthropic"]:
                try:
                    __import__(name)
                    frameworks.append(name)
                except ImportError:
                    pass
        auto_inst = (
            ("ok", ", ".join(frameworks) if frameworks else "enabled")
            if _instrumentation_enabled
            else ("skip", "disabled")
        )

        # Compression
        try:
            import zstandard

            compression = ("ok", "zstd")
        except ImportError:
            compression = ("error", "zstandard not installed [AIGIE-I001]")

        return {
            "version": version,
            "mode": os.getenv("AIGIE_MODE", "observe"),
            "platform_url": self._aigie_url or "not configured",
            "auth": auth,
            "gateway": ("skip", "disabled"),
            "interception": interception,
            "judge": ("skip", "not initialized"),
            "auto_instrument": auto_inst,
            "compression": compression,
        }

    def _handle_auth_failure(self) -> None:
        """Handle a 401 auth failure with exponential backoff.

        Instead of permanently killing the SDK (old behaviour), suspends
        network I/O for an increasing backoff window:
          retries 1-5: 2s, 4s, 8s, 16s, 32s
          after max retries: one attempt every 5 minutes

        This allows recovery after token rotation or transient backend issues
        without requiring a pod restart.
        """
        self._auth_retry_count += 1
        if self._auth_retry_count <= self._auth_max_retries:
            backoff = self._auth_backoff_base * (2 ** (self._auth_retry_count - 1))
        else:
            backoff = self._auth_periodic_retry_interval

        self._auth_suspended = True
        self._auth_next_retry_at = time.monotonic() + backoff
        logger.warning(
            "[AIGIE] Auth failed (401) — suspending network I/O for %.0fs "
            "(retry %d). Fix: check your KYTTE_TOKEN.",
            backoff,
            self._auth_retry_count,
        )

    def _is_auth_suspended(self) -> bool:
        """Check if auth is currently suspended (backing off after 401).

        Returns False once the backoff window expires, allowing one retry.
        """
        if not self._auth_suspended:
            return False
        if time.monotonic() >= self._auth_next_retry_at:
            self._auth_suspended = False  # Allow one retry attempt
            return False
        return True

    def _handle_auth_success(self) -> None:
        """Reset auth retry state after a successful request."""
        if self._auth_retry_count > 0:
            logger.info("[AIGIE] Auth recovered after %d retries.", self._auth_retry_count)
            self._auth_retry_count = 0
            self._auth_suspended = False
            self._auth_next_retry_at = 0.0

    async def _check_platform_health(self) -> None:
        """Quick connectivity check against the platform health endpoint.

        Runs as a _safe_init task — non-blocking, non-fatal.
        Logs a clear message so the customer knows immediately if the
        platform URL is reachable and the API key is accepted.
        """
        if not self.client:
            raise RuntimeError("httpx client not initialized")

        # Try /health (no auth required)
        health_url = f"{self._aigie_url}/health"
        response = await self.client.get(health_url, timeout=3.0)
        response.raise_for_status()

        health = response.json()
        version = health.get("version", "unknown")
        logger.info(f"[AIGIE] Platform reachable — {self._aigie_url} (v{version})")

    def _wire_components(self) -> None:
        """Wire SDK components together using their existing setter APIs."""
        # InterceptorChain ← Aigie client reference
        if self._interceptor_chain is not None:
            self._interceptor_chain.set_aigie_client(self)

        logger.debug("Component wiring complete")

    def trace(
        self,
        name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        environment: str | None = None,
        release: str | None = None,
        version: str | None = None,
        release_version: str | None = None,  # Backward compatibility
        input: Any | None = None,
        output: Any | None = None,
        trace_id: str | None = None,
        # Agent plan tracking for drift detection
        system_prompt: str | None = None,
        agent_plan: str | list[str] | None = None,
        expected_steps: list[str] | None = None,
    ) -> TraceContext | Any:
        """
        Create a new trace context manager or decorator.

        Usage as context manager:
            async with aigie.trace("My Workflow") as trace:
                # Your code here
                pass

        Usage with custom trace ID (e.g. your request/action ID):
            async with aigie.trace(name=request_id, trace_id=action_id, input={"event": data}) as trace:
                await graph.ainvoke(...)

        Usage as decorator (with parentheses):
            @aigie.trace(name="my_function", metadata={"key": "value"})
            async def my_function():
                pass

        Usage as decorator (without parentheses):
            @aigie.trace
            async def my_function():
                pass

        Args:
            name: Trace name (required for context manager, optional for decorator)
            metadata: Optional metadata dictionary
            tags: Optional list of tags
            user_id: Optional user identifier for session tracking
            session_id: Optional session identifier for multi-turn conversations
            environment: Optional environment name (e.g., "production", "staging", "development")
            release_version: Optional application version/release identifier
            system_prompt: Optional system prompt/instructions given to the agent (for drift detection)
            agent_plan: Optional agent plan - either a string description or list of planned steps
            expected_steps: Optional list of expected step names the agent should execute

        Returns:
            TraceContext manager or decorator
        """
        if not self._initialized:
            raise RuntimeError("Aigie not initialized. Call await aigie.initialize() first.")

        from aigie.decorators_v3 import traceable as _traceable_v3

        # Merge session/user tracking into metadata
        enriched_metadata = dict(metadata or {})
        if user_id:
            enriched_metadata["user_id"] = user_id
        if session_id:
            enriched_metadata["session_id"] = session_id
        if environment:
            enriched_metadata["environment"] = environment
        if release:
            enriched_metadata["release"] = release
        if release_version:  # Backward compatibility
            enriched_metadata["release"] = release_version
            enriched_metadata["release_version"] = release_version
        if version:
            enriched_metadata["version"] = version
        if input is not None:
            enriched_metadata["input"] = input
        if output is not None:
            enriched_metadata["output"] = output

        # Agent plan tracking for drift detection
        if system_prompt:
            enriched_metadata["kytte.system_prompt"] = system_prompt
        if agent_plan:
            enriched_metadata["kytte.agent_plan"] = agent_plan
        if expected_steps:
            enriched_metadata["kytte.expected_steps"] = expected_steps

        # If name is provided and it's a string, use as context manager
        if name is not None and isinstance(name, str):
            ctx = TraceContext(
                buffer=self._buffer,
                name=name,
                metadata=enriched_metadata,
                tags=tags or [],
                sample_rate=_SAMPLING_RATE,
            )
            # Allow customers to pass their own trace ID (e.g. request_id, action_id)
            if trace_id:
                ctx.id = str(trace_id)
            return ctx

        # Otherwise, return a decorator
        return _traceable_v3(name=name if isinstance(name, str) else None)

    def get_current_trace(self) -> "TraceContext | None":
        """Get the active trace from the current context.

        Use this to enrich auto-instrumented traces with your own identifiers::

            trace = aigie.get_current_trace()
            if trace:
                trace.update(metadata={"request_id": req_id})
        """
        from aigie.trace import get_current_trace

        return get_current_trace()

    def update_current_trace(
        self,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        name: str | None = None,
        input: Any | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
    ) -> bool:
        """Enrich the current auto-instrumented trace with custom data.

        Example::

            aigie.update_current_trace(
                name=request_id,
                metadata={"action_id": action_id, "customer_id": cid},
            )
            await graph.ainvoke(...)
        """
        from aigie.trace import update_current_trace

        return update_current_trace(
            metadata=metadata,
            tags=tags,
            name=name,
            input=input,
            user_id=user_id,
            session_id=session_id,
        )

    @property
    def prompts(self):
        """
        Get prompt manager.

        Usage:
            prompt = await aigie.prompts.create(
                name="customer_support",
                template="You are a helpful assistant. Customer: {customer_name}"
            )
        """
        from aigie.prompts import PromptRegistry

        if not hasattr(self, "_prompt_manager"):
            self._prompt_manager = PromptRegistry()
        return self._prompt_manager

    @property
    def signals(self):
        """Get the Signal Reporter for sending signals to backend."""
        return self._signal_reporter

    @property
    def health(self):
        """Get the Health Monitor for backend health status."""
        return self._health_monitor

    def extract_trace_context(self, headers: dict[str, str]) -> Any | None:
        """
        Extract W3C trace context from HTTP headers.

        Usage:
            context = aigie.extract_trace_context(request.headers)
            if context:
                async with aigie.trace("workflow") as trace:
                    trace.set_trace_context(context)

        Args:
            headers: HTTP headers dictionary

        Returns:
            TraceContext if found, None otherwise
        """
        from aigie.context import extract_trace_context

        return extract_trace_context(headers)

    def create_trace_context(self, parent_context: Any | None = None) -> Any:
        """
        Create a new W3C trace context.

        Usage:
            context = aigie.create_trace_context()
            headers = context.to_headers()
            # Add headers to HTTP request

        Args:
            parent_context: Optional parent context (creates child context)

        Returns:
            TraceContext object
        """
        from aigie.context import TraceContext

        if parent_context:
            return parent_context.create_child()
        return TraceContext()

    async def intercept_before_tool(
        self,
        tool_name: str,
        tool_args: dict[str, Any],
        *,
        trace_id: str | None = None,
        span_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Run pre-execution interception for a tool call.

        Called by framework handlers (Strands, LangGraph, etc.) BEFORE a tool
        executes. Routes through the InterceptorChain with tiered early-exit:
        - Tier 1: Local rules engine (<5ms, runs always, pure CPU)
        - Tier 2: Gateway WebSocket validation (<100ms, only if connected)
        - Tier 3: Backend consultation (only on CONSULT decisions — rare)
        Most calls exit at Tier 1. Hard cap: 200ms total.

        Fail-open design: if anything fails (WebSocket down, timeout, error),
        returns ALLOW so the agent is never blocked by Aigie issues.

        Args:
            tool_name: Name of the tool being called
            tool_args: Tool call arguments
            trace_id: Optional trace ID
            span_id: Optional span ID

        Returns:
            Dict with: decision ("allow"/"block"/"modify"/"delay"),
            reason, modified_args (if modify), delay_ms (if delay)
        """
        allow_result = {
            "decision": "allow",
            "reason": None,
            "modified_args": None,
            "delay_ms": None,
        }

        if not self._initialized or not self._interceptor_chain:
            return allow_result

        try:
            from aigie.interceptor.protocols import InterceptionContext, InterceptionDecision

            ctx = InterceptionContext(
                provider="tool",
                model=tool_name,
                messages=[{"role": "tool_call", "content": str(tool_args)[:500]}],
                request_kwargs=tool_args,
                trace_id=trace_id,
                span_id=span_id,
                metadata={"tool_name": tool_name},
            )

            result = await asyncio.wait_for(
                self._interceptor_chain.pre_call(ctx),
                timeout=0.2,  # 200ms hard cap — never block the agent
            )

            if result.decision == InterceptionDecision.BLOCK:
                return {
                    "decision": "block",
                    "reason": result.reason or "Blocked by interception chain",
                    "modified_args": None,
                    "delay_ms": None,
                }
            if result.decision == InterceptionDecision.MODIFY:
                return {
                    "decision": "modify",
                    "reason": result.reason,
                    "modified_args": result.modified_kwargs,
                    "delay_ms": None,
                }

            return allow_result

        except asyncio.TimeoutError:
            logger.debug("Pre-tool interception timed out (fail-open)")
            return allow_result
        except Exception as e:
            logger.debug(f"Pre-tool interception error (fail-open): {e}")
            return allow_result

    async def intercept_after_tool(
        self,
        tool_name: str,
        result: Any,
        *,
        error: str | None = None,
        error_type: str | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
        duration_ms: float = 0.0,
    ) -> dict[str, Any]:
        """
        Run post-execution interception for a tool call.

        Called by framework handlers AFTER a tool executes. Routes through
        the InterceptorChain post-call hooks and backend consultation for
        remediation when errors are detected.

        Fail-open: never blocks or crashes the agent.

        Args:
            tool_name: Name of the tool
            result: Tool result (or error message)
            error: Error message if tool failed
            error_type: Type of error
            trace_id: Optional trace ID
            span_id: Optional span ID
            duration_ms: Execution duration

        Returns:
            Dict with: decision, fixes (list of fix actions), modified_result
        """
        noop_result = {"decision": "allow", "fixes": [], "modified_result": None}

        if not self._initialized or not self._interceptor_chain:
            return noop_result

        try:
            from aigie.interceptor.protocols import InterceptionContext

            ctx = InterceptionContext(
                provider="tool",
                model=tool_name,
                trace_id=trace_id,
                span_id=span_id,
                response_content=str(result)[:1000] if result else None,
                response_time_ms=duration_ms,
                error=Exception(error) if error else None,
                error_type=error_type,
                metadata={"tool_name": tool_name},
            )

            post_result = await asyncio.wait_for(
                self._interceptor_chain.post_call(ctx),
                timeout=0.5,  # 500ms for post-call (can be slower, not blocking)
            )

            fixes = []
            for fix in post_result.fixes_applied or []:
                fixes.append(
                    {
                        "action_type": fix.action_type.value
                        if hasattr(fix.action_type, "value")
                        else str(fix.action_type),
                        "parameters": fix.parameters if hasattr(fix, "parameters") else {},
                        "confidence": fix.confidence if hasattr(fix, "confidence") else 0.0,
                        "reason": fix.reason if hasattr(fix, "reason") else None,
                    }
                )

            return {
                "decision": post_result.decision.value
                if hasattr(post_result.decision, "value")
                else "allow",
                "fixes": fixes,
                "modified_result": post_result.modified_content or post_result.modified_response,
            }

        except asyncio.TimeoutError:
            logger.debug("Post-tool interception timed out (fail-open)")
            return noop_result
        except Exception as e:
            logger.debug(f"Post-tool interception error (fail-open): {e}")
            return noop_result

    async def _dispatch_v2_spans(self, events: list[BufferedEvent]) -> None:
        """Send finalized spans to the gRPC Ingest Gateway.

        This is the only telemetry that leaves the SDK — every buffered event
        is a finalized span, and the platform mints trace rows server-side
        from root spans. The legacy HTTP write endpoints no longer exist.

        Raises on gRPC failure so the buffer's retry/offline machinery owns
        redelivery; there is no HTTP fallback.
        """
        if not events:
            return

        client = self._ingest_client
        if client is None:
            logger.warning(
                "[AIGIE] gRPC ingest not configured — dropping %d finalized spans "
                "(set KYTTE_URL so the gRPC target can be derived).",
                len(events),
            )
            return

        pairs = [(e, _span_to_proto(e.payload)) for e in events]
        spans_pb = [span_pb for _, span_pb in pairs]
        # First-attempt, not-yet-judged spans only: judge verdicts are not
        # idempotent, so neither a buffer-driven ingest retry (retry_count > 0)
        # nor a span already fired at emit time (evaluated) may be judged again.
        self._fire_evaluate_spans(
            [span_pb for e, span_pb in pairs if e.retry_count == 0 and not e.evaluated]
        )
        response = await client.send_spans(spans_pb)
        if response.rejected:
            logger.warning(
                "[AIGIE] gRPC ingest rejected %d of %d spans: %s",
                response.rejected,
                response.rejected + response.accepted,
                "; ".join(response.errors[:3]),
            )

    async def _drain_decision_tasks(self, timeout_s: float) -> None:
        """Bounded wait for in-flight EvaluateSpan tasks before closing the
        decision channel: a client-side cancel propagates to the server
        handler and kills verdict persistence mid-flight. Never raises."""
        tasks = getattr(self, "_decision_tasks", None)
        if not tasks:
            return
        try:
            await asyncio.wait(set(tasks), timeout=timeout_s)
        except Exception as e:
            logger.debug("decision task drain: %s", e)

    def _try_fire_evaluate_span(self, payload: dict[str, Any]) -> bool:
        """Fire EvaluateSpan for one finalized span at emit time (Determine
        Error MVP) instead of waiting for the next buffer flush.

        Called by ``TraceEmitter`` on every span-completion emission —
        including from framework worker threads — so this never raises and
        never blocks. The task must run on the buffer's owner loop: the
        decision channel (``grpc.aio``) is bound to the loop it was created
        on, which is where the dispatch-time fires already run.

        Returns True only when the call was actually scheduled. False means
        the dispatch-time fire in ``_dispatch_v2_spans`` still owns this
        span (no decision client, proto conversion error, no usable loop).
        """
        try:
            if payload.get("status") in JUDGE_SKIP_STATUSES:
                return False
            if getattr(self, "_decision_client", None) is None:
                return False
            buffer = getattr(self, "_buffer", None)
            owner = getattr(buffer, "_owner_loop", None)
            if owner is None or owner.is_closed():
                return False
            try:
                current = asyncio.get_running_loop()
            except RuntimeError:
                current = None
            if current is not owner and not owner.is_running():
                return False
            span_pb = _span_to_proto(payload)
            if current is owner:
                self._fire_evaluate_spans([span_pb])
            else:
                owner.call_soon_threadsafe(self._fire_evaluate_spans, [span_pb])
            return True
        except Exception as e:
            logger.debug("[AIGIE] emit-time EvaluateSpan skipped (%s); deferring to flush", e)
            return False

    def _fire_evaluate_spans(self, spans_pb: list) -> None:
        """Fire one fire-and-forget EvaluateSpan task per finalized span
        (Determine Error MVP). ``DecisionClient.evaluate_span`` never raises,
        so these tasks can't surface errors into the ingest path; the bounded
        set just keeps strong references until each task completes."""
        decision_client = getattr(self, "_decision_client", None)
        if decision_client is None:
            return
        for span_pb in spans_pb:
            # Authoritative judge gate (covers both the emit-time and
            # dispatch-time fire paths): never judge a paused/interrupted span.
            if span_pb.status in JUDGE_SKIP_STATUSES:
                continue
            self._track_decision_task(decision_client.evaluate_span(span_pb))

    def register_tool_catalog(self, tools: Iterable[Any]) -> str | None:
        """Register tools once by content hash and return that hash for span metadata."""
        from aigie.decision.tool_catalog import catalog_hash, normalize_tools

        if getattr(self, "_decision_client", None) is None:
            return None
        catalog = normalize_tools(tools)
        if not catalog:
            return None
        digest = catalog_hash(catalog)
        self._retain_tool_catalog(digest, catalog)
        if digest not in self._tool_catalog_hashes:
            self._schedule_tool_catalog_registration(digest, catalog)
        return digest

    def _retain_tool_catalog(self, digest: str, catalog: list[dict[str, Any]]) -> None:
        _lru_put(self._tool_catalog_by_hash, digest, catalog, _TOOL_CATALOG_CAP)

    def tool_catalog_for_hash(self, tool_registry_hash: str | None) -> list[dict[str, Any]] | None:
        """Return the normalized catalog registered under ``tool_registry_hash``."""
        if not tool_registry_hash:
            return None
        return self._tool_catalog_by_hash.get(tool_registry_hash)

    def bind_trace_tool_hash(self, trace_id: str, tool_hash: str) -> None:
        """Bind a run's ``tool_registry_hash`` to its trace so ``ToolHashStamper``
        stamps every span of the trace. Bounded to cap process memory."""
        _lru_put(self._tool_hash_by_trace, trace_id, tool_hash, _TOOL_HASH_TRACE_CAP)

    def tool_hash_for_trace(self, trace_id: str | None) -> str | None:
        """Return the ``tool_registry_hash`` bound to ``trace_id``, if any."""
        if not trace_id:
            return None
        return self._tool_hash_by_trace.get(trace_id)

    def _schedule_tool_catalog_registration(
        self, digest: str, catalog: list[dict[str, Any]]
    ) -> None:
        """Schedule RegisterToolCatalog on the buffer's owner loop."""
        owner = getattr(getattr(self, "_buffer", None), "_owner_loop", None)
        if owner is None or owner.is_closed():
            return
        try:
            current = asyncio.get_running_loop()
        except RuntimeError:
            current = None
        if current is owner:
            self._track_decision_task(self._register_and_mark_catalog(digest, catalog))
        elif owner.is_running():
            # Ignore shutdown races with the owner loop.
            try:
                owner.call_soon_threadsafe(
                    lambda: self._track_decision_task(
                        self._register_and_mark_catalog(digest, catalog)
                    )
                )
            except RuntimeError:
                logger.debug("owner loop closed before tool-catalog registration scheduled")

    async def _register_and_mark_catalog(self, digest: str, catalog: list[dict[str, Any]]) -> None:
        """Register catalog, then mark its hash for dedupe."""
        accepted = await self._decision_client.register_tool_catalog(digest, catalog)
        if accepted is not None:
            self._tool_catalog_hashes.add(digest)

    def _track_decision_task(self, coro: Coroutine[Any, Any, Any]) -> None:
        """Schedule a fire-and-forget decision-path task, holding a strong
        reference in ``_decision_tasks`` until it completes so it isn't GC'd
        mid-flight; drained on shutdown by ``_drain_decision_tasks``."""
        tasks = getattr(self, "_decision_tasks", None)
        if tasks is None:
            tasks = self._decision_tasks = set()
        task = asyncio.create_task(coro)
        tasks.add(task)
        task.add_done_callback(tasks.discard)

    async def _flush_events(self, events: list[BufferedEvent]) -> None:
        """
        Flush buffered events: finalized spans go to the gRPC Ingest
        Gateway; everything else is dropped (no V2 transport yet — the legacy
        HTTP write endpoints were removed from the platform).

        SECURITY: Requires valid authentication token. Without a token,
        data will NOT be sent to the platform to prevent unauthorized injection.
        """
        if not events:
            return

        # Auth suspended — waiting for backoff window
        if self._is_auth_suspended():
            return

        # SECURITY CHECK: Block data sending without valid token
        # This prevents unauthorized data injection to the platform
        if not self._auth_token:
            logger.warning(
                "[AIGIE] Dropping %d events — no authentication token. "
                "Set KYTTE_TOKEN environment variable or pass kytte_token to init().",
                len(events),
            )
            return

        await self._dispatch_v2_spans(events)

    async def flush(self) -> None:
        """Manually flush all buffered events."""
        if self._buffer:
            await self._buffer.flush()

    def sdk_status(self) -> dict[str, Any]:
        """Return SDK connectivity status for external monitoring.

        Can be used in health endpoints, k8s liveness probes, or dashboards.

        Returns:
            Dict with keys: initialized, init_status, auth_ok, auth_suspended,
            auth_retry_count, buffer_pending, kytte_url.
        """
        return {
            "initialized": self._initialized,
            "init_status": self._init_status,
            "auth_ok": bool(self._auth_token) and not self._auth_suspended,
            "auth_suspended": self._auth_suspended,
            "auth_retry_count": self._auth_retry_count,
            "buffer_pending": self._buffer.size() if self._buffer else 0,
            "kytte_url": self._aigie_url or "",
        }

    async def doctor(self) -> "DoctorResult":
        """Run a health check on SDK configuration and connectivity.

        Prints results to stdout and returns a DoctorResult.

        Usage:
            aigie = Aigie()
            await aigie.initialize()
            result = await aigie.doctor()
        """
        import platform
        import time

        from aigie.diagnostics import DoctorResult, format_doctor_output

        checks = []
        warnings = []
        errors = []

        # SDK version
        try:
            from aigie import __version__ as ver

            checks.append(("SDK version", "ok", str(ver)))
        except Exception:
            checks.append(("SDK version", "ok", "unknown"))

        # Python version
        checks.append(("Python version", "ok", platform.python_version()))

        # Platform URL
        if self._aigie_url:
            checks.append(("Platform URL", "ok", self._aigie_url))
        else:
            checks.append(("Platform URL", "error", "not configured [AIGIE-C001]"))
            errors.append("AIGIE-C001")

        # Authentication
        if self._auth_token:
            checks.append(("Authentication", "ok", "token set"))
        else:
            checks.append(("Authentication", "error", "no token [AIGIE-C002]"))
            errors.append("AIGIE-C002")

        # Ingestion API ping
        if self._aigie_url and self.client:
            try:
                start = time.perf_counter()
                response = await self.client.get(f"{self._aigie_url}/health")
                latency_ms = (time.perf_counter() - start) * 1000
                if response.status_code < 500:
                    checks.append(
                        ("Ingestion API", "ok", f"reachable (latency: {latency_ms:.0f}ms)")
                    )
                else:
                    checks.append(
                        ("Ingestion API", "error", f"server error {response.status_code}")
                    )
                    errors.append("AIGIE-N002")
            except Exception as e:
                checks.append(("Ingestion API", "error", f"unreachable: {e} [AIGIE-N002]"))
                errors.append("AIGIE-N002")
        else:
            checks.append(("Ingestion API", "skip", "skipped (no URL configured)"))

        # Compression
        try:
            import zstandard

            checks.append(("Compression", "ok", "zstd"))
        except ImportError:
            checks.append(("Compression", "warn", "zstandard not installed [AIGIE-I001]"))
            warnings.append("AIGIE-I001")

        healthy = len(errors) == 0
        result = DoctorResult(healthy=healthy, checks=checks, warnings=warnings, errors=errors)

        # Print to stdout (always visible, not gated by log level)
        print(format_doctor_output(result))

        return result

    async def _stop_component(self, name: str, coro, timeout: float = 2.0) -> None:
        """Await a component's stop coroutine with a timeout.

        Logs a warning on hang or unexpected exception so a stuck component
        cannot pin shutdown indefinitely (atexit hooks have a hard wallclock
        budget; better to leak a task than to delay process exit).
        """
        try:
            await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            logger.warning(f"[AIGIE] {name} did not stop within {timeout}s — abandoning")
        except Exception as e:
            logger.warning(f"[AIGIE] {name} stop raised: {e}")

    def _finalize_open_spans_at_shutdown(self) -> None:
        """Emit any spans still open at shutdown as interrupted.

        A span built mutably in memory registers a finalize callable in the
        global open-span registry; on clean close the emitter deregisters it.
        Survivors here are orphans (unclean exit) — emit each finalized with
        ``status="interrupted"`` so the root still ships instead of being
        abandoned in a handler's ``_open`` map. ``evaluated=True`` keeps the
        judge from firing on an incomplete span.
        """
        if self._buffer is None:
            return
        for payload in drain_open_spans_as_interrupted():
            self._buffer.add_sync(payload, evaluated=True)

    async def close(self) -> None:
        """Close the HTTP client and flush remaining events."""
        self._closing = True

        from aigie import telemetry as _internal_telemetry

        await _internal_telemetry.shutdown(timeout_ms=5_000)

        # Tear down event-emitting components FIRST. Several of these can
        # enqueue events into `self._buffer` from their shutdown paths (or
        # from in-flight tasks they cancel during shutdown). Nulling the
        # buffer before they're stopped would NPE those final emits.

        if self._signal_reporter:
            try:
                await self._signal_reporter.close()
            except Exception as e:
                logger.debug(f"Signal reporter close: {e}")
            self._signal_reporter = None

        if self._health_monitor:
            try:
                await self._health_monitor.close()
            except Exception as e:
                logger.debug(f"Health monitor close: {e}")
            self._health_monitor = None

        # Finalize any spans still open at shutdown before draining the buffer.
        self._finalize_open_spans_at_shutdown()

        # Now drain the buffer. Background flusher's final flush picks up any
        # events the components above queued during their teardown.
        if self._buffer:
            await self._buffer.stop_background_flusher()
            self._buffer = None

        # gRPC clients close AFTER the buffer drain — the final flush sends
        # the run's last finalized spans through them.
        if self._ingest_client is not None:
            try:
                await self._ingest_client.close()
            except grpc.RpcError as e:
                logger.debug("ingest client close: %s", e)
            self._ingest_client = None

        if getattr(self, "_decision_client", None) is not None:
            await self._drain_decision_tasks(
                timeout_s=float(os.getenv("KYTTE_DECISION_DRAIN_TIMEOUT_S", "30"))
            )
            try:
                await self._decision_client.close()
            except grpc.RpcError as e:
                logger.debug("decision client close: %s", e)
            self._decision_client = None

        # Close judge LLM client (httpx connection pool)
        if self._judge_llm_client and hasattr(self._judge_llm_client, "close"):
            try:
                await self._judge_llm_client.close()
            except Exception as e:
                logger.debug(f"Judge LLM client close: {e}")
            self._judge_llm_client = None

        if self.client:
            await self.client.aclose()
            self.client = None
            self._initialized = False

        # CRITICAL FIX: Complete cleanup for millions-of-runs production scale
        # Accumulated _global_aigie references and patching state corrupts the class after ~30 instances
        global _global_aigie
        with _global_lock:
            if _global_aigie is self:
                _global_aigie = None

        # Clear all component references to prevent reference cycles
        self._interceptor_chain = None
        self._rules_engine = None
        self._drift_monitor = None
        self._callbacks = []

        logger.debug("Aigie instance fully cleaned up")

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    # ==================== Real-time Interception API ====================

    @property
    def interceptor(self) -> Optional["InterceptorChain"]:
        """Get the interceptor chain for direct access."""
        return self._interceptor_chain

    @property
    def rules_engine(self) -> Optional["LocalRulesEngine"]:
        """Get the rules engine for direct access."""
        return self._rules_engine

    @property
    def drift_monitor(self) -> Optional["DriftMonitor"]:
        """Get the drift monitor for direct access."""
        return self._drift_monitor

    def add_pre_call_hook(
        self,
        hook: Optional["PreCallHook"] = None,
        priority: int = 50,
        name: str | None = None,
    ) -> Callable:
        """
        Add a pre-call hook for real-time interception.

        Can be used as a decorator or called directly:

            # As decorator
            @aigie.add_pre_call_hook(priority=10)
            async def my_hook(ctx: InterceptionContext) -> PreCallResult:
                if "unsafe" in str(ctx.messages):
                    return PreCallResult.block(reason="Unsafe content")
                return PreCallResult.allow()

            # Direct call
            aigie.add_pre_call_hook(my_hook_function, priority=10)

        Args:
            hook: Hook function (if using as direct call)
            priority: Hook priority (lower = runs first)
            name: Optional name for the hook

        Returns:
            Decorator if hook is None, otherwise None
        """
        if self._interceptor_chain is None:
            raise RuntimeError("Interception chain not initialized.")

        def decorator(fn: "PreCallHook") -> "PreCallHook":
            self._interceptor_chain.add_pre_hook(fn, priority=priority, name=name)
            return fn

        if hook is not None:
            self._interceptor_chain.add_pre_hook(hook, priority=priority, name=name)
            return hook

        return decorator

    def add_post_call_hook(
        self,
        hook: Optional["PostCallHook"] = None,
        priority: int = 50,
        name: str | None = None,
    ) -> Callable:
        """
        Add a post-call hook for real-time interception.

        Can be used as a decorator or called directly:

            # As decorator
            @aigie.add_post_call_hook(priority=10)
            async def my_hook(ctx: InterceptionContext) -> PostCallResult:
                if ctx.drift_score and ctx.drift_score > 0.8:
                    return PostCallResult.retry(reason="High drift detected")
                return PostCallResult.allow()

            # Direct call
            aigie.add_post_call_hook(my_hook_function, priority=10)

        Args:
            hook: Hook function (if using as direct call)
            priority: Hook priority (lower = runs first)
            name: Optional name for the hook

        Returns:
            Decorator if hook is None, otherwise None
        """
        if self._interceptor_chain is None:
            raise RuntimeError("Interception chain not initialized.")

        def decorator(fn: "PostCallHook") -> "PostCallHook":
            self._interceptor_chain.add_post_hook(fn, priority=priority, name=name)
            return fn

        if hook is not None:
            self._interceptor_chain.add_post_hook(hook, priority=priority, name=name)
            return hook

        return decorator

    def add_rule(
        self,
        rule: "Rule",
        priority: int | None = None,
        name: str | None = None,
    ) -> None:
        """
        Add a custom rule to the local rules engine.

        Args:
            rule: Rule object implementing the Rule protocol
            priority: Override priority (default: use rule.priority)
            name: Override name (default: use rule.name)

        Example:
            from aigie.rules import CostLimitRule

            aigie.add_rule(CostLimitRule(max_cost=0.50, limit_type="request"))
        """
        if self._rules_engine is None:
            raise RuntimeError("Interception chain not initialized.")

        self._rules_engine.add_rule(rule, priority=priority, name=name)

    async def intercept_pre_call(
        self,
        provider: str,
        model: str,
        messages: list[dict[str, Any]],
        trace_id: str | None = None,
        span_id: str | None = None,
        estimated_cost: float = 0.0,
        user_id: str | None = None,
        session_id: str | None = None,
        **kwargs,
    ) -> "InterceptionContext":
        """
        Run pre-call interception on an LLM call.

        This is called automatically by wrap_openai and other wrappers.
        Can also be called directly for custom integrations.

        Args:
            provider: LLM provider name (e.g., "openai", "anthropic")
            model: Model name
            messages: Chat messages
            trace_id: Optional trace ID for correlation
            span_id: Optional span ID for correlation
            estimated_cost: Estimated cost for this call
            user_id: Optional user identifier
            session_id: Optional session identifier
            **kwargs: Additional request parameters

        Returns:
            InterceptionContext with decision

        Raises:
            InterceptionBlockedError: If the request is blocked
        """
        if self._interceptor_chain is None:
            # Interception not enabled, create pass-through context
            from aigie.interceptor.protocols import InterceptionContext, InterceptionDecision

            ctx = InterceptionContext(
                provider=provider,
                model=model,
                messages=messages,
                trace_id=trace_id,
                span_id=span_id,
                estimated_cost=estimated_cost,
                user_id=user_id,
                session_id=session_id,
                request_kwargs=kwargs,
            )
            ctx.decision = InterceptionDecision.ALLOW
            return ctx

        from aigie.interceptor.protocols import InterceptionContext

        # Create interception context
        ctx = InterceptionContext(
            provider=provider,
            model=model,
            messages=messages,
            trace_id=trace_id,
            span_id=span_id,
            estimated_cost=estimated_cost,
            user_id=user_id,
            session_id=session_id,
            request_kwargs=kwargs,
        )

        # Run pre-call hooks
        result = await self._interceptor_chain.pre_call(ctx)

        # Update context with decision
        ctx.decision = result.decision
        ctx.modified_messages = result.modified_messages
        ctx.modified_kwargs = result.modified_kwargs

        return ctx

    def _sync_post_call(
        self,
        ctx: "InterceptionContext",
        response: Any,
        error: Exception | None = None,
    ) -> "InterceptionContext":
        """Synchronous bridge to :meth:`intercept_post_call`.

        Used by call_sync_with_autonomous (sync LLM wrappers) so a single
        helper covers both async and sync call sites. If a loop is already
        running on this thread, we delegate to a fresh worker thread so we
        never call ``loop.run_until_complete`` on a live loop.
        """
        coro = self.intercept_post_call(ctx, response=response, error=error)
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            # No loop on this thread — safe to drive a fresh one.
            return asyncio.run(coro)

        # We are inside a running loop. Run the coroutine on a helper
        # thread with its own loop so we can block here without nesting.
        import threading

        result: dict[str, Any] = {}

        def _runner() -> None:
            try:
                result["value"] = asyncio.run(
                    self.intercept_post_call(ctx, response=response, error=error)
                )
            except BaseException as exc:  # noqa: BLE001
                result["error"] = exc

        t = threading.Thread(target=_runner, daemon=True, name="aigie-sync-post-call")
        t.start()
        t.join()
        if "error" in result:
            raise result["error"]
        return result["value"]

    async def intercept_post_call(
        self,
        ctx: "InterceptionContext",
        response: Any,
        error: Exception | None = None,
    ) -> "InterceptionContext":
        """
        Run post-call interception after an LLM call.

        This is called automatically by wrap_openai and other wrappers.
        Can also be called directly for custom integrations.

        Args:
            ctx: The interception context from pre-call
            response: The LLM response (or None if error)
            error: The exception if the call failed

        Returns:
            Updated InterceptionContext with post-call decision

        Raises:
            InterceptionRetryError: If the call should be retried
        """
        if self._interceptor_chain is None:
            # Interception not enabled, just update context
            ctx.response = response
            ctx.error = error
            return ctx

        # Update context with response/error
        ctx.response = response
        ctx.error = error
        if error:
            ctx.error_type = type(error).__name__

        # Extract response content if available
        if response and hasattr(response, "choices") and response.choices:
            choice = response.choices[0]
            if hasattr(choice, "message") and choice.message:
                ctx.response_content = getattr(choice.message, "content", None)

        # Run drift detection
        if self._drift_monitor:
            alerts = await self._drift_monitor.check_drift(ctx)
            if alerts:
                # Set drift score based on highest alert
                ctx.drift_score = max(a.score for a in alerts)
                # Report each drift alert to the platform
                if self._signal_reporter:
                    trace_id = getattr(ctx, "trace_id", "") or ""
                    for alert in alerts:
                        try:
                            await self._signal_reporter.report_drift(
                                trace_id=trace_id,
                                drift_type=alert.drift_type.value,
                                score=alert.score,
                                details={
                                    "reason": alert.reason,
                                    "level": alert.level.value,
                                },
                            )
                        except Exception as e:
                            logger.debug(f"Failed to report drift signal: {e}")

        # Run post-call hooks
        result = await self._interceptor_chain.post_call(ctx)

        # Update context with decision and fixes
        ctx.decision = result.decision
        ctx.fixes_applied = result.fixes_applied if hasattr(result, "fixes_applied") else []

        return ctx

    def get_interception_stats(self) -> dict[str, Any]:
        """
        Get statistics from all interception components.

        Returns:
            Dict with stats from interceptor, rules engine, drift monitor, etc.
        """
        stats = {}

        if self._interceptor_chain:
            stats["interceptor"] = self._interceptor_chain.get_stats()

        if self._rules_engine:
            stats["rules_engine"] = self._rules_engine.get_stats()

        if self._drift_monitor:
            metrics = self._drift_monitor.get_metrics()
            stats["drift_monitor"] = {
                "total_checks": metrics.total_checks,
                "alerts_generated": metrics.alerts_generated,
                "alerts_by_type": metrics.alerts_by_type,
                "avg_drift_score": metrics.avg_drift_score,
            }

        return stats

    # ========== Self-Hosted Health Checks ==========

    async def check_connection(self, timeout: float = 5.0) -> dict[str, Any]:
        """
        Verify connectivity to the Aigie backend.

        Use this to check if the backend is reachable and responding.
        Useful for self-hosted deployments to verify installation.

        Args:
            timeout: Request timeout in seconds

        Returns:
            Dict with connection status:
            - connected: bool - Whether connection succeeded
            - latency_ms: float - Round-trip latency in milliseconds
            - api_url: str - The API URL that was tested
            - error: str - Error message if connection failed
        """
        import time

        result = {
            "connected": False,
            "latency_ms": None,
            "api_url": self._aigie_url,
            "error": None,
            "server_version": None,
        }

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                start = time.monotonic()
                response = await client.get(
                    f"{self._aigie_url}/health",
                    headers={"X-API-Key": self._auth_token} if self._auth_token else {},
                )
                latency = (time.monotonic() - start) * 1000

                result["latency_ms"] = round(latency, 2)

                if response.status_code == 200:
                    result["connected"] = True
                    try:
                        health_data = response.json()
                        result["server_version"] = health_data.get("version")
                    except Exception:
                        pass
                else:
                    result["error"] = f"HTTP {response.status_code}: {response.text[:100]}"

        except httpx.ConnectError as e:
            result["error"] = f"Connection failed: {e}"
        except httpx.TimeoutException:
            result["error"] = f"Connection timed out after {timeout}s"
        except Exception as e:
            result["error"] = f"Unexpected error: {type(e).__name__}: {e}"

        return result

    async def get_installation_status(self) -> dict[str, Any]:
        """
        Get comprehensive status for self-hosted installations.

        Returns a complete health check including:
        - Backend connectivity
        - Configuration validation
        - Feature availability

        Returns:
            Dict with installation status
        """
        status = {
            "healthy": True,
            "components": {},
            "warnings": [],
            "errors": [],
        }

        # Check backend connection
        connection = await self.check_connection()
        status["components"]["backend"] = {
            "status": "healthy" if connection["connected"] else "unhealthy",
            "latency_ms": connection["latency_ms"],
            "api_url": connection["api_url"],
            "error": connection["error"],
        }
        if not connection["connected"]:
            status["healthy"] = False
            status["errors"].append(f"Backend unreachable: {connection['error']}")

        # Check configuration
        config_warnings = self.config.validate_self_hosted()
        if config_warnings:
            status["warnings"].extend(config_warnings)
            status["components"]["configuration"] = {
                "status": "warning",
                "warnings": config_warnings,
            }
        else:
            status["components"]["configuration"] = {"status": "healthy"}

        # Check buffer status
        if self._buffer:
            buffer_stats = {
                "status": "healthy",
                "pending_events": len(self._buffer._buffer)
                if hasattr(self._buffer, "_buffer")
                else 0,
            }
            status["components"]["buffer"] = buffer_stats
        else:
            status["components"]["buffer"] = {"status": "disabled"}

        # Check interception status
        if self._interceptor_chain:
            status["components"]["interception"] = {"status": "enabled"}
        else:
            status["components"]["interception"] = {"status": "disabled"}

        return status

    # ========== Callback Management ==========

    def add_callback(self, callback: Any) -> None:
        """
        Add a callback handler for receiving span/trace events.

        This follows the LiteLLM pattern of registering callbacks that
        receive events during tracing.

        Args:
            callback: A callback instance (must implement BaseCallback interface)
                     or a callable that accepts CallbackEvent

        Usage:
            from aigie.callbacks import GenericWebhookCallback

            webhook = GenericWebhookCallback(
                endpoint="https://my-service.com/logs",
                headers={"Authorization": "Bearer token"}
            )
            aigie.add_callback(webhook)
        """
        self._callbacks.append(callback)
        logger.debug(f"Added callback: {callback}")

    def remove_callback(self, callback: Any) -> bool:
        """
        Remove a callback handler.

        Args:
            callback: The callback instance to remove

        Returns:
            True if callback was found and removed
        """
        try:
            self._callbacks.remove(callback)
            logger.debug(f"Removed callback: {callback}")
            return True
        except ValueError:
            return False

    def list_callbacks(self) -> list[Any]:
        """Get list of registered callbacks."""
        return list(self._callbacks)

    async def _notify_callbacks(self, event: Any) -> None:
        """
        Notify all registered callbacks of an event.

        This is called internally by trace/span lifecycle methods.
        """
        for callback in self._callbacks:
            try:
                # Check if callback is enabled
                if hasattr(callback, "enabled") and not callback.enabled:
                    continue

                # Call the callback
                if hasattr(callback, "on_event"):
                    await callback.on_event(event)
                elif callable(callback):
                    result = callback(event)
                    if asyncio.iscoroutine(result):
                        await result
            except Exception as e:
                logger.warning(f"Callback error ({callback}): {e}")


def _run_async_init(aigie_instance: Aigie, timeout: float = 10.0) -> None:
    """Run initialize() in a dedicated thread with its own event loop.

    Works identically from sync code, async code, Jupyter, nested loops.
    The loop stays alive after init so background tasks (gateway, signals,
    pattern cache, event buffer) keep running.
    """
    init_done = threading.Event()
    init_error: list = [None]
    loop = asyncio.new_event_loop()

    def _target():
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(aigie_instance.initialize())
        except Exception as e:
            init_error[0] = e
            aigie_instance._init_status = "failed"
            aigie_instance._init_errors = [str(e)]
        finally:
            init_done.set()
        loop.run_forever()  # Keep running for background tasks

    thread = threading.Thread(target=_target, daemon=True)
    thread.start()
    completed = init_done.wait(timeout=timeout)

    if not completed:
        logger.warning("[AIGIE] Init timed out — continuing in background, agent not blocked")
        aigie_instance._init_status = "partial"
    elif init_error[0]:
        logger.warning(f"[AIGIE] Init failed: {init_error[0]}")

    # Store references so fire_and_forget() and shutdown() can find the loop
    aigie_instance._bg_loop = loop
    aigie_instance._bg_thread = thread


def init(
    kytte_url: str | None = None,  # Positional arg #1 — Kytte platform URL
    kytte_token: str | None = None,  # Positional arg #2 — Kytte license token
    *,  # Everything else keyword-only
    log_level: str | None = None,  # Logging verbosity (DEBUG/INFO/WARNING/...)
    agent_name: str | None = None,  # Agent/deployment name for identification
    config: Config | None = None,
) -> Aigie:
    """
    Initialize global Aigie instance with auto-instrumentation.

    This is the recommended way to initialize Aigie. After calling init(),
    all LLM calls will be automatically traced.

    Usage:
        import aigie
        aigie.init("https://your-kytte-instance.com/api", "your-kytte-token")

    Args:
        kytte_url: Kytte platform URL (unique per deployment)
        kytte_token: Kytte license token for authentication
        log_level: Logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        agent_name: Agent/deployment name for identification
        config: Optional Config object (if provided, overrides other params)

    Returns:
        Initialized Aigie instance
    """
    global _global_aigie, _instrumentation_enabled

    # ── URL / token resolution: explicit param > KYTTE_* env vars
    effective_url = kytte_url or os.getenv("KYTTE_URL")
    effective_token = kytte_token or os.getenv("KYTTE_TOKEN")

    # ── Token validation feedback ────────────────────────────────────
    if not effective_url and not effective_token:
        logger.warning(format_diagnostic(C003))
    elif not effective_token:
        logger.warning(format_diagnostic(C002))

    # ── Create global instance ───────────────────────────────────────
    _global_aigie = Aigie(
        effective_url,
        effective_token,
        config=config,
        log_level=log_level,
        agent_name=agent_name,
    )

    # ── Step 1: Auto-instrumentation SYNCHRONOUSLY (always on)
    _enable_auto_instrumentation()

    # ── Step 2: Async init in dedicated background thread ────────────
    try:
        _run_async_init(_global_aigie, timeout=10.0)
    except Exception as e:
        logger.warning(format_diagnostic(I004, extra=str(e)))

    # ── Step 4: Register atexit → shutdown() ─────────────────────────
    import atexit

    atexit.register(lambda: shutdown(timeout=5.0))

    # SIGTERM (k8s pod stop) skips atexit; wire it to shutdown() too.
    _install_termination_flush()

    return _global_aigie


_termination_handlers_installed = False
_prev_signal_handlers: dict[int, Any] = {}


def _termination_handler(sig, frame):  # type: ignore[no-untyped-def]
    """Flush, then chain to the handler we replaced."""
    try:
        shutdown(timeout=5.0)
    except Exception:
        pass
    previous = _prev_signal_handlers.get(sig)
    if callable(previous):
        previous(sig, frame)
    else:
        # No prior handler: re-raise with the default disposition.
        signal.signal(sig, signal.SIG_DFL)
        os.kill(os.getpid(), sig)


def _install_termination_flush() -> None:
    """Run shutdown() on SIGTERM/SIGINT, then chain to the prior handler.

    SIGTERM's default disposition skips atexit, so the root span never ships.
    Best-effort, main-thread-only (signal.signal() raises elsewhere).
    """
    global _termination_handlers_installed
    if _termination_handlers_installed:
        return
    installed = False
    for signum in (signal.SIGTERM, signal.SIGINT):
        try:
            _prev_signal_handlers[signum] = signal.getsignal(signum)
            signal.signal(signum, _termination_handler)
            installed = True
        except (ValueError, OSError):
            pass  # off main thread / unsupported
    _termination_handlers_installed = installed


def shutdown(timeout: float = 10.0) -> None:
    """Flush remaining traces and shut down the Aigie runtime.

    Call before program exits to ensure all data is sent.
    Automatically registered via atexit when init() is called.
    """
    from aigie import telemetry as _internal_telemetry

    _internal_telemetry.shutdown_sync(timeout_ms=5_000)

    global _global_aigie
    instance = _global_aigie
    if instance is None:
        return

    loop = getattr(instance, "_bg_loop", None)
    if loop and loop.is_running():
        # Use the persistent bg loop — run close() there, then stop it
        future = asyncio.run_coroutine_threadsafe(instance.close(), loop)
        try:
            future.result(timeout=timeout)
        except Exception:
            pass  # Best effort cleanup
        loop.call_soon_threadsafe(loop.stop)
        thread = getattr(instance, "_bg_thread", None)
        if thread:
            thread.join(timeout=2.0)
    else:
        # Fallback: no persistent loop (edge case)
        def _target():
            _loop = asyncio.new_event_loop()
            asyncio.set_event_loop(_loop)
            try:
                _loop.run_until_complete(instance.close())
            except Exception:
                pass
            finally:
                _loop.close()

        try:
            t = threading.Thread(target=_target, daemon=True)
            t.start()
            t.join(timeout=timeout)
        except Exception:
            pass


def get_aigie() -> Aigie | None:
    """
    Get the global Aigie instance.

    Returns:
        Global Aigie instance if initialized, None otherwise
    """
    return _global_aigie


def _enable_auto_instrumentation() -> None:
    """Enable auto-instrumentation for all supported frameworks."""
    global _instrumentation_enabled

    if _instrumentation_enabled:
        return  # Already enabled

    # Import and enable auto-instrumentation modules
    try:
        from aigie.auto_instrument import enable_all

        enable_all()
        _instrumentation_enabled = True
    except ImportError as e:
        # Auto-instrumentation modules not available yet
        import logging

        logger = logging.getLogger(__name__)
        logger.warning(f"Auto-instrumentation not available: {e}")
