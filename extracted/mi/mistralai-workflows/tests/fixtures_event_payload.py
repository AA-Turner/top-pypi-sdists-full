from mistralai.workflows.core._events.event_context import (
    EventContext,
)
from mistralai.workflows.core._events.event_utils import create_base_event_fields
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.workflow import workflow
from mistralai.workflows.protocol.v1.events import (
    CustomTaskCompleted,
    CustomTaskCompletedAttributes,
    JSONPayload,
)


async def publish_manual_payloads() -> None:
    context = EventContext.get_singleton()
    assert context is not None
    await context.publish_events_batch(
        [
            CustomTaskCompleted(
                **create_base_event_fields(),
                attributes=CustomTaskCompletedAttributes(
                    custom_task_id=task_id,
                    custom_task_type="manual_payload",
                    payload=JSONPayload(value=value),
                ),
            )
            for task_id, value in [
                ("unserializable", object()),
                ("serializable", {"secret": "still-private"}),
            ]
        ]
    )


@activity(name="publish_manual_payloads", retry_policy_max_attempts=1)
async def publish_manual_payloads_activity() -> None:
    await publish_manual_payloads()


@workflow.define(name="manual_payload_events")
class ManualPayloadEventsWorkflow:
    @workflow.entrypoint
    async def run(self, in_activity: bool = False) -> None:
        if in_activity:
            await publish_manual_payloads_activity()
        else:
            await publish_manual_payloads()
