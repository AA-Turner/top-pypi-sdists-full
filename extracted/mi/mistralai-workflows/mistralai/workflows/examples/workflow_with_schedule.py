import asyncio
from typing import List

import pydantic

import mistralai.workflows as workflows
from mistralai.workflows import workflow

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.getLogger(__name__)


class Params(pydantic.BaseModel):
    query: str


class Result(pydantic.BaseModel):
    results: List[str] = pydantic.Field(description="List of results")


class WorkflowParams(pydantic.BaseModel):
    document_title: str = pydantic.Field(description="Title of the document")


@workflows.activity()
async def my_activity_workflow_example_with_schedule(params: Params) -> Result:
    async with workflows.task("activity.processing", {"query": params.query}):
        await asyncio.sleep(1)

    return Result(results=["result1", "result2"])


@workflows.workflow.define(
    name="example-with-schedule",
    schedules=[
        workflows.Schedule(
            input=WorkflowParams(document_title="test"),
            cron_expressions=["* * * * *"],
        )
    ],
)
class WorkflowExampleWithSchedule:
    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> Result:
        results = await my_activity_workflow_example_with_schedule(Params(query=params.document_title))
        return results


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([WorkflowExampleWithSchedule]))
