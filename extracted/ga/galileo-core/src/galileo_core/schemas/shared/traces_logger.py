from collections import deque
from contextvars import ContextVar
from datetime import datetime
from json import dumps
from typing import Any, Deque, Dict, List, Mapping, Optional

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from pydantic.types import UUID4

from galileo_core.schemas.logging.agent import AgentType
from galileo_core.schemas.logging.llm import Event
from galileo_core.schemas.logging.span import (
    AgentSpan,
    LlmMetrics,
    LlmSpan,
    LlmSpanAllowedInputType,
    LlmSpanAllowedOutputType,
    RetrieverSpan,
    Span,
    StepWithChildSpans,
    ToolSpan,
    WorkflowSpan,
)
from galileo_core.schemas.logging.step import Metrics
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.shared.document import Document
from galileo_core.utils.json import PydanticJsonEncoder


class TracesLogger(BaseModel):
    """Logger for managing traces and spans with async-safe parent tracking.

    Each TracesLogger instance maintains its own isolated ContextVar for tracking
    the current parent in the trace hierarchy. This allows:
    - Multiple TracesLogger instances to operate independently
    - Async-safe parent tracking within each instance (via ContextVar semantics)
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    traces: List[Trace] = Field(default_factory=list, description="List of traces.")

    # Per-instance ContextVar for async-safe parent tracking.
    # Each instance has its own ContextVar, providing isolation between logger instances.
    _parent_context_var: ContextVar[Optional[StepWithChildSpans]] = PrivateAttr()

    def _create_context_var(self) -> None:
        """Create a new ContextVar for this instance.

        Each instance must have its own ContextVar to maintain isolation.
        """
        self._parent_context_var = ContextVar(f"_current_parent_{id(self)}", default=None)

    def model_post_init(self, __context: Any) -> None:
        """Initialize the per-instance ContextVar after model construction."""
        self._create_context_var()

    def model_copy(self, *, update: Optional[Mapping[str, Any]] = None, deep: bool = False) -> "TracesLogger":
        """Override model_copy to create a fresh ContextVar on the copy.

        Pydantic's model_copy bypasses model_post_init and would share the
        same ContextVar reference, so we must create a new one for isolation.
        """
        copied = super().model_copy(update=update, deep=deep)
        copied._create_context_var()
        return copied

    def __copy__(self) -> "TracesLogger":
        """Create fresh ContextVar when using copy.copy()."""
        copied = super().__copy__()
        copied._create_context_var()
        return copied

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None) -> "TracesLogger":
        """Create fresh ContextVar when using copy.deepcopy().

        ContextVar objects cannot be pickled, so we must handle deepcopy
        by creating a new instance with deepcopied data, then creating
        a fresh ContextVar.
        """
        import copy

        if memo is None:
            memo = {}

        # Deepcopy the traces (the main data)
        copied_traces = copy.deepcopy(self.traces, memo)

        # Create new instance with copied data
        copied = TracesLogger(traces=copied_traces)
        # model_post_init already creates the ContextVar for new instances

        # Register in memo to handle circular references
        memo[id(self)] = copied

        return copied

    def _set_current_parent(self, parent: Optional[StepWithChildSpans]) -> None:
        """Set the current parent for the current async context."""
        self._parent_context_var.set(parent)

    def current_parent(self) -> Optional[StepWithChildSpans]:
        """Get the current parent span/trace for the current async context."""
        return self._parent_context_var.get()

    def reset_parent_tracking(self) -> None:
        """Reset the current parent tracking for this logger instance.

        Call this when reinitializing the logger or switching contexts.
        """
        self._parent_context_var.set(None)

    @property
    def _parent_stack(self) -> Deque[StepWithChildSpans]:
        """Reconstruct the parent stack by walking up the _parent chain.

        This property provides backward compatibility for code that accesses
        _parent_stack directly. The returned deque represents the path from
        root to current position.

        Note: This is a read-only view. Mutations to this deque will not
        affect the actual parent tracking. Use the span methods instead.
        """
        path: List[StepWithChildSpans] = []
        current = self.current_parent()
        while current is not None:
            path.append(current)
            current = current._parent
        # Reverse to get root-to-current order (like a stack bottom-to-top)
        return deque(reversed(path))

    @_parent_stack.setter
    def _parent_stack(self, value: Deque[StepWithChildSpans]) -> None:
        """Set the current parent from a deque (for backward compatibility).

        If deque is empty, clears the current parent.
        Otherwise, sets current parent to the last item and rebuilds _parent chain.
        """
        if not value:
            self._set_current_parent(None)
            return

        # Build the _parent chain from the deque
        items = list(value)
        for i, item in enumerate(items):
            if i == 0:
                item._parent = None
            else:
                item._parent = items[i - 1]

        # Set current parent to the top of the stack (last item)
        self._set_current_parent(items[-1])

    def add_child_span_to_parent(self, span: Span) -> None:
        current_parent = self.current_parent()
        if current_parent is None:
            raise ValueError("A trace needs to be created in order to add a span.")
        span.dataset_input = current_parent.dataset_input
        span.dataset_output = current_parent.dataset_output
        span.dataset_metadata = current_parent.dataset_metadata
        current_parent.add_child_span(span)

    def _get_child_span_timestamp(self) -> datetime:
        """Gets a unique timestamp for a child span from its parent."""
        parent = self.current_parent()
        if not parent:
            raise ValueError("A parent trace or span is required to generate a timestamp.")
        return parent._generate_unique_timestamp()

    def add_trace(
        self,
        input: str,
        redacted_input: Optional[str] = None,
        output: Optional[str] = None,
        redacted_output: Optional[str] = None,
        name: Optional[str] = None,
        created_at: Optional[datetime] = None,
        duration_ns: Optional[int] = None,
        user_metadata: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        dataset_input: Optional[str] = None,
        dataset_output: Optional[str] = None,
        dataset_metadata: Optional[Dict[str, str]] = None,
        external_id: Optional[str] = None,
        id: Optional[UUID4] = None,
    ) -> Trace:
        """
        Create a new trace and add it to the list of traces.
        Simple usage:
        ```
        my_traces.add_trace("input")
        my_traces.add_llm_span("input", "output", model="<my_model>")
        my_traces.conclude("output")
        ```
        Parameters:
        ----------
            input: str: Input to the node.
            redacted_input: Optional[str]: Redacted input to the node.
            output: Optional[str]: Output of the node.
            redacted_output: Optional[str]: Redacted output of the node.
            name: Optional[str]: Name of the trace.
            duration_ns: Optional[int]: Duration of the trace in nanoseconds.
            created_at: Optional[datetime]: Timestamp of the trace's creation.
            user_metadata: Optional[Dict[str, str]]: Metadata associated with this trace.
            ground_truth: Optional[str]: Ground truth, expected output of the trace.
        Returns:
        -------
            Trace: The created trace.
        """
        if self.current_parent() is not None:
            raise ValueError("You must conclude the existing trace before adding a new one.")
        trace = Trace(
            input=input,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at=created_at,
            user_metadata=user_metadata,
            tags=tags,
            metrics=Metrics(duration_ns=duration_ns),
            dataset_input=dataset_input,
            dataset_output=dataset_output,
            dataset_metadata=dataset_metadata if dataset_metadata is not None else {},
            external_id=external_id,
            id=id,
        )
        trace._parent = None  # Trace is root
        self.traces.append(trace)
        self._set_current_parent(trace)
        return trace

    def add_single_llm_span_trace(
        self,
        input: LlmSpanAllowedInputType,
        output: LlmSpanAllowedOutputType,
        model: Optional[str],
        redacted_input: Optional[LlmSpanAllowedInputType] = None,
        redacted_output: Optional[LlmSpanAllowedOutputType] = None,
        tools: Optional[List[Dict]] = None,
        events: Optional[List[Event]] = None,
        name: Optional[str] = None,
        created_at: Optional[datetime] = None,
        duration_ns: Optional[int] = None,
        user_metadata: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        num_input_tokens: Optional[int] = None,
        num_output_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        status_code: Optional[int] = None,
        time_to_first_token_ns: Optional[int] = None,
        dataset_input: Optional[str] = None,
        dataset_output: Optional[str] = None,
        dataset_metadata: Optional[Dict[str, str]] = None,
        trace_id: Optional[UUID4] = None,
        span_id: Optional[UUID4] = None,
        span_step_number: Optional[int] = None,
    ) -> Trace:
        """
        Create a new trace with a single span and add it to the list of traces.

        Parameters:
        ----------
            input: LlmStepAllowedIOType: Input to the node.
            output: LlmStepAllowedIOType: Output of the node.
            model: str: Model used for this span. Feedback from April: Good docs about what model names we use.
            redacted_input: Optional[LlmStepAllowedIOType]: Redacted input to the node.
            redacted_output: Optional[LlmStepAllowedIOType]: Redacted output of the node
            tools: Optional[List[Dict]]: List of available tools passed to LLM on invocation.
            events: Optional[List[Event]]: List of reasoning, internal tool call, or MCP events.
            name: Optional[str]: Name of the span.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at: Optional[datetime]: Timestamp of the span's creation.
            user_metadata: Optional[Dict[str, str]]: Metadata associated with this span.
            num_input_tokens: Optional[int]: Number of input tokens.
            num_output_tokens: Optional[int]: Number of output tokens.
            total_tokens: Optional[int]: Total number of tokens.
            temperature: Optional[float]: Temperature used for generation.
            ground_truth: Optional[str]: Ground truth, expected output of the workflow.
            status_code: Optional[int]: Status code of the node execution.
            time_to_first_token_ns: Optional[int]: Time until the first token was returned.
            dataset_input: Optional[str]: Dataset input for the span.
            dataset_output: Optional[str]: Dataset output for the span.
            dataset_metadata: Optional[Dict[str, str]]: Dataset metadata for the span.
            trace_id: Optional[UUID4]: ID of the trace.
            span_id: Optional[UUID4]: ID of the span.
            span_step_number: Optional[int]: Step number of the span.
        Returns:
        -------
            Trace: The created trace.
        """
        if self.current_parent() is not None:
            raise ValueError("A trace cannot be created within a parent trace or span, it must always be the root.")

        trace = Trace(
            input=dumps(input, cls=PydanticJsonEncoder),
            redacted_input=dumps(redacted_input, cls=PydanticJsonEncoder) if redacted_input else None,
            output=dumps(output, cls=PydanticJsonEncoder),
            redacted_output=dumps(redacted_output, cls=PydanticJsonEncoder) if redacted_output else None,
            name=name,
            created_at=created_at,
            user_metadata=user_metadata,
            tags=tags,
            dataset_input=dataset_input,
            dataset_output=dataset_output,
            dataset_metadata=dataset_metadata if dataset_metadata is not None else {},
            id=trace_id,
        )
        trace.add_child_span(
            LlmSpan(
                name=name,
                created_at=created_at,
                user_metadata=user_metadata,
                tags=tags,
                input=input,
                redacted_input=redacted_input,
                output=output,
                redacted_output=redacted_output,
                metrics=LlmMetrics(
                    duration_ns=duration_ns,
                    num_input_tokens=num_input_tokens,
                    num_output_tokens=num_output_tokens,
                    num_total_tokens=total_tokens,
                    time_to_first_token_ns=time_to_first_token_ns,
                ),
                tools=tools,
                events=events,
                model=model,
                temperature=temperature,
                status_code=status_code,
                dataset_input=dataset_input,
                dataset_output=dataset_output,
                dataset_metadata=dataset_metadata if dataset_metadata is not None else {},
                id=span_id,
                step_number=span_step_number,
            )
        )
        self.traces.append(trace)
        # Single span traces are automatically concluded so we reset the current parent.
        self._set_current_parent(None)
        return trace

    def add_llm_span(
        self,
        input: LlmSpanAllowedInputType,
        output: LlmSpanAllowedOutputType,
        model: Optional[str],
        redacted_input: Optional[LlmSpanAllowedInputType] = None,
        redacted_output: Optional[LlmSpanAllowedOutputType] = None,
        tools: Optional[List[Dict]] = None,
        events: Optional[List[Event]] = None,
        name: Optional[str] = None,
        created_at: Optional[datetime] = None,
        duration_ns: Optional[int] = None,
        user_metadata: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        num_input_tokens: Optional[int] = None,
        num_output_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        status_code: Optional[int] = None,
        time_to_first_token_ns: Optional[int] = None,
        id: Optional[UUID4] = None,
        step_number: Optional[int] = None,
    ) -> LlmSpan:
        """
        Add a new llm span to the current parent.

        Parameters:
        ----------
            input: LlmStepAllowedIOType: Input to the node.
            output: LlmStepAllowedIOType: Output of the node.
            model: str: Model used for this span.
            redacted_input: Optional[LlmStepAllowedIOType]: Redacted input to the node.
            redacted_output: Optional[LlmStepAllowedIOType]: Redacted output of the node
            tools: Optional[List[Dict]]: List of available tools passed to LLM on invocation.
            events: Optional[List[Event]]: List of reasoning, internal tool call, or MCP events.
            name: Optional[str]: Name of the span.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at: Optional[datetime]: Timestamp of the span's creation.
            user_metadata: Optional[Dict[str, str]]: Metadata associated with this span.
            num_input_tokens: Optional[int]: Number of input tokens.
            num_output_tokens: Optional[int]: Number of output tokens.
            total_tokens: Optional[int]: Total number of tokens.
            temperature: Optional[float]: Temperature used for generation.
            status_code: Optional[int]: Status code of the node execution.
            time_to_first_token_ns: Optional[int]: Time until the first token was returned.
            id: Optional[UUID4]: ID of the span.
            step_number: Optional[int]: Step number of the span.
        Returns:
        -------
            LlmSpan: The created span.
        """

        span = LlmSpan(
            input=input,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at=self._get_child_span_timestamp() if created_at is None else created_at,
            user_metadata=user_metadata,
            tags=tags,
            metrics=LlmMetrics(
                duration_ns=duration_ns,
                num_input_tokens=num_input_tokens,
                num_output_tokens=num_output_tokens,
                num_total_tokens=total_tokens,
                time_to_first_token_ns=time_to_first_token_ns,
            ),
            tools=tools,
            events=events,
            model=model,
            temperature=temperature,
            status_code=status_code,
            id=id,
            step_number=step_number,
        )
        self.add_child_span_to_parent(span)
        return span

    def add_retriever_span(
        self,
        input: str,
        documents: List[Document],
        redacted_input: Optional[str] = None,
        redacted_documents: Optional[List[Document]] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at: Optional[datetime] = None,
        user_metadata: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        status_code: Optional[int] = None,
        id: Optional[UUID4] = None,
        step_number: Optional[int] = None,
    ) -> RetrieverSpan:
        """
        Add a new retriever span to the current parent.

        Parameters:
        ----------
            input: str: Input to the node.
            documents: List[Document]: Documents retrieved from the retriever.
            redacted_input: Optional[str]: Redacted input to the node.
            redacted_documents: Optional[List[Document]]: Redacted documents retrieved from the retriever.
            name: Optional[str]: Name of the span.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at: Optional[datetime]: Timestamp of the span's creation.
            user_metadata: Optional[Dict[str, str]]: Metadata associated with this span.
            status_code: Optional[int]: Status code of the node execution.
            id: Optional[UUID4]: ID of the span.
            step_number: Optional[int]: Step number of the span.
        Returns:
        -------
            RetrieverSpan: The created span.
        """
        span = RetrieverSpan(
            input=input,
            redacted_input=redacted_input,
            output=documents,
            redacted_output=redacted_documents,
            name=name,
            created_at=self._get_child_span_timestamp() if created_at is None else created_at,
            user_metadata=user_metadata,
            tags=tags,
            status_code=status_code,
            metrics=Metrics(duration_ns=duration_ns),
            id=id,
            step_number=step_number,
        )
        self.add_child_span_to_parent(span)
        return span

    def add_tool_span(
        self,
        input: str,
        redacted_input: Optional[str] = None,
        output: Optional[str] = None,
        redacted_output: Optional[str] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at: Optional[datetime] = None,
        user_metadata: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        status_code: Optional[int] = None,
        tool_call_id: Optional[str] = None,
        id: Optional[UUID4] = None,
        step_number: Optional[int] = None,
    ) -> ToolSpan:
        """
        Add a new tool span to the current parent.

        Parameters:
        ----------
            input: str: Input to the node.
            redacted_input: Optional[str]: Redacted input to the node.
            output: Optional[str]: Output of the node.
            redacted_output: Optional[str]: Redacted output of the node.
            name: Optional[str]: Name of the span.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at: Optional[datetime]: Timestamp of the span's creation.
            user_metadata: Optional[Dict[str, str]]: Metadata associated with this span.
            status_code: Optional[int]: Status code of the node execution.
            tool_call_id: Optional[str]: ID of the tool call.
            id: Optional[UUID4]: ID of the span.
            step_number: Optional[int]: Step number of the span.
        Returns:
        -------
            ToolSpan: The created span.
        """
        span = ToolSpan(
            input=input,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at=self._get_child_span_timestamp() if created_at is None else created_at,
            user_metadata=user_metadata,
            tags=tags,
            status_code=status_code,
            tool_call_id=tool_call_id,
            metrics=Metrics(duration_ns=duration_ns),
            id=id,
            step_number=step_number,
        )
        self.add_child_span_to_parent(span)
        return span

    def add_workflow_span(
        self,
        input: str,
        redacted_input: Optional[str] = None,
        output: Optional[str] = None,
        redacted_output: Optional[str] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at: Optional[datetime] = None,
        user_metadata: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        id: Optional[UUID4] = None,
        step_number: Optional[int] = None,
    ) -> WorkflowSpan:
        """
        Add a workflow span to the current parent. This is useful when you want to create a nested workflow span
        within the trace or current workflow span. The next span you add will be a child of the current parent. To
        move out of the nested workflow, use conclude().

        Parameters:
        ----------
            input: str: Input to the node.
            redacted_input: Optional[str]: Redacted input to the node.
            output: Optional[str]: Output of the node. This can also be set on conclude().
            redacted_output: Optional[str]: Redacted output of the node.
            name: Optional[str]: Name of the span.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at: Optional[datetime]: Timestamp of the span's creation.
            user_metadata: Optional[Dict[str, str]]: Metadata associated with this span.
            id: Optional[UUID4]: ID of the span.
            step_number: Optional[int]: Step number of the span.
        Returns:
        -------
            WorkflowSpan: The created span.
        """
        parent = self.current_parent()
        span = WorkflowSpan(
            input=input,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at=self._get_child_span_timestamp() if created_at is None else created_at,
            user_metadata=user_metadata,
            tags=tags,
            metrics=Metrics(duration_ns=duration_ns),
            id=id,
            step_number=step_number,
        )
        span._parent = parent  # Set back-pointer before adding to parent
        self.add_child_span_to_parent(span)
        self._set_current_parent(span)
        return span

    def add_agent_span(
        self,
        input: str,
        redacted_input: Optional[str] = None,
        output: Optional[str] = None,
        redacted_output: Optional[str] = None,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at: Optional[datetime] = None,
        user_metadata: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        agent_type: Optional[AgentType] = None,
        id: Optional[UUID4] = None,
        step_number: Optional[int] = None,
    ) -> AgentSpan:
        """
        Parameters:
        ----------
            input: str: Input to the node.
            redacted_input: Optional[str]: Redacted input to the node.
            output: Optional[str]: Output of the node. This can also be set on conclude().
            redacted_output: Optional[str]: Redacted output of the node.
            name: Optional[str]: Name of the span.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            created_at: Optional[datetime]: Timestamp of the span's creation.
            user_metadata: Optional[Dict[str, str]]: Metadata associated with this span.
            agent_type: Optional[AgentType]: Agent type of the span.
            step_number: Optional[int]: Step number of the span.
        Returns
        -------
            AgentSpan: The created span.
        """
        parent = self.current_parent()
        span = AgentSpan(
            input=input,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at=self._get_child_span_timestamp() if created_at is None else created_at,
            user_metadata=user_metadata,
            tags=tags,
            metrics=Metrics(duration_ns=duration_ns),
            agent_type=agent_type,
            id=id,
            step_number=step_number,
        )
        span._parent = parent  # Set back-pointer before adding to parent
        self.add_child_span_to_parent(span)
        self._set_current_parent(span)
        return span

    def conclude(
        self,
        output: Optional[str] = None,
        redacted_output: Optional[str] = None,
        duration_ns: Optional[int] = None,
        status_code: Optional[int] = None,
    ) -> Optional[StepWithChildSpans]:
        """
        Conclude the current trace or workflow span by setting the output of the current node. In the case of nested
        workflow spans, this will point the workflow back to the parent of the current workflow span.

        Parameters:
        ----------
            output: Optional[str]: Output of the node.
            redacted_output: Optional[str]: Redacted output of the node.
            duration_ns: Optional[int]: duration_ns of the node in nanoseconds.
            status_code: Optional[int]: Status code of the node execution.
        Returns:
        -------
            Optional[StepWithChildSpans]: The parent of the current workflow. None if no parent exists.
        """
        current_parent = self.current_parent()
        if current_parent is None:
            raise ValueError("No existing workflow to conclude.")

        current_parent.output = output or current_parent.output
        if redacted_output is not None:
            current_parent.redacted_output = redacted_output or current_parent.redacted_output
        current_parent.status_code = status_code
        if duration_ns is not None:
            current_parent.metrics.duration_ns = duration_ns

        # Navigate up to parent via _parent pointer
        parent = current_parent._parent
        self._set_current_parent(parent)

        if parent is None and not isinstance(current_parent, Trace):
            raise ValueError("Finished step is not a trace, but has no parent.  Not added to the list of traces.")
        return self.current_parent()
