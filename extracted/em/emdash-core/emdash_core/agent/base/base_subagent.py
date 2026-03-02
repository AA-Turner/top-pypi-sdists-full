"""Abstract base class for sub-agents.

Sub-agents are specialized agents that handle focused tasks like
exploration, planning, research, etc. They inherit from BaseSubAgent
and define their own toolkit and system prompt.
"""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, TYPE_CHECKING

from ...utils.logger import log
from ..events import AgentEventEmitter, NullEmitter
from ..providers import get_provider
from ..providers.factory import DEFAULT_MODEL
from ..tools.base import ToolResult

if TYPE_CHECKING:
    from ..toolkits.base import BaseToolkit


@dataclass
class SubAgentResult:
    """Result from a sub-agent execution."""

    success: bool
    content: str
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "success": self.success,
            "content": self.content,
            "error": self.error,
            "metadata": self.metadata,
        }


class BaseSubAgent(ABC):
    """Abstract base class for sub-agents.

    Sub-agents are specialized agents for focused tasks. They run with
    restricted toolkits and specific system prompts.

    Subclasses must implement:
    - _get_toolkit(): Return the toolkit for this sub-agent type
    - _build_system_prompt(): Build the system prompt

    Example:
        class CodingExplorer(BaseSubAgent):
            def _get_toolkit(self) -> ExploreToolkit:
                return ExploreToolkit(repo_root=self.repo_root)

            def _build_system_prompt(self) -> str:
                return EXPLORE_PROMPT
    """

    # Class-level configuration
    DEFAULT_MAX_TURNS = 10

    def __init__(
        self,
        repo_root: Optional[Path] = None,
        emitter: Optional[AgentEventEmitter] = None,
        model: Optional[str] = None,
        max_turns: Optional[int] = None,
        thoroughness: str = "medium",
        subagent_id: Optional[str] = None,
    ):
        """Initialize the sub-agent.

        Args:
            repo_root: Repository root path
            emitter: Event emitter for streaming
            model: LLM model to use (defaults to DEFAULT_MODEL)
            max_turns: Maximum number of turns (API calls)
            thoroughness: How thorough to be ("quick", "medium", "thorough")
            subagent_id: Unique ID for this sub-agent instance
        """
        self.repo_root = repo_root or Path.cwd()
        self.emitter = emitter or NullEmitter()
        self.model = model or DEFAULT_MODEL
        self.max_turns = max_turns or self.DEFAULT_MAX_TURNS
        self.thoroughness = thoroughness
        self.subagent_id = subagent_id

        # Initialize provider
        self.provider = get_provider(self.model)

        # Get toolkit from subclass
        self.toolkit = self._get_toolkit()

        # Build system prompt from subclass
        self.system_prompt = self._build_system_prompt()

        # Inject thoroughness guidance into prompt
        if self.thoroughness:
            self.system_prompt = self._inject_thoroughness(self.system_prompt)

        # Message history for this sub-agent
        self._messages: list[dict] = []

        # Token tracking
        self._total_input_tokens: int = 0
        self._total_output_tokens: int = 0

    # -------------------------------------------------------------------------
    # Abstract methods
    # -------------------------------------------------------------------------

    @abstractmethod
    def _get_toolkit(self) -> "BaseToolkit":
        """Return the toolkit for this sub-agent type.

        Returns:
            BaseToolkit instance with appropriate tools
        """
        pass

    @abstractmethod
    def _build_system_prompt(self) -> str:
        """Build the system prompt for this sub-agent.

        Returns:
            System prompt string
        """
        pass

    # -------------------------------------------------------------------------
    # Optional hooks
    # -------------------------------------------------------------------------

    def _on_start(self, prompt: str) -> None:
        """Hook called when sub-agent starts execution.

        Args:
            prompt: The task prompt
        """
        pass

    def _on_complete(self, result: SubAgentResult) -> None:
        """Hook called when sub-agent completes.

        Args:
            result: The execution result
        """
        pass

    # -------------------------------------------------------------------------
    # Thoroughness injection
    # -------------------------------------------------------------------------

    def _inject_thoroughness(self, prompt: str) -> str:
        """Inject thoroughness guidance into the prompt."""
        guidance = {
            "quick": """
## Thoroughness: QUICK
- Do minimal exploration
- Stop after finding first reasonable answer
- Prioritize speed over completeness
- Maximum 3-5 tool calls
""",
            "medium": """
## Thoroughness: MEDIUM
- Balance speed and completeness
- Explore 2-3 alternatives before deciding
- Verify findings with one additional check
- Maximum 10-15 tool calls
""",
            "thorough": """
## Thoroughness: THOROUGH
- Be comprehensive and detailed
- Explore all relevant alternatives
- Cross-reference findings
- Verify with multiple sources
- Maximum 25-30 tool calls
""",
        }

        if self.thoroughness in guidance:
            return prompt + "\n" + guidance[self.thoroughness]
        return prompt

    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------

    def run(self, prompt: str) -> SubAgentResult:
        """Execute the sub-agent task.

        Args:
            prompt: The task to perform

        Returns:
            SubAgentResult with the outcome
        """
        self._on_start(prompt)

        # Emit start event
        self.emitter.emit_subagent_start(
            subagent_type=self.__class__.__name__,
            prompt=prompt[:200],
            subagent_id=self.subagent_id,
        )

        # Initialize messages
        self._messages = [{"role": "user", "content": prompt}]

        # Get tool schemas
        tools = self.toolkit.get_all_schemas()

        try:
            result = self._run_loop(tools)
            self._on_complete(result)

            # Emit end event
            self.emitter.emit_subagent_end(
                subagent_type=self.__class__.__name__,
                success=result.success,
                summary=result.content[:200] if result.content else "",
                subagent_id=self.subagent_id,
            )

            return result

        except Exception as e:
            log.exception(f"Sub-agent {self.__class__.__name__} failed")
            error_result = SubAgentResult(
                success=False,
                content="",
                error=str(e),
            )
            self._on_complete(error_result)

            self.emitter.emit_subagent_end(
                subagent_type=self.__class__.__name__,
                success=False,
                summary=f"Error: {e}",
                subagent_id=self.subagent_id,
            )

            return error_result

    def _run_loop(self, tools: list[dict]) -> SubAgentResult:
        """Run the sub-agent loop until completion.

        Args:
            tools: Tool schemas

        Returns:
            SubAgentResult with the outcome
        """
        for turn in range(self.max_turns):
            log.debug(
                "Sub-agent {} turn {}/{}",
                self.__class__.__name__, turn + 1, self.max_turns
            )

            # Call LLM
            response = self.provider.chat(
                messages=self._messages,
                system=self.system_prompt,
                tools=tools,
                thinking=False,  # Sub-agents don't use extended thinking
            )

            # Track tokens
            self._total_input_tokens += response.input_tokens
            self._total_output_tokens += response.output_tokens

            # Handle tool calls
            if response.tool_calls:
                # Add assistant message with tool calls
                tool_calls_data = []
                for tc in response.tool_calls:
                    args = tc.arguments
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = {}
                    tool_calls_data.append({
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": json.dumps(args) if isinstance(args, dict) else args,
                        },
                    })

                self._messages.append({
                    "role": "assistant",
                    "content": response.content or "",
                    "tool_calls": tool_calls_data,
                })

                # Execute tools and add results
                for tc in response.tool_calls:
                    args = tc.arguments
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = {}

                    try:
                        result = self.toolkit.execute(tc.name, **args)
                        result_content = json.dumps(result.to_dict())
                    except Exception as e:
                        log.warning(f"Tool {tc.name} failed: {e}")
                        result_content = json.dumps({
                            "success": False,
                            "error": str(e),
                        })

                    self._messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result_content,
                    })

            else:
                # No tool calls - sub-agent is done
                if response.content:
                    return SubAgentResult(
                        success=True,
                        content=response.content,
                        metadata={
                            "turns": turn + 1,
                            "input_tokens": self._total_input_tokens,
                            "output_tokens": self._total_output_tokens,
                        },
                    )
                else:
                    return SubAgentResult(
                        success=False,
                        content="",
                        error="Sub-agent returned empty response",
                    )

        # Max turns reached
        return SubAgentResult(
            success=False,
            content="",
            error=f"Max turns ({self.max_turns}) reached without completion",
            metadata={
                "turns": self.max_turns,
                "input_tokens": self._total_input_tokens,
                "output_tokens": self._total_output_tokens,
            },
        )

    def get_token_usage(self) -> dict:
        """Get token usage statistics."""
        return {
            "input": self._total_input_tokens,
            "output": self._total_output_tokens,
            "total": self._total_input_tokens + self._total_output_tokens,
        }
