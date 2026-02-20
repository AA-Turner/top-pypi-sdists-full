"""Tool dispatcher for agent execution.

Routes actions to registered tool handlers and collects results.
Each handler implements the ToolHandler protocol.
"""

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Protocol, runtime_checkable


@runtime_checkable
class ToolHandler(Protocol):
    """Protocol for agent tool handlers."""

    @property
    def name(self) -> str: ...

    @property
    def description(self) -> str: ...

    @property
    def input_schema(self) -> Dict[str, Any]: ...

    def execute(self, action_input: Dict[str, Any]) -> str: ...


@dataclass
class FinishHandler:
    """Built-in handler for finishing execution."""

    @property
    def name(self) -> str:
        return "finish"

    @property
    def description(self) -> str:
        return "Complete the task and provide the final answer."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "answer": {
                    "type": "string",
                    "description": "The final answer or summary of what was accomplished.",
                },
            },
            "required": ["answer"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        return action_input.get("answer", "Task completed.")


class ToolDispatcher:
    """Routes actions to registered tool handlers."""

    def __init__(self, handlers: List[ToolHandler]) -> None:
        self._handlers: Dict[str, ToolHandler] = {h.name: h for h in handlers}
        self._sent_tasks: List[Dict[str, Any]] = []

    def get_tool_descriptions(self) -> str:
        lines = []
        for handler in self._handlers.values():
            schema_str = json.dumps(handler.input_schema, indent=2)
            lines.append(
                f"- **{handler.name}**: {handler.description}\n"
                f"  Input schema: {schema_str}"
            )
        return "\n\n".join(lines)

    def get_action_names(self) -> List[str]:
        return list(self._handlers.keys())

    def dispatch(self, action: str, action_input: Dict[str, Any]) -> str:
        handler = self._handlers.get(action)
        if handler is None:
            available = ", ".join(self._handlers.keys())
            hint = ""
            if "execute_connection_action" in self._handlers:
                hint = (
                    " HINT: To call external service actions (Slack, etc.), "
                    "use 'execute_connection_action' with connection_name and action_name parameters. "
                    "Use 'get_connection_action_details' to find available actions."
                )
            return f"Error: Unknown action '{action}'. Available actions: [{available}].{hint}"

        try:
            result = handler.execute(action_input)
            return result
        except Exception as e:
            return f"Error executing '{action}': {str(e)}"

    def record_sent_task(self, task_data: Dict[str, Any]) -> None:
        self._sent_tasks.append(task_data)

    def get_sent_tasks(self) -> List[Dict[str, Any]]:
        return list(self._sent_tasks)
