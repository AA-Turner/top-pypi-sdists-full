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
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from aigie.auto_instrument._callback_utils import normalize_callbacks
from aigie.auto_instrument.trace import get_or_create_trace, get_or_create_trace_sync
from aigie.context_manager import merge_metadata
from aigie.decision.tool_catalog import bind_trace_hash
from aigie.integrations.langgraph.control_flow import is_control_flow_signal
from aigie.integrations.langgraph.native_callback import LangGraphNativeCallback
from aigie.integrations.langgraph.rewind import LangGraphRewindCapability
from aigie.integrations.langgraph.tool_catalog import register_graph_tools, stashed_hash
from aigie.integrations.langgraph.utils import extract_reasoning_plan
from aigie.rewind.coordinator import RewindCoordinator
from aigie.tracing.callback_lifecycle import CallbackLifecycle
from aigie.tracing.lifecycle import FrameworkLifecycleBridge
from aigie.tracing.reasoning_plan import ReasoningPlan
from aigie.tracing.trace_state import (
    _dec_thread_counter,
    _inc_thread_counter,
    current_trace_id,
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


@dataclass(frozen=True)
class _RewindHook:
    coordinator: RewindCoordinator
    capability: LangGraphRewindCapability
    app: Any
    config: dict | None


def _is_aigie_callback(cb: object) -> bool:
    """Detect any Aigie-injected callback handler regardless of its concrete
    class. Aigie native callbacks (LangGraph / LangChain) set
    ``_is_aigie_handler = True`` on the class.

    Strict ``is True`` check on the marker so MagicMocks (which auto-vivify
    attributes into truthy MagicMock instances) don't match.
    """
    return getattr(cb, "_is_aigie_handler", False) is True


class LangGraphLifecycle(FrameworkLifecycleBridge, CallbackLifecycle):
    framework_type = "langgraph"

    def __init__(
        self,
        emitter: TraceEmitter | None,
        adapter: Any = None,
        *,
        config: Any = None,
        coordinator: RewindCoordinator | None = None,
    ) -> None:
        CallbackLifecycle.__init__(self)
        self._emitter = emitter
        self._adapter = adapter  # set by LangGraphAdapter._install_tracing
        self._config = config
        self._current_workflow_name: str = "LangGraph Workflow"
        self._current_graph_schema: Any = None
        self._coordinator = coordinator
        self._capability: LangGraphRewindCapability | None = None
        if coordinator is not None:
            self._capability = LangGraphRewindCapability()
            coordinator.register(self._capability)

    def _zero_retention_from_handler(self) -> bool:
        cfg = self._config
        return bool(cfg and getattr(cfg, "zero_retention", False))

    # ---- Framework hooks --------------------------------------------------

    def _is_controlled_pause(self, error: BaseException | None) -> bool:
        return is_control_flow_signal(error)

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

    def _make_handler(self, trace: Any) -> Any:
        classifier = self._adapter.event_classifier() if self._adapter is not None else None
        handler = LangGraphNativeCallback(
            emitter=self._emitter,
            workflow_name=self._current_workflow_name,
            classifier=classifier,
            config=self._config,
        )
        # Bound here, where the handler's type is known: a bridge-driven run
        # never opens a callback root, so this is its only chance to count into
        # the trace's tally rather than its own.
        handler.bind_trace_tally(trace, owns_trace=getattr(trace, "_aigie_minted", True))
        return handler

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

    def _before_run(
        self, handler: Any, framework_handle: Any, input: Any, config: dict | None
    ) -> None:
        handler.open_workflow_span(input=input)
        self._stamp_tool_catalog(handler, framework_handle)
        if config is not None and self._adapter is not None:
            self._adapter.register_callback(handler, config)
        self._synthesize_thread_id(framework_handle, config)
        self._arm_rewind(handler, framework_handle, config)
        # Thread-counter is a fallback for raw-thread code paths where the
        # ambient ContextVar doesn't propagate (e.g. LangChain dispatching
        # callbacks from a threadpool without copy_context).
        _inc_thread_counter()

    def _stamp_tool_catalog(self, handler: Any, framework_handle: Any) -> None:
        """Copy the compiled graph's tool hash onto this run."""
        catalog_hash = stashed_hash(framework_handle)
        if catalog_hash:
            handler._aigie_tool_registry_hash = catalog_hash
            bind_trace_hash(current_trace_id(), catalog_hash)

    def _synthesize_thread_id(self, app: Any, config: dict | None) -> None:
        """Add a per-invoke thread_id for Aigie-injected checkpointers."""
        if config is None or getattr(app, "_aigie_injected_checkpointer", None) is None:
            return
        if self._extract_thread_id(config):
            return
        configurable = config.get("configurable")
        configurable = dict(configurable) if isinstance(configurable, dict) else {}
        configurable["thread_id"] = uuid.uuid4().hex
        config["configurable"] = configurable

    def _arm_rewind(self, handler: Any, app: Any, config: dict | None) -> None:
        if self._coordinator is None or self._capability is None:
            return
        handler._aigie_rewind = _RewindHook(
            coordinator=self._coordinator,
            capability=self._capability,
            app=app,
            config=config,
        )

    def _after_run(
        self,
        handler: Any,
        input: Any,
        config: dict | None,
        error: BaseException | None,
        result: Any = None,
    ) -> None:
        try:
            if not self._is_controlled_pause(error):
                # A null root output lets a later span fill the gap.
                handler.close_workflow_span(output=result, error=error)
        finally:
            _dec_thread_counter()

    def _finalize(
        self,
        framework_handle: Any,
        config: dict | None,
        handler: Any,
        error: BaseException | None,
    ) -> None:
        """Pause cases still need the substrate's paused-status emit; final
        cases (success/error) are handled by _after_run via close_workflow_span
        + finalize, so we skip the close_trace emit here to avoid emitting two
        trace_update events.

        On graph-done we also evict the resume-registry entry for this thread
        so long-running services don't accumulate Trace objects indefinitely.
        """
        if self._is_controlled_pause(error) or (
            not self._graph_is_done(framework_handle, config) and error is None
        ):
            self._pause_and_clear(handler)
            return
        pop_resumable_trace(self._extract_thread_id(config))

    def _pause_and_clear(self, handler: Any) -> None:
        handler.spans.close_pending_spans(status="paused")
        handler.spans.clear_pending_spans()

    def _auto_checkpointer_for_rewind(self) -> bool:
        cfg = self._config
        return bool(cfg and getattr(cfg, "auto_checkpointer_for_rewind", False))

    def _inject_checkpointer(self, kwargs: dict[str, Any]) -> Any:
        """Inject MemorySaver only when the rewind auto-checkpointer flag is enabled."""
        if self._coordinator is None or not self._auto_checkpointer_for_rewind():
            return None
        if kwargs.get("checkpointer") is not None:
            return None
        try:
            from langgraph.checkpoint.memory import MemorySaver
        except ImportError:
            return None
        saver = MemorySaver()
        kwargs["checkpointer"] = saver
        return saver

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
            injected = lifecycle._inject_checkpointer(kwargs)
            app = original_compile(graph_self, **kwargs)
            if injected is not None:
                with contextlib.suppress(AttributeError, TypeError):
                    app._aigie_injected_checkpointer = injected  # type: ignore[attr-defined]
            lifecycle._capture_schema(graph_self)
            register_graph_tools(graph_self, app)
            lifecycle._wrap_compiled_app(app)
            return app

        traced_compile._aigie_patched = True  # type: ignore[attr-defined]
        StateGraph.compile = traced_compile  # type: ignore[assignment]

        _install_prebuilt_prompt_capture()
        self._patch_compiled_class()
        return True

    # batch/abatch are excluded: Runnable.batch fans out to invoke on a
    # threadpool the ambient trace doesn't reach, so wrapping the outer batch
    # opens duplicate roots on the pool threads (per-input invoke is traced).
    _CLS_SYNC = ("invoke",)
    _CLS_ASYNC = ("ainvoke",)
    _CLS_STREAM_SYNC = ("stream",)
    _CLS_STREAM_ASYNC = ("astream", "astream_events", "astream_log")

    def _patch_compiled_class(self) -> None:
        """Wrap the run entrypoints on ``CompiledStateGraph`` itself so a graph
        compiled before ``aigie.init()`` is still traced as langgraph rather
        than mislabeled by the LangChain callback. Nested calls stand down via
        ``_already_tracing()``; per-instance wraps shadow these (no double-wrap).
        """
        try:
            from langgraph.graph.state import CompiledStateGraph
        except ImportError:
            return
        for name in self._CLS_SYNC:
            self._patch_class_method(CompiledStateGraph, name, self.wrap_cls_sync)
        for name in self._CLS_ASYNC:
            self._patch_class_method(CompiledStateGraph, name, self.wrap_cls_async)
        for name in self._CLS_STREAM_SYNC:
            self._patch_class_method(CompiledStateGraph, name, self.wrap_cls_stream_sync)
        for name in self._CLS_STREAM_ASYNC:
            self._patch_class_method(CompiledStateGraph, name, self.wrap_cls_stream_async)

    @staticmethod
    def _patch_class_method(cls: type, name: str, wrap_factory: Any) -> None:
        original = getattr(cls, name, None)
        if original is None or getattr(original, "_aigie_patched", False):
            return
        wrapped = wrap_factory(original=original)
        wrapped._aigie_patched = True  # type: ignore[attr-defined]
        wrapped._aigie_was_own = name in cls.__dict__  # type: ignore[attr-defined]
        setattr(cls, name, wrapped)

    def _uninstall_native_hook(self) -> None:
        """Best-effort: StateGraph.compile patches are not reversed in
        production. Tests reverse both patches via ``unpatch_langgraph_compile``."""

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
    _prebuilt: Any = None
    try:
        import langgraph.prebuilt as _prebuilt  # type: ignore[no-redef]
    except ImportError:
        _prebuilt = None
    if _prebuilt is not None and hasattr(_prebuilt, "create_react_agent"):
        _wrap_prebuilt_factory(_prebuilt, "create_react_agent", ("prompt", "system_prompt"))

    _lc_agents: Any = None
    try:
        import langchain.agents as _lc_agents  # type: ignore[no-redef]
    except ImportError:
        _lc_agents = None
    if _lc_agents is not None and hasattr(_lc_agents, "create_agent"):
        _wrap_prebuilt_factory(_lc_agents, "create_agent", ("system_prompt", "prompt"))


def install_langgraph_patches() -> None:
    """Module-level entry point matching the registry's ``patch_function`` shape."""
    LangGraphLifecycle(emitter=None).install()
