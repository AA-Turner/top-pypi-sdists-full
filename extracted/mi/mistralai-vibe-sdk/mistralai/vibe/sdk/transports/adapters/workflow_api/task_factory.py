"""Workflow-API-backed agent task factory.

Builds durable remote agent tasks backed by the workflow API transport. The
heavy ``WorkflowAPIRemoteTask`` binding is imported lazily inside the factory so
importing this module stays cheap and does not pull in the workflow client.
"""

from typing import TYPE_CHECKING

from mistralai.vibe.sdk.agent.tasks.agent_task import AgentTaskConfig
from mistralai.vibe.sdk.agent.tasks.core import Task

if TYPE_CHECKING:
    from mistralai.client.workflows import Workflows

    from mistralai.vibe.sdk.agent.tasks.helpers import AgentTaskFactory
    from mistralai.vibe.sdk.agent.tasks.runtime import ModuleTaskRegistry


def create_durable_agent_task_factory(
    *,
    client: "Workflows",
    workflow_identifier: str | None = None,
    task_queue: str | None = None,
    registry: "ModuleTaskRegistry | None" = None,
) -> "AgentTaskFactory":
    """Create a factory that builds workflow-backed remote tasks."""

    from mistralai.vibe.sdk.transports.adapters.workflow_api.task import WorkflowAPIRemoteTask

    def factory(task_config: AgentTaskConfig) -> Task:
        return WorkflowAPIRemoteTask(
            config=task_config,
            client=client,
            workflow_identifier=workflow_identifier,
            task_queue=task_queue,
            name=task_config.name,
            description=task_config.description,
            input_schema=task_config.input_schema,
            callbacks=task_config.direct_callbacks,
            registry=registry,
        )

    return factory
