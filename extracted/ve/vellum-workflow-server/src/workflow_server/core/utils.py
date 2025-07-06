from datetime import datetime
from uuid import uuid4
from typing import Optional

from workflow_server.core.events import VembdaExecutionFulfilledBody, VembdaExecutionFulfilledEvent
from workflow_server.core.workflow_executor_context import BaseExecutorContext


def _create_vembda_rejected_event_base(
    executor_context: Optional[BaseExecutorContext], error_message: str
) -> VembdaExecutionFulfilledEvent:
    if executor_context:
        trace_id = executor_context.trace_id
        span_id = executor_context.execution_id
        container_overhead_latency = executor_context.container_overhead_latency
    else:
        trace_id = uuid4()
        span_id = uuid4()
        container_overhead_latency = None

    return VembdaExecutionFulfilledEvent(
        id=uuid4(),
        timestamp=datetime.now(),
        trace_id=trace_id,
        span_id=span_id,
        body=VembdaExecutionFulfilledBody(
            exit_code=-1,
            stderr=error_message,
            container_overhead_latency=container_overhead_latency,
        ),
        parent=None,
    )


def create_vembda_rejected_event(executor_context: Optional[BaseExecutorContext], error_message: str) -> dict:
    return _create_vembda_rejected_event_base(executor_context, error_message).model_dump(mode="json")


def serialize_vembda_rejected_event(executor_context: Optional[BaseExecutorContext], error_message: str) -> str:
    return _create_vembda_rejected_event_base(executor_context, error_message).model_dump_json()
