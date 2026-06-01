import asyncio

import pydantic

import mistralai.workflows as workflows
from mistralai.workflows.core.encoding.fields_offloader import OffloadableField, OffloadableModel


class WorkflowInput(pydantic.BaseModel):
    content: str = pydantic.Field(description="Content to process")


class WorkflowOutput(pydantic.BaseModel):
    original_length: int = pydantic.Field(description="Length of original content")
    processed_length: int = pydantic.Field(description="Length of processed content")
    activity_received_length: int = pydantic.Field(description="Length received by activity")


class ActivityInput(OffloadableModel):
    data: OffloadableField[str]


class ActivityOutput(OffloadableModel):
    data: OffloadableField[str]
    input_length: int


@workflows.activity()
async def process_offloadable_data(params: ActivityInput) -> ActivityOutput:
    async with workflows.task("activity.process_offloadable", {}):
        await asyncio.sleep(0.1)
        value = params.data.get_value()
        processed_value = value + "_processed"
        return ActivityOutput(
            data=OffloadableField(value=processed_value),
            input_length=len(value),
        )


@workflows.activity()
async def get_processed_length(result: ActivityOutput) -> int:
    return len(result.data.get_value())


@workflows.workflow.define(
    name="example-activity-offloading-workflow",
    workflow_display_name="Activity Offloading Example",
    workflow_description="Example workflow demonstrating activity attribute offloading for large payloads",
)
class WorkflowActivityOffloading:
    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowInput) -> WorkflowOutput:
        activity_input = ActivityInput(data=OffloadableField(value=params.content))
        activity_result = await process_offloadable_data(activity_input)
        processed_length = await get_processed_length(activity_result)

        return WorkflowOutput(
            original_length=len(params.content),
            processed_length=processed_length,
            activity_received_length=activity_result.input_length,
        )
