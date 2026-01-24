from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.assay_run_created_event import AssayRunCreatedEvent
from ..models.assay_run_updated_fields_event import AssayRunUpdatedFieldsEvent
from ..models.automation_input_generator_completed_v2_beta_event import (
    AutomationInputGeneratorCompletedV2BetaEvent,
)
from ..models.automation_input_generator_completed_v2_event import AutomationInputGeneratorCompletedV2Event
from ..models.automation_output_processor_completed_v2_beta_event import (
    AutomationOutputProcessorCompletedV2BetaEvent,
)
from ..models.automation_output_processor_completed_v2_event import AutomationOutputProcessorCompletedV2Event
from ..models.automation_output_processor_uploaded_v2_beta_event import (
    AutomationOutputProcessorUploadedV2BetaEvent,
)
from ..models.automation_output_processor_uploaded_v2_event import AutomationOutputProcessorUploadedV2Event
from ..models.automation_transform_status_failed_event_v2_event import (
    AutomationTransformStatusFailedEventV2Event,
)
from ..models.automation_transform_status_pending_event_v2_event import (
    AutomationTransformStatusPendingEventV2Event,
)
from ..models.automation_transform_status_running_event_v2_event import (
    AutomationTransformStatusRunningEventV2Event,
)
from ..models.automation_transform_status_succeeded_event_v2_event import (
    AutomationTransformStatusSucceededEventV2Event,
)
from ..models.entity_registered_event import EntityRegisteredEvent
from ..models.entry_created_event import EntryCreatedEvent
from ..models.entry_updated_assigned_reviewers_event import EntryUpdatedAssignedReviewersEvent
from ..models.entry_updated_fields_event import EntryUpdatedFieldsEvent
from ..models.entry_updated_review_record_event import EntryUpdatedReviewRecordEvent
from ..models.entry_updated_review_snapshot_beta_event import EntryUpdatedReviewSnapshotBetaEvent
from ..models.request_created_event import RequestCreatedEvent
from ..models.request_updated_fields_event import RequestUpdatedFieldsEvent
from ..models.stage_entry_created_event import StageEntryCreatedEvent
from ..models.stage_entry_updated_assigned_reviewers_event import StageEntryUpdatedAssignedReviewersEvent
from ..models.stage_entry_updated_fields_event import StageEntryUpdatedFieldsEvent
from ..models.stage_entry_updated_review_record_event import StageEntryUpdatedReviewRecordEvent
from ..models.workflow_output_created_event import WorkflowOutputCreatedEvent
from ..models.workflow_output_updated_fields_event import WorkflowOutputUpdatedFieldsEvent
from ..models.workflow_task_created_event import WorkflowTaskCreatedEvent
from ..models.workflow_task_group_created_event import WorkflowTaskGroupCreatedEvent
from ..models.workflow_task_group_mapping_completed_event import WorkflowTaskGroupMappingCompletedEvent
from ..models.workflow_task_group_updated_watchers_event import WorkflowTaskGroupUpdatedWatchersEvent
from ..models.workflow_task_updated_assignee_event import WorkflowTaskUpdatedAssigneeEvent
from ..models.workflow_task_updated_fields_event import WorkflowTaskUpdatedFieldsEvent
from ..models.workflow_task_updated_scheduled_on_event import WorkflowTaskUpdatedScheduledOnEvent
from ..models.workflow_task_updated_status_event import WorkflowTaskUpdatedStatusEvent
from ..models.worksheet_updated_review_snapshot_beta_event import WorksheetUpdatedReviewSnapshotBetaEvent
from ..types import UNSET, Unset

T = TypeVar("T", bound="EventsPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class EventsPaginatedList:
    """  """

    _events: Union[
        Unset,
        List[
            Union[
                EntityRegisteredEvent,
                EntryCreatedEvent,
                EntryUpdatedFieldsEvent,
                EntryUpdatedReviewRecordEvent,
                EntryUpdatedAssignedReviewersEvent,
                EntryUpdatedReviewSnapshotBetaEvent,
                StageEntryCreatedEvent,
                StageEntryUpdatedFieldsEvent,
                StageEntryUpdatedReviewRecordEvent,
                StageEntryUpdatedAssignedReviewersEvent,
                RequestCreatedEvent,
                RequestUpdatedFieldsEvent,
                AssayRunCreatedEvent,
                AssayRunUpdatedFieldsEvent,
                AutomationInputGeneratorCompletedV2BetaEvent,
                AutomationOutputProcessorCompletedV2BetaEvent,
                AutomationOutputProcessorUploadedV2BetaEvent,
                AutomationInputGeneratorCompletedV2Event,
                AutomationOutputProcessorCompletedV2Event,
                AutomationOutputProcessorUploadedV2Event,
                AutomationTransformStatusPendingEventV2Event,
                AutomationTransformStatusRunningEventV2Event,
                AutomationTransformStatusSucceededEventV2Event,
                AutomationTransformStatusFailedEventV2Event,
                WorkflowTaskGroupCreatedEvent,
                WorkflowTaskGroupMappingCompletedEvent,
                WorkflowTaskCreatedEvent,
                WorkflowTaskUpdatedFieldsEvent,
                WorkflowTaskUpdatedStatusEvent,
                WorkflowTaskUpdatedAssigneeEvent,
                WorkflowTaskUpdatedScheduledOnEvent,
                WorkflowTaskGroupUpdatedWatchersEvent,
                WorkflowOutputCreatedEvent,
                WorkflowOutputUpdatedFieldsEvent,
                WorksheetUpdatedReviewSnapshotBetaEvent,
                UnknownType,
            ]
        ],
    ] = UNSET
    _next_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("events={}".format(repr(self._events)))
        fields.append("next_token={}".format(repr(self._next_token)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "EventsPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        events: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._events, Unset):
            events = []
            for events_item_data in self._events:
                if isinstance(events_item_data, UnknownType):
                    events_item = events_item_data.value
                elif isinstance(events_item_data, EntityRegisteredEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, EntryCreatedEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, EntryUpdatedFieldsEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, EntryUpdatedReviewRecordEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, EntryUpdatedAssignedReviewersEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, EntryUpdatedReviewSnapshotBetaEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, StageEntryCreatedEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, StageEntryUpdatedFieldsEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, StageEntryUpdatedReviewRecordEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, StageEntryUpdatedAssignedReviewersEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, RequestCreatedEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, RequestUpdatedFieldsEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, AssayRunCreatedEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, AssayRunUpdatedFieldsEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, AutomationInputGeneratorCompletedV2BetaEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, AutomationOutputProcessorCompletedV2BetaEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, AutomationOutputProcessorUploadedV2BetaEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, AutomationInputGeneratorCompletedV2Event):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, AutomationOutputProcessorCompletedV2Event):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, AutomationOutputProcessorUploadedV2Event):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, AutomationTransformStatusPendingEventV2Event):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, AutomationTransformStatusRunningEventV2Event):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, AutomationTransformStatusSucceededEventV2Event):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, AutomationTransformStatusFailedEventV2Event):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, WorkflowTaskGroupCreatedEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, WorkflowTaskGroupMappingCompletedEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, WorkflowTaskCreatedEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, WorkflowTaskUpdatedFieldsEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, WorkflowTaskUpdatedStatusEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, WorkflowTaskUpdatedAssigneeEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, WorkflowTaskUpdatedScheduledOnEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, WorkflowTaskGroupUpdatedWatchersEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, WorkflowOutputCreatedEvent):
                    events_item = events_item_data.to_dict()

                elif isinstance(events_item_data, WorkflowOutputUpdatedFieldsEvent):
                    events_item = events_item_data.to_dict()

                else:
                    events_item = events_item_data.to_dict()

                events.append(events_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if events is not UNSET:
            field_dict["events"] = events
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_events() -> Union[
            Unset,
            List[
                Union[
                    EntityRegisteredEvent,
                    EntryCreatedEvent,
                    EntryUpdatedFieldsEvent,
                    EntryUpdatedReviewRecordEvent,
                    EntryUpdatedAssignedReviewersEvent,
                    EntryUpdatedReviewSnapshotBetaEvent,
                    StageEntryCreatedEvent,
                    StageEntryUpdatedFieldsEvent,
                    StageEntryUpdatedReviewRecordEvent,
                    StageEntryUpdatedAssignedReviewersEvent,
                    RequestCreatedEvent,
                    RequestUpdatedFieldsEvent,
                    AssayRunCreatedEvent,
                    AssayRunUpdatedFieldsEvent,
                    AutomationInputGeneratorCompletedV2BetaEvent,
                    AutomationOutputProcessorCompletedV2BetaEvent,
                    AutomationOutputProcessorUploadedV2BetaEvent,
                    AutomationInputGeneratorCompletedV2Event,
                    AutomationOutputProcessorCompletedV2Event,
                    AutomationOutputProcessorUploadedV2Event,
                    AutomationTransformStatusPendingEventV2Event,
                    AutomationTransformStatusRunningEventV2Event,
                    AutomationTransformStatusSucceededEventV2Event,
                    AutomationTransformStatusFailedEventV2Event,
                    WorkflowTaskGroupCreatedEvent,
                    WorkflowTaskGroupMappingCompletedEvent,
                    WorkflowTaskCreatedEvent,
                    WorkflowTaskUpdatedFieldsEvent,
                    WorkflowTaskUpdatedStatusEvent,
                    WorkflowTaskUpdatedAssigneeEvent,
                    WorkflowTaskUpdatedScheduledOnEvent,
                    WorkflowTaskGroupUpdatedWatchersEvent,
                    WorkflowOutputCreatedEvent,
                    WorkflowOutputUpdatedFieldsEvent,
                    WorksheetUpdatedReviewSnapshotBetaEvent,
                    UnknownType,
                ]
            ],
        ]:
            events = []
            _events = d.pop("events")
            for events_item_data in _events or []:

                def _parse_events_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[
                    EntityRegisteredEvent,
                    EntryCreatedEvent,
                    EntryUpdatedFieldsEvent,
                    EntryUpdatedReviewRecordEvent,
                    EntryUpdatedAssignedReviewersEvent,
                    EntryUpdatedReviewSnapshotBetaEvent,
                    StageEntryCreatedEvent,
                    StageEntryUpdatedFieldsEvent,
                    StageEntryUpdatedReviewRecordEvent,
                    StageEntryUpdatedAssignedReviewersEvent,
                    RequestCreatedEvent,
                    RequestUpdatedFieldsEvent,
                    AssayRunCreatedEvent,
                    AssayRunUpdatedFieldsEvent,
                    AutomationInputGeneratorCompletedV2BetaEvent,
                    AutomationOutputProcessorCompletedV2BetaEvent,
                    AutomationOutputProcessorUploadedV2BetaEvent,
                    AutomationInputGeneratorCompletedV2Event,
                    AutomationOutputProcessorCompletedV2Event,
                    AutomationOutputProcessorUploadedV2Event,
                    AutomationTransformStatusPendingEventV2Event,
                    AutomationTransformStatusRunningEventV2Event,
                    AutomationTransformStatusSucceededEventV2Event,
                    AutomationTransformStatusFailedEventV2Event,
                    WorkflowTaskGroupCreatedEvent,
                    WorkflowTaskGroupMappingCompletedEvent,
                    WorkflowTaskCreatedEvent,
                    WorkflowTaskUpdatedFieldsEvent,
                    WorkflowTaskUpdatedStatusEvent,
                    WorkflowTaskUpdatedAssigneeEvent,
                    WorkflowTaskUpdatedScheduledOnEvent,
                    WorkflowTaskGroupUpdatedWatchersEvent,
                    WorkflowOutputCreatedEvent,
                    WorkflowOutputUpdatedFieldsEvent,
                    WorksheetUpdatedReviewSnapshotBetaEvent,
                    UnknownType,
                ]:
                    events_item: Union[
                        EntityRegisteredEvent,
                        EntryCreatedEvent,
                        EntryUpdatedFieldsEvent,
                        EntryUpdatedReviewRecordEvent,
                        EntryUpdatedAssignedReviewersEvent,
                        EntryUpdatedReviewSnapshotBetaEvent,
                        StageEntryCreatedEvent,
                        StageEntryUpdatedFieldsEvent,
                        StageEntryUpdatedReviewRecordEvent,
                        StageEntryUpdatedAssignedReviewersEvent,
                        RequestCreatedEvent,
                        RequestUpdatedFieldsEvent,
                        AssayRunCreatedEvent,
                        AssayRunUpdatedFieldsEvent,
                        AutomationInputGeneratorCompletedV2BetaEvent,
                        AutomationOutputProcessorCompletedV2BetaEvent,
                        AutomationOutputProcessorUploadedV2BetaEvent,
                        AutomationInputGeneratorCompletedV2Event,
                        AutomationOutputProcessorCompletedV2Event,
                        AutomationOutputProcessorUploadedV2Event,
                        AutomationTransformStatusPendingEventV2Event,
                        AutomationTransformStatusRunningEventV2Event,
                        AutomationTransformStatusSucceededEventV2Event,
                        AutomationTransformStatusFailedEventV2Event,
                        WorkflowTaskGroupCreatedEvent,
                        WorkflowTaskGroupMappingCompletedEvent,
                        WorkflowTaskCreatedEvent,
                        WorkflowTaskUpdatedFieldsEvent,
                        WorkflowTaskUpdatedStatusEvent,
                        WorkflowTaskUpdatedAssigneeEvent,
                        WorkflowTaskUpdatedScheduledOnEvent,
                        WorkflowTaskGroupUpdatedWatchersEvent,
                        WorkflowOutputCreatedEvent,
                        WorkflowOutputUpdatedFieldsEvent,
                        WorksheetUpdatedReviewSnapshotBetaEvent,
                        UnknownType,
                    ]
                    discriminator_value: str = cast(str, data.get("eventType"))
                    if discriminator_value is not None:
                        event: Union[
                            EntityRegisteredEvent,
                            EntryCreatedEvent,
                            EntryUpdatedFieldsEvent,
                            EntryUpdatedReviewRecordEvent,
                            EntryUpdatedAssignedReviewersEvent,
                            EntryUpdatedReviewSnapshotBetaEvent,
                            StageEntryCreatedEvent,
                            StageEntryUpdatedFieldsEvent,
                            StageEntryUpdatedReviewRecordEvent,
                            StageEntryUpdatedAssignedReviewersEvent,
                            RequestCreatedEvent,
                            RequestUpdatedFieldsEvent,
                            AssayRunCreatedEvent,
                            AssayRunUpdatedFieldsEvent,
                            AutomationInputGeneratorCompletedV2BetaEvent,
                            AutomationOutputProcessorCompletedV2BetaEvent,
                            AutomationOutputProcessorUploadedV2BetaEvent,
                            AutomationInputGeneratorCompletedV2Event,
                            AutomationOutputProcessorCompletedV2Event,
                            AutomationOutputProcessorUploadedV2Event,
                            AutomationTransformStatusPendingEventV2Event,
                            AutomationTransformStatusRunningEventV2Event,
                            AutomationTransformStatusSucceededEventV2Event,
                            AutomationTransformStatusFailedEventV2Event,
                            WorkflowTaskGroupCreatedEvent,
                            WorkflowTaskGroupMappingCompletedEvent,
                            WorkflowTaskCreatedEvent,
                            WorkflowTaskUpdatedFieldsEvent,
                            WorkflowTaskUpdatedStatusEvent,
                            WorkflowTaskUpdatedAssigneeEvent,
                            WorkflowTaskUpdatedScheduledOnEvent,
                            WorkflowTaskGroupUpdatedWatchersEvent,
                            WorkflowOutputCreatedEvent,
                            WorkflowOutputUpdatedFieldsEvent,
                            WorksheetUpdatedReviewSnapshotBetaEvent,
                            UnknownType,
                        ]
                        if discriminator_value == "v2-alpha.stageEntry.created":
                            event = StageEntryCreatedEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2-alpha.stageEntry.updated.assignedReviewers":
                            event = StageEntryUpdatedAssignedReviewersEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2-beta.automationInputGenerator.completed":
                            event = AutomationInputGeneratorCompletedV2BetaEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2-beta.automationOutputProcessor.completed":
                            event = AutomationOutputProcessorCompletedV2BetaEvent.from_dict(
                                data, strict=False
                            )

                            return event
                        if discriminator_value == "v2-beta.automationOutputProcessor.uploaded":
                            event = AutomationOutputProcessorUploadedV2BetaEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2-beta.entry.updated.reviewSnapshot":
                            event = EntryUpdatedReviewSnapshotBetaEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2-beta.worksheet.updated.reviewSnapshot":
                            event = WorksheetUpdatedReviewSnapshotBetaEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.assayRun.created":
                            event = AssayRunCreatedEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.assayRun.updated.fields":
                            event = AssayRunUpdatedFieldsEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.automationFileTransform.updated.status.failed":
                            event = AutomationTransformStatusFailedEventV2Event.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.automationFileTransform.updated.status.pending":
                            event = AutomationTransformStatusPendingEventV2Event.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.automationFileTransform.updated.status.running":
                            event = AutomationTransformStatusRunningEventV2Event.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.automationFileTransform.updated.status.succeeded":
                            event = AutomationTransformStatusSucceededEventV2Event.from_dict(
                                data, strict=False
                            )

                            return event
                        if discriminator_value == "v2.automationInputGenerator.completed":
                            event = AutomationInputGeneratorCompletedV2Event.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.automationOutputProcessor.completed":
                            event = AutomationOutputProcessorCompletedV2Event.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.automationOutputProcessor.uploaded":
                            event = AutomationOutputProcessorUploadedV2Event.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.entity.registered":
                            event = EntityRegisteredEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.entry.created":
                            event = EntryCreatedEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.entry.updated.assignedReviewers":
                            event = EntryUpdatedAssignedReviewersEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.entry.updated.fields":
                            event = EntryUpdatedFieldsEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.entry.updated.reviewRecord":
                            event = EntryUpdatedReviewRecordEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.request.created":
                            event = RequestCreatedEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.request.updated.fields":
                            event = RequestUpdatedFieldsEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.workflowOutput.created":
                            event = WorkflowOutputCreatedEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.workflowOutput.updated.fields":
                            event = WorkflowOutputUpdatedFieldsEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.workflowTask.created":
                            event = WorkflowTaskCreatedEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.workflowTask.updated.assignee":
                            event = WorkflowTaskUpdatedAssigneeEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.workflowTask.updated.fields":
                            event = WorkflowTaskUpdatedFieldsEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.workflowTask.updated.scheduledOn":
                            event = WorkflowTaskUpdatedScheduledOnEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.workflowTask.updated.status":
                            event = WorkflowTaskUpdatedStatusEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.workflowTaskGroup.created":
                            event = WorkflowTaskGroupCreatedEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.workflowTaskGroup.mappingCompleted":
                            event = WorkflowTaskGroupMappingCompletedEvent.from_dict(data, strict=False)

                            return event
                        if discriminator_value == "v2.workflowTaskGroup.updated.watchers":
                            event = WorkflowTaskGroupUpdatedWatchersEvent.from_dict(data, strict=False)

                            return event

                        return UnknownType(value=data)
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = EntityRegisteredEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = EntryCreatedEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = EntryUpdatedFieldsEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = EntryUpdatedReviewRecordEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = EntryUpdatedAssignedReviewersEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = EntryUpdatedReviewSnapshotBetaEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = StageEntryCreatedEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = StageEntryUpdatedFieldsEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = StageEntryUpdatedReviewRecordEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = StageEntryUpdatedAssignedReviewersEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = RequestCreatedEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = RequestUpdatedFieldsEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = AssayRunCreatedEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = AssayRunUpdatedFieldsEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = AutomationInputGeneratorCompletedV2BetaEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = AutomationOutputProcessorCompletedV2BetaEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = AutomationOutputProcessorUploadedV2BetaEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = AutomationInputGeneratorCompletedV2Event.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = AutomationOutputProcessorCompletedV2Event.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = AutomationOutputProcessorUploadedV2Event.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = AutomationTransformStatusPendingEventV2Event.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = AutomationTransformStatusRunningEventV2Event.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = AutomationTransformStatusSucceededEventV2Event.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = AutomationTransformStatusFailedEventV2Event.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = WorkflowTaskGroupCreatedEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = WorkflowTaskGroupMappingCompletedEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = WorkflowTaskCreatedEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = WorkflowTaskUpdatedFieldsEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = WorkflowTaskUpdatedStatusEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = WorkflowTaskUpdatedAssigneeEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = WorkflowTaskUpdatedScheduledOnEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = WorkflowTaskGroupUpdatedWatchersEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = WorkflowOutputCreatedEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = WorkflowOutputUpdatedFieldsEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        event = WorksheetUpdatedReviewSnapshotBetaEvent.from_dict(data, strict=True)

                        return event
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                events_item = _parse_events_item(events_item_data)

                events.append(events_item)

            return events

        try:
            events = get_events()
        except KeyError:
            if strict:
                raise
            events = cast(
                Union[
                    Unset,
                    List[
                        Union[
                            EntityRegisteredEvent,
                            EntryCreatedEvent,
                            EntryUpdatedFieldsEvent,
                            EntryUpdatedReviewRecordEvent,
                            EntryUpdatedAssignedReviewersEvent,
                            EntryUpdatedReviewSnapshotBetaEvent,
                            StageEntryCreatedEvent,
                            StageEntryUpdatedFieldsEvent,
                            StageEntryUpdatedReviewRecordEvent,
                            StageEntryUpdatedAssignedReviewersEvent,
                            RequestCreatedEvent,
                            RequestUpdatedFieldsEvent,
                            AssayRunCreatedEvent,
                            AssayRunUpdatedFieldsEvent,
                            AutomationInputGeneratorCompletedV2BetaEvent,
                            AutomationOutputProcessorCompletedV2BetaEvent,
                            AutomationOutputProcessorUploadedV2BetaEvent,
                            AutomationInputGeneratorCompletedV2Event,
                            AutomationOutputProcessorCompletedV2Event,
                            AutomationOutputProcessorUploadedV2Event,
                            AutomationTransformStatusPendingEventV2Event,
                            AutomationTransformStatusRunningEventV2Event,
                            AutomationTransformStatusSucceededEventV2Event,
                            AutomationTransformStatusFailedEventV2Event,
                            WorkflowTaskGroupCreatedEvent,
                            WorkflowTaskGroupMappingCompletedEvent,
                            WorkflowTaskCreatedEvent,
                            WorkflowTaskUpdatedFieldsEvent,
                            WorkflowTaskUpdatedStatusEvent,
                            WorkflowTaskUpdatedAssigneeEvent,
                            WorkflowTaskUpdatedScheduledOnEvent,
                            WorkflowTaskGroupUpdatedWatchersEvent,
                            WorkflowOutputCreatedEvent,
                            WorkflowOutputUpdatedFieldsEvent,
                            WorksheetUpdatedReviewSnapshotBetaEvent,
                            UnknownType,
                        ]
                    ],
                ],
                UNSET,
            )

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        events_paginated_list = cls(
            events=events,
            next_token=next_token,
        )

        events_paginated_list.additional_properties = d
        return events_paginated_list

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def events(
        self,
    ) -> List[
        Union[
            EntityRegisteredEvent,
            EntryCreatedEvent,
            EntryUpdatedFieldsEvent,
            EntryUpdatedReviewRecordEvent,
            EntryUpdatedAssignedReviewersEvent,
            EntryUpdatedReviewSnapshotBetaEvent,
            StageEntryCreatedEvent,
            StageEntryUpdatedFieldsEvent,
            StageEntryUpdatedReviewRecordEvent,
            StageEntryUpdatedAssignedReviewersEvent,
            RequestCreatedEvent,
            RequestUpdatedFieldsEvent,
            AssayRunCreatedEvent,
            AssayRunUpdatedFieldsEvent,
            AutomationInputGeneratorCompletedV2BetaEvent,
            AutomationOutputProcessorCompletedV2BetaEvent,
            AutomationOutputProcessorUploadedV2BetaEvent,
            AutomationInputGeneratorCompletedV2Event,
            AutomationOutputProcessorCompletedV2Event,
            AutomationOutputProcessorUploadedV2Event,
            AutomationTransformStatusPendingEventV2Event,
            AutomationTransformStatusRunningEventV2Event,
            AutomationTransformStatusSucceededEventV2Event,
            AutomationTransformStatusFailedEventV2Event,
            WorkflowTaskGroupCreatedEvent,
            WorkflowTaskGroupMappingCompletedEvent,
            WorkflowTaskCreatedEvent,
            WorkflowTaskUpdatedFieldsEvent,
            WorkflowTaskUpdatedStatusEvent,
            WorkflowTaskUpdatedAssigneeEvent,
            WorkflowTaskUpdatedScheduledOnEvent,
            WorkflowTaskGroupUpdatedWatchersEvent,
            WorkflowOutputCreatedEvent,
            WorkflowOutputUpdatedFieldsEvent,
            WorksheetUpdatedReviewSnapshotBetaEvent,
            UnknownType,
        ]
    ]:
        if isinstance(self._events, Unset):
            raise NotPresentError(self, "events")
        return self._events

    @events.setter
    def events(
        self,
        value: List[
            Union[
                EntityRegisteredEvent,
                EntryCreatedEvent,
                EntryUpdatedFieldsEvent,
                EntryUpdatedReviewRecordEvent,
                EntryUpdatedAssignedReviewersEvent,
                EntryUpdatedReviewSnapshotBetaEvent,
                StageEntryCreatedEvent,
                StageEntryUpdatedFieldsEvent,
                StageEntryUpdatedReviewRecordEvent,
                StageEntryUpdatedAssignedReviewersEvent,
                RequestCreatedEvent,
                RequestUpdatedFieldsEvent,
                AssayRunCreatedEvent,
                AssayRunUpdatedFieldsEvent,
                AutomationInputGeneratorCompletedV2BetaEvent,
                AutomationOutputProcessorCompletedV2BetaEvent,
                AutomationOutputProcessorUploadedV2BetaEvent,
                AutomationInputGeneratorCompletedV2Event,
                AutomationOutputProcessorCompletedV2Event,
                AutomationOutputProcessorUploadedV2Event,
                AutomationTransformStatusPendingEventV2Event,
                AutomationTransformStatusRunningEventV2Event,
                AutomationTransformStatusSucceededEventV2Event,
                AutomationTransformStatusFailedEventV2Event,
                WorkflowTaskGroupCreatedEvent,
                WorkflowTaskGroupMappingCompletedEvent,
                WorkflowTaskCreatedEvent,
                WorkflowTaskUpdatedFieldsEvent,
                WorkflowTaskUpdatedStatusEvent,
                WorkflowTaskUpdatedAssigneeEvent,
                WorkflowTaskUpdatedScheduledOnEvent,
                WorkflowTaskGroupUpdatedWatchersEvent,
                WorkflowOutputCreatedEvent,
                WorkflowOutputUpdatedFieldsEvent,
                WorksheetUpdatedReviewSnapshotBetaEvent,
                UnknownType,
            ]
        ],
    ) -> None:
        self._events = value

    @events.deleter
    def events(self) -> None:
        self._events = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
