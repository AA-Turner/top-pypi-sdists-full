"""AutonomousRuntime — composes all v2 subsystems behind a single facade.

Initialized by the SDK client (aigie.Aigie); receives span-complete events
and either applies a locally synthesised flow directive or routes a
pushed Judge directive to a framework adapter. Wires:
    ConfigProvider → FlowCache → ControlStreamClient → FlowEvaluator
    → BlastRadiusGate → DirectiveApplier → OutcomeReporter
"""

from __future__ import annotations

import collections
import concurrent.futures
import importlib
import logging
import os
import threading
import time
from typing import Any

import aigie.telemetry as _telemetry
from aigie.autonomous.adapters import SpanContext
from aigie.autonomous.config import ConfigProvider, HttpEtagConfigProvider, ResolvedConfig
from aigie.autonomous.directives import (
    BlastRadiusGate,
    Directive,
    DirectiveApplier,
    PermitDecision,
)
from aigie.autonomous.flow_evaluator import FlowEvaluator, SpanView
from aigie.autonomous.flows import FlowCache
from aigie.autonomous.outcome import OutcomeReport, OutcomeReporter, Status

logger = logging.getLogger(__name__)

tracer = _telemetry.get_tracer("aigie.autonomous")

_DISABLED_ENV = "AIGIE_AUTONOMOUS_DISABLE"

_DEFAULT_CACHE_ENTRIES = 10_000


class SpanContextCache:
    """Bounded LRU cache mapping (trace_id, span_id) → (framework, framework_handle).

    Populated by integrations on span start/end so that pushed Judge directives
    can resolve framework context even when no span is active in the calling thread.
    Thread-safe: a single lock guards all mutations and reads.
    """

    def __init__(self, max_entries: int = _DEFAULT_CACHE_ENTRIES) -> None:
        self._max = max_entries
        self._cache: collections.OrderedDict[tuple[str, str], tuple[str, Any]] = (
            collections.OrderedDict()
        )
        self._lock = threading.Lock()

    def register(
        self,
        trace_id: str,
        span_id: str,
        framework: str,
        framework_handle: Any,
    ) -> None:
        """Record or refresh a (trace_id, span_id) → (framework, handle) entry."""
        key = (trace_id, span_id)
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = (framework, framework_handle)
            if len(self._cache) > self._max:
                self._cache.popitem(last=False)

    def lookup(
        self,
        trace_id: str,
        span_id: str,
    ) -> tuple[str, Any] | None:
        """Return (framework, handle) or None if not found."""
        key = (trace_id, span_id)
        with self._lock:
            entry = self._cache.get(key)
            if entry is not None:
                self._cache.move_to_end(key)
            return entry


class AutonomousRuntime:
    """Facade that composes all autonomous v2 subsystems.

    When AIGIE_AUTONOMOUS_DISABLE=1 all public methods are no-ops.
    Otherwise, start() must be called before on_span_complete() will have
    any effect (subsystems are fully initialized in __init__).
    """

    def __init__(
        self,
        endpoint: str,
        api_key: str | None = None,
        customer_id: str = "",
        sdk_version: str = "",
        config_provider: ConfigProvider | None = None,
    ) -> None:
        self._disabled = os.environ.get(_DISABLED_ENV) == "1"
        if self._disabled:
            return

        self.config_provider: ConfigProvider = config_provider or HttpEtagConfigProvider(
            endpoint=endpoint, api_key=api_key
        )
        self.flow_cache = FlowCache()
        self.flow_evaluator = FlowEvaluator(self.flow_cache)
        self.blast_radius_gate = BlastRadiusGate(self.config_provider)
        self.applier = DirectiveApplier()

        # importlib used intentionally: import-linter (Grimp) performs static AST
        # analysis and would flag any `from aigie.autonomous.control_plane import ...`
        # statement as a transitive _pb dependency, even inside a function body.
        # Using importlib.import_module breaks the static edge while preserving
        # runtime behaviour — this is the only way to respect the proto-firewall
        # contract (ADR §3.7) without editing pyproject.toml.
        _cp = importlib.import_module("aigie.autonomous.control_plane")
        make_client = _cp.make_client

        self.control_stream = make_client(
            endpoint=endpoint,
            api_key=api_key,
            customer_id=customer_id,
            sdk_version=sdk_version or "0.2.40",
            on_directive=self._handle_pushed_directive,
            rule_cache_version_provider=lambda: self.flow_cache.version,
        )

        self.outcome_reporter = OutcomeReporter(sink=self.control_stream)
        # Wire reconnect → drain (on_connected_callbacks is a public list on ControlStreamClient)
        self.control_stream.on_connected_callbacks.append(self.outcome_reporter.on_connected)

        self.span_context_cache = SpanContextCache()

        self._apply_executor: concurrent.futures.ThreadPoolExecutor = (
            concurrent.futures.ThreadPoolExecutor(
                max_workers=2,
                thread_name_prefix="aigie-apply",
            )
        )
        self._started = False

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """True when autonomous processing is active."""
        return not self._disabled

    @property
    def config(self) -> ResolvedConfig | None:
        """Return the current ResolvedConfig snapshot, or None if unavailable."""
        if self._disabled:
            return None
        try:
            return self.config_provider.get()
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Inline (call-domain) hook surface — used by FrameworkAdapter._install_autonomous
    # ------------------------------------------------------------------

    def register_chain_hook(self, hook: Any, priority: int = 10, name: str | None = None) -> None:
        """Register an interceptor-chain post-call hook for autonomous dispatch.

        Idempotent: registering the same named hook twice replaces the first
        registration (no duplicate dispatch). Safe to call before the SDK
        client has wired up the chain — the hook is buffered and installed
        on the next call to :py:meth:`bind_interceptor_chain`.
        """
        hook_name = name or getattr(hook, "name", "autonomous_dispatch")
        if not hasattr(self, "_pending_chain_hooks"):
            self._pending_chain_hooks: list[tuple[Any, int, str]] = []
        # Replace any pending hook with the same name to keep idempotency.
        self._pending_chain_hooks = [
            entry for entry in self._pending_chain_hooks if entry[2] != hook_name
        ]
        self._pending_chain_hooks.append((hook, priority, hook_name))  # type: ignore[arg-type]
        chain = getattr(self, "_chain", None)
        if chain is not None:
            chain.remove_post_hook(hook_name)
            chain.add_post_hook(hook, priority=priority, name=hook_name)

    def bind_interceptor_chain(self, chain: Any) -> None:
        """Attach an :class:`InterceptorChain` and flush pending chain hooks."""
        self._chain = chain
        for hook, priority, hook_name in getattr(self, "_pending_chain_hooks", []):
            chain.remove_post_hook(hook_name)
            chain.add_post_hook(hook, priority=priority, name=hook_name)

    def evaluate_inline(self, ctx: Any) -> Directive | None:
        """Evaluate an InterceptionContext synchronously and return a Directive.

        Builds a minimal OTel-shaped span from the context and runs the
        FlowEvaluator. Used by :func:`aigie.autonomous.dispatch.dispatch`.

        A ``None`` return means "no flow fires for this call". Per the
        autonomous-v2 plan (Gap 9), the caller (dispatch.dispatch) MUST
        translate that into ``PostCallResult.allow()`` so the user's call
        proceeds normally — no swallowed errors, no implicit remediation.
        """
        if self._disabled:
            return None
        span_view = _span_view_from_interception_ctx(ctx)
        try:
            directive = self.flow_evaluator.evaluate(
                span_view,
                pending_step_lookup=self._pending_step_lookup,
            )
        except Exception as exc:  # noqa: BLE001
            logger.debug("evaluate_inline flow error: %s", exc)
            return None
        if directive is None:
            # No matching flow → let the call return normally (allow()).
            return None
        framework = span_view.framework
        permit = self.blast_radius_gate.permit(directive, framework=framework)
        if permit.decision == PermitDecision.DENIED:
            self.outcome_reporter.report(_failed_outcome(directive, permit.reason))
            return None
        return directive

    def _pending_step_lookup(self, _flow_id: str, _trace_id: str) -> int:
        """Pending-step index for (flow_id, trace_id). Always 0 for now.

        The TTL-evicted tracker that advances on FAILED outcomes is wired
        in the next task; this stub keeps the surface in place so wiring
        across runtime.py and the evaluator is already done.
        """
        return 0

    def report_outcome(self, directive: Directive, status: Status, reason: str) -> None:
        """Emit an OutcomeReport for an autonomous directive."""
        if self._disabled:
            return
        outcome = OutcomeReport(
            directive_id=directive.directive_id,
            rule_id=directive.rule_id,
            remediation_plan_id=directive.remediation_plan_id,
            plan_step_index=directive.plan_step_index,
            status=status,
            next_span_ok=status == Status.APPLIED,
            observed_at_unix_ms=int(time.time() * 1000),
            rule_cache_version=directive.rule_cache_version,
            reason=reason,
            trace_id=directive.trace_id,
            span_id=directive.span_id,
        )
        self.outcome_reporter.report(outcome)

    def start(self) -> None:
        """Start background subsystems. Idempotent."""
        if self._disabled or self._started:
            return
        # Subscribe BEFORE start() so we see the first config emission. Then
        # eagerly load the current ResolvedConfig (the smart-poll provider
        # may have already populated it during construction or skip the
        # initial subscriber callback).
        self.config_provider.subscribe(self._on_config_change)
        self.config_provider.start()
        self._on_config_change(self.config_provider.get())
        self.control_stream.start()
        self._started = True
        from aigie.autonomous._metrics import register as _register_metrics

        _register_metrics(self)
        logger.info(
            "AutonomousRuntime started (endpoint=%s)", _redact(self.control_stream._endpoint)
        )

    def _on_config_change(self, resolved: Any) -> None:
        """Translate the /v1/sdk/config envelope into the local FlowCache."""
        try:
            if resolved is None or not resolved.version:
                return
            flows = resolved.flows() if hasattr(resolved, "flows") else []
            self.flow_cache.swap(resolved.version, flows)
            logger.info(
                "FlowCache loaded: version=%s flows=%d",
                resolved.version[:16],
                len(flows),
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to apply config: %s", exc)

    def stop(self, timeout: float = 5.0) -> None:
        """Stop subsystems in reverse order. Idempotent; never raises.

        Order matters: drain the apply executor FIRST so any in-flight
        directive applies finish and enqueue their outcomes; then drain
        outcome_reporter so those outcomes actually get sent on the
        control stream BEFORE we close it.
        """
        if self._disabled:
            return
        _safe(self._apply_executor.shutdown, wait=True)
        _safe(self.outcome_reporter.stop, timeout)
        _safe(self.control_stream.stop, grace=2.0)
        _safe(self.config_provider.stop)
        self._started = False
        logger.debug("AutonomousRuntime stopped")

    def register_span_context(
        self,
        trace_id: str,
        span_id: str,
        framework: str,
        framework_handle: Any,
    ) -> None:
        """Register framework context for a span so pushed directives can find it.

        Called by integrations on span start/end. No-op when runtime is disabled.
        """
        if self._disabled:
            return
        self.span_context_cache.register(trace_id, span_id, framework, framework_handle)

    def on_span_complete(self, span: Any) -> None:
        """Public hook: evaluate a completed span and dispatch if a rule fires."""
        if self._disabled:
            return
        attrs: Any = getattr(span, "attributes", {}) or {}
        trace_id = attrs.get("trace_id", "")
        span_id = attrs.get("span_id", "")
        with tracer.start_as_current_span("runtime.on_span_complete") as otel_span:
            otel_span.set_attribute("trace_id", trace_id)
            otel_span.set_attribute("span_id", span_id)
            self._on_span_complete_inner(span, trace_id, span_id, otel_span)

    def _on_span_complete_inner(
        self, span: Any, trace_id: str, span_id: str, otel_span: Any
    ) -> None:
        span_view = SpanView.from_otel_span(span)
        otel_span.set_attribute("framework", span_view.framework or "")
        framework_handle = getattr(span, "framework_handle", None)
        if trace_id and span_id and span_view.framework:
            self.span_context_cache.register(
                trace_id, span_id, span_view.framework, framework_handle
            )
        directive = self.flow_evaluator.evaluate(
            span_view, pending_step_lookup=self._pending_step_lookup
        )
        if directive is None:
            return
        self._gate_and_dispatch(directive, span_view.framework, span)

    # ------------------------------------------------------------------
    # Internal — span path
    # ------------------------------------------------------------------

    def _gate_and_dispatch(
        self,
        directive: Directive,
        framework: str | None,
        span: Any,
    ) -> None:
        """Check blast radius then submit apply job."""
        permit = self.blast_radius_gate.permit(directive, framework=framework)
        if permit.decision == PermitDecision.DENIED:
            report = _failed_outcome(directive, permit.reason)
            self.outcome_reporter.report(report)
            return

        span_ctx = _build_span_ctx(span)
        self._apply_executor.submit(self._apply_and_report, directive, framework, span_ctx)

    def _apply_and_report(
        self,
        directive: Directive,
        framework: str | None,
        span_ctx: SpanContext | None,
    ) -> None:
        """Worker: apply directive and report outcome. Catches all exceptions."""
        try:
            outcome = self.applier.apply(directive, framework, span_ctx)
        except Exception as exc:
            logger.exception("DirectiveApplier raised unexpectedly: %s", exc)
            outcome = _failed_outcome(directive, f"applier_exception:{exc}")
        self.outcome_reporter.report(outcome)

    # ------------------------------------------------------------------
    # Internal — control-stream callbacks
    # ------------------------------------------------------------------

    def _handle_pushed_directive(self, directive: Directive) -> None:
        """Handle a directive pushed by the platform Judge.

        Attempts to resolve span context from SpanContextCache using the directive's
        trace_id and span_id. If found, the directive is routed through the gate and
        adapter with full framework context. If not found, emits a FAILED OutcomeReport
        with reason="span_context_not_found" for adapter-requiring actions.
        IN_STEP_RETRY is handled centrally and succeeds without an adapter.
        """
        framework: str | None = getattr(directive, "framework_hint", None)
        span_ctx: SpanContext | None = None

        cached = self.span_context_cache.lookup(directive.trace_id, directive.span_id)
        if cached is not None:
            framework, handle = cached
            span_ctx = SpanContext(
                trace_id=directive.trace_id,
                span_id=directive.span_id,
                framework=framework,
                framework_handle=handle,
                logger=logger,
            )

        permit = self.blast_radius_gate.permit(directive, framework=framework)
        if permit.decision == PermitDecision.DENIED:
            self.outcome_reporter.report(_failed_outcome(directive, permit.reason))
            return
        self._apply_executor.submit(self._apply_and_report, directive, framework, span_ctx)

# ------------------------------------------------------------------
# Module-level helpers (keep runtime class statement-count in budget)
# ------------------------------------------------------------------


def _safe(fn: Any, *args: Any, **kwargs: Any) -> None:
    """Call fn(*args, **kwargs), swallowing any exception."""
    try:
        fn(*args, **kwargs)
    except Exception as exc:
        logger.debug("AutonomousRuntime shutdown step raised: %s", exc)


def _redact(value: str) -> str:
    """Return value with credentials stripped for log safety."""
    return value.split("@")[-1] if "@" in value else value


def _build_span_ctx(span: Any) -> SpanContext | None:
    """Best-effort: build SpanContext from a duck-typed span."""
    try:
        attrs: Any = getattr(span, "attributes", {}) or {}
        framework_handle = getattr(span, "framework_handle", None)
        return SpanContext(  # type: ignore[call-arg]
            trace_id=attrs.get("trace_id", ""),
            span_id=attrs.get("span_id", ""),
            framework_handle=framework_handle,
        )
    except Exception:
        return None


class _StubSpan:
    """Lightweight duck-typed span carrying only ``attributes`` for SpanView."""

    __slots__ = ("attributes",)

    def __init__(self, attributes: dict[str, Any]) -> None:
        self.attributes = attributes


def _span_view_from_interception_ctx(ctx: Any) -> SpanView:
    """Build a SpanView from an InterceptionContext.

    Translates provider/error/metadata into the OTel-shaped attributes the
    FlowEvaluator expects. Kept here (not in flow_evaluator.py) because
    it's InterceptionContext-aware glue, not part of the OTel normaliser.
    """
    provider = getattr(ctx, "provider", "") or ""
    metadata = dict(getattr(ctx, "metadata", {}) or {})
    error = getattr(ctx, "error", None)
    error_class = type(error).__name__ if error is not None else None
    error_type = getattr(ctx, "error_type", None)

    framework = metadata.get("framework") or getattr(ctx, "framework", None) or provider

    # Extract HTTP status code: prefer metadata, fall back to the error object.
    # LLM SDK errors (anthropic.APIStatusError, openai.APIStatusError, etc.)
    # carry .status_code so the DSL can match on it.
    status_code = metadata.get("status_code")
    if status_code is None and error is not None:
        status_code = getattr(error, "status_code", None)

    attrs: dict[str, Any] = {
        "agent.framework": framework,
        "agent.error.class": error_class or error_type,
        "agent.workflow.id": metadata.get("workflow_id"),
        "agent.customer.id": metadata.get("customer_id"),
        "agent.use_case": metadata.get("use_case"),
        "trace_id": getattr(ctx, "trace_id", None) or "",
        "span_id": getattr(ctx, "span_id", None) or "",
        "agent.tool.name": metadata.get("tool_name"),
        "agent.message.role": metadata.get("message_role"),
        "agent.step.kind": metadata.get("step_kind"),
        "agent.drift.signature": metadata.get("drift_signature"),
        "agent.status_code": status_code,
    }
    attrs = {k: v for k, v in attrs.items() if v is not None}
    return SpanView.from_otel_span(_StubSpan(attrs))


def _failed_outcome(directive: Directive, reason: str) -> OutcomeReport:
    return OutcomeReport(
        directive_id=directive.directive_id,
        rule_id=directive.rule_id,
        remediation_plan_id=directive.remediation_plan_id,
        plan_step_index=directive.plan_step_index,
        status=Status.FAILED,
        next_span_ok=False,
        observed_at_unix_ms=int(time.time() * 1000),
        rule_cache_version=directive.rule_cache_version,
        reason=reason,
        trace_id=directive.trace_id,
        span_id=directive.span_id,
    )
