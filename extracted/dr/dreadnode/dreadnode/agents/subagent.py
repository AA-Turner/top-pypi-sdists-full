"""
Sub-agent spawning tools for complex task delegation.

Similar to Claude Code's Task tool, this allows spawning specialized agents
to handle specific subtasks autonomously.
"""

import typing as t
from textwrap import dedent

from loguru import logger

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

    run_in_background: bool = Config(default=False)
    """Whether to run sub-agents in background (not yet implemented)."""

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
        - Parallel work (with run_in_background)

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
            trajectory = await sub_agent.run(task)
            # Get the last assistant message content as the response
            last_message = trajectory.messages[-1] if trajectory.messages else None
            response = str(last_message.content) if last_message else ""

            result = f"## Sub-agent: {config['name']}\n\n"
            result += f"**Task:** {task}\n\n"
            result += f"**Steps taken:** {len(trajectory.steps)}\n"
            result += f"**Tokens used:** {trajectory.usage.total_tokens}\n\n"
            result += f"**Result:**\n{response}"

            logger.info(f"Sub-agent completed in {len(trajectory.steps)} steps")
        except Exception as e:
            logger.error(f"Sub-agent failed: {e}")
            return f"Sub-agent failed: {e}"
        else:
            # Stash the sub-agent's LLM cost on the tool result metadata so
            # the agent framework can lift it onto the ``ToolEnd`` event and
            # the TUI can display it in the parent session's footer.
            msg = Message(role="tool", content=result)
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
