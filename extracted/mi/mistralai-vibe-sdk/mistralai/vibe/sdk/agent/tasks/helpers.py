"""Helpers for building agent task factories."""

from collections.abc import Callable

from mistralai.vibe.sdk.agent.tasks.agent_task import AgentTask, AgentTaskConfig
from mistralai.vibe.sdk.agent.tasks.core import Task

type AgentTaskFactory = Callable[[AgentTaskConfig], Task]


def create_agent_task(task_config: AgentTaskConfig) -> Task:
    """Build a local AgentTask from task config."""
    return AgentTask.from_config(config=task_config)
