from typing import Union

from ..extensions import UnknownType
from ..models.assay_run_created_event import AssayRunCreatedEvent
from ..models.assay_run_updated_fields_event import AssayRunUpdatedFieldsEvent
from ..models.automation_input_generator_completed_v2_beta_event import (
    AutomationInputGeneratorCompletedV2BetaEvent,
)
from ..models.automation_output_processor_completed_v2_beta_event import (
    AutomationOutputProcessorCompletedV2BetaEvent,
)
from ..models.automation_output_processor_uploaded_v2_beta_event import (
    AutomationOutputProcessorUploadedV2BetaEvent,
)
from ..models.entity_registered_event import EntityRegisteredEvent
from ..models.entry_created_event import EntryCreatedEvent
from ..models.entry_updated_fields_event import EntryUpdatedFieldsEvent
from ..models.entry_updated_review_record_event import EntryUpdatedReviewRecordEvent
from ..models.request_created_event import RequestCreatedEvent
from ..models.request_updated_fields_event import RequestUpdatedFieldsEvent
from ..models.stage_entry_created_event import StageEntryCreatedEvent
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

Event = Union[
    EntityRegisteredEvent,
    EntryCreatedEvent,
    EntryUpdatedFieldsEvent,
    EntryUpdatedReviewRecordEvent,
    StageEntryCreatedEvent,
    StageEntryUpdatedFieldsEvent,
    StageEntryUpdatedReviewRecordEvent,
    RequestCreatedEvent,
    RequestUpdatedFieldsEvent,
    AssayRunCreatedEvent,
    AssayRunUpdatedFieldsEvent,
    AutomationInputGeneratorCompletedV2BetaEvent,
    AutomationOutputProcessorCompletedV2BetaEvent,
    AutomationOutputProcessorUploadedV2BetaEvent,
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
    UnknownType,
]
