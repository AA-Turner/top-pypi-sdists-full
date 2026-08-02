"""Agent task-runtime context.

Namespace for the task runtime mechanism used by agentic work.
"""

from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "AgentTask",
    "AgentTaskConfig",
    "AgentTaskFactory",
    "Card",
    "ModuleTask",
    "ModuleTaskRegistry",
    "QueueDownstreamWriter",
    "StatefulTask",
    "Task",
    "TaskCallback",
    "TaskConfigBase",
    "TaskExtension",
    "ToolAsCodeModule",
    "ToolAsCodeTask",
    "create_agent_task",
    "default_registry",
    "extract_impl_configs",
    "task_from_config",
]

if TYPE_CHECKING:
    from mistralai.vibe.sdk.agent.tasks.agent_task import AgentTask, AgentTaskConfig
    from mistralai.vibe.sdk.agent.tasks.code_task import ToolAsCodeModule, ToolAsCodeTask
    from mistralai.vibe.sdk.agent.tasks.core import Card, StatefulTask, Task, TaskCallback
    from mistralai.vibe.sdk.agent.tasks.helpers import AgentTaskFactory, create_agent_task
    from mistralai.vibe.sdk.agent.tasks.runtime import (
        ModuleTask,
        ModuleTaskRegistry,
        QueueDownstreamWriter,
        TaskConfigBase,
        TaskExtension,
        default_registry,
        extract_impl_configs,
        task_from_config,
    )

_LAZY_EXPORTS = {
    "AgentTask": "mistralai.vibe.sdk.agent.tasks.agent_task",
    "AgentTaskConfig": "mistralai.vibe.sdk.agent.tasks.agent_task",
    "AgentTaskFactory": "mistralai.vibe.sdk.agent.tasks.helpers",
    "Card": "mistralai.vibe.sdk.agent.tasks.core",
    "ModuleTask": "mistralai.vibe.sdk.agent.tasks.runtime",
    "ModuleTaskRegistry": "mistralai.vibe.sdk.agent.tasks.runtime",
    "QueueDownstreamWriter": "mistralai.vibe.sdk.agent.tasks.runtime",
    "StatefulTask": "mistralai.vibe.sdk.agent.tasks.core",
    "Task": "mistralai.vibe.sdk.agent.tasks.core",
    "TaskCallback": "mistralai.vibe.sdk.agent.tasks.core",
    "TaskConfigBase": "mistralai.vibe.sdk.agent.tasks.runtime",
    "TaskExtension": "mistralai.vibe.sdk.agent.tasks.runtime",
    "ToolAsCodeModule": "mistralai.vibe.sdk.agent.tasks.code_task",
    "ToolAsCodeTask": "mistralai.vibe.sdk.agent.tasks.code_task",
    "create_agent_task": "mistralai.vibe.sdk.agent.tasks.helpers",
    "default_registry": "mistralai.vibe.sdk.agent.tasks.runtime",
    "extract_impl_configs": "mistralai.vibe.sdk.agent.tasks.runtime",
    "task_from_config": "mistralai.vibe.sdk.agent.tasks.runtime",
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value
