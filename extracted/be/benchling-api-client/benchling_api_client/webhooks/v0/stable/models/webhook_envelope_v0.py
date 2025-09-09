from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
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
from ..models.webhook_envelope_v0_app import WebhookEnvelopeV0App
from ..models.webhook_envelope_v0_app_definition import WebhookEnvelopeV0AppDefinition
from ..models.webhook_envelope_v0_version import WebhookEnvelopeV0Version
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
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookEnvelopeV0")


@attr.s(auto_attribs=True, repr=False)
class WebhookEnvelopeV0:
    """  """

    _app: WebhookEnvelopeV0App
    _app_definition: WebhookEnvelopeV0AppDefinition
    _base_url: str
    _message: Union[
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
    _tenant_id: str
    _version: WebhookEnvelopeV0Version
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("app={}".format(repr(self._app)))
        fields.append("app_definition={}".format(repr(self._app_definition)))
        fields.append("base_url={}".format(repr(self._base_url)))
        fields.append("message={}".format(repr(self._message)))
        fields.append("tenant_id={}".format(repr(self._tenant_id)))
        fields.append("version={}".format(repr(self._version)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WebhookEnvelopeV0({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app = self._app.to_dict()

        app_definition = self._app_definition.to_dict()

        base_url = self._base_url
        if isinstance(self._message, UnknownType):
            message = self._message.value
        elif isinstance(self._message, LifecycleConfigurationUpdateWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, CanvasInteractionWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, CanvasInitializeWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, CanvasCreatedWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, CanvasCreatedWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, AutomationFileTransformRunningWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, AutomationFileTransformPendingWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, AutomationFileTransformSucceededWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, AutomationFileTransformFailedWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, AppActivateRequestedWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, AppDeactivatedWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, AppInstalledWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, AssayRunCreatedWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, AssayRunUpdatedFieldsWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, EntityRegisteredWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, EntryCreatedWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, EntryUpdatedFieldsWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, EntryUpdatedReviewRecordWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, RequestCreatedWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, RequestUpdatedFieldsWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, RequestUpdatedStatusWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskGroupCreatedWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskGroupMappingCompletedWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskGroupUpdatedWatchersWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskCreatedWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskUpdatedAssigneeWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskUpdatedScheduledOnWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskUpdatedStatusWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskUpdatedFieldsWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowOutputCreatedWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowOutputUpdatedFieldsWebhookV2):
            message = self._message.to_dict()

        elif isinstance(self._message, LifecycleActivateWebhookV0):
            message = self._message.to_dict()

        elif isinstance(self._message, LifecycleDeactivateWebhookV0):
            message = self._message.to_dict()

        elif isinstance(self._message, LifecycleActivateWebhookV0Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, LifecycleDeactivateWebhookV0Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, LifecycleConfigurationUpdateWebhookV0Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, EntryCreatedWebhookV3):
            message = self._message.to_dict()

        elif isinstance(self._message, RunCreatedWebhookV3):
            message = self._message.to_dict()

        elif isinstance(self._message, ProjectCreatedWebhookV3):
            message = self._message.to_dict()

        elif isinstance(self._message, CustomEntityCreatedWebhookV3):
            message = self._message.to_dict()

        elif isinstance(self._message, DnaOligoCreatedWebhookV3):
            message = self._message.to_dict()

        elif isinstance(self._message, DnaSequenceCreatedWebhookV3):
            message = self._message.to_dict()

        elif isinstance(self._message, RnaOligoCreatedWebhookV3):
            message = self._message.to_dict()

        elif isinstance(self._message, RnaSequenceCreatedWebhookV3):
            message = self._message.to_dict()

        elif isinstance(self._message, ProjectUpdatedWebhookV3):
            message = self._message.to_dict()

        elif isinstance(self._message, CustomEntityUpdatedWebhookV3):
            message = self._message.to_dict()

        elif isinstance(self._message, DnaOligoUpdatedWebhookV3):
            message = self._message.to_dict()

        elif isinstance(self._message, DnaSequenceUpdatedWebhookV3):
            message = self._message.to_dict()

        elif isinstance(self._message, RnaOligoUpdatedWebhookV3):
            message = self._message.to_dict()

        else:
            message = self._message.to_dict()

        tenant_id = self._tenant_id
        version = self._version.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app is not UNSET:
            field_dict["app"] = app
        if app_definition is not UNSET:
            field_dict["appDefinition"] = app_definition
        if base_url is not UNSET:
            field_dict["baseURL"] = base_url
        if message is not UNSET:
            field_dict["message"] = message
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_app() -> WebhookEnvelopeV0App:
            app = WebhookEnvelopeV0App.from_dict(d.pop("app"), strict=False)

            return app

        try:
            app = get_app()
        except KeyError:
            if strict:
                raise
            app = cast(WebhookEnvelopeV0App, UNSET)

        def get_app_definition() -> WebhookEnvelopeV0AppDefinition:
            app_definition = WebhookEnvelopeV0AppDefinition.from_dict(d.pop("appDefinition"), strict=False)

            return app_definition

        try:
            app_definition = get_app_definition()
        except KeyError:
            if strict:
                raise
            app_definition = cast(WebhookEnvelopeV0AppDefinition, UNSET)

        def get_base_url() -> str:
            base_url = d.pop("baseURL")
            return base_url

        try:
            base_url = get_base_url()
        except KeyError:
            if strict:
                raise
            base_url = cast(str, UNSET)

        def get_message() -> Union[
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
        ]:
            message: Union[
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
            _message = d.pop("message")

            if True:
                discriminator = _message["type"]
                if discriminator == "v0-beta.app.configuration.updated":
                    message = LifecycleConfigurationUpdateWebhookV0Beta.from_dict(_message)
                elif discriminator == "v0-beta.lifecycle.activateRequested":
                    message = LifecycleActivateWebhookV0Beta.from_dict(_message)
                elif discriminator == "v0-beta.lifecycle.deactivated":
                    message = LifecycleDeactivateWebhookV0Beta.from_dict(_message)
                elif discriminator == "v0.app.activateRequested":
                    message = LifecycleActivateWebhookV0.from_dict(_message)
                elif discriminator == "v0.app.deactivated":
                    message = LifecycleDeactivateWebhookV0.from_dict(_message)
                elif discriminator == "v2-beta.app.configuration.updated":
                    message = LifecycleConfigurationUpdateWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.canvas.created":
                    message = CanvasCreatedWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2.app.activateRequested":
                    message = AppActivateRequestedWebhookV2.from_dict(_message)
                elif discriminator == "v2.app.deactivated":
                    message = AppDeactivatedWebhookV2.from_dict(_message)
                elif discriminator == "v2.app.installed":
                    message = AppInstalledWebhookV2.from_dict(_message)
                elif discriminator == "v2.assayRun.created":
                    message = AssayRunCreatedWebhookV2.from_dict(_message)
                elif discriminator == "v2.assayRun.updated.fields":
                    message = AssayRunUpdatedFieldsWebhookV2.from_dict(_message)
                elif discriminator == "v2.automationFileTransform.updated.status.failed":
                    message = AutomationFileTransformFailedWebhookV2.from_dict(_message)
                elif discriminator == "v2.automationFileTransform.updated.status.pending":
                    message = AutomationFileTransformPendingWebhookV2.from_dict(_message)
                elif discriminator == "v2.automationFileTransform.updated.status.running":
                    message = AutomationFileTransformRunningWebhookV2.from_dict(_message)
                elif discriminator == "v2.automationFileTransform.updated.status.succeeded":
                    message = AutomationFileTransformSucceededWebhookV2.from_dict(_message)
                elif discriminator == "v2.canvas.created":
                    message = CanvasCreatedWebhookV2.from_dict(_message)
                elif discriminator == "v2.canvas.initialized":
                    message = CanvasInitializeWebhookV2.from_dict(_message)
                elif discriminator == "v2.canvas.userInteracted":
                    message = CanvasInteractionWebhookV2.from_dict(_message)
                elif discriminator == "v2.entity.registered":
                    message = EntityRegisteredWebhookV2.from_dict(_message)
                elif discriminator == "v2.entry.created":
                    message = EntryCreatedWebhookV2.from_dict(_message)
                elif discriminator == "v2.entry.updated.fields":
                    message = EntryUpdatedFieldsWebhookV2.from_dict(_message)
                elif discriminator == "v2.entry.updated.reviewRecord":
                    message = EntryUpdatedReviewRecordWebhookV2.from_dict(_message)
                elif discriminator == "v2.request.created":
                    message = RequestCreatedWebhookV2.from_dict(_message)
                elif discriminator == "v2.request.updated.fields":
                    message = RequestUpdatedFieldsWebhookV2.from_dict(_message)
                elif discriminator == "v2.request.updated.status":
                    message = RequestUpdatedStatusWebhookV2.from_dict(_message)
                elif discriminator == "v2.workflowOutput.created":
                    message = WorkflowOutputCreatedWebhookV2.from_dict(_message)
                elif discriminator == "v2.workflowOutput.updated.fields":
                    message = WorkflowOutputUpdatedFieldsWebhookV2.from_dict(_message)
                elif discriminator == "v2.workflowTask.created":
                    message = WorkflowTaskCreatedWebhookV2.from_dict(_message)
                elif discriminator == "v2.workflowTask.updated.assignee":
                    message = WorkflowTaskUpdatedAssigneeWebhookV2.from_dict(_message)
                elif discriminator == "v2.workflowTask.updated.fields":
                    message = WorkflowTaskUpdatedFieldsWebhookV2.from_dict(_message)
                elif discriminator == "v2.workflowTask.updated.scheduledOn":
                    message = WorkflowTaskUpdatedScheduledOnWebhookV2.from_dict(_message)
                elif discriminator == "v2.workflowTask.updated.status":
                    message = WorkflowTaskUpdatedStatusWebhookV2.from_dict(_message)
                elif discriminator == "v2.workflowTaskGroup.created":
                    message = WorkflowTaskGroupCreatedWebhookV2.from_dict(_message)
                elif discriminator == "v2.workflowTaskGroup.mappingCompleted":
                    message = WorkflowTaskGroupMappingCompletedWebhookV2.from_dict(_message)
                elif discriminator == "v2.workflowTaskGroup.updated.watchers":
                    message = WorkflowTaskGroupUpdatedWatchersWebhookV2.from_dict(_message)
                elif discriminator == "v3.customEntity.created":
                    message = CustomEntityCreatedWebhookV3.from_dict(_message)
                elif discriminator == "v3.customEntity.updated":
                    message = CustomEntityUpdatedWebhookV3.from_dict(_message)
                elif discriminator == "v3.dnaOligo.created":
                    message = DnaOligoCreatedWebhookV3.from_dict(_message)
                elif discriminator == "v3.dnaOligo.updated":
                    message = DnaOligoUpdatedWebhookV3.from_dict(_message)
                elif discriminator == "v3.dnaSequence.created":
                    message = DnaSequenceCreatedWebhookV3.from_dict(_message)
                elif discriminator == "v3.dnaSequence.updated":
                    message = DnaSequenceUpdatedWebhookV3.from_dict(_message)
                elif discriminator == "v3.entry.created":
                    message = EntryCreatedWebhookV3.from_dict(_message)
                elif discriminator == "v3.project.created":
                    message = ProjectCreatedWebhookV3.from_dict(_message)
                elif discriminator == "v3.project.updated":
                    message = ProjectUpdatedWebhookV3.from_dict(_message)
                elif discriminator == "v3.rnaOligo.created":
                    message = RnaOligoCreatedWebhookV3.from_dict(_message)
                elif discriminator == "v3.rnaOligo.updated":
                    message = RnaOligoUpdatedWebhookV3.from_dict(_message)
                elif discriminator == "v3.rnaSequence.created":
                    message = RnaSequenceCreatedWebhookV3.from_dict(_message)
                elif discriminator == "v3.rnaSequence.updated":
                    message = RnaSequenceUpdatedWebhookV3.from_dict(_message)
                elif discriminator == "v3.run.created":
                    message = RunCreatedWebhookV3.from_dict(_message)
                else:
                    message = UnknownType(value=_message)

            return message

        try:
            message = get_message()
        except KeyError:
            if strict:
                raise
            message = cast(
                Union[
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
                ],
                UNSET,
            )

        def get_tenant_id() -> str:
            tenant_id = d.pop("tenantId")
            return tenant_id

        try:
            tenant_id = get_tenant_id()
        except KeyError:
            if strict:
                raise
            tenant_id = cast(str, UNSET)

        def get_version() -> WebhookEnvelopeV0Version:
            _version = d.pop("version")
            try:
                version = WebhookEnvelopeV0Version(_version)
            except ValueError:
                version = WebhookEnvelopeV0Version.of_unknown(_version)

            return version

        try:
            version = get_version()
        except KeyError:
            if strict:
                raise
            version = cast(WebhookEnvelopeV0Version, UNSET)

        webhook_envelope_v0 = cls(
            app=app,
            app_definition=app_definition,
            base_url=base_url,
            message=message,
            tenant_id=tenant_id,
            version=version,
        )

        webhook_envelope_v0.additional_properties = d
        return webhook_envelope_v0

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
    def app(self) -> WebhookEnvelopeV0App:
        if isinstance(self._app, Unset):
            raise NotPresentError(self, "app")
        return self._app

    @app.setter
    def app(self, value: WebhookEnvelopeV0App) -> None:
        self._app = value

    @property
    def app_definition(self) -> WebhookEnvelopeV0AppDefinition:
        if isinstance(self._app_definition, Unset):
            raise NotPresentError(self, "app_definition")
        return self._app_definition

    @app_definition.setter
    def app_definition(self, value: WebhookEnvelopeV0AppDefinition) -> None:
        self._app_definition = value

    @property
    def base_url(self) -> str:
        """ Base tenant URL from which the webhook is coming """
        if isinstance(self._base_url, Unset):
            raise NotPresentError(self, "base_url")
        return self._base_url

    @base_url.setter
    def base_url(self, value: str) -> None:
        self._base_url = value

    @property
    def message(
        self,
    ) -> Union[
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
    ]:
        if isinstance(self._message, Unset):
            raise NotPresentError(self, "message")
        return self._message

    @message.setter
    def message(
        self,
        value: Union[
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
        ],
    ) -> None:
        self._message = value

    @property
    def tenant_id(self) -> str:
        """ Global tenant id from which the webhook is coming """
        if isinstance(self._tenant_id, Unset):
            raise NotPresentError(self, "tenant_id")
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, value: str) -> None:
        self._tenant_id = value

    @property
    def version(self) -> WebhookEnvelopeV0Version:
        """ Version of the webhook envelope shape. Always 0. """
        if isinstance(self._version, Unset):
            raise NotPresentError(self, "version")
        return self._version

    @version.setter
    def version(self, value: WebhookEnvelopeV0Version) -> None:
        self._version = value
