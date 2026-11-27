from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core._events.event_utils import create_base_event_fields
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.workflow import workflow
from mistralai.workflows.protocol.v1.events import (
    CustomTaskCompleted,
    CustomTaskCompletedAttributes,
    CustomTaskInProgress,
    CustomTaskInProgressAttributes,
    CustomTaskStarted,
    CustomTaskStartedAttributes,
    JSONPatchPayload,
    JSONPayload,
    WorkflowEvent,
)


async def publish_manual_events(single: bool = False) -> str:
    context = EventContext.get_singleton()
    assert context is not None
    events: list[WorkflowEvent] = [
        CustomTaskStarted(
            **create_base_event_fields(),
            attributes=CustomTaskStartedAttributes(custom_task_id="manual", custom_task_type="manual_progress"),
        ),
        CustomTaskCompleted(
            **create_base_event_fields(),
            attributes=CustomTaskCompletedAttributes(
                custom_task_id="manual",
                custom_task_type="manual_progress",
                payload=JSONPayload(value={"progress": "done"}),
            ),
        ),
    ]
    if single:
        await context.publish_event(events[-1])
    else:
        await context.publish_events_batch(events)
    return "done"


@workflow.define(name="manual_patch_events")
class ManualPatchEventsWorkflow:
    @workflow.entrypoint
    async def run(self) -> None:
        context = EventContext.get_singleton()
        assert context is not None
        payload = JSONPatchPayload(value=[{"op": "replace", "path": "/content", "value": "private"}])
        payload._encrypted_paths = {"/content"}
        await context.publish_events_batch(
            [
                CustomTaskInProgress(
                    **create_base_event_fields(),
                    attributes=CustomTaskInProgressAttributes(
                        custom_task_id="manual", custom_task_type="manual_progress", payload=payload
                    ),
                )
            ]
        )


@activity(name="publish_manual_events", retry_policy_max_attempts=2)
async def publish_manual_events_activity(single: bool = False) -> str:
    return await publish_manual_events(single)


@workflow.define(name="manual_events_across_signals")
class ManualEventsAcrossSignalsWorkflow:
    # Slots make the SDK fail if it stores its own state on the workflow instance.
    __slots__ = ("advances", "published")

    def __init__(self) -> None:
        self.published = 0
        self.advances = 0

    @workflow.signal()
    async def advance(self) -> None:
        self.advances += 1

    @workflow.query()
    def published_batches(self) -> int:
        return self.published

    @workflow.entrypoint
    async def run(self) -> None:
        context = EventContext.get_singleton()
        assert context is not None
        for step in range(3):
            await workflow.wait_condition(lambda: self.advances >= step)
            fields = create_base_event_fields()
            fields["event_id"] = "reused-user-event-id"
            await context.publish_events_batch(
                [
                    CustomTaskCompleted(
                        **fields,
                        attributes=CustomTaskCompletedAttributes(
                            custom_task_id="manual",
                            custom_task_type="manual_progress",
                            payload=JSONPayload(value={"batch": step}),
                        ),
                    )
                ]
            )
            self.published += 1


@workflow.define(name="manual_events")
class ManualEventsWorkflow:
    @workflow.entrypoint
    async def run(self, in_activity: bool = False, single: bool = False) -> str:
        if in_activity:
            return await publish_manual_events_activity(single)
        return await publish_manual_events(single)
