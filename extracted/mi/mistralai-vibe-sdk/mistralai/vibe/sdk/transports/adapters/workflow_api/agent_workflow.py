"""DurableAgentWorkflow — reference TaskWorkflowMixin implementation for AgentTask.

Separated from workflow.py so the generic mixin has no agent-specific
imports. Importing this module triggers __init_subclass__ which computes
AgentModule's activities and installs the workflow binding.
"""

from mistralai.workflows import workflow  # type: ignore[reportMissingImports]

with workflow.unsafe.imports_passed_through():
    from mistralai.vibe.sdk.agent.tasks.agent_task import AgentTask, AgentTaskConfig
    from mistralai.vibe.sdk.agent.tasks.runtime import TaskExtension, default_registry
    from mistralai.vibe.sdk.execution_record.state import TaskState
    from mistralai.vibe.sdk.transports.adapters.workflow_api.types import WorkflowTaskInput
    from mistralai.vibe.sdk.transports.adapters.workflow_api.workflow import TaskWorkflowMixin


@workflow.define(name="DurableAgentWorkflow", enforce_determinism=False)
class DurableAgentWorkflow(TaskWorkflowMixin[AgentTask, AgentTaskConfig]):
    """Runs an AgentTask as a durable Temporal workflow."""

    @workflow.entrypoint
    async def run(self, input: WorkflowTaskInput[AgentTaskConfig]) -> TaskState:
        return await self.run_task(input)


# Install built-in workflow binding
default_registry.install(
    TaskExtension(
        config_cls=AgentTaskConfig,
        task_cls=AgentTask,
        workflow_cls=DurableAgentWorkflow,
    )
)
