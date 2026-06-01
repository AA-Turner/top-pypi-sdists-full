import asyncio

from pydantic import BaseModel, Field

import mistralai.workflows as workflows

"""
Workflow for testing encoding (offloading + encryption).

Sends a large payload to all handler inputs/results to verify offloading.
All input/result payloads are used to ensure proper decoding.
"""


class WeightedPayloadBase(BaseModel):
    large_payload: str = Field(default="", description="Large payload data for testing")


class WorkflowParams(WeightedPayloadBase):
    initial_string: str = Field(description="Initial string value")
    signal_wait_attempt: int = Field(default=30, description="Timeout for workflow execution")


class ActivityParams(WeightedPayloadBase):
    base_string: str = Field(description="Base string for activity processing")


class ActivityResult(WeightedPayloadBase):
    processed_string: str = Field(description="String processed by activity")


class SignalParams(WeightedPayloadBase):
    signal_string: str = Field(description="Signal string value")


class QueryParams(WeightedPayloadBase):
    query_string: str = Field(description="Query string value")


class QueryResult(WeightedPayloadBase):
    current_string: str = Field(description="Current string value")
    query_string: str = Field(description="Query string sent as param")


class UpdateParams(WeightedPayloadBase):
    suffix: str = Field(description="Suffix to append to current string")


class UpdateResult(WeightedPayloadBase):
    new_string: str = Field(description="String after update")


class WorkflowResult(WeightedPayloadBase):
    final_string: str = Field(description="Final string value")
    timeout: bool = Field(description="Whether the workflow timed out")


@workflows.activity()
async def initialize_string_activity(params: ActivityParams) -> ActivityResult:
    processed_string = f"{params.base_string};activity_call"
    return ActivityResult(processed_string=processed_string, large_payload=params.large_payload)


@workflows.workflow.define(
    name="workflow-with-weighted-payloads",
    workflow_description="Workflow to test all handler types with optional large payload weight",
)
class WorkflowWithWeightedPayloads:
    def __init__(self) -> None:
        self.current_string = "init"
        self.weighted_payload = ""
        self.should_continue = True

    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> WorkflowResult:
        # Initialize string using activity
        self.current_string = params.initial_string
        activity_params = ActivityParams(base_string=params.initial_string, large_payload=params.large_payload)
        activity_result = await initialize_string_activity(activity_params)

        self.current_string = activity_result.processed_string
        self.weighted_payload = activity_result.large_payload
        self.signal_wait_attempt = params.signal_wait_attempt

        while self.should_continue and self.signal_wait_attempt > 0:
            await asyncio.sleep(1)
            self.signal_wait_attempt -= 1

        return WorkflowResult(
            final_string=self.current_string, large_payload=self.weighted_payload, timeout=self.should_continue
        )

    @workflows.workflow.signal(name="stop_workflow")
    async def exit_loop_signal(self, params: SignalParams) -> None:
        self.current_string = f"{self.current_string};{params.signal_string}"
        self.weighted_payload = params.large_payload
        self.should_continue = False

    @workflows.workflow.query(name="get_current_string")
    def get_current_string_query(self, params: QueryParams) -> QueryResult:
        return QueryResult(
            current_string=self.current_string, query_string=params.query_string, large_payload=params.large_payload
        )

    @workflows.workflow.update(name="append_suffix")
    async def append_suffix_update(self, params: UpdateParams) -> UpdateResult:
        self.current_string += f";{params.suffix}"
        return UpdateResult(new_string=self.current_string, large_payload=params.large_payload)


@workflows.workflow.define(
    name="workflow-scheduled-with-weighted-payloads",
    workflow_description="Workflow to test schedules with large payload weight",
)
class WorkflowScheduledWithWeightedPayloads:
    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> WorkflowResult:
        return WorkflowResult(
            final_string=params.initial_string,
            large_payload=params.large_payload,
            timeout=False,
        )


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([WorkflowWithWeightedPayloads, WorkflowScheduledWithWeightedPayloads]))
