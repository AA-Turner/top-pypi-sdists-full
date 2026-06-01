"""FrameworkAdapter ABC, shared data types, and ActionType enum.

This module defines the internal representation of action types and the
contract every framework adapter must implement.  It intentionally has NO
imports from aigie.autonomous.control_plane._pb — proto values are converted
to/from this IntEnum exclusively inside control_plane/codec.py.
"""

from __future__ import annotations

import abc
import logging
from dataclasses import dataclass, field
from enum import IntEnum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aigie.autonomous.interventions.base import WorkflowIntervention
    from aigie.autonomous.runtime import AutonomousRuntime
    from aigie.tracing.emitter import TraceEmitter
    from aigie.tracing.errors import KytteError

# ---------------------------------------------------------------------------
# ActionType — mirrors the proto enum values but is NOT the proto enum.
# codec.py is the only place that converts between proto ActionType and this.
# ---------------------------------------------------------------------------


class ActionType(IntEnum):
    """Internal representation of proto ActionType (values must match proto)."""

    IN_STEP_RETRY = 1
    IN_STEP_REWRITE_ARGS = 2
    NEXT_STEP_INJECT_MESSAGE = 3
    TRAJECTORY_REWRITE_OUTPUT = 4
    TRAJECTORY_FORCE_FALLBACK = 5
    TRAJECTORY_BREAK_LOOP = 6


# ---------------------------------------------------------------------------
# ApplyStatus — what the adapter returns to the dispatcher
# ---------------------------------------------------------------------------


class ApplyStatus(IntEnum):
    """Result status returned by an adapter method to the dispatcher."""

    APPLIED = 1
    FAILED = 2
    SKIPPED = 3


# ---------------------------------------------------------------------------
# ApplyResult — frozen dataclass returned by every adapter method
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ApplyResult:
    """The outcome of an adapter capability invocation.

    Attributes:
        status:   Whether the action was applied, failed, or skipped.
        reason:   Human-readable explanation (especially for FAILED/SKIPPED).
        observed: Free-form adapter observations included in OutcomeReport.
    """

    status: ApplyStatus
    reason: str = ""
    observed: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def applied(cls, reason: str = "", **observed: Any) -> ApplyResult:
        return cls(status=ApplyStatus.APPLIED, reason=reason, observed=dict(observed))

    @classmethod
    def failed(cls, reason: str, **observed: Any) -> ApplyResult:
        return cls(status=ApplyStatus.FAILED, reason=reason, observed=dict(observed))

    @classmethod
    def skipped(cls, reason: str, **observed: Any) -> ApplyResult:
        return cls(status=ApplyStatus.SKIPPED, reason=reason, observed=dict(observed))


# ---------------------------------------------------------------------------
# SpanContext — what the dispatcher passes to every adapter method
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SpanContext:
    """Context passed from the dispatcher to each adapter method invocation.

    Attributes:
        trace_id:         OTel trace identifier.
        span_id:          OTel span identifier.
        framework:        Framework name (e.g. "langgraph", "openai_agents").
        framework_handle: The framework's native object (LangGraph state,
                          RunContext, etc.).  Typed loosely — the adapter
                          knows what to expect for its framework.
        logger:           Logger scoped to the dispatcher call site.
        attrs:            Span attributes forwarded for adapter use.
    """

    trace_id: str
    span_id: str
    framework: str
    framework_handle: Any
    logger: logging.Logger
    attrs: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# FrameworkAdapter ABC
# ---------------------------------------------------------------------------


class FrameworkAdapter(abc.ABC):
    """Abstract base class for framework adapters.

    Public entry point is :py:meth:`install` — gated by config.

    Subclasses MUST implement:
    - :py:meth:`_install_autonomous` — register the chain hook so this
      framework participates in autonomous interventions.
    - :py:meth:`capabilities` — declare which :class:`ActionType` values
      this adapter supports.
    - :py:meth:`apply` — enact a :class:`WorkflowIntervention`. Call-domain
      interventions produce their ``PostCallResult`` directly via
      ``CallIntervention.to_post_call_result`` and never reach this method.

    Subclasses MAY override:
    - :py:meth:`_install_tracing` — patch the framework so tracing events
      flow to a :class:`TraceEmitter`. Defaults to a no-op so adapters
      that don't yet support tracing keep working.

    Registration is done via the :func:`aigie.autonomous.adapters.register_adapter`
    decorator — see ``docs/adapter-matrix.md`` for the three-step contract.
    """

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def install(
        self,
        runtime: AutonomousRuntime | None = None,
        emitter: TraceEmitter | None = None,
    ) -> None:
        """Install everything this adapter contributes.

        Dispatches to :py:meth:`_install_autonomous` if a runtime is given
        and autonomous mode is enabled, and to :py:meth:`_install_tracing`
        if an emitter is given. Both surfaces are optional and independent.
        """
        if runtime is not None:
            cfg = getattr(runtime, "config", None)
            autonomous_cfg = getattr(cfg, "autonomous", None) if cfg is not None else None
            autonomous_on = (
                bool(getattr(autonomous_cfg, "enabled", False))
                if autonomous_cfg is not None
                else bool(getattr(runtime, "enabled", False))
            )
            if autonomous_on:
                self._install_autonomous(runtime)

        if emitter is not None:
            self._install_tracing(emitter)

    def _install_tracing(self, emitter: TraceEmitter) -> None:
        """Patch the framework so it emits typed tracing events to *emitter*.

        Default: no-op. Override to wire framework callbacks/hooks that
        publish via :py:meth:`TraceEmitter.emit_span_create` and friends.
        """
        return

    def _uninstall_tracing(self) -> None:
        """Reverse :py:meth:`_install_tracing`. Default: no-op."""
        return

    # ------------------------------------------------------------------
    # Per-invocation callback registration (optional override)
    # ------------------------------------------------------------------

    def register_callback(self, callback: Any, framework_config: Any) -> None:
        """Wire ``callback`` into the framework so it receives events for one run.

        Called by the lifecycle bridge inside ``_before_run``. Each framework
        maps this to its native registration idiom:
          - LangGraph/LangChain: append to ``config["callbacks"]``
          - CrewAI: ``crew.callbacks.append(callback)``
          - OpenAI Agents: ``Runner.add_tracer(callback)``

        Default: no-op. Adapters whose framework has no per-invocation
        callback registration concept can leave this as-is.
        """
        return

    def is_aigie_callback_already_registered(self, framework_config: Any) -> bool:
        """True if an Aigie callback is already wired into ``framework_config``.

        Used by the lifecycle bridge to short-circuit subgraph/sub-agent
        re-entry — if the parent run already registered our callback, we
        don't create a second trace for the inner invocation. Default:
        False (most adapters override when they implement register_callback).
        """
        return False

    def event_classifier(self) -> Any:
        """Return the framework's event classifier (a FrameworkEventClassifier).

        Used by L3 callbacks to dispatch raw framework events into canonical
        EventKind values. Default: None — frameworks that don't need
        classification (e.g. raw HTTP wrappers) can leave this. Frameworks
        with stacked filter rules MUST override and return a singleton.
        """
        return None

    # ------------------------------------------------------------------
    # Required overrides
    # ------------------------------------------------------------------

    @abc.abstractmethod
    def _install_autonomous(self, runtime: AutonomousRuntime) -> None:
        """Register the autonomous chain hook into *runtime*.

        Most adapters call ``runtime.register_chain_hook(...)`` with a hook
        that ultimately routes through :func:`aigie.autonomous.dispatch.dispatch`.
        """

    @classmethod
    @abc.abstractmethod
    def capabilities(cls) -> frozenset[ActionType] | set[ActionType]:
        """Return the set of ActionTypes this adapter can handle."""

    @abc.abstractmethod
    def apply(
        self,
        intervention: WorkflowIntervention,
        ctx: SpanContext,
    ) -> ApplyResult:
        """Enact a workflow-domain intervention.

        Call-domain interventions never reach this method — they produce a
        ``PostCallResult`` synchronously via ``to_post_call_result``.
        """

    @abc.abstractmethod
    def extract_error(self, span: dict) -> KytteError | None:
        """Map a framework-native failure into a canonical :class:`KytteError`.

        Called by the tracing emitter's pre-send hook for every span dict
        whose ``status`` is ``"error"`` (or which carries a non-empty
        ``error`` field). Return ``None`` to skip enrichment (e.g., the
        adapter does not recognize the failure shape).

        REQUIRED for every framework adapter. The platform clusters and
        analyzes errors based on the returned blob — adapters that skip
        this method cannot have their failures clustered. The method is
        intentionally abstract: failing at class definition is the only
        reliable way to make sure no framework forgets to map its errors.

        Args:
            span: The span payload (dict shape that hits the wire) about
                to be emitted. Adapters must NOT mutate this dict; the
                emitter's hook is responsible for writing the result
                into ``span["metadata"]["error"]``.

        Returns:
            A :class:`KytteError` carrying the normalized error fields,
            or ``None`` if the adapter cannot classify this failure.
        """
