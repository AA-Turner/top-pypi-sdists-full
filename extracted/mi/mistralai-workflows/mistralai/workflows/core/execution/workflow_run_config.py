"""Worker settings that workflow code reads, recorded once per run so replay never sees a later value.

Workflow code that branches on a worker setting must read it from here, never from `config.worker`:
the setting can change between two replays of the same run, which would make the run fail to replay.
"""

from contextvars import ContextVar
from datetime import timedelta

import temporalio.workflow
from pydantic import BaseModel, ConfigDict

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.config.config import INTERNAL_ACTIVITY_PREFIX, config
from mistralai.workflows.core.utils.contextvars import unwrap_contextual_result
from mistralai.workflows.protocol.v1.events import WorkflowEventCategory

RECORD_WORKFLOW_RUN_CONFIG_PATCH = "record-workflow-run-config"
RECORD_WORKFLOW_RUN_CONFIG_ACTIVITY_NAME = f"{INTERNAL_ACTIVITY_PREFIX}record_workflow_run_config"


class WorkflowRunConfig(BaseModel):
    """A field's default must reproduce the behaviour of runs recorded before the field existed."""

    model_config = ConfigDict(frozen=True)

    emitted_event_categories: frozenset[WorkflowEventCategory] = frozenset(WorkflowEventCategory)

    def emits(self, category: WorkflowEventCategory) -> bool:
        return category in self.emitted_event_categories


class WorkflowRunConfigHolder:
    """One per run, shared by the entrypoint and the signal and update handlers."""

    def __init__(self) -> None:
        self.run_config: WorkflowRunConfig | None = None


workflow_run_config_holder_var: ContextVar[WorkflowRunConfigHolder | None] = ContextVar(
    "workflow_run_config_holder", default=None
)


def current_workflow_run_config() -> WorkflowRunConfig:
    """The current run's snapshot, or the defaults for a run that has not recorded one."""
    holder = workflow_run_config_holder_var.get()
    if holder is None or holder.run_config is None:
        return WorkflowRunConfig()
    return holder.run_config


@activity(name=RECORD_WORKFLOW_RUN_CONFIG_ACTIVITY_NAME, _allow_reserved_name=True)
async def _record_workflow_run_config() -> WorkflowRunConfig:
    context = EventContext.get_singleton()
    categories = context.emitted_event_categories if context else config.worker.emitted_event_categories
    return WorkflowRunConfig(emitted_event_categories=frozenset(categories))


async def record_workflow_run_config() -> WorkflowRunConfig:
    """Record the snapshot in the run's history. Runs started before the patch keep the defaults."""
    if not temporalio.workflow.patched(RECORD_WORKFLOW_RUN_CONFIG_PATCH):
        return WorkflowRunConfig()
    result = await temporalio.workflow.execute_local_activity(
        _record_workflow_run_config,
        start_to_close_timeout=timedelta(seconds=10),
    )
    _, run_config = unwrap_contextual_result(result)
    return WorkflowRunConfig.model_validate(run_config)
