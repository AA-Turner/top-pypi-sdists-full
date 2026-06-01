"""Helper workflow for the route-token integration test.

It stays alive long enough to expose its execution token via query, so the
integration test can mint a route token and ingest a v2 event end to end.
"""

from pydantic import BaseModel

import mistralai.workflows as workflows
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context


class ExecutionTokenQueryResult(BaseModel):
    execution_token: str | None


@workflows.workflow.define(
    name="example-execution-token-running-workflow",
    workflow_description="Keeps running until stopped and exposes its execution token via query",
)
class ExecutionTokenRunningWorkflow:
    def __init__(self) -> None:
        self._execution_token: str | None = None
        self._stop_requested = False

    @workflows.workflow.entrypoint
    async def run(self) -> None:
        context = retrieve_context()
        self._execution_token = context.execution_token if context else None
        await workflows.workflow.wait_condition(lambda: self._stop_requested)

    @workflows.workflow.query(name="get_execution_token")
    def get_execution_token_query(self) -> ExecutionTokenQueryResult:
        return ExecutionTokenQueryResult(execution_token=self._execution_token)

    @workflows.workflow.signal(name="stop")
    async def stop_signal(self) -> None:
        self._stop_requested = True
