"""
LangChain/LangGraph Callback Handler for Aigie.
"""

import asyncio
import contextlib
import logging
import os
import traceback
from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Any

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

from aigie._legacy_stubs import ErrorDetector, get_error_detector  # legacy autonomous-mode shim
from aigie.client import Aigie
from aigie.tracing.trace_state import deregister_open_span, register_open_span
from aigie.trace import TraceContext

# Optional error and drift detection imports
try:
    from aigie.integrations.langchain.drift_detection import DriftDetector
    from aigie.integrations.langchain.error_detection import ErrorDetector, get_error_detector

    HAS_DETECTION = True
except ImportError:
    HAS_DETECTION = False
    ErrorDetector = None
    DriftDetector = None
    get_error_detector = None

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    """Return current UTC time with timezone info for consistent timestamp handling."""
    return datetime.now(timezone.utc)


def _utc_now_iso() -> str:
    """Return current UTC time as ISO format string with timezone info."""
    return datetime.now(timezone.utc).isoformat()


# TODO(kyt-9-followup): this handler is still used by the `langchain`
# integration (sdk/aigie/integrations/langchain/). The LangGraph integration
# now uses _LangGraphCallback (sdk/aigie/integrations/langgraph/_callback.py)
# which subclasses this and routes emission through TraceEmitter. Migrate
# `langchain` onto a FrameworkAdapter + _LangChainCallback in a follow-up
# and remove this comment.
class AigieCallbackHandler(BaseCallbackHandler):
    """
    LangChain callback handler for automatic trace/span creation.

    Usage:
        aigie = Aigie()
        await aigie.initialize()

        # Pass trace context to callback
        async with aigie.trace("My Workflow") as trace:
            callback = AigieCallbackHandler(trace=trace)
            result = await chain.ainvoke(
                input,
                config={"callbacks": [callback]}
            )
    """

    def __init__(self, aigie: Aigie | None = None, trace: TraceContext | None = None):
        """
        Initialize callback handler.

        Args:
            aigie: Aigie client instance (optional if trace provided)
            trace: Active trace context (preferred - avoids async issues)
        """
        super().__init__()
        self.aigie = aigie
        self.trace = trace
        self.span_stack = []
        self._span_contexts = {}  # Map run_id to span context
        self._pending_trace_name = None
        self._pending_trace_metadata = None
        self._root_run_id = None  # Track root chain run_id for trace completion

        # LangGraph mode: when True, filter internal chains and use langgraph_node metadata
        self._langgraph_mode: bool = False
        self._workflow_name: str | None = None

        # Internal class names that are graph-level wrappers
        self._LANGGRAPH_GRAPH_NAMES = frozenset(
            {
                "LangGraph",
                "Pregel",
                "CompiledStateGraph",
                "CompiledGraph",
            }
        )

        # Execution path tracking for workflow execution data
        self._execution_paths: dict[str, list[str]] = {}  # trace_id -> [span_name, ...]
        self._execution_timing: dict[
            str, dict[str, dict[str, Any]]
        ] = {}  # trace_id -> {span_name: {start_time, end_time, duration_ms}}
        self._execution_status: dict[str, dict[str, str]] = {}  # trace_id -> {span_name: status}
        self._execution_errors: dict[
            str, dict[str, str]
        ] = {}  # trace_id -> {span_name: error_message}
        self._edge_conditions: dict[
            str, list[dict[str, Any]]
        ] = {}  # trace_id -> [{step, condition, result}]
        self._agent_iterations: dict[
            str, dict[str, int]
        ] = {}  # trace_id -> {agent_name: iteration_count}
        self._span_start_times: dict[
            str, dict[str, str]
        ] = {}  # trace_id -> {span_name: iso_timestamp}
        self._retry_info: dict[
            str, list[dict[str, Any]]
        ] = {}  # trace_id -> [{span_name, attempt, reason}]
        self._state_transitions: dict[
            str, list[dict[str, Any]]
        ] = {}  # trace_id -> [{from_state, to_state, trigger}]
        self._nested_workflows: dict[
            str, list[dict[str, Any]]
        ] = {}  # trace_id -> [{workflow_name, trace_id}]

        # Depth tracking for span hierarchy visualization
        self._span_depth_map: dict[str, int] = {}  # run_id -> depth level

        # Turn and call counting
        self._turn_count: int = 0
        self._total_tool_calls: int = 0

        # Agent plan tracking
        self._plan_sent: bool = False

        # LangGraph thread_id this handler is bound to (for trace stitching across
        # interrupt/resume). Set by the LangGraph auto-instrumentation wrapper.
        self._thread_id: str | None = None

        # Error and drift detection (optional)
        self._error_detector: ErrorDetector | None = None
        self._drift_detector: DriftDetector | None = None
        if HAS_DETECTION:
            self._error_detector = get_error_detector()
            self._drift_detector = DriftDetector()

    # ------------------------------------------------------------------
    # Emit seams — subclasses override to route through TraceEmitter etc.
    # Each takes the dict already built by the calling on_* handler.
    # Default: pushes directly to aigie._buffer.add_sync. Behavior must
    # stay byte-identical for langchain (which uses the default).
    # ------------------------------------------------------------------

    def _emit_span_create(self, aigie: Any, span_data: dict) -> None:
        # A span is built mutably in memory and emitted exactly once (finalized)
        # by _emit_span_update — no create event is sent. Register a finalize
        # callable so an unclean shutdown still ships the span as interrupted.
        span_id = span_data.get("id")
        if span_id:
            register_open_span(span_id, lambda: self._finalize_open_payload(span_data))

    @staticmethod
    def _finalize_open_payload(span_data: dict) -> dict:
        """Build a finalized payload from a create record for the shutdown drain.
        Status is overwritten to ``interrupted`` by the registry drain."""
        end = _utc_now()
        start_iso = span_data.get("start_time")
        duration_ns = 0
        if start_iso:
            with contextlib.suppress(Exception):
                duration_ns = int(
                    (end - datetime.fromisoformat(start_iso)).total_seconds() * 1_000_000_000
                )
        return {
            "id": span_data.get("id"),
            "trace_id": span_data.get("trace_id"),
            "parent_id": span_data.get("parent_id"),
            "name": span_data.get("name"),
            "type": span_data.get("type"),
            "input": span_data.get("input"),
            "metadata": span_data.get("metadata"),
            "status": "interrupted",
            "start_time": start_iso,
            "end_time": end.isoformat(),
            "duration_ns": duration_ns,
        }

    def _emit_span_update(self, aigie: Any, update_data: dict) -> None:
        span_id = update_data.get("id")
        if span_id:
            deregister_open_span(span_id)
        aigie._buffer.add_sync(update_data)

    def _emit_trace_update(self, aigie: Any, update_data: dict) -> None:
        # Trace identity now rides the root span (root.id == trace_id). A
        # finalization/pause payload (carries ``status``) becomes the root
        # SPAN_UPDATE; mid-run metadata-only updates (e.g. agent_plan) carried
        # no wire weight before — TRACE_UPDATE was dropped in transit — so they
        # are not re-introduced as judgeable spans here.
        if "status" not in update_data:
            return
        root = dict(update_data)
        root["parent_id"] = None
        root.setdefault("type", "workflow")
        aigie._buffer.add_sync(root)

    @staticmethod
    def _normalize_run_id(run_id) -> str:
        """Normalize run_id to string (LangChain may pass UUID objects)."""
        if run_id is None:
            return None
        return str(run_id)

    def _calculate_depth(self, run_id: str, parent_run_id: str | None) -> int:
        """Calculate the depth level for a span based on its parent hierarchy."""
        if not parent_run_id:
            # Root level span
            depth = 0
        elif parent_run_id in self._span_depth_map:
            # Parent depth + 1
            depth = self._span_depth_map[parent_run_id] + 1
        else:
            # Unknown parent, assume depth 1
            depth = 1

        # Store depth for this run_id
        self._span_depth_map[run_id] = depth
        return depth

    def _resolve_parent(self, parent_run_id: str | None) -> str | None:
        """Resolve parent span ID from LangChain's parent_run_id.

        Uses the run_id → span map (_span_contexts) to find the parent span.
        This is the universal pattern used by Langfuse, LangSmith, Braintrust.
        """
        if not parent_run_id:
            return None
        ctx = self._span_contexts.get(parent_run_id)
        if ctx:
            span = ctx["span"]
            if hasattr(span, "id") and span.id:
                return span.id
        return None

    def on_chain_start(
        self,
        serialized: dict[str, Any],
        inputs: dict[str, Any],
        *,
        run_id: str,
        parent_run_id: str | None = None,
        tags: list | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Called when a chain starts."""
        if getattr(self, "_paused", False):
            return
        import logging

        logger = logging.getLogger(__name__)

        # Normalize UUIDs to strings for consistent dictionary lookups
        run_id = self._normalize_run_id(run_id)
        parent_run_id = self._normalize_run_id(parent_run_id)

        # Extract LangGraph node information from tags and metadata
        langgraph_node = None
        langgraph_step = None

        # Check metadata for LangGraph node info
        if metadata and isinstance(metadata, dict):
            langgraph_node = (
                metadata.get("langgraph_node") or metadata.get("node") or metadata.get("graph_node")
            )
            langgraph_step = metadata.get("langgraph_step") or metadata.get("step")

        # Check tags for LangGraph patterns
        if tags and isinstance(tags, list):
            for tag in tags:
                if isinstance(tag, str):
                    if tag.startswith("graph:") or tag.startswith("langgraph:"):
                        parts = tag.split(":")
                        if len(parts) >= 3 and parts[1] == "step":
                            langgraph_node = langgraph_node or parts[2]
                    elif tag.startswith("seq:step:"):
                        with contextlib.suppress(ValueError, IndexError):
                            langgraph_step = langgraph_step or int(tag.split(":")[2])
                    elif tag.startswith("node:"):
                        langgraph_node = langgraph_node or tag.split(":", 1)[1]

        # Extract workflow metadata from LangChain config if available
        workflow_metadata = {}
        if metadata and isinstance(metadata, dict):
            workflow_type = metadata.get("workflow_type") or metadata.get("use_case")
            domain = metadata.get("domain")
            if workflow_type:
                workflow_metadata["workflow_type"] = workflow_type
            if domain:
                workflow_metadata["domain"] = domain

        # Store workflow metadata for later use
        if workflow_metadata:
            self._pending_trace_metadata = workflow_metadata

        # Extract chain name from LangChain's serialized dict (no hardcoding - pure extraction)
        def _get_chain_name(serialized: dict[str, Any] | None) -> str:
            # If serialized is None, we can't extract - return generic name
            if not serialized:
                return "chain_step"

            # Method 1: Extract from serialized["name"] (LangChain's primary identifier)
            name = serialized.get("name")
            if name and name not in ["chain", "Chain", "chain_step", ""]:
                return name

            # Method 2: Extract from serialized["id"] - LangChain's class path identifier
            # Format can be: ["langchain_core", "prompts", "chat", "ChatPromptTemplate"]
            # or: ["langchain", "chains", "llm", "LLMChain"]
            chain_id = serialized.get("id")
            if isinstance(chain_id, list) and chain_id:
                # Try each element in the id array (LangChain stores class path as array)
                for part in reversed(chain_id):  # Start from most specific (last element)
                    if isinstance(part, str):
                        # Extract class name from fully qualified path
                        if "." in part:
                            # Handle "langchain.chains.llm.LLMChain" format
                            parts = part.split(".")
                            class_name = parts[-1]
                        else:
                            # Handle just "LLMChain" format
                            class_name = part

                        # Return the class name if it's meaningful
                        if class_name and class_name not in [
                            "chain",
                            "Chain",
                            "chain_step",
                            "",
                            "chains",
                            "prompts",
                        ]:
                            return class_name

                # Fallback: use first element if nothing else worked
                if chain_id[0]:
                    return str(chain_id[0])
            elif isinstance(chain_id, str):
                # Handle string format: "langchain.chains.llm.LLMChain"
                if "." in chain_id:
                    parts = chain_id.split(".")
                    class_name = parts[-1]
                    if class_name and class_name not in ["chain", "Chain", "chain_step"]:
                        return class_name
                elif chain_id not in ["chain", "Chain", "chain_step"]:
                    return chain_id

            # Method 3: Try to get chain object from kwargs (if LangChain passes it)
            if kwargs:
                chain_obj = (
                    kwargs.get("chain") or kwargs.get("chain_instance") or kwargs.get("chain_obj")
                )
                if chain_obj:
                    # Extract class name from actual chain object
                    if hasattr(chain_obj, "__class__"):
                        class_name = chain_obj.__class__.__name__
                        if class_name and class_name not in ["Chain", "chain_step"]:
                            return class_name
                    # Or get name attribute if available
                    if hasattr(chain_obj, "name"):
                        obj_name = chain_obj.name
                        if obj_name and obj_name not in ["chain", "Chain", "chain_step"]:
                            return obj_name

            # Method 4: Check metadata for chain_class (set by our patched Chain methods)
            if metadata and isinstance(metadata, dict):
                chain_class = metadata.get("chain_class")
                if chain_class:
                    # Extract class name from full path if needed
                    class_name = chain_class.split(".")[-1] if "." in chain_class else chain_class
                    if class_name and class_name not in ["Chain", "chain_step"]:
                        return class_name

            # Method 5: Check serialized for _type or other identifying fields
            if "_type" in serialized:
                type_val = serialized["_type"]
                if type_val and type_val not in ["chain", "Chain", "chain_step"]:
                    return type_val

            # If we can't extract anything meaningful, return generic name
            return "chain_step"

        # If no trace provided, try to get one from auto-instrumentation
        if not self.trace:
            from aigie.auto_instrument.trace import get_current_trace

            self.trace = get_current_trace()

            # If still no trace and we have aigie, try to create one synchronously
            if not self.trace and self.aigie and self.aigie._initialized:
                try:
                    from aigie.auto_instrument.trace import get_or_create_trace_sync

                    chain_name = _get_chain_name(serialized)
                    # Try to create trace synchronously
                    trace = get_or_create_trace_sync(
                        name=chain_name, metadata={"type": "chain", "inputs": inputs}
                    )
                    if trace:
                        self.trace = trace
                except Exception as e:
                    # If sync creation fails, mark for async creation later
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.debug(f"Could not create trace synchronously: {e}")
                    pass

        if not self.trace:
            # Still no trace, can't create spans
            return

        # IMPORTANT: Set _current_trace so nested LLM calls inside workflow nodes
        # can find the parent trace via get_current_trace()
        # This is critical for proper trace nesting without requiring customer code changes
        from aigie.auto_instrument.trace import set_current_trace

        set_current_trace(self.trace)

        # Create span for this chain step
        chain_name = _get_chain_name(serialized)

        # Extract additional chain information for metadata
        chain_class = None
        chain_type = "chain"  # Default type

        if serialized:
            chain_id = serialized.get("id")
            if isinstance(chain_id, list) and chain_id:
                # Extract full class path
                chain_class = ".".join(str(p) for p in chain_id)
                # Extract class name
                if chain_id:
                    last_part = chain_id[-1]
                    if (isinstance(last_part, str) and "." in last_part) or isinstance(
                        last_part, str
                    ):
                        chain_class = last_part
            elif isinstance(chain_id, str):
                chain_class = chain_id

            # Try to infer chain type from name/class
            chain_name_lower = chain_name.lower()
            chain_class_lower = (chain_class or "").lower()

            # Detect workflow types (LangGraph)
            if (
                "stategraph" in chain_class_lower
                or "langgraph" in chain_class_lower
                or "workflow" in chain_name_lower
                or "graph" in chain_name_lower
            ):
                chain_type = "workflow"
            # Detect agent types
            elif (
                "agent" in chain_name_lower
                or "agentexecutor" in chain_class_lower
                or "react" in chain_class_lower
                or ("openai" in chain_class_lower and "agent" in chain_class_lower)
            ):
                chain_type = "agent"
            elif "prompt" in chain_name_lower or "template" in chain_name_lower:
                chain_type = "prompt"
            elif "llm" in chain_name_lower:
                chain_type = "llm"
            elif "sequential" in chain_name_lower:
                chain_type = "sequential"
            elif "router" in chain_name_lower:
                chain_type = "router"
            else:
                chain_type = "chain"

        # Use langgraph_node in span name if available for better workflow visualization
        if langgraph_node:
            span_name = f"{langgraph_node} ({chain_name})"
            # If we have a langgraph node, this is part of a workflow
            if chain_type == "chain":
                chain_type = "workflow"
        else:
            span_name = chain_name

        # --- Parent resolution (single path for all modes) ---
        parent_span_id = self._resolve_parent(parent_run_id)

        # --- LangGraph mode: filter noise and enrich span names ---
        if self._langgraph_mode:
            name = kwargs.get("name") or (serialized.get("name", "") if serialized else "")

            # Skip chains tagged as hidden by LangGraph
            if tags and "langsmith:hidden" in tags:
                return
            # Skip internal LangGraph machinery by prefix (ChannelWrite<...>, ChannelRead<...>)
            # and exact match (__start__, __end__)
            if any(name.startswith(skip) for skip in ("ChannelWrite", "ChannelRead")) or name in (
                "__start__",
                "__end__",
            ):
                return

            # Detect span type from LangGraph metadata
            langgraph_node = (metadata or {}).get("langgraph_node")
            if name in self._LANGGRAPH_GRAPH_NAMES or (not parent_run_id):
                # Graph-level wrapper
                span_name = self._workflow_name or name or "LangGraph"
                chain_type = "workflow"
            elif langgraph_node and name == langgraph_node:
                span_name = langgraph_node
                chain_type = "chain"
            else:
                span_name = name or "chain_step"
                chain_type = "chain"

        span = self.trace.span(
            name=span_name,
            type=chain_type,  # Use detected type (workflow, agent, chain, etc.)
            parent=parent_span_id,
        )

        # Set process-level span ID synchronously for OTel bridge.
        # span.id is pre-generated in __init__ — available immediately.
        try:
            from aigie.auto_instrument.span_enricher import set_active_span_id

            set_active_span_id(span.id)
        except Exception:
            pass

        logger.debug(
            f"Created span: {span_name}, id={span.id[:8]}, parent={parent_span_id[:8] if parent_span_id else 'None'}"
        )

        # Set enriched metadata including LangGraph info
        if hasattr(span, "set_metadata"):
            span_metadata = {}
            if chain_class:
                span_metadata["chain_class"] = chain_class
            if chain_type:
                span_metadata["chain_type"] = chain_type
            # Add LangGraph metadata for workflow definition extraction
            if langgraph_node:
                span_metadata["langgraph_node"] = langgraph_node
            if langgraph_step is not None:
                span_metadata["langgraph_step"] = langgraph_step
            # Graph node parent tracking for DAG visualization (OpenInference convention)
            if langgraph_node:
                span_metadata["graph_node_id"] = run_id
                span_metadata["graph_node_name"] = langgraph_node
                if parent_run_id:
                    span_metadata["graph_parent_node_id"] = parent_run_id
            if span_metadata:
                span.set_metadata(span_metadata)

        # Track root chain for trace completion
        if parent_run_id is None:
            self._root_run_id = run_id

        # Calculate depth for this span
        depth = self._calculate_depth(run_id, parent_run_id)

        # Store span context for this run (including LangGraph info for on_chain_end)
        self._span_contexts[run_id] = {
            "span": span,
            "parent_run_id": parent_run_id,
            "inputs": inputs,
            "entered": False,  # Track if span has been entered
            "entry_failed": False,  # Track if entry failed
            "entry_task": None,  # Store entry task reference if async
            "langgraph_node": langgraph_node,
            "langgraph_step": langgraph_step,
            "depth": depth,  # Depth level for flow visualization
        }

        # Track execution path for workflow execution data
        self._track_span_start(span, "chain", chain_name)

        # Track edge conditions/routing decisions from metadata
        if metadata and isinstance(metadata, dict):
            condition = (
                metadata.get("condition")
                or metadata.get("edge_condition")
                or metadata.get("routing_decision")
            )
            if condition:
                self._track_edge_condition(chain_name, condition, metadata.get("condition_result"))

            # Track state transitions if present in metadata
            from_state = metadata.get("from_state") or metadata.get("previous_state")
            to_state = (
                metadata.get("to_state")
                or metadata.get("current_state")
                or metadata.get("next_state")
            )
            if from_state and to_state:
                self._track_state_transition(
                    from_state, to_state, chain_name, metadata.get("transition_trigger")
                )

            # Track nested workflows if present
            nested_trace_id = metadata.get("nested_trace_id") or metadata.get("sub_trace_id")
            nested_workflow_name = metadata.get("nested_workflow") or metadata.get("sub_workflow")
            if nested_trace_id or nested_workflow_name:
                self._track_nested_workflow(nested_workflow_name or chain_name, nested_trace_id)

        # Drift detection: capture plan from root chain
        if self._drift_detector and parent_run_id is None:
            # Root chain - capture initial input and system prompt
            self._drift_detector.capture_initial_input(inputs)
            # Try to extract system prompt from inputs
            if isinstance(inputs, dict):
                system_prompt = inputs.get("system_prompt") or inputs.get("system_message")
                if not system_prompt and "messages" in inputs:
                    msgs = inputs["messages"]
                    if isinstance(msgs, list):
                        for msg in msgs:
                            if isinstance(msg, dict) and msg.get("role") == "system":
                                system_prompt = msg.get("content", "")
                                break
                            if hasattr(msg, "type") and msg.type == "system":
                                system_prompt = getattr(msg, "content", "")
                                break
                if system_prompt:
                    self._drift_detector.capture_system_prompt(system_prompt)

        # Store chain_name and chain_type in span context for drift tracking
        self._span_contexts[run_id]["chain_name"] = chain_name
        self._span_contexts[run_id]["chain_type"] = chain_type
        self._span_contexts[run_id]["start_time_chain"] = _utc_now()

        # Send span creation directly to buffer/backend (more reliable than async entry)
        self._send_span_create(span, run_id, inputs)

    def on_chain_end(
        self,
        outputs: dict[str, Any],
        *,
        run_id: str,
        **kwargs: Any,
    ) -> None:
        """Called when a chain ends."""
        run_id = self._normalize_run_id(run_id)
        if os.environ.get("AIGIE_DEBUG"):
            print(
                f"  [DEBUG on_chain_end] run_id={run_id[:8] if run_id else 'None'}, in_contexts={run_id in self._span_contexts}"
            )
        if run_id in self._span_contexts:
            span_context = self._span_contexts[run_id]
            span = span_context["span"]
            if hasattr(span, "set_output"):
                span.set_output(outputs)

            # Check if output contains error status (for caught exceptions)
            detected_error = None
            output_is_error_flag = False
            if isinstance(outputs, dict):
                output_status = outputs.get("status")
                if output_status == "error":
                    output_is_error_flag = True
                    error_type = outputs.get("error_type", "Error")
                    error_message = outputs.get(
                        "error", outputs.get("error_message", "Unknown error")
                    )
                    detected_error = Exception(f"{error_type}: {error_message}")

            # Wire detect_from_chain_result so ErrorDetector classifies non-exception
            # error outputs (e.g. caught failures returned as data). Wrapped to keep
            # detection failures from breaking the hook.
            if self._error_detector is not None:
                try:
                    chain_name = span_context.get("chain_name", "unknown")
                    start_time_chain = span_context.get("start_time_chain")
                    duration_ms_chain: float | None = None
                    if start_time_chain:
                        duration_ms_chain = (_utc_now() - start_time_chain).total_seconds() * 1000
                    self._error_detector.detect_from_chain_result(
                        chain_name=chain_name,
                        run_id=run_id,
                        result=outputs,
                        is_error_flag=output_is_error_flag,
                        duration_ms=duration_ms_chain,
                    )
                except Exception as detection_exc:
                    logger.warning("[AIGIE] detect_from_chain_result failed: %s", detection_exc)

            # Ensure LangGraph metadata is included in the final span update
            if hasattr(span, "set_metadata"):
                current_metadata = getattr(span, "_metadata", {})
                enriched_metadata = dict(current_metadata)

                # Add LangGraph metadata from span context
                langgraph_node = span_context.get("langgraph_node")
                langgraph_step = span_context.get("langgraph_step")
                if langgraph_node:
                    enriched_metadata["langgraph_node"] = langgraph_node
                if langgraph_step is not None:
                    enriched_metadata["langgraph_step"] = langgraph_step

                # Add error info to metadata if error detected
                if detected_error:
                    enriched_metadata["error"] = str(detected_error)
                    enriched_metadata["error_type"] = type(detected_error).__name__
                    enriched_metadata["status"] = "error"
                    enriched_metadata["level"] = "ERROR"
                    enriched_metadata["status_message"] = str(detected_error)

                span.set_metadata(enriched_metadata)

            # Set agent_type for dashboard grouping
            if hasattr(span, "set_agent_type"):
                # Use langgraph_node if available, otherwise detect from span type or name
                chain_type = span_context.get("chain_type", "chain")
                langgraph_node = span_context.get("langgraph_node")
                span_name = getattr(span, "name", "") or ""

                if langgraph_node:
                    span.set_agent_type(langgraph_node)
                elif chain_type == "workflow":
                    span.set_agent_type("workflow")
                elif chain_type == "agent":
                    span.set_agent_type("agent")
                elif "research" in span_name.lower():
                    span.set_agent_type("research_agent")
                elif "search" in span_name.lower():
                    span.set_agent_type("search_agent")
                elif "summarize" in span_name.lower() or "compress" in span_name.lower():
                    span.set_agent_type("summarization_agent")
                else:
                    span.set_agent_type(chain_type)

            # Track execution path end (with detected error if any)
            self._track_span_end(span, "chain", detected_error)

            # Drift detection: record chain execution
            if self._drift_detector:
                chain_name = span_context.get("chain_name", "unknown")
                chain_type = span_context.get("chain_type", "chain")
                start_time_chain = span_context.get("start_time_chain")
                duration_ms = 0
                if start_time_chain:
                    duration_ms = (_utc_now() - start_time_chain).total_seconds() * 1000
                self._drift_detector.record_chain_execution(
                    chain_name,
                    chain_type,
                    duration_ms=duration_ms,
                )

                # Check if this is a planning node/chain and capture its output
                planning_keywords = {
                    "planner",
                    "plan",
                    "planning",
                    "think",
                    "thinking",
                    "reason",
                    "reasoning",
                    "decide",
                    "decision",
                    "route",
                    "router",
                }
                if any(kw in chain_name.lower() for kw in planning_keywords) and outputs:
                    try:
                        self._drift_detector.capture_planning_chain_output(
                            chain_name,
                            chain_type,
                            outputs,
                        )
                        self._send_agent_plan_update("planning_node")
                    except Exception:
                        pass

            # Sync update — stamps end_time now, no async race.
            self._send_span_update(
                span, run_id, outputs if isinstance(outputs, dict) else {}, detected_error
            )

            # If this is the root chain, complete the trace — UNLESS this handler
            # is bound to a LangGraph thread_id, in which case the auto-instrument
            # wrapper owns trace lifecycle (it can tell whether the graph actually
            # reached END or just paused at an interrupt). The wrapper calls
            # _finalize_run() once the graph is confirmed done.
            if run_id == self._root_run_id and self._thread_id is None:
                self._finalize_run(outputs, detected_error)

            # Restore process-level span ID to parent for OTel bridge
            try:
                from aigie.auto_instrument.span_enricher import set_active_span_id

                parent_run = self._span_contexts[run_id].get("parent_run_id")
                parent_span = (
                    self._span_contexts.get(parent_run, {}).get("span") if parent_run else None
                )
                set_active_span_id(getattr(parent_span, "id", None))
            except Exception:
                pass

            # Clean up
            del self._span_contexts[run_id]

    def on_agent_finish(
        self,
        finish: Any,
        *,
        run_id: str,
        **kwargs: Any,
    ) -> None:
        """Called when an agent finishes with a final answer.

        Captures the agent's final output on the parent chain/agent span so that
        agent spans are not left with empty output.
        """
        run_id = self._normalize_run_id(run_id)
        if run_id in self._span_contexts:
            span_context = self._span_contexts[run_id]
            span = span_context["span"]

            # Extract return values from AgentFinish object
            output = None
            if hasattr(finish, "return_values"):
                output = finish.return_values
            elif hasattr(finish, "log"):
                output = {"log": finish.log}
            elif isinstance(finish, dict):
                output = finish

            if output and hasattr(span, "set_output"):
                span.set_output(output)

    def on_llm_start(
        self,
        serialized: dict[str, Any],
        prompts: list,
        *,
        run_id: str,
        parent_run_id: str | None = None,
        tags: list | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Called when an LLM starts."""
        if getattr(self, "_paused", False):
            return
        # Debug: Always print when called
        import os

        if os.environ.get("AIGIE_DEBUG"):
            model_name_debug = serialized.get("name", "unknown") if serialized else "no-serialized"
            print(
                f"  [DEBUG on_llm_start ENTERED] handler={id(self)}, model={model_name_debug}, has_trace={self.trace is not None}"
            )

        # Normalize UUIDs to strings for consistent dictionary lookups
        run_id = self._normalize_run_id(run_id)
        parent_run_id = self._normalize_run_id(parent_run_id)

        # Try to get trace from context if not set
        if not self.trace:
            from aigie.auto_instrument.trace import get_current_trace

            self.trace = get_current_trace()
            if os.environ.get("AIGIE_DEBUG"):
                print(f"  [DEBUG on_llm_start] Got trace from context: {self.trace}")

        if not self.trace:
            if os.environ.get("AIGIE_DEBUG"):
                print("  [DEBUG on_llm_start] No trace, returning early!")
            return

        # Ensure _current_trace is set so any nested calls can find parent trace
        from aigie.auto_instrument.trace import set_current_trace

        set_current_trace(self.trace)

        # Extract LangGraph node information from tags and metadata
        langgraph_node = None
        langgraph_step = None
        langgraph_path = None

        # Check metadata first (LangGraph passes node info here)
        if metadata and isinstance(metadata, dict):
            langgraph_node = (
                metadata.get("langgraph_node") or metadata.get("node") or metadata.get("graph_node")
            )
            langgraph_step = metadata.get("langgraph_step") or metadata.get("step")
            langgraph_path = metadata.get("langgraph_path") or metadata.get("path")
            # Also check for checkpoint info
            if not langgraph_node:
                langgraph_node = metadata.get("checkpoint_id") or metadata.get("thread_id")

        # Check tags for LangGraph patterns (e.g., "graph:step:search", "seq:step:1")
        if tags and isinstance(tags, list):
            for tag in tags:
                if isinstance(tag, str):
                    # Pattern: "graph:step:<node_name>" or similar
                    if tag.startswith("graph:") or tag.startswith("langgraph:"):
                        parts = tag.split(":")
                        if len(parts) >= 3 and parts[1] == "step":
                            langgraph_node = langgraph_node or parts[2]
                    # Pattern: "seq:step:<number>"
                    elif tag.startswith("seq:step:"):
                        with contextlib.suppress(ValueError, IndexError):
                            langgraph_step = langgraph_step or int(tag.split(":")[2])
                    # Pattern: "node:<name>"
                    elif tag.startswith("node:"):
                        langgraph_node = langgraph_node or tag.split(":", 1)[1]

        # --- Parent resolution: single path ---
        parent_span_id = self._resolve_parent(parent_run_id)

        # Safely extract model name from serialized (which might be None)
        model_id = None  # Initialize model_id first
        actual_model = None  # The actual model identifier (e.g., "gemini-2.5-flash")

        if not serialized:
            model_name = "LLM Call"
        else:
            name = serialized.get("name")
            if name:
                model_name = name
                # Try to get model_id from serialized even if we have name
                llm_id = serialized.get("id")
                if isinstance(llm_id, list) and llm_id:
                    model_id = ".".join(str(x) for x in llm_id)
                elif llm_id:
                    model_id = str(llm_id)
            else:
                llm_id = serialized.get("id")
                if isinstance(llm_id, list) and llm_id:
                    model_name = llm_id[-1] if len(llm_id) > 1 else llm_id[0]
                    model_id = ".".join(str(x) for x in llm_id)
                elif llm_id:
                    model_name = str(llm_id)
                    model_id = str(llm_id)
                else:
                    model_name = "LLM Call"

            # Try to get actual model from serialized kwargs (for LangChain LLMs)
            serialized_kwargs = serialized.get("kwargs", {})
            if serialized_kwargs:
                # Google Generative AI uses "model"
                actual_model = serialized_kwargs.get("model")
                # OpenAI uses "model_name" or "model"
                if not actual_model:
                    actual_model = serialized_kwargs.get("model_name")
                # Anthropic uses "model"
                if not actual_model:
                    actual_model = serialized_kwargs.get("model")

        # Also check invocation_params for model (some LangChain versions pass it here)
        invocation_params = kwargs.get("invocation_params", {})
        if not actual_model and invocation_params:
            actual_model = invocation_params.get("model") or invocation_params.get("model_name")

        # If we found an actual model, use it for cost calculations instead of class name
        # But keep model_name for display purposes if it's meaningful
        if actual_model:
            # If model_name is just a class name (e.g., "ChatGoogleGenerativeAI"), use actual_model
            if model_name and (
                "Chat" in model_name or "LLM" in model_name or model_name == "LLM Call"
            ):
                model_name = actual_model
            # Store actual_model for cost calculations
            model_id = actual_model

        # Extract prompt content from prompts list
        prompt_contents = []
        system_prompt = None
        if prompts:
            for prompt in prompts:
                if isinstance(prompt, str):
                    prompt_contents.append({"content": prompt, "role": "user"})
                elif hasattr(prompt, "content"):
                    # LangChain message object
                    role = getattr(prompt, "type", "user")
                    if hasattr(prompt, "content"):
                        content = prompt.content
                        # Separate system prompts
                        if role == "system" or (isinstance(role, str) and role.lower() == "system"):
                            system_prompt = content
                        else:
                            prompt_contents.append({"role": role, "content": content})
                elif isinstance(prompt, dict):
                    role = prompt.get("role", "user")
                    content = prompt.get("content", str(prompt))
                    # Separate system prompts
                    if role == "system" or (isinstance(role, str) and role.lower() == "system"):
                        system_prompt = content
                    else:
                        prompt_contents.append({"role": role, "content": content})

        # Extract LLM parameters from kwargs (LangChain passes invocation_params)
        # Note: invocation_params was already extracted above for model name detection
        llm_params = {}
        if invocation_params:
            # Extract common LLM parameters
            llm_params = {
                "temperature": invocation_params.get("temperature"),
                "top_p": invocation_params.get("top_p"),
                "top_k": invocation_params.get("top_k"),
                "max_tokens": invocation_params.get("max_tokens")
                or invocation_params.get("max_tokens_to_sample"),
                "frequency_penalty": invocation_params.get("frequency_penalty"),
                "presence_penalty": invocation_params.get("presence_penalty"),
                "stop": invocation_params.get("stop") or invocation_params.get("stop_sequences"),
                "logprobs": invocation_params.get("logprobs"),
                "logit_bias": invocation_params.get("logit_bias"),
            }
            # Remove None values
            llm_params = {k: v for k, v in llm_params.items() if v is not None}

        # Also check kwargs directly for parameters (some LangChain versions pass them here)
        if not llm_params:
            llm_params = {
                "temperature": kwargs.get("temperature"),
                "top_p": kwargs.get("top_p"),
                "top_k": kwargs.get("top_k"),
                "max_tokens": kwargs.get("max_tokens") or kwargs.get("max_tokens_to_sample"),
                "frequency_penalty": kwargs.get("frequency_penalty"),
                "presence_penalty": kwargs.get("presence_penalty"),
                "stop": kwargs.get("stop") or kwargs.get("stop_sequences"),
            }
            llm_params = {k: v for k, v in llm_params.items() if v is not None}

        # Build structured LLM input data
        llm_input_data = {
            "model": model_name,
            "prompts": prompt_contents if prompt_contents else prompts,
            "prompt_count": len(prompts) if prompts else 0,
        }
        if model_id:
            llm_input_data["model_id"] = model_id
        if system_prompt:
            llm_input_data["system_prompt"] = system_prompt
        if llm_params:
            llm_input_data["parameters"] = llm_params

        # Add LangGraph metadata to input data for workflow definition extraction
        if langgraph_node:
            llm_input_data["langgraph_node"] = langgraph_node
        if langgraph_step is not None:
            llm_input_data["langgraph_step"] = langgraph_step
        if langgraph_path:
            llm_input_data["langgraph_path"] = langgraph_path

        # Use langgraph_node in span name if available for better workflow visualization
        # Model name is stored in metadata, no need to duplicate in span name
        span_name = langgraph_node or f"LLM: {model_name}"

        # Create span for LLM call
        span = self.trace.span(name=span_name, type="llm", parent=parent_span_id)

        # Set model eagerly so it's captured even if on_llm_end is never reached
        effective_model = model_id or model_name
        if effective_model and effective_model != "LLM Call" and hasattr(span, "set_model"):
            span.set_model(effective_model)

        # Debug: log span creation details
        import os

        if os.environ.get("AIGIE_DEBUG"):
            print(f"  [DEBUG on_llm_start] Created span id={span.id}, parent_id={span.parent_id}")

        # Calculate depth for this span
        depth = self._calculate_depth(run_id, parent_run_id)

        # Store span context with LLM parameters for later use
        self._span_contexts[run_id] = {
            "span": span,
            "parent_run_id": parent_run_id,
            "prompts": prompts,
            "input_messages": prompt_contents,  # Normalized message dicts for remediation loop
            "model_name": model_name,
            "model_id": model_id,
            "llm_params": llm_params,
            "invocation_params": llm_params,  # Alias for set_model_parameters in on_llm_end
            "system_prompt": system_prompt,
            "entered": False,
            "completion_start_time": None,  # Will be set when first token received
            "langgraph_node": langgraph_node,
            "langgraph_step": langgraph_step,
            "depth": depth,  # Depth level for flow visualization
        }

        # Increment turn count (each LLM call is a turn)
        self._turn_count += 1

        # Track execution path for workflow execution data
        self._track_span_start(span, "llm", span_name)

        # Track agent iterations if this is an agent LLM call
        if parent_run_id and parent_run_id in self._span_contexts:
            parent_span = self._span_contexts[parent_run_id]["span"]
            if hasattr(parent_span, "span_type") and parent_span.span_type == "agent":
                agent_name = parent_span.name if hasattr(parent_span, "name") else "Agent"
                self._track_agent_iteration(agent_name)

        # Stamp start_time synchronously — eliminates async race on start_time.
        self._send_span_create(span, run_id, llm_input_data)

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: str,
        **kwargs: Any,
    ) -> None:
        """Called when an LLM ends."""
        run_id = self._normalize_run_id(run_id)
        import logging

        logger = logging.getLogger(__name__)

        if run_id in self._span_contexts:
            span_context = self._span_contexts[run_id]
            span = span_context["span"]

            # Extract token usage from LLM response
            token_usage_data = None
            # Get model_name from span_context (stored in on_llm_start) as fallback
            model_name = span_context.get("model_name")
            estimated_cost = 0.0

            # Try to get raw response from kwargs (some LLMs pass it here)
            raw_response_obj = kwargs.get("response") or kwargs.get("raw_response")
            if raw_response_obj:
                # Try to extract usage from raw response
                if hasattr(raw_response_obj, "usage"):
                    usage_obj = raw_response_obj.usage
                    if usage_obj:
                        token_usage_data = {
                            "prompt_tokens": getattr(usage_obj, "prompt_tokens", 0),
                            "completion_tokens": getattr(usage_obj, "completion_tokens", 0),
                            "total_tokens": getattr(usage_obj, "total_tokens", 0),
                            "cache_read_input_tokens": getattr(
                                usage_obj, "cache_read_input_tokens", 0
                            ),
                            "cache_creation_input_tokens": getattr(
                                usage_obj, "cache_creation_input_tokens", 0
                            ),
                        }
                elif isinstance(raw_response_obj, dict) and "usage" in raw_response_obj:
                    token_usage_data = raw_response_obj["usage"]

            # Try multiple locations for token usage

            if hasattr(response, "llm_output") and response.llm_output:
                # Debug: log the entire llm_output to see what's available
                logger.debug(
                    f"LLM output keys: {list(response.llm_output.keys()) if isinstance(response.llm_output, dict) else 'not a dict'}"
                )
                logger.debug(f"LLM output: {response.llm_output}")

                # Try standard token_usage field
                token_usage_data = response.llm_output.get("token_usage")
                # Only update model_name if we got a non-empty one from llm_output
                llm_output_model = response.llm_output.get("model_name")
                if llm_output_model:
                    model_name = llm_output_model

                # Try alternative locations for token usage
                if not token_usage_data:
                    token_usage_data = response.llm_output.get("usage")

                # Extract from nested structures
                if not token_usage_data and "metadata" in response.llm_output:
                    token_usage_data = response.llm_output["metadata"].get("token_usage")

                # Try to extract from response_metadata
                if not token_usage_data and "response_metadata" in response.llm_output:
                    response_metadata = response.llm_output["response_metadata"]
                    if isinstance(response_metadata, dict):
                        token_usage_data = response_metadata.get(
                            "token_usage"
                        ) or response_metadata.get("usage")

                # Try to get raw response object if available (some LLMs store it)
                if not token_usage_data and "raw" in response.llm_output:
                    raw_response = response.llm_output["raw"]
                    # Try to extract from raw response object
                    if hasattr(raw_response, "usage"):
                        usage_obj = raw_response.usage
                        if usage_obj:
                            token_usage_data = {
                                "prompt_tokens": getattr(usage_obj, "prompt_tokens", 0),
                                "completion_tokens": getattr(usage_obj, "completion_tokens", 0),
                                "total_tokens": getattr(usage_obj, "total_tokens", 0),
                            }
                    elif isinstance(raw_response, dict) and "usage" in raw_response:
                        usage_dict = raw_response["usage"]
                        if isinstance(usage_dict, dict):
                            token_usage_data = usage_dict
                        elif hasattr(usage_dict, "prompt_tokens"):
                            token_usage_data = {
                                "prompt_tokens": getattr(usage_dict, "prompt_tokens", 0),
                                "completion_tokens": getattr(usage_dict, "completion_tokens", 0),
                                "total_tokens": getattr(usage_dict, "total_tokens", 0),
                            }

            # Fallback: Try to extract from response object directly (for some providers)
            if not token_usage_data and hasattr(response, "response_metadata"):
                response_metadata = response.response_metadata
                if isinstance(response_metadata, dict):
                    token_usage_data = response_metadata.get(
                        "token_usage"
                    ) or response_metadata.get("usage")

            # Fallback: Try to extract from generations (some providers store it there)
            if not token_usage_data and hasattr(response, "generations") and response.generations:
                for gen_list in response.generations:
                    if gen_list:
                        for gen in gen_list:
                            # Check generation_info first
                            if hasattr(gen, "generation_info") and gen.generation_info:
                                token_usage_data = gen.generation_info.get(
                                    "token_usage"
                                ) or gen.generation_info.get("usage")
                                if token_usage_data:
                                    break

                            # Check message.usage_metadata (Gemini returns tokens here!)
                            if hasattr(gen, "message") and hasattr(gen.message, "usage_metadata"):
                                usage_meta = gen.message.usage_metadata
                                if usage_meta:
                                    # Handle dict format
                                    if isinstance(usage_meta, dict):
                                        token_usage_data = {
                                            "prompt_tokens": usage_meta.get("input_tokens", 0),
                                            "completion_tokens": usage_meta.get("output_tokens", 0),
                                            "total_tokens": usage_meta.get("total_tokens", 0),
                                        }
                                    # Handle object format
                                    elif hasattr(usage_meta, "input_tokens"):
                                        token_usage_data = {
                                            "prompt_tokens": getattr(usage_meta, "input_tokens", 0),
                                            "completion_tokens": getattr(
                                                usage_meta, "output_tokens", 0
                                            ),
                                            "total_tokens": getattr(usage_meta, "total_tokens", 0),
                                        }
                                    if token_usage_data:
                                        logger.debug(
                                            f"Extracted token usage from message.usage_metadata: {token_usage_data}"
                                        )
                                        break
                        if token_usage_data:
                            break

            # Ensure token_usage_data is a dict
            if token_usage_data and not isinstance(token_usage_data, dict):
                # If it's a Usage object, convert to dict
                if hasattr(token_usage_data, "__dict__"):
                    token_usage_data = token_usage_data.__dict__
                elif hasattr(token_usage_data, "prompt_tokens"):
                    token_usage_data = {
                        "prompt_tokens": getattr(token_usage_data, "prompt_tokens", 0),
                        "completion_tokens": getattr(token_usage_data, "completion_tokens", 0),
                        "total_tokens": getattr(token_usage_data, "total_tokens", 0),
                    }
                else:
                    token_usage_data = {}

            if not token_usage_data:
                token_usage_data = {}

            # Calculate cost if we have token usage
            input_cost = 0.0
            output_cost = 0.0
            pricing_tier = None

            # Check if we actually have token usage data (not just empty dict)
            has_token_usage = (
                token_usage_data
                and isinstance(token_usage_data, dict)
                and (
                    token_usage_data.get("prompt_tokens")
                    or token_usage_data.get("input_tokens")
                    or token_usage_data.get("completion_tokens")
                    or token_usage_data.get("output_tokens")
                    or token_usage_data.get("total_tokens")
                )
            )

            if has_token_usage:
                try:
                    from aigie.cost_tracking import calculate_cost, get_model_pricing

                    # Extract token counts
                    input_tokens = token_usage_data.get("prompt_tokens") or token_usage_data.get(
                        "input_tokens", 0
                    )
                    output_tokens = token_usage_data.get(
                        "completion_tokens"
                    ) or token_usage_data.get("output_tokens", 0)
                    total_tokens = token_usage_data.get(
                        "total_tokens", input_tokens + output_tokens
                    )

                    # Extract cache tokens (Anthropic models)
                    cache_read_tokens = (
                        token_usage_data.get("cache_read_input_tokens", 0)
                        or token_usage_data.get("cache_read_tokens", 0)
                        or 0
                    )
                    cache_creation_tokens = (
                        token_usage_data.get("cache_creation_input_tokens", 0)
                        or token_usage_data.get("cache_write_tokens", 0)
                        or 0
                    )

                    # Extract reasoning/thinking tokens (Claude extended thinking, o1/o3)
                    _ = (
                        token_usage_data.get("reasoning_tokens", 0)
                        or token_usage_data.get("thinking_tokens", 0)
                        or token_usage_data.get("reasoning_completion_tokens", 0)
                        or 0
                    )

                    # Create usage dict for cost calculation
                    usage_dict = {
                        "prompt_tokens": input_tokens,
                        "completion_tokens": output_tokens,
                        "total_tokens": total_tokens,
                        "cache_read_input_tokens": cache_read_tokens,
                        "cache_creation_input_tokens": cache_creation_tokens,
                    }

                    # Calculate cost with breakdown
                    if model_name:
                        # Try to get pricing info for tier
                        pricing_info = get_model_pricing(model_name)
                        if pricing_info:
                            pricing_tier = f"{pricing_info.provider}:{model_name}"

                        # Calculate cost breakdown
                        from aigie.cost_tracking import UsageMetadata

                        usage_metadata = UsageMetadata(
                            input_tokens=input_tokens,
                            output_tokens=output_tokens,
                            total_tokens=total_tokens,
                            model=model_name,
                        )
                        cost_breakdown = calculate_cost(usage_metadata, model_name)
                        if cost_breakdown:
                            estimated_cost = float(cost_breakdown.total_cost)
                            input_cost = float(cost_breakdown.input_cost)
                            output_cost = float(cost_breakdown.output_cost)
                except Exception as e:
                    logger.warning(f"Failed to calculate cost for LLM span: {e}", exc_info=True)

            # Debug logging to help diagnose token extraction issues
            if not has_token_usage:
                logger.debug(
                    f"No token usage found in LLM response for span {span.name if hasattr(span, 'name') else 'unknown'}. "
                    f"llm_output keys: {list(response.llm_output.keys()) if (hasattr(response, 'llm_output') and response.llm_output and isinstance(response.llm_output, dict)) else 'N/A'}. "
                    f"Attempting token estimation..."
                )
                # Estimate tokens from prompt and response content
                # Average: ~4 characters per token for English text
                try:
                    prompt_text = ""
                    if run_id in self._span_contexts:
                        input_data = span_context.get("input_data", {})
                        if isinstance(input_data, dict):
                            # Try to get prompt from various locations
                            prompt_text = str(input_data.get("prompt", ""))
                            if not prompt_text and "messages" in input_data:
                                prompt_text = str(input_data.get("messages", ""))
                            if not prompt_text and "prompts" in input_data:
                                prompt_text = str(input_data.get("prompts", ""))
                        elif isinstance(input_data, str):
                            prompt_text = input_data

                    # Get response text from generations
                    response_text = ""
                    if hasattr(response, "generations") and response.generations:
                        for gen_list in response.generations:
                            for gen in gen_list:
                                if hasattr(gen, "text"):
                                    response_text += gen.text
                                elif hasattr(gen, "message") and hasattr(gen.message, "content"):
                                    response_text += str(gen.message.content)

                    # Estimate tokens (average 4 chars per token)
                    estimated_prompt_tokens = len(prompt_text) // 4 if prompt_text else 0
                    estimated_completion_tokens = len(response_text) // 4 if response_text else 0
                    estimated_total_tokens = estimated_prompt_tokens + estimated_completion_tokens

                    if estimated_total_tokens > 0:
                        token_usage_data = {
                            "prompt_tokens": estimated_prompt_tokens,
                            "completion_tokens": estimated_completion_tokens,
                            "total_tokens": estimated_total_tokens,
                            "estimated": True,  # Mark as estimated
                        }
                        has_token_usage = True
                        logger.debug(
                            f"Estimated tokens for span: prompt={estimated_prompt_tokens}, completion={estimated_completion_tokens}"
                        )
                except Exception as e:
                    logger.debug(f"Failed to estimate tokens: {e}")
            else:
                logger.debug(
                    f"Found token usage for span {span.name if hasattr(span, 'name') else 'unknown'}: prompt={token_usage_data.get('prompt_tokens', 0)}, completion={token_usage_data.get('completion_tokens', 0)}, total={token_usage_data.get('total_tokens', 0)}"
                )

            # Extract response content from generations
            response_contents = []
            tool_calls = []
            finish_reasons = []
            model_name_from_context = span_context.get("model_name", "LLM")

            if hasattr(response, "generations") and response.generations:
                for gen_list in response.generations:
                    for gen in gen_list:
                        finish_reason = None
                        if hasattr(gen, "text"):
                            response_contents.append({"content": gen.text, "type": "text"})
                            # Try to get finish reason from generation
                            if hasattr(gen, "generation_info") and isinstance(
                                gen.generation_info, dict
                            ):
                                finish_reason = gen.generation_info.get(
                                    "finish_reason"
                                ) or gen.generation_info.get("finishReason")
                        elif hasattr(gen, "message"):
                            msg = gen.message
                            if hasattr(msg, "content"):
                                resp_obj = {
                                    "content": msg.content,
                                    "type": getattr(msg, "type", "ai"),
                                }
                                # Extract tool calls if present
                                if hasattr(msg, "tool_calls") and msg.tool_calls:
                                    resp_obj["tool_calls"] = msg.tool_calls
                                    tool_calls.extend(msg.tool_calls)
                                    finish_reason = "tool_calls"
                                # Extract finish reason if available
                                if hasattr(msg, "response_metadata") and isinstance(
                                    msg.response_metadata, dict
                                ):
                                    finish_reason = msg.response_metadata.get(
                                        "finish_reason"
                                    ) or msg.response_metadata.get("finishReason")
                                response_contents.append(resp_obj)
                        elif isinstance(gen, dict):
                            response_contents.append(
                                {"content": gen.get("text", str(gen)), "type": "text"}
                            )
                            finish_reason = gen.get("finish_reason") or gen.get("finishReason")
                        else:
                            response_contents.append({"content": str(gen), "type": "unknown"})

                        if finish_reason:
                            finish_reasons.append(finish_reason)

            # Extract response metadata from llm_output
            response_metadata = {}
            request_id = None
            response_id = None
            model_version = None
            system_fingerprint = None
            completion_start_time = None

            if hasattr(response, "llm_output") and response.llm_output:
                # Extract request_id and model_version from llm_output metadata
                if isinstance(response.llm_output, dict):
                    metadata = response.llm_output.get("metadata", {})
                    if isinstance(metadata, dict):
                        request_id = (
                            metadata.get("request_id")
                            or metadata.get("id")
                            or metadata.get("requestId")
                        )
                        model_version = (
                            metadata.get("model_version")
                            or metadata.get("modelVersion")
                            or metadata.get("model")
                        )
                        # Extract system fingerprint (OpenAI)
                        system_fingerprint = metadata.get("system_fingerprint")
                        if system_fingerprint:
                            response_metadata["system_fingerprint"] = system_fingerprint
                        # Extract response ID (Anthropic)
                        response_id = metadata.get("response_id") or metadata.get("id")
                        if response_id:
                            response_metadata["response_id"] = response_id
                        # Extract completion start time (when LLM started generating)
                        completion_start_time = metadata.get(
                            "completion_start_time"
                        ) or metadata.get("completionStartTime")

                # Also check top-level llm_output for these fields
                if not request_id:
                    request_id = response.llm_output.get("request_id") or response.llm_output.get(
                        "id"
                    )
                if not model_version:
                    model_version = response.llm_output.get(
                        "model_version"
                    ) or response.llm_output.get("model")
                if not system_fingerprint:
                    system_fingerprint = response.llm_output.get("system_fingerprint")
                if not response_id:
                    response_id = response.llm_output.get("response_id")
                if not completion_start_time:
                    completion_start_time = response.llm_output.get(
                        "completion_start_time"
                    ) or response.llm_output.get("completionStartTime")

            # Also check response object directly (for direct API calls)
            if hasattr(response, "system_fingerprint") and not system_fingerprint:
                system_fingerprint = response.system_fingerprint
                response_metadata["system_fingerprint"] = system_fingerprint
            if hasattr(response, "id") and not response_id:
                # For Anthropic, response.id is the response_id
                if model_name and "claude" in model_name.lower():
                    response_id = response.id
                    response_metadata["response_id"] = response_id

            # Build structured output data
            output_data = {
                "model": model_name or model_name_from_context,
                "response": response_contents[0]["content"] if response_contents else None,
                "responses": response_contents,
                "generations_count": len(response.generations)
                if hasattr(response, "generations")
                else 0,
                "status": "success",
            }

            # Add response metadata
            if finish_reasons:
                output_data["finish_reasons"] = finish_reasons
                output_data["finish_reason"] = finish_reasons[0]  # Primary finish reason
            if request_id:
                output_data["request_id"] = request_id
            if model_version:
                output_data["model_version"] = model_version
            if response_metadata:
                output_data["response_metadata"] = response_metadata

            if has_token_usage:
                output_data["token_usage"] = token_usage_data
                # Calculate token totals
                if isinstance(token_usage_data, dict):
                    total_tokens = token_usage_data.get("total_tokens") or (
                        (token_usage_data.get("prompt_tokens") or 0)
                        + (token_usage_data.get("completion_tokens") or 0)
                    )
                    output_data["total_tokens"] = total_tokens
                    output_data["prompt_tokens"] = token_usage_data.get("prompt_tokens")
                    output_data["completion_tokens"] = token_usage_data.get("completion_tokens")

            if has_token_usage:
                output_data["estimated_cost"] = estimated_cost
                output_data["input_cost"] = input_cost
                output_data["output_cost"] = output_cost
            if completion_start_time:
                output_data["completion_start_time"] = completion_start_time

            if tool_calls:
                output_data["tool_calls"] = tool_calls

            if hasattr(span, "set_output"):
                span.set_output(output_data)

            # Extract token counts for direct field storage
            prompt_tokens = 0
            completion_tokens = 0
            total_tokens = 0
            if has_token_usage:
                prompt_tokens = (
                    token_usage_data.get("prompt_tokens")
                    or token_usage_data.get("input_tokens", 0)
                    or 0
                )
                completion_tokens = (
                    token_usage_data.get("completion_tokens")
                    or token_usage_data.get("output_tokens", 0)
                    or 0
                )
                total_tokens = token_usage_data.get("total_tokens") or (
                    prompt_tokens + completion_tokens
                )

            # Store comprehensive metadata in span for aggregation and analysis
            if hasattr(span, "set_metadata"):
                current_metadata = getattr(span, "_metadata", {})
                enriched_metadata = dict(current_metadata)

                # Token usage (also store in metadata for backward compatibility)
                if has_token_usage:
                    enriched_metadata["token_usage"] = {
                        "prompt_tokens": prompt_tokens,  # Backend expects prompt_tokens, not input_tokens
                        "completion_tokens": completion_tokens,  # Backend expects completion_tokens, not output_tokens
                        "input_tokens": prompt_tokens,  # Keep for backward compatibility
                        "output_tokens": completion_tokens,  # Keep for backward compatibility
                        "total_tokens": total_tokens,
                        "estimated_cost": estimated_cost,
                        "input_cost": input_cost,
                        "output_cost": output_cost,
                    }

                # Store token counts as direct fields in metadata (will be extracted to direct columns by backend)
                # Always store these fields, even if 0, so backend can see them
                enriched_metadata["prompt_tokens"] = prompt_tokens
                enriched_metadata["completion_tokens"] = completion_tokens
                enriched_metadata["total_tokens"] = total_tokens
                enriched_metadata["input_cost"] = input_cost
                enriched_metadata["output_cost"] = output_cost
                enriched_metadata["total_cost"] = estimated_cost

                # Reasoning/thinking tokens (Claude extended thinking, o1/o3 models)
                _reasoning_tokens = (
                    token_usage_data.get("reasoning_tokens", 0)
                    or token_usage_data.get("thinking_tokens", 0)
                    or token_usage_data.get("reasoning_completion_tokens", 0)
                    or 0
                )
                if _reasoning_tokens:
                    enriched_metadata["reasoning_tokens"] = _reasoning_tokens

                # Model information (store as direct fields)
                if model_name:
                    enriched_metadata["model"] = model_name
                    enriched_metadata["model_name"] = model_name  # Backward compatibility
                # Get model_id from span context (stored in on_llm_start)
                model_id = span_context.get("model_id")
                if model_id:
                    enriched_metadata["model_id"] = model_id
                if model_version:
                    enriched_metadata["model_version"] = model_version
                if pricing_tier:
                    enriched_metadata["pricing_tier"] = pricing_tier

                # LLM parameters (store as model_parameters)
                llm_params = span_context.get("llm_params", {})
                if llm_params:
                    enriched_metadata["model_parameters"] = llm_params
                    enriched_metadata["llm_parameters"] = llm_params  # Backward compatibility

                # System prompt
                system_prompt = span_context.get("system_prompt")
                if system_prompt:
                    enriched_metadata["system_prompt"] = system_prompt

                # Response metadata
                if finish_reasons:
                    enriched_metadata["finish_reason"] = finish_reasons[0]
                if request_id:
                    enriched_metadata["request_id"] = request_id
                if response_id:
                    enriched_metadata["response_id"] = response_id
                if system_fingerprint:
                    enriched_metadata["system_fingerprint"] = system_fingerprint
                if completion_start_time:
                    enriched_metadata["completion_start_time"] = completion_start_time
                    # Also store in span context for later use
                    span_context["completion_start_time"] = completion_start_time
                if response_metadata:
                    enriched_metadata.update(response_metadata)

                # Retry count tracking
                if self.trace and hasattr(self.trace, "id") and self.trace.id:
                    trace_id = self.trace.id
                    span_name = span_context.get("model_name") or "LLM"
                    if trace_id in self._retry_info:
                        retries_for_span = [
                            r for r in self._retry_info[trace_id] if r.get("span_name") == span_name
                        ]
                        retry_count = len(retries_for_span)
                        if retry_count > 0:
                            enriched_metadata["retry_count"] = retry_count

                # Add LangGraph metadata for workflow definition extraction
                langgraph_node = span_context.get("langgraph_node")
                langgraph_step = span_context.get("langgraph_step")
                if langgraph_node:
                    enriched_metadata["langgraph_node"] = langgraph_node
                if langgraph_step is not None:
                    enriched_metadata["langgraph_step"] = langgraph_step

                span.set_metadata(enriched_metadata)

            # Set direct fields on span object (will be included in __aexit__ update)
            # This is more reliable than separate API calls
            if hasattr(span, "set_model") and (model_name or model_name_from_context):
                span.set_model(model_name or model_name_from_context)

            if hasattr(span, "set_usage") and has_token_usage:
                span.set_usage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens,
                    input_cost=input_cost,
                    output_cost=output_cost,
                    total_cost=estimated_cost,
                )

            # Set completion_start_time for TTFT calculation
            if hasattr(span, "set_completion_start_time") and completion_start_time:
                span.set_completion_start_time(completion_start_time)

            # Set model parameters (temperature, top_p, etc.)
            if hasattr(span, "set_model_parameters"):
                model_params = span_context.get("invocation_params", {})
                if model_params:
                    # Extract common model parameters
                    params_to_send = {}
                    for key in [
                        "temperature",
                        "top_p",
                        "top_k",
                        "max_tokens",
                        "max_output_tokens",
                        "stop",
                        "stop_sequences",
                        "presence_penalty",
                        "frequency_penalty",
                    ]:
                        if key in model_params:
                            params_to_send[key] = model_params[key]
                    if params_to_send:
                        span.set_model_parameters(params_to_send)

            # Set agent_type for dashboard grouping
            if hasattr(span, "set_agent_type"):
                span.set_agent_type("llm")

            # Drift detection: record LLM response to capture planning
            if self._drift_detector:
                try:
                    llm_text = ""
                    if hasattr(response, "generations") and response.generations:
                        for gen_list in response.generations:
                            for gen in gen_list:
                                if hasattr(gen, "text") and gen.text:
                                    llm_text += gen.text
                                elif hasattr(gen, "message") and hasattr(gen.message, "content"):
                                    llm_text += str(gen.message.content)
                    if llm_text:
                        self._drift_detector.record_llm_response(
                            llm_text,
                            model=span_context.get("model_name"),
                        )
                        # Send agent plan update if plan was just captured
                        if self._drift_detector._plan_captured and not self._plan_sent:
                            self._send_agent_plan_update("first_llm_response")
                except Exception:
                    pass  # Don't fail on drift tracking

            # Wire detect_from_llm_response so ErrorDetector classifies error
            # content embedded in successful LLM responses (e.g. rate-limit text
            # returned as a generation). Exceptions are handled in on_llm_error.
            if self._error_detector is not None:
                try:
                    self._error_detector.detect_from_llm_response(
                        response,
                        model=model_name,
                        run_id=run_id,
                    )
                except Exception as detection_exc:
                    logger.warning("[AIGIE] detect_from_llm_response failed: %s", detection_exc)

            # Track execution path end
            self._track_span_end(span, "llm", None)

            # Sync update — stamps end_time now, no async race.
            self._send_span_update(span, run_id, {}, None)

            # Clean up
            del self._span_contexts[run_id]

    def on_llm_new_token(
        self,
        token: str,
        *,
        run_id: str,
        **kwargs: Any,
    ) -> None:
        """Called on each new LLM token during streaming.

        Records completion_start_time on the FIRST token only (TTFT metric).
        """
        run_id = self._normalize_run_id(run_id)
        if run_id in self._span_contexts:
            span_context = self._span_contexts[run_id]
            # Record TTFT on first token only
            if span_context.get("completion_start_time") is None:
                now = _utc_now()
                span_context["completion_start_time"] = now.isoformat()

    def on_tool_start(
        self,
        serialized: dict[str, Any],
        input_str: str,
        *,
        run_id: str,
        parent_run_id: str | None = None,
        tags: list | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Called when a tool starts.

        Extracts tool information from LangChain's serialized dict. The serialized
        dict contains all the information LangChain has about the tool, including:
        - name: Tool name
        - id: Tool class path (array or string)
        - description: Tool description
        - func/function: Function object for function-based tools

        Note: run_id and parent_run_id may be UUID objects from LangChain.
        """
        if getattr(self, "_paused", False):
            return
        # Normalize UUIDs to strings for consistent dictionary lookups
        run_id = self._normalize_run_id(run_id)
        parent_run_id = self._normalize_run_id(parent_run_id)

        # Try to get trace from context if not set
        if not self.trace:
            from aigie.auto_instrument.trace import get_current_trace

            self.trace = get_current_trace()

        if not self.trace:
            return

        # Ensure _current_trace is set so any nested calls can find parent trace
        from aigie.auto_instrument.trace import set_current_trace

        set_current_trace(self.trace)

        # Increment tool call count
        self._total_tool_calls += 1

        # --- Parent resolution: single path ---
        parent_span_id = self._resolve_parent(parent_run_id)

        # Extract comprehensive tool information from LangChain's serialized dict
        if not serialized:
            tool_name = "Tool"
            tool_description = None
            tool_id = None
            tool_class = None
            tool_type = None
            func_name = None
            tool_version = None
            tool_return_type = None
        else:
            # Extract tool name (primary identifier)
            tool_name = serialized.get("name", "Tool")

            # Extract tool ID (can be array like ["langchain", "tools", "tool", "Tool"] or string)
            tool_id = serialized.get("id")
            tool_class = None
            if tool_id:
                if isinstance(tool_id, list) and tool_id:
                    # Extract class name from class path (e.g., ["langchain", "tools", "tool", "Tool"] -> "Tool")
                    tool_class = ".".join(str(x) for x in tool_id)
                    # Extract class name from path
                    if tool_id:
                        last_part = tool_id[-1]
                        if isinstance(last_part, str):
                            # Handle cases like "langchain.tools.tool.Tool" or just "Tool"
                            if "." in last_part:
                                tool_class = last_part
                                tool_name_from_class = last_part.split(".")[-1]
                            else:
                                tool_class = ".".join(str(x) for x in tool_id)
                                tool_name_from_class = str(last_part)
                            # Use class name if name is generic
                            if tool_name == "Tool" or not tool_name:
                                tool_name = tool_name_from_class
                elif isinstance(tool_id, str):
                    tool_class = tool_id
                    # Extract class name from string path
                    if "." in tool_id:
                        tool_name_from_class = tool_id.split(".")[-1]
                        if tool_name == "Tool" or not tool_name:
                            tool_name = tool_name_from_class

            # Extract tool description
            tool_description = serialized.get("description")

            # Determine tool type from class/id
            tool_type = None
            if tool_class:
                tool_class_lower = tool_class.lower()
                if "function" in tool_class_lower or "func" in tool_class_lower:
                    tool_type = "function"
                elif "structured" in tool_class_lower:
                    tool_type = "structured_tool"
                elif "tool" in tool_class_lower:
                    tool_type = "tool"
                else:
                    tool_type = "custom"

            # Extract function name if available (for function-based tools)
            # LangChain stores the actual function object in serialized["func"] or serialized["function"]
            func_name = None
            func_obj = serialized.get("func") or serialized.get("function")
            if func_obj:
                if hasattr(func_obj, "__name__"):
                    # Extract function name from function object (e.g., search_database, calculate_total)
                    func_name = func_obj.__name__
                elif isinstance(func_obj, str):
                    func_name = func_obj
                elif callable(func_obj):
                    # Try to get name from callable
                    func_name = getattr(func_obj, "__name__", None) or getattr(
                        func_obj, "__qualname__", None
                    )

            # Also check kwargs for tool object (some LangChain versions pass it directly)
            if not func_name and kwargs:
                tool_obj = kwargs.get("tool") or kwargs.get("tool_instance")
                if tool_obj:
                    # Try to get function from tool object
                    if hasattr(tool_obj, "func"):
                        func_obj_from_tool = tool_obj.func
                        if hasattr(func_obj_from_tool, "__name__"):
                            func_name = func_obj_from_tool.__name__
                    # Or get name directly from tool
                    elif hasattr(tool_obj, "name"):
                        if not tool_name or tool_name == "Tool":
                            tool_name = tool_obj.name

            # Extract additional metadata
            tool_version = serialized.get("version")
            tool_return_type = serialized.get("return_type")

        # Parse tool input - try to parse as JSON if it looks like JSON
        parsed_input = input_str
        try:
            import json

            # Try to parse as JSON
            if isinstance(input_str, str) and (
                input_str.strip().startswith("{") or input_str.strip().startswith("[")
            ):
                parsed_input = json.loads(input_str)
        except (json.JSONDecodeError, ValueError):
            # If parsing fails, keep as string but try to extract structured data
            parsed_input = input_str

        # Build comprehensive tool input data structure
        tool_input_data = {"tool_name": tool_name, "input": parsed_input}

        # Add all extracted tool metadata
        if tool_description:
            tool_input_data["description"] = tool_description
        if tool_id:
            tool_input_data["tool_id"] = tool_id
        if tool_class:
            tool_input_data["tool_class"] = tool_class
        if tool_type:
            tool_input_data["tool_type"] = tool_type
        if func_name:
            tool_input_data["function_name"] = func_name
        if tool_version:
            tool_input_data["tool_version"] = tool_version
        if tool_return_type:
            tool_input_data["return_type"] = tool_return_type

        # Extract tool arguments if input is a dict
        if isinstance(parsed_input, dict):
            tool_input_data["parameters"] = parsed_input
        elif isinstance(parsed_input, str):
            tool_input_data["raw_input"] = parsed_input

        # Store full serialized config for reference
        tool_input_data["serialized"] = serialized

        # Create span with tool name extracted from LangChain serialized data
        # Use function name if available, otherwise use tool name
        span_display_name = func_name if func_name else tool_name
        span = self.trace.span(
            name=f"Tool: {span_display_name}", type="tool", parent=parent_span_id
        )

        # Set process-level span ID synchronously for OTel bridge
        try:
            from aigie.auto_instrument.span_enricher import set_active_span_id

            set_active_span_id(span.id)
        except Exception:
            pass

        # Store comprehensive span context
        # Store span context with start time for execution time calculation

        start_time = _utc_now()

        # Calculate depth for this span
        depth = self._calculate_depth(run_id, parent_run_id)

        self._span_contexts[run_id] = {
            "span": span,
            "parent_run_id": parent_run_id,
            "parent_span_id": parent_span_id,  # Store for later use
            "input": input_str,
            "tool_name": tool_name,
            "tool_input": parsed_input,  # Store parsed input for drift detection
            "function_name": func_name,
            "tool_class": tool_class,
            "tool_type": tool_type,
            "start_time": start_time,
            "entered": False,
            "depth": depth,  # Depth level for flow visualization
        }

        # If parent span doesn't have ID yet, try to resolve it when parent is entered
        if parent_run_id and not parent_span_id and parent_run_id in self._span_contexts:
            # Store reference to this span so parent can update it when it gets an ID
            parent_context = self._span_contexts[parent_run_id]
            if "child_spans" not in parent_context:
                parent_context["child_spans"] = []
            parent_context["child_spans"].append(run_id)

        # Set metadata on span for better tracking
        if hasattr(span, "set_metadata"):
            span_metadata = {"tool_name": tool_name, "tool_type": tool_type or "tool"}
            if func_name:
                span_metadata["function_name"] = func_name
            if tool_class:
                span_metadata["tool_class"] = tool_class
            if tool_description:
                span_metadata["description"] = tool_description
            # Add framework identifier so backend knows which framework spawned this tool
            if self._langgraph_mode:
                span_metadata["framework"] = "langgraph"
            # Add tool_category hint for component registry classification
            try:
                from aigie.tool_category import infer_tool_category

                category = infer_tool_category(tool_name, tool_description)
                if category:
                    span_metadata["tool_category"] = category
            except ImportError:
                pass
            span.set_metadata(span_metadata)

        # Track execution path for workflow execution data
        self._track_span_start(span, "tool", f"Tool: {span_display_name}")

        # Stamp start_time synchronously — eliminates async race on start_time.
        self._send_span_create(span, run_id, tool_input_data)

    def on_tool_end(
        self,
        output: str,
        *,
        run_id: str,
        **kwargs: Any,
    ) -> None:
        """Called when a tool ends."""
        run_id = self._normalize_run_id(run_id)
        if run_id in self._span_contexts:
            span_context = self._span_contexts[run_id]
            span = span_context["span"]
            tool_name = span_context.get("tool_name", "Tool")

            # Parse tool output - try to parse as JSON if it looks like JSON
            parsed_output = output
            try:
                import json

                if isinstance(output, str) and (
                    output.strip().startswith("{") or output.strip().startswith("[")
                ):
                    parsed_output = json.loads(output)
            except (json.JSONDecodeError, ValueError):
                parsed_output = output

            # Calculate execution time if we have start time
            execution_time_ms = None
            if run_id in self._span_contexts:
                start_time = span_context.get("start_time")
                if start_time:
                    import time
                    from datetime import datetime

                    if isinstance(start_time, datetime):
                        execution_time_ms = (_utc_now() - start_time).total_seconds() * 1000
                    elif isinstance(start_time, float):
                        execution_time_ms = (time.time() - start_time) * 1000

            # Build structured output data
            tool_output_data = {
                "tool_name": tool_name,
                "output": parsed_output,
                "status": "success",
            }

            # If output is a dict, include it as structured data
            if isinstance(parsed_output, dict):
                tool_output_data["result"] = parsed_output
            elif isinstance(parsed_output, str):
                tool_output_data["raw_output"] = parsed_output

            if execution_time_ms is not None:
                tool_output_data["execution_time_ms"] = execution_time_ms

            if hasattr(span, "set_output"):
                span.set_output(tool_output_data)

            # Store enhanced metadata
            if hasattr(span, "set_metadata"):
                current_metadata = getattr(span, "_metadata", {})
                enriched_metadata = dict(current_metadata)
                enriched_metadata["tool"] = {
                    "tool_name": tool_name,
                    "tool_type": span_context.get("tool_type", "tool"),
                }
                if span_context.get("tool_class"):
                    enriched_metadata["tool"]["tool_class"] = span_context["tool_class"]
                if span_context.get("function_name"):
                    enriched_metadata["tool"]["function_name"] = span_context["function_name"]
                if execution_time_ms is not None:
                    enriched_metadata["tool"]["execution_time_ms"] = execution_time_ms
                span.set_metadata(enriched_metadata)

            # Set agent_type for dashboard grouping
            if hasattr(span, "set_agent_type"):
                span.set_agent_type("tool")

            # Set latency for tools
            if hasattr(span, "set_latency") and execution_time_ms is not None:
                span.set_latency(execution_time_ms / 1000)  # Convert to seconds

            # Drift detection: record tool use
            if self._drift_detector:
                try:
                    tool_input = span_context.get("tool_input", {})
                    self._drift_detector.record_tool_use(
                        tool_name,
                        tool_input if isinstance(tool_input, dict) else {},
                        duration_ms=execution_time_ms or 0,
                        is_error=False,
                    )
                except Exception:
                    pass  # Don't fail on drift tracking

            # Track execution path end
            self._track_span_end(span, "tool", None)

            # Sync update — stamps end_time now, no async race.
            self._send_span_update(span, run_id, {}, None)

            # Restore process-level span ID to parent for OTel bridge
            try:
                from aigie.auto_instrument.span_enricher import set_active_span_id

                parent_run = span_context.get("parent_run_id")
                parent_span = (
                    self._span_contexts.get(parent_run, {}).get("span") if parent_run else None
                )
                set_active_span_id(getattr(parent_span, "id", None))
            except Exception:
                pass

            # Clean up
            del self._span_contexts[run_id]

    def on_chain_error(
        self,
        error: Exception,
        *,
        run_id: str,
        **kwargs: Any,
    ) -> None:
        """Called when a chain errors."""
        run_id = self._normalize_run_id(run_id)
        if run_id in self._span_contexts:
            span_context = self._span_contexts[run_id]
            span = span_context["span"]

            # Detect and classify error
            detected_error = None
            if self._error_detector:
                chain_name = span.name if hasattr(span, "name") else "chain"
                detected_error = self._error_detector.detect_from_exception(
                    error, f"chain:{chain_name}", {"run_id": run_id}
                )

            if hasattr(span, "set_output"):
                output = {
                    "error": str(error),
                    "error_type": type(error).__name__,
                    "status": "error",
                }
                if detected_error:
                    output["error_classification"] = {
                        "type": detected_error.error_type.value,
                        "severity": detected_error.severity.value,
                        "is_transient": detected_error.is_transient,
                    }
                span.set_output(output)

            # Set level and statusMessage for error using span methods
            if hasattr(span, "set_level"):
                span.set_level("ERROR", str(error))

            # Also store in metadata for backward compatibility
            if hasattr(span, "set_metadata"):
                current_metadata = getattr(span, "_metadata", {})
                enriched_metadata = dict(current_metadata)
                enriched_metadata["level"] = "ERROR"
                enriched_metadata["status_message"] = str(error)
                enriched_metadata["error_type"] = type(error).__name__
                if detected_error:
                    enriched_metadata["error_detection"] = {
                        "type": detected_error.error_type.value,
                        "severity": detected_error.severity.value,
                        "is_transient": detected_error.is_transient,
                        "message": detected_error.message,
                    }
                span.set_metadata(enriched_metadata)

            # Track execution path end with error
            self._track_span_end(span, "chain", error)

            # Sync update with error — stamps end_time now, no async race.
            self._send_span_update(span, run_id, {}, error)

            # If this is the root chain, complete the trace with error
            # (LangGraph wrapper owns lifecycle when _thread_id is set).
            if run_id == self._root_run_id and self._thread_id is None:
                self._schedule_trace_completion(error)

            del self._span_contexts[run_id]

    def on_llm_error(
        self,
        error: Exception,
        *,
        run_id: str,
        **kwargs: Any,
    ) -> None:
        """Called when an LLM errors."""
        run_id = self._normalize_run_id(run_id)
        if run_id in self._span_contexts:
            span_context = self._span_contexts[run_id]
            span = span_context["span"]

            # Detect and classify error
            detected_error = None
            if self._error_detector:
                model_name = span_context.get("model_name", "llm")
                detected_error = self._error_detector.detect_from_exception(
                    error, f"llm:{model_name}", {"run_id": run_id}
                )

            if hasattr(span, "set_output"):
                output = {
                    "error": str(error),
                    "error_type": type(error).__name__,
                    "status": "error",
                }
                if detected_error:
                    output["error_classification"] = {
                        "type": detected_error.error_type.value,
                        "severity": detected_error.severity.value,
                        "is_transient": detected_error.is_transient,
                    }
                span.set_output(output)

            # Set level and statusMessage for error using span methods
            if hasattr(span, "set_level"):
                span.set_level("ERROR", str(error))

            # Also store in metadata for backward compatibility
            if hasattr(span, "set_metadata"):
                current_metadata = getattr(span, "_metadata", {})
                enriched_metadata = dict(current_metadata)
                enriched_metadata["level"] = "ERROR"
                enriched_metadata["status_message"] = str(error)
                enriched_metadata["error_type"] = type(error).__name__
                if detected_error:
                    enriched_metadata["error_detection"] = {
                        "type": detected_error.error_type.value,
                        "severity": detected_error.severity.value,
                        "is_transient": detected_error.is_transient,
                        "message": detected_error.message,
                    }
                span.set_metadata(enriched_metadata)

            # Track execution path end with error
            self._track_span_end(span, "llm", error)

            # Sync update with error — stamps end_time now, no async race.
            self._send_span_update(span, run_id, {}, error)

            del self._span_contexts[run_id]

    def on_tool_error(
        self,
        error: Exception,
        *,
        run_id: str,
        **kwargs: Any,
    ) -> None:
        """Called when a tool errors."""
        run_id = self._normalize_run_id(run_id)
        if run_id in self._span_contexts:
            span_context = self._span_contexts[run_id]
            span = span_context["span"]

            # Detect and classify error
            detected_error = None
            if self._error_detector:
                tool_name = span_context.get("tool_name", "tool")
                detected_error = self._error_detector.detect_from_exception(
                    error, f"tool:{tool_name}", {"run_id": run_id}
                )

            # Record error in drift detector
            if self._drift_detector:
                tool_name = span_context.get("tool_name", "tool")
                tool_input = span_context.get("tool_input", {})
                self._drift_detector.record_tool_use(tool_name, tool_input, 0, is_error=True)

            if hasattr(span, "set_output"):
                output = {
                    "error": str(error),
                    "error_type": type(error).__name__,
                    "status": "error",
                }
                if detected_error:
                    output["error_classification"] = {
                        "type": detected_error.error_type.value,
                        "severity": detected_error.severity.value,
                        "is_transient": detected_error.is_transient,
                    }
                span.set_output(output)

            # Set level and statusMessage for error using span methods
            if hasattr(span, "set_level"):
                span.set_level("ERROR", str(error))

            # Also store in metadata for backward compatibility
            if hasattr(span, "set_metadata"):
                current_metadata = getattr(span, "_metadata", {})
                enriched_metadata = dict(current_metadata)
                enriched_metadata["level"] = "ERROR"
                enriched_metadata["status_message"] = str(error)
                enriched_metadata["error_type"] = type(error).__name__
                if detected_error:
                    enriched_metadata["error_detection"] = {
                        "type": detected_error.error_type.value,
                        "severity": detected_error.severity.value,
                        "is_transient": detected_error.is_transient,
                        "message": detected_error.message,
                    }
                span.set_metadata(enriched_metadata)

            # Track execution path end with error
            self._track_span_end(span, "tool", error)

            # Sync update with error — stamps end_time now, no async race.
            self._send_span_update(span, run_id, {}, error)

            del self._span_contexts[run_id]

    def on_retriever_start(
        self,
        serialized: dict[str, Any],
        query: str,
        *,
        run_id: str,
        parent_run_id: str | None = None,
        tags: list | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Called when a retriever starts (LangChain retrieval)."""
        if getattr(self, "_paused", False):
            return
        # Normalize run_ids to strings (LangChain may pass UUID objects)
        run_id = self._normalize_run_id(run_id)
        parent_run_id = self._normalize_run_id(parent_run_id)

        if not self.trace:
            return

        # --- Parent resolution: single path ---
        parent_span_id = self._resolve_parent(parent_run_id)

        # Extract retriever information
        retriever_name = "Retriever"
        retriever_type = "retriever"
        if serialized:
            retriever_name = serialized.get("name", "Retriever")
            retriever_id = serialized.get("id")
            if isinstance(retriever_id, list) and retriever_id:
                retriever_name = retriever_id[-1] if retriever_id else "Retriever"
                # Determine retriever type from class path
                if "vectorstore" in str(retriever_id).lower():
                    retriever_type = "vectorstore"
                elif "embedding" in str(retriever_id).lower():
                    retriever_type = "embedding"

        # Build retrieval input data
        retrieval_input = {
            "query": query,
            "retriever_name": retriever_name,
            "retriever_type": retriever_type,
        }

        # Extract additional parameters
        if kwargs:
            top_k = kwargs.get("k") or kwargs.get("top_k")
            if top_k:
                retrieval_input["top_k"] = top_k

        # Create span for retrieval
        span = self.trace.span(
            name=f"Retriever: {retriever_name}", type="retriever", parent=parent_span_id
        )

        # Calculate depth for this span
        depth = self._calculate_depth(run_id, parent_run_id)

        # Store span context
        self._span_contexts[run_id] = {
            "span": span,
            "parent_run_id": parent_run_id,
            "query": query,
            "retriever_name": retriever_name,
            "start_time": None,  # Will be set on entry
            "entered": False,
            "depth": depth,  # Depth level for flow visualization
        }

        # Track execution path for workflow execution data
        self._track_span_start(span, "retriever", f"Retriever: {retriever_name}")

        # Stamp start_time synchronously — eliminates async race on start_time.
        self._send_span_create(span, run_id, retrieval_input)

    def on_retriever_end(
        self,
        documents: list,
        *,
        run_id: str,
        **kwargs: Any,
    ) -> None:
        """Called when a retriever ends."""
        run_id = self._normalize_run_id(run_id)
        if run_id in self._span_contexts:
            span_context = self._span_contexts[run_id]
            span = span_context["span"]

            # Extract retrieved documents with metadata and scores
            retrieved_docs = []
            for doc in documents:
                content = doc.page_content if hasattr(doc, "page_content") else str(doc)
                doc_data = {
                    "content": content,
                    "content_preview": content[:200] if content else "",
                }
                # Extract metadata and scores
                if hasattr(doc, "metadata") and doc.metadata:
                    doc_data["metadata"] = doc.metadata
                    # Extract similarity/relevance score from multiple common keys
                    if isinstance(doc.metadata, dict):
                        score = (
                            doc.metadata.get("score")
                            or doc.metadata.get("similarity_score")
                            or doc.metadata.get("relevance_score")
                        )
                        # Also check distance-based scores (lower = better)
                        if score is None and "distance" in doc.metadata:
                            distance = doc.metadata["distance"]
                            with contextlib.suppress(TypeError, ValueError):
                                doc_data["distance"] = float(distance)
                        if score is not None:
                            doc_data["score"] = float(score)
                elif isinstance(doc, dict):
                    content = doc.get("page_content") or doc.get("content") or str(doc)
                    doc_data["content"] = content
                    doc_data["content_preview"] = content[:200] if content else ""
                    doc_data["metadata"] = doc.get("metadata", {})
                    if "score" in doc:
                        doc_data["score"] = float(doc["score"])
                    elif "relevance_score" in doc:
                        doc_data["score"] = float(doc["relevance_score"])

                retrieved_docs.append(doc_data)

            # Build structured output data
            output_data = {
                "retrieved_documents": retrieved_docs,
                "document_count": len(retrieved_docs),
                "status": "success",
            }

            # Extract query embedding info if available
            if kwargs and "query_embedding" in kwargs:
                output_data["query_embedding_dim"] = (
                    len(kwargs["query_embedding"])
                    if isinstance(kwargs["query_embedding"], list)
                    else None
                )

            if hasattr(span, "set_output"):
                span.set_output(output_data)

            # Store in metadata for analysis
            if hasattr(span, "set_metadata"):
                current_metadata = getattr(span, "_metadata", {})
                enriched_metadata = dict(current_metadata)
                enriched_metadata["retrieval"] = {
                    "document_count": len(retrieved_docs),
                    "retriever_name": span_context.get("retriever_name", "Retriever"),
                }
                # Store average similarity score if available
                scores = [
                    doc.get("score") for doc in retrieved_docs if doc.get("score") is not None
                ]
                if scores:
                    enriched_metadata["retrieval"]["avg_score"] = sum(scores) / len(scores)
                    enriched_metadata["retrieval"]["min_score"] = min(scores)
                    enriched_metadata["retrieval"]["max_score"] = max(scores)
                span.set_metadata(enriched_metadata)

            # Wire detect_from_retriever_result so ErrorDetector can classify
            # error payloads embedded in retriever output. Exceptions raised by
            # retrievers are handled in on_retriever_error.
            if self._error_detector is not None:
                try:
                    retriever_name = span_context.get("retriever_name", "Retriever")
                    self._error_detector.detect_from_retriever_result(
                        retriever_name=retriever_name,
                        run_id=run_id,
                        result=documents,
                        is_error_flag=False,
                    )
                except Exception as detection_exc:
                    logger.warning("[AIGIE] detect_from_retriever_result failed: %s", detection_exc)

            # Sync update — stamps end_time now, no async race.
            self._send_span_update(span, run_id, {}, None)

            # Clean up
            del self._span_contexts[run_id]

    def on_retriever_error(
        self,
        error: Exception,
        *,
        run_id: str,
        **kwargs: Any,
    ) -> None:
        """Called when a retriever errors."""
        run_id = self._normalize_run_id(run_id)
        if run_id in self._span_contexts:
            span_context = self._span_contexts[run_id]
            span = span_context["span"]
            if hasattr(span, "set_output"):
                span.set_output(
                    {"error": str(error), "error_type": type(error).__name__, "status": "error"}
                )

            # Sync update with error — stamps end_time now, no async race.
            self._send_span_update(span, run_id, {}, error)

            del self._span_contexts[run_id]

    def _track_span_start(self, span: Any, span_type: str, span_name: str) -> None:
        """Track span start for execution path tracking."""
        if not self.trace or not hasattr(self.trace, "id") or not self.trace.id:
            return

        trace_id = self.trace.id

        # Initialize tracking structures for this trace if needed
        if trace_id not in self._execution_paths:
            self._execution_paths[trace_id] = []
            self._execution_timing[trace_id] = {}
            self._execution_status[trace_id] = {}
            self._execution_errors[trace_id] = {}
            self._edge_conditions[trace_id] = []
            self._agent_iterations[trace_id] = {}
            self._span_start_times[trace_id] = {}
            self._retry_info[trace_id] = []
            self._state_transitions[trace_id] = []
            self._nested_workflows[trace_id] = []

        # Track agent, chain, tool, llm, and retriever spans in execution path
        if span_type in ["agent", "chain", "tool", "llm", "retriever"]:
            if span_name and span_name not in self._execution_paths[trace_id]:
                self._execution_paths[trace_id].append(span_name)

            # Record start time - use actual span start time if available, otherwise use current time
            if span_name:
                start_time = _utc_now_iso()
                # Try to get actual span start time if span has been entered
                # Note: We'll update this when span is actually entered with real timestamp
                self._span_start_times[trace_id][span_name] = start_time

                self._execution_timing[trace_id][span_name] = {
                    "start_time": start_time,
                    "end_time": None,
                    "duration_ms": 0,
                }
                self._execution_status[trace_id][span_name] = "running"

    def _track_span_end(self, span: Any, span_type: str, error: Exception | None = None) -> None:
        """Track span end for execution path tracking."""
        if not self.trace or not hasattr(self.trace, "id") or not self.trace.id:
            return

        trace_id = self.trace.id
        if trace_id not in self._execution_paths:
            return

        # Get span name
        span_name = None
        if hasattr(span, "name"):
            span_name = span.name
        elif hasattr(span, "_name"):
            span_name = span._name

        if not span_name:
            return

        # Track agent, chain, tool, llm, and retriever spans
        if span_type in [
            "agent",
            "chain",
            "tool",
            "llm",
            "retriever",
        ] and span_name in self._execution_timing.get(trace_id, {}):
            from datetime import datetime

            # Get actual end time - try to get from span if available, otherwise use current time
            end_time = _utc_now_iso()
            # Note: We'll update this when span actually exits with real timestamp

            # Record end time and calculate duration
            timing = self._execution_timing[trace_id][span_name]
            timing["end_time"] = end_time

            if timing.get("start_time"):
                try:
                    start_dt = datetime.fromisoformat(timing["start_time"].replace("Z", "+00:00"))
                    end_dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
                    duration_ms = int((end_dt - start_dt).total_seconds() * 1000)
                    timing["duration_ms"] = duration_ms
                except Exception:
                    pass

            # Update status
            if error:
                self._execution_status[trace_id][span_name] = "failed"
                self._execution_errors[trace_id][span_name] = str(error)

                # Track retry information if this is a retry
                # Check if this span was retried by looking at metadata or previous attempts
                if trace_id in self._retry_info:
                    # Check if this span name appears in retry info (indicating a previous retry)
                    existing_retries = [
                        r for r in self._retry_info[trace_id] if r.get("span_name") == span_name
                    ]
                    attempt_number = len(existing_retries) + 1
                    if attempt_number > 1:
                        from datetime import datetime

                        self._retry_info[trace_id].append(
                            {
                                "span_name": span_name,
                                "attempt": attempt_number,
                                "reason": str(error),
                                "timestamp": _utc_now_iso(),
                            }
                        )
            else:
                self._execution_status[trace_id][span_name] = "completed"

    def _track_edge_condition(self, step_name: str, condition: Any, result: Any = None) -> None:
        """Track edge condition/routing decision."""
        if not self.trace or not hasattr(self.trace, "id") or not self.trace.id:
            return

        trace_id = self.trace.id
        if trace_id not in self._edge_conditions:
            self._edge_conditions[trace_id] = []

        self._edge_conditions[trace_id].append(
            {
                "step": step_name,
                "condition": str(condition),
                "result": str(result) if result is not None else None,
            }
        )

    def _track_agent_iteration(self, agent_name: str) -> None:
        """Track agent iteration count."""
        if not self.trace or not hasattr(self.trace, "id") or not self.trace.id:
            return

        trace_id = self.trace.id
        if trace_id not in self._agent_iterations:
            self._agent_iterations[trace_id] = {}

        if agent_name not in self._agent_iterations[trace_id]:
            self._agent_iterations[trace_id][agent_name] = 0

        self._agent_iterations[trace_id][agent_name] += 1

    def _track_state_transition(
        self,
        from_state: str,
        to_state: str,
        trigger: str | None = None,
        transition_trigger: str | None = None,
    ) -> None:
        """Track state transition in stateful workflows."""
        if not self.trace or not hasattr(self.trace, "id") or not self.trace.id:
            return

        trace_id = self.trace.id
        if trace_id not in self._state_transitions:
            self._state_transitions[trace_id] = []

        self._state_transitions[trace_id].append(
            {
                "from_state": str(from_state),
                "to_state": str(to_state),
                "trigger": str(transition_trigger or trigger or "unknown"),
                "timestamp": _utc_now_iso(),
            }
        )

    def _track_nested_workflow(
        self, workflow_name: str, nested_trace_id: str | None = None
    ) -> None:
        """Track nested workflow execution."""
        if not self.trace or not hasattr(self.trace, "id") or not self.trace.id:
            return

        trace_id = self.trace.id
        if trace_id not in self._nested_workflows:
            self._nested_workflows[trace_id] = []

        self._nested_workflows[trace_id].append(
            {
                "workflow_name": workflow_name,
                "nested_trace_id": nested_trace_id,
                "timestamp": _utc_now_iso(),
            }
        )

    def get_execution_data(self) -> dict[str, Any] | None:
        """Get execution data for the current trace."""
        import logging

        logger = logging.getLogger(__name__)

        if not self.trace or not hasattr(self.trace, "id") or not self.trace.id:
            logger.debug("No trace available for execution data")
            return None

        trace_id = self.trace.id
        if trace_id not in self._execution_paths:
            logger.debug(f"No execution paths tracked for trace {trace_id}")
            return None

        try:
            execution_data = {
                "execution_path": self._execution_paths.get(trace_id, []),
                "execution_timing": self._execution_timing.get(trace_id, {}),
                "execution_status": self._execution_status.get(trace_id, {}),
                "execution_errors": self._execution_errors.get(trace_id, {}),
            }

            # Validate execution data
            if not execution_data["execution_path"]:
                logger.debug(f"Empty execution path for trace {trace_id}")
                # Still return data even if empty - let backend decide

            # Add edge conditions if available
            if self._edge_conditions.get(trace_id):
                execution_data["edge_conditions"] = self._edge_conditions[trace_id]

            # Add agent iterations if available
            if self._agent_iterations.get(trace_id):
                execution_data["agent_iterations"] = self._agent_iterations[trace_id]

            # Add retry information if available
            if self._retry_info.get(trace_id):
                execution_data["retry_info"] = self._retry_info[trace_id]

            # Add state transitions if available
            if self._state_transitions.get(trace_id):
                execution_data["state_transitions"] = self._state_transitions[trace_id]

            # Add nested workflows if available
            if self._nested_workflows.get(trace_id):
                execution_data["nested_workflows"] = self._nested_workflows[trace_id]

            # Validate timing data consistency
            for span_name in execution_data["execution_path"]:
                if span_name in execution_data["execution_timing"]:
                    timing = execution_data["execution_timing"][span_name]
                    if "start_time" not in timing:
                        logger.warning(
                            f"Missing start_time for span {span_name} in trace {trace_id}"
                        )
                    # end_time may be missing if span is still running

            logger.debug(
                f"Retrieved execution data for trace {trace_id}: {len(execution_data.get('execution_path', []))} steps"
            )
            return execution_data

        except Exception as e:
            logger.error(f"Error getting execution data for trace {trace_id}: {e}", exc_info=True)
            # Return minimal data on error
            return {
                "execution_path": self._execution_paths.get(trace_id, []),
                "execution_timing": {},
                "execution_status": {},
                "execution_errors": {},
            }

    def _send_span_create(self, span: Any, run_id: str, input_data: dict[str, Any]) -> None:
        """Send span creation directly to buffer (synchronous, thread-safe)."""
        from uuid import uuid4

        if not self.trace:
            logger.warning("[AIGIE] _send_span_create: no trace for span %s", run_id)
            return

        # Generate span ID if not already set
        if not hasattr(span, "id") or not span.id:
            span.id = str(uuid4())

        # Get trace ID
        trace_id = self.trace.id if hasattr(self.trace, "id") else None
        if not trace_id:
            logger.warning("[AIGIE] _send_span_create: no trace_id for span %s", run_id)
            return

        # Duplicate span-ID detection (indicates a callback race or double-patch)
        if not hasattr(self, "_created_span_ids"):
            self._created_span_ids: set = set()
        if span.id in self._created_span_ids:
            logger.error(
                "[AIGIE] _send_span_create: DUPLICATE span_id=%s name=%s run_id=%s\n%s",
                span.id,
                span.name if hasattr(span, "name") else "unknown",
                run_id,
                "".join(traceback.format_stack()),
            )
        else:
            self._created_span_ids.add(span.id)

        # Build span data payload (similar to LangGraphHandler)
        start_time = _utc_now()
        span_data = {
            "id": span.id,
            "trace_id": trace_id,
            "parent_id": span.parent_id if hasattr(span, "parent_id") else None,
            "name": span.name if hasattr(span, "name") else "chain_step",
            "type": span.span_type if hasattr(span, "span_type") else "chain",
            "input": input_data,
            "metadata": span._metadata if hasattr(span, "_metadata") else {},
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        # Include model for LLM spans so it's captured in the initial SPAN_CREATE event
        if hasattr(span, "_model") and span._model:
            span_data["model"] = span._model

        # Mark as entered for proper cleanup
        if run_id in self._span_contexts:
            self._span_contexts[run_id]["entered"] = True
            self._span_contexts[run_id]["entry_failed"] = False
            self._span_contexts[run_id]["span_data"] = span_data

        logger.debug(
            "[AIGIE] span_create name=%s id=%s run_id=%s trace=%s handler=%s",
            span_data.get("name"),
            span_data.get("id", "N/A")[:8],
            run_id[:8] if run_id else "?",
            trace_id[:8] if trace_id else "?",
            id(self),  # handler instance id — same value = same handler, different = double-handler
        )

        # Directly add to buffer's deque (thread-safe, no async needed)
        try:
            aigie = self.aigie
            if not aigie:
                from aigie.client import get_aigie

                aigie = get_aigie()

            if aigie and aigie._buffer:
                self._emit_span_create(aigie, span_data)
            else:
                logger.warning(
                    "[AIGIE] _send_span_create: no buffer, span lost: %s", span_data.get("name")
                )
        except Exception as e:
            logger.debug(f"Failed to add span to buffer {run_id}: {e}")

    def _send_span_update(
        self, span: Any, run_id: str, outputs: dict[str, Any], error: Exception | None = None
    ) -> None:
        """Send span update directly to buffer (synchronous, thread-safe)."""
        if not self.trace:
            return

        span_id = span.id if hasattr(span, "id") else None
        if not span_id:
            return

        trace_id = self.trace.id if hasattr(self.trace, "id") else None
        if not trace_id:
            return

        end_time = _utc_now()
        duration_ns = 0
        start_time_iso = None
        span_data_ctx: dict = {}

        if run_id in self._span_contexts:
            ctx = self._span_contexts[run_id]
            span_data_ctx = ctx.get("span_data", {})
            start_time_iso = span_data_ctx.get("start_time")
            if start_time_iso is None:
                # Fall back to the ctx-level start datetime when span_data is absent.
                start_dt = ctx.get("start_time_chain") or ctx.get("start_time")
                if isinstance(start_dt, datetime):
                    start_time_iso = start_dt.isoformat()
            if start_time_iso is None:
                logger.warning(
                    "[AIGIE] _send_span_update: missing start_time for span %s", span_id[:8]
                )
            elif start_time_iso:
                with contextlib.suppress(Exception):
                    duration_ns = int(
                        (end_time - datetime.fromisoformat(start_time_iso)).total_seconds()
                        * 1_000_000_000
                    )

        update_data = {
            "id": span_id,
            "trace_id": trace_id,
            "name": span.name if hasattr(span, "name") else span_data_ctx.get("name"),
            "type": span.span_type if hasattr(span, "span_type") else span_data_ctx.get("type"),
            "start_time": start_time_iso,
            "end_time": end_time.isoformat(),
            "input": span_data_ctx.get("input"),
            "output": outputs if outputs else (span._output if hasattr(span, "_output") else None),
            "metadata": span._metadata
            if hasattr(span, "_metadata")
            else span_data_ctx.get("metadata"),
            "status": "error" if error else "success",
            "duration_ns": duration_ns,
            "parent_id": span.parent_id
            if hasattr(span, "parent_id")
            else span_data_ctx.get("parent_id"),
            "latency_seconds": duration_ns / 1_000_000_000 if duration_ns else None,
        }

        if hasattr(span, "_model") and span._model:
            update_data["model"] = span._model
        for usage_attr in ("_input_tokens", "_output_tokens", "_total_tokens", "_cost"):
            if hasattr(span, usage_attr) and getattr(span, usage_attr) is not None:
                update_data[usage_attr.lstrip("_")] = getattr(span, usage_attr)

        if error:
            update_data["error"] = str(error)
            update_data["error_message"] = str(error)

        logger.debug(
            "[AIGIE] span_update name=%s id=%s dur_ms=%.1f",
            update_data.get("name"),
            span_id[:8],
            duration_ns / 1_000_000 if duration_ns else 0,
        )

        # Directly add to buffer's deque (thread-safe operation)
        try:
            aigie = self.aigie
            if not aigie:
                from aigie.client import get_aigie

                aigie = get_aigie()

            if aigie and aigie._buffer:
                self._emit_span_update(aigie, update_data)
                logger.debug(
                    f"Added span update to buffer: {span_id[:8]} status={update_data.get('status')}"
                )
            else:
                logger.debug(
                    f"No aigie/buffer to send span update: {span_id[:8] if span_id else 'unknown'}"
                )
        except Exception as e:
            logger.debug(f"Failed to add span update to buffer {run_id}: {e}")

        # Autonomous v2: dispatch to AutonomousRuntime.on_span_complete so
        # FlowEvaluator can evaluate the span against the flow cache. Never raises.
        self._dispatch_to_autonomous(span, trace_id, span_id, error)

    def _dispatch_to_autonomous(
        self,
        span: Any,
        trace_id: str,
        span_id: str,
        error: Exception | None,
    ) -> None:
        """Fire AutonomousRuntime.on_span_complete for this completed span.

        Builds a duck-typed SpanView-compatible adapter and forwards to the
        runtime. Failures are logged at debug and never propagate.
        """
        try:
            aigie = self.aigie
            if not aigie:
                from aigie.client import get_aigie

                aigie = get_aigie()
            runtime = getattr(aigie, "_autonomous_runtime", None) if aigie else None
            if runtime is None:
                return

            attrs: dict[str, Any] = {
                "trace_id": trace_id,
                "span_id": span_id,
            }
            framework = getattr(aigie, "_framework", None)
            if framework:
                attrs["agent.framework"] = framework
            if error is not None:
                attrs["agent.error.class"] = type(error).__name__
            metadata = getattr(span, "_metadata", None)
            if isinstance(metadata, dict):
                if metadata.get("workflow_id"):
                    attrs["agent.workflow.id"] = metadata["workflow_id"]
                if metadata.get("tool_name"):
                    attrs["agent.tool.name"] = metadata["tool_name"]
                if metadata.get("status_code"):
                    attrs["agent.status_code"] = metadata["status_code"]

            runtime.on_span_complete(SimpleNamespace(attributes=attrs, framework_handle=None))
        except Exception:  # noqa: BLE001
            logger.exception("AutonomousRuntime.on_span_complete failed")

    def _send_agent_plan_update(self, source: str) -> None:
        """Send agent_plan metadata via TRACE_UPDATE to buffer."""
        if not self._drift_detector or not self.trace:
            return

        # Check config toggle
        try:
            from aigie.integrations.langgraph.config import LangGraphConfig

            config = LangGraphConfig.from_env()
            if not config.capture_agent_plan:
                return
        except ImportError:
            pass  # If config not available, proceed with default (enabled)

        trace_id = self.trace.id if hasattr(self.trace, "id") else None
        if not trace_id:
            return

        try:
            plan_metadata = self._drift_detector.get_plan_metadata(source=source)
            if not plan_metadata:
                return

            update_data = {
                "id": trace_id,
                "metadata": {
                    "agent_plan": plan_metadata,
                },
            }

            aigie = self.aigie
            if not aigie:
                from aigie.client import get_aigie

                aigie = get_aigie()

            if aigie and aigie._buffer:
                self._emit_trace_update(aigie, update_data)
                self._plan_sent = True
                logger.debug(f"Sent agent_plan update for trace {trace_id[:8]}, source={source}")
            else:
                logger.debug(
                    f"No aigie/buffer for agent_plan update: {trace_id[:8] if trace_id else 'unknown'}"
                )
        except Exception as e:
            logger.debug(f"Failed to send agent_plan update: {e}")

    def _close_pending_spans(self, status: str = "paused") -> None:
        """Close open spans on interrupt/subgraph completion.

        Uses _schedule_span_exit so span.__aexit__() → buffer.add() → flush
        is triggered, ensuring end_time reaches the DB. Direct buffer append
        (_emit_paused_span_update) is unreliable because it bypasses the flush
        scheduler.

        NOTE: Safe to call after LangChain's on_llm_end / on_chain_end have
        already fired for completed spans (LangChain fires end-callbacks
        synchronously before GraphInterrupt propagates). Only genuinely-open
        spans remain at this point.
        """
        trace_id = self.trace.id if self.trace and hasattr(self.trace, "id") else None
        if not trace_id:
            self._paused = True
            return
        aigie = self.aigie
        if not aigie:
            try:
                from aigie.client import get_aigie

                aigie = get_aigie()
            except Exception:
                aigie = None
        if not (aigie and aigie._buffer):
            self._span_contexts.clear()
            self._paused = True
            return

        end_time = _utc_now()
        for _run_id, ctx in list(self._span_contexts.items()):
            span = ctx.get("span")
            span_id = span.id if span and hasattr(span, "id") else None
            if not span_id:
                continue
            # Gateway requires start_time: span_data iso stamp, then ctx datetime,
            # then end_time as a zero-duration last resort.
            start_iso = ctx.get("span_data", {}).get("start_time")
            start_dt = ctx.get("start_time_chain") or ctx.get("start_time")
            if start_dt is None and start_iso:
                with contextlib.suppress(ValueError):
                    start_dt = datetime.fromisoformat(start_iso)
            if start_iso is None:
                start_iso = start_dt.isoformat() if start_dt else end_time.isoformat()
            duration_ns = 0
            if start_dt:
                duration_ns = int((end_time - start_dt).total_seconds() * 1_000_000_000)
            self._emit_span_update(
                aigie,
                {
                    "id": span_id,
                    "trace_id": trace_id,
                    "status": status,
                    "start_time": start_iso,
                    "end_time": end_time.isoformat(),
                    "duration_ns": duration_ns,
                    "metadata": {"pending_cleanup": True},
                },
            )
        self._span_contexts.clear()
        self._emit_trace_update(aigie, {"id": trace_id, "status": "paused"})
        self._paused = True
        # Flush SPAN_UPDATE events synchronously: yield once to let queued
        # _exit_span coroutines run (they call buffer.add()), then flush.
        _aigie = self.aigie
        _bg = getattr(_aigie, "_bg_loop", None) if _aigie else None
        _buf = getattr(_aigie, "_buffer", None) if _aigie else None
        if _bg is not None and _bg.is_running() and _buf is not None:

            async def _yield_flush(b: Any) -> None:
                await asyncio.sleep(0)
                await b.flush()

            coro = _yield_flush(_buf)
            try:
                asyncio.run_coroutine_threadsafe(coro, _bg).result(timeout=2.0)
            except Exception:
                coro.close()  # prevent RuntimeWarning about unawaited coroutine

    def _finalize_run(
        self, outputs: dict[str, Any] | None = None, error: Exception | None = None
    ) -> None:
        """Finalize the current run: drift report, trace update, registry cleanup.

        Idempotent — safe to call once per logical graph run. Used both by the
        normal on_chain_end path (no thread stitching) and by the LangGraph
        auto-instrument wrapper (which calls this once the graph confirms END).
        """
        # Pause this handler immediately so subsequent outer-graph callbacks
        # (e.g. from langgraph_swarm routing after a sub-agent finishes) don't
        # create new spans on a finalized handler.
        self._paused = True

        # In LangGraph mode, drain any spans still open in _span_contexts. This
        # handles the case where LangGraph fires on_chain_start for routing
        # supersteps without a matching on_chain_end (e.g. langgraph_swarm fires
        # multiple outer-graph on_chain_start events but only one on_chain_end).
        # Use _send_span_update (direct buffer) + synchronous flush so end_times
        # are guaranteed to reach the DB before this method returns — fire-and-
        # forget _schedule_span_exit is unreliable here because the process may
        # exit before the bg_loop processes the queued coroutines.
        # Drain any open spans remaining in _span_contexts that were missed by
        # on_chain_end (e.g. LangGraph routing supersteps that fire on_chain_start
        # without a matching on_chain_end, as seen in langgraph_swarm). Events are
        # added to the buffer and the buffer is flushed synchronously by
        # _finalize_if_graph_done after _finalize_run returns.
        if getattr(self, "_langgraph_mode", False) and self._span_contexts:
            for _run_id in list(self._span_contexts.keys()):
                _ctx = self._span_contexts.get(_run_id, {})
                _span = _ctx.get("span")
                if _span:
                    self._send_span_update(_span, _run_id, None, error)

        # Drift detection: finalize and attach report to trace
        if self._drift_detector:
            try:
                drifts = self._drift_detector.finalize(
                    total_duration_ms=0,
                    total_tokens=0,
                    total_cost=0,
                    final_output=str(outputs)[:500] if outputs else None,
                )
                if drifts:
                    drift_report = {
                        "plan": self._drift_detector.plan.to_dict(),
                        "execution": self._drift_detector.execution.to_dict(),
                        "drifts": [d.to_dict() for d in drifts],
                        "drift_count": len(drifts),
                    }
                    logger.info(f"Drift detection report: {len(drifts)} drifts found")
                    if hasattr(self.trace, "set_metadata"):
                        trace_meta = getattr(self.trace, "_metadata", {}) or {}
                        trace_meta["drift_report"] = drift_report
                        self.trace.set_metadata(trace_meta)
            except Exception as e:
                logger.debug(f"Drift finalization error: {e}")
            self._drift_detector = DriftDetector() if HAS_DETECTION else None
            self._plan_sent = False

        self._send_trace_update(error)

        from aigie.auto_instrument.trace import clear_current_trace, pop_thread_trace

        clear_current_trace()
        # Only the handler that created the trace (not sub-invocation handlers
        # that reused it) should evict it from the thread registry.
        if getattr(self, "_is_trace_owner", True):
            pop_thread_trace(self._thread_id)

    def _send_trace_update(self, error: Exception | None = None) -> None:
        """Send trace update directly to buffer (synchronous, thread-safe)."""
        import logging

        logger = logging.getLogger(__name__)

        if not self.trace:
            return

        trace_id = self.trace.id if hasattr(self.trace, "id") else None
        if not trace_id:
            return

        end_time = _utc_now()

        # Get execution data
        execution_data = self.get_execution_data()

        # Build execution plan summary
        execution_plan = {
            "agent": getattr(self.trace, "name", "LangChain") if self.trace else "LangChain",
            "tool_calls": self._total_tool_calls,
            "turn_count": self._turn_count,
            "status": "error" if error else "success",
        }

        # Build update payload
        update_data = {
            "id": trace_id,
            "status": "error" if error else "success",
            "end_time": end_time.isoformat(),
        }

        if error:
            update_data["error"] = str(error)
            update_data["error_message"] = str(error)
            update_data["error_type"] = type(error).__name__

        if execution_data:
            update_data["execution_data"] = execution_data

        # Include trace metadata (drift report, etc.) merged with execution_plan
        # Try both .metadata (TraceContext) and ._metadata (legacy) attributes
        trace_metadata = dict(
            getattr(self.trace, "metadata", None) or getattr(self.trace, "_metadata", None) or {}
        )
        trace_metadata["execution_plan"] = execution_plan
        trace_metadata["turn_count"] = self._turn_count
        update_data["metadata"] = trace_metadata

        # Directly add to buffer's deque (thread-safe operation)
        try:
            aigie = self.aigie
            if not aigie:
                from aigie.client import get_aigie

                aigie = get_aigie()

            if aigie and aigie._buffer:
                self._emit_trace_update(aigie, update_data)
                logger.debug(
                    f"Added trace update to buffer: {trace_id[:8]} status={update_data.get('status')}"
                )
            else:
                logger.debug(
                    f"No aigie/buffer to send trace update: {trace_id[:8] if trace_id else 'unknown'}"
                )
        except Exception as e:
            logger.debug(f"Failed to add trace update to buffer: {e}")

    def _fire_and_forget(self, coro) -> None:
        """Submit a coroutine to the SDK's isolated background loop.

        NEVER uses the agent's event loop. All SDK I/O runs in the dedicated
        background thread created by _run_async_init(), so connectivity issues
        or slow backend calls cannot affect agent execution.
        """
        import threading

        bg_loop = getattr(self.aigie, "_bg_loop", None) if self.aigie else None
        if bg_loop is not None and bg_loop.is_running():
            # Route to the SDK's isolated background thread — zero impact on agent.
            asyncio.run_coroutine_threadsafe(coro, bg_loop)
            return

        # Aigie was initialised directly (await aigie.initialize()) without a
        # background loop. Spin up a daemon thread so we still never block the
        # agent's event loop.
        def _run_in_thread() -> None:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                new_loop.run_until_complete(coro)
            except Exception:
                pass
            finally:
                new_loop.close()

        try:
            threading.Thread(target=_run_in_thread, daemon=True).start()
        except RuntimeError:
            pass  # process is shutting down — drop the coroutine

    def _schedule_trace_completion(self, error: Exception | None = None) -> None:
        """Schedule async trace completion from sync callback."""
        if not self.trace:
            return

        from aigie.utils.safe import schedule_async

        schedule_async(self._complete_trace(error))

    async def _complete_trace(self, error: Exception | None = None) -> None:
        """Complete the trace asynchronously."""
        import logging

        logger = logging.getLogger(__name__)

        try:
            if self.trace:
                # Get execution data from callback handler and pass to trace
                execution_data = self.get_execution_data()
                if execution_data:
                    self.trace.set_callback_execution_data(execution_data)
                    logger.debug(
                        f"Set execution data for trace {self.trace.id if hasattr(self.trace, 'id') else 'unknown'}"
                    )
                else:
                    logger.debug("No execution data available for trace completion")

                # Exit the trace (this sets end_time and finalizes status)
                await self.trace.__aexit__(type(error) if error else None, error, None)
                logger.debug("Trace completion finished")
        except Exception as e:
            logger.error(f"Failed to complete trace: {e}", exc_info=True)
            # Try to ensure trace is marked as failed even if completion fails
            try:
                if self.trace and hasattr(self.trace, "complete"):
                    await self.trace.complete(status="failure", error=e)
            except Exception:
                pass
