import asyncio
from typing import List

import pydantic

import mistralai.workflows as workflows
from mistralai.workflows import workflow
from mistralai.workflows.examples.workflow_example import Workflow as WorkflowExample

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.getLogger(__name__)


class WorkflowParams(pydantic.BaseModel):
    document_title: str


class Result(pydantic.BaseModel):
    results: List[str] = pydantic.Field(description="List of results")


@workflows.workflow.define(name="example-with-sub-workflow")
class WorkflowExampleWithSubWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, document_title: str) -> Result:
        res: Result = await workflows.workflow.execute_workflow(
            WorkflowExample, params=WorkflowParams(document_title=document_title)
        )
        return Result(results=res.results)


if __name__ == "__main__":
    asyncio.run(workflows.run_worker(workflows=[WorkflowExampleWithSubWorkflow, WorkflowExample]))

    # or for running it as a script
    # asyncio.run(
    #     workflows.workflow.execute_workflow(
    #         WorkflowExampleWithSubWorkflow,
    #         params=WorkflowParams(document_title="test"),
    #     )
    # )
