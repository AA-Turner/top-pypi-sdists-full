from typing import Union

from ..extensions import UnknownType
from ..models.app_activate_requested_webhook_v2 import AppActivateRequestedWebhookV2
from ..models.app_deactivated_webhook_v2 import AppDeactivatedWebhookV2
from ..models.app_installed_webhook_v2 import AppInstalledWebhookV2
from ..models.assay_run_created_webhook_v2 import AssayRunCreatedWebhookV2
from ..models.assay_run_updated_fields_webhook_v2 import AssayRunUpdatedFieldsWebhookV2
from ..models.automation_file_transform_failed_webhook_v2 import AutomationFileTransformFailedWebhookV2
from ..models.automation_file_transform_pending_webhook_v2 import AutomationFileTransformPendingWebhookV2
from ..models.automation_file_transform_running_webhook_v2 import AutomationFileTransformRunningWebhookV2
from ..models.automation_file_transform_succeeded_webhook_v2 import AutomationFileTransformSucceededWebhookV2
from ..models.canvas_created_webhook_v2 import CanvasCreatedWebhookV2
from ..models.canvas_created_webhook_v2_beta import CanvasCreatedWebhookV2Beta
from ..models.canvas_initialize_webhook_v2 import CanvasInitializeWebhookV2
from ..models.canvas_interaction_webhook_v2 import CanvasInteractionWebhookV2
from ..models.custom_entity_created_webhook_v3 import CustomEntityCreatedWebhookV3
from ..models.custom_entity_updated_webhook_v3 import CustomEntityUpdatedWebhookV3
from ..models.dna_oligo_created_webhook_v3 import DnaOligoCreatedWebhookV3
from ..models.dna_oligo_updated_webhook_v3 import DnaOligoUpdatedWebhookV3
from ..models.dna_sequence_created_webhook_v3 import DnaSequenceCreatedWebhookV3
from ..models.dna_sequence_updated_webhook_v3 import DnaSequenceUpdatedWebhookV3
from ..models.entity_registered_webhook_v2 import EntityRegisteredWebhookV2
from ..models.entry_created_webhook_v2 import EntryCreatedWebhookV2
from ..models.entry_created_webhook_v3 import EntryCreatedWebhookV3
from ..models.entry_updated_fields_webhook_v2 import EntryUpdatedFieldsWebhookV2
from ..models.entry_updated_review_record_webhook_v2 import EntryUpdatedReviewRecordWebhookV2
from ..models.lifecycle_activate_webhook_v0 import LifecycleActivateWebhookV0
from ..models.lifecycle_activate_webhook_v0_beta import LifecycleActivateWebhookV0Beta
from ..models.lifecycle_configuration_update_webhook_v0_beta import LifecycleConfigurationUpdateWebhookV0Beta
from ..models.lifecycle_configuration_update_webhook_v2_beta import LifecycleConfigurationUpdateWebhookV2Beta
from ..models.lifecycle_deactivate_webhook_v0 import LifecycleDeactivateWebhookV0
from ..models.lifecycle_deactivate_webhook_v0_beta import LifecycleDeactivateWebhookV0Beta
from ..models.project_created_webhook_v3 import ProjectCreatedWebhookV3
from ..models.project_updated_webhook_v3 import ProjectUpdatedWebhookV3
from ..models.request_created_webhook_v2 import RequestCreatedWebhookV2
from ..models.request_updated_fields_webhook_v2 import RequestUpdatedFieldsWebhookV2
from ..models.request_updated_status_webhook_v2 import RequestUpdatedStatusWebhookV2
from ..models.rna_oligo_created_webhook_v3 import RnaOligoCreatedWebhookV3
from ..models.rna_oligo_updated_webhook_v3 import RnaOligoUpdatedWebhookV3
from ..models.rna_sequence_created_webhook_v3 import RnaSequenceCreatedWebhookV3
from ..models.rna_sequence_updated_webhook_v3 import RnaSequenceUpdatedWebhookV3
from ..models.run_created_webhook_v3 import RunCreatedWebhookV3
from ..models.workflow_output_created_webhook_v2 import WorkflowOutputCreatedWebhookV2
from ..models.workflow_output_updated_fields_webhook_v2 import WorkflowOutputUpdatedFieldsWebhookV2
from ..models.workflow_task_created_webhook_v2 import WorkflowTaskCreatedWebhookV2
from ..models.workflow_task_group_created_webhook_v2 import WorkflowTaskGroupCreatedWebhookV2
from ..models.workflow_task_group_mapping_completed_webhook_v2 import (
    WorkflowTaskGroupMappingCompletedWebhookV2,
)
from ..models.workflow_task_group_updated_watchers_webhook_v2 import WorkflowTaskGroupUpdatedWatchersWebhookV2
from ..models.workflow_task_updated_assignee_webhook_v2 import WorkflowTaskUpdatedAssigneeWebhookV2
from ..models.workflow_task_updated_fields_webhook_v2 import WorkflowTaskUpdatedFieldsWebhookV2
from ..models.workflow_task_updated_scheduled_on_webhook_v2 import WorkflowTaskUpdatedScheduledOnWebhookV2
from ..models.workflow_task_updated_status_webhook_v2 import WorkflowTaskUpdatedStatusWebhookV2

WebhookMessageV0 = Union[
    LifecycleConfigurationUpdateWebhookV2Beta,
    CanvasInteractionWebhookV2,
    CanvasInitializeWebhookV2,
    CanvasCreatedWebhookV2,
    CanvasCreatedWebhookV2Beta,
    AutomationFileTransformRunningWebhookV2,
    AutomationFileTransformPendingWebhookV2,
    AutomationFileTransformSucceededWebhookV2,
    AutomationFileTransformFailedWebhookV2,
    AppActivateRequestedWebhookV2,
    AppDeactivatedWebhookV2,
    AppInstalledWebhookV2,
    AssayRunCreatedWebhookV2,
    AssayRunUpdatedFieldsWebhookV2,
    EntityRegisteredWebhookV2,
    EntryCreatedWebhookV2,
    EntryUpdatedFieldsWebhookV2,
    EntryUpdatedReviewRecordWebhookV2,
    RequestCreatedWebhookV2,
    RequestUpdatedFieldsWebhookV2,
    RequestUpdatedStatusWebhookV2,
    WorkflowTaskGroupCreatedWebhookV2,
    WorkflowTaskGroupMappingCompletedWebhookV2,
    WorkflowTaskGroupUpdatedWatchersWebhookV2,
    WorkflowTaskCreatedWebhookV2,
    WorkflowTaskUpdatedAssigneeWebhookV2,
    WorkflowTaskUpdatedScheduledOnWebhookV2,
    WorkflowTaskUpdatedStatusWebhookV2,
    WorkflowTaskUpdatedFieldsWebhookV2,
    WorkflowOutputCreatedWebhookV2,
    WorkflowOutputUpdatedFieldsWebhookV2,
    LifecycleActivateWebhookV0,
    LifecycleDeactivateWebhookV0,
    LifecycleActivateWebhookV0Beta,
    LifecycleDeactivateWebhookV0Beta,
    LifecycleConfigurationUpdateWebhookV0Beta,
    EntryCreatedWebhookV3,
    RunCreatedWebhookV3,
    ProjectCreatedWebhookV3,
    CustomEntityCreatedWebhookV3,
    DnaOligoCreatedWebhookV3,
    DnaSequenceCreatedWebhookV3,
    RnaOligoCreatedWebhookV3,
    RnaSequenceCreatedWebhookV3,
    ProjectUpdatedWebhookV3,
    CustomEntityUpdatedWebhookV3,
    DnaOligoUpdatedWebhookV3,
    DnaSequenceUpdatedWebhookV3,
    RnaOligoUpdatedWebhookV3,
    RnaSequenceUpdatedWebhookV3,
    UnknownType,
]
