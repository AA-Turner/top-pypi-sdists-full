# Re-export benchling_sdk.models benchling_sdk such that
# users can import from benchling_sdk without exposing benchling_api_client.
#
# Do not write by hand. Run `poetry run task models` to generate.
# This file should be committed as part of source control.


import sys
from typing import TYPE_CHECKING

__all__ = [
    "AppActivateRequestedWebhookV2",
    "AppActivateRequestedWebhookV2Type",
    "AppDeactivatedWebhookV2",
    "AppDeactivatedWebhookV2Type",
    "AppInstalledWebhookV2",
    "AppInstalledWebhookV2Type",
    "AssayRunCreatedWebhookV2",
    "AssayRunCreatedWebhookV2Type",
    "AssayRunUpdatedFieldsWebhookV2",
    "AssayRunUpdatedFieldsWebhookV2Type",
    "AutomationFileTransformFailedWebhookV2",
    "AutomationFileTransformFailedWebhookV2Type",
    "AutomationFileTransformPendingWebhookV2",
    "AutomationFileTransformPendingWebhookV2Type",
    "AutomationFileTransformRunningWebhookV2",
    "AutomationFileTransformRunningWebhookV2Type",
    "AutomationFileTransformSucceededWebhookV2",
    "AutomationFileTransformSucceededWebhookV2Type",
    "CanvasCreatedWebhookV2",
    "CanvasCreatedWebhookV2Beta",
    "CanvasCreatedWebhookV2BetaType",
    "CanvasCreatedWebhookV2Type",
    "CanvasInitializeWebhookV2",
    "CanvasInitializeWebhookV2Type",
    "CanvasInteractionWebhookV2",
    "CanvasInteractionWebhookV2Type",
    "CustomEntityCreatedWebhookV3",
    "CustomEntityCreatedWebhookV3Type",
    "CustomEntityUpdatedWebhookV3",
    "CustomEntityUpdatedWebhookV3Type",
    "DnaOligoCreatedWebhookV3",
    "DnaOligoCreatedWebhookV3Type",
    "DnaOligoUpdatedWebhookV3",
    "DnaOligoUpdatedWebhookV3Type",
    "DnaSequenceCreatedWebhookV3",
    "DnaSequenceCreatedWebhookV3Type",
    "DnaSequenceUpdatedWebhookV3",
    "DnaSequenceUpdatedWebhookV3Type",
    "EntityRegisteredWebhookV2",
    "EntityRegisteredWebhookV2Type",
    "EntryCreatedWebhookV2",
    "EntryCreatedWebhookV2Type",
    "EntryCreatedWebhookV3",
    "EntryCreatedWebhookV3Type",
    "EntryUpdatedFieldsWebhookV2",
    "EntryUpdatedFieldsWebhookV2Type",
    "EntryUpdatedReviewRecordWebhookV2",
    "EntryUpdatedReviewRecordWebhookV2Type",
    "EventBaseWebhookV2",
    "EventBaseWebhookV2Schematized",
    "EventResourceSchema",
    "LifecycleActivateWebhookV0",
    "LifecycleActivateWebhookV0Beta",
    "LifecycleActivateWebhookV0BetaType",
    "LifecycleActivateWebhookV0Type",
    "LifecycleConfigurationUpdateWebhookV0Beta",
    "LifecycleConfigurationUpdateWebhookV0BetaType",
    "LifecycleConfigurationUpdateWebhookV2Beta",
    "LifecycleConfigurationUpdateWebhookV2BetaType",
    "LifecycleDeactivateWebhookV0",
    "LifecycleDeactivateWebhookV0Beta",
    "LifecycleDeactivateWebhookV0BetaType",
    "LifecycleDeactivateWebhookV0Type",
    "MessageBase",
    "MessageBaseV0",
    "ProjectCreatedWebhookV3",
    "ProjectCreatedWebhookV3Type",
    "ProjectUpdatedWebhookV3",
    "ProjectUpdatedWebhookV3Type",
    "RequestCreatedWebhookV2",
    "RequestCreatedWebhookV2Type",
    "RequestUpdatedFieldsWebhookV2",
    "RequestUpdatedFieldsWebhookV2Type",
    "RequestUpdatedStatusWebhookV2",
    "RequestUpdatedStatusWebhookV2Type",
    "RnaOligoCreatedWebhookV3",
    "RnaOligoCreatedWebhookV3Type",
    "RnaOligoUpdatedWebhookV3",
    "RnaOligoUpdatedWebhookV3Type",
    "RnaSequenceCreatedWebhookV3",
    "RnaSequenceCreatedWebhookV3Type",
    "RnaSequenceUpdatedWebhookV3",
    "RnaSequenceUpdatedWebhookV3Type",
    "RunCreatedWebhookV3",
    "RunCreatedWebhookV3Type",
    "UpdateEventBaseWebhookV2",
    "UpdateEventBaseWebhookV2Schematized",
    "V2AssayRunCreatedEvent",
    "V2AssayRunCreatedEventEventType",
    "V2AssayRunUpdatedFieldsEvent",
    "V2AssayRunUpdatedFieldsEventEventType",
    "V2EntityRegisteredEvent",
    "V2EntityRegisteredEventEventType",
    "V2EntryCreatedEvent",
    "V2EntryCreatedEventEventType",
    "V2EntryUpdatedFieldsEvent",
    "V2EntryUpdatedFieldsEventEventType",
    "V2EntryUpdatedReviewRecordEvent",
    "V2EntryUpdatedReviewRecordEventEventType",
    "V2RequestCreatedEvent",
    "V2RequestCreatedEventEventType",
    "V2RequestUpdatedFieldsEvent",
    "V2RequestUpdatedFieldsEventEventType",
    "V2RequestUpdatedStatusEvent",
    "V2RequestUpdatedStatusEventEventType",
    "V2WorkflowOutputCreatedEvent",
    "V2WorkflowOutputCreatedEventEventType",
    "V2WorkflowOutputUpdatedFieldsEvent",
    "V2WorkflowOutputUpdatedFieldsEventEventType",
    "V2WorkflowTaskCreatedEvent",
    "V2WorkflowTaskCreatedEventEventType",
    "V2WorkflowTaskGroupCreatedEvent",
    "V2WorkflowTaskGroupCreatedEventEventType",
    "V2WorkflowTaskGroupUpdatedWatchersEvent",
    "V2WorkflowTaskGroupUpdatedWatchersEventEventType",
    "V2WorkflowTaskUpdatedAssigneeEvent",
    "V2WorkflowTaskUpdatedAssigneeEventEventType",
    "V2WorkflowTaskUpdatedFieldsEvent",
    "V2WorkflowTaskUpdatedFieldsEventEventType",
    "V2WorkflowTaskUpdatedScheduledOnEvent",
    "V2WorkflowTaskUpdatedScheduledOnEventEventType",
    "V2WorkflowTaskUpdatedStatusEvent",
    "V2WorkflowTaskUpdatedStatusEventEventType",
    "V3EventBase",
    "V3EventBaseStability",
    "V3UpdateEventBase",
    "WebhookEnvelopeV0",
    "WebhookEnvelopeV0App",
    "WebhookEnvelopeV0AppDefinition",
    "WebhookEnvelopeV0Version",
    "WebhookMessageV0",
    "WorkflowOutputCreatedWebhookV2",
    "WorkflowOutputCreatedWebhookV2Type",
    "WorkflowOutputUpdatedFieldsWebhookV2",
    "WorkflowOutputUpdatedFieldsWebhookV2Type",
    "WorkflowTaskCreatedWebhookV2",
    "WorkflowTaskCreatedWebhookV2Type",
    "WorkflowTaskGroupCreatedWebhookV2",
    "WorkflowTaskGroupCreatedWebhookV2Type",
    "WorkflowTaskGroupMappingCompletedWebhookV2",
    "WorkflowTaskGroupMappingCompletedWebhookV2Type",
    "WorkflowTaskGroupUpdatedWatchersWebhookV2",
    "WorkflowTaskGroupUpdatedWatchersWebhookV2Type",
    "WorkflowTaskUpdatedAssigneeWebhookV2",
    "WorkflowTaskUpdatedAssigneeWebhookV2Type",
    "WorkflowTaskUpdatedFieldsWebhookV2",
    "WorkflowTaskUpdatedFieldsWebhookV2Type",
    "WorkflowTaskUpdatedScheduledOnWebhookV2",
    "WorkflowTaskUpdatedScheduledOnWebhookV2Type",
    "WorkflowTaskUpdatedStatusWebhookV2",
    "WorkflowTaskUpdatedStatusWebhookV2Type",
]

if TYPE_CHECKING:
    import benchling_api_client.webhooks.v0.stable.models.app_activate_requested_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.app_activate_requested_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.app_deactivated_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.app_deactivated_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.app_installed_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.app_installed_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.assay_run_created_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.assay_run_created_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.assay_run_updated_fields_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.assay_run_updated_fields_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.automation_file_transform_failed_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.automation_file_transform_failed_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.automation_file_transform_pending_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.automation_file_transform_pending_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.automation_file_transform_running_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.automation_file_transform_running_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.automation_file_transform_succeeded_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.automation_file_transform_succeeded_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.canvas_created_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.canvas_created_webhook_v2_beta
    import benchling_api_client.webhooks.v0.stable.models.canvas_created_webhook_v2_beta_type
    import benchling_api_client.webhooks.v0.stable.models.canvas_created_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.custom_entity_created_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.custom_entity_created_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.custom_entity_updated_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.custom_entity_updated_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.dna_oligo_created_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.dna_oligo_created_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.dna_oligo_updated_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.dna_oligo_updated_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.dna_sequence_created_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.dna_sequence_created_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.dna_sequence_updated_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.dna_sequence_updated_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.entity_registered_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.entity_registered_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.entry_created_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.entry_created_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.entry_created_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.entry_created_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.entry_updated_fields_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.entry_updated_fields_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.entry_updated_review_record_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.entry_updated_review_record_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.event_base_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.event_base_webhook_v2_schematized
    import benchling_api_client.webhooks.v0.stable.models.event_resource_schema
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0_beta
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0_beta_type
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0_type
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_configuration_update_webhook_v0_beta
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_configuration_update_webhook_v0_beta_type
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_configuration_update_webhook_v2_beta
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_configuration_update_webhook_v2_beta_type
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0_beta
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0_beta_type
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0_type
    import benchling_api_client.webhooks.v0.stable.models.message_base
    import benchling_api_client.webhooks.v0.stable.models.message_base_v0
    import benchling_api_client.webhooks.v0.stable.models.project_created_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.project_created_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.project_updated_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.project_updated_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.request_created_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.request_created_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.request_updated_fields_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.request_updated_fields_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.request_updated_status_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.request_updated_status_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.rna_oligo_created_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.rna_oligo_created_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.rna_oligo_updated_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.rna_oligo_updated_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.rna_sequence_created_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.rna_sequence_created_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.rna_sequence_updated_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.rna_sequence_updated_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.run_created_webhook_v3
    import benchling_api_client.webhooks.v0.stable.models.run_created_webhook_v3_type
    import benchling_api_client.webhooks.v0.stable.models.update_event_base_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.update_event_base_webhook_v2_schematized
    import benchling_api_client.webhooks.v0.stable.models.v2_assay_run_created_event
    import benchling_api_client.webhooks.v0.stable.models.v2_assay_run_created_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_assay_run_updated_fields_event
    import benchling_api_client.webhooks.v0.stable.models.v2_assay_run_updated_fields_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_entity_registered_event
    import benchling_api_client.webhooks.v0.stable.models.v2_entity_registered_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_entry_created_event
    import benchling_api_client.webhooks.v0.stable.models.v2_entry_created_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_entry_updated_fields_event
    import benchling_api_client.webhooks.v0.stable.models.v2_entry_updated_fields_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_entry_updated_review_record_event
    import benchling_api_client.webhooks.v0.stable.models.v2_entry_updated_review_record_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_request_created_event
    import benchling_api_client.webhooks.v0.stable.models.v2_request_created_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_request_updated_fields_event
    import benchling_api_client.webhooks.v0.stable.models.v2_request_updated_fields_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_request_updated_status_event
    import benchling_api_client.webhooks.v0.stable.models.v2_request_updated_status_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_output_created_event
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_output_created_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_output_updated_fields_event
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_output_updated_fields_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_created_event
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_created_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_group_created_event
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_group_created_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_group_updated_watchers_event
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_group_updated_watchers_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_assignee_event
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_assignee_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_fields_event
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_fields_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_scheduled_on_event
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_scheduled_on_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_status_event
    import benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_status_event_event_type
    import benchling_api_client.webhooks.v0.stable.models.v3_event_base
    import benchling_api_client.webhooks.v0.stable.models.v3_event_base_stability
    import benchling_api_client.webhooks.v0.stable.models.v3_update_event_base
    import benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0
    import benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_app
    import benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_app_definition
    import benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_version
    import benchling_api_client.webhooks.v0.stable.models.webhook_message_v0
    import benchling_api_client.webhooks.v0.stable.models.workflow_output_created_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.workflow_output_created_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.workflow_output_updated_fields_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.workflow_output_updated_fields_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_created_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_created_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_group_created_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_group_created_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_group_mapping_completed_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_group_mapping_completed_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_group_updated_watchers_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_group_updated_watchers_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_assignee_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_assignee_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_fields_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_fields_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_scheduled_on_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_scheduled_on_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_status_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_status_webhook_v2_type

    AppActivateRequestedWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.app_activate_requested_webhook_v2.AppActivateRequestedWebhookV2
    )
    AppActivateRequestedWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.app_activate_requested_webhook_v2_type.AppActivateRequestedWebhookV2Type
    )
    AppDeactivatedWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.app_deactivated_webhook_v2.AppDeactivatedWebhookV2
    )
    AppDeactivatedWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.app_deactivated_webhook_v2_type.AppDeactivatedWebhookV2Type
    )
    AppInstalledWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.app_installed_webhook_v2.AppInstalledWebhookV2
    )
    AppInstalledWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.app_installed_webhook_v2_type.AppInstalledWebhookV2Type
    )
    AssayRunCreatedWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.assay_run_created_webhook_v2.AssayRunCreatedWebhookV2
    )
    AssayRunCreatedWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.assay_run_created_webhook_v2_type.AssayRunCreatedWebhookV2Type
    )
    AssayRunUpdatedFieldsWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.assay_run_updated_fields_webhook_v2.AssayRunUpdatedFieldsWebhookV2
    )
    AssayRunUpdatedFieldsWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.assay_run_updated_fields_webhook_v2_type.AssayRunUpdatedFieldsWebhookV2Type
    )
    AutomationFileTransformFailedWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.automation_file_transform_failed_webhook_v2.AutomationFileTransformFailedWebhookV2
    )
    AutomationFileTransformFailedWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.automation_file_transform_failed_webhook_v2_type.AutomationFileTransformFailedWebhookV2Type
    )
    AutomationFileTransformPendingWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.automation_file_transform_pending_webhook_v2.AutomationFileTransformPendingWebhookV2
    )
    AutomationFileTransformPendingWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.automation_file_transform_pending_webhook_v2_type.AutomationFileTransformPendingWebhookV2Type
    )
    AutomationFileTransformRunningWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.automation_file_transform_running_webhook_v2.AutomationFileTransformRunningWebhookV2
    )
    AutomationFileTransformRunningWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.automation_file_transform_running_webhook_v2_type.AutomationFileTransformRunningWebhookV2Type
    )
    AutomationFileTransformSucceededWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.automation_file_transform_succeeded_webhook_v2.AutomationFileTransformSucceededWebhookV2
    )
    AutomationFileTransformSucceededWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.automation_file_transform_succeeded_webhook_v2_type.AutomationFileTransformSucceededWebhookV2Type
    )
    CanvasCreatedWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.canvas_created_webhook_v2.CanvasCreatedWebhookV2
    )
    CanvasCreatedWebhookV2Beta = (
        benchling_api_client.webhooks.v0.stable.models.canvas_created_webhook_v2_beta.CanvasCreatedWebhookV2Beta
    )
    CanvasCreatedWebhookV2BetaType = (
        benchling_api_client.webhooks.v0.stable.models.canvas_created_webhook_v2_beta_type.CanvasCreatedWebhookV2BetaType
    )
    CanvasCreatedWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.canvas_created_webhook_v2_type.CanvasCreatedWebhookV2Type
    )
    CanvasInitializeWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v2.CanvasInitializeWebhookV2
    )
    CanvasInitializeWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v2_type.CanvasInitializeWebhookV2Type
    )
    CanvasInteractionWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v2.CanvasInteractionWebhookV2
    )
    CanvasInteractionWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v2_type.CanvasInteractionWebhookV2Type
    )
    CustomEntityCreatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.custom_entity_created_webhook_v3.CustomEntityCreatedWebhookV3
    )
    CustomEntityCreatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.custom_entity_created_webhook_v3_type.CustomEntityCreatedWebhookV3Type
    )
    CustomEntityUpdatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.custom_entity_updated_webhook_v3.CustomEntityUpdatedWebhookV3
    )
    CustomEntityUpdatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.custom_entity_updated_webhook_v3_type.CustomEntityUpdatedWebhookV3Type
    )
    DnaOligoCreatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.dna_oligo_created_webhook_v3.DnaOligoCreatedWebhookV3
    )
    DnaOligoCreatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.dna_oligo_created_webhook_v3_type.DnaOligoCreatedWebhookV3Type
    )
    DnaOligoUpdatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.dna_oligo_updated_webhook_v3.DnaOligoUpdatedWebhookV3
    )
    DnaOligoUpdatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.dna_oligo_updated_webhook_v3_type.DnaOligoUpdatedWebhookV3Type
    )
    DnaSequenceCreatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.dna_sequence_created_webhook_v3.DnaSequenceCreatedWebhookV3
    )
    DnaSequenceCreatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.dna_sequence_created_webhook_v3_type.DnaSequenceCreatedWebhookV3Type
    )
    DnaSequenceUpdatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.dna_sequence_updated_webhook_v3.DnaSequenceUpdatedWebhookV3
    )
    DnaSequenceUpdatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.dna_sequence_updated_webhook_v3_type.DnaSequenceUpdatedWebhookV3Type
    )
    EntityRegisteredWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.entity_registered_webhook_v2.EntityRegisteredWebhookV2
    )
    EntityRegisteredWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.entity_registered_webhook_v2_type.EntityRegisteredWebhookV2Type
    )
    EntryCreatedWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.entry_created_webhook_v2.EntryCreatedWebhookV2
    )
    EntryCreatedWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.entry_created_webhook_v2_type.EntryCreatedWebhookV2Type
    )
    EntryCreatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.entry_created_webhook_v3.EntryCreatedWebhookV3
    )
    EntryCreatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.entry_created_webhook_v3_type.EntryCreatedWebhookV3Type
    )
    EntryUpdatedFieldsWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.entry_updated_fields_webhook_v2.EntryUpdatedFieldsWebhookV2
    )
    EntryUpdatedFieldsWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.entry_updated_fields_webhook_v2_type.EntryUpdatedFieldsWebhookV2Type
    )
    EntryUpdatedReviewRecordWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.entry_updated_review_record_webhook_v2.EntryUpdatedReviewRecordWebhookV2
    )
    EntryUpdatedReviewRecordWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.entry_updated_review_record_webhook_v2_type.EntryUpdatedReviewRecordWebhookV2Type
    )
    EventBaseWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.event_base_webhook_v2.EventBaseWebhookV2
    )
    EventBaseWebhookV2Schematized = (
        benchling_api_client.webhooks.v0.stable.models.event_base_webhook_v2_schematized.EventBaseWebhookV2Schematized
    )
    EventResourceSchema = (
        benchling_api_client.webhooks.v0.stable.models.event_resource_schema.EventResourceSchema
    )
    LifecycleActivateWebhookV0 = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0.LifecycleActivateWebhookV0
    )
    LifecycleActivateWebhookV0Beta = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0_beta.LifecycleActivateWebhookV0Beta
    )
    LifecycleActivateWebhookV0BetaType = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0_beta_type.LifecycleActivateWebhookV0BetaType
    )
    LifecycleActivateWebhookV0Type = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0_type.LifecycleActivateWebhookV0Type
    )
    LifecycleConfigurationUpdateWebhookV0Beta = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_configuration_update_webhook_v0_beta.LifecycleConfigurationUpdateWebhookV0Beta
    )
    LifecycleConfigurationUpdateWebhookV0BetaType = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_configuration_update_webhook_v0_beta_type.LifecycleConfigurationUpdateWebhookV0BetaType
    )
    LifecycleConfigurationUpdateWebhookV2Beta = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_configuration_update_webhook_v2_beta.LifecycleConfigurationUpdateWebhookV2Beta
    )
    LifecycleConfigurationUpdateWebhookV2BetaType = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_configuration_update_webhook_v2_beta_type.LifecycleConfigurationUpdateWebhookV2BetaType
    )
    LifecycleDeactivateWebhookV0 = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0.LifecycleDeactivateWebhookV0
    )
    LifecycleDeactivateWebhookV0Beta = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0_beta.LifecycleDeactivateWebhookV0Beta
    )
    LifecycleDeactivateWebhookV0BetaType = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0_beta_type.LifecycleDeactivateWebhookV0BetaType
    )
    LifecycleDeactivateWebhookV0Type = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0_type.LifecycleDeactivateWebhookV0Type
    )
    MessageBase = (
        benchling_api_client.webhooks.v0.stable.models.message_base.MessageBase
    )
    MessageBaseV0 = (
        benchling_api_client.webhooks.v0.stable.models.message_base_v0.MessageBaseV0
    )
    ProjectCreatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.project_created_webhook_v3.ProjectCreatedWebhookV3
    )
    ProjectCreatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.project_created_webhook_v3_type.ProjectCreatedWebhookV3Type
    )
    ProjectUpdatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.project_updated_webhook_v3.ProjectUpdatedWebhookV3
    )
    ProjectUpdatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.project_updated_webhook_v3_type.ProjectUpdatedWebhookV3Type
    )
    RequestCreatedWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.request_created_webhook_v2.RequestCreatedWebhookV2
    )
    RequestCreatedWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.request_created_webhook_v2_type.RequestCreatedWebhookV2Type
    )
    RequestUpdatedFieldsWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.request_updated_fields_webhook_v2.RequestUpdatedFieldsWebhookV2
    )
    RequestUpdatedFieldsWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.request_updated_fields_webhook_v2_type.RequestUpdatedFieldsWebhookV2Type
    )
    RequestUpdatedStatusWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.request_updated_status_webhook_v2.RequestUpdatedStatusWebhookV2
    )
    RequestUpdatedStatusWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.request_updated_status_webhook_v2_type.RequestUpdatedStatusWebhookV2Type
    )
    RnaOligoCreatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.rna_oligo_created_webhook_v3.RnaOligoCreatedWebhookV3
    )
    RnaOligoCreatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.rna_oligo_created_webhook_v3_type.RnaOligoCreatedWebhookV3Type
    )
    RnaOligoUpdatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.rna_oligo_updated_webhook_v3.RnaOligoUpdatedWebhookV3
    )
    RnaOligoUpdatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.rna_oligo_updated_webhook_v3_type.RnaOligoUpdatedWebhookV3Type
    )
    RnaSequenceCreatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.rna_sequence_created_webhook_v3.RnaSequenceCreatedWebhookV3
    )
    RnaSequenceCreatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.rna_sequence_created_webhook_v3_type.RnaSequenceCreatedWebhookV3Type
    )
    RnaSequenceUpdatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.rna_sequence_updated_webhook_v3.RnaSequenceUpdatedWebhookV3
    )
    RnaSequenceUpdatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.rna_sequence_updated_webhook_v3_type.RnaSequenceUpdatedWebhookV3Type
    )
    RunCreatedWebhookV3 = (
        benchling_api_client.webhooks.v0.stable.models.run_created_webhook_v3.RunCreatedWebhookV3
    )
    RunCreatedWebhookV3Type = (
        benchling_api_client.webhooks.v0.stable.models.run_created_webhook_v3_type.RunCreatedWebhookV3Type
    )
    UpdateEventBaseWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.update_event_base_webhook_v2.UpdateEventBaseWebhookV2
    )
    UpdateEventBaseWebhookV2Schematized = (
        benchling_api_client.webhooks.v0.stable.models.update_event_base_webhook_v2_schematized.UpdateEventBaseWebhookV2Schematized
    )
    V2AssayRunCreatedEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_assay_run_created_event.V2AssayRunCreatedEvent
    )
    V2AssayRunCreatedEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_assay_run_created_event_event_type.V2AssayRunCreatedEventEventType
    )
    V2AssayRunUpdatedFieldsEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_assay_run_updated_fields_event.V2AssayRunUpdatedFieldsEvent
    )
    V2AssayRunUpdatedFieldsEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_assay_run_updated_fields_event_event_type.V2AssayRunUpdatedFieldsEventEventType
    )
    V2EntityRegisteredEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_entity_registered_event.V2EntityRegisteredEvent
    )
    V2EntityRegisteredEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_entity_registered_event_event_type.V2EntityRegisteredEventEventType
    )
    V2EntryCreatedEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_entry_created_event.V2EntryCreatedEvent
    )
    V2EntryCreatedEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_entry_created_event_event_type.V2EntryCreatedEventEventType
    )
    V2EntryUpdatedFieldsEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_entry_updated_fields_event.V2EntryUpdatedFieldsEvent
    )
    V2EntryUpdatedFieldsEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_entry_updated_fields_event_event_type.V2EntryUpdatedFieldsEventEventType
    )
    V2EntryUpdatedReviewRecordEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_entry_updated_review_record_event.V2EntryUpdatedReviewRecordEvent
    )
    V2EntryUpdatedReviewRecordEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_entry_updated_review_record_event_event_type.V2EntryUpdatedReviewRecordEventEventType
    )
    V2RequestCreatedEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_request_created_event.V2RequestCreatedEvent
    )
    V2RequestCreatedEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_request_created_event_event_type.V2RequestCreatedEventEventType
    )
    V2RequestUpdatedFieldsEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_request_updated_fields_event.V2RequestUpdatedFieldsEvent
    )
    V2RequestUpdatedFieldsEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_request_updated_fields_event_event_type.V2RequestUpdatedFieldsEventEventType
    )
    V2RequestUpdatedStatusEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_request_updated_status_event.V2RequestUpdatedStatusEvent
    )
    V2RequestUpdatedStatusEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_request_updated_status_event_event_type.V2RequestUpdatedStatusEventEventType
    )
    V2WorkflowOutputCreatedEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_output_created_event.V2WorkflowOutputCreatedEvent
    )
    V2WorkflowOutputCreatedEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_output_created_event_event_type.V2WorkflowOutputCreatedEventEventType
    )
    V2WorkflowOutputUpdatedFieldsEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_output_updated_fields_event.V2WorkflowOutputUpdatedFieldsEvent
    )
    V2WorkflowOutputUpdatedFieldsEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_output_updated_fields_event_event_type.V2WorkflowOutputUpdatedFieldsEventEventType
    )
    V2WorkflowTaskCreatedEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_created_event.V2WorkflowTaskCreatedEvent
    )
    V2WorkflowTaskCreatedEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_created_event_event_type.V2WorkflowTaskCreatedEventEventType
    )
    V2WorkflowTaskGroupCreatedEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_group_created_event.V2WorkflowTaskGroupCreatedEvent
    )
    V2WorkflowTaskGroupCreatedEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_group_created_event_event_type.V2WorkflowTaskGroupCreatedEventEventType
    )
    V2WorkflowTaskGroupUpdatedWatchersEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_group_updated_watchers_event.V2WorkflowTaskGroupUpdatedWatchersEvent
    )
    V2WorkflowTaskGroupUpdatedWatchersEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_group_updated_watchers_event_event_type.V2WorkflowTaskGroupUpdatedWatchersEventEventType
    )
    V2WorkflowTaskUpdatedAssigneeEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_assignee_event.V2WorkflowTaskUpdatedAssigneeEvent
    )
    V2WorkflowTaskUpdatedAssigneeEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_assignee_event_event_type.V2WorkflowTaskUpdatedAssigneeEventEventType
    )
    V2WorkflowTaskUpdatedFieldsEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_fields_event.V2WorkflowTaskUpdatedFieldsEvent
    )
    V2WorkflowTaskUpdatedFieldsEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_fields_event_event_type.V2WorkflowTaskUpdatedFieldsEventEventType
    )
    V2WorkflowTaskUpdatedScheduledOnEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_scheduled_on_event.V2WorkflowTaskUpdatedScheduledOnEvent
    )
    V2WorkflowTaskUpdatedScheduledOnEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_scheduled_on_event_event_type.V2WorkflowTaskUpdatedScheduledOnEventEventType
    )
    V2WorkflowTaskUpdatedStatusEvent = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_status_event.V2WorkflowTaskUpdatedStatusEvent
    )
    V2WorkflowTaskUpdatedStatusEventEventType = (
        benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_status_event_event_type.V2WorkflowTaskUpdatedStatusEventEventType
    )
    V3EventBase = (
        benchling_api_client.webhooks.v0.stable.models.v3_event_base.V3EventBase
    )
    V3EventBaseStability = (
        benchling_api_client.webhooks.v0.stable.models.v3_event_base_stability.V3EventBaseStability
    )
    V3UpdateEventBase = (
        benchling_api_client.webhooks.v0.stable.models.v3_update_event_base.V3UpdateEventBase
    )
    WebhookEnvelopeV0 = (
        benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0.WebhookEnvelopeV0
    )
    WebhookEnvelopeV0App = (
        benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_app.WebhookEnvelopeV0App
    )
    WebhookEnvelopeV0AppDefinition = (
        benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_app_definition.WebhookEnvelopeV0AppDefinition
    )
    WebhookEnvelopeV0Version = (
        benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_version.WebhookEnvelopeV0Version
    )
    WebhookMessageV0 = (
        benchling_api_client.webhooks.v0.stable.models.webhook_message_v0.WebhookMessageV0
    )
    WorkflowOutputCreatedWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.workflow_output_created_webhook_v2.WorkflowOutputCreatedWebhookV2
    )
    WorkflowOutputCreatedWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.workflow_output_created_webhook_v2_type.WorkflowOutputCreatedWebhookV2Type
    )
    WorkflowOutputUpdatedFieldsWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.workflow_output_updated_fields_webhook_v2.WorkflowOutputUpdatedFieldsWebhookV2
    )
    WorkflowOutputUpdatedFieldsWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.workflow_output_updated_fields_webhook_v2_type.WorkflowOutputUpdatedFieldsWebhookV2Type
    )
    WorkflowTaskCreatedWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_created_webhook_v2.WorkflowTaskCreatedWebhookV2
    )
    WorkflowTaskCreatedWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_created_webhook_v2_type.WorkflowTaskCreatedWebhookV2Type
    )
    WorkflowTaskGroupCreatedWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_group_created_webhook_v2.WorkflowTaskGroupCreatedWebhookV2
    )
    WorkflowTaskGroupCreatedWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_group_created_webhook_v2_type.WorkflowTaskGroupCreatedWebhookV2Type
    )
    WorkflowTaskGroupMappingCompletedWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_group_mapping_completed_webhook_v2.WorkflowTaskGroupMappingCompletedWebhookV2
    )
    WorkflowTaskGroupMappingCompletedWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_group_mapping_completed_webhook_v2_type.WorkflowTaskGroupMappingCompletedWebhookV2Type
    )
    WorkflowTaskGroupUpdatedWatchersWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_group_updated_watchers_webhook_v2.WorkflowTaskGroupUpdatedWatchersWebhookV2
    )
    WorkflowTaskGroupUpdatedWatchersWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_group_updated_watchers_webhook_v2_type.WorkflowTaskGroupUpdatedWatchersWebhookV2Type
    )
    WorkflowTaskUpdatedAssigneeWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_assignee_webhook_v2.WorkflowTaskUpdatedAssigneeWebhookV2
    )
    WorkflowTaskUpdatedAssigneeWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_assignee_webhook_v2_type.WorkflowTaskUpdatedAssigneeWebhookV2Type
    )
    WorkflowTaskUpdatedFieldsWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_fields_webhook_v2.WorkflowTaskUpdatedFieldsWebhookV2
    )
    WorkflowTaskUpdatedFieldsWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_fields_webhook_v2_type.WorkflowTaskUpdatedFieldsWebhookV2Type
    )
    WorkflowTaskUpdatedScheduledOnWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_scheduled_on_webhook_v2.WorkflowTaskUpdatedScheduledOnWebhookV2
    )
    WorkflowTaskUpdatedScheduledOnWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_scheduled_on_webhook_v2_type.WorkflowTaskUpdatedScheduledOnWebhookV2Type
    )
    WorkflowTaskUpdatedStatusWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_status_webhook_v2.WorkflowTaskUpdatedStatusWebhookV2
    )
    WorkflowTaskUpdatedStatusWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_status_webhook_v2_type.WorkflowTaskUpdatedStatusWebhookV2Type
    )

else:
    model_to_module_mapping = {
        "AppActivateRequestedWebhookV2": "benchling_api_client.webhooks.v0.stable.models.app_activate_requested_webhook_v2",
        "AppActivateRequestedWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.app_activate_requested_webhook_v2_type",
        "AppDeactivatedWebhookV2": "benchling_api_client.webhooks.v0.stable.models.app_deactivated_webhook_v2",
        "AppDeactivatedWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.app_deactivated_webhook_v2_type",
        "AppInstalledWebhookV2": "benchling_api_client.webhooks.v0.stable.models.app_installed_webhook_v2",
        "AppInstalledWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.app_installed_webhook_v2_type",
        "AssayRunCreatedWebhookV2": "benchling_api_client.webhooks.v0.stable.models.assay_run_created_webhook_v2",
        "AssayRunCreatedWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.assay_run_created_webhook_v2_type",
        "AssayRunUpdatedFieldsWebhookV2": "benchling_api_client.webhooks.v0.stable.models.assay_run_updated_fields_webhook_v2",
        "AssayRunUpdatedFieldsWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.assay_run_updated_fields_webhook_v2_type",
        "AutomationFileTransformFailedWebhookV2": "benchling_api_client.webhooks.v0.stable.models.automation_file_transform_failed_webhook_v2",
        "AutomationFileTransformFailedWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.automation_file_transform_failed_webhook_v2_type",
        "AutomationFileTransformPendingWebhookV2": "benchling_api_client.webhooks.v0.stable.models.automation_file_transform_pending_webhook_v2",
        "AutomationFileTransformPendingWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.automation_file_transform_pending_webhook_v2_type",
        "AutomationFileTransformRunningWebhookV2": "benchling_api_client.webhooks.v0.stable.models.automation_file_transform_running_webhook_v2",
        "AutomationFileTransformRunningWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.automation_file_transform_running_webhook_v2_type",
        "AutomationFileTransformSucceededWebhookV2": "benchling_api_client.webhooks.v0.stable.models.automation_file_transform_succeeded_webhook_v2",
        "AutomationFileTransformSucceededWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.automation_file_transform_succeeded_webhook_v2_type",
        "CanvasCreatedWebhookV2": "benchling_api_client.webhooks.v0.stable.models.canvas_created_webhook_v2",
        "CanvasCreatedWebhookV2Beta": "benchling_api_client.webhooks.v0.stable.models.canvas_created_webhook_v2_beta",
        "CanvasCreatedWebhookV2BetaType": "benchling_api_client.webhooks.v0.stable.models.canvas_created_webhook_v2_beta_type",
        "CanvasCreatedWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.canvas_created_webhook_v2_type",
        "CanvasInitializeWebhookV2": "benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v2",
        "CanvasInitializeWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v2_type",
        "CanvasInteractionWebhookV2": "benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v2",
        "CanvasInteractionWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v2_type",
        "CustomEntityCreatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.custom_entity_created_webhook_v3",
        "CustomEntityCreatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.custom_entity_created_webhook_v3_type",
        "CustomEntityUpdatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.custom_entity_updated_webhook_v3",
        "CustomEntityUpdatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.custom_entity_updated_webhook_v3_type",
        "DnaOligoCreatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.dna_oligo_created_webhook_v3",
        "DnaOligoCreatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.dna_oligo_created_webhook_v3_type",
        "DnaOligoUpdatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.dna_oligo_updated_webhook_v3",
        "DnaOligoUpdatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.dna_oligo_updated_webhook_v3_type",
        "DnaSequenceCreatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.dna_sequence_created_webhook_v3",
        "DnaSequenceCreatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.dna_sequence_created_webhook_v3_type",
        "DnaSequenceUpdatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.dna_sequence_updated_webhook_v3",
        "DnaSequenceUpdatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.dna_sequence_updated_webhook_v3_type",
        "EntityRegisteredWebhookV2": "benchling_api_client.webhooks.v0.stable.models.entity_registered_webhook_v2",
        "EntityRegisteredWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.entity_registered_webhook_v2_type",
        "EntryCreatedWebhookV2": "benchling_api_client.webhooks.v0.stable.models.entry_created_webhook_v2",
        "EntryCreatedWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.entry_created_webhook_v2_type",
        "EntryCreatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.entry_created_webhook_v3",
        "EntryCreatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.entry_created_webhook_v3_type",
        "EntryUpdatedFieldsWebhookV2": "benchling_api_client.webhooks.v0.stable.models.entry_updated_fields_webhook_v2",
        "EntryUpdatedFieldsWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.entry_updated_fields_webhook_v2_type",
        "EntryUpdatedReviewRecordWebhookV2": "benchling_api_client.webhooks.v0.stable.models.entry_updated_review_record_webhook_v2",
        "EntryUpdatedReviewRecordWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.entry_updated_review_record_webhook_v2_type",
        "EventBaseWebhookV2": "benchling_api_client.webhooks.v0.stable.models.event_base_webhook_v2",
        "EventBaseWebhookV2Schematized": "benchling_api_client.webhooks.v0.stable.models.event_base_webhook_v2_schematized",
        "EventResourceSchema": "benchling_api_client.webhooks.v0.stable.models.event_resource_schema",
        "LifecycleActivateWebhookV0": "benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0",
        "LifecycleActivateWebhookV0Beta": "benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0_beta",
        "LifecycleActivateWebhookV0BetaType": "benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0_beta_type",
        "LifecycleActivateWebhookV0Type": "benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0_type",
        "LifecycleConfigurationUpdateWebhookV0Beta": "benchling_api_client.webhooks.v0.stable.models.lifecycle_configuration_update_webhook_v0_beta",
        "LifecycleConfigurationUpdateWebhookV0BetaType": "benchling_api_client.webhooks.v0.stable.models.lifecycle_configuration_update_webhook_v0_beta_type",
        "LifecycleConfigurationUpdateWebhookV2Beta": "benchling_api_client.webhooks.v0.stable.models.lifecycle_configuration_update_webhook_v2_beta",
        "LifecycleConfigurationUpdateWebhookV2BetaType": "benchling_api_client.webhooks.v0.stable.models.lifecycle_configuration_update_webhook_v2_beta_type",
        "LifecycleDeactivateWebhookV0": "benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0",
        "LifecycleDeactivateWebhookV0Beta": "benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0_beta",
        "LifecycleDeactivateWebhookV0BetaType": "benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0_beta_type",
        "LifecycleDeactivateWebhookV0Type": "benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0_type",
        "MessageBase": "benchling_api_client.webhooks.v0.stable.models.message_base",
        "MessageBaseV0": "benchling_api_client.webhooks.v0.stable.models.message_base_v0",
        "ProjectCreatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.project_created_webhook_v3",
        "ProjectCreatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.project_created_webhook_v3_type",
        "ProjectUpdatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.project_updated_webhook_v3",
        "ProjectUpdatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.project_updated_webhook_v3_type",
        "RequestCreatedWebhookV2": "benchling_api_client.webhooks.v0.stable.models.request_created_webhook_v2",
        "RequestCreatedWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.request_created_webhook_v2_type",
        "RequestUpdatedFieldsWebhookV2": "benchling_api_client.webhooks.v0.stable.models.request_updated_fields_webhook_v2",
        "RequestUpdatedFieldsWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.request_updated_fields_webhook_v2_type",
        "RequestUpdatedStatusWebhookV2": "benchling_api_client.webhooks.v0.stable.models.request_updated_status_webhook_v2",
        "RequestUpdatedStatusWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.request_updated_status_webhook_v2_type",
        "RnaOligoCreatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.rna_oligo_created_webhook_v3",
        "RnaOligoCreatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.rna_oligo_created_webhook_v3_type",
        "RnaOligoUpdatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.rna_oligo_updated_webhook_v3",
        "RnaOligoUpdatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.rna_oligo_updated_webhook_v3_type",
        "RnaSequenceCreatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.rna_sequence_created_webhook_v3",
        "RnaSequenceCreatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.rna_sequence_created_webhook_v3_type",
        "RnaSequenceUpdatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.rna_sequence_updated_webhook_v3",
        "RnaSequenceUpdatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.rna_sequence_updated_webhook_v3_type",
        "RunCreatedWebhookV3": "benchling_api_client.webhooks.v0.stable.models.run_created_webhook_v3",
        "RunCreatedWebhookV3Type": "benchling_api_client.webhooks.v0.stable.models.run_created_webhook_v3_type",
        "UpdateEventBaseWebhookV2": "benchling_api_client.webhooks.v0.stable.models.update_event_base_webhook_v2",
        "UpdateEventBaseWebhookV2Schematized": "benchling_api_client.webhooks.v0.stable.models.update_event_base_webhook_v2_schematized",
        "V2AssayRunCreatedEvent": "benchling_api_client.webhooks.v0.stable.models.v2_assay_run_created_event",
        "V2AssayRunCreatedEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_assay_run_created_event_event_type",
        "V2AssayRunUpdatedFieldsEvent": "benchling_api_client.webhooks.v0.stable.models.v2_assay_run_updated_fields_event",
        "V2AssayRunUpdatedFieldsEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_assay_run_updated_fields_event_event_type",
        "V2EntityRegisteredEvent": "benchling_api_client.webhooks.v0.stable.models.v2_entity_registered_event",
        "V2EntityRegisteredEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_entity_registered_event_event_type",
        "V2EntryCreatedEvent": "benchling_api_client.webhooks.v0.stable.models.v2_entry_created_event",
        "V2EntryCreatedEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_entry_created_event_event_type",
        "V2EntryUpdatedFieldsEvent": "benchling_api_client.webhooks.v0.stable.models.v2_entry_updated_fields_event",
        "V2EntryUpdatedFieldsEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_entry_updated_fields_event_event_type",
        "V2EntryUpdatedReviewRecordEvent": "benchling_api_client.webhooks.v0.stable.models.v2_entry_updated_review_record_event",
        "V2EntryUpdatedReviewRecordEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_entry_updated_review_record_event_event_type",
        "V2RequestCreatedEvent": "benchling_api_client.webhooks.v0.stable.models.v2_request_created_event",
        "V2RequestCreatedEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_request_created_event_event_type",
        "V2RequestUpdatedFieldsEvent": "benchling_api_client.webhooks.v0.stable.models.v2_request_updated_fields_event",
        "V2RequestUpdatedFieldsEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_request_updated_fields_event_event_type",
        "V2RequestUpdatedStatusEvent": "benchling_api_client.webhooks.v0.stable.models.v2_request_updated_status_event",
        "V2RequestUpdatedStatusEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_request_updated_status_event_event_type",
        "V2WorkflowOutputCreatedEvent": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_output_created_event",
        "V2WorkflowOutputCreatedEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_output_created_event_event_type",
        "V2WorkflowOutputUpdatedFieldsEvent": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_output_updated_fields_event",
        "V2WorkflowOutputUpdatedFieldsEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_output_updated_fields_event_event_type",
        "V2WorkflowTaskCreatedEvent": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_created_event",
        "V2WorkflowTaskCreatedEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_created_event_event_type",
        "V2WorkflowTaskGroupCreatedEvent": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_group_created_event",
        "V2WorkflowTaskGroupCreatedEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_group_created_event_event_type",
        "V2WorkflowTaskGroupUpdatedWatchersEvent": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_group_updated_watchers_event",
        "V2WorkflowTaskGroupUpdatedWatchersEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_group_updated_watchers_event_event_type",
        "V2WorkflowTaskUpdatedAssigneeEvent": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_assignee_event",
        "V2WorkflowTaskUpdatedAssigneeEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_assignee_event_event_type",
        "V2WorkflowTaskUpdatedFieldsEvent": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_fields_event",
        "V2WorkflowTaskUpdatedFieldsEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_fields_event_event_type",
        "V2WorkflowTaskUpdatedScheduledOnEvent": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_scheduled_on_event",
        "V2WorkflowTaskUpdatedScheduledOnEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_scheduled_on_event_event_type",
        "V2WorkflowTaskUpdatedStatusEvent": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_status_event",
        "V2WorkflowTaskUpdatedStatusEventEventType": "benchling_api_client.webhooks.v0.stable.models.v2_workflow_task_updated_status_event_event_type",
        "V3EventBase": "benchling_api_client.webhooks.v0.stable.models.v3_event_base",
        "V3EventBaseStability": "benchling_api_client.webhooks.v0.stable.models.v3_event_base_stability",
        "V3UpdateEventBase": "benchling_api_client.webhooks.v0.stable.models.v3_update_event_base",
        "WebhookEnvelopeV0": "benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0",
        "WebhookEnvelopeV0App": "benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_app",
        "WebhookEnvelopeV0AppDefinition": "benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_app_definition",
        "WebhookEnvelopeV0Version": "benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_version",
        "WebhookMessageV0": "benchling_api_client.webhooks.v0.stable.models.webhook_message_v0",
        "WorkflowOutputCreatedWebhookV2": "benchling_api_client.webhooks.v0.stable.models.workflow_output_created_webhook_v2",
        "WorkflowOutputCreatedWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.workflow_output_created_webhook_v2_type",
        "WorkflowOutputUpdatedFieldsWebhookV2": "benchling_api_client.webhooks.v0.stable.models.workflow_output_updated_fields_webhook_v2",
        "WorkflowOutputUpdatedFieldsWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.workflow_output_updated_fields_webhook_v2_type",
        "WorkflowTaskCreatedWebhookV2": "benchling_api_client.webhooks.v0.stable.models.workflow_task_created_webhook_v2",
        "WorkflowTaskCreatedWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.workflow_task_created_webhook_v2_type",
        "WorkflowTaskGroupCreatedWebhookV2": "benchling_api_client.webhooks.v0.stable.models.workflow_task_group_created_webhook_v2",
        "WorkflowTaskGroupCreatedWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.workflow_task_group_created_webhook_v2_type",
        "WorkflowTaskGroupMappingCompletedWebhookV2": "benchling_api_client.webhooks.v0.stable.models.workflow_task_group_mapping_completed_webhook_v2",
        "WorkflowTaskGroupMappingCompletedWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.workflow_task_group_mapping_completed_webhook_v2_type",
        "WorkflowTaskGroupUpdatedWatchersWebhookV2": "benchling_api_client.webhooks.v0.stable.models.workflow_task_group_updated_watchers_webhook_v2",
        "WorkflowTaskGroupUpdatedWatchersWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.workflow_task_group_updated_watchers_webhook_v2_type",
        "WorkflowTaskUpdatedAssigneeWebhookV2": "benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_assignee_webhook_v2",
        "WorkflowTaskUpdatedAssigneeWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_assignee_webhook_v2_type",
        "WorkflowTaskUpdatedFieldsWebhookV2": "benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_fields_webhook_v2",
        "WorkflowTaskUpdatedFieldsWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_fields_webhook_v2_type",
        "WorkflowTaskUpdatedScheduledOnWebhookV2": "benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_scheduled_on_webhook_v2",
        "WorkflowTaskUpdatedScheduledOnWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_scheduled_on_webhook_v2_type",
        "WorkflowTaskUpdatedStatusWebhookV2": "benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_status_webhook_v2",
        "WorkflowTaskUpdatedStatusWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.workflow_task_updated_status_webhook_v2_type",
    }

    from types import ModuleType

    # Custom module to allow for lazy loading of models
    class _Models(ModuleType):
        def __getattr__(self, name):
            if module_name := model_to_module_mapping.get(name):
                module = __import__(module_name, None, None, [name])
                setattr(self, name, getattr(module, name))
                return ModuleType.__getattribute__(self, name)
            return ModuleType.__getattr__(self, name)

    # keep a reference to this module so that it's not garbage collected
    old_module = sys.modules[__name__]

    new_module = sys.modules[__name__] = _Models(__name__)
    new_module.__dict__.update(
        {
            "__file__": __file__,
            "__path__": __path__,
            "__doc__": __doc__,
            "__all__": __all__,
        }
    )
