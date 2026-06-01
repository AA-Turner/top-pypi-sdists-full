import asyncio
from typing import List

import pydantic

import mistralai.workflows as workflows


class Params(pydantic.BaseModel):
    query: str


class Result(pydantic.BaseModel):
    results: List[str] = pydantic.Field(description="List of results")


class WorkflowParams(pydantic.BaseModel):
    document_title: str = pydantic.Field(description="Title of the document")


@workflows.activity()
async def my_activity_different_task_queue(params: Params) -> Result:
    async with workflows.task("activity.processing", {"query": params.query}):
        await asyncio.sleep(1)  # Simulating work

    return Result(results=["result1", "result2"])


@workflows.activity()
async def my_activity_different_task_queue_2(params: Params) -> Result:
    await asyncio.sleep(1)  # Simulating work
    return Result(results=["result1", "result2"])


@workflows.workflow.define(name="example-different-task-queue-workflow", workflow_description="Example workflow")
class Workflow:
    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> Result:
        results = await my_activity_different_task_queue(Params(query=params.document_title))
        results = await my_activity_different_task_queue_2(Params(query=params.document_title))
        return results


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([Workflow]))
