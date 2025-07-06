from typing import Literal

from vellum.client.core import UniversalBaseModel
from vellum.workflows import BaseWorkflow
from vellum.workflows.events.types import BaseEvent
from vellum.workflows.nodes import BaseNode

VEMBDA_EXECUTION_INITIATED_EVENT_NAME = "vembda.execution.initiated"
VEMBDA_EXECUTION_FULFILLED_EVENT_NAME = "vembda.execution.fulfilled"
STREAM_FINISHED_EVENT = "STREAM_FINISHED"
SPAN_ID_EVENT = "SPAN_ID_EVENT"


class VembdaExecutionFulfilledBody(UniversalBaseModel):
    exit_code: int = 0
    log: str = ""
    stderr: str = ""
    timed_out: bool = False
    container_overhead_latency: float = 0


class VembdaExecutionFulfilledEvent(BaseEvent):
    name: Literal["vembda.execution.fulfilled"] = VEMBDA_EXECUTION_FULFILLED_EVENT_NAME  # type: ignore
    body: VembdaExecutionFulfilledBody


class VembdaExecutionInitiatedBody(UniversalBaseModel):
    sdk_version: str
    server_version: str


class VembdaExecutionInitiatedEvent(BaseEvent):
    name: Literal["vembda.execution.initiated"] = VEMBDA_EXECUTION_INITIATED_EVENT_NAME  # type: ignore
    body: VembdaExecutionInitiatedBody


VembdaExecutionFulfilledEvent.model_rebuild(
    # Not sure why this is needed, but it is required for the VembdaExecutionFulfilledEvent to be
    # properly rebuilt with the recursive types.
    _types_namespace={
        "BaseWorkflow": BaseWorkflow,
        "BaseNode": BaseNode,
    },
)
