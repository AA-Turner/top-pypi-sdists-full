"""
Workflows for testing error handling when workflow task is in failed state (599 worker error).

- stuck-task-workflow: Raises exception in entrypoint, task keeps retrying.
- failing-handlers-workflow: Handlers raise exceptions, causing task to fail.

Query/Update on these workflows should return 599.
"""

import asyncio

import pydantic

import mistralai.workflows as workflows


class EmptyInput(pydantic.BaseModel):
    pass


class StatusResult(pydantic.BaseModel):
    status: str


@workflows.workflow.define(
    name="stuck-task-workflow",
    workflow_description="Workflow that raises exception in entrypoint, causing task to be stuck retrying.",
)
class StuckTaskWorkflow:
    """
    Raises exception in entrypoint. The workflow task will keep failing and retrying.
    Query/Update on this workflow will return 599 (worker error).
    """

    def __init__(self) -> None:
        self._status = "initialized"

    @workflows.workflow.entrypoint
    async def run(self, input: EmptyInput) -> int:
        raise Exception("Intentional exception in workflow entrypoint")

    @workflows.workflow.query(name="get_status")
    def get_status(self) -> StatusResult:
        return StatusResult(status=self._status)

    @workflows.workflow.signal(name="do_signal")
    async def do_signal(self) -> None:
        self._status = "signaled"

    @workflows.workflow.update(name="do_update")
    async def do_update(self) -> StatusResult:
        return StatusResult(status="updated")


@workflows.workflow.define(
    name="failing-handlers-workflow",
    workflow_description="Workflow where handlers raise exceptions, causing task to fail.",
)
class FailingHandlersWorkflow:
    """
    Workflow runs normally, but handlers raise exceptions when called.
    This causes the workflow task to fail and retry.
    Query/Update on this workflow will return 599 (worker error).
    """

    def __init__(self) -> None:
        self._done = False

    @workflows.workflow.entrypoint
    async def run(self, input: EmptyInput) -> int:
        await workflows.workflow.wait_condition(lambda: self._done)
        return 0

    @workflows.workflow.query(name="failing_query")
    def failing_query(self) -> StatusResult:
        raise Exception("Intentional exception in query handler")

    @workflows.workflow.signal(name="failing_signal")
    async def failing_signal(self) -> None:
        raise Exception("Intentional exception in signal handler")

    @workflows.workflow.update(name="failing_update")
    async def failing_update(self) -> StatusResult:
        raise Exception("Intentional exception in update handler")

    @workflows.workflow.signal(name="done")
    async def done(self) -> None:
        self._done = True


if __name__ == "__main__":
    asyncio.run(
        workflows.run_worker(
            [StuckTaskWorkflow, FailingHandlersWorkflow],
            enable_config_discovery=False,
        )
    )
