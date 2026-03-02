"""Agent session state management."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class ExplorationStep:
    """Record of a single exploration step."""

    tool: str
    params: dict
    result_summary: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    entities_found: list[str] = field(default_factory=list)
    content_preview: Optional[str] = None  # For read_file, grep - first few lines of content
    token_count: int = 0  # Estimated token count for this step's content


class AgentSession:
    """Manages exploration session state.

    Tracks the history of tool calls and their results to provide
    context for subsequent explorations.

    Example:
        session = AgentSession()

        # Record an action
        result = toolkit.execute("semantic_search", query="auth")
        session.record_action("semantic_search", {"query": "auth"}, result)

        # Get context for next action
        context = session.get_context_summary()
    """

    def __init__(self, max_steps: int = 100):
        """Initialize the session.

        Args:
            max_steps: Maximum steps to retain in history
        """
        self.max_steps = max_steps
        self.steps: list[ExplorationStep] = []
        self._visited_entities: set[str] = set()
        self._files_read: set[str] = set()  # Track file paths that have been read

    def record_action(
        self,
        tool_name: str,
        params: dict,
        result: Any,
    ) -> None:
        """Record an exploration action.

        Args:
            tool_name: Name of the tool executed
            params: Parameters passed to the tool
            result: ToolResult from execution
        """
        # Extract entities from result
        entities = self._extract_entities(result)

        # Extract content preview for file reads and greps
        content_preview = self._extract_content_preview(tool_name, result)

        # Estimate token count from result content
        token_count = self._estimate_token_count(tool_name, result)

        # Create step record
        step = ExplorationStep(
            tool=tool_name,
            params=params,
            result_summary=self._summarize_result(result),
            entities_found=entities,
            content_preview=content_preview,
            token_count=token_count,
        )

        self.steps.append(step)
        self._visited_entities.update(entities)

        # Track file paths for read_file calls
        if tool_name == "read_file" and "path" in params:
            self._files_read.add(params["path"])

        # Trim if needed
        if len(self.steps) > self.max_steps:
            self.steps = self.steps[-self.max_steps :]

    def get_context_summary(self) -> dict:
        """Get a summary of the exploration context.

        Returns:
            Dict with context information for the agent
        """
        recent_steps = self.steps[-10:] if self.steps else []

        return {
            "total_steps": len(self.steps),
            "entities_visited": list(self._visited_entities)[-20:],
            "files_read": list(self._files_read),
            "recent_actions": [
                {
                    "tool": s.tool,
                    "params": s.params,
                    "summary": s.result_summary,
                }
                for s in recent_steps
            ],
        }

    def get_files_read(self) -> list[str]:
        """Get list of file paths that have been read in this session.

        Returns:
            List of file paths
        """
        return list(self._files_read)

    def reset(self) -> None:
        """Reset the session state."""
        self.steps.clear()
        self._visited_entities.clear()
        self._files_read.clear()

    def clear_file_tracking(self) -> None:
        """Clear file tracking state without clearing exploration steps.

        This is called during context compaction so the LLM can re-read files
        that it no longer has content for in its context window.
        """
        self._files_read.clear()

    def partial_reset_for_compaction(self) -> None:
        """Partial reset for context compaction.

        Clears file tracking and old exploration steps but keeps recent ones.
        This allows the LLM to:
        - Re-read files whose contents are no longer in context
        - Still have access to recent exploration history
        """
        self._files_read.clear()
        # Keep only the last 10 steps for recent context
        if len(self.steps) > 10:
            self.steps = self.steps[-10:]
        # Keep only recent entities
        recent_entities = set()
        for step in self.steps:
            recent_entities.update(step.entities_found)
        self._visited_entities = recent_entities

    def _extract_entities(self, result: Any) -> list[str]:
        """Extract entity identifiers from a result."""
        entities = []

        if not hasattr(result, "data") or not result.data:
            return entities

        data = result.data

        # Ensure data is a dict before accessing keys
        if not isinstance(data, dict):
            return entities

        # Extract from results list
        if "results" in data:
            for item in data["results"][:10]:
                if isinstance(item, dict):
                    for key in ["qualified_name", "file_path", "identifier"]:
                        if key in item:
                            entities.append(str(item[key]))
                            break

        # Extract from root_node
        if "root_node" in data:
            root = data["root_node"]
            for key in ["qualified_name", "file_path"]:
                if key in root:
                    entities.append(str(root[key]))

        return entities

    def _summarize_result(self, result: Any) -> str:
        """Create a brief summary of a result."""
        if not hasattr(result, "success"):
            return "Unknown result"

        if not result.success:
            return f"Error: {result.error}"

        if not result.data:
            return "Empty result"

        data = result.data

        # Ensure data is a dict before accessing keys
        if not isinstance(data, dict):
            return str(data)[:200] if data else "Completed"

        if "results" in data:
            return f"Found {len(data['results'])} results"
        elif "root_node" in data:
            node = data["root_node"]
            if isinstance(node, dict):
                name = node.get("qualified_name") or node.get("file_path", "unknown")
            else:
                name = str(node)
            return f"Expanded: {name}"
        elif "callers" in data:
            return f"Found {len(data['callers'])} callers"
        elif "callees" in data:
            return f"Found {len(data['callees'])} callees"
        elif "prs" in data:
            return f"Found {len(data['prs'])} PRs"
        else:
            return "Completed"

    def _extract_content_preview(
        self,
        tool_name: str,
        result: Any,
        max_lines: int = 5,
        max_chars: int = 300,
    ) -> Optional[str]:
        """Extract a content preview from tool results.

        Args:
            tool_name: Name of the tool
            result: ToolResult from execution
            max_lines: Maximum lines to include
            max_chars: Maximum characters to include

        Returns:
            Content preview string or None
        """
        if not hasattr(result, "success") or not result.success:
            return None

        if not hasattr(result, "data") or not result.data:
            return None

        data = result.data

        # read_file - show first few lines
        if tool_name == "read_file" and "content" in data:
            content = data["content"]
            lines = content.split("\n")[:max_lines]
            preview = "\n".join(lines)
            if len(preview) > max_chars:
                preview = preview[:max_chars] + "..."
            elif len(content.split("\n")) > max_lines:
                preview += "\n..."
            return preview

        # grep - show first few matches
        if tool_name == "grep" and "results" in data:
            matches = data["results"][:max_lines]
            lines = [f"{m.get('file', '')}:{m.get('line_number', '')}: {m.get('line', '')}"
                     for m in matches if isinstance(m, dict)]
            preview = "\n".join(lines)
            if len(preview) > max_chars:
                preview = preview[:max_chars] + "..."
            return preview if lines else None

        # semantic_search - show first few result names
        if tool_name == "semantic_search" and "results" in data:
            results = data["results"][:max_lines]
            lines = [f"{r.get('type', '')}: {r.get('qualified_name', r.get('identifier', ''))}"
                     for r in results if isinstance(r, dict)]
            preview = "\n".join(lines)
            return preview if lines else None

        return None

    def _estimate_token_count(self, tool_name: str, result: Any) -> int:
        """Estimate token count from tool result content.

        Uses ~4 characters per token as rough estimate.

        Args:
            tool_name: Name of the tool
            result: ToolResult from execution

        Returns:
            Estimated token count
        """
        if not hasattr(result, "success") or not result.success:
            return 0

        if not hasattr(result, "data") or not result.data:
            return 0

        data = result.data

        # read_file - estimate from content
        if tool_name == "read_file" and "content" in data:
            content = data["content"]
            return len(content) // 4 if content else 0

        # grep - estimate from all matched lines
        if tool_name == "grep" and "results" in data:
            total_chars = 0
            for match in data["results"]:
                if isinstance(match, dict) and "line" in match:
                    total_chars += len(match["line"])
            return total_chars // 4

        # semantic_search - minimal tokens (just metadata)
        if tool_name == "semantic_search" and "results" in data:
            return len(data["results"]) * 20  # ~20 tokens per result metadata

        return 0
