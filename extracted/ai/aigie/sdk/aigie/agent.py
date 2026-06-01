"""
Agent - Type-safe agent with dependency injection and tool registration.

Provides a clean, type-safe API for building AI agents with automatic
tracing, tool management, and structured outputs.

Example:
    ```python
    from aigie import Agent, RunContext
    from pydantic import BaseModel

    class MyDeps:
        db: Database

    class OutputModel(BaseModel):
        answer: str
        confidence: float

    agent = Agent[MyDeps, OutputModel](
        'openai:gpt-4',
        output_type=OutputModel,
        system_prompt='You are a helpful assistant'
    )

    @agent.tool
    async def search(ctx: RunContext[MyDeps], query: str) -> str:
        return await ctx.deps.db.search(query)

    result = await agent.run('Find info about AI', deps=MyDeps(db=db))
    print(result.data.answer)  # Typed!
    ```
"""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import uuid
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import (
    Any,
    Generic,
    Literal,
    TypeVar,
    Union,
)

from .result import AgentResult, UnifiedError, UsageInfo
from .run_context import (
    DepsT,
    Message,
    ModelRetry,
    RunContext,
    run_context,
)

# Type variables
OutputT = TypeVar("OutputT")
ArgsT = TypeVar("ArgsT")
ResultT = TypeVar("ResultT")


@dataclass
class Tool:
    """
    Tool definition with auto-schema generation.

    Tools are registered on agents and can be called by the LLM
    during execution. The schema is automatically generated from
    function type hints.

    Attributes:
        func: The function to call
        name: Name of the tool (used by LLM)
        description: Description for the LLM
        schema: JSON Schema for parameters
        requires_context: Whether the function takes RunContext
    """

    func: Callable
    name: str
    description: str
    schema: dict[str, Any]
    requires_context: bool = True
    is_async: bool = True

    def to_openai_tool(self) -> dict[str, Any]:
        """Convert to OpenAI function calling format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.schema,
            },
        }

    def to_anthropic_tool(self) -> dict[str, Any]:
        """Convert to Anthropic tool format."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.schema,
        }


@dataclass
class ModelSettings:
    """
    Settings for model configuration.

    Supports provider-namespaced settings to avoid conflicts.

    Attributes:
        temperature: Sampling temperature (0-2)
        max_tokens: Maximum tokens to generate
        top_p: Nucleus sampling parameter
        timeout: Request timeout in seconds

        # OpenAI-specific
        openai_reasoning_effort: Reasoning effort for o1/o3 models

        # Anthropic-specific
        anthropic_thinking_budget: Token budget for extended thinking
    """

    temperature: float | None = None
    max_tokens: int | None = None
    top_p: float | None = None
    timeout: float | None = None
    seed: int | None = None

    # OpenAI-specific
    openai_reasoning_effort: str | None = None
    openai_response_format: dict[str, Any] | None = None

    # Anthropic-specific
    anthropic_thinking_budget: int | None = None

    # Additional settings
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result: dict[str, Any] = {}
        if self.temperature is not None:
            result["temperature"] = self.temperature
        if self.max_tokens is not None:
            result["max_tokens"] = self.max_tokens
        if self.top_p is not None:
            result["top_p"] = self.top_p
        if self.timeout is not None:
            result["timeout"] = self.timeout
        if self.seed is not None:
            result["seed"] = self.seed
        result.update(self.extra)
        return result

    def merge(self, other: ModelSettings) -> ModelSettings:
        """Merge with another settings object (other takes precedence)."""
        return ModelSettings(
            temperature=other.temperature if other.temperature is not None else self.temperature,
            max_tokens=other.max_tokens if other.max_tokens is not None else self.max_tokens,
            top_p=other.top_p if other.top_p is not None else self.top_p,
            timeout=other.timeout if other.timeout is not None else self.timeout,
            seed=other.seed if other.seed is not None else self.seed,
            openai_reasoning_effort=other.openai_reasoning_effort or self.openai_reasoning_effort,
            openai_response_format=other.openai_response_format or self.openai_response_format,
            anthropic_thinking_budget=other.anthropic_thinking_budget
            or self.anthropic_thinking_budget,
            extra={**self.extra, **other.extra},
        )


class Agent(Generic[DepsT, OutputT]):
    """
    Type-safe agent with dependency injection and tool registration.

    The Agent class provides a clean, type-safe API for building AI agents
    with automatic tracing, tool management, and structured outputs.

    Type Parameters:
        DepsT: Type of dependencies passed to tools
        OutputT: Type of the validated output

    Attributes:
        model: Model identifier (e.g., 'openai:gpt-4')
        output_type: Pydantic model or type for output validation
        system_prompt: Static system prompt
        model_settings: Default model settings

    Example:
        ```python
        from aigie import Agent, RunContext
        from pydantic import BaseModel

        class SearchDeps:
            api_client: SearchAPI

        class SearchResult(BaseModel):
            results: list[str]
            confidence: float

        agent = Agent[SearchDeps, SearchResult](
            'openai:gpt-4',
            output_type=SearchResult,
            system_prompt='You are a search assistant'
        )

        @agent.tool
        async def search(ctx: RunContext[SearchDeps], query: str) -> str:
            return await ctx.deps.api_client.search(query)

        result = await agent.run('Find AI papers', deps=SearchDeps(...))
        print(result.data.results)  # Type-safe!
        ```
    """

    def __init__(
        self,
        model: str,
        *,
        deps_type: type[DepsT] | None = None,
        output_type: type[OutputT] | None = None,
        system_prompt: str | None = None,
        instructions: str | None = None,
        model_settings: ModelSettings | None = None,
        max_retries: int = 2,
        name: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        """
        Initialize an Agent.

        Args:
            model: Model identifier (e.g., 'openai:gpt-4', 'anthropic:claude-3-5-sonnet')
            deps_type: Optional type hint for dependencies (for documentation)
            output_type: Pydantic model for output validation
            system_prompt: Static system prompt (always at the start)
            instructions: Additional instructions (can be dynamic)
            model_settings: Default settings for model calls
            max_retries: Maximum retries on validation failure
            name: Name for tracing
            tags: Tags for tracing
            metadata: Additional metadata for tracing
        """
        self.model = model
        self._deps_type = deps_type
        self._output_type = output_type
        self._system_prompt = system_prompt
        self._instructions = instructions
        self._model_settings = model_settings or ModelSettings()
        self._max_retries = max_retries
        self._name = name or f"Agent({model})"
        self._tags = tags or []
        self._metadata = metadata or {}

        # Tool registry
        self._tools: list[Tool] = []
        self._instruction_funcs: list[Callable] = []
        self._result_validators: list[Callable] = []

    @property
    def tools(self) -> list[Tool]:
        """Get registered tools."""
        return list(self._tools)

    def tool(
        self,
        fn: Callable | None = None,
        *,
        name: str | None = None,
        description: str | None = None,
        retries: int = 0,
    ) -> Callable:
        """
        Decorator to register a function as a tool.

        The tool's schema is automatically generated from type hints.
        The description is extracted from the docstring if not provided.

        Args:
            fn: The function to register
            name: Override tool name (default: function name)
            description: Override description (default: from docstring)
            retries: Number of retries on tool failure

        Returns:
            The decorated function.

        Example:
            ```python
            @agent.tool
            async def get_weather(ctx: RunContext[Deps], location: str) -> str:
                '''Get weather for a location.'''
                return await ctx.deps.weather_api.get(location)
            ```
        """

        def decorator(func: Callable) -> Callable:
            tool_name = name or func.__name__
            tool_desc = (
                description or (func.__doc__ or "").strip().split("\n")[0] or f"Call {tool_name}"
            )

            # Generate schema from type hints
            schema = self._generate_tool_schema(func)

            # Check if function takes context
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())
            requires_context = len(params) > 0 and params[0] in ("ctx", "context", "run_context")

            # Check if async
            is_async = asyncio.iscoroutinefunction(func)

            tool = Tool(
                func=func,
                name=tool_name,
                description=tool_desc,
                schema=schema,
                requires_context=requires_context,
                is_async=is_async,
            )
            self._tools.append(tool)

            return func

        if fn is not None:
            return decorator(fn)
        return decorator

    def tool_plain(
        self,
        fn: Callable | None = None,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> Callable:
        """
        Register a tool that doesn't need RunContext.

        Same as @agent.tool but for functions that don't need
        access to the execution context.

        Example:
            ```python
            @agent.tool_plain
            def calculate(expression: str) -> float:
                '''Calculate a mathematical expression.'''
                return eval(expression)
            ```
        """

        def decorator(func: Callable) -> Callable:
            tool_name = name or func.__name__
            tool_desc = (
                description or (func.__doc__ or "").strip().split("\n")[0] or f"Call {tool_name}"
            )

            schema = self._generate_tool_schema(func)
            is_async = asyncio.iscoroutinefunction(func)

            tool = Tool(
                func=func,
                name=tool_name,
                description=tool_desc,
                schema=schema,
                requires_context=False,
                is_async=is_async,
            )
            self._tools.append(tool)

            return func

        if fn is not None:
            return decorator(fn)
        return decorator

    def instructions(self, fn: Callable) -> Callable:
        """
        Decorator for dynamic instruction generation.

        Instructions are re-evaluated on each run based on context.
        Unlike system_prompt which is static, instructions can vary
        based on dependencies or runtime state.

        Example:
            ```python
            @agent.instructions
            async def get_instructions(ctx: RunContext[Deps]) -> str:
                user = await ctx.deps.db.get_user(ctx.deps.user_id)
                return f"User's name is {user.name}. Be helpful."
            ```
        """
        self._instruction_funcs.append(fn)
        return fn

    def result_validator(self, fn: Callable) -> Callable:
        """
        Decorator to register a result validator.

        Validators run after the LLM response is parsed but before
        the result is returned. They can modify the output or raise
        ModelRetry to trigger a retry.

        Example:
            ```python
            @agent.result_validator
            async def validate_result(ctx: RunContext[Deps], result: OutputType) -> OutputType:
                if result.confidence < 0.5:
                    raise ModelRetry("Confidence too low, please be more certain")
                return result
            ```
        """
        self._result_validators.append(fn)
        return fn

    def _generate_tool_schema(self, func: Callable) -> dict[str, Any]:
        """Generate JSON Schema from function type hints."""
        hints = {}
        with contextlib.suppress(AttributeError):
            hints = func.__annotations__.copy()

        sig = inspect.signature(func)
        properties: dict[str, Any] = {}
        required: list[str] = []

        for param_name, param in sig.parameters.items():
            # Skip context parameter
            if param_name in ("ctx", "context", "run_context", "self"):
                continue

            param_type = hints.get(param_name)
            schema = self._type_to_json_schema(param_type)
            properties[param_name] = schema

            if param.default is param.empty:
                required.append(param_name)

        return {
            "type": "object",
            "properties": properties,
            "required": required,
        }

    def _type_to_json_schema(self, type_hint: Any) -> dict[str, Any]:
        """Convert a Python type hint to JSON Schema."""
        if type_hint is None:
            return {"type": "string"}

        # Get origin for generic types
        origin = getattr(type_hint, "__origin__", None)
        args = getattr(type_hint, "__args__", ())

        # Handle Optional
        if origin is Union and type(None) in args:
            non_none = [a for a in args if a is not type(None)]
            if len(non_none) == 1:
                return self._type_to_json_schema(non_none[0])

        # Handle List
        if origin is list:
            item_schema = self._type_to_json_schema(args[0]) if args else {"type": "string"}
            return {"type": "array", "items": item_schema}

        # Handle Dict
        if origin is dict:
            return {"type": "object"}

        # Handle Literal
        if origin is Literal:
            return {"type": "string", "enum": list(args)}

        # Handle basic types
        type_map = {
            str: {"type": "string"},
            int: {"type": "integer"},
            float: {"type": "number"},
            bool: {"type": "boolean"},
        }

        if type_hint in type_map:
            return type_map[type_hint]

        # Handle Pydantic models
        if hasattr(type_hint, "model_json_schema"):
            return type_hint.model_json_schema()

        # Default
        return {"type": "string"}

    async def run(
        self,
        prompt: str,
        *,
        deps: DepsT | None = None,
        message_history: list[Message] | None = None,
        model_settings: ModelSettings | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AgentResult[OutputT]:
        """
        Execute the agent with the given prompt.

        Args:
            prompt: The user prompt
            deps: Dependencies for tool execution
            message_history: Previous messages for continuation
            model_settings: Override model settings for this run
            tags: Additional tags for tracing
            metadata: Additional metadata for tracing

        Returns:
            AgentResult with typed data, usage, and messages.

        Example:
            ```python
            result = await agent.run(
                "What is the weather in Tokyo?",
                deps=MyDeps(weather_api=api)
            )
            print(result.data)
            print(f"Cost: ${result.usage.cost_usd}")
            ```
        """
        start_time = datetime.utcnow()
        trace_id = str(uuid.uuid4())

        # Merge settings
        settings = self._model_settings
        if model_settings:
            settings = settings.merge(model_settings)

        # Build messages
        messages: list[Message] = []

        # Add system prompt
        if self._system_prompt:
            messages.append(Message(role="system", content=self._system_prompt))

        # Add message history
        if message_history:
            messages.extend(message_history)

        # Create context
        ctx = RunContext(
            deps=deps,  # type: ignore
            model=self.model,
            messages=messages,
            trace_id=trace_id,
            max_retries=self._max_retries,
        )

        # Add dynamic instructions
        async with run_context(ctx):
            for instr_fn in self._instruction_funcs:
                if asyncio.iscoroutinefunction(instr_fn):
                    instr = await instr_fn(ctx)
                else:
                    instr = instr_fn(ctx)
                if instr:
                    messages.append(Message(role="system", content=instr))

            # Add user prompt
            messages.append(Message(role="user", content=prompt))
            ctx.mark_message_index()

            # Execute agent loop
            usage = UsageInfo(model=self.model)
            tool_calls_count = 0
            retries = 0

            try:
                # Call the LLM (to be implemented with actual provider)
                output = await self._execute_llm(ctx, settings)

                # Validate output
                if self._output_type:
                    output = await self._validate_output(ctx, output)

                # Run result validators
                for validator in self._result_validators:
                    if asyncio.iscoroutinefunction(validator):
                        output = await validator(ctx, output)
                    else:
                        output = validator(ctx, output)

                duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000

                return AgentResult(
                    data=output,  # type: ignore
                    usage=usage,
                    messages=ctx.messages,
                    model=self.model,
                    trace_id=trace_id,
                    duration_ms=duration_ms,
                    tool_calls=tool_calls_count,
                    retries=retries,
                    metadata={**self._metadata, **(metadata or {})},
                )

            except ModelRetry as e:
                # Handle retry
                if ctx.retry_count < self._max_retries:
                    ctx = ctx.with_retry()
                    ctx.add_user_message(f"Error: {e.message}. Please try again.")
                    return await self.run(
                        prompt="",
                        deps=deps,
                        message_history=ctx.messages,
                        model_settings=model_settings,
                        tags=tags,
                        metadata=metadata,
                    )
                raise UnifiedError(
                    message=e.message,
                    error_type="retry_exhausted",
                    trace_id=trace_id,
                    retry_count=ctx.retry_count,
                )
            except Exception as e:
                raise UnifiedError(
                    message=str(e),
                    error_type="agent_error",
                    original_error=e,
                    trace_id=trace_id,
                )

    async def _execute_llm(
        self,
        ctx: RunContext[DepsT],
        settings: ModelSettings,
    ) -> Any:
        """
        Execute LLM call with tool handling.

        This is a placeholder - actual implementation should:
        1. Parse model identifier (provider:model_name)
        2. Call the appropriate provider
        3. Handle tool calls in a loop
        4. Return final output

        For now, returns a placeholder.
        """
        # TODO: Implement actual LLM execution
        # This requires integration with the existing wrapper system
        # For now, return a placeholder that will be replaced

        # Parse model
        provider, model_name = (
            self.model.split(":", 1) if ":" in self.model else ("openai", self.model)
        )

        # Build tool definitions
        [tool.to_openai_tool() for tool in self._tools]

        # The actual implementation would:
        # 1. Get the appropriate client (OpenAI, Anthropic, etc.)
        # 2. Make the API call with tools
        # 3. Handle tool calls in a loop
        # 4. Return the final response

        # Placeholder return
        return "Placeholder response - implement LLM execution"

    async def _validate_output(
        self,
        ctx: RunContext[DepsT],
        output: Any,
    ) -> OutputT:
        """Validate and parse output against output_type."""
        if self._output_type is None:
            return output  # type: ignore

        # Handle Pydantic models
        if hasattr(self._output_type, "model_validate"):
            try:
                return self._output_type.model_validate(output)  # type: ignore
            except Exception as e:
                raise ModelRetry(f"Output validation failed: {e}")

        # Handle dict output
        if hasattr(self._output_type, "model_validate_json"):
            try:
                if isinstance(output, str):
                    return self._output_type.model_validate_json(output)  # type: ignore
            except Exception as e:
                raise ModelRetry(f"Output validation failed: {e}")

        return output  # type: ignore

    async def run_stream(
        self,
        prompt: str,
        *,
        deps: DepsT | None = None,
        message_history: list[Message] | None = None,
        model_settings: ModelSettings | None = None,
    ) -> AsyncIterator[str]:
        """
        Execute the agent with streaming output.

        Yields text chunks as they are generated.

        Example:
            ```python
            async for chunk in agent.run_stream("Tell me a story", deps=deps):
                print(chunk, end='', flush=True)
            ```
        """
        # TODO: Implement streaming
        result = await self.run(
            prompt, deps=deps, message_history=message_history, model_settings=model_settings
        )
        yield str(result.data)

    def clone(
        self,
        *,
        model: str | None = None,
        system_prompt: str | None = None,
        model_settings: ModelSettings | None = None,
    ) -> Agent[DepsT, OutputT]:
        """
        Create a copy of this agent with modified settings.

        Useful for creating variants without modifying the original.

        Example:
            ```python
            creative_agent = agent.clone(
                model_settings=ModelSettings(temperature=0.9)
            )
            ```
        """
        new_agent = Agent[DepsT, OutputT](
            model=model or self.model,
            deps_type=self._deps_type,
            output_type=self._output_type,
            system_prompt=system_prompt if system_prompt is not None else self._system_prompt,
            model_settings=model_settings or self._model_settings,
            max_retries=self._max_retries,
            name=self._name,
            tags=self._tags.copy(),
            metadata=self._metadata.copy(),
        )
        new_agent._tools = self._tools.copy()
        new_agent._instruction_funcs = self._instruction_funcs.copy()
        new_agent._result_validators = self._result_validators.copy()
        return new_agent


# Convenience function to create an agent
def create_agent(
    model: str,
    **kwargs: Any,
) -> Agent[Any, Any]:
    """
    Create an agent with the given model.

    Convenience function for creating agents without explicit type parameters.

    Example:
        ```python
        agent = create_agent('openai:gpt-4', system_prompt='You are helpful')
        ```
    """
    return Agent(model, **kwargs)


__all__ = [
    "Agent",
    "ModelSettings",
    "Tool",
    "create_agent",
]
