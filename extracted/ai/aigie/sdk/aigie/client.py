"""
Aigie Client - Main SDK class for integrating Aigie monitoring.
"""

import asyncio
import logging
import os
import time
from collections.abc import Callable
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Optional

import httpx

from .buffer import BufferedEvent, EventBuffer, EventType
from .config import Config
from .diagnostics import (
    A001,
    A002,
    A003,
    C002,
    C003,
    I004,
    R001,
    R002,
    R006,
    format_diagnostic,
)
from .trace import TraceContext

if TYPE_CHECKING:
    from .diagnostics import DoctorResult
    from .drift import DriftMonitor
    from .interceptor import InterceptionContext, InterceptorChain, PostCallHook, PreCallHook
    from .licensing import LicenseInfo, LicenseValidator
    from .rules import LocalRulesEngine, Rule

logger = logging.getLogger(__name__)

# Global singleton instance
_global_aigie: Optional["Aigie"] = None
_instrumentation_enabled: bool = False
import threading

_global_lock = threading.Lock()


class Aigie:
    """
    Main Aigie client for monitoring AI agent workflows.

    Usage:
        aigie = Aigie()
        await aigie.initialize()

        async with aigie.trace("My Workflow") as trace:
            # Your code here
            pass

    With data masking:
        def mask_pii(data: dict) -> dict:
            # Redact emails, phone numbers, etc.
            return redacted_data

        aigie = Aigie(mask=mask_pii)

    With debug mode:
        aigie = Aigie(debug=True)  # or AIGIE_DEBUG=true
    """

    def __init__(
        self,
        kytte_url: str | None = None,  # Primary: Kytte platform URL
        kytte_token: str | None = None,  # Primary: Kytte authentication token
        *,
        config: Config | None = None,
        mask: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
        debug: bool = False,
        log_level: str | None = None,
        llm_api_key: str | None = None,
        judge_model: str | None = None,
        agent_name: str | None = None,
        framework: str | None = None,
        # DEPRECATED aliases — still work, emit warnings
        aigie_url: str | None = None,
        aigie_token: str | None = None,
        api_url: str | None = None,
        api_key: str | None = None,
    ):
        """
        Initialize Aigie client.

        Args:
            kytte_url: Kytte platform URL (defaults to KYTTE_URL env var)
            kytte_token: Kytte authentication token (REQUIRED for data to be sent)
            config: Optional Config object (if provided, overrides other params)
            mask: Optional function to mask sensitive data (PII protection)
            debug: Enable debug mode for detailed logging
            log_level: Control logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            aigie_url: DEPRECATED — use kytte_url
            aigie_token: DEPRECATED — use kytte_token
            api_url: DEPRECATED — use kytte_url
            api_key: DEPRECATED — use kytte_token
        """
        import warnings

        # ── URL resolution: kytte_url > aigie_url (deprecated) > api_url (deprecated) > env vars
        effective_url = kytte_url

        if effective_url is None and aigie_url is not None:
            effective_url = aigie_url
            warnings.warn(
                "Aigie(aigie_url=...) is deprecated, use kytte_url instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        if effective_url is None and api_url is not None:
            effective_url = api_url
            warnings.warn(
                "Aigie(api_url=...) is deprecated, use kytte_url instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        if effective_url is None:
            _env_url = os.getenv("KYTTE_URL")
            if not _env_url:
                _env_url = os.getenv("AIGIE_URL") or os.getenv("AIGIE_API_URL")
                if _env_url:
                    warnings.warn(
                        "AIGIE_URL / AIGIE_API_URL env vars are deprecated, use KYTTE_URL.",
                        DeprecationWarning,
                        stacklevel=2,
                    )
            effective_url = _env_url or ""

        # ── Token resolution: kytte_token > aigie_token (deprecated) > api_key (deprecated) > env vars
        effective_token = kytte_token

        if effective_token is None and aigie_token is not None:
            effective_token = aigie_token
            warnings.warn(
                "Aigie(aigie_token=...) is deprecated, use kytte_token instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        if effective_token is None and api_key is not None:
            effective_token = api_key
            warnings.warn(
                "Aigie(api_key=...) is deprecated, use kytte_token instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        if effective_token is None:
            _env_token = os.getenv("KYTTE_TOKEN")
            if not _env_token:
                _env_token = os.getenv("AIGIE_TOKEN") or os.getenv("AIGIE_API_KEY")
                if _env_token:
                    warnings.warn(
                        "AIGIE_TOKEN / AIGIE_API_KEY env vars are deprecated, use KYTTE_TOKEN.",
                        DeprecationWarning,
                        stacklevel=2,
                    )
            effective_token = _env_token

        # Use config if provided, otherwise create from params/env
        if config:
            self.config = config
            self._aigie_url = config.aigie_url
            # Use the effective token from constructor if provided, otherwise from config
            self._auth_token = effective_token or config.get_auth_token()
        else:
            self.config = Config(
                aigie_url=effective_url,
                api_key=api_key or "",  # Deprecated, kept for backward compat
                aigie_token=effective_token,
                mask=mask,
                debug=debug or os.getenv("AIGIE_DEBUG", "").lower() in ("true", "1", "yes"),
            )
            self._aigie_url = self.config.aigie_url
            self._auth_token = self.config.get_auth_token()

        # DEPRECATED: Keep api_url for backward compatibility but use _aigie_url internally
        self.api_url = self._aigie_url

        # DEPRECATED: Keep api_key for backward compatibility but use _auth_token internally
        self.api_key = self._auth_token or ""

        # Store mask function for use in traces/spans
        self._mask_fn = mask or self.config.mask
        self._debug = debug or self.config.debug

        # Agent identification metadata
        self._agent_name = agent_name or os.getenv("AIGIE_AGENT_NAME")
        self._framework = framework or os.getenv("AIGIE_FRAMEWORK")

        # Set global mask function for decorators
        if self._mask_fn:
            from . import decorators_v3

            decorators_v3.set_global_mask_fn(self._mask_fn)

        # Configure logging level
        # Priority: debug parameter > log_level parameter > AIGIE_LOG_LEVEL env var > default WARNING
        if debug:
            effective_log_level = logging.DEBUG
        else:
            level_str = log_level or os.getenv("AIGIE_LOG_LEVEL", "WARNING").upper()
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

        # Set debug mode
        if self._debug:
            from . import decorators_v3

            decorators_v3.set_debug_mode(True)
            logger.debug("Aigie client initialized in debug mode")

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
        self._enable_compression: bool = os.getenv("AIGIE_ENABLE_COMPRESSION", "").lower() in (
            "true",
            "1",
            "yes",
        )
        self._compressor = None  # Lazily initialized Compressor

        # Real-time interception components
        self._interceptor_chain: InterceptorChain | None = None
        self._rules_engine: LocalRulesEngine | None = None
        self._legacy_backend: Any | None = None  # autonomous mode removed
        self._drift_monitor: DriftMonitor | None = None
        self._legacy_autofix: Any | None = None  # autonomous mode removed

        # LLM Judge and Runtime components (autonomous mode removed)
        self._llm_judge: Any | None = None
        self._context_aggregator: Any | None = None
        self._span_interceptor: Any | None = None
        self._legacy_remediation: Any | None = None  # autonomous mode removed

        # User-supplied callable for autonomous retries: (provider, model, messages, **kwargs) -> response
        self._llm_retry_executor: Any = None

        # License validation (for self-hosted installations)
        self._license_validator: LicenseValidator | None = None
        self._license_info: LicenseInfo | None = None

        # Callback handlers (LiteLLM-style)
        self._callbacks: list[Any] = []

        # Gateway and Autonomous Mode (auto-enabled via env vars)
        self._legacy_gateway: Any | None = None  # autonomous mode removed
        self._legacy_mode: Any | None = None  # autonomous mode removed
        self._signal_reporter: Any | None = None
        self._health_monitor: Any | None = None

        # Runtime reliability components (Tier 1 + Tier 2)
        self._fast_detector: Any | None = None
        self._legacy_async_judge: Any | None = None  # autonomous mode removed
        self._pattern_cache: Any | None = None
        self._judge_selector: Any | None = None

        # LLM API key for Aigie's internal judge model
        # Today: OpenAI gpt-4o-mini / Gemini flash. Future: local SLM in customer's cluster.
        self._judge_model: str | None = judge_model or os.getenv("AIGIE_JUDGE_MODEL")
        self._judge_model_from_code: bool = (
            judge_model is not None
        )  # Code-level override takes priority over platform
        self._llm_api_key: str | None = llm_api_key or self._resolve_llm_api_key()
        self._judge_llm_client: Any | None = None

        # Autonomous v2 runtime — single gate: config.autonomous.
        # (Legacy AIGIE_AUTONOMOUS_DISABLE is honored via Config defaults, which
        # also emits a one-line deprecation warning at construct time.)
        self._autonomous_runtime: Any | None = None  # AutonomousRuntime | None
        if self.config.autonomous and self._aigie_url:
            try:
                from aigie.autonomous.runtime import AutonomousRuntime as _AR

                self._autonomous_runtime = _AR(
                    endpoint=self._aigie_url,
                    api_key=self._auth_token,
                )
            except Exception as _e:
                logger.debug("AutonomousRuntime init skipped: %s", _e)

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
            "aigie.autonomous",  # v2: reflex hits, directives, outcomes (ADR 0001)
            "aigie.integrations",
            "aigie.gateway",
            "aigie.client",
            "aigie.callback",
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

    @property
    def autonomous_runtime(self) -> Any:
        """Return the v2 AutonomousRuntime instance, or None if disabled/unavailable.

        Integrations (Wave H) call ``runtime.on_span_complete(span)`` here.
        The runtime type is AutonomousRuntime | None at runtime.
        """
        return self._autonomous_runtime

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
                from . import __version__ as _ver

                headers["X-SDK-Version"] = str(_ver)
            except Exception:
                pass
            self.client = httpx.AsyncClient(
                timeout=httpx.Timeout(
                    connect=self.config.connect_timeout,
                    read=self.config.timeout,
                    write=self.config.timeout,
                    pool=self.config.connect_timeout,
                ),
                limits=httpx.Limits(max_connections=self.config.max_connections),
                headers=headers,
            )

            if self.config.internal_telemetry.enabled:
                from aigie import telemetry as _internal_telemetry
                _internal_telemetry.initialize(self.config.internal_telemetry)

            # Initialize event buffer if enabled
            if self.config.enable_buffering:
                self._buffer = EventBuffer(
                    max_size=self.config.batch_size,
                    flush_interval=self.config.flush_interval,
                    max_retries=self.config.max_retries,
                    retry_delay=self.config.retry_delay,
                    enable_circuit_breaker=self.config.enable_circuit_breaker,
                    circuit_breaker_threshold=self.config.circuit_breaker_threshold,
                    circuit_breaker_timeout=self.config.circuit_breaker_timeout,
                )
                self._buffer.set_flusher(self._flush_events)
                # Wire the atexit-safe sync-urllib fallback so terminal
                # trace_update events still reach the backend after the bg
                # loop has been torn down. Buffer is a no-op fallback when
                # url is None.
                fallback_headers: dict[str, str] = {}
                if self._auth_token:
                    fallback_headers["Authorization"] = f"Bearer {self._auth_token}"
                self._buffer.set_sync_fallback(
                    api_url=self._aigie_url, headers=fallback_headers
                )
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
            if self.api_url:
                parallel_tasks.append(_safe_init("platform", self._check_platform_health(), 5.0))
                parallel_tasks.append(
                    _safe_init("legacy_transport", self._init_legacy_transport(), 10.0)
                )

            # License validation
            if self.config.aigie_token and not self.config.skip_license_validation:
                parallel_tasks.append(_safe_init("license", self._initialize_license(), 5.0))

            # Real-time interception (chain). Gated on the single autonomous toggle.
            if self.config.autonomous:
                parallel_tasks.append(
                    _safe_init("interception", self._initialize_interception(), 10.0)
                )

            # Gateway and Autonomous Mode
            parallel_tasks.append(
                _safe_init("autonomous", self._initialize_autonomous_features(), 5.0)
            )

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

            # ── Phase 3: Wiring + pattern cache ─────────────────────────
            self._wire_components()

            if self._pattern_cache:
                try:
                    from .utils.safe import schedule_async

                    schedule_async(self._pattern_cache.initial_sync())
                    self._pattern_cache.start_background_refresh()
                except Exception as e:
                    logger.debug(f"Pattern cache sync failed (non-fatal): {e}")

            # ── Phase 4: Auto-instrumentation (sync, idempotent) ────────
            should_auto_instrument = getattr(self.config, "enable_auto_instrument", True)
            explicitly_disabled = getattr(self.config, "disable_auto_instrument", False)

            if should_auto_instrument and not explicitly_disabled:
                try:
                    from .integrations.install import install_framework_adapters

                    install_framework_adapters(
                        aigie=self, runtime=self._autonomous_runtime
                    )
                except Exception as e:
                    logger.debug("Framework adapter install failed (non-fatal): %s", e)
                _enable_auto_instrumentation()
                logger.info("Auto-instrumentation enabled - LLM calls will be automatically traced")

            # ── Phase 5: Startup diagnostics banner ────────────────────────
            try:
                from .diagnostics import format_startup_banner

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
            from . import __version__ as ver

            version = str(ver) if ver else "unknown"
        except Exception:
            version = "unknown"

        # Auth status
        if self._auth_token and self._license_info and self._license_info.valid:
            auth = ("ok", f"connected (tier: {self._license_info.tier})")
        elif self._auth_token:
            auth = ("ok", "token set (license not validated)")
        else:
            auth = ("error", "no token [AIGIE-C002]")

        # Gateway
        if self._legacy_gateway and getattr(self._legacy_gateway, "is_connected", False):
            gateway = ("ok", "connected")
        elif not self._auth_token or not self._aigie_url:
            gateway = ("skip", "skipped (no auth)")
        else:
            gateway = ("error", "not connected [AIGIE-N001]")

        # Interception
        if self._interceptor_chain is not None:
            rule_count = len(self._rules_engine.list_rules()) if self._rules_engine else 0
            mode = "full" if self._legacy_backend else "local-only"
            interception = ("ok", f"enabled ({mode}, {rule_count} rules)")
        else:
            interception = ("skip", "disabled")

        # Auto-instrument
        frameworks = []
        if _instrumentation_enabled:
            for name in ["langchain", "langgraph", "openai", "anthropic", "strands", "google_adk"]:
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

        # Judge mode
        if self._judge_llm_client:
            model = self._judge_model or "gpt-4o-mini"
            method = "SDK" if getattr(self._judge_llm_client, "_use_sdk", False) else "httpx"
            judge = ("ok", f"LLM ({model} via {method})")
        else:
            judge = ("warn", "heuristic-only (set AIGIE_LLM_API_KEY for LLM evaluation)")

        return {
            "version": version,
            "mode": os.getenv("AIGIE_MODE", "observe"),
            "platform_url": self._aigie_url or "not configured",
            "auth": auth,
            "gateway": gateway,
            "interception": interception,
            "judge": judge,
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

        # Try /v1/health (no auth required)
        health_url = f"{self.api_url}/v1/health"
        response = await self.client.get(health_url, timeout=3.0)
        response.raise_for_status()

        health = response.json()
        version = health.get("version", "unknown")
        logger.info(f"[AIGIE] Platform reachable — {self.api_url} (v{version})")

    async def _init_legacy_transport(self) -> None:
        """No-op (Redis transport removed with autonomous mode)."""
        return

    async def _initialize_interception(self) -> None:
        """Initialize real-time interception components."""
        from .drift import DriftConfig, DriftMonitor
        from .interceptor import InterceptorChain
        from .rules import LocalRulesEngine

        # AutoFixApplicator / FixConfig live in an optional realtime module that
        # may not be present in all deployments. The chain itself is the critical
        # path; legacy autofix is not required for IN_STEP_RETRY to work.
        try:
            from .realtime import AutoFixApplicator  # type: ignore[import]
            from .realtime import FixConfig as _FixConfig

            _fix_config = _FixConfig(
                max_retries=self.config.auto_fix_max_retries,
                fallback_models=getattr(self.config, "fallback_models", []),
            )
            self._legacy_autofix = AutoFixApplicator(config=_fix_config)
        except ImportError:
            logger.debug("aigie.realtime not available — legacy autofix disabled")

        logger.info("Initializing real-time interception components")

        # Initialize local rules engine with config-based rules
        self._rules_engine = LocalRulesEngine(config=self.config)
        logger.debug(f"Rules engine initialized with {len(self._rules_engine.list_rules())} rules")

        # Initialize drift monitor
        drift_config = DriftConfig(
            topic_drift_threshold=self.config.drift_threshold,
            behavior_drift_threshold=self.config.drift_threshold,
            enable_topic_detection=self.config.enable_drift_detection,
            enable_behavior_detection=self.config.enable_drift_detection,
            enable_quality_detection=self.config.enable_drift_detection,
            enable_coherence_detection=self.config.enable_drift_detection,
        )
        self._drift_monitor = DriftMonitor(config=drift_config)

        # Initialize interceptor chain with rules engine
        self._interceptor_chain = InterceptorChain(
            rules_engine=self._rules_engine,
            local_timeout_ms=self.config.local_decision_timeout_ms,
        )

        # Backend WebSocket connector removed with autonomous mode.

        # Register drift monitor alerts with interceptor chain
        async def on_drift_alert(alert):
            logger.warning(f"Drift alert: {alert.drift_type.value} - {alert.reason}")

        self._drift_monitor.on_alert(on_drift_alert)

        # Initialize LLM Judge and Runtime components
        await self._initialize_judge_and_runtime()

        logger.info("Real-time interception initialized successfully")

    async def _initialize_autonomous_features(self) -> None:
        """Start autonomous v2 runtime and bind the interceptor chain.

        When both runtime and chain exist, bind unconditionally so the
        autonomous_dispatch hook flushes from `_pending_chain_hooks` onto
        the chain and IN_STEP_RETRY can actually fire.
        """
        if self._autonomous_runtime is None:
            return
        if self._interceptor_chain is not None:
            self._autonomous_runtime.bind_interceptor_chain(self._interceptor_chain)
        try:
            self._autonomous_runtime.start()
        except Exception as e:
            logger.debug("AutonomousRuntime.start() failed (non-fatal): %s", e)

    def _wire_components(self) -> None:
        """Wire all SDK components together using their existing setter APIs.

        This method closes the "connection gap" — components are created in
        _initialize_interception() and _initialize_autonomous_features() but
        their cross-references are never set because of initialization order.

        Every connection is guarded by None checks so nothing breaks if a
        component wasn't initialized (e.g. due to config flags or init failure).
        """
        # InterceptorChain ← Aigie client reference
        if self._interceptor_chain is not None:
            self._interceptor_chain.set_aigie_client(self)

        # Autonomous remediation wiring removed.

        # SpanInterceptor ← retry callback
        if self._span_interceptor is not None:
            self._span_interceptor.retry_callback = self._create_retry_callback()

        # Legacy autonomous backend wiring removed.
        if False:
            if hasattr(self._legacy_backend, "on_fix_push"):
                self._legacy_backend.on_fix_push(self._handle_fix_push)
            if hasattr(self._legacy_backend, "on_alert"):
                self._legacy_backend.on_alert(self._handle_alert)
            if hasattr(self._legacy_backend, "on_pattern_update") and self._pattern_cache:

                async def _on_pattern_update(data: dict[str, Any]) -> None:
                    """Trigger immediate pattern cache refresh on backend notification."""
                    logger.info(
                        f"[AIGIE] Pattern update from backend: {data.get('reason', 'unknown')}"
                    )
                    if self._pattern_cache:
                        await self._pattern_cache.force_refresh()

                self._legacy_backend.on_pattern_update(_on_pattern_update)

        logger.debug("Component wiring complete")

    def _create_retry_executor(self):
        """Create a retry executor function for AutoFixApplicator.

        Returns a stub that raises NotImplementedError so that AutoFixApplicator
        correctly reports fix failure instead of silently returning None.
        Override by calling set_llm_retry_executor(callable) with a real provider callable.
        """

        async def retry_executor(provider: str, model: str, messages: list, **kwargs):
            """Execute a retry through the wrapper layer."""
            logger.debug(f"Retry executor called: provider={provider}, model={model}")
            if self._llm_retry_executor is not None:
                return await self._llm_retry_executor(
                    provider=provider, model=model, messages=messages, **kwargs
                )
            raise NotImplementedError(
                f"No LLM retry executor configured for provider={provider}, model={model}. "
                "Call aigie.set_llm_retry_executor(callable) to enable autonomous retries."
            )

        return retry_executor

    def _create_retry_callback(self):
        """Create a retry callback for SpanInterceptor."""

        async def retry_callback(span_id: str, messages: list, **kwargs):
            """Callback invoked when SpanInterceptor decides to retry a span."""
            logger.debug(f"Retry callback for span {span_id}")

        return retry_callback

    def _handle_fix_push(self, fix_data: dict) -> None:
        """No-op (autonomous fix push removed)."""
        return

    def _handle_alert(self, alert_data: dict) -> None:
        """Handle an alert from the backend via WebSocket."""
        logger.info(f"Received alert from backend: {alert_data.get('alert_type', 'unknown')}")

    async def _initialize_license(self) -> None:
        """Initialize license validation for self-hosted installations."""
        from .licensing import (
            LicenseError,
            LicenseExpiredError,
            LicenseRevokedError,
            LicenseValidator,
        )

        logger.info("Initializing license validation")

        self._license_validator = LicenseValidator(
            aigie_token=self.config.aigie_token,
            license_server_url=self.config.license_server_url,
            installation_id=self.config.installation_id,
            enable_telemetry=self.config.enable_usage_telemetry,
        )

        try:
            # Validate license with the licensing server
            self._license_info = await self._license_validator.validate()

            if not self._license_info.valid:
                raise LicenseError(self._license_info.error or "License validation failed")

            logger.info(
                f"License validated: tier={self._license_info.tier}, "
                f"features={list(self._license_info.features.keys())}"
            )

            # Start background tasks for heartbeat and usage reporting
            await self._license_validator.start_background_tasks()

        except LicenseExpiredError as e:
            # License expired - log warning but don't crash the customer's app
            # SDK will operate in degraded mode (stop sending data)
            logger.warning(format_diagnostic(A001, extra=str(e)))
        except LicenseRevokedError as e:
            # License revoked - log warning but don't crash the customer's app
            logger.warning(format_diagnostic(A002, extra=str(e)))
        except LicenseError as e:
            logger.warning(format_diagnostic(A003, extra=str(e)))
        except Exception as e:
            # For network errors, log warning but allow operation if license was previously valid
            logger.warning(f"License validation error (non-fatal): {e}")

    def _resolve_llm_api_key(self) -> str | None:
        """Resolve LLM API key from env vars (LiteLLM-style fallback chain).

        Priority:
        1. AIGIE_LLM_API_KEY (explicit Aigie judge key)
        2. Provider-specific key based on judge_model
        3. Generic OPENAI_API_KEY fallback
        """
        # 1. Explicit Aigie judge key
        key = os.getenv("AIGIE_LLM_API_KEY")
        if key:
            return key

        # 2. Provider-specific key based on judge_model
        model = (self._judge_model or "").lower()
        provider_key_map = {
            "gemini": ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
            "anthropic": ["ANTHROPIC_API_KEY"],
            "groq": ["GROQ_API_KEY"],
            "together": ["TOGETHER_API_KEY"],
            "fireworks": ["FIREWORKS_API_KEY"],
            "mistral": ["MISTRAL_API_KEY"],
            "openrouter": ["OPENROUTER_API_KEY"],
        }
        for provider, env_vars in provider_key_map.items():
            if model.startswith(f"{provider}/") or model.startswith(f"{provider}-"):
                for env_var in env_vars:
                    key = os.getenv(env_var)
                    if key:
                        return key
        if model.startswith("bedrock/"):
            return None  # Bedrock uses IAM, not API key

        # 3. Generic fallback
        return os.getenv("OPENAI_API_KEY")

    async def _initialize_judge_and_runtime(self) -> None:
        """No-op (LLM judge and remediation runtime removed with autonomous mode)."""
        return

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

        from .decorators_v3 import traceable as _traceable_v3

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
                client=self.client,
                api_url=self.api_url,
                buffer=self._buffer,
                name=name,
                metadata=enriched_metadata,
                tags=tags or [],
                sample_rate=self.config.sampling_rate,
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
        from .trace import get_current_trace

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
        from .trace import update_current_trace

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
        from .prompts import PromptRegistry

        if not hasattr(self, "_prompt_manager"):
            self._prompt_manager = PromptRegistry()
        return self._prompt_manager

    @property
    def feedback(self):
        """
        Get feedback collector for human feedback and eval ground truth.

        Usage:
            # Submit human override of LLM judgment
            await aigie.feedback.submit_eval_override(
                judge_run_id="judge-123",
                human_score=0.9,
                human_verdict="pass",
                human_reasoning="The response was actually helpful"
            )

            # Submit trace feedback (thumbs up/down)
            await aigie.feedback.submit_trace_feedback(
                trace_id="trace-abc",
                rating="positive",
                comment="Great response!"
            )
        """
        from .feedback import FeedbackCollector

        if not hasattr(self, "_feedback_collector"):
            self._feedback_collector = FeedbackCollector(self._buffer)
        return self._feedback_collector

    @property
    def gateway(self):
        """Get the Gateway client for real-time validation."""
        return self._legacy_gateway

    @property
    def mode(self):
        """Get the current operation mode (observe/autonomous)."""
        if self._legacy_mode:
            return self._legacy_mode.current_mode
        return None

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
        from .context import extract_trace_context

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
        from .context import TraceContext

        if parent_context:
            return parent_context.create_child()
        return TraceContext()

    async def remediate(self, trace_id: str, error: Exception) -> dict[str, Any]:
        """
        Trigger autonomous remediation for an error.

        Args:
            trace_id: Trace ID with the error
            error: The exception that occurred

        Returns:
            Remediation result
        """
        if not self._initialized:
            await self.initialize()

        response = await self.client.post(
            f"{self.api_url}/v1/remediation/autonomous/fix",
            json={
                "trace_id": trace_id,
                "error": {"type": type(error).__name__, "message": str(error)},
            },
        )
        response.raise_for_status()
        return response.json()

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
            from .interceptor.protocols import InterceptionContext, InterceptionDecision

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
            from .interceptor.protocols import InterceptionContext

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

    async def detect_precursors(self, context: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Detect error precursors in the given context.

        Args:
            context: Context data to analyze

        Returns:
            List of detected precursors
        """
        if not self._initialized:
            await self.initialize()

        response = await self.client.post(
            f"{self.api_url}/v1/prevention/detect-precursors", json={"context": context}
        )
        response.raise_for_status()
        return response.json().get("precursors", [])

    async def apply_preventive_fix(
        self, trace_id: str, precursors: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Apply preventive fixes based on detected precursors.

        Args:
            trace_id: Trace ID
            precursors: List of detected precursors

        Returns:
            Fix application result
        """
        if not self._initialized:
            await self.initialize()

        response = await self.client.post(
            f"{self.api_url}/v1/prevention/apply-preventive-fix",
            json={"trace_id": trace_id, "precursors": precursors},
        )
        response.raise_for_status()
        return response.json()

    async def _send_batch(self, events: list[dict[str, Any]]) -> None:
        """
        Send batch of events to batch ingestion endpoint.

        Supports compression with Zstandard if available.

        Args:
            events: List of event dictionaries already in correct format from _flush_events
                   Format: {"type": "trace-create", "id": "...", "timestamp": "...", "body": {...}}
        """
        from datetime import datetime

        # Events are already in the correct format from _flush_events
        # Just ensure timestamps are strings and validate structure
        batch_events = []
        for event in events:
            # Validate required fields
            if "type" not in event or "id" not in event or "body" not in event:
                logger.warning(f"Skipping invalid event: missing required fields: {event.keys()}")
                continue

            # Ensure timestamp is a string
            if "timestamp" not in event:
                event["timestamp"] = datetime.utcnow().isoformat()
            elif isinstance(event["timestamp"], datetime):
                event["timestamp"] = event["timestamp"].isoformat()

            # Ensure body is a dict
            if not isinstance(event.get("body"), dict):
                logger.warning(f"Skipping event with invalid body type: {type(event.get('body'))}")
                continue

            batch_events.append(event)

        if not batch_events:
            logger.warning("No valid events to send in batch")
            return

        # Skip while auth is suspended (backing off after 401)
        if self._is_auth_suspended():
            return

        # Prepare request payload
        request_payload = {"batch": batch_events}

        # Validate payload can be serialized to JSON
        import json

        try:
            json.dumps(request_payload, default=str)  # Test serialization
        except Exception as e:
            logger.error(format_diagnostic(R002, extra=str(e)))
            return

        # Debug: Log first event structure (only in debug mode)
        if logger.isEnabledFor(logging.DEBUG) and batch_events:
            logger.debug(f"Sample event structure: {batch_events[0]}")

        headers = {"Content-Type": "application/json"}
        if self._auth_token:
            headers["X-API-Key"] = self._auth_token
        try:
            from . import __version__ as _ver

            headers["X-SDK-Version"] = str(_ver)
        except Exception:
            pass

        # Check if event loop is available before attempting to send
        try:
            loop = asyncio.get_running_loop()
            if loop.is_closed():
                logger.debug(
                    f"Event loop is closed, skipping batch send ({len(batch_events)} events)"
                )
                return
        except RuntimeError:
            # No event loop running - this is expected during shutdown
            logger.debug(f"No event loop running, skipping batch send ({len(batch_events)} events)")
            return

        try:
            if self._enable_compression:
                # Use Zstandard compression for bandwidth savings
                from .compression import get_compressor, is_compression_available

                if is_compression_available():
                    if self._compressor is None:
                        self._compressor = get_compressor(level=1)
                    json_bytes = json.dumps(request_payload, default=str).encode("utf-8")
                    compressed = self._compressor.compress(json_bytes)
                    headers["Content-Encoding"] = "zstd"
                    headers["Content-Type"] = "application/json"
                    response = await self.client.post(
                        f"{self.api_url}/v1/ingestion",
                        content=compressed,
                        headers=headers,
                    )
                    if logger.isEnabledFor(logging.DEBUG):
                        ratio = len(compressed) / len(json_bytes) if json_bytes else 1.0
                        logger.debug(
                            f"Compressed batch: {len(json_bytes)}→{len(compressed)} bytes ({ratio:.1%})"
                        )
                else:
                    response = await self.client.post(
                        f"{self.api_url}/v1/ingestion",
                        json=request_payload,
                        headers=headers,
                    )
            else:
                # Use content= with default=str to handle any non-serializable types (UUID, datetime, etc.)
                json_bytes = json.dumps(request_payload, default=str).encode("utf-8")
                headers["Content-Type"] = "application/json"
                response = await self.client.post(
                    f"{self.api_url}/v1/ingestion",
                    content=json_bytes,
                    headers=headers,
                )
        except Exception as e:
            # Check if it's an event loop issue - if so, we can't recover
            error_str = str(e).lower()
            if (
                "event loop is closed" in error_str
                or "event loop" in error_str
                or "runtimeerror" in error_str
            ):
                # This is expected during application shutdown - log as debug instead of error
                logger.debug(
                    f"Event loop issue, cannot send batch ({len(batch_events)} events): {e}"
                )
                return  # Can't recover from event loop closure
            # Re-raise network/connectivity errors so the buffer's circuit breaker and
            # retry/offline-storage logic can handle them.  Swallowing these caused the
            # circuit breaker to never open and events to be silently dropped (AIGIE-R001).
            if isinstance(e, (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError)):
                raise
            logger.error(format_diagnostic(R001, extra=f"{type(e).__name__}: {e}"))
            import traceback

            logger.error(f"Batch send traceback: {traceback.format_exc()}")
            return

        # Handle response - log validation/server errors with details for debugging
        if response.status_code == 401:
            self._handle_auth_failure()
            return  # Suspended — will retry after backoff
        if response.status_code == 403:
            # 403 is retryable (transient permission propagation, nginx rate limit)
            logger.warning("[AIGIE] 403 Forbidden on /v1/ingestion — will retry via buffer.")
            raise httpx.HTTPStatusError(
                "403 Forbidden", request=response.request, response=response
            )
        if response.status_code in (400, 422):  # 422 is FastAPI validation error
            error_text = response.text[:1000] if response.text else "No error message"
            status_name = "validation" if response.status_code == 422 else "client"
            logger.warning(
                f"Batch ingestion {status_name} error ({response.status_code}): {error_text}"
            )
            # Try to parse error details
            try:
                error_json = response.json()
                if isinstance(error_json, dict):
                    detail = error_json.get("detail", error_json)
                    logger.warning(f"Batch ingestion error details: {detail}")
                else:
                    logger.warning(f"Batch ingestion error response: {error_json}")
            except Exception as e:
                logger.warning(f"Failed to parse batch ingestion error response: {e}")
            return  # Don't process response, just return
        if response.status_code == 500:
            error_text = response.text[:1000] if response.text else "No error message"
            logger.error(format_diagnostic(R006, extra=error_text))
            return  # Don't process response, just return

        response.raise_for_status()
        self._handle_auth_success()  # Reset retry state on success

        # Check for errors in 207 Multi-Status response
        try:
            result = response.json()
            if result.get("errors"):
                # Log errors but don't fail (some events may have succeeded)
                logger.debug(
                    f"Batch ingestion had {len(result.get('errors', []))} errors out of {len(result.get('successes', [])) + len(result.get('errors', []))} total events"
                )
                # Log first few errors for debugging
                for error in result.get("errors", [])[:3]:
                    logger.debug(f"Batch ingestion error: {error}")
            else:
                logger.debug(
                    f"Batch ingestion successful: {len(result.get('successes', []))} events processed"
                )
        except Exception as e:
            # If response parsing fails, just continue
            logger.warning(f"Batch ingestion response parsing failed (non-critical): {e}")

    async def _flush_events(self, events: list[BufferedEvent]) -> None:
        """
        Flush buffered events to the API.

        Tries batch ingestion endpoint first, falls back to individual endpoints.

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

        # Apply mask function to event payloads before sending (PII protection)
        if self.config.mask:
            for event in events:
                try:
                    event.payload = self.config.mask(event.payload)
                except Exception as e:
                    logger.warning(f"Mask function failed for event {event.event_type.value}: {e}")

        # Try batch ingestion endpoint first
        try:
            # Convert to batch format matching backend schema
            batch_events = []
            for event in events:
                # Map event type from underscore to hyphen format
                # Core events use hyphen format, intelligence events keep underscore
                event_type_map = {
                    "trace_create": "trace-create",
                    "trace_update": "trace-update",
                    "span_create": "span-create",
                    "span_update": "span-update",
                    # Intelligence events stay as-is (underscore format)
                    "guardrail_check": "guardrail_check",
                    "eval_feedback": "eval_feedback",
                    "remediation_result": "remediation_result",
                    "workflow_pattern": "workflow_pattern",
                    "health_ping": "health_ping",
                }
                event_type = event_type_map.get(event.event_type.value, event.event_type.value)

                # Get event ID
                event_id = (
                    event.payload.get("id")
                    or event.payload.get("trace_id")
                    or event.payload.get("span_id")
                )
                if not event_id:
                    logger.warning(f"Skipping event without ID: {event.event_type.value}")
                    continue

                # Get timestamp from payload or use current time
                timestamp_str = (
                    event.payload.get("timestamp")
                    or event.payload.get("start_time")
                    or event.payload.get("created_at")
                )
                if timestamp_str:
                    # If it's already a string, use it; if datetime, convert
                    if isinstance(timestamp_str, datetime):
                        timestamp = timestamp_str.isoformat()
                    else:
                        timestamp = timestamp_str
                else:
                    timestamp = datetime.now(timezone.utc).isoformat()

                # Prepare body - ensure it matches TraceBody/SpanBody schema
                body = event.payload.copy()

                # For trace events, map fields to TraceBody schema
                if "trace" in event_type:
                    # TraceBody expects: id, timestamp, name, input, output, metadata, tags, etc.
                    # Ensure id is in body
                    if "id" not in body:
                        body["id"] = event_id
                    # Convert start_time/created_at to timestamp (as ISO string, Pydantic will parse)
                    if "timestamp" not in body:
                        if "start_time" in body:
                            body["timestamp"] = body.pop("start_time")
                        elif "created_at" in body:
                            body["timestamp"] = body.pop("created_at")
                    # Remove fields not in TraceBody schema
                    body.pop("type", None)  # TraceBody doesn't have type
                    if event_type == "trace-create":
                        body.pop("status", None)  # TraceBody CREATE doesn't have status
                    # Ensure timestamp is a string if it's a datetime
                    if "timestamp" in body and isinstance(body["timestamp"], datetime):
                        body["timestamp"] = body["timestamp"].isoformat()

                # For span events, map fields to SpanBody schema
                elif "span" in event_type:
                    # SpanBody expects: id, trace_id, parent_id, name, type, start_time, end_time, input, output, etc.
                    # Ensure id is in body
                    if "id" not in body:
                        body["id"] = event_id
                    # Ensure trace_id is in body (not traceId)
                    if "trace_id" not in body and "traceId" in body:
                        body["trace_id"] = body.pop("traceId")
                    if "parent_id" not in body and "parentId" in body:
                        body["parent_id"] = body.pop("parentId")
                    # Ensure start_time is present (not created_at)
                    if "start_time" not in body and "created_at" in body:
                        body["start_time"] = body.pop("created_at")
                    # Convert endTime to end_time
                    if "end_time" not in body and "endTime" in body:
                        body["end_time"] = body.pop("endTime")
                    # Note: Keep status field for backend (it may extract it for span status)
                    # Remove timestamp as SpanBody uses start_time/end_time
                    body.pop("timestamp", None)  # SpanBody uses start_time/end_time, not timestamp
                    # Ensure start_time/end_time are strings if they're datetimes
                    if "start_time" in body and isinstance(body["start_time"], datetime):
                        body["start_time"] = body["start_time"].isoformat()
                    if "end_time" in body and isinstance(body["end_time"], datetime):
                        body["end_time"] = body["end_time"].isoformat()

                # Create event dict matching IngestionEvent schema
                # The type must be exactly "trace-create", "span-create", etc. (literal)
                event_dict = {
                    "type": event_type,  # Must match EventType enum exactly
                    "id": event_id,
                    "timestamp": timestamp,  # ISO string, Pydantic will parse to datetime
                    "body": body,  # Must match TraceBody or SpanBody schema
                }
                batch_events.append(event_dict)

            if not batch_events:
                logger.warning("No valid events to send in batch")
                return

            # Sort events so trace-create comes first, then span-create, span-update, trace-update
            # This prevents the backend from auto-creating traces from orphan spans
            _event_order = {
                "trace-create": 0,
                "span-create": 1,
                "span-update": 2,
                "trace-update": 3,
            }
            batch_events.sort(key=lambda e: _event_order.get(e["type"], 99))

            logger.info(
                f"Attempting batch ingestion for {len(batch_events)} events via /v1/ingestion"
            )
            await self._send_batch(batch_events)
            logger.info(
                f"Successfully sent {len(batch_events)} events via batch ingestion endpoint"
            )
            return  # Success, exit early
        except Exception as e:
            # Connectivity errors (ConnectTimeout, ConnectError, NetworkError) must propagate so
            # the buffer's circuit breaker can open and stop hammering the unreachable backend.
            # Falling back to individual endpoints on a connectivity failure would just multiply
            # the timeouts (N events × connect_timeout seconds) and make things much slower.
            if isinstance(e, (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError)):
                raise
            # Fallback to individual endpoints for non-connectivity failures (e.g. 4xx schema errors)
            logger.warning(
                f"Batch ingestion failed for {len(events)} events, falling back to individual endpoints: {type(e).__name__}: {e!s}"
            )

        # Fallback: Group events by type and send individually
        events_by_type: dict[EventType, list[BufferedEvent]] = {}
        for event in events:
            if event.event_type not in events_by_type:
                events_by_type[event.event_type] = []
            events_by_type[event.event_type].append(event)

        # Send batches
        for event_type, type_events in events_by_type.items():
            if self._is_auth_suspended():
                return  # Auth suspended during this flush — stop immediately
            if event_type == EventType.TRACE_CREATE:
                # Batch create traces
                for event in type_events:
                    try:
                        response = await self.client.post(
                            f"{self.api_url}/v1/traces", json=event.payload
                        )
                        response.raise_for_status()
                    except httpx.HTTPStatusError as e:
                        if e.response.status_code == 401:
                            self._handle_auth_failure()
                            return
                        if e.response.status_code == 403:
                            raise  # Retryable — let buffer retry
                        if e.response.status_code in (400, 500):
                            logger.debug(
                                f"Trace creation failed (non-critical): {e.response.status_code} - {e.response.text[:200]}"
                            )
                            continue
                        raise
                    except Exception as e:
                        logger.debug(f"Trace creation failed (non-critical): {e}")
                        continue
            elif event_type == EventType.TRACE_UPDATE:
                # Batch update traces
                for event in type_events:
                    try:
                        # Get trace_id without modifying original payload
                        payload = event.payload.copy()
                        trace_id = payload.pop("id", payload.pop("trace_id", None))
                        if not trace_id:
                            logger.debug("Trace update skipped: trace_id not found in payload")
                            continue
                        response = await self.client.put(
                            f"{self.api_url}/v1/traces/{trace_id}", json=payload
                        )
                        response.raise_for_status()
                    except httpx.HTTPStatusError as e:
                        if e.response.status_code == 401:
                            self._handle_auth_failure()
                            return
                        if e.response.status_code == 403:
                            raise  # Retryable — let buffer retry
                        if e.response.status_code in (400, 500):
                            logger.debug(
                                f"Trace update failed (non-critical): {e.response.status_code} - {e.response.text[:200]}"
                            )
                            continue
                        raise
                    except Exception as e:
                        logger.debug(f"Trace update failed (non-critical): {e}")
                        continue
            elif event_type == EventType.SPAN_CREATE:
                # Batch create spans
                for event in type_events:
                    try:
                        response = await self.client.post(
                            f"{self.api_url}/v1/spans",
                            json=event.payload,
                            headers={"X-API-Key": self._auth_token} if self._auth_token else {},
                            timeout=5.0,
                        )
                        response.raise_for_status()
                    except httpx.HTTPStatusError as e:
                        if e.response.status_code == 401:
                            self._handle_auth_failure()
                            return
                        # Suppress 400/500 errors - likely format or backend issues
                        if e.response.status_code in (400, 500):
                            logger.debug(
                                f"Span creation failed (non-critical): {e.response.status_code} - {e.response.text[:200]}"
                            )
                            continue
                        raise
                    except Exception as e:
                        # Suppress connection errors
                        logger.debug(f"Span creation failed (non-critical): {e}")
                        continue
            elif event_type == EventType.SPAN_UPDATE:
                # Batch update spans
                for event in type_events:
                    try:
                        # Get span_id without modifying original payload
                        payload = event.payload.copy()
                        span_id = payload.pop("id", payload.pop("span_id", None))
                        if not span_id:
                            logger.debug("Span update skipped: span_id not found in payload")
                            continue
                        response = await self.client.put(
                            f"{self.api_url}/v1/spans/{span_id}",
                            json=payload,
                            headers={"X-API-Key": self._auth_token} if self._auth_token else {},
                            timeout=5.0,
                        )
                        response.raise_for_status()
                    except httpx.HTTPStatusError as e:
                        if e.response.status_code == 401:
                            self._handle_auth_failure()
                            return
                        # Suppress 400/500 errors - likely format or backend issues
                        if e.response.status_code in (400, 500):
                            logger.debug(
                                f"Span update failed (non-critical): {e.response.status_code} - {e.response.text[:200]}"
                            )
                            continue
                        raise
                    except Exception as e:
                        # Suppress connection errors
                        logger.debug(f"Span update failed (non-critical): {e}")
                        continue

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

        from .diagnostics import DoctorResult, format_doctor_output

        checks = []
        warnings = []
        errors = []

        # SDK version
        try:
            from . import __version__ as ver

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
            if self._license_info and self._license_info.valid:
                tier = self._license_info.tier or "unknown"
                expires = (
                    self._license_info.expires_at.strftime("%Y-%m-%d")
                    if self._license_info.expires_at
                    else "n/a"
                )
                checks.append(("Authentication", "ok", f"valid (tier: {tier}, expires: {expires})"))
            else:
                checks.append(("Authentication", "ok", "token set (license not validated)"))
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

        # Gateway WS
        if self._legacy_gateway:
            if getattr(self._legacy_gateway, "is_connected", False):
                checks.append(("Gateway WS", "ok", "connected"))
            else:
                checks.append(("Gateway WS", "error", "not connected [AIGIE-N001]"))
                errors.append("AIGIE-N001")
        else:
            checks.append(("Gateway WS", "skip", "skipped (no auth or URL)"))

        # License
        if self._license_validator and getattr(self._license_validator, "usage_summary", None):
            summary = self._license_validator.usage_summary
            limit = self._license_info.max_traces_per_month if self._license_info else 0
            if limit and limit < 0:
                checks.append(
                    (
                        "License",
                        "ok",
                        f"active (unlimited, {summary.traces_this_month} traces this month)",
                    )
                )
            elif limit and limit > 0:
                checks.append(
                    (
                        "License",
                        "ok",
                        f"active ({summary.traces_this_month:,} / {limit:,} traces this month)",
                    )
                )
            else:
                checks.append(("License", "ok", "active"))
        elif self._license_info:
            checks.append(("License", "ok", f"valid (tier: {self._license_info.tier})"))
        else:
            checks.append(("License", "skip", "not validated"))

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

    async def close(self) -> None:
        """Close the HTTP client and flush remaining events."""
        self._closing = True

        from aigie import telemetry as _internal_telemetry
        await _internal_telemetry.shutdown(timeout_ms=5_000)

        # Tear down event-emitting components FIRST. Several of these can
        # enqueue events into `self._buffer` from their shutdown paths (or
        # from in-flight tasks they cancel during shutdown). Nulling the
        # buffer before they're stopped would NPE those final emits.

        # Stop autonomous v2 runtime (additive; does not affect legacy components)
        if self._autonomous_runtime is not None:
            try:
                self._autonomous_runtime.stop()
            except Exception as e:
                logger.debug("AutonomousRuntime.stop() failed (non-fatal): %s", e)
            self._autonomous_runtime = None

        # Close autonomous features
        if self._legacy_gateway:
            try:
                await self._legacy_gateway.disconnect()
            except Exception as e:
                logger.debug(f"Gateway disconnect: {e}")
            self._legacy_gateway = None

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

        # Legacy autonomous mode controller and backend connector were removed.

        if self._pattern_cache:
            try:
                await self._pattern_cache.stop()
            except Exception as e:
                logger.debug(f"Pattern cache stop: {e}")
            self._pattern_cache = None

        # Now drain the buffer. Background flusher's final flush picks up any
        # events the components above queued during their teardown.
        if self._buffer:
            await self._buffer.stop_background_flusher()
            self._buffer = None

        # Close judge LLM client (httpx connection pool)
        if self._judge_llm_client and hasattr(self._judge_llm_client, "close"):
            try:
                await self._judge_llm_client.close()
            except Exception as e:
                logger.debug(f"Judge LLM client close: {e}")
            self._judge_llm_client = None

        # Close license validator (stops background tasks, reports final usage)
        if self._license_validator:
            try:
                # Report any pending usage before closing
                await self._license_validator.report_usage()
            except Exception as e:
                logger.debug(f"Failed to report final usage: {e}")
            finally:
                await self._license_validator.close()
                self._license_validator = None

        # Legacy Redis intervention transport removed.

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
        self._legacy_backend = None
        self._drift_monitor = None
        self._legacy_autofix = None
        self._llm_judge = None
        self._context_aggregator = None
        self._span_interceptor = None
        self._legacy_remediation = None
        self._callbacks = []

        logger.debug("Aigie instance fully cleaned up")

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    # ==================== Guardrails API ====================

    async def report_guardrail_check(
        self,
        trace_id: str,
        guardrail_name: str,
        action: str,
        passed: bool,
        span_id: str | None = None,
        score: float = 1.0,
        issues: list[str] | None = None,
        modified_content: str | None = None,
        details: dict[str, Any] | None = None,
        duration_ms: float | None = None,
        timestamp: datetime | None = None,
    ) -> None:
        """
        Report a guardrail check result to the backend.

        This sends guardrail check events to Kytte for monitoring and display
        in the execution detail view.

        Args:
            trace_id: ID of the trace this guardrail check belongs to
            guardrail_name: Name of the guardrail (e.g., "PIIDetector", "ToxicityDetector")
            action: Action taken (pass, warn, retry, redirect, adjust, escalate)
            passed: Whether the content passed the check
            span_id: Optional span ID if check is associated with a specific span
            score: Confidence score (0.0 to 1.0)
            issues: List of detected issues
            modified_content: Modified content if action was adjust
            details: Additional details about the check
            duration_ms: Time taken for the check in milliseconds
            timestamp: When the check was performed (defaults to now)

        Example:
            await aigie.report_guardrail_check(
                trace_id="abc-123",
                guardrail_name="PIIDetector",
                action="adjust",
                passed=True,
                score=0.95,
                issues=["Found email address"],
                modified_content="[REDACTED]",
                duration_ms=12.5,
            )
        """
        if not self._buffer:
            logger.warning("Event buffer not initialized, skipping guardrail check report")
            return

        payload = {
            "trace_id": trace_id,
            "span_id": span_id,
            "guardrail_name": guardrail_name,
            "action": action,
            "passed": passed,
            "score": score,
            "issues": issues or [],
            "modified_content": modified_content,
            "details": details or {},
            "duration_ms": duration_ms,
            "timestamp": (timestamp or datetime.utcnow()).isoformat(),
        }

        await self._buffer.add(EventType.GUARDRAIL_CHECK, payload)
        logger.debug(f"Queued guardrail check event for trace {trace_id}: {guardrail_name}")

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

    @property
    def auto_fix(self) -> Any:
        """Get the auto-fix applicator for direct access (always None now)."""
        return self._legacy_autofix

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
            raise RuntimeError(
                "Interception not initialized. Set Config(autonomous=True) (the default) to enable the autonomous chain."
            )

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
            raise RuntimeError(
                "Interception not initialized. Set Config(autonomous=True) (the default) to enable the autonomous chain."
            )

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
            raise RuntimeError(
                "Interception not initialized. Set Config(autonomous=True) (the default) to enable the autonomous chain."
            )

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
            from .interceptor.protocols import InterceptionContext, InterceptionDecision

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

        from .interceptor.protocols import InterceptionContext

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

        # If retry requested and auto-fix is enabled, apply fixes via applicator
        if result.should_retry and self._legacy_autofix and result.fixes_applied:
            fix_result = await self._legacy_autofix.apply_fixes(ctx, result.fixes_applied)
            if fix_result.success:
                ctx.modified_response = fix_result.modified_response
                ctx.retry_kwargs = fix_result.retry_kwargs

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

        if self._legacy_autofix:
            stats["auto_fix"] = self._legacy_autofix.get_stats()

        if self._legacy_backend:
            stats["backend_connector"] = self._legacy_backend.get_stats()

        # Add judge and runtime stats
        if self._llm_judge:
            stats["judge"] = self._llm_judge.get_stats()

        if self._context_aggregator:
            stats["context_aggregator"] = self._context_aggregator.get_stats()

        if self._span_interceptor:
            stats["span_interceptor"] = self._span_interceptor.get_stats()

        if self._legacy_remediation:
            stats["remediation_loop"] = self._legacy_remediation.get_stats()

        return stats

    # ========== Autonomous Mode Control ==========

    def enable_autonomous_mode(self) -> bool:
        """
        Enable autonomous mode for automatic fixes in runtime.

        Call this when user clicks the "autonomous" button.
        Aigie will now automatically fix detected issues instead
        of just showing what it would do.

        Returns:
            True if autonomous mode was enabled successfully,
            False if not enough learning has occurred.
        """
        if not self._legacy_remediation:
            logger.warning("Remediation loop not initialized")
            return False

        enabled = self._legacy_remediation.enable_autonomous_mode()
        if enabled:
            logger.info("🤖 Autonomous mode ENABLED - Aigie will now fix issues automatically")
        return enabled

    def disable_autonomous_mode(self) -> None:
        """
        Disable autonomous mode and return to recommendation mode.

        Aigie will continue detecting issues but will only show
        what it would do, not automatically fix.
        """
        if self._legacy_remediation:
            self._legacy_remediation.disable_autonomous_mode()
            logger.info("👁️ Autonomous mode DISABLED - Returning to recommendation mode")

    def is_autonomous_mode(self) -> bool:
        """Check if autonomous mode is currently enabled."""
        return False

    def is_ready_for_autonomous(self) -> dict[str, Any]:
        """
        Check if the system is ready for autonomous mode.

        Returns a dict with:
        - ready: bool - Whether autonomous mode can be enabled
        - traces_processed: int - Number of traces analyzed
        - traces_needed: int - Minimum traces needed
        - patterns_learned: int - Workflow patterns identified
        - avg_pattern_confidence: float - Average confidence in patterns
        """
        if self._legacy_remediation:
            return self._legacy_remediation.is_ready_for_autonomous()
        return {
            "ready": False,
            "traces_processed": 0,
            "traces_needed": 100,
            "patterns_learned": 0,
            "avg_pattern_confidence": 0.0,
        }

    def get_pending_recommendations(self) -> list[Any]:
        """
        Get pending recommendations (what Aigie would fix in autonomous mode).

        These show the customer what fixes would be applied if they
        enable autonomous mode, helping build trust.
        """
        if self._legacy_remediation:
            return self._legacy_remediation.get_pending_recommendations()
        return []

    def accept_recommendation(self, span_id: str) -> bool:
        """
        Mark a recommendation as accepted (user applied fix manually).

        This helps Aigie learn from manual fixes.
        """
        if self._legacy_remediation:
            return self._legacy_remediation.accept_recommendation(span_id)
        return False

    def get_workflow_patterns(self) -> list[Any]:
        """
        Get the workflow patterns Aigie has learned.

        Shows the customer what workflows Aigie understands.
        """
        if self._legacy_remediation:
            return self._legacy_remediation.get_workflow_patterns()
        return []

    def set_llm_retry_executor(self, executor: Any) -> None:
        """
        Register a callable for autonomous LLM retries.

        Required to enable RETRY_REQUEST and FALLBACK_MODEL fix strategies in
        autonomous mode. Without this, those strategies report failure instead of
        silently returning None.

        Args:
            executor: Async callable with signature:
                async def executor(provider: str, model: str, messages: list, **kwargs) -> response

        Example::

            async def my_retry(provider, model, messages, **kwargs):
                client = openai.AsyncOpenAI()
                return await client.chat.completions.create(
                    model=model, messages=messages, **kwargs
                )

            aigie.set_llm_retry_executor(my_retry)
        """
        self._llm_retry_executor = executor
        logger.debug("LLM retry executor set")

    def set_judge_llm_client(self, client: Any) -> None:
        """
        Set the LLM client for the judge.

        The judge uses this client to evaluate span outputs.
        Should be a wrapped OpenAI or Anthropic client.
        """
        if self._llm_judge:
            self._llm_judge.set_llm_client(client)
            logger.debug("Judge LLM client set")

    # ========== License Management ==========

    @property
    def license_info(self) -> Optional["LicenseInfo"]:
        """Get the current license information."""
        return self._license_info

    @property
    def license_tier(self) -> str | None:
        """Get the current license tier (starter, pro, enterprise)."""
        return self._license_info.tier if self._license_info else None

    @property
    def license_features(self) -> dict[str, bool]:
        """Get available features based on license."""
        return self._license_info.features if self._license_info else {}

    def has_feature(self, feature: str) -> bool:
        """
        Check if a feature is available in the current license.

        Args:
            feature: Feature name (e.g., 'realtime', 'drift_detection', 'auto_remediation')

        Returns:
            True if feature is available
        """
        if not self._license_info:
            return True  # No license configured, allow all features
        return self._license_info.features.get(feature, False)

    def is_within_limits(self, metric: str, value: int) -> bool:
        """
        Check if a usage metric is within license limits.

        Args:
            metric: Metric name ('traces', 'seats', 'projects')
            value: Current value to check

        Returns:
            True if within limits
        """
        if not self._license_validator:
            return True  # No license configured, no limits
        return self._license_validator.is_within_limits(metric, value)

    def track_usage(self, traces: int = 0, spans: int = 0, api_calls: int = 0) -> None:
        """
        Track usage for license telemetry.

        This is called automatically by trace/span creation, but can be
        called manually for custom tracking.

        Args:
            traces: Number of traces created
            spans: Number of spans created
            api_calls: Number of API calls made
        """
        if self._license_validator:
            self._license_validator.track_usage(
                traces=traces,
                spans=spans,
                api_calls=api_calls,
            )

    async def validate_license(self, force: bool = False) -> Optional["LicenseInfo"]:
        """
        Manually validate the license.

        Args:
            force: Force validation even if cached

        Returns:
            LicenseInfo if valid, raises exception otherwise
        """
        if self._license_validator:
            self._license_info = await self._license_validator.validate(force=force)
            return self._license_info
        return None

    def get_license_status(self) -> dict[str, Any]:
        """
        Get comprehensive license status for display.

        Returns:
            Dict with license status information
        """
        if not self._license_info:
            return {
                "configured": False,
                "valid": True,  # No license = no restrictions
                "tier": None,
                "features": {},
                "usage": None,
            }

        usage = None
        if self._license_validator and self._license_validator.usage_summary:
            summary = self._license_validator.usage_summary
            usage = {
                "traces_this_month": summary.traces_this_month,
                "traces_remaining": summary.traces_remaining,
                "spans_this_month": summary.spans_this_month,
                "active_users": summary.active_users,
            }

        return {
            "configured": True,
            "valid": self._license_info.valid,
            "tier": self._license_info.tier,
            "features": self._license_info.features,
            "max_seats": self._license_info.max_seats,
            "max_traces_per_month": self._license_info.max_traces_per_month,
            "max_projects": self._license_info.max_projects,
            "expires_at": self._license_info.expires_at.isoformat()
            if self._license_info.expires_at
            else None,
            "is_unlimited": self._license_info.is_unlimited,
            "usage": usage,
        }

    # ========== Drift Detection API ==========

    async def detect_drift(
        self,
        trace_id: str,
        force: bool = False,
    ) -> dict[str, Any]:
        """
        Detect context drift in a trace.

        Analyzes a trace for various types of drift:
        - goal_drift: Agent deviating from original goal
        - plan_deviation: Agent not following expected execution plan
        - instruction_violation: Agent violating system prompt guidelines
        - topic_drift: Conversation veering off topic
        - hallucination: Inconsistent or fabricated outputs
        - tool_loop: Repeated tool calls in a loop
        - token_exhaustion: Running out of context window

        Args:
            trace_id: The trace ID to analyze
            force: Force re-detection even if cached

        Returns:
            Dict with drift analysis results:
            - trace_id: str
            - has_drift: bool
            - drift_type: str (e.g., "goal_drift", "tool_loop")
            - severity: str ("low", "medium", "high", "critical")
            - confidence: float (0.0-1.0)
            - signals: List of detected drift signals
            - recommendation: str (suggested action)
            - analyzed_at: str (ISO timestamp)

        Example:
            result = await aigie.detect_drift("trace-123")
            if result["has_drift"]:
                print(f"Drift detected: {result['drift_type']}")
                print(f"Recommendation: {result['recommendation']}")
        """
        if not self._initialized:
            await self.initialize()

        params = {}
        if force:
            params["force"] = "true"

        response = await self.client.post(
            f"{self.api_url}/v1/analytics/drift/detect",
            json={"trace_id": trace_id},
            params=params,
        )
        response.raise_for_status()
        return response.json()

    async def get_drift_history(
        self,
        trace_id: str,
    ) -> dict[str, Any]:
        """
        Get historical drift detections for a trace.

        Returns all drift detection results for a trace,
        useful for tracking drift over time during long-running agents.

        Args:
            trace_id: The trace ID to get history for

        Returns:
            Dict with:
            - trace_id: str
            - detections: List of drift detection results
            - total_detections: int

        Example:
            history = await aigie.get_drift_history("trace-123")
            for detection in history["detections"]:
                print(f"{detection['detected_at']}: {detection['drift_type']}")
        """
        if not self._initialized:
            await self.initialize()

        response = await self.client.get(
            f"{self.api_url}/v1/analytics/drift/history/{trace_id}",
        )
        response.raise_for_status()
        return response.json()

    async def get_drift_metrics(
        self,
        time_range: str = "24h",
        environment: str | None = None,
    ) -> dict[str, Any]:
        """
        Get aggregate drift metrics across traces.

        Provides overview statistics about drift patterns,
        useful for monitoring overall agent health.

        Args:
            time_range: Time range to analyze ("1h", "24h", "7d", "30d")
            environment: Optional environment filter (e.g., "production")

        Returns:
            Dict with:
            - time_range: str
            - total_traces: int
            - traces_with_drift: int
            - drift_rate: float (percentage)
            - drift_by_type: Dict[str, int] (counts per drift type)
            - drift_by_severity: Dict[str, int]
            - avg_confidence: float
            - top_recommendations: List[str]

        Example:
            metrics = await aigie.get_drift_metrics("24h")
            print(f"Drift rate: {metrics['drift_rate']}%")
            print(f"Most common: {metrics['drift_by_type']}")
        """
        if not self._initialized:
            await self.initialize()

        params = {"time_range": time_range}
        if environment:
            params["environment"] = environment

        response = await self.client.get(
            f"{self.api_url}/v1/analytics/drift/metrics",
            params=params,
        )
        response.raise_for_status()
        return response.json()

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
            "api_url": self.api_url,
            "error": None,
            "server_version": None,
        }

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                start = time.monotonic()
                response = await client.get(
                    f"{self.api_url}/v1/health",
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
        - License status
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

        # Check license status
        license_status = self.get_license_status()
        if license_status["configured"]:
            if license_status["valid"]:
                status["components"]["license"] = {
                    "status": "healthy",
                    "tier": license_status["tier"],
                    "features": list(license_status.get("features", {}).keys()),
                }
            else:
                status["healthy"] = False
                status["errors"].append("License validation failed")
                status["components"]["license"] = {"status": "unhealthy"}
        else:
            status["components"]["license"] = {
                "status": "not_configured",
                "message": "No license configured - operating in unlimited mode",
            }

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
    debug: bool = False,  # Debug mode
    mask: Callable | None = None,  # PII masking function
    llm_api_key: str | None = None,  # LLM API key for Aigie's internal judge
    judge_model: str | None = None,  # Override judge model (e.g. "gemini/gemini-2.0-flash")
    agent_name: str | None = None,  # Agent/deployment name for identification
    framework: str | None = None,  # Agent framework (langchain, langgraph, claude, etc.)
    # Backward-compatible (hidden from docs, still work)
    api_url: str | None = None,  # DEPRECATED alias for kytte_url
    api_key: str | None = None,  # DEPRECATED alias for kytte_token
    config: Config | None = None,
    **kwargs,
) -> Aigie:
    """
    Initialize global Aigie instance with auto-instrumentation.

    This is the recommended way to initialize Aigie. After calling init(),
    all LLM calls will be automatically traced and runtime protection is active.

    Usage:
        import aigie
        aigie.init("https://your-kytte-instance.com/api", "your-kytte-token")

        # With LLM-powered judge for real-time quality evaluation:
        aigie.init("https://your-kytte.com/api", "your-token", llm_api_key="sk-...")

    Args:
        kytte_url: Kytte platform URL (unique per deployment)
        kytte_token: Kytte license token for authentication
        debug: Enable debug mode for detailed logging
        mask: Optional function to mask sensitive data (PII protection)
        llm_api_key: API key for Aigie's internal judge model (enables Tier 2
            real-time quality evaluation). Today uses gpt-4o-mini; future
            releases will use a local SLM in the Kytte cluster for lower latency.
            Also configurable via AIGIE_LLM_API_KEY env var.
        api_url: DEPRECATED - Use kytte_url instead
        api_key: DEPRECATED - Use kytte_token instead
        config: Optional Config object (if provided, overrides other params)
        **kwargs: Additional config options passed to Config

    Returns:
        Initialized Aigie instance
    """
    global _global_aigie, _instrumentation_enabled
    import warnings

    # Import module-level settings
    import aigie as _aigie_module

    # ── URL resolution priority chain ────────────────────────────────
    # kytte_url → api_url (deprecated) → KYTTE_URL env → AIGIE_URL env → module-level vars
    effective_url = kytte_url
    _url_source = "kytte_url" if kytte_url else None

    if effective_url is None and api_url is not None:
        effective_url = api_url
        _url_source = "api_url"
        warnings.warn(
            "api_url is deprecated, use kytte_url instead.",
            DeprecationWarning,
            stacklevel=2,
        )

    if effective_url is None:
        # Try env vars — prefer KYTTE_URL, warn on deprecated names
        _env_url = os.getenv("KYTTE_URL")
        if not _env_url:
            _env_url = os.getenv("AIGIE_URL") or os.getenv("AIGIE_API_URL")
            if _env_url:
                warnings.warn(
                    "AIGIE_URL / AIGIE_API_URL env vars are deprecated, use KYTTE_URL.",
                    DeprecationWarning,
                    stacklevel=2,
                )
        if _env_url:
            effective_url = _env_url

    if effective_url is None:
        # Try module-level vars
        if hasattr(_aigie_module, "kytte_url") and _aigie_module.kytte_url:
            effective_url = _aigie_module.kytte_url
        elif hasattr(_aigie_module, "api_url") and _aigie_module.api_url:
            effective_url = _aigie_module.api_url

    # ── Token resolution priority chain ──────────────────────────────
    # kytte_token → api_key (deprecated) → KYTTE_TOKEN env → AIGIE_TOKEN env → module-level vars
    effective_token = kytte_token
    _token_source = "kytte_token" if kytte_token else None

    if effective_token is None and api_key is not None:
        effective_token = api_key
        _token_source = "api_key"
        warnings.warn(
            "api_key is deprecated, use kytte_token instead.",
            DeprecationWarning,
            stacklevel=2,
        )

    if effective_token is None:
        # Try env vars — prefer KYTTE_TOKEN, warn on deprecated names
        _env_token = os.getenv("KYTTE_TOKEN")
        if not _env_token:
            _env_token = os.getenv("AIGIE_TOKEN") or os.getenv("AIGIE_API_KEY")
            if _env_token:
                warnings.warn(
                    "AIGIE_TOKEN / AIGIE_API_KEY env vars are deprecated, use KYTTE_TOKEN.",
                    DeprecationWarning,
                    stacklevel=2,
                )
        if _env_token:
            effective_token = _env_token

    if effective_token is None:
        # Try module-level vars
        if hasattr(_aigie_module, "kytte_token") and _aigie_module.kytte_token:
            effective_token = _aigie_module.kytte_token
        elif hasattr(_aigie_module, "api_key") and _aigie_module.api_key:
            effective_token = _aigie_module.api_key

    # ── Token validation feedback ────────────────────────────────────
    if not effective_url and not effective_token:
        logger.warning(format_diagnostic(C003))
    elif not effective_token:
        logger.warning(format_diagnostic(C002))

    # Check debug mode from kwargs or module level
    effective_debug = debug
    if not effective_debug and hasattr(_aigie_module, "debug"):
        effective_debug = _aigie_module.debug
    if effective_debug:
        kwargs["debug"] = True

    # ── Create config ────────────────────────────────────────────────
    if config is None:
        config_kwargs: dict[str, Any] = {}
        if effective_url:
            config_kwargs["aigie_url"] = effective_url
        if effective_token:
            config_kwargs["aigie_token"] = effective_token
        if mask:
            config_kwargs["mask"] = mask
        config_kwargs.update(kwargs)
        config = Config(**{k: v for k, v in config_kwargs.items() if v is not None})

    # ── Create global instance ───────────────────────────────────────
    _global_aigie = Aigie(
        effective_url,
        effective_token,
        config=config,
        mask=mask,
        debug=effective_debug,
        llm_api_key=llm_api_key,
        judge_model=judge_model,
        agent_name=agent_name,
        framework=framework,
    )

    # Add any module-level callbacks
    if hasattr(_aigie_module, "_module_callbacks"):
        for callback in _aigie_module._module_callbacks:
            _global_aigie.add_callback(callback)

    # ── Step 1: Auto-instrumentation SYNCHRONOUSLY (must be ready before first LLM call)
    disable_env = os.getenv("AIGIE_DISABLE_AUTO_INSTRUMENT", "").lower()
    if disable_env not in ("true", "1", "yes"):
        _enable_auto_instrumentation()

    # ── Step 2: Async init in dedicated background thread ────────────
    try:
        _run_async_init(_global_aigie, timeout=10.0)
    except Exception as e:
        logger.warning(format_diagnostic(I004, extra=str(e)))

    # ── Step 4: Register atexit → shutdown() ─────────────────────────
    import atexit

    atexit.register(lambda: shutdown(timeout=5.0))

    return _global_aigie


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
        from .auto_instrument import enable_all

        enable_all()
        _instrumentation_enabled = True
    except ImportError as e:
        # Auto-instrumentation modules not available yet
        import logging

        logger = logging.getLogger(__name__)
        logger.warning(f"Auto-instrumentation not available: {e}")
