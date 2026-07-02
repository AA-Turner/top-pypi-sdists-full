import json
import typing as t
from datetime import UTC, datetime
from uuid import UUID, uuid4

import typing_extensions as te
from pydantic import BaseModel, ConfigDict, Field, PlainSerializer, WithJsonSchema
from rich.console import Console, ConsoleOptions, RenderableType, RenderResult
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from dreadnode.agents.format import format_message
from dreadnode.agents.reactions import (
    Continue,
    Fail,
    Finish,
    Reaction,
    RetryWithFeedback,
)
from dreadnode.agents.tools import ToolCall
from dreadnode.core.metric import MetricSeries
from dreadnode.core.util import format_dict, shorten_string
from dreadnode.generators.generator import Generator, Usage
from dreadnode.generators.message import Message
from dreadnode.tracing.constants import (
    AGENT_ATTRIBUTE_GOAL,
    AGENT_ATTRIBUTE_ID,
    AGENT_ATTRIBUTE_MODEL,
    AGENT_ATTRIBUTE_NAME,
    AGENT_ATTRIBUTE_SESSION_ID,
    AGENT_ATTRIBUTE_TOOLS,
    GENERATION_ATTRIBUTE_CONTENT,
    GENERATION_ATTRIBUTE_FAILED,
    GENERATION_ATTRIBUTE_INPUT_TOKENS,
    GENERATION_ATTRIBUTE_MODEL,
    GENERATION_ATTRIBUTE_OUTPUT_TOKENS,
    GENERATION_ATTRIBUTE_ROLE,
    GENERATION_ATTRIBUTE_STOP_REASON,
    GENERATION_ATTRIBUTE_TOOL_CALLS,
    GENERATION_ATTRIBUTE_TOTAL_TOKENS,
    TOOL_ATTRIBUTE_ARGUMENTS,
    TOOL_ATTRIBUTE_CALL_ID,
    TOOL_ATTRIBUTE_ERROR,
    TOOL_ATTRIBUTE_NAME,
    TOOL_ATTRIBUTE_RESULT,
    TOOL_ATTRIBUTE_STOPPED,
)

if t.TYPE_CHECKING:
    from dreadnode.core.types.common import AnyDict
    from dreadnode.tracing.span import TaskSpan

AgentEventT = te.TypeVar("AgentEventT", bound="AgentEvent", default="AgentEvent")
AgentStepT = te.TypeVar("AgentStepT", bound="AgentStep", default="AgentStep")
AgentStopReason = t.Literal["finished", "max_steps_reached", "error", "stalled"]

# Reusable annotation for error fields that store raw exception objects.
# Pydantic can't serialize exceptions to JSON, so we coerce to str on serialization.
# Same pattern as dreadnode.generators.chat.Chat.error.
_ErrorSerializer = PlainSerializer(lambda x: str(x), return_type=str, when_used="json-unless-none")
_ErrorJsonSchema = WithJsonSchema({"type": "string", "description": "Error message"})
SerializableError = t.Annotated[BaseException, _ErrorSerializer, _ErrorJsonSchema]
SerializableException = t.Annotated[Exception, _ErrorSerializer, _ErrorJsonSchema]
AgentStatus = t.Literal["running", "stalled", "errored", "finished"]


class AgentEvent(BaseModel):
    """
    A log event in the agent's lifecycle.

    Attributes:
        timestamp: The timestamp of when the event occurred (UTC).
        agent_id: The name of the agent that generated this event.
        agent_name: The name of the agent that generated this event.
        status: The status of the agent at the time of this event.
        metrics: Metrics attached to this event by scoring conditions.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), kw_only=True)
    agent_id: UUID = Field(default_factory=uuid4)
    agent_name: str | None = None
    status: AgentStatus | None = Field(default=None)
    metrics: dict[str, MetricSeries] = Field(default_factory=dict)

    def as_dict(self) -> dict[str, t.Any]:
        """Serialize event for frontend transport."""
        return {
            "type": self.__class__.__name__.lower(),
            "timestamp": self.timestamp.isoformat(),
            "agent_id": str(self.agent_id),
            "agent_name": self.agent_name,
            "status": self.status,
            "data": self._get_data(),
        }

    def _get_data(self) -> dict[str, t.Any]:
        """Override in subclasses to provide event-specific data."""
        return {}

    def emit(self, span: "TaskSpan") -> None:
        """
        Emit this event's telemetry to the span.

        Events own their telemetry - this method defines what attributes,
        metrics, inputs, and outputs each event type logs.

        Override in subclasses to add event-specific telemetry.
        """
        # Log minimal timeline event
        span.log_event(
            f"agent.{self.__class__.__name__}",
            {"event_type": self.__class__.__name__, "timestamp": self.timestamp.isoformat()},
        )

        # Log attached metrics from scoring conditions
        for name, series in self.metrics.items():
            if series.value is not None:
                step = series.steps[-1] if series.steps else 0
                span.log_metric(f"scorer/{name}", series.value, step=step)


class AgentStep(AgentEvent):
    """
    A discrete unit of work that advances the agent's state.

    A Step is an Event that contains messages that will be part of the
    ongoing chat history.

    Additionally, tracks step count, token usage, etc.

    Attributes:
        generator: The model or generator used by the agent during this step.
        step: The step number in the agent's execution when this event occurred.
        messages: The messages generated or processed during this step.
        usage: The token usage associated with this step, if applicable.
        error: An optional error that occurred during this step's execution.
        stop: Indicates if this step signals a stop condition for the agent.
        estimated_cost: Estimates the cost of the agent run based on total token usage and model pricing.

    """

    generator: Generator | None = None
    step: int = 0
    messages: list[Message] = Field(default_factory=list)
    usage: Usage = Usage(input_tokens=0, output_tokens=0, total_tokens=0)
    error: SerializableException | None = None
    stop: bool | None = None

    @property
    def estimated_cost(self) -> float | None:
        # Prefer the cost litellm attached to the response - it dispatches
        # per-provider (anthropic_cost_per_token, openai_cost_per_token,
        # bedrock_*, vertex_*, gemini_*, ...) and honours cache_read /
        # cache_creation rates, reasoning tokens, tiered pricing, and
        # region/service-tier multipliers. The naive math below ignores
        # all of that and is wrong by 30-80% under prompt caching.
        if self.usage.cost_usd is not None:
            return self.usage.cost_usd

        import litellm

        if self.generator is None:
            return None

        model = self.generator.model
        while model not in litellm.model_cost:
            if "/" not in model:
                return None
            model = "/".join(model.split("/")[1:])

        model_info: AnyDict = litellm.model_cost[model]
        input_token_cost = float(model_info.get("input_cost_per_token", 0))
        output_token_cost = float(model_info.get("output_cost_per_token", 0))

        return (
            input_token_cost * self.usage.input_tokens
            + output_token_cost * self.usage.output_tokens
        )

    def __repr__(self) -> str:
        message_content = shorten_string(str(self.messages[0].content), 50)
        tool_call_count = len(self.messages[0].tool_calls) if self.messages[0].tool_calls else 0
        message = f"Message(role={self.messages[0].role}, content='{message_content}', tool_calls={tool_call_count})"
        return f"StepEnd(message={message})"

    def format_as_panel(self, *, truncate: bool = False) -> Panel:
        cost = round(self.estimated_cost, 6) if self.estimated_cost else ""
        usage = str(self.usage) or ""
        return Panel(
            format_message(self.messages[0], truncate=truncate),
            title="Step End",
            title_align="left",
            subtitle=f"[dim]{usage} [{cost} USD][/dim]",
            subtitle_align="right",
            padding=(1, 1),
        )


class AgentStart(AgentEvent):
    """Event: The agent's execution process has started.

    Attributes:
        inputs: The inputs provided to the agent at the start of execution.
        params: The parameters used to configure the agent at the start of execution.
    """

    inputs: dict[str, t.Any] = Field(default_factory=dict)
    params: dict[str, t.Any] = Field(default_factory=dict)

    def _get_data(self) -> dict[str, t.Any]:
        return {"inputs": self.inputs, "params": self.params}

    def emit(self, span: "TaskSpan") -> None:
        span.set_attribute(AGENT_ATTRIBUTE_ID, str(self.agent_id))
        if self.agent_name:
            span.set_attribute(AGENT_ATTRIBUTE_NAME, self.agent_name)

        goal = self.inputs.get("goal")
        if goal is not None:
            span.set_attribute(AGENT_ATTRIBUTE_GOAL, str(goal))
            span.log_input(name="goal", value=goal)

        if session_id := self.params.get("session_id"):
            span.set_attribute(AGENT_ATTRIBUTE_SESSION_ID, str(session_id))
        if model := self.params.get("model"):
            span.set_attribute(AGENT_ATTRIBUTE_MODEL, str(model))
        if tools := self.params.get("tools"):
            span.set_attribute(AGENT_ATTRIBUTE_TOOLS, tools)

        # Log goal/input
        # Log params
        for key, value in self.params.items():
            span.log_param(key, value)

        super().emit(span)


class AgentEnd(AgentEvent):
    """Event: The agent's execution process has finished.

    Attributes:
        stop_reason: The reason why the agent stopped, if applicable.
        error: The error that caused the agent to stop, if applicable.
    """

    stop_reason: AgentStopReason
    error: SerializableException | str | None = None

    def _get_data(self) -> dict[str, t.Any]:
        error = self.error
        error_str = str(error) if error else None
        error_type: str | None = None
        if error is not None:
            error_type = type(error).__name__ if isinstance(error, BaseException) else None
            # Preserve chained exception context for richer debugging
            cause = getattr(error, "__cause__", None) or getattr(error, "__context__", None)
            if cause and str(cause) not in (error_str or ""):
                error_str = f"{error_str} — {type(cause).__name__}: {cause}"
        return {
            "stop_reason": self.stop_reason,
            "error": error_str,
            "error_type": error_type,
        }

    def emit(self, span: "TaskSpan") -> None:
        if self.error:
            span.log_output(name="error", value=str(self.error))

        super().emit(span)


class Heartbeat(AgentEvent):
    """Event: Keepalive signal emitted during long-running operations.

    Used to indicate that the agent is still processing when no other events
    have been emitted for a period of time. This helps frontends detect whether
    the stream is still active vs. stalled.

    Attributes:
        message: Optional status message describing current activity.
    """

    message: str = "Processing..."

    def _get_data(self) -> dict[str, t.Any]:
        return {"message": self.message}

    def emit(self, span: "TaskSpan") -> None:
        # Heartbeats are informational only, don't need to log anything
        pass


CompactionTrigger = t.Literal["manual", "threshold", "overflow_recovery"]


class CompactionEvent(AgentEvent):
    """Lifecycle event for session compaction (CMP-LIFE-001).

    This is a lifecycle signal, not a trajectory step — it extends AgentEvent,
    not AgentStep, so it does not carry messages or get added to the trajectory.
    """

    trigger: CompactionTrigger
    compaction_status: t.Literal["started", "completed", "skipped", "failed"]
    reason: str | None = None
    messages_before: int = 0
    messages_after: int = 0

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "trigger": self.trigger,
            "compaction_status": self.compaction_status,
            "reason": self.reason,
            "messages_before": self.messages_before,
            "messages_after": self.messages_after,
        }


class GenerationRetry(AgentEvent):
    """Lifecycle event: the agent is about to sleep and retry a failed generation.

    Emitted by the agent loop when a transient LLM API error (rate limit, etc.)
    is recovered in place via ``Agent._try_backoff``. This is a lifecycle signal
    only — it does not consume a step or land in the trajectory.
    """

    step: int
    attempt: int
    max_attempts: int
    wait_seconds: float
    error_type: str
    error_message: str

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "step": self.step,
            "attempt": self.attempt,
            "max_attempts": self.max_attempts,
            "wait_seconds": self.wait_seconds,
            "error_type": self.error_type,
            "error_message": self.error_message,
        }


class AgentStalled(AgentEvent):
    """Event: The agent is stalled and there are no tool calls, or stop condition)."""

    def _get_data(self) -> dict[str, t.Any]:
        return {"reason": "No tool calls and no stop condition met"}

    def emit(self, span: "TaskSpan") -> None:
        span.log_metric("agent/stalled", 1)
        super().emit(span)

    def format_as_panel(self, *, truncate: bool = False) -> Panel:  # noqa: ARG002
        return Panel(
            Text(
                "Agent has no tool calls to make and has not met a stop condition.",
                style="dim white",
            ),
            title="Agent Stalled",
            title_align="left",
            border_style="bright_black",
        )


class AgentError(AgentEvent):
    """Event: An error occurred, functionally halting the agent.

    Attributes:
        error: The error that occurred during the agent's execution.
    """

    error: SerializableError

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "error": str(self.error),
            "error_type": type(self.error).__name__,
        }

    def emit(self, span: "TaskSpan") -> None:
        span.log_metric("agent/error", 1)
        super().emit(span)

    def format_as_panel(self, *, truncate: bool = False) -> Panel:  # noqa: ARG002
        return Panel(
            repr(self),
            title="Agent Error",
            title_align="left",
            border_style="red",
        )


class ToolStep(AgentStep):
    """A step representing the completion of a tool call by the agent.

    Attributes:
       tool_call: The tool call that was completed."""

    tool_call: ToolCall

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "tool_call": {
                "id": self.tool_call.id,
                "name": self.tool_call.name,
            },
            "step": self.step,
            "stop": self.stop,
            "error": str(self.error) if self.error else None,
        }

    def __repr__(self) -> str:
        message_content = shorten_string(str(self.messages[0].content), 50)
        message = f"Message(role={self.messages[0].role}, content='{message_content}')"
        return f"ToolEnd(tool_call={self.tool_call}, message={message}, stop={self.stop})"

    def emit(self, span: "TaskSpan") -> None:
        # ToolStep is for trajectory only - telemetry handled by ToolStart/ToolEnd
        # Just log a minimal event for timeline tracking
        span.log_event(
            f"agent.{self.__class__.__name__}",
            {
                "tool_name": self.tool_call.name,
                "step": self.step,
                "tool_call_id": self.tool_call.id,
            },
        )

    def format_as_panel(self, *, truncate: bool = False) -> Panel:
        panel = format_message(self.messages[0], truncate=truncate)
        subtitle = f"[dim]{self.tool_call.id}[/dim]"
        if self.stop:
            subtitle += " [bold red](Requesting Stop)[/bold red]"
        return Panel(
            panel.renderable,
            title=f"Tool End: {self.tool_call.name}",
            title_align="left",
            border_style="orange3",
            subtitle=subtitle,
            subtitle_align="right",
            padding=(1, 1),
        )


class ToolStart(AgentEvent):
    """Event: A tool call is about to be executed.

    Attributes:
        tool_call: The tool call that is being started.
    """

    tool_call: ToolCall

    def _get_data(self) -> dict[str, t.Any]:
        try:
            args = json.loads(self.tool_call.function.arguments)
        except (json.JSONDecodeError, TypeError):
            args = self.tool_call.function.arguments
        return {
            "tool_call": {
                "id": self.tool_call.id,
                "name": self.tool_call.name,
                "arguments": args,
            },
        }

    def __repr__(self) -> str:
        return f"ToolStart(tool_call={self.tool_call})"

    def emit(self, span: "TaskSpan") -> None:
        # Attributes
        span.set_attribute(TOOL_ATTRIBUTE_NAME, self.tool_call.name)
        span.set_attribute(TOOL_ATTRIBUTE_CALL_ID, self.tool_call.id)

        # Parse and set arguments
        try:
            args = json.loads(self.tool_call.function.arguments)
        except (json.JSONDecodeError, TypeError):
            args = self.tool_call.function.arguments

        span.set_attribute(TOOL_ATTRIBUTE_ARGUMENTS, args)
        span.log_input("arguments", args)

        super().emit(span)

    def format_as_panel(self, *, truncate: bool = False) -> Panel:
        content: RenderableType
        try:
            args: AnyDict = json.loads(self.tool_call.function.arguments)
            if not args:
                content = Text("No arguments.", style="dim")
            elif truncate:
                content = Text(format_dict(args), style="default")
            else:
                content = Table.grid(padding=(0, 1))
                content.add_column("key", style="dim", no_wrap=True)
                content.add_column("value")
                for k, v in args.items():
                    content.add_row(f"{k}:", repr(v))
        except (json.JSONDecodeError, TypeError):
            # Fallback for non-JSON or unparsable arguments
            content = Text(self.tool_call.function.arguments, style="default")

        return Panel(
            content,
            title=f"Tool Start: {self.tool_call.name}",
            title_align="left",
            border_style="dark_orange3",
            subtitle=f"[dim]{self.tool_call.id}[/dim]",
            subtitle_align="right",
            padding=(1, 1),
        )


class ToolEnd(AgentEvent):
    """Event: A tool call has completed.

    A non-empty ``error`` means the tool ran to completion but reported
    a failure (e.g. bash non-zero exit, ``@tool(catch=True)`` swallowing
    an exception, or an MCP server returning ``isError=true``). Uncaught
    exceptions go through :class:`ToolError` instead.

    Attributes:
        tool_call: The tool call that was completed.
        result: The result returned by the tool, if applicable.
        stop: Whether this tool requested the agent to stop.
        error: A failure message lifted from ``message.metadata['error']``.
        error_type: Exception class name when the error was sourced from
            an :class:`ErrorModel` carrying that metadata.
    """

    tool_call: ToolCall
    result: str | None = None
    stop: bool = False
    output_file: str | None = None
    error: str | None = None
    error_type: str | None = None
    cost_usd: float | None = None
    """Estimated USD cost contributed by this tool call, when the tool
    ran an internal LLM (e.g. ``spawn_agent``). ``None`` for ordinary
    tools — the TUI only accumulates this into the sub-agent cost
    display, never the main session cost."""

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "tool_call": {
                "id": self.tool_call.id,
                "name": self.tool_call.name,
            },
            "result": self.result or None,
            "output_file": self.output_file,
            "stop": self.stop,
            "error": self.error,
            "error_type": self.error_type,
            "cost_usd": self.cost_usd,
        }

    def __repr__(self) -> str:
        result_content = shorten_string(str(self.result), 50)
        return f"ToolEnd(tool_call={self.tool_call}, result='{result_content}')"

    def emit(self, span: "TaskSpan") -> None:
        # Attributes
        if self.result:
            span.set_attribute(TOOL_ATTRIBUTE_RESULT, self.result)
            span.log_output("result", self.result)

        span.set_attribute(TOOL_ATTRIBUTE_STOPPED, self.stop)

        if self.error:
            span.set_attribute(TOOL_ATTRIBUTE_ERROR, self.error)
            span.log_metric(f"tool/{self.tool_call.name}/error", 1)

        super().emit(span)

    def format_as_panel(self, *, truncate: bool = False) -> Panel:
        result_text = self.result or "No result."
        if truncate:
            result_text = shorten_string(result_text, 100)

        return Panel(
            Text(result_text, style="default"),
            title=f"Tool End: {self.tool_call.name}",
            title_align="left",
            border_style="orange3",
            subtitle=f"[dim]{self.tool_call.id}[/dim]",
            subtitle_align="right",
            padding=(1, 1),
        )


class ToolError(AgentEvent):
    """Event: An error occurred during a tool call.

    Attributes:
        tool_call: The tool call that caused the error.
        error: The error that occurred during the tool call.
    """

    tool_call: ToolCall
    error: SerializableError

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "tool_call": {
                "id": self.tool_call.id,
                "name": self.tool_call.name,
            },
            "error": str(self.error),
            "error_type": type(self.error).__name__,
        }

    def emit(self, span: "TaskSpan") -> None:
        # Attributes
        span.set_attribute(TOOL_ATTRIBUTE_ERROR, str(self.error))

        # Metrics
        span.log_metric(f"tool/{self.tool_call.name}/error", 1)

        super().emit(span)

    def format_as_panel(self, *, truncate: bool = False) -> Panel:  # noqa: ARG002
        return Panel(
            repr(self.error),
            title=f"Tool Error: {self.tool_call.name}",
            title_align="left",
            border_style="red",
        )


class UserInputRequired(AgentEvent):
    """Event: The agent needs human input to continue.

    Emitted when a tool (like ask_the_user) requests input from the user.
    The agent execution is suspended until the input is provided.

    Attributes:
        request_id: Unique identifier for this input request.
        question: The question to ask the user.
        options: Optional list of choices to present to the user.
    """

    request_id: str
    question: str
    options: list[str] | None = None

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "request_id": self.request_id,
            "question": self.question,
            "options": self.options,
        }

    def format_as_panel(self, *, truncate: bool = False) -> Panel:  # noqa: ARG002
        content_parts = [f"Question: {self.question}"]
        if self.options:
            content_parts.append(f"Options: {', '.join(self.options)}")
        content_parts.append(f"[dim]Request ID: {self.request_id}[/dim]")

        return Panel(
            Text("\n".join(content_parts), style="default"),
            title="User Input Required",
            title_align="left",
            border_style="cyan",
        )


class GenerationStep(AgentStep):
    """
    A step representing a call to the generator.

    Attributes:
        generator: The model or generator used by the agent during this step.
        stop_reason: Why the generation stopped (end_turn, tool_use, max_tokens, etc.).
        extra: Additional metadata from the generator/chat.
        generation_failed: Whether the generation failed.
    """

    generator: Generator | None = None
    stop_reason: str | None = None
    extra: dict[str, t.Any] = Field(default_factory=dict)
    generation_failed: bool = False

    def _get_data(self) -> dict[str, t.Any]:
        content = None
        tool_calls = []

        if self.messages:
            last_msg = self.messages[-1]
            content = str(last_msg.content) if last_msg.content else None

            for tc in last_msg.tool_calls or []:
                try:
                    args = json.loads(tc.function.arguments)
                except (json.JSONDecodeError, TypeError):
                    args = tc.function.arguments
                tool_calls.append(
                    {
                        "id": tc.id,
                        "name": tc.name,
                        "arguments": args,
                    }
                )

        return {
            "step": self.step,
            "content": content,
            "tool_calls": tool_calls,
            "usage": {
                "input_tokens": self.usage.input_tokens,
                "output_tokens": self.usage.output_tokens,
                "total_tokens": self.usage.total_tokens,
                "cost_usd": self.estimated_cost,
            },
            "stop_reason": self.stop_reason,
            "model": self.generator.model if self.generator else None,
            "failed": self.generation_failed,
            "extra": self.extra,
        }

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield Rule(f"Step {self.step}: Generation", style="dim cyan", characters="·")

    def emit(self, span: "TaskSpan") -> None:
        # Attributes - model
        if self.generator:
            span.set_attribute(GENERATION_ATTRIBUTE_MODEL, self.generator.model)

        # Attributes - tokens
        if self.usage:
            span.set_attribute(GENERATION_ATTRIBUTE_INPUT_TOKENS, self.usage.input_tokens)
            span.set_attribute(GENERATION_ATTRIBUTE_OUTPUT_TOKENS, self.usage.output_tokens)
            span.set_attribute(GENERATION_ATTRIBUTE_TOTAL_TOKENS, self.usage.total_tokens)

        # Attributes - status
        span.set_attribute(GENERATION_ATTRIBUTE_FAILED, self.generation_failed)
        if self.stop_reason:
            span.set_attribute(GENERATION_ATTRIBUTE_STOP_REASON, self.stop_reason)

        # Attributes - content and tool calls
        if self.messages:
            last_msg = self.messages[-1]
            span.set_attribute(GENERATION_ATTRIBUTE_ROLE, last_msg.role)

            if last_msg.content:
                span.set_attribute(GENERATION_ATTRIBUTE_CONTENT, str(last_msg.content))

            if last_msg.tool_calls:
                span.set_attribute(
                    GENERATION_ATTRIBUTE_TOOL_CALLS,
                    [{"name": tc.name, "id": tc.id} for tc in last_msg.tool_calls],
                )

        # Metrics
        if self.usage:
            span.log_metric("generation/input_tokens", self.usage.input_tokens, step=self.step)
            span.log_metric("generation/output_tokens", self.usage.output_tokens, step=self.step)
            span.log_metric("generation/total_tokens", self.usage.total_tokens, step=self.step)

        model_name = self.generator.model if self.generator else "unknown"
        span.log_metric(f"generation/{model_name}/count", 1, step=self.step)

        # Output (last message content)
        if self.messages:
            last_msg = self.messages[-1]
            if last_msg.content:
                span.log_output(
                    name="generation",
                    value=last_msg.content,
                    attributes={"step": self.step, "role": last_msg.role},
                )

        super().emit(span)


class GenerationStart(AgentEvent):
    """Event: The agent is starting a generation step.

    Attributes:
        generator: The model or generator used by the agent during this step.
        step: The step number in the agent's execution.
        messages: The input messages being sent to the model.
    """

    generator: Generator | None = None
    step: int = 0
    messages: list[Message] = Field(default_factory=list)

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "model": self.generator.model if self.generator else None,
            "step": self.step,
        }

    def emit(self, span: "TaskSpan") -> None:
        if self.generator:
            span.set_attribute(GENERATION_ATTRIBUTE_MODEL, self.generator.model)

        # Log input messages being sent to the model
        if self.messages:
            input_messages = []
            for m in self.messages:
                msg: dict[str, t.Any] = {"role": m.role}
                if m.content:
                    msg["content"] = str(m.content)
                if m.tool_calls:
                    msg["tool_calls"] = [{"name": tc.name, "id": tc.id} for tc in m.tool_calls]
                input_messages.append(msg)
            span.log_input("messages", input_messages)

        super().emit(span)


class GenerationEnd(AgentStep):
    """Event: The agent has completed a generation step.

    Attributes:
        generator: The model or generator used by the agent during this step.
        stop_reason: Why the generation stopped (end_turn, tool_use, max_tokens, etc.).
    """

    generator: Generator | None = None
    stop_reason: str | None = None

    def _get_data(self) -> dict[str, t.Any]:
        content = None
        tool_calls = []

        if self.messages:
            last_msg = self.messages[-1]
            content = str(last_msg.content) if last_msg.content else None

            for tc in last_msg.tool_calls or []:
                try:
                    args = json.loads(tc.function.arguments)
                except (json.JSONDecodeError, TypeError):
                    args = tc.function.arguments
                tool_calls.append(
                    {
                        "id": tc.id,
                        "name": tc.name,
                        "arguments": args,
                    }
                )

        return {
            "step": self.step,
            "content": content,
            "tool_calls": tool_calls,
            "usage": {
                "input_tokens": self.usage.input_tokens,
                "output_tokens": self.usage.output_tokens,
                "total_tokens": self.usage.total_tokens,
            },
            "stop_reason": self.stop_reason,
            "model": self.generator.model if self.generator else None,
        }

    def emit(self, span: "TaskSpan") -> None:
        # Attributes - tokens
        if self.usage:
            span.set_attribute(GENERATION_ATTRIBUTE_INPUT_TOKENS, self.usage.input_tokens)
            span.set_attribute(GENERATION_ATTRIBUTE_OUTPUT_TOKENS, self.usage.output_tokens)
            span.set_attribute(GENERATION_ATTRIBUTE_TOTAL_TOKENS, self.usage.total_tokens)
            span.log_metric("generation/input_tokens", self.usage.input_tokens, step=self.step)
            span.log_metric("generation/output_tokens", self.usage.output_tokens, step=self.step)

        # Attributes - content and tool calls
        if self.messages:
            last_msg = self.messages[-1]
            span.set_attribute(GENERATION_ATTRIBUTE_ROLE, last_msg.role)

            if last_msg.content:
                span.set_attribute(GENERATION_ATTRIBUTE_CONTENT, str(last_msg.content))
                span.log_output(
                    name="generation",
                    value=last_msg.content,
                    attributes={"step": self.step, "role": last_msg.role},
                )

            if last_msg.tool_calls:
                span.set_attribute(
                    GENERATION_ATTRIBUTE_TOOL_CALLS,
                    [{"name": tc.name, "id": tc.id} for tc in last_msg.tool_calls],
                )

        if self.stop_reason:
            span.set_attribute(GENERATION_ATTRIBUTE_STOP_REASON, self.stop_reason)

        super().emit(span)


class GenerationContent(AgentEvent):
    """Event: The LLM produced content, emitted before tool execution.

    This is a TUI rendering signal — it carries the generation text so it can
    be displayed immediately, before tools run. GenerationEnd/GenerationStep
    still fire after tools for trajectory, hooks, and telemetry.

    Attributes:
        step: The step number.
        content: The generated text content.
        tool_calls: Tool calls requested by the generation.
        extra: Additional metadata (reasoning_content, etc.).
    """

    step: int = 0
    content: str | None = None
    tool_calls: list[dict[str, t.Any]] = Field(default_factory=list)
    extra: dict[str, t.Any] = Field(default_factory=dict)

    def _get_data(self) -> dict[str, t.Any]:
        return {
            "step": self.step,
            "content": self.content,
            "tool_calls": self.tool_calls,
            "extra": self.extra,
        }

    def emit(self, span: "TaskSpan") -> None:
        # No telemetry — GenerationEnd handles that
        pass


class GenerationError(AgentEvent):
    """Event: An error occurred during a generation step

    Attributes:
        generator: The model or generator used by the agent during this step.
        error: The error that occurred during the generation step.
        step: The step number in the agent's execution.
        messages: The conversation messages at the time of failure (for recovery hooks).
    """

    generator: Generator | None = None
    error: SerializableError
    step: int = 0
    messages: list["Message"] = Field(default_factory=list)

    def _get_data(self) -> dict[str, t.Any]:
        error_str = str(self.error)
        # When litellm wraps provider exceptions with empty messages (e.g.
        # "AnthropicException - ."), enrich with the underlying cause so the
        # user gets something actionable instead of a cryptic dot.
        if error_str.endswith(
            ("Exception - .", "Exception - . Handle with `litellm.InternalServerError`.")
        ):
            cause = getattr(self.error, "__cause__", None) or getattr(
                self.error, "__context__", None
            )
            if cause:
                error_str = f"{error_str} (cause: {cause})"
            else:
                error_str = (
                    f"{type(self.error).__name__}: The API returned an error with no details. "
                    "This is usually a transient issue — try again."
                )
        return {
            "model": self.generator.model if self.generator else None,
            "error": error_str,
            "error_type": type(self.error).__name__,
            "step": self.step,
        }

    def emit(self, span: "TaskSpan") -> None:
        # Attributes
        failed = True
        span.set_attribute(GENERATION_ATTRIBUTE_FAILED, failed)
        if self.generator:
            span.set_attribute(GENERATION_ATTRIBUTE_MODEL, self.generator.model)

        # Metrics
        span.log_metric("generation/error", 1, step=self.step)

        super().emit(span)


class ReactStep(AgentStep):
    """A step representing a reaction from a hook.

    ReactStep is an AgentStep because reactions can provide feedback to the LLM
    through messages (e.g., Continue with modified messages, RetryWithFeedback).

    Note: The hook dispatch system filters out ReactStep when calling hooks
    that listen to AgentStep, preventing hooks from reacting to their own reactions.

    Attributes:
        hook_name: The name of the hook that generated this event.
        reaction: The reaction taken by the hook.

    """

    hook_name: str | None = None
    reaction: Reaction | None = None

    def _get_data(self) -> dict[str, t.Any]:
        reaction_data: dict[str, t.Any] = {}
        if self.reaction:
            reaction_data["type"] = type(self.reaction).__name__
            if hasattr(self.reaction, "feedback"):
                reaction_data["feedback"] = self.reaction.feedback
            if hasattr(self.reaction, "reason"):
                reaction_data["reason"] = self.reaction.reason
            if hasattr(self.reaction, "error"):
                reaction_data["error"] = str(self.reaction.error)
        return {
            "hook_name": self.hook_name,
            "reaction": reaction_data,
            "step": self.step,
        }

    def format_as_panel(self, *, truncate: bool = False) -> Panel:  # noqa: ARG002
        reaction_name = self.reaction.__class__.__name__
        details = ""

        if isinstance(self.reaction, RetryWithFeedback):
            details = f" ▸ Feedback: [italic]{self.reaction.feedback}[/italic]"
        elif isinstance(self.reaction, Finish) and self.reaction.reason:
            details = f" ▸ Reason: [italic]{self.reaction.reason}[/italic]"
        elif isinstance(self.reaction, Fail) and self.reaction.error:
            details = f" ▸ Error: [italic]{self.reaction.error}[/italic]"
        elif isinstance(self.reaction, Continue):
            details = (
                f" ▸ Modifying messages ({len(self.messages)} -> {len(self.reaction.messages)})"
            )

        return Panel(
            Text.from_markup(details, style="default"),
            title=f"Hook '{self.hook_name}' reacted: {reaction_name}",
            title_align="left",
            border_style="blue_violet",
        )

    def emit(self, span: "TaskSpan") -> None:
        span.log_metric("hook/total_count", 1, step=self.step)

        if self.hook_name:
            span.log_metric(f"hook/{self.hook_name}/count", 1, step=self.step)

        if self.reaction:
            reaction_type = type(self.reaction).__name__
            span.log_metric(f"reaction/{reaction_type}", 1, step=self.step)

        super().emit(span)


# =============================================================================
# Event Serialization Registry
# =============================================================================

# All concrete event types for deserialization
EVENT_TYPES: dict[str, type[AgentEvent]] = {
    "AgentEvent": AgentEvent,
    "AgentStep": AgentStep,
    "AgentStart": AgentStart,
    "AgentEnd": AgentEnd,
    "AgentStalled": AgentStalled,
    "AgentError": AgentError,
    "ToolStart": ToolStart,
    "ToolEnd": ToolEnd,
    "ToolStep": ToolStep,
    "ToolError": ToolError,
    "GenerationStart": GenerationStart,
    "GenerationEnd": GenerationEnd,
    "GenerationStep": GenerationStep,
    "GenerationContent": GenerationContent,
    "GenerationError": GenerationError,
    "GenerationRetry": GenerationRetry,
    "ReactStep": ReactStep,
    "UserInputRequired": UserInputRequired,
    "Heartbeat": Heartbeat,
    "CompactionEvent": CompactionEvent,
}


def event_to_dict(event: AgentEvent) -> dict[str, t.Any]:
    """
    Serialize an AgentEvent to a JSON-compatible dict for persistence.

    Includes a '_type' discriminator for deserialization.
    """
    data = event.model_dump(mode="json", exclude_none=True)
    data["_type"] = type(event).__name__
    return data


def event_from_dict(data: dict[str, t.Any]) -> AgentEvent:
    """
    Deserialize a dict back to the appropriate AgentEvent subclass.

    Uses the '_type' field to determine the correct class.
    """
    from loguru import logger

    data = dict(data)  # Don't mutate input
    type_name = data.pop("_type", "AgentEvent")
    event_class = EVENT_TYPES.get(type_name)

    if event_class is None:
        logger.warning(f"Unknown event type: {type_name}, using AgentEvent")
        event_class = AgentEvent

    try:
        return event_class.model_validate(data)
    except Exception as e:
        logger.warning(f"Failed to deserialize {type_name}: {e}")
        # Return a basic AgentEvent as fallback
        return AgentEvent.model_validate(
            {
                k: v
                for k, v in data.items()
                if k in {"timestamp", "agent_id", "agent_name", "status"}
            }
        )
