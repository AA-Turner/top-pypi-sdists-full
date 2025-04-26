from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
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
from ..models.webhook_envelope_app import WebhookEnvelopeApp
from ..models.webhook_envelope_version import WebhookEnvelopeVersion
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
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookEnvelope")


@attr.s(auto_attribs=True, repr=False)
class WebhookEnvelope:
    """  """

    _app: WebhookEnvelopeApp
    _base_url: str
    _message: Union[
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
    _tenant_id: str
    _version: WebhookEnvelopeVersion
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("app={}".format(repr(self._app)))
        fields.append("base_url={}".format(repr(self._base_url)))
        fields.append("message={}".format(repr(self._message)))
        fields.append("tenant_id={}".format(repr(self._tenant_id)))
        fields.append("version={}".format(repr(self._version)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WebhookEnvelope({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app = self._app.to_dict()

        base_url = self._base_url
        if isinstance(self._message, UnknownType):
            message = self._message.value
        elif isinstance(self._message, LifecycleActivateWebhookV0Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, LifecycleDeactivateWebhookV0Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, LifecycleConfigurationUpdateWebhookV0Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, LifecycleConfigurationUpdateWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, AssayRunCreatedWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, AssayRunUpdatedFieldsWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, EntityRegisteredWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, EntryCreatedWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, EntryUpdatedFieldsWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, EntryUpdatedReviewRecordWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, RequestCreatedWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, RequestUpdatedFieldsWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, RequestUpdatedStatusWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskGroupCreatedWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskGroupUpdatedWatchersWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskCreatedWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskUpdatedAssigneeWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskUpdatedScheduledOnWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskUpdatedStatusWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowTaskUpdatedFieldsWebhookV2Beta):
            message = self._message.to_dict()

        elif isinstance(self._message, WorkflowOutputCreatedWebhookV2Beta):
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

        def get_app() -> WebhookEnvelopeApp:
            app = WebhookEnvelopeApp.from_dict(d.pop("app"), strict=False)

            return app

        try:
            app = get_app()
        except KeyError:
            if strict:
                raise
            app = cast(WebhookEnvelopeApp, UNSET)

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
        ]:
            message: Union[
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
            _message = d.pop("message")

            if True:
                discriminator = _message["type"]
                if discriminator == "v0-beta.app.configuration.updated":
                    message = LifecycleConfigurationUpdateWebhookV0Beta.from_dict(_message)
                elif discriminator == "v0-beta.lifecycle.activateRequested":
                    message = LifecycleActivateWebhookV0Beta.from_dict(_message)
                elif discriminator == "v0-beta.lifecycle.deactivated":
                    message = LifecycleDeactivateWebhookV0Beta.from_dict(_message)
                elif discriminator == "v2-beta.app.configuration.updated":
                    message = LifecycleConfigurationUpdateWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.assayRun.created":
                    message = AssayRunCreatedWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.assayRun.updated.fields":
                    message = AssayRunUpdatedFieldsWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.entity.registered":
                    message = EntityRegisteredWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.entry.created":
                    message = EntryCreatedWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.entry.updated.fields":
                    message = EntryUpdatedFieldsWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.entry.updated.reviewRecord":
                    message = EntryUpdatedReviewRecordWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.request.created":
                    message = RequestCreatedWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.request.updated.fields":
                    message = RequestUpdatedFieldsWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.request.updated.status":
                    message = RequestUpdatedStatusWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.workflowOutput.created":
                    message = WorkflowOutputCreatedWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.workflowOutput.updated.fields":
                    message = WorkflowOutputUpdatedFieldsWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.workflowTask.created":
                    message = WorkflowTaskCreatedWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.workflowTask.updated.assignee":
                    message = WorkflowTaskUpdatedAssigneeWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.workflowTask.updated.fields":
                    message = WorkflowTaskUpdatedFieldsWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.workflowTask.updated.scheduledOn":
                    message = WorkflowTaskUpdatedScheduledOnWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.workflowTask.updated.status":
                    message = WorkflowTaskUpdatedStatusWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.workflowTaskGroup.created":
                    message = WorkflowTaskGroupCreatedWebhookV2Beta.from_dict(_message)
                elif discriminator == "v2-beta.workflowTaskGroup.updated.watchers":
                    message = WorkflowTaskGroupUpdatedWatchersWebhookV2Beta.from_dict(_message)
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

        def get_version() -> WebhookEnvelopeVersion:
            _version = d.pop("version")
            try:
                version = WebhookEnvelopeVersion(_version)
            except ValueError:
                version = WebhookEnvelopeVersion.of_unknown(_version)

            return version

        try:
            version = get_version()
        except KeyError:
            if strict:
                raise
            version = cast(WebhookEnvelopeVersion, UNSET)

        webhook_envelope = cls(
            app=app,
            base_url=base_url,
            message=message,
            tenant_id=tenant_id,
            version=version,
        )

        webhook_envelope.additional_properties = d
        return webhook_envelope

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
    def app(self) -> WebhookEnvelopeApp:
        if isinstance(self._app, Unset):
            raise NotPresentError(self, "app")
        return self._app

    @app.setter
    def app(self, value: WebhookEnvelopeApp) -> None:
        self._app = value

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
    ]:
        if isinstance(self._message, Unset):
            raise NotPresentError(self, "message")
        return self._message

    @message.setter
    def message(
        self,
        value: Union[
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
        ],
    ) -> None:
        self._message = value

    @property
    def tenant_id(self) -> str:
        """ Global tenant id from which webhook is coming """
        if isinstance(self._tenant_id, Unset):
            raise NotPresentError(self, "tenant_id")
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, value: str) -> None:
        self._tenant_id = value

    @property
    def version(self) -> WebhookEnvelopeVersion:
        """ Version of the webhook envelope shape. Always 0 for now. """
        if isinstance(self._version, Unset):
            raise NotPresentError(self, "version")
        return self._version

    @version.setter
    def version(self, value: WebhookEnvelopeVersion) -> None:
        self._version = value
