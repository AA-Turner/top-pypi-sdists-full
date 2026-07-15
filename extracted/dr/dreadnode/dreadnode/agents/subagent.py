"""
Sub-agent spawning tools for complex task delegation.

Similar to Claude Code's Task tool, this allows spawning specialized agents
to handle specific subtasks autonomously.
"""

import asyncio
import typing as t
from textwrap import dedent

from loguru import logger

from dreadnode.agents.events import AgentEnd
from dreadnode.agents.tools import Toolset, tool_method
from dreadnode.core.meta import Config
from dreadnode.generators.message import Message

if t.TYPE_CHECKING:
    from dreadnode.core.agents import Agent


# Pre-defined agent configurations
AGENT_CONFIGS: dict[str, dict[str, t.Any]] = {
    "explore": {
        "name": "explorer",
        "instructions": dedent("""
            You are a codebase exploration agent. Your job is to:
            - Find files matching patterns
            - Search for code, functions, classes
            - Understand codebase structure
            - Report findings concisely

            Be thorough but efficient. Return a clear summary of what you found.
        """),
        "max_steps": 20,
    },
    "plan": {
        "name": "planner",
        "instructions": dedent("""
            You are a planning agent. Your job is to:
            - Analyze the task requirements
            - Explore relevant code to understand context
            - Design an implementation approach
            - Return a step-by-step plan

            Do NOT implement - just plan. Be specific about files and changes.
        """),
        "max_steps": 15,
    },
    "test": {
        "name": "tester",
        "instructions": dedent("""
            You are a testing agent. Your job is to:
            - Run existing tests
            - Analyze test failures
            - Suggest fixes for failing tests
            - Verify code changes work correctly

            Focus on test execution and verification.
        """),
        "max_steps": 25,
    },
    "review": {
        "name": "reviewer",
        "instructions": dedent("""
            You are a code review agent. Your job is to:
            - Read the specified code
            - Check for bugs, security issues, and improvements
            - Verify code style and best practices
            - Provide actionable feedback

            Be constructive and specific in your review.
        """),
        "max_steps": 15,
    },
    "general": {
        "name": "assistant",
        "instructions": dedent("""
            You are a general-purpose assistant agent.
            Complete the given task efficiently and report results.
        """),
        "max_steps": 30,
    },
}


class SubAgentToolset(Toolset):
    """
    Toolset for spawning and managing sub-agents.

    Requires a parent agent to clone from.
    """

    parent_agent: t.Any = Config(default=None)
    """The parent agent to clone sub-agents from."""

    timeout: float | None = Config(default=3600.0)
    """Maximum seconds a spawned sub-agent may run before it is cancelled and
    reported as a timeout. ``None`` disables the ceiling (unbounded). A wedged
    tool inside a sub-agent (hung MCP transport, stuck LLM stream) would
    otherwise hang the parent session indefinitely."""

    @tool_method
    async def spawn_agent(
        self,
        task: t.Annotated[str, "The task for the sub-agent to complete"],
        agent_type: t.Annotated[
            str,
            "Agent type: 'explore' (find code), 'plan' (design approach), "
            "'test' (run tests), 'review' (code review), 'general' (any task)",
        ] = "general",
        *,
        custom_instructions: t.Annotated[
            str | None, "Optional custom instructions to override defaults"
        ] = None,
    ) -> str | Message:
        """
        Spawn a sub-agent to handle a specific task autonomously.

        Use this to delegate complex subtasks to specialized agents:
        - 'explore': Search and understand code
        - 'plan': Design implementation approach
        - 'test': Run and verify tests
        - 'review': Review code for issues
        - 'general': Any other task

        The sub-agent runs to completion and returns its findings.

        ## When to Use
        - Complex tasks requiring focused work
        - Exploration that might take many steps
        - Tasks where you want isolated context

        ## Examples

        Explore codebase:
        ```
        spawn_agent("Find all API endpoint definitions", agent_type="explore")
        ```

        Plan implementation:
        ```
        spawn_agent("Plan how to add user authentication", agent_type="plan")
        ```

        Args:
            task: What the sub-agent should accomplish.
            agent_type: Type of agent to spawn.
            custom_instructions: Override default instructions.

        Returns:
            The sub-agent's final response and summary.
        """

        if self.parent_agent is None:
            raise ValueError("SubAgentToolset requires parent_agent to be set")

        # Get config for agent type
        config = AGENT_CONFIGS.get(agent_type, AGENT_CONFIGS["general"]).copy()

        if custom_instructions:
            config["instructions"] = custom_instructions

        logger.info(f"Spawning {agent_type} sub-agent: {task[:50]}...")

        sub_agent: Agent = self.parent_agent.with_(
            name=config["name"],
            instructions=config["instructions"],
            max_steps=config["max_steps"],
        )
        # Give sub-agent its own tools list (model_copy shares references)
        # and filter out SubAgentToolset to prevent recursive spawning
        sub_agent.tools = [
            tool for tool in sub_agent.tools if not isinstance(tool, SubAgentToolset)
        ]
        sub_agent.reset()

        try:
            # Bound the sub-agent run so a wedged tool inside it can't hang the
            # parent session forever. ``asyncio.timeout(None)`` is a no-op, so a
            # single path covers both the bounded and unbounded cases. On expiry
            # it cancels the inner run and raises ``TimeoutError`` here; the
            # ``CancelledError`` it uses internally never escapes. We check
            # ``cm.expired()`` to tell our ceiling breach apart from a builtin
            # ``TimeoutError`` raised *inside* the sub-agent, and deliberately do
            # NOT catch ``CancelledError`` (a genuine parent-step cancellation
            # must propagate, not be swallowed into a tool result).
            async with asyncio.timeout(self.timeout) as cm:
                trajectory = await sub_agent.run(task)
        except TimeoutError as e:
            if not cm.expired():
                # A builtin ``TimeoutError`` from within the sub-agent (socket,
                # inner ``async_timeout``, …) — not our ceiling. Surface it as an
                # ordinary failure rather than a false "cancelled at ceiling".
                logger.error(f"Sub-agent failed: {e}")
                return f"Sub-agent failed: {e}"
            logger.warning("Sub-agent '{}' timed out after {}s", config["name"], self.timeout)
            # The cancelled run still burned tokens; carry its partial cost so
            # the parent session's accounting isn't understated.
            return self._tool_result(
                f"Sub-agent '{config['name']}' timed out after {self.timeout} seconds "
                "and was cancelled. Consider narrowing the task or raising the "
                "SubAgentToolset timeout.",
                sub_agent.trajectory,
            )
        except Exception as e:
            logger.error(f"Sub-agent failed: {e}")
            return f"Sub-agent failed: {e}"
        else:
            terminal_event = next(
                (event for event in reversed(trajectory.events) if isinstance(event, AgentEnd)),
                None,
            )
            if terminal_event is not None and terminal_event.error:
                error_text = str(terminal_event.error)
                logger.error(
                    "Sub-agent ended with error | type={} | message={}",
                    type(terminal_event.error).__name__
                    if isinstance(terminal_event.error, BaseException)
                    else "error",
                    error_text,
                )
                return f"Sub-agent failed: {error_text}"

            # Get the last assistant message content as the response
            last_message = trajectory.messages[-1] if trajectory.messages else None
            response = str(last_message.content) if last_message else ""

            result = f"## Sub-agent: {config['name']}\n\n"
            result += f"**Task:** {task}\n\n"
            result += f"**Steps taken:** {len(trajectory.steps)}\n"
            result += f"**Tokens used:** {trajectory.usage.total_tokens}\n\n"
            result += f"**Result:**\n{response}"

            logger.info(f"Sub-agent completed in {len(trajectory.steps)} steps")
            return self._tool_result(result, trajectory)

    @staticmethod
    def _tool_result(content: str, trajectory: t.Any) -> Message:
        """Build the tool-result message, stashing the sub-agent's LLM cost on
        its metadata so the agent framework can lift it onto the ``ToolEnd``
        event and the TUI can display it in the parent session's footer."""
        msg = Message(role="tool", content=content)
        if trajectory.usage.cost_usd is not None:
            msg.metadata["subagent_cost_usd"] = trajectory.usage.cost_usd
        return msg


def create_subagent_tool(parent_agent: "Agent") -> SubAgentToolset:
    """
    Create a SubAgentToolset bound to a parent agent.

    Usage:
        agent = Agent(...)
        subagent_tools = create_subagent_tool(agent)
        agent.tools.append(subagent_tools)
    """
    return SubAgentToolset(parent_agent=parent_agent)
