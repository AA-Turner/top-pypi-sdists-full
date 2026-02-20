"""Tool handler for sending tasks to downstream stages.

Creates one handler per workflow transition, using the task SDK
to dispatch tasks to connected stages.
"""

import json
from typing import Any, Dict, Optional

from abstra_internals.controllers.sdk.sdk_tasks import TasksSDKController


class SendTaskHandler:
    """Handler for sending a task to a downstream stage."""

    def __init__(
        self,
        task_type: str,
        task_sdk: TasksSDKController,
        task_schema: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._task_type = task_type
        self._task_sdk = task_sdk
        self._task_schema = task_schema
        self._sent_tasks: list[Dict[str, Any]] = []

    @property
    def name(self) -> str:
        return f"send_task_{self._task_type}"

    @property
    def description(self) -> str:
        schema_hint = ""
        if self._task_schema:
            schema_hint = f" Expected payload schema: {json.dumps(self._task_schema)}"
        return (
            f"Send a task of type '{self._task_type}' to the next stage "
            f"in the workflow.{schema_hint}"
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        if self._task_schema:
            return self._task_schema
        return {
            "type": "object",
            "description": "The task payload data.",
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        payload = action_input
        if not isinstance(payload, dict):
            return "Error: action_input must be an object."

        try:
            self._task_sdk.send_task(
                type=self._task_type,
                payload=payload,
                show_warning=False,
            )
            self._sent_tasks.append(
                {
                    "type": self._task_type,
                    "payload": payload,
                }
            )
            return f"Task of type '{self._task_type}' sent successfully."
        except Exception as e:
            return f"Error sending task: {str(e)}"

    def get_sent_tasks(self) -> list[Dict[str, Any]]:
        return list(self._sent_tasks)
