import asyncio
import contextlib
import inspect
import random
import time
import typing as t
from contextlib import AsyncExitStack, asynccontextmanager, suppress
from copy import deepcopy
from textwrap import dedent
from uuid import UUID, uuid4

from loguru import logger
from pydantic import (
    AfterValidator,
    ConfigDict,
    Field,
    PrivateAttr,
    field_validator,
    model_validator,
)

import dreadnode
from dreadnode.agents.engines import AgentEngine, EngineContext, PermissionBridge, resolve_engine
from dreadnode.agents.events import (
    AgentEnd,
    AgentError,
    AgentEvent,
    AgentStalled,
    AgentStart,
    AgentStep,
    AgentStopReason,
    CompactionEvent,
    GenerationContent,
    GenerationEnd,
    GenerationError,
    GenerationRetry,
    GenerationStart,
    GenerationStep,
    ReactStep,
    ToolEnd,
    ToolError,
    ToolStart,
    ToolStep,
)
from dreadnode.agents.reactions import (
    Continue,
    Fail,
    Finish,
    Reaction,
    Retry,
    RetryWithFeedback,
)
from dreadnode.agents.tools import Tool, ToolCall, ToolMode, Toolset, discover_tools_on_obj
from dreadnode.agents.trajectory import Trajectory
from dreadnode.core.exceptions import warn_at_user_stacklevel
from dreadnode.core.execution import Executor
from dreadnode.core.hook import Hook
from dreadnode.core.judge import Judge, Rubric
from dreadnode.core.meta import Component, Config, component
from dreadnode.core.stopping import StopCondition
from dreadnode.core.task import Task, task
from dreadnode.core.transforms import PostTransform, Transform
from dreadnode.core.util import flatten_list, safe_repr
from dreadnode.generators import caching
from dreadnode.generators.chat import Chat
from dreadnode.generators.generator import GenerateParams, Generator, Usage, get_generator
from dreadnode.generators.message import Message, inject_system_content, make_compaction_message
from dreadnode.generators.models import SystemErrorModel
from dreadnode.transforms import (
    make_tools_to_xml_transform,
    tools_to_json_in_xml_transform,
    tools_to_json_transform,
    tools_to_json_with_tag_transform,
    tools_to_pythonic_transform,
)


class AgentWarning(UserWarning):
    """Warning raised when an agent is used in a way that may not be safe or intended."""


def _raise_exception(error: BaseException) -> t.NoReturn:
    """Raise an exception from a dedicated helper to keep Ruff happy."""
    raise error


_TRANSIENT_LITELLM_EXCEPTION_NAMES: tuple[str, ...] = (
    "RateLimitError",
    "Timeout",
    "APIConnectionError",
    "APIConnectionTimeoutError",
    "ServiceUnavailableError",
    "InternalServerError",
    "BadGatewayError",
    "APIError",
)


def _is_transient_api_error(error: BaseException) -> bool:
    """Classify an error as a transient LLM API failure worth retrying.

    Matches an explicit allow-list of ``litellm.exceptions`` classes that
    represent recoverable conditions: rate limits, timeouts, connection
    failures, and 5xx responses. Notably **does not** match
    ``BadRequestError``, ``AuthenticationError``,
    ``ContextWindowExceededError`` (handled by overflow recovery), or other
    deterministic client errors.

    The allow-list is walked dynamically because ``litellm.exceptions`` does
    not expose a single common ancestor for its transient exceptions.
    Returns ``False`` if ``litellm`` is not importable.
    """
    with contextlib.suppress(ImportError):
        import litellm.exceptions as _litellm_exc

        classes = tuple(
            cls
            for name in _TRANSIENT_LITELLM_EXCEPTION_NAMES
            if (cls := getattr(_litellm_exc, name, None)) is not None
        )
        if classes and isinstance(error, classes):
            # OpenAI returns 429 with code "insufficient_quota" when the
            # account is out of credits — a permanent billing condition,
            # not a rate limit. litellm packs the provider body into the
            # message verbatim, so substring-match to exclude.
            rate_limit_cls = getattr(_litellm_exc, "RateLimitError", None)
            return not (
                rate_limit_cls is not None
                and isinstance(error, rate_limit_cls)
                and "insufficient_quota" in str(error)
            )
    return False


class Agent(Executor[AgentEvent, Trajectory]):
    """
    Agent abstraction for applying tools, event logic, and message state to LLM generation.

    Now extends Executor for consistent streaming/tracing patterns.

    Args:

        name: The name of the agent.
        description: A brief description of the agent.
        tags: Tags associated with the agent.
        label: An optional label for the agent.
        agent_id: The unique identifier for this agent instance.
        model: Inference model (generator or identifier).
        instructions: The agent's core instructions.
        cache: How to handle cache_control entries on inference messages.
        tools: Tools the agent can use.
        tool_mode: The tool calling mode to use.
        stop_conditions: The logical condition for successfully stopping a run.
        hooks: Hooks to apply during agent execution.
        trajectory: Stateful trajectory for this agent.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, use_attribute_docstrings=True)

    agent_id: UUID = Field(default_factory=uuid4)
    model: str | Generator | None = Config(default=None, expose_as=str | None)
    instructions: t.Annotated[str | None, AfterValidator(lambda x: dedent(x) if x else x)] = Config(
        default=None
    )
    cache: caching.CacheMode | None = Config(default="latest", repr=False)
    tools: list[Tool | Toolset] = Config(default_factory=list, validate_default=False)
    tool_mode: ToolMode = Config(default="auto", repr=False)
    hooks: list[Hook] = Config(default_factory=list, repr=False)
    stop_conditions: list[StopCondition[t.Sequence[AgentEvent]]] = Config(
        default_factory=list,
        repr=False,
    )
    judge: Judge[Rubric] | None = Config(default=None, repr=False)
    trajectory: Trajectory = Field(default_factory=Trajectory, exclude=True, repr=False)
    max_steps: int = Config(default=1000, ge=1)
    """Maximum number of generation/tool steps before the agent stops."""
    generation_timeout: int | None = Config(default=None)
    """Timeout in seconds for each LLM generation call. None = no timeout."""
    generate_params_extra: dict[str, t.Any] = Config(default_factory=dict)
    """Extra parameters merged into GenerateParams for every generation (e.g. thinking config)."""
    backoff_max_tries: int = Config(default=8, ge=0)
    """Maximum retries on transient LLM API errors per step. ``0`` disables retry."""
    backoff_max_time: float = Config(default=300.0, ge=0)
    """Maximum total seconds to spend retrying transient LLM API errors per step."""
    backoff_base_factor: float = Config(default=1.0, ge=0)
    """Base factor for exponential backoff: wait = base_factor * 2 ** (attempt - 1)."""
    backoff_jitter: bool = Config(default=True)
    """Whether to add up to ``backoff_base_factor`` seconds of random jitter to each wait."""
    engine: str | AgentEngine | None = Config(default=None, expose_as=str | None)
    """Owner of the agent loop. ``None``/``"native"`` runs the in-process loop; a
    built-in name (e.g. ``"claude-code"``) or a ``mod:attr`` reference delegates the
    loop to a foreign harness while sessions/eval/optimization/policy keep working."""

    # Private state
    _generator: Generator | None = PrivateAttr(None, init=False)
    _current_input: str = PrivateAttr("", init=False)
    _permission_bridge: PermissionBridge | None = PrivateAttr(None, init=False)
    """Tool-approval bridge injected by the runtime so foreign engines wire their
    permission callback into the native HITL path. ``None`` for bare-SDK use."""

    # Discoverability namespace for the AgentJudge specialized construction.
    # Assigned at module-load time by ``dreadnode.agents.__init__._lazy_init``
    # to break the import cycle between Agent and AgentJudge (which in turn
    # imports the llm_judge scorer stack).
    if t.TYPE_CHECKING:
        from dreadnode.agents.judge import AgentJudge

        Judge: t.ClassVar[type[AgentJudge]]

    @field_validator("tools", mode="before")
    @classmethod
    def validate_tools(cls, value: t.Any) -> t.Any:
        resolved = flatten_list(value)

        tools: list[Tool | Toolset] = []
        for tool in resolved:
            if isinstance(tool, (Toolset, Tool)):
                tools.append(tool)
            elif interior_tools := discover_tools_on_obj(tool):
                tools.extend(interior_tools)
            else:
                tools.append(
                    Tool.from_callable(tool if isinstance(tool, Component) else component(tool))
                )
        return tools

    @field_validator("hooks", mode="before")
    @classmethod
    def validate_hooks(cls, value: t.Any) -> list[Hook]:
        if value is None:
            return []
        if callable(value):
            return [value]
        return list(value)

    @field_validator("stop_conditions", mode="before")
    @classmethod
    def validate_stop_conditions(
        cls,
        value: t.Any,
    ) -> list[StopCondition[t.Sequence[AgentEvent]]]:
        return StopCondition.fit_many(value)

    @model_validator(mode="after")
    def ensure_agent_tag(self) -> "Agent":
        if "agent" not in self.tags:
            self.tags.insert(0, "agent")
        return self

    @property
    def model_name(self) -> str | None:
        if self.model is not None:
            return self.generator.to_identifier(short=True)
        return None

    @property
    def generator(self) -> Generator:
        if self._generator is not None:
            return self._generator

        if isinstance(self.model, str):
            self._generator = get_generator(self.model)
        elif isinstance(self.model, Generator):
            self._generator = self.model
        else:
            raise TypeError("Model must be a string or a Generator instance.")

        return self._generator

    @property
    def all_tools(self) -> list[Tool]:
        flat_tools: list[Tool] = []
        for item in self.tools:
            if isinstance(item, Toolset):
                flat_tools.extend(item.get_tools())
            elif isinstance(item, Tool):
                flat_tools.append(item)
        return flat_tools

    @property
    def history(self) -> list[Message]:
        """Get conversation history."""
        return self.trajectory.messages

    def _get_transforms(self) -> list[Transform]:
        """Resolve message transforms for the current configuration."""
        transforms = []
        if self.tools:
            match self.tool_mode:
                case "xml":
                    transforms.append(
                        make_tools_to_xml_transform(self.all_tools, add_tool_stop_token=True)
                    )
                case "json-in-xml":
                    transforms.append(tools_to_json_in_xml_transform)
                case "json-with-tag":
                    transforms.append(tools_to_json_with_tag_transform)
                case "json":
                    transforms.append(tools_to_json_transform)
                case "pythonic":
                    transforms.append(tools_to_pythonic_transform)
        return transforms

    async def _generate(self, messages: list[Message]) -> Chat:
        """Execute a single LLM generation step."""
        messages = list(messages)
        extra = dict(self.generate_params_extra) if self.generate_params_extra else {}
        params_kwargs: dict[str, t.Any] = {
            "tools": [tool.api_definition for tool in self.all_tools],
            "timeout": self.generation_timeout,
        }
        if extra:
            params_kwargs["extra"] = extra
        params = GenerateParams(**params_kwargs)

        if self.tool_mode == "auto" and self.tools:
            self.tool_mode = (
                "api" if await self.generator.supports_function_calling() else "json-in-xml"
            )

        transforms = self._get_transforms()
        post_transforms: list[PostTransform | None] = []
        for transform_callback in transforms:
            messages, params, post_transform = await transform_callback(messages, params)
            post_transforms.append(post_transform)

        try:
            if self.cache is not None and self.generator.supports_prompt_caching():
                messages = caching.apply_cache_mode_to_messages(self.cache, [messages])[0]
            logger.trace(f"Generating with model '{self.generator.model}'. Messages: {messages!r}")

            generated = (await self.generator.generate_messages([messages], [params]))[0]
            if isinstance(generated, BaseException):
                _raise_exception(generated)

            chat = Chat(
                messages,
                [generated.message],
                generator=self.generator,
                params=params,
                stop_reason=generated.stop_reason,
                usage=generated.usage,
                extra=generated.extra,
            )
        except Exception as error:
            logger.opt(exception=True).error("Error during generation")
            chat = Chat(
                messages,
                [],
                generator=self.generator,
                params=params,
                failed=True,
                error=error,
            )

        for post_transform in [tf for tf in post_transforms if tf]:
            chat = await post_transform(chat) or chat

        return chat

    async def _dispatch(self, event: AgentEvent) -> t.AsyncIterator[AgentEvent]:
        """
        Dispatch an event through hooks and handle reactions.

        Hooks are evaluated in order. Each hook may:
        1. Check `when` conditions (ScoringConditions attach metrics as side effects)
        2. Run `scorers` and attach metrics to the event
        3. Return a Reaction to control agent flow

        Metrics attached by hooks are available on event.metrics after dispatch.
        """
        # Run all hooks first (may attach metrics to event)
        hook_reactions: dict[str, Reaction | None] = {}
        for hook in self.hooks:
            hook_name = getattr(hook, "__name__", getattr(hook, "__qualname__", safe_repr(hook)))

            reaction: Reaction | None = None
            try:
                reaction = hook(event)
                if inspect.isawaitable(reaction):
                    reaction = t.cast("Reaction", await reaction)
            except Reaction as r:
                reaction = r

            if reaction is None:
                continue

            logger.debug(f"Hook '{hook_name}' returned reaction: {reaction!r}")

            if not isinstance(reaction, Reaction):
                warn_at_user_stacklevel(
                    f"Hook '{hook_name}' returned {reaction}, expected a Reaction.",
                    AgentWarning,
                )
                continue

            if isinstance(event, (AgentEnd, ReactStep)):
                warn_at_user_stacklevel(
                    f"Hook '{hook_name}' returned {reaction} during {type(event).__name__}, ignored.",
                    AgentWarning,
                )
                continue

            hook_reactions[hook_name] = reaction

        # Yield event after hooks have attached metrics
        yield event

        if not hook_reactions:
            return

        # Priority: Finish > Fail > Retry > Continue
        winning_reaction = next((r for r in hook_reactions.values() if isinstance(r, Finish)), None)
        winning_reaction = winning_reaction or next(
            (r for r in hook_reactions.values() if isinstance(r, Fail)), None
        )
        winning_reaction = winning_reaction or next(
            (r for r in hook_reactions.values() if isinstance(r, (Retry, RetryWithFeedback))), None
        )
        winning_reaction = winning_reaction or next(
            (r for r in hook_reactions.values() if isinstance(r, Continue)), None
        )
        winning_reaction = winning_reaction or next(
            (r for r in hook_reactions.values() if r is not None), None
        )

        if winning_reaction is None:
            return

        winning_hook_name = next(
            (name for name, r in hook_reactions.items() if r is winning_reaction), "unknown"
        )

        async for _event in self._dispatch(
            ReactStep(
                agent_id=self.agent_id,
                hook_name=winning_hook_name,
                reaction=winning_reaction,
            )
        ):
            yield _event

        if isinstance(winning_reaction, Continue):
            messages = list(winning_reaction.messages)
            if winning_reaction.feedback:
                messages.append(Message("user", winning_reaction.feedback))
            raise Continue(messages=messages)
        if isinstance(winning_reaction, RetryWithFeedback):
            messages = [Message("user", winning_reaction.feedback)]
            raise Retry(messages=messages)

        raise winning_reaction

    def _try_backoff(
        self,
        error: BaseException,
        *,
        tries: int,
        start_time: float,
    ) -> float | None:
        """Compute a retry sleep for a transient LLM API error.

        Returns the sleep duration in seconds if the caller should retry, or
        ``None`` if the error is not transient, tries are exhausted, or the
        per-step time budget has been spent. Caller owns sleeping and emitting
        the ``GenerationRetry`` event. Backoff is agent-owned at the error
        site, mirroring ``_try_overflow_recovery`` — no step is consumed and
        no hook indirection is involved.
        """
        if self.backoff_max_tries <= 0:
            return None

        if not _is_transient_api_error(error):
            return None

        if tries >= self.backoff_max_tries:
            logger.warning("Backoff aborted: max tries ({}) exceeded.", self.backoff_max_tries)
            return None

        remaining = self.backoff_max_time - (time.monotonic() - start_time)
        if remaining <= 0:
            logger.warning("Backoff aborted: max time ({:.2f}s) exceeded.", self.backoff_max_time)
            return None

        seconds = self.backoff_base_factor * (2**tries)
        if self.backoff_jitter:
            seconds += random.uniform(0, self.backoff_base_factor)
        if seconds > remaining:
            logger.warning(
                "Backoff aborted: next sleep ({:.2f}s) would exceed remaining budget ({:.2f}s).",
                seconds,
                remaining,
            )
            return None
        return seconds

    async def _try_overflow_recovery(
        self,
        error: BaseException,
        messages: list[Message],
    ) -> list[Message] | None:
        """Attempt to recover from a context length error by compacting messages.

        Returns compacted messages on success, None if recovery is not possible.
        Overflow recovery is agent-owned — it happens at the error site rather
        than via hook indirection.
        """
        from dreadnode.agents.hooks import (
            _get_model_context_budget,
            _is_context_length_error,
            find_summarization_boundary,
            summarize_conversation,
        )

        if not _is_context_length_error(error):
            logger.debug(
                "Overflow recovery: error not classified as context-length ({}: {}); skipping",
                type(error).__name__,
                str(error)[:200],
            )
            return None

        if len(messages) <= 10:
            logger.info(
                "Overflow recovery: too few messages to compact ({} <= 10); skipping",
                len(messages),
            )
            return None

        work = list(messages)
        system_message: Message | None = work.pop(0) if work and work[0].role == "system" else None

        summarizer = self._generator
        if summarizer is None:
            logger.warning("Overflow recovery: no summarizer generator available; skipping")
            return None

        # Cap summarizer input at ~60% of the model's token budget (~3 chars/token,
        # conservative to prefer over-truncating on code/JSON-heavy content).
        # This keeps the recovery call itself from overflowing the same provider
        # context that triggered recovery.
        budget_tokens = _get_model_context_budget(summarizer)
        max_summarize_chars = int(budget_tokens * 0.6 * 3)

        boundary = find_summarization_boundary(
            work,
            min_messages_to_keep=10,
            max_summarize_chars=max_summarize_chars,
        )
        if boundary == 0:
            # Distinguish "no safe boundary exists" (neither a simple-assistant
            # nor a complete tool-call group anywhere in the trajectory) from
            # "boundaries exist but none fit the summarizer budget". Both
            # currently return 0; telling them apart is the diagnostic split
            # point ENG-6545 needs.
            uncapped_boundary = find_summarization_boundary(work, min_messages_to_keep=10)
            if uncapped_boundary == 0:
                logger.info(
                    "Overflow recovery: no API-safe boundary in {} messages "
                    "(no simple-assistant or complete tool-call group); skipping",
                    len(work),
                )
            else:
                logger.info(
                    "Overflow recovery: valid boundary at index {} exceeds summarizer "
                    "budget (messages={}, budget_tokens={}, max_chars={}); skipping",
                    uncapped_boundary,
                    len(work),
                    budget_tokens,
                    max_summarize_chars,
                )
            return None

        to_summarize = work[:boundary]
        to_keep = work[boundary:]

        logger.info(
            "Overflow recovery: summarizing {} messages, keeping {}",
            len(to_summarize),
            len(to_keep),
        )

        try:
            summary = await summarize_conversation(
                summarizer,
                "\n".join(str(msg) for msg in to_summarize),
            )
        except Exception:
            logger.warning("Overflow recovery: summarization failed", exc_info=True)
            return None

        new_messages: list[Message] = []
        if system_message:
            new_messages.append(system_message)
        new_messages.append(
            make_compaction_message(
                summary.summary,
                messages_compacted=len(to_summarize),
                trigger="overflow_recovery",
            )
        )
        new_messages.extend(to_keep)
        return new_messages

    async def _process_tool_call(
        self, tool_call: "ToolCall", step_count: int
    ) -> t.AsyncGenerator[AgentEvent, None]:
        """Process a single tool call with its own span."""
        with dreadnode.task_span(
            f"tool:{tool_call.name}",
            type="tool",
            label=tool_call.id[:8],
            tags=["tool", tool_call.name],
        ) as t_span:
            start_event = ToolStart(
                agent_id=self.agent_id,
                agent_name=self.name,
                status="running",
                tool_call=tool_call,
            )
            start_event.emit(t_span)
            async for event in self._dispatch(start_event):
                yield event

            tool = next((t for t in self.all_tools if t.wire_name == tool_call.name), None)

            if tool is None:
                error_msg = f"Tool '{tool_call.name}' not found."
                logger.warning(error_msg)

                error_event = ToolError(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    tool_call=tool_call,
                    error=NameError(error_msg),
                )
                error_event.emit(t_span)
                async for event in self._dispatch(error_event):
                    yield event

                message = Message.from_model(
                    SystemErrorModel(content=f"Tool '{tool_call.name}' not found.")
                )

                step_event = ToolStep(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    status="running",
                    step=step_count,
                    messages=[message],
                    error=None,
                    stop=False,
                    tool_call=tool_call,
                )
                async for event in self._dispatch(step_event):
                    yield event
                step_event.emit(t_span)  # Emit after dispatch - metrics attached

                return

            try:
                message, stop = await tool.handle_tool_call(tool_call)

                # Tools that catch their own exceptions (bash non-zero,
                # @tool(catch=True), MCP isError) lift the failure into
                # message.metadata. Surface it on ToolEnd so renderers can
                # mark the call as errored without needing to parse XML
                # out of the result body.
                tool_error = message.metadata.get("error")
                tool_error_type = message.metadata.get("error_type")
                tool_cost_usd = message.metadata.get("subagent_cost_usd")

                end_event = ToolEnd(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    tool_call=tool_call,
                    result=message.content,
                    output_file=message.metadata.get("output_file"),
                    stop=stop,
                    error=tool_error,
                    error_type=tool_error_type,
                    cost_usd=tool_cost_usd,
                )
                async for event in self._dispatch(end_event):
                    yield event
                end_event.emit(t_span)  # Emit after dispatch - metrics attached

                # ToolStep.error is typed for actual exceptions (uncaught
                # errors that get re-raised). The metadata error string is
                # already on ToolEnd.error above — don't double-emit it
                # here, or Pydantic will reject the str input and the
                # raised ValidationError will surface as a duplicate
                # ToolError row in the TUI.
                step_event = ToolStep(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    status="running",
                    step=step_count,
                    messages=[message],
                    error=None,
                    stop=stop,
                    tool_call=tool_call,
                )
                async for event in self._dispatch(step_event):
                    yield event
                step_event.emit(t_span)  # Emit after dispatch - metrics attached

            except Exception as e:
                if isinstance(e, Reaction):
                    raise

                logger.opt(exception=True).error(f"Error executing tool '{tool_call.name}'")

                error_event = ToolError(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    status="errored",
                    tool_call=tool_call,
                    error=e,
                )
                error_event.emit(t_span)
                async for event in self._dispatch(error_event):
                    yield event
                raise

    async def _stream(
        self, trajectory: Trajectory | None = None
    ) -> t.AsyncGenerator[AgentEvent, None]:
        """Drive the loop through the resolved :class:`AgentEngine`.

        For the native engine this delegates straight to ``_native_run_loop``
        (which dispatches its own hooks inline). Foreign engines yield translated
        native events and call ``ctx.dispatch`` themselves for observational hooks.
        This shim is the ``Executor._stream`` implementation; the surrounding span,
        trajectory accumulation, and tool-context management stay in ``stream``.
        """
        engine = self._resolve_engine()
        ctx = EngineContext(
            agent=self,
            trajectory=trajectory if trajectory is not None else self.trajectory,
            goal=self._current_input,
            dispatch=self._dispatch,
            permission=self._permission_bridge,
        )
        async for event in engine.run_loop(ctx):
            yield event

    def _resolve_engine(self) -> AgentEngine:
        """Resolve this agent's ``engine`` selector to a concrete engine instance."""
        return resolve_engine(self.engine)

    async def _native_run_loop(
        self, trajectory: Trajectory | None = None
    ) -> t.AsyncGenerator[AgentEvent, None]:
        """
        Core agent execution loop with inline tracing.

        Events own their telemetry via emit(span). This method just creates
        spans, creates events, calls event.emit(span), and yields.

        Args:
            trajectory: The trajectory to read state from during execution.
                        Falls back to ``self.trajectory`` when ``None``.
        """
        traj = trajectory if trajectory is not None else self.trajectory
        messages = [
            *deepcopy(traj.messages),
            Message(
                "user",
                str(self._current_input),
                metadata={"agent": self.name, "model": self.model_name},
            ),
        ]
        messages = inject_system_content(messages, self.instructions)

        # The user message we just added - needed for trajectory on first step
        user_message = messages[-1]

        step_count = 0
        error: Exception | str | None = None

        async for event in self._dispatch(
            AgentStart(
                agent_id=self.agent_id,
                agent_name=self.name,
                inputs={"goal": self._current_input},
                params={
                    "session_id": str(traj.session_id),
                    "max_steps": self.max_steps,
                    **({"model": self.model_name} if self.model_name else {}),
                    **({"tools": [tool.name for tool in self.all_tools]} if self.all_tools else {}),
                },
            )
        ):
            yield event

        # Core step loop
        max_steps_reached = False
        while True:
            if step_count >= self.max_steps:
                max_steps_reached = True
                break
            step_count += 1

            try:
                # Keep generation span open for entire step (generation + tools)
                # This ensures tool spans are children of the generation span
                with dreadnode.task_span(
                    "generation",
                    type="generation",
                    label=f"step:{step_count}",
                    tags=["llm", "generation", self.model_name]
                    if self.model_name
                    else ["llm", "generation"],
                ) as gen_span:
                    # Emit GenerationStart before LLM call
                    gen_start = GenerationStart(
                        agent_id=self.agent_id,
                        agent_name=self.name,
                        generator=self._generator,
                        step=step_count,
                        messages=list(messages),
                    )
                    gen_start.emit(gen_span)
                    async for event in self._dispatch(gen_start):
                        yield event

                    step_chat = await self._generate(messages)

                    # In-place transient-error backoff — rate limits and
                    # other litellm.APIError failures get retried at the
                    # error site with exponential backoff. No step budget
                    # consumed; clients observe GenerationRetry events
                    # rather than a spurious terminal GenerationError.
                    backoff_tries = 0
                    backoff_started = time.monotonic()
                    while step_chat.failed and step_chat.error:
                        wait = self._try_backoff(
                            step_chat.error,
                            tries=backoff_tries,
                            start_time=backoff_started,
                        )
                        if wait is None:
                            break
                        backoff_tries += 1
                        logger.warning(
                            "Backing off {:.2f}s (try {}/{})",
                            wait,
                            backoff_tries,
                            self.backoff_max_tries,
                        )
                        retry_event = GenerationRetry(
                            agent_id=self.agent_id,
                            agent_name=self.name,
                            step=step_count,
                            attempt=backoff_tries,
                            max_attempts=self.backoff_max_tries,
                            wait_seconds=wait,
                            error_type=type(step_chat.error).__name__,
                            error_message=str(step_chat.error),
                        )
                        async for event in self._dispatch(retry_event):
                            yield event
                        await asyncio.sleep(wait)
                        step_chat = await self._generate(messages)

                    # In-place overflow recovery — at most once per step,
                    # no step budget consumed, preserves step_count for
                    # user_message inclusion in trajectory.
                    if step_chat.failed and step_chat.error:
                        recovered_messages = await self._try_overflow_recovery(
                            step_chat.error, messages
                        )
                        if recovered_messages is not None:
                            ce = CompactionEvent(
                                agent_id=self.agent_id,
                                agent_name=self.name,
                                trigger="overflow_recovery",
                                compaction_status="completed",
                                messages_before=len(messages),
                                messages_after=len(recovered_messages),
                            )
                            async for event in self._dispatch(ce):
                                yield event
                            messages = recovered_messages
                            step_chat = await self._generate(messages)
                            if step_chat.failed and step_chat.error:
                                logger.warning(
                                    "Overflow recovery: compacted regenerate also failed ({}: {})",
                                    type(step_chat.error).__name__,
                                    str(step_chat.error)[:200],
                                )

                    if step_chat.failed and step_chat.error:
                        from dreadnode.agents.hooks import _describe_generation_error

                        logger.error(
                            "Generation step failed: {}",
                            _describe_generation_error(step_chat.error),
                        )
                        error_event = GenerationError(
                            agent_id=self.agent_id,
                            agent_name=self.name,
                            generator=self._generator,
                            error=step_chat.error,
                            step=step_count,
                            messages=list(messages),
                        )
                        error_event.emit(gen_span)
                        async for event in self._dispatch(error_event):
                            yield event
                        error = t.cast("Exception", step_chat.error)
                        break

                    step_chat.generated[-1].metadata.update(step_chat.extra)
                    for msg in step_chat.generated:
                        msg.metadata.setdefault("agent", self.name)
                        msg.metadata.setdefault("model", self.model_name)
                    messages.extend(step_chat.generated)

                    # Emit content for TUI rendering BEFORE tools/stop-checks
                    # so text is visible immediately (ENG-5879)
                    last_msg = step_chat.generated[-1] if step_chat.generated else None
                    if last_msg and last_msg.content:
                        yield GenerationContent(
                            agent_id=self.agent_id,
                            agent_name=self.name,
                            step=step_count,
                            content=str(last_msg.content),
                            extra=step_chat.extra,
                        )

                    # Check stop conditions INSIDE span
                    if any(cond(traj.steps) for cond in self.stop_conditions):
                        logger.info("A stop condition was met. Ending run.")
                        gen_end = GenerationEnd(
                            agent_id=self.agent_id,
                            agent_name=self.name,
                            generator=self._generator,
                            messages=step_chat.generated,
                            step=step_count,
                            usage=step_chat.usage or Usage(),
                            stop_reason=step_chat.stop_reason,
                        )
                        gen_end.emit(gen_span)
                        async for event in self._dispatch(gen_end):
                            yield event

                        # First step includes user message, subsequent steps only assistant
                        step_messages = (
                            [user_message, *step_chat.generated]
                            if step_count == 1
                            else list(step_chat.generated)
                        )
                        gen_event = GenerationStep(
                            agent_id=self.agent_id,
                            agent_name=self.name,
                            status="running",
                            generator=self._generator,
                            messages=step_messages,
                            step=step_count,
                            usage=step_chat.usage or Usage(),
                            stop_reason=step_chat.stop_reason,
                            extra=step_chat.extra,
                            generation_failed=step_chat.failed,
                        )
                        async for event in self._dispatch(gen_event):
                            yield event
                        gen_event.emit(gen_span)  # Emit after dispatch - metrics attached
                        break

                    # Check if no tool calls - emit GenerationEnd and GenerationStep
                    if not messages[-1].tool_calls:
                        gen_end = GenerationEnd(
                            agent_id=self.agent_id,
                            agent_name=self.name,
                            generator=self._generator,
                            messages=step_chat.generated,
                            step=step_count,
                            usage=step_chat.usage or Usage(),
                            stop_reason=step_chat.stop_reason,
                        )
                        gen_end.emit(gen_span)
                        async for event in self._dispatch(gen_end):
                            yield event

                        # First step includes user message, subsequent steps only assistant
                        step_messages = (
                            [user_message, *step_chat.generated]
                            if step_count == 1
                            else list(step_chat.generated)
                        )
                        gen_event = GenerationStep(
                            agent_id=self.agent_id,
                            agent_name=self.name,
                            status="running",
                            generator=self._generator,
                            messages=step_messages,
                            step=step_count,
                            usage=step_chat.usage or Usage(),
                            stop_reason=step_chat.stop_reason,
                            extra=step_chat.extra,
                            generation_failed=step_chat.failed,
                        )
                        async for event in self._dispatch(gen_event):
                            yield event
                        gen_event.emit(gen_span)  # Emit after dispatch - metrics attached

                        if not self.stop_conditions:
                            break

                        logger.warning(
                            f"Agent '{self.name}' stalled: No tool calls and no stop conditions met."
                        )
                        async for event in self._dispatch(
                            AgentStalled(
                                agent_id=self.agent_id, agent_name=self.name, status="stalled"
                            )
                        ):
                            yield event
                        break

                    # Process tool calls in parallel with streaming events
                    stopped_by_tool_call: ToolCall | None = None
                    tool_messages: list[Message] = []
                    tool_execution_error: Exception | None = None

                    # Queue for events from parallel tool execution
                    event_queue: asyncio.Queue[AgentEvent | None] = asyncio.Queue()

                    async def run_tool_with_queue(
                        tc: ToolCall,
                        _step_count: int = step_count,
                        _event_queue: asyncio.Queue[AgentEvent | None] = event_queue,
                    ) -> None:
                        """Run tool and put events in queue."""
                        async for event in self._process_tool_call(tc, _step_count):
                            await _event_queue.put(event)

                    async def run_all_tools(
                        _messages: list[Message] = messages,
                        _event_queue: asyncio.Queue[AgentEvent | None] = event_queue,
                    ) -> None:
                        """Run all tools and signal completion."""
                        nonlocal tool_execution_error
                        try:
                            await asyncio.gather(
                                *[
                                    run_tool_with_queue(tc)
                                    for tc in (_messages[-1].tool_calls or [])
                                ]
                            )
                        except Exception as exc:
                            tool_execution_error = exc
                        finally:
                            await _event_queue.put(None)  # Signal done

                    # Start tools in background
                    tools_task = asyncio.create_task(run_all_tools())

                    # Yield events as they arrive
                    while True:
                        event = await event_queue.get()
                        if event is None:
                            break
                        yield event
                        if isinstance(event, ToolStep):
                            tool_messages.extend(event.messages)
                            if stopped_by_tool_call is None and event.stop:
                                stopped_by_tool_call = event.tool_call

                    await tools_task  # Ensure task completes
                    if tool_execution_error is not None:
                        _raise_exception(tool_execution_error)
                    messages.extend(tool_messages)

                    # Emit GenerationEnd AFTER tools (closes generation span)
                    gen_end = GenerationEnd(
                        agent_id=self.agent_id,
                        agent_name=self.name,
                        generator=self._generator,
                        messages=step_chat.generated,
                        step=step_count,
                        usage=step_chat.usage or Usage(),
                        stop_reason=step_chat.stop_reason,
                    )
                    gen_end.emit(gen_span)
                    async for event in self._dispatch(gen_end):
                        yield event

                    # GenerationStep for trajectory
                    # First step includes user message, subsequent steps only assistant
                    # Tool results are captured by ToolStep events separately
                    step_messages = (
                        [user_message, *step_chat.generated]
                        if step_count == 1
                        else list(step_chat.generated)
                    )
                    gen_event = GenerationStep(
                        agent_id=self.agent_id,
                        agent_name=self.name,
                        status="running",
                        generator=self._generator,
                        messages=step_messages,
                        step=step_count,
                        usage=step_chat.usage or Usage(),
                        stop_reason=step_chat.stop_reason,
                        extra=step_chat.extra,
                        generation_failed=step_chat.failed,
                    )
                    async for event in self._dispatch(gen_event):
                        yield event
                    gen_event.emit(gen_span)  # Emit after dispatch - metrics attached

                    if stopped_by_tool_call:
                        _raise_exception(
                            Finish(
                                f"Tool '{stopped_by_tool_call.name}' requested to stop the agent."
                            )
                        )

                    # Check stop conditions again INSIDE span
                    if any(cond(traj.steps) for cond in self.stop_conditions):
                        break

            except Continue as e:
                # Continue with feedback - append messages and proceed
                if e.messages:
                    messages.extend(e.messages)
                continue
            except Retry as e:
                messages = e.messages or messages
                continue
            except Fail as e:
                error = e.error
                break
            except Finish:
                break
            except Exception as e:
                logger.opt(exception=True).error("Agent execution error")
                error = e
                break

        # Determine stop reason
        stop_reason: AgentStopReason = "finished"
        if error is not None:
            stop_reason = "error"
        elif max_steps_reached:
            stop_reason = "max_steps_reached"
        elif traj.steps and isinstance(traj.steps[-1], AgentStalled):
            stop_reason = "stalled"

        async for event in self._dispatch(
            AgentEnd(
                agent_id=self.agent_id,
                agent_name=self.name,
                status="errored" if error else "finished",
                stop_reason=stop_reason,
                error=error,
            )
        ):
            yield event

    async def _stream_batch(self, batch: list[t.Any]) -> t.AsyncGenerator[AgentEvent, None]:  # noqa: ARG002
        """Agent execution is goal-based and does not support batch streaming."""
        raise NotImplementedError("Agent uses stream(goal=...), not batch streaming.")
        if False:  # pragma: no cover
            yield t.cast("AgentEvent", None)

    @asynccontextmanager
    async def stream(
        self,
        goal: str,
        *,
        reset: bool = True,
        trajectory: Trajectory | None = None,
    ) -> t.AsyncIterator[t.AsyncGenerator[AgentEvent, None]]:
        """
        Stream agent execution.

        Args:
            goal: Input message for the agent.
            reset: If True, start new conversation. If False, continue existing.
                   Ignored when *trajectory* is provided.
            trajectory: External trajectory to operate on.  When provided the
                        agent's internal trajectory is left untouched and all
                        events accumulate on the supplied object instead.
        """
        self._current_input = goal

        # Resolve the active trajectory for this run.
        if trajectory is not None:
            # External trajectory — operate directly on it, leave self.trajectory alone.
            active_trajectory = trajectory
        elif reset:
            # Fresh internal trajectory.
            self.trajectory = Trajectory(
                agent_id=self.agent_id,
                system_prompt=self.instructions,
            )
            active_trajectory = self.trajectory
        else:
            # Continue on the existing internal trajectory.
            active_trajectory = self.trajectory

        async with AsyncExitStack() as stack:
            # Enter tool contexts
            for tool_container in self.tools:
                if hasattr(tool_container, "__aenter__") and hasattr(tool_container, "__aexit__"):
                    await stack.enter_async_context(tool_container)

            display_name = self.name or str(self.agent_id)[:8]
            ctx = dreadnode.task_span(
                f"agent:{display_name}",
                type="agent",
                label=display_name,
                tags=["agent"],
            )

            with ctx as parent_span:

                async def _events() -> t.AsyncGenerator[AgentEvent, None]:
                    async for event in self._stream(active_trajectory):
                        # Emit agent-level events to parent span
                        if parent_span and isinstance(
                            event, (AgentStart, AgentEnd, AgentStalled, AgentError)
                        ):
                            with suppress(AttributeError):
                                event.emit(parent_span)

                        # Track steps and lifecycle events in trajectory
                        if isinstance(event, (AgentStep, AgentStart, AgentEnd)):
                            active_trajectory.add_event(event)

                        yield event

                yield _events()

    async def run(  # ty: ignore[invalid-method-override]  # intentional override with agent-specific parameters
        self, goal: str, *, reset: bool = True, trajectory: Trajectory | None = None
    ) -> Trajectory:
        """Execute the agent and return the trajectory."""
        async with self.stream(goal, reset=reset, trajectory=trajectory) as events:
            async for event in events:
                if isinstance(event, AgentEnd):
                    return trajectory if trajectory is not None else self.trajectory

        raise RuntimeError("Agent run finished unexpectedly.")

    def reset(self) -> Trajectory:
        """Reset the agent's internal state."""
        previous = self.trajectory
        self.trajectory = Trajectory(
            agent_id=self.agent_id,
            system_prompt=self.instructions,
        )
        return previous

    def task(self, *, name: str | None = None) -> Task[[str], Trajectory]:
        """
        Convert this agent to a Task for use with Evaluation or Study.

        The resulting Task takes a goal string and returns a Trajectory.
        This is the bridge between Agent and the evaluation/optimization systems.

        Args:
            name: Optional name for the task. Defaults to agent name.

        Returns:
            A Task that wraps agent.run().

        Example:
            ```python
            agent = Agent(name="my_agent", ...)

            # Use with Evaluation
            evaluation = Evaluation(
                task=agent.as_task(),
                dataset=[{"goal": "..."}],
                scorers=[my_scorer],
            )
            result = await evaluation.run()

            # Use with Study
            study = Study(
                task_factory=lambda params: agent.with_(**params).as_task(),
                ...
            )
            ```
        """
        agent = self
        task_name = name or self.name

        @task(name=task_name)
        async def agent_task(goal: str) -> Trajectory:
            return await agent.run(goal)

        return agent_task
