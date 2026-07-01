"""
Agent-specific stopping hooks.

This module provides hooks that return Finish() to stop agent execution.
Each factory function returns a Hook instance that can be passed to Agent(hooks=[...]).
"""

from __future__ import annotations

import re
import typing as t

from dreadnode.agents.events import (
    AgentEvent,
    AgentStart,
    GenerationEnd,
    GenerationStep,
    ToolEnd,
    ToolError,
)
from dreadnode.agents.reactions import Finish, Reaction
from dreadnode.core.hook import Hook

if t.TYPE_CHECKING:
    from datetime import datetime


def step_count(max_steps: int, *, name: str | None = None) -> Hook:
    """
    Stop after a maximum number of agent steps.

    Args:
        max_steps: The maximum number of steps to allow.
        name: Optional name for the hook.

    Returns:
        A Hook that returns Finish after the specified number of steps.
    """
    reason = name or f"stop_on_step_count({max_steps})"

    async def check(event: GenerationStep) -> Reaction | None:
        if event.step >= max_steps:
            return Finish(reason=reason)
        return None

    hook = Hook(check, GenerationStep)
    hook.__name__ = reason
    return hook  # ty: ignore[invalid-return-type]  # Hook is covariant on event subtype


def generation_count(max_generations: int, *, name: str | None = None) -> Hook:
    """
    Stop after a maximum number of LLM generations (inference calls).

    This is slightly more robust than using `step_count` as retry calls
    to the LLM will also count towards this limit.

    Args:
        max_generations: The maximum number of LLM generations to allow.
        name: Optional name for the hook.

    Returns:
        A Hook that returns Finish after the specified number of generations.
    """
    reason = name or f"stop_on_generation_count({max_generations})"
    count = 0

    async def check(event: AgentEvent) -> Reaction | None:
        nonlocal count
        if isinstance(event, AgentStart):
            count = 0
            return None
        if isinstance(event, GenerationEnd):
            count += 1
            if count >= max_generations:
                return Finish(reason=reason)
        return None

    hook = Hook(check, AgentEvent)
    hook.__name__ = reason
    return hook


def tool_use(tool_name: str, *, count: int = 1, name: str | None = None) -> Hook:
    """
    Stop after a specific tool has been successfully used.

    Args:
        tool_name: The name of the tool to monitor.
        count: The number of times the tool must be used to trigger stopping.
        name: Optional name for the hook.

    Returns:
        A Hook that returns Finish after the tool is used the specified number of times.
    """
    reason = name or f"stop_on_tool_use({tool_name}, {count})"
    seen = 0

    async def check(event: AgentEvent) -> Reaction | None:
        nonlocal seen
        if isinstance(event, AgentStart):
            seen = 0
            return None
        if isinstance(event, ToolEnd) and event.tool_call.name == tool_name:
            seen += 1
            if seen >= count:
                return Finish(reason=reason)
        return None

    hook = Hook(check, AgentEvent)
    hook.__name__ = reason
    return hook


def any_tool_use(*, count: int = 1, name: str | None = None) -> Hook:
    """
    Stop after any tool has been used a specified number of times.

    Args:
        count: The total number of tool uses to trigger stopping.
        name: Optional name for the hook.

    Returns:
        A Hook that returns Finish after any tools are used the specified number of times.
    """
    reason = name or f"stop_on_any_tool_use({count})"
    seen = 0

    async def check(event: AgentEvent) -> Reaction | None:
        nonlocal seen
        if isinstance(event, AgentStart):
            seen = 0
            return None
        if isinstance(event, ToolEnd):
            seen += 1
            if seen >= count:
                return Finish(reason=reason)
        return None

    hook = Hook(check, AgentEvent)
    hook.__name__ = reason
    return hook


def output(
    pattern: str | re.Pattern[str],
    *,
    case_sensitive: bool = False,
    exact: bool = False,
    regex: bool = False,
    name: str | None = None,
) -> Hook:
    """
    Stop if a specific string or pattern is mentioned in the last generated message.

    Args:
        pattern: The string or compiled regex pattern to search for.
        case_sensitive: If True, the match is case-sensitive.
        exact: If True, performs an exact string match instead of containment.
        regex: If True, treats the `pattern` string as a regular expression.
        name: Optional name for the hook.

    Returns:
        A Hook that returns Finish when the pattern is found in the output.
    """
    pattern_str = pattern.pattern if isinstance(pattern, re.Pattern) else pattern
    reason = name or f"stop_on_output({pattern_str!r})"

    async def check(event: GenerationEnd) -> Reaction | None:
        if not event.messages:
            return None
        text = event.messages[-1].content or ""
        if _match_pattern(text, pattern, case_sensitive=case_sensitive, exact=exact, regex=regex):
            return Finish(reason=reason)
        return None

    hook = Hook(check, GenerationEnd)
    hook.__name__ = reason
    return hook  # ty: ignore[invalid-return-type]  # Hook is covariant on event subtype


def tool_output(
    pattern: str | re.Pattern[str],
    *,
    tool_name: str | None = None,
    case_sensitive: bool = False,
    exact: bool = False,
    regex: bool = False,
    name: str | None = None,
) -> Hook:
    """
    Stop if a specific string or pattern is found in the output of a tool call.

    Args:
        pattern: The string or compiled regex pattern to search for.
        tool_name: If specified, only considers outputs from this tool.
        case_sensitive: If True, the match is case-sensitive.
        exact: If True, performs an exact string match instead of containment.
        regex: If True, treats the `pattern` string as a regular expression.
        name: Optional name for the hook.

    Returns:
        A Hook that returns Finish when the pattern is found in tool output.
    """
    pattern_str = pattern.pattern if isinstance(pattern, re.Pattern) else pattern
    tool_suffix = f", tool={tool_name}" if tool_name else ""
    reason = name or f"stop_on_tool_output({pattern_str!r}{tool_suffix})"

    async def check(event: ToolEnd) -> Reaction | None:
        if tool_name and event.tool_call.name != tool_name:
            return None
        if event.result is None:
            return None
        if _match_pattern(
            str(event.result), pattern, case_sensitive=case_sensitive, exact=exact, regex=regex
        ):
            return Finish(reason=reason)
        return None

    hook = Hook(check, ToolEnd)
    hook.__name__ = reason
    return hook  # ty: ignore[invalid-return-type]  # Hook is covariant on event subtype


def tool_error(tool_name: str | None = None, *, name: str | None = None) -> Hook:
    """
    Stop if any tool call results in an error.

    Args:
        tool_name: If specified, only considers errors from this tool.
        name: Optional name for the hook.

    Returns:
        A Hook that returns Finish when a tool error occurs.
    """
    reason = name or f"stop_on_tool_error({tool_name or 'any'})"

    async def check(event: ToolError) -> Reaction | None:
        if tool_name and event.tool_call.name != tool_name:
            return None
        return Finish(reason=reason)

    hook = Hook(check, ToolError)
    hook.__name__ = reason
    return hook  # ty: ignore[invalid-return-type]  # Hook is covariant on event subtype


def no_new_tool_used(for_steps: int, *, name: str | None = None) -> Hook:
    """
    Stop if the agent goes for a number of consecutive steps without using a new tool.

    A "new tool" is one that hasn't been used in any prior step. This detects
    stagnation where the agent keeps calling the same tools repeatedly.

    Args:
        for_steps: The number of consecutive steps without a new tool use
            before the agent should stop.
        name: Optional name for the hook.

    Returns:
        A Hook that returns Finish when no new tools are used for the specified steps.
    """
    reason = name or f"stop_on_no_new_tool({for_steps})"
    all_prior_tools: set[str] = set()
    steps_since_new_tool = 0
    current_step_tools: set[str] = set()

    async def check(event: AgentEvent) -> Reaction | None:
        nonlocal all_prior_tools, steps_since_new_tool, current_step_tools
        if isinstance(event, AgentStart):
            all_prior_tools = set()
            steps_since_new_tool = 0
            current_step_tools = set()
            return None
        if isinstance(event, ToolEnd):
            current_step_tools.add(event.tool_call.name)
            return None
        if isinstance(event, GenerationStep):
            new_tools = current_step_tools - all_prior_tools
            all_prior_tools.update(current_step_tools)
            current_step_tools = set()

            if new_tools:
                steps_since_new_tool = 0
            else:
                steps_since_new_tool += 1

            if steps_since_new_tool >= for_steps:
                return Finish(reason=reason)
        return None

    hook = Hook(check, AgentEvent)
    hook.__name__ = reason
    return hook


def no_tool_calls(for_steps: int = 1, *, name: str | None = None) -> Hook:
    """
    Stop if the agent goes for a number of steps without making any tool calls.

    Args:
        for_steps: The number of consecutive steps without any tool calls.
        name: Optional name for the hook.

    Returns:
        A Hook that returns Finish when no tool calls are made for the specified steps.
    """
    reason = name or f"stop_on_no_tool_calls({for_steps})"
    steps_without_tools = 0
    had_tools_this_step = False

    async def check(event: AgentEvent) -> Reaction | None:
        nonlocal steps_without_tools, had_tools_this_step
        if isinstance(event, AgentStart):
            steps_without_tools = 0
            had_tools_this_step = False
            return None
        if isinstance(event, ToolEnd):
            had_tools_this_step = True
            return None
        if isinstance(event, GenerationStep):
            if had_tools_this_step:
                steps_without_tools = 0
            else:
                steps_without_tools += 1
            had_tools_this_step = False
            if steps_without_tools >= for_steps:
                return Finish(reason=reason)
        return None

    hook = Hook(check, AgentEvent)
    hook.__name__ = reason
    return hook


def token_usage(
    limit: int,
    *,
    mode: t.Literal["total", "in", "out"] = "total",
    name: str | None = None,
) -> Hook:
    """
    Stop if the token usage exceeds a specified limit.

    Args:
        limit: The maximum number of tokens allowed.
        mode: Which token count to consider: "total", "in", or "out".
        name: Optional name for the hook.

    Returns:
        A Hook that returns Finish when token usage exceeds the limit.
    """
    reason = name or f"stop_on_token_usage({limit}, {mode})"

    async def check(event: GenerationEnd) -> Reaction | None:
        if not event.usage:
            return None
        token_count = (
            event.usage.total_tokens
            if mode == "total"
            else (event.usage.input_tokens if mode == "in" else event.usage.output_tokens)
        )
        if token_count > limit:
            return Finish(reason=reason)
        return None

    hook = Hook(check, GenerationEnd)
    hook.__name__ = reason
    return hook  # ty: ignore[invalid-return-type]  # Hook is covariant on event subtype


def elapsed_time(max_seconds: float, *, name: str | None = None) -> Hook:
    """
    Stop if the total execution time exceeds a given duration.

    Args:
        max_seconds: The maximum number of seconds the agent is allowed to run.
        name: Optional name for the hook.

    Returns:
        A Hook that returns Finish when elapsed time exceeds the limit.
    """
    reason = name or f"stop_on_elapsed_time({max_seconds}s)"
    start_time: datetime | None = None

    async def check(event: AgentEvent) -> Reaction | None:
        nonlocal start_time
        if isinstance(event, AgentStart):
            start_time = event.timestamp
            return None
        if isinstance(event, GenerationEnd) and start_time is not None:
            delta = event.timestamp - start_time
            if delta.total_seconds() > max_seconds:
                return Finish(reason=reason)
        return None

    hook = Hook(check, AgentEvent)
    hook.__name__ = reason
    return hook


def estimated_cost(limit: float, *, name: str | None = None) -> Hook:
    """
    Stop if the estimated cost of LLM generations exceeds a limit.

    Args:
        limit: The maximum cost allowed (USD).
        name: Optional name for the hook.

    Returns:
        A Hook that returns Finish when estimated cost exceeds the limit.
    """
    reason = name or f"stop_on_estimated_cost(${limit:.2f})"

    async def check(event: GenerationEnd) -> Reaction | None:
        cost = event.estimated_cost
        if cost is not None and cost > limit:
            return Finish(reason=reason)
        return None

    hook = Hook(check, GenerationEnd)
    hook.__name__ = reason
    return hook  # ty: ignore[invalid-return-type]  # Hook is covariant on event subtype


def consecutive_errors(count: int, *, name: str | None = None) -> Hook:
    """
    Stop if there are consecutive tool errors.

    Args:
        count: The number of consecutive errors before stopping.
        name: Optional name for the hook.

    Returns:
        A Hook that returns Finish after consecutive errors.
    """
    reason = name or f"stop_on_consecutive_errors({count})"
    consecutive = 0

    async def check(event: AgentEvent) -> Reaction | None:
        nonlocal consecutive
        if isinstance(event, AgentStart):
            consecutive = 0
            return None
        if isinstance(event, ToolError):
            consecutive += 1
            if consecutive >= count:
                return Finish(reason=reason)
        elif isinstance(event, ToolEnd):
            consecutive = 0
        return None

    hook = Hook(check, AgentEvent)
    hook.__name__ = reason
    return hook


def _match_pattern(
    text: str,
    pattern: str | re.Pattern[str],
    *,
    case_sensitive: bool,
    exact: bool,
    regex: bool,
) -> bool:
    """
    Helper to match text against a pattern with various options.

    Args:
        text: The text to search in.
        pattern: The pattern to search for.
        case_sensitive: Whether the match should be case-sensitive.
        exact: Whether to do an exact match.
        regex: Whether to treat the pattern as a regex.

    Returns:
        True if the pattern matches, False otherwise.
    """
    if isinstance(pattern, re.Pattern) or regex:
        compiled = pattern
        if isinstance(pattern, str):
            flags = 0 if case_sensitive else re.IGNORECASE
            compiled = re.compile(pattern, flags)

        if isinstance(compiled, re.Pattern):
            return bool(compiled.search(text))
        return False

    if exact:
        return text == pattern if case_sensitive else text.lower() == pattern.lower()

    # Default to substring containment
    search_text = text if case_sensitive else text.lower()
    search_pattern = pattern if case_sensitive else pattern.lower()
    return search_pattern in search_text
