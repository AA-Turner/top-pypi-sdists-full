"""SubAgentRunner - subprocess agent runner for focused tasks.

This module provides the SubAgentRunner class for executing sub-agents in
separate processes, plus a CLI entry point for subprocess execution.

Usage:
    # From parent process via Task tool
    result = subprocess.run([
        sys.executable, "-m", "emdash_core.agent.subagent",
        "--type", "Explore",
        "--prompt", "Find authentication handlers",
        "--repo-root", "/path/to/repo",
    ])

    # Result is JSON on stdout
"""

import argparse
import json
import os
import sys
import time
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

from .toolkits import get_toolkit
from .prompts import get_subagent_prompt
from .providers import get_provider
from ..utils.logger import log


# Environment variables for model configuration
MODEL_ENV_VARS = {
    "fast": "FAST_MODEL",
}


def get_model_for_tier(tier: str = "fast") -> str:
    """Get model name from environment variable or registry default.

    Args:
        tier: Model tier (fast, model)

    Returns:
        Model name/path
    """
    from .providers.models import ModelRegistry

    if tier == "fast":
        env_value = os.environ.get(MODEL_ENV_VARS["fast"])
        if env_value:
            return env_value
    # Fall back to registry config
    registry = ModelRegistry.get()
    if tier == "fast" and registry.fast_model:
        return registry.fast_model
    return registry.default_model


@dataclass
class SubAgentResult:
    """Result from a sub-agent execution."""

    success: bool
    agent_type: str
    agent_id: str
    task: str

    # Findings
    summary: str
    files_explored: list[str]
    findings: list[dict]

    # Metadata
    iterations: int
    tools_used: list[str]
    execution_time: float
    error: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class SubAgentRunner:
    """Subprocess agent runner for focused tasks.

    Runs a lightweight agent loop with a type-specific toolkit.
    Designed to be spawned as a subprocess from the parent agent.
    """

    def __init__(
        self,
        subagent_type: str,
        repo_root: Path,
        model_tier: str = "fast",
        max_turns: int = 10,
        agent_id: Optional[str] = None,
    ):
        """Initialize the sub-agent runner.

        Args:
            subagent_type: Type of agent (Explore, Plan, etc.)
            repo_root: Root directory of the repository
            model_tier: Model tier (fast, standard, powerful)
            max_turns: Maximum API round-trips before stopping
            agent_id: Optional agent ID for resume support
        """
        self.subagent_type = subagent_type
        self.repo_root = repo_root.resolve()
        self.max_turns = max_turns
        self.agent_id = agent_id or str(uuid.uuid4())[:8]

        # Get toolkit for this agent type
        self.toolkit = get_toolkit(subagent_type, repo_root)

        # Get model and create provider
        model_name = get_model_for_tier(model_tier)
        self.provider = get_provider(model_name)

        # Get system prompt
        self.system_prompt = get_subagent_prompt(subagent_type)

        # Transcript for resume support
        self.transcript_dir = repo_root / ".emdash" / "agents"
        self.transcript_path = self.transcript_dir / f"{self.agent_id}.jsonl"

        # Tracking
        self.files_explored: set[str] = set()
        self.tools_used: list[str] = []

    def _emit_progress(self, event_type: str, data: dict) -> None:
        """Emit progress event to stderr for parent process to capture.

        Events are JSON lines with format: {"event": "type", "data": {...}}
        """
        import sys
        event = {"event": event_type, "data": data}
        print(json.dumps(event), file=sys.stderr, flush=True)

    def run(self, prompt: str) -> SubAgentResult:
        """Execute the task and return results.

        Args:
            prompt: The task to perform

        Returns:
            SubAgentResult with findings
        """
        start_time = time.time()

        # Load existing transcript if resuming
        messages = self._load_transcript()

        # Add user message with prompt
        if not messages or messages[-1].get("role") != "user":
            messages.append({"role": "user", "content": prompt})

        iterations = 0
        last_content = ""
        error = None

        try:
            # Emit start event
            self._emit_progress("agent_start", {
                "agent_type": self.subagent_type,
                "agent_id": self.agent_id,
                "max_turns": self.max_turns,
            })

            # Agent loop
            while iterations < self.max_turns:
                iterations += 1

                self._emit_progress("turn_start", {
                    "turn": iterations,
                    "max_turns": self.max_turns,
                })

                # Call LLM
                response = self.provider.chat(
                    messages=messages,
                    tools=self.toolkit.get_all_schemas(),
                    system=self.system_prompt,
                )

                # Add assistant response to messages
                assistant_msg = self.provider.format_assistant_message(response)
                if assistant_msg:
                    messages.append(assistant_msg)

                # Save content
                if response.content:
                    last_content = response.content

                # Check if done (no tool calls)
                if not response.tool_calls:
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
                    self._emit_progress("tool_start", {
                        "name": tool_call.name,
                        "args": {k: str(v)[:100] for k, v in args.items()},  # Truncate args
                    })

                    # Track file operations
                    if "path" in args:
                        self.files_explored.add(args["path"])

                    # Execute tool
                    result = self.toolkit.execute(tool_call.name, **args)

                    # Emit tool result
                    self._emit_progress("tool_result", {
                        "name": tool_call.name,
                        "success": result.success,
                        "summary": str(result.data)[:200] if result.data else None,
                    })

                    # Add tool result to messages
                    tool_result_msg = self.provider.format_tool_result(
                        tool_call.id,
                        json.dumps(result.to_dict(), indent=2),
                    )
                    if tool_result_msg:
                        messages.append(tool_result_msg)

                # Save transcript after each iteration
                self._save_transcript(messages)

        except Exception as e:
            log.exception("Sub-agent execution failed")
            error = str(e)
            self._emit_progress("agent_error", {"error": str(e)})

        execution_time = time.time() - start_time

        # Emit completion event
        self._emit_progress("agent_end", {
            "success": error is None,
            "iterations": iterations,
            "files_explored": len(self.files_explored),
            "tools_used": len(set(self.tools_used)),
            "execution_time": execution_time,
        })

        # Build result
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
            error=error,
        )

    def _load_transcript(self) -> list[dict]:
        """Load transcript from file for resume support."""
        if not self.transcript_path.exists():
            return []

        messages = []
        try:
            with open(self.transcript_path) as f:
                for line in f:
                    if line.strip():
                        messages.append(json.loads(line))
            log.info(f"Resumed agent {self.agent_id} with {len(messages)} messages")
        except Exception as e:
            log.warning(f"Failed to load transcript: {e}")
            return []

        return messages

    def _save_transcript(self, messages: list[dict]) -> None:
        """Save transcript to file for resume support."""
        try:
            self.transcript_dir.mkdir(parents=True, exist_ok=True)
            with open(self.transcript_path, "w") as f:
                for msg in messages:
                    f.write(json.dumps(msg) + "\n")
        except Exception as e:
            log.warning(f"Failed to save transcript: {e}")

    def _extract_findings(self, messages: list[dict]) -> list[dict]:
        """Extract key findings from tool results.

        Args:
            messages: Conversation messages

        Returns:
            List of finding dicts
        """
        findings = []
        for msg in messages:
            if msg and msg.get("role") == "tool":
                try:
                    content = json.loads(msg.get("content", "{}"))
                    if content and content.get("success") and content.get("data"):
                        findings.append(content["data"])
                except (json.JSONDecodeError, TypeError):
                    pass
        return findings[-10:]  # Limit to last 10 findings


def main():
    """CLI entry point for subprocess execution."""
    parser = argparse.ArgumentParser(
        description="Run a sub-agent task",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=["Explore", "Plan", "Bash", "Research"],
        help="Type of sub-agent",
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Task prompt",
    )
    parser.add_argument(
        "--repo-root",
        required=True,
        type=Path,
        help="Repository root directory",
    )
    parser.add_argument(
        "--model-tier",
        default="fast",
        choices=["fast", "model"],
        help="Model tier to use (fast=cheap/quick, model=standard)",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=10,
        help="Maximum API round-trips",
    )
    parser.add_argument(
        "--agent-id",
        help="Agent ID (for resume)",
    )

    args = parser.parse_args()

    try:
        runner = SubAgentRunner(
            subagent_type=args.type,
            repo_root=args.repo_root,
            model_tier=args.model_tier,
            max_turns=args.max_turns,
            agent_id=args.agent_id,
        )

        result = runner.run(args.prompt)

        # Output result as JSON to stdout
        print(result.to_json())
        sys.exit(0 if result.success else 1)

    except Exception as e:
        # Output error as JSON
        error_result = {
            "success": False,
            "error": str(e),
            "agent_type": args.type,
            "task": args.prompt,
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
