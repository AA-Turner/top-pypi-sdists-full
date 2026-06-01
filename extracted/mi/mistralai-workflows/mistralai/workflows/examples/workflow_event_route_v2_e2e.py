import uuid
from datetime import timedelta

from pydantic import BaseModel

import mistralai.workflows as workflows
from mistralai.workflows.core._events.event_route_publisher import EventRoutePublisher
from mistralai.workflows.core._events.event_utils import create_base_event_fields
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.protocol.v1.events import (
    CustomTaskCompleted,
    CustomTaskCompletedAttributes,
    JSONPayload,
)

WORKFLOW_NAME = "example-event-route-v2-e2e-workflow"


class EventRouteV2Result(BaseModel):
    used_v2_event_route: bool
    event_id: str
    custom_task_id: str


@workflows.activity(start_to_close_timeout=timedelta(minutes=1))
async def publish_event_route_v2_event() -> EventRouteV2Result:
    context = retrieve_context()
    if context is None or context.execution_token is None:
        raise RuntimeError("Execution token is not available")

    api_key = config.common.mistral_api_key
    if api_key is None:
        raise RuntimeError("MISTRAL_API_KEY is not configured")

    custom_task_id = f"event-route-v2-{uuid.uuid4().hex[:8]}"
    event = CustomTaskCompleted(
        **create_base_event_fields(),
        attributes=CustomTaskCompletedAttributes(
            custom_task_id=custom_task_id,
            custom_task_type="event-route-v2-e2e",
            payload=JSONPayload(value={"used_v2_event_route": True}),
        ),
    )

    server_url = config.worker.server_url.rstrip("/")
    async with get_worker_client(base_url=server_url, api_key=api_key.get_secret_value()) as worker_client:
        publisher = EventRoutePublisher(worker_client, events_api_version="v2")
        used_v2_event_route = await publisher.publish_events([event])

    if not used_v2_event_route:
        raise RuntimeError("v2 event route was not used")

    return EventRouteV2Result(
        used_v2_event_route=used_v2_event_route,
        event_id=event.event_id,
        custom_task_id=custom_task_id,
    )


@workflows.workflow.define(
    name=WORKFLOW_NAME,
    workflow_description="E2E test: publishes a worker event through v2 route tokens",
)
class EventRouteV2E2EWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> EventRouteV2Result:
        return await publish_event_route_v2_event()
