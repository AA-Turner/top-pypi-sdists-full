"""LangGraph FrameworkAdapter.

Registers as framework="langgraph". Owns both halves of the SDK's
LangGraph integration surface:

- Autonomous: chain-hook registration (`_install_autonomous`), capability
  declaration (`capabilities`), and WorkflowIntervention application
  (`apply` dispatches by action_type).
- Tracing: framework patching (`_install_tracing`) so LangGraph workflows
  emit events to the platform via a `TraceEmitter`.

A single class per framework owns both surfaces.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, ClassVar

from aigie.auto_instrument._callback_utils import _safe_add_callback, normalize_callbacks
from aigie.autonomous.adapters import (
    ActionType,
    ApplyResult,
    ApplyStatus,
    FrameworkAdapter,
    SpanContext,
    register_adapter,
)
from aigie.integrations.langgraph.error_conversion import to_kytte_error
from aigie.integrations.langgraph.event_classifier import LangGraphEventClassifier
from aigie.integrations.langgraph.lifecycle import LangGraphLifecycle, _is_aigie_callback
from aigie.tracing.error_enricher import KytteErrorEnricher
from aigie.tracing.errors import KytteError

if TYPE_CHECKING:
    from aigie.autonomous.interventions.base import WorkflowIntervention
    from aigie.autonomous.runtime import AutonomousRuntime
    from aigie.tracing.emitter import TraceEmitter

# ---------------------------------------------------------------------------
# Optional langchain_core import — graceful degradation to plain dicts
# ---------------------------------------------------------------------------

try:
    from langchain_core.messages import HumanMessage, SystemMessage
except ImportError:
    SystemMessage = None  # type: ignore[assignment,misc]
    HumanMessage = None  # type: ignore[assignment,misc]

_log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Break-loop sentinel exception (sets state flag; graph interrupt wiring is integration work)
# ---------------------------------------------------------------------------


class LangGraphBreakLoop(RuntimeError):
    """Raised to signal an agent loop break via autonomous v2 directive."""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_state(ctx: SpanContext) -> Any:
    """Return the framework_handle dict-like state object."""
    return ctx.framework_handle


def _state_set(state: Any, key: str, value: Any) -> bool:
    """Set key on state; return True if successful."""
    try:
        state[key] = value
        return True
    except (TypeError, KeyError, AttributeError):
        return False


def _apply_tool_overrides(messages: list[Any], overrides: dict[str, str]) -> bool:
    """Apply overrides to the last message's tool_calls; return True if applied."""
    if not messages:
        return False
    last = messages[-1]
    tool_calls = getattr(last, "tool_calls", None)
    if tool_calls is None and isinstance(last, dict):
        tool_calls = last.get("tool_calls")
    if not tool_calls:
        return False
    for tc in tool_calls:
        args = tc.get("args") if isinstance(tc, dict) else getattr(tc, "args", None)
        if isinstance(args, dict):
            args.update(overrides)
    return True


# ---------------------------------------------------------------------------
# LangGraphAdapter
# ---------------------------------------------------------------------------


@register_adapter(framework="langgraph")
class LangGraphAdapter(FrameworkAdapter):
    """FrameworkAdapter for LangGraph state-machine agents.

    Operates on the LangGraph state dict passed as ``ctx.framework_handle``.
    All methods degrade gracefully when the state shape is unexpected.
    """

    # ------------------------------------------------------------------
    # Generic FrameworkAdapter interface
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()
        self._emitter: TraceEmitter | None = None
        self._lifecycle: LangGraphLifecycle | None = None

    def extract_error(self, span: dict) -> KytteError | None:
        """Map a LangGraph failure dict to the canonical :class:`KytteError`.

        Delegates to :func:`to_kytte_error`; the adapter is the registered
        entry point so :class:`FrameworkAdapter`'s abstract contract is
        satisfied, but the actual mapping rules live in the conversion
        helper module.
        """
        return to_kytte_error(span)

    def _install_autonomous(self, runtime: AutonomousRuntime) -> None:
        """Register the autonomous chain hook so LangGraph LLM calls participate."""
        # Lazy: aigie.autonomous.dispatch transitively depends on the SDK's
        # client/runtime layer that imports this adapter; top-level would
        # cycle. Kept in-function deliberately.
        from aigie.autonomous.dispatch import make_chain_hook

        hook = make_chain_hook(runtime)
        runtime.register_chain_hook(hook, priority=10, name="autonomous_dispatch")

    def _install_tracing(self, emitter: TraceEmitter) -> None:
        """Install LangGraph tracing through the native callback substrate.

        Registers ``KytteErrorEnricher`` as the canonical post-emit hook
        that produces ``metadata.error``, then installs
        ``LangGraphLifecycle`` which monkey-patches ``StateGraph.compile``
        so every compiled workflow runs through ``LangGraphNativeCallback``.
        """
        self._emitter = emitter
        emitter.register_span_complete_hook(KytteErrorEnricher(self.extract_error))
        self._lifecycle = LangGraphLifecycle(emitter=emitter, adapter=self)
        self._lifecycle.install()

    def _uninstall_tracing(self) -> None:
        """Drop the stored emitter. Monkey-patches applied by
        ``LangGraphLifecycle.install()`` are idempotent and not reversible
        here — production code never uninstalls.
        """
        self._lifecycle = None
        self._emitter = None

    # ------------------------------------------------------------------
    # Per-invocation callback registration (FrameworkAdapter overrides)
    # ------------------------------------------------------------------

    def register_callback(self, callback: Any, framework_config: Any) -> None:
        """Inject ``callback`` into LangGraph's per-invocation callbacks list.

        LangGraph/LangChain dispatch events only to callbacks present in
        ``config["callbacks"]``; without this registration, the framework
        runs but our callback receives zero events. ``_safe_add_callback``
        handles the three shapes ``config["callbacks"]`` can take (list,
        AsyncCallbackManager, CallbackManager).
        """
        if framework_config is None:
            return
        _safe_add_callback(framework_config, callback)

    def is_aigie_callback_already_registered(self, framework_config: Any) -> bool:
        """True if a LangGraphNativeCallback (or legacy AigieCallbackHandler)
        is already wired into ``framework_config["callbacks"]``."""
        return any(_is_aigie_callback(cb) for cb in normalize_callbacks(framework_config))

    _classifier: Any = None

    def event_classifier(self) -> Any:
        """Return the singleton LangGraphEventClassifier for this adapter.
        Used by LangGraphNativeCallback to dispatch raw events into kinds.
        """
        if self._classifier is None:
            self._classifier = LangGraphEventClassifier()
        return self._classifier

    _CAPABILITIES: ClassVar[frozenset[ActionType]] = frozenset(
        {
            ActionType.IN_STEP_RETRY,
            ActionType.NEXT_STEP_INJECT_MESSAGE,
            ActionType.TRAJECTORY_REWRITE_OUTPUT,
            ActionType.TRAJECTORY_FORCE_FALLBACK,
            ActionType.TRAJECTORY_BREAK_LOOP,
            ActionType.IN_STEP_REWRITE_ARGS,
        }
    )

    @classmethod
    def capabilities(cls) -> frozenset[ActionType]:
        """All action types this adapter can handle.

        Includes IN_STEP_RETRY (call-domain, handled inline by
        RetryIntervention.to_post_call_result) plus the workflow-domain
        actions implemented below.
        """
        return cls._CAPABILITIES

    def apply(
        self,
        intervention: WorkflowIntervention,
        ctx: SpanContext,
    ) -> ApplyResult:
        """Dispatch a WorkflowIntervention to the matching capability method.

        Call-domain interventions (RetryIntervention) never reach this
        method — they produce a PostCallResult synchronously upstream.
        """
        action = intervention.action_type
        params = intervention.action_params

        if action == ActionType.NEXT_STEP_INJECT_MESSAGE:
            return self.inject_next_message(
                ctx, role=params.get("role", "system"), content=params.get("content", "")
            )
        if action == ActionType.TRAJECTORY_REWRITE_OUTPUT:
            return self.rewrite_span_output(ctx, output=params.get("output", ""))
        if action == ActionType.TRAJECTORY_FORCE_FALLBACK:
            return self.force_fallback_model(ctx, model=params.get("model", ""))
        if action == ActionType.TRAJECTORY_BREAK_LOOP:
            return self.break_loop(ctx, reason=params.get("reason", ""))
        if action == ActionType.IN_STEP_REWRITE_ARGS:
            return self.rewrite_tool_args(ctx, overrides=params.get("args_overrides", {}))
        return ApplyResult.skipped(reason=f"unsupported_action:{action.name}")

    # ------------------------------------------------------------------
    # inject_next_message
    # ------------------------------------------------------------------

    def inject_next_message(self, ctx: SpanContext, role: str, content: str) -> ApplyResult:
        """Append a message to the LangGraph state messages list."""
        try:
            state = _get_state(ctx)
            if state is None:
                raise ValueError("framework_handle is None")

            if HumanMessage is not None and SystemMessage is not None:
                msg: Any = (
                    SystemMessage(content=content)
                    if role == "system"
                    else HumanMessage(content=content)
                )
            else:
                msg = {"role": role, "content": content}

            messages = state.get("messages", []) if hasattr(state, "get") else state["messages"]
            messages = list(messages)
            messages.append(msg)
            _state_set(state, "messages", messages)

            ctx.logger.info(
                "LangGraphAdapter.inject_next_message: appended role=%s to messages", role
            )
            return ApplyResult(status=ApplyStatus.APPLIED, observed={"message_appended": True})
        except Exception as exc:
            return ApplyResult(
                status=ApplyStatus.FAILED,
                reason=f"{type(exc).__name__}: {exc}",
                observed={},
            )

    # ------------------------------------------------------------------
    # rewrite_span_output
    # ------------------------------------------------------------------

    def rewrite_span_output(self, ctx: SpanContext, output: str) -> ApplyResult:
        """Set the output field on state or attach to attrs as side channel."""
        try:
            state = _get_state(ctx)
            if state is not None and _state_set(state, "output", output):
                ctx.logger.info("LangGraphAdapter.rewrite_span_output: set state['output']")
            else:
                ctx.attrs["_directive_output_rewrite"] = output
                ctx.logger.info(
                    "LangGraphAdapter.rewrite_span_output: attached to ctx.attrs (state unavailable)"
                )
            return ApplyResult(status=ApplyStatus.APPLIED, observed={"output_rewritten": True})
        except Exception as exc:
            return ApplyResult(
                status=ApplyStatus.FAILED,
                reason=f"{type(exc).__name__}: {exc}",
                observed={},
            )

    # ------------------------------------------------------------------
    # force_fallback_model
    # ------------------------------------------------------------------

    def force_fallback_model(self, ctx: SpanContext, model: str) -> ApplyResult:
        """Set the model field on state or attach to attrs as side channel."""
        try:
            state = _get_state(ctx)
            if state is not None and _state_set(state, "model", model):
                ctx.logger.info(
                    "LangGraphAdapter.force_fallback_model: set state['model']=%s", model
                )
            else:
                ctx.attrs["_directive_fallback_model"] = model
                ctx.logger.info(
                    "LangGraphAdapter.force_fallback_model: attached to ctx.attrs (state unavailable)"
                )
            return ApplyResult(status=ApplyStatus.APPLIED, observed={"model_override": model})
        except Exception as exc:
            return ApplyResult(
                status=ApplyStatus.FAILED,
                reason=f"{type(exc).__name__}: {exc}",
                observed={},
            )

    # ------------------------------------------------------------------
    # break_loop
    # ------------------------------------------------------------------

    def break_loop(self, ctx: SpanContext, reason: str) -> ApplyResult:
        """Signal an agent loop break by setting a state flag."""
        try:
            state = _get_state(ctx)
            if state is not None:
                _state_set(state, "__break_loop__", True)
            ctx.logger.info(
                "LangGraphAdapter.break_loop: agent loop break requested via autonomous v2 directive"
                " (reason=%s); state flag set, graph interrupt wired in P11",
                reason,
            )
            return ApplyResult(
                status=ApplyStatus.APPLIED, observed={"break_loop_flag": True, "reason": reason}
            )
        except Exception as exc:
            return ApplyResult(
                status=ApplyStatus.FAILED,
                reason=f"{type(exc).__name__}: {exc}",
                observed={},
            )

    # ------------------------------------------------------------------
    # rewrite_tool_args
    # ------------------------------------------------------------------

    def rewrite_tool_args(self, ctx: SpanContext, overrides: dict[str, str]) -> ApplyResult:
        """Apply overrides to the last AIMessage's tool_calls in state."""
        try:
            state = _get_state(ctx)
            if state is None:
                raise ValueError("framework_handle is None")
            messages = state.get("messages", []) if hasattr(state, "get") else state["messages"]
            applied_via_state = _apply_tool_overrides(messages, overrides)
            if not applied_via_state:
                ctx.attrs["_directive_tool_arg_overrides"] = overrides
            ctx.logger.info(
                "LangGraphAdapter.rewrite_tool_args: applied overrides=%r via_state=%s",
                list(overrides.keys()),
                applied_via_state,
            )
            return ApplyResult(
                status=ApplyStatus.APPLIED,
                observed={"overrides_applied": True, "via_state": applied_via_state},
            )
        except Exception as exc:
            return ApplyResult(
                status=ApplyStatus.FAILED,
                reason=f"{type(exc).__name__}: {exc}",
                observed={},
            )
