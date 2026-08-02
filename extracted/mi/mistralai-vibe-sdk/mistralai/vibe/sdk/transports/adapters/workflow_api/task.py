"""WorkflowAPIRemoteTask — caller-side remote task over the Workflows API.

Usage:
    from mistralai.vibe.sdk.agent.tasks.agent_task import AgentTaskConfig
    from mistralai.vibe.sdk.providers.completion import MistralCompletionConfig

    config = AgentTaskConfig(
        completion=MistralCompletionConfig(model="mistral-large-latest"),
        ...
    )
    task = WorkflowAPIRemoteTask(config, client, task_queue="my-queue")
    channel = await task.run(state)
    async for message in channel:
        apply_patches(state, message.payload.patches)
"""

import asyncio
from importlib import import_module
from typing import Any

import structlog
from mistralai.client.workflows import Workflows
from structlog.contextvars import bound_contextvars

from mistralai.vibe.sdk.agent.tasks.core import Card, Task, TaskCallback
from mistralai.vibe.sdk.agent.tasks.runtime import (
    ModuleTaskRegistry,
    TaskConfigBase,
    default_registry,
)
from mistralai.vibe.sdk.execution_record.state import TaskState
from mistralai.vibe.sdk.observability import COMMON_CONTEXT_KEYS, attributes_from_context
from mistralai.vibe.sdk.transports.adapters.workflow_api.channel import _DeferredWorkflowAPIChannel
from mistralai.vibe.sdk.transports.adapters.workflow_api.types import WorkflowTaskInput
from mistralai.vibe.sdk.transports.channel import Channel

logger = structlog.get_logger()


class WorkflowAPIRemoteTask(Task):
    """Caller-side remote task over the Workflows API.

    Implements the Task protocol. Call run(state) to start a durable workflow;
    it returns a channel that streams TaskStateUpdateEvent patches reconstructed
    from the Workflows API NATS observability stream.

    The task config is pure (AgentTaskConfig, etc.) — workflow plumbing
    (task_id, initial_state_dict) is built at run time from the TaskState.
    """

    # TODO: Infer most params from the workflow definition metadata instead of
    # requiring them as constructor params. The workflows SDK exposes:
    #   - @workflow.define(name=..., workflow_description=..., workflow_display_name=...)
    #   - input_schema / output_schema auto-derived from entrypoint type annotations
    #   - Retrievable via get_workflow(identifier) -> WorkflowGetResponse
    # So name, description, input_schema, output_schema can all be fetched from
    # the workflow definition. Only callbacks has no workflow SDK equivalent and
    # must remain a constructor param.
    def __init__(
        self,
        config: TaskConfigBase,
        client: Workflows,
        workflow_identifier: str | None = None,
        task_queue: str | None = None,
        name: str = "",
        description: str = "",
        input_schema: dict[str, Any] | None = None,
        output_schema: dict[str, Any] | None = None,
        callbacks: list[TaskCallback] | None = None,
        registry: ModuleTaskRegistry | None = None,  # construction-time only; see note below
    ) -> None:
        # registry is used here only to resolve the workflow_identifier at
        # construction time. It does not propagate to the Temporal worker:
        # the worker reconstructs tasks via default_registry. The deploying
        # process must install matching extensions globally.
        self._config = config
        self._client = client
        reg = registry or default_registry
        self._registry = reg
        if workflow_identifier is None:
            import_module("mistralai.vibe.sdk.transports.adapters.workflow_api.agent_workflow")
        self._workflow_identifier = workflow_identifier or reg.resolve_workflow_name(config)
        self._task_queue = task_queue
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.callbacks: list[TaskCallback] = callbacks or []

    @property
    def card(self) -> Card:
        return Card(
            name=self.name,
            description=self.description,
            input_schema=self.input_schema,
            output_schema=self.output_schema,
            callbacks=self.callbacks,
        )

    async def run(self, state: TaskState) -> Channel:
        """Start the workflow and return a streaming channel.

        Builds WorkflowTaskInput from the config + state, starts the workflow
        via execute_workflow(), and returns a _DeferredWorkflowAPIChannel that
        subscribes to NATS events once the exec_id is available.
        """
        binding = self._registry.get_binding(self._config.type)
        config_cls = binding.config_cls if binding is not None else type(self._config)
        input_data = WorkflowTaskInput[config_cls](
            task_config=self._config,
            task_id=state.id,
            initial_state_dict=state.model_dump(),
            observability_context=attributes_from_context(*COMMON_CONTEXT_KEYS),
        )
        workflow_id = self._workflow_identifier

        with bound_contextvars(task_id=state.id):
            logger.info("task.run", workflow=workflow_id)

        async def _start() -> str:
            with bound_contextvars(task_id=state.id):
                response = await self._client.execute_workflow_async(
                    workflow_identifier=workflow_id,
                    input=input_data,  # type: ignore[arg-type]
                    task_queue=self._task_queue,
                )
                logger.info("task.run.started", exec_id=response.execution_id)
                return response.execution_id

        future: asyncio.Task[str] = asyncio.get_running_loop().create_task(_start())
        return _DeferredWorkflowAPIChannel(self._client, future, initial_state=state)
