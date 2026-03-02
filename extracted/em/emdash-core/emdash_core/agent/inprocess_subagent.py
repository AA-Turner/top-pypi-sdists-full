"""In-process sub-agent runner.

Runs sub-agents in the same process for better UX (real-time events)
while keeping isolated message histories.

Simple two-layer model:
- Main agent can spawn Explore, Plan, Coder sub-agents
- Sub-agents cannot spawn further (they don't have the task tool)
"""

import json
import time
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, Future

from .toolkits import get_toolkit
from .subagent_prompts import get_subagent_prompt
from .providers import get_provider
from .providers.factory import DEFAULT_MODEL
from .context_manager import (
    truncate_tool_output,
    reduce_context_for_retry,
    is_context_overflow_error,
)
from .runner.context import estimate_context_tokens
from ..utils.logger import log


@dataclass
class SubAgentResult:
    """Result from a sub-agent execution."""

    success: bool
    agent_type: str
    agent_id: str
    task: str
    summary: str
    files_explored: list[str]
    findings: list[dict]
    iterations: int
    tools_used: list[str]
    execution_time: float
    exploration_steps: list[dict] = None  # Detailed exploration steps
    files_modified: list[str] = None  # Files modified by Coder
    error: Optional[str] = None
    usage: dict[str, int] | None = None  # Token usage (input_tokens, output_tokens, thinking_tokens)

    def __post_init__(self):
        if self.exploration_steps is None:
            self.exploration_steps = []
        if self.files_modified is None:
            self.files_modified = []

    def to_dict(self) -> dict:
        return asdict(self)


class InProcessSubAgent:
    """Sub-agent that runs in the same process.

    Benefits over subprocess:
    - Real-time event streaming to parent emitter
    - No stdout/stderr parsing
    - Simpler debugging
    - Natural UI integration

    Each sub-agent has its own:
    - Message history (isolated)
    - Agent ID (for event tagging)
    - Toolkit instance
    """

    def __init__(
        self,
        subagent_type: str,
        repo_root: Path,
        emitter=None,
        model: Optional[str] = None,
        max_turns: int = 10,
        agent_id: Optional[str] = None,
        thoroughness: str = "medium",
    ):
        """Initialize in-process sub-agent.

        Args:
            subagent_type: Type of agent (Explore, Plan, Coder, etc.)
            repo_root: Repository root directory
            emitter: Parent emitter for events (optional)
            model: Model to use (defaults to fast model)
            max_turns: Maximum iterations
            agent_id: Optional agent ID (generated if not provided)
            thoroughness: Search thoroughness level (quick, medium, thorough)
        """
        self.subagent_type = subagent_type
        self.repo_root = repo_root.resolve()
        self.emitter = emitter
        self.max_turns = max_turns
        self.agent_id = agent_id or str(uuid.uuid4())[:8]
        self.thoroughness = thoroughness

        # Get toolkit for this agent type
        self.toolkit = get_toolkit(subagent_type, repo_root)

        # For Coder toolkit, set the emitter (though Coder can't spawn, it may need it for events)
        if subagent_type == "Coder" and hasattr(self.toolkit, "set_emitter"):
            self.toolkit.set_emitter(emitter)

        # Get model and create provider
        model_name = model or DEFAULT_MODEL
        self.provider = get_provider(model_name)

        # Get system prompt and inject thoroughness level
        base_prompt = get_subagent_prompt(subagent_type, repo_root=repo_root)
        self.system_prompt = self._inject_thoroughness(base_prompt)

        # Tracking
        self.files_explored: set[str] = set()
        self.tools_used: list[str] = []
        self.exploration_steps: list[dict] = []  # Detailed step tracking
        self.files_modified: list[str] = []  # For Coder - track modifications

        # Token usage tracking
        self._total_input_tokens: int = 0
        self._total_output_tokens: int = 0
        self._total_thinking_tokens: int = 0

    def _inject_thoroughness(self, prompt: str) -> str:
        """Inject thoroughness level into the system prompt."""
        thoroughness_guidance = {
            "quick": """
## Thoroughness Level: QUICK
- Do basic searches only - find the most obvious matches first
- Stop after finding 2-3 relevant files
- Don't explore deeply - just locate the key files
- Prioritize speed over completeness""",
            "medium": """
## Thoroughness Level: MEDIUM
- Do moderate exploration - check multiple locations
- Follow 1-2 levels of imports/references
- Balance speed with coverage
- Stop when you have reasonable confidence""",
            "thorough": """
## Thoroughness Level: THOROUGH
- Do comprehensive analysis across the codebase
- Check multiple naming conventions and locations
- Follow import chains and cross-references deeply
- Explore edge cases and alternative implementations
- Only stop when you've exhausted relevant areas""",
        }
        guidance = thoroughness_guidance.get(self.thoroughness, thoroughness_guidance["medium"])
        return prompt + "\n" + guidance

    def _emit(self, event_type: str, **data) -> None:
        """Emit event with agent tagging.

        Uses the generic emit() method to preserve subagent_id and subagent_type
        in the event data, allowing the UI to display sub-agent events differently.
        """
        if self.emitter and hasattr(self.emitter, "emit"):
            from .events import EventType

            # Tag event with agent info
            data["subagent_id"] = self.agent_id
            data["subagent_type"] = self.subagent_type

            # Map event types
            event_map = {
                "tool_start": EventType.TOOL_START,
                "tool_result": EventType.TOOL_RESULT,
                "thinking": EventType.THINKING,
                "error": EventType.ERROR,
                "progress": EventType.PROGRESS,
            }

            if event_type in event_map:
                self.emitter.emit(event_map[event_type], data)

    def _get_project_context(self) -> str:
        """Get PROJECT.md and directory structure for context."""
        context_parts = []

        # Try to read PROJECT.md
        project_md = self.repo_root / "PROJECT.md"
        if project_md.exists():
            try:
                content = project_md.read_text()
                # Truncate if too long
                if len(content) > 8000:
                    content = content[:8000] + "\n...[truncated]"
                context_parts.append(f"## PROJECT.md\n\n{content}")
            except Exception as e:
                log.debug(f"Could not read PROJECT.md: {e}")

        # Get directory structure (top 2 levels)
        try:
            structure_lines = ["## Project Structure\n"]
            for item in sorted(self.repo_root.iterdir()):
                if item.name.startswith(".") and item.name not in (".emdash",):
                    continue
                if item.name in ("node_modules", "__pycache__", ".git", "dist", "build", ".venv", "venv"):
                    continue
                if item.is_dir():
                    structure_lines.append(f"  {item.name}/")
                    # Show first level contents
                    try:
                        for subitem in sorted(item.iterdir())[:10]:
                            if not subitem.name.startswith("."):
                                suffix = "/" if subitem.is_dir() else ""
                                structure_lines.append(f"    {subitem.name}{suffix}")
                        if len(list(item.iterdir())) > 10:
                            structure_lines.append(f"    ...")
                    except PermissionError:
                        pass
                else:
                    structure_lines.append(f"  {item.name}")
            context_parts.append("\n".join(structure_lines))
        except Exception as e:
            log.debug(f"Could not get directory structure: {e}")

        return "\n\n".join(context_parts) if context_parts else ""

    def run(self, prompt: str) -> SubAgentResult:
        """Execute the task and return results.

        Args:
            prompt: The task to perform

        Returns:
            SubAgentResult with findings
        """
        start_time = time.time()
        messages = []
        iterations = 0
        last_content = ""
        error = None

        # For Plan agents, inject project context
        if self.subagent_type == "Plan":
            context = self._get_project_context()
            if context:
                prompt = f"""Here is context about the project:

{context}

---

Now, your task:
{prompt}"""

        # Add user message
        messages.append({"role": "user", "content": prompt})

        log.info(
            "SubAgent {} starting: type={} prompt={}",
            self.agent_id,
            self.subagent_type,
            prompt[:50] + "..." if len(prompt) > 50 else prompt,
        )

        try:
            # Agent loop
            while iterations < self.max_turns:
                iterations += 1

                log.debug(f"SubAgent {self.agent_id} turn {iterations}/{self.max_turns}")

                # Emit progress so TUI shows activity
                # Don't show max_turns limit - agent stops when it's done (no more tool calls)
                self._emit("progress", message=f"Turn {iterations}")

                # Check context size and compact if needed
                context_tokens = estimate_context_tokens(messages, self.system_prompt)
                context_limit = self.provider.get_context_limit()

                if context_tokens > context_limit * 0.8:
                    log.info(
                        f"SubAgent {self.agent_id} context at {context_tokens:,}/{context_limit:,} "
                        f"({context_tokens/context_limit:.0%}), reducing..."
                    )
                    messages = reduce_context_for_retry(messages, keep_recent=6)

                # Call LLM with retry on context overflow
                response = None
                max_retries = 2
                for retry in range(max_retries + 1):
                    try:
                        response = self.provider.chat(
                            messages=messages,
                            tools=self.toolkit.get_all_schemas(),
                            system=self.system_prompt,
                        )
                        break  # Success
                    except Exception as e:
                        if is_context_overflow_error(e) and retry < max_retries:
                            log.warning(
                                f"SubAgent {self.agent_id} context overflow on attempt {retry + 1}, reducing..."
                            )
                            messages = reduce_context_for_retry(messages, keep_recent=4 - retry)
                        else:
                            raise  # Re-raise if not overflow or out of retries

                if response is None:
                    raise RuntimeError("Failed to get response from LLM")

                # Accumulate token usage
                self._total_input_tokens += response.input_tokens
                self._total_output_tokens += response.output_tokens
                self._total_thinking_tokens += getattr(response, "thinking_tokens", 0)

                # Add assistant response
                assistant_msg = self.provider.format_assistant_message(response)
                if assistant_msg:
                    messages.append(assistant_msg)

                # Save content for final summary
                if response.content:
                    last_content = response.content

                # Only emit actual thinking content (extended thinking from Claude), not response content
                if hasattr(response, 'thinking') and response.thinking:
                    self._emit("thinking", content=response.thinking)

                # Check if done
                if not response.tool_calls:
                    # Check if response was truncated due to max_tokens
                    if response.stop_reason in ("max_tokens", "length"):
                        log.debug(f"SubAgent {self.agent_id} response truncated, requesting continuation")
                        if response.content:
                            messages.append({
                                "role": "assistant",
                                "content": response.content,
                            })
                        messages.append({
                            "role": "user",
                            "content": "Your response was cut off. Please continue.",
                        })
                        continue
                    break

                # Execute tool calls
                for tool_call in response.tool_calls:
                    self.tools_used.append(tool_call.name)

                    # Parse arguments
                    try:
                        args = json.loads(tool_call.arguments) if tool_call.arguments else {}
                    except (json.JSONDecodeError, TypeError):
                        args = {}

                    # Emit tool start
                    self._emit("tool_start", name=tool_call.name, args=args)

                    # Track files
                    if "path" in args:
                        self.files_explored.add(args["path"])
                    if "file_path" in args:
                        self.files_explored.add(args["file_path"])

                    # Execute tool
                    result = self.toolkit.execute(tool_call.name, **args)

                    # Track file modifications for Coder
                    if tool_call.name in ("write_to_file", "edit_file", "apply_diff") and result.success:
                        modified_path = args.get("path") or args.get("file_path")
                        if modified_path and modified_path not in self.files_modified:
                            self.files_modified.append(modified_path)

                    # Emit tool result
                    summary = str(result.data)[:100] if result.data else ""
                    self._emit(
                        "tool_result",
                        name=tool_call.name,
                        success=result.success,
                        summary=summary,
                    )

                    # Track exploration step with details
                    step = {
                        "tool": tool_call.name,
                        "params": self._sanitize_params(args),
                        "success": result.success,
                        "summary": self._extract_result_summary(tool_call.name, args, result),
                    }
                    self.exploration_steps.append(step)

                    # Add tool result to messages (truncated to avoid context overflow)
                    tool_output = json.dumps(result.to_dict(), indent=2)
                    tool_output = truncate_tool_output(tool_output, max_tokens=15000)
                    tool_result_msg = self.provider.format_tool_result(
                        tool_call.id,
                        tool_output,
                    )
                    if tool_result_msg:
                        messages.append(tool_result_msg)

        except Exception as e:
            log.exception(f"SubAgent {self.agent_id} failed")
            error = str(e)
            # Emit error event so TUI can show it immediately
            self._emit("error", message=f"Sub-agent error: {error}")

        execution_time = time.time() - start_time

        log.info(
            "SubAgent {} completed: {} turns, {} files, {:.1f}s",
            self.agent_id,
            iterations,
            len(self.files_explored),
            execution_time,
        )

        return SubAgentResult(
            success=error is None,
            agent_type=self.subagent_type,
            agent_id=self.agent_id,
            task=prompt,
            summary=last_content or "No response generated",
            files_explored=list(self.files_explored),
            findings=self._extract_findings(messages),
            iterations=iterations,
            tools_used=list(set(self.tools_used)),
            execution_time=execution_time,
            exploration_steps=self.exploration_steps[-30:],  # Last 30 steps
            files_modified=self.files_modified,
            error=error,
            usage={
                "input_tokens": self._total_input_tokens,
                "output_tokens": self._total_output_tokens,
                "thinking_tokens": self._total_thinking_tokens,
            },
        )

    def _extract_findings(self, messages: list[dict]) -> list[dict]:
        """Extract key findings from tool results."""
        findings = []
        for msg in messages:
            if msg and msg.get("role") == "tool":
                try:
                    content = json.loads(msg.get("content", "{}"))
                    if content and content.get("success") and content.get("data"):
                        findings.append(content["data"])
                except (json.JSONDecodeError, TypeError):
                    pass
        return findings[-10:]

    def _sanitize_params(self, args: dict) -> dict:
        """Sanitize params for logging - truncate long values."""
        sanitized = {}
        for key, value in args.items():
            if isinstance(value, str) and len(value) > 200:
                sanitized[key] = value[:200] + "..."
            else:
                sanitized[key] = value
        return sanitized

    def _extract_result_summary(self, tool_name: str, args: dict, result) -> str:
        """Extract a meaningful summary from tool result based on tool type."""
        if not result.success:
            return f"Failed: {result.error or 'unknown error'}"

        data = result.data or {}

        # Tool-specific summaries
        if tool_name == "read_file":
            path = args.get("path", args.get("file_path", ""))
            lines = data.get("line_count", data.get("lines", "?"))
            return f"Read {path} ({lines} lines)"

        elif tool_name == "glob":
            matches = data.get("matches", data.get("files", []))
            pattern = args.get("pattern", "")
            return f"Found {len(matches)} files matching '{pattern}'"

        elif tool_name == "grep":
            matches = data.get("matches", [])
            pattern = args.get("pattern", "")
            return f"Found {len(matches)} matches for '{pattern}'"

        elif tool_name == "semantic_search":
            results = data.get("results", [])
            query = args.get("query", "")[:50]
            return f"Found {len(results)} results for '{query}'"

        elif tool_name == "list_files":
            files = data.get("files", data.get("entries", []))
            path = args.get("path", "")
            return f"Listed {len(files)} items in {path}"

        else:
            # Generic summary
            if isinstance(data, dict):
                keys = list(data.keys())[:3]
                return f"Returned: {', '.join(keys)}" if keys else "Success"
            return str(data)[:100] if data else "Success"


# Thread pool for parallel execution
_executor: Optional[ThreadPoolExecutor] = None


def _get_executor() -> ThreadPoolExecutor:
    """Get or create thread pool executor.

    4 workers allows up to 4 sub-agents to run in parallel.
    """
    global _executor
    if _executor is None:
        _executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="subagent")
    return _executor


def run_subagent(
    subagent_type: str,
    prompt: str,
    repo_root: Path,
    emitter=None,
    model: Optional[str] = None,
    max_turns: int = 10,
    thoroughness: str = "medium",
) -> SubAgentResult:
    """Run a sub-agent synchronously.

    Args:
        subagent_type: Type of agent (Explore, Plan, Coder)
        prompt: Task to perform
        repo_root: Repository root
        emitter: Event emitter
        model: Model to use
        max_turns: Max iterations
        thoroughness: Search thoroughness level (quick, medium, thorough)

    Returns:
        SubAgentResult
    """
    try:
        agent = InProcessSubAgent(
            subagent_type=subagent_type,
            repo_root=repo_root,
            emitter=emitter,
            model=model,
            max_turns=max_turns,
            thoroughness=thoroughness,
        )
        return agent.run(prompt)
    except Exception as e:
        # Return a proper error result instead of letting the exception propagate
        # This prevents 0.0s "silent" failures and gives clear error messages
        log.error(f"Failed to create sub-agent: {e}")
        return SubAgentResult(
            success=False,
            agent_type=subagent_type,
            agent_id="init-failed",
            task=prompt,
            summary="",
            files_explored=[],
            findings=[],
            iterations=0,
            tools_used=[],
            execution_time=0.0,
            error=f"Sub-agent initialization failed: {e}",
        )


def run_subagent_async(
    subagent_type: str,
    prompt: str,
    repo_root: Path,
    emitter=None,
    model: Optional[str] = None,
    max_turns: int = 10,
    thoroughness: str = "medium",
) -> Future[SubAgentResult]:
    """Run a sub-agent asynchronously (returns Future).

    Args:
        subagent_type: Type of agent (Explore, Plan, Coder)
        prompt: Task to perform
        repo_root: Repository root
        emitter: Event emitter
        model: Model to use
        max_turns: Max iterations
        thoroughness: Search thoroughness level (quick, medium, thorough)

    Returns:
        Future[SubAgentResult] - call .result() to get result
    """
    executor = _get_executor()
    return executor.submit(
        run_subagent,
        subagent_type=subagent_type,
        prompt=prompt,
        repo_root=repo_root,
        emitter=emitter,
        model=model,
        max_turns=max_turns,
        thoroughness=thoroughness,
    )


def run_subagents_parallel(
    tasks: list[dict],
    repo_root: Path,
    emitter=None,
) -> list[SubAgentResult]:
    """Run multiple sub-agents in parallel.

    Args:
        tasks: List of task dicts with keys:
            - subagent_type: str
            - prompt: str
            - model: str (optional)
            - max_turns: int (optional)
            - thoroughness: str (optional, default "medium")
        repo_root: Repository root
        emitter: Shared event emitter

    Returns:
        List of SubAgentResults in same order as tasks
    """
    futures = []
    for task in tasks:
        future = run_subagent_async(
            subagent_type=task.get("subagent_type", "Explore"),
            prompt=task["prompt"],
            repo_root=repo_root,
            emitter=emitter,
            model=task.get("model"),
            max_turns=task.get("max_turns", 10),
            thoroughness=task.get("thoroughness", "medium"),
        )
        futures.append(future)

    # Wait for all to complete and gather results
    results = []
    for future in futures:
        try:
            results.append(future.result())
        except Exception as e:
            log.exception("Sub-agent failed")
            results.append(SubAgentResult(
                success=False,
                agent_type="unknown",
                agent_id="error",
                task="",
                summary="",
                files_explored=[],
                findings=[],
                iterations=0,
                tools_used=[],
                execution_time=0,
                error=str(e),
            ))

    return results
