from typing import Union

from ..extensions import UnknownType
from ..models.assay_run_created_webhook_v2_beta import AssayRunCreatedWebhookV2Beta
from ..models.assay_run_updated_fields_webhook_v2_beta import AssayRunUpdatedFieldsWebhookV2Beta
from ..models.entity_registered_webhook_v2_beta import EntityRegisteredWebhookV2Beta
from ..models.entry_created_webhook_v2_beta import EntryCreatedWebhookV2Beta
from ..models.entry_updated_fields_webhook_v2_beta import EntryUpdatedFieldsWebhookV2Beta
from ..models.entry_updated_review_record_webhook_v2_beta import EntryUpdatedReviewRecordWebhookV2Beta
from ..models.lifecycle_activate_webhook_v0_beta import LifecycleActivateWebhookV0Beta
from ..models.lifecycle_configuration_update_webhook_v0_beta import LifecycleConfigurationUpdateWebhookV0Beta
from ..models.lifecycle_configuration_update_webhook_v2_beta import LifecycleConfigurationUpdateWebhookV2Beta
from ..models.lifecycle_deactivate_webhook_v0_beta import LifecycleDeactivateWebhookV0Beta
from ..models.request_created_webhook_v2_beta import RequestCreatedWebhookV2Beta
from ..models.request_updated_fields_webhook_v2_beta import RequestUpdatedFieldsWebhookV2Beta
from ..models.request_updated_status_webhook_v2_beta import RequestUpdatedStatusWebhookV2Beta
from ..models.workflow_output_created_webhook_v2_beta import WorkflowOutputCreatedWebhookV2Beta
from ..models.workflow_output_updated_fields_webhook_v2_beta import WorkflowOutputUpdatedFieldsWebhookV2Beta
from ..models.workflow_task_created_webhook_v2_beta import WorkflowTaskCreatedWebhookV2Beta
from ..models.workflow_task_group_created_webhook_v2_beta import WorkflowTaskGroupCreatedWebhookV2Beta
from ..models.workflow_task_group_updated_watchers_webhook_v2_beta import (
    WorkflowTaskGroupUpdatedWatchersWebhookV2Beta,
)
from ..models.workflow_task_updated_assignee_webhook_v2_beta import WorkflowTaskUpdatedAssigneeWebhookV2Beta
from ..models.workflow_task_updated_fields_webhook_v2_beta import WorkflowTaskUpdatedFieldsWebhookV2Beta
from ..models.workflow_task_updated_scheduled_on_webhook_v2_beta import (
    WorkflowTaskUpdatedScheduledOnWebhookV2Beta,
)
from ..models.workflow_task_updated_status_webhook_v2_beta import WorkflowTaskUpdatedStatusWebhookV2Beta

WebhookMessage = Union[
    LifecycleActivateWebhookV0Beta,
    LifecycleDeactivateWebhookV0Beta,
    LifecycleConfigurationUpdateWebhookV0Beta,
    LifecycleConfigurationUpdateWebhookV2Beta,
    AssayRunCreatedWebhookV2Beta,
    AssayRunUpdatedFieldsWebhookV2Beta,
    EntityRegisteredWebhookV2Beta,
    EntryCreatedWebhookV2Beta,
    EntryUpdatedFieldsWebhookV2Beta,
    EntryUpdatedReviewRecordWebhookV2Beta,
    RequestCreatedWebhookV2Beta,
    RequestUpdatedFieldsWebhookV2Beta,
    RequestUpdatedStatusWebhookV2Beta,
    WorkflowTaskGroupCreatedWebhookV2Beta,
    WorkflowTaskGroupUpdatedWatchersWebhookV2Beta,
    WorkflowTaskCreatedWebhookV2Beta,
    WorkflowTaskUpdatedAssigneeWebhookV2Beta,
    WorkflowTaskUpdatedScheduledOnWebhookV2Beta,
    WorkflowTaskUpdatedStatusWebhookV2Beta,
    WorkflowTaskUpdatedFieldsWebhookV2Beta,
    WorkflowOutputCreatedWebhookV2Beta,
    WorkflowOutputUpdatedFieldsWebhookV2Beta,
    UnknownType,
]
