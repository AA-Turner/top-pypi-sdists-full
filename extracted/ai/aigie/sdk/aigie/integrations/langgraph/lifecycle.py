"""LangGraph-specific lifecycle binding.

Subclass of FrameworkLifecycleBridge that supplies the framework hooks
plus owns the StateGraph.compile monkey-patch. Replaces the entire
sdk/aigie/auto_instrument/langgraph.py module — its 735 lines are split
between this file and FrameworkLifecycleBridge (sdk/aigie/tracing/lifecycle.py).
"""

from __future__ import annotations

import contextlib
import functools
import logging
import re
from typing import TYPE_CHECKING, Any

from aigie.auto_instrument._callback_utils import normalize_callbacks
from aigie.auto_instrument.trace import get_or_create_trace, get_or_create_trace_sync
from aigie.context_manager import merge_metadata
from aigie.integrations.langgraph.native_callback import LangGraphNativeCallback
from aigie.integrations.langgraph.utils import extract_reasoning_plan
from aigie.tracing.callback_lifecycle import CallbackLifecycle
from aigie.tracing.lifecycle import FrameworkLifecycleBridge
from aigie.tracing.reasoning_plan import ReasoningPlan
from aigie.tracing.trace_state import (
    _dec_thread_counter,
    _inc_thread_counter,
    get_resumed_trace,
    is_inside_traced_run,
    pop_resumable_trace,
    register_resumable_trace,
)

if TYPE_CHECKING:
    from aigie.tracing.emitter import TraceEmitter

logger = logging.getLogger(__name__)


_GENERIC_SCHEMA_NAMES = frozenset(
    {"dict", "Dict", "TypedDict", "State", "str", "int", "list", "bool", "float", "NoneType"}
)


def _is_aigie_callback(cb: object) -> bool:
    """Detect any Aigie-injected callback handler regardless of its concrete
    class. Native LangGraph callbacks set ``_is_aigie_handler = True`` on the
    class; legacy ``AigieCallbackHandler`` is matched by MRO name walk so
    callback.py stays untouched.

    Strict ``is True`` check on the marker so MagicMocks (which auto-vivify
    attributes into truthy MagicMock instances) don't match.
    """
    if getattr(cb, "_is_aigie_handler", False) is True:
        return True
    return any(c.__name__ == "AigieCallbackHandler" for c in type(cb).__mro__)


class LangGraphLifecycle(FrameworkLifecycleBridge, CallbackLifecycle):
    framework_type = "langgraph"

    def __init__(
        self,
        emitter: TraceEmitter | None,
        adapter: Any = None,
        *,
        config: Any = None,
    ) -> None:
        CallbackLifecycle.__init__(self)
        self._emitter = emitter
        self._adapter = adapter  # set by LangGraphAdapter._install_tracing
        self._config = config
        self._current_workflow_name: str = "LangGraph Workflow"
        self._current_graph_schema: Any = None

    def _zero_retention_from_handler(self) -> bool:
        cfg = self._config
        return bool(cfg and getattr(cfg, "zero_retention", False))

    # ---- Framework hooks --------------------------------------------------

    def _is_controlled_pause(self, error: Exception | None) -> bool:
        if error is None:
            return False
        try:
            from langgraph.errors import GraphInterrupt

            return isinstance(error, GraphInterrupt)
        except ImportError:
            return False

    def _extract_thread_id(self, config: dict | None) -> str | None:
        if not config or not isinstance(config, dict):
            return None
        cfg = config.get("configurable")
        if isinstance(cfg, dict):
            tid = cfg.get("thread_id")
            return None if tid is None else str(tid)
        return None

    def _extract_workflow_name(
        self, input: Any, schema: Any = None, *, graph_schema: Any = None
    ) -> str:
        # ``graph_schema=`` is an alias kept for tests written against the
        # pre-rewrite function signature.
        if schema is None and graph_schema is not None:
            schema = graph_schema
        if isinstance(input, dict):
            meta = input.get("metadata", {})
            if isinstance(meta, dict):
                if meta.get("workflow_name"):
                    return str(meta["workflow_name"])
                if meta.get("workflow_type"):
                    wt = str(meta["workflow_type"])
                    return wt if wt.endswith("_workflow") else f"{wt}_workflow"
                if meta.get("use_case"):
                    return f"{meta['use_case']}_workflow"

        schema = schema if schema is not None else self._current_graph_schema
        if (
            schema is not None
            and isinstance(schema, type)
            and schema.__name__ not in _GENERIC_SCHEMA_NAMES
        ):
            snake = re.sub(r"(?<!^)(?=[A-Z])", "_", schema.__name__).lower()
            if snake.endswith("_state"):
                snake = snake[:-6]
            if snake:
                return f"{snake}_workflow"

        return "LangGraph Workflow"

    def _graph_is_done(self, framework_handle: Any, config: dict | None) -> bool:
        try:
            state = framework_handle.get_state(config) if config else None
            next_nodes = getattr(state, "next", None) if state is not None else None
            return not next_nodes
        except Exception:  # noqa: BLE001
            return True

    def _already_tracing(self, config: dict | None) -> bool:
        # Prefer adapter delegation (canonical path). Fall back to inline scan
        # for test paths constructing LangGraphLifecycle without install().
        if config:
            if self._adapter is not None:
                if self._adapter.is_aigie_callback_already_registered(config):
                    return True
            elif any(_is_aigie_callback(cb) for cb in normalize_callbacks(config)):
                return True
        return is_inside_traced_run()

    def _make_handler(self, trace_id: str) -> Any:
        classifier = self._adapter.event_classifier() if self._adapter is not None else None
        return LangGraphNativeCallback(
            emitter=self._emitter,
            workflow_name=self._current_workflow_name,
            classifier=classifier,
            config=self._config,
        )

    _PLAN_CACHE_ATTR = "_aigie_reasoning_plan"

    def extract_reasoning_plan(self, framework_handle: Any) -> ReasoningPlan | None:
        """Return the static plan for the compiled LangGraph app being invoked.

        Memoized on the compiled app via ``_aigie_reasoning_plan`` — the
        topology of a compiled graph never changes, so we walk it at most
        once per app instance regardless of invocation count.
        """
        cached = getattr(framework_handle, self._PLAN_CACHE_ATTR, None)
        if cached is not None:
            return cached if isinstance(cached, ReasoningPlan) else None

        # CompiledStateGraph exposes the source StateGraph as .builder; that's
        # where the user-supplied node specs (with `.runnable`) live.
        source = getattr(framework_handle, "builder", framework_handle)
        try:
            plan = extract_reasoning_plan(source)
        except Exception as e:  # noqa: BLE001
            logger.debug(f"extract_reasoning_plan failed: {e}")
            return None
        result: ReasoningPlan | None = (
            None if (plan.node_count == 0 and plan.agent_prompt is None) else plan
        )
        with contextlib.suppress(AttributeError, TypeError):
            setattr(framework_handle, self._PLAN_CACHE_ATTR, result if result else False)
        return result

    def _create_trace_sync(self, *, name: str, metadata: dict[str, Any]) -> Any:
        self._current_workflow_name = name
        # Reuse an existing trace for this LangGraph thread (e.g. resume
        # after interrupt) so multi-call runs land in one trace.
        thread_id = metadata.get("thread_id") if metadata else None
        existing = get_resumed_trace(thread_id) if thread_id else None
        if existing is not None:
            return existing
        trace = get_or_create_trace_sync(name=name, metadata=merge_metadata(metadata))
        if thread_id:
            register_resumable_trace(thread_id, trace)
        return trace

    async def _create_trace(self, *, name: str, metadata: dict[str, Any]) -> Any:
        self._current_workflow_name = name
        thread_id = metadata.get("thread_id") if metadata else None
        existing = get_resumed_trace(thread_id) if thread_id else None
        if existing is not None:
            return existing
        trace = await get_or_create_trace(name=name, metadata=merge_metadata(metadata))
        if thread_id:
            register_resumable_trace(thread_id, trace)
        return trace

    # ---- Workflow-span integration (uses the L2 _before_run/_after_run) ---

    def _before_run(self, handler: Any, input: Any, config: dict | None) -> None:
        handler.open_workflow_span(input=input)
        if config is not None and self._adapter is not None:
            self._adapter.register_callback(handler, config)
        # Thread-counter is a fallback for raw-thread code paths where the
        # ambient ContextVar doesn't propagate (e.g. LangChain dispatching
        # callbacks from a threadpool without copy_context).
        _inc_thread_counter()

    def _after_run(
        self, handler: Any, input: Any, config: dict | None, error: Exception | None
    ) -> None:
        try:
            handler.close_workflow_span(error=error)
        finally:
            _dec_thread_counter()

    def _finalize(
        self,
        framework_handle: Any,
        config: dict | None,
        handler: Any,
        error: Exception | None,
    ) -> None:
        """Pause cases still need the substrate's paused-status emit; final
        cases (success/error) are handled by _after_run via close_workflow_span
        + finalize, so we skip the close_trace emit here to avoid emitting two
        trace_update events.

        On graph-done we also evict the resume-registry entry for this thread
        so long-running services don't accumulate Trace objects indefinitely.
        """
        if self._is_controlled_pause(error):
            handler.spans.close_pending_spans(status="paused")
            return
        if not self._graph_is_done(framework_handle, config) and error is None:
            handler.spans.close_pending_spans(status="paused")
            return
        pop_resumable_trace(self._extract_thread_id(config))

    # ---- StateGraph.compile patcher --------------------------------------

    def _install_native_hook(self) -> bool:
        """Patch StateGraph.compile so every compiled app gets wrapped."""
        try:
            from langgraph.graph import StateGraph
        except ImportError:
            return False

        if getattr(StateGraph.compile, "_aigie_patched", False):
            return True

        original_compile = StateGraph.compile
        lifecycle = self

        @functools.wraps(original_compile)
        def traced_compile(graph_self: Any, **kwargs: Any) -> Any:
            app = original_compile(graph_self, **kwargs)
            lifecycle._capture_schema(graph_self)
            lifecycle._wrap_compiled_app(app)
            return app

        traced_compile._aigie_patched = True  # type: ignore[attr-defined]
        StateGraph.compile = traced_compile  # type: ignore[assignment]

        _install_prebuilt_prompt_capture()
        return True

    def _uninstall_native_hook(self) -> None:
        """Best-effort: StateGraph.compile patches are not reversed in
        production. Tests rely on idempotency rather than reversal."""

    def _capture_schema(self, graph: Any) -> None:
        for attr in ("schema", "_schema"):
            cls = getattr(graph, attr, None)
            if isinstance(cls, type) and cls not in (dict, str, int, list, bool, float):
                self._current_graph_schema = cls
                return
        schemas = getattr(graph, "schemas", None)
        if isinstance(schemas, dict):
            for cls in schemas:
                if isinstance(cls, type) and cls not in (dict, str, int, list, bool, float):
                    self._current_graph_schema = cls
                    return

    def _wrap_compiled_app(self, app: Any) -> None:
        if hasattr(app, "invoke") and not getattr(app.invoke, "_aigie_patched", False):
            w = self.wrap_sync(framework_handle=app, original=app.invoke)
            w._aigie_patched = True  # type: ignore[attr-defined]
            app.invoke = w
        if hasattr(app, "ainvoke") and not getattr(app.ainvoke, "_aigie_patched", False):
            w_a = self.wrap_async(framework_handle=app, original=app.ainvoke)
            w_a._aigie_patched = True  # type: ignore[attr-defined]
            app.ainvoke = w_a
        if hasattr(app, "stream") and not getattr(app.stream, "_aigie_patched", False):
            w_s = self.wrap_stream_sync(framework_handle=app, original=app.stream)
            w_s._aigie_patched = True  # type: ignore[attr-defined]
            app.stream = w_s
        if hasattr(app, "astream") and not getattr(app.astream, "_aigie_patched", False):
            w_as = self.wrap_stream_async(framework_handle=app, original=app.astream)
            w_as._aigie_patched = True  # type: ignore[attr-defined]
            app.astream = w_as


def _wrap_prebuilt_factory(module: Any, attr: str, prompt_kwargs: tuple[str, ...]) -> None:
    """Wrap a prebuilt agent factory so its `prompt`/`system_prompt` lands on the result."""
    original = getattr(module, attr, None)
    if original is None or getattr(original, "_aigie_prompt_capture", False):
        return

    @functools.wraps(original)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        prompt_val: Any = None
        for key in prompt_kwargs:
            if key in kwargs and isinstance(kwargs[key], str) and kwargs[key]:
                prompt_val = kwargs[key]
                break
        app = original(*args, **kwargs)
        if prompt_val and app is not None:
            with contextlib.suppress(AttributeError, TypeError):
                app._aigie_static_prompt = prompt_val  # type: ignore[attr-defined]
        return app

    wrapper._aigie_prompt_capture = True  # type: ignore[attr-defined]
    setattr(module, attr, wrapper)


def _install_prebuilt_prompt_capture() -> None:
    """Patch create_react_agent / langchain.agents.create_agent to stamp the
    static `prompt`/`system_prompt` kwarg onto the returned CompiledStateGraph
    as ``_aigie_static_prompt``. Idempotent and silent on import failure."""
    _prebuilt: Any
    try:
        import langgraph.prebuilt as _prebuilt
    except ImportError:
        _prebuilt = None
    if _prebuilt is not None and hasattr(_prebuilt, "create_react_agent"):
        _wrap_prebuilt_factory(_prebuilt, "create_react_agent", ("prompt", "system_prompt"))

    _lc_agents: Any
    try:
        import langchain.agents as _lc_agents
    except ImportError:
        _lc_agents = None
    if _lc_agents is not None and hasattr(_lc_agents, "create_agent"):
        _wrap_prebuilt_factory(_lc_agents, "create_agent", ("system_prompt", "prompt"))


def install_langgraph_patches() -> None:
    """Module-level entry point matching the registry's ``patch_function`` shape."""
    LangGraphLifecycle(emitter=None).install()
