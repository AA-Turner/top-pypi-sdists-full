import asyncio

import pydantic

import mistralai.workflows as workflows
from mistralai.workflows.examples.workflow_example import Workflow as WorkflowExample


class CompareWaitModesParams(pydantic.BaseModel):
    document_title: str


class CompareWaitModesResult(pydantic.BaseModel):
    wait_true: list[str]
    wait_false: list[str]
    match: bool


@workflows.workflow.define(name="example-compare-child-wait-modes")
class WorkflowCompareChildWaitModes:
    @workflows.workflow.entrypoint
    async def run(self, document_title: str) -> CompareWaitModesResult:
        params = CompareWaitModesParams(document_title=document_title)

        wait_true_result = await workflows.workflow.execute_workflow(
            WorkflowExample,
            params=params,
            wait=True,
        )

        handle = await workflows.workflow.execute_workflow(
            WorkflowExample,
            params=params,
            wait=False,
        )
        wait_false_result = await handle

        return CompareWaitModesResult(
            wait_true=wait_true_result.results,
            wait_false=wait_false_result.results,
            match=wait_true_result.results == wait_false_result.results,
        )


if __name__ == "__main__":
    asyncio.run(workflows.run_worker(workflows=[WorkflowCompareChildWaitModes, WorkflowExample]))
