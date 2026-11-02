from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_azure_trigger_json_body_azure_mode import CreateAzureTriggerJsonBodyAzureMode
from ..models.create_azure_trigger_json_body_mode import CreateAzureTriggerJsonBodyMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_azure_trigger_json_body_error_handler_args import CreateAzureTriggerJsonBodyErrorHandlerArgs
    from ..models.create_azure_trigger_json_body_retry import CreateAzureTriggerJsonBodyRetry


T = TypeVar("T", bound="CreateAzureTriggerJsonBody")


@_attrs_define
class CreateAzureTriggerJsonBody:
    """Data for creating or updating an Azure Event Grid trigger.

    Attributes:
        azure_resource_path (str):
        azure_mode (CreateAzureTriggerJsonBodyAzureMode): Azure Event Grid trigger mode.
        scope_resource_id (str):
        subscription_name (str):
        path (str): The unique Windmill path for this trigger. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`. This is the trigger object path, not the HTTP route path.
        script_path (str):
        is_flow (bool):
        topic_name (Union[Unset, None, str]):
        base_endpoint (Union[Unset, str]): Base URL for push delivery endpoints (push modes only).
        event_type_filters (Union[Unset, List[str]]):
        mode (Union[Unset, CreateAzureTriggerJsonBodyMode]): job trigger mode
        error_handler_path (Union[Unset, str]):
        error_handler_args (Union[Unset, CreateAzureTriggerJsonBodyErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, CreateAzureTriggerJsonBodyRetry]): Retry configuration for failed module executions
        permissioned_as (Union[Unset, str]):
        preserve_permissioned_as (Union[Unset, bool]):
        labels (Union[Unset, List[str]]):
    """

    azure_resource_path: str
    azure_mode: CreateAzureTriggerJsonBodyAzureMode
    scope_resource_id: str
    subscription_name: str
    path: str
    script_path: str
    is_flow: bool
    topic_name: Union[Unset, None, str] = UNSET
    base_endpoint: Union[Unset, str] = UNSET
    event_type_filters: Union[Unset, List[str]] = UNSET
    mode: Union[Unset, CreateAzureTriggerJsonBodyMode] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "CreateAzureTriggerJsonBodyErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "CreateAzureTriggerJsonBodyRetry"] = UNSET
    permissioned_as: Union[Unset, str] = UNSET
    preserve_permissioned_as: Union[Unset, bool] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        azure_resource_path = self.azure_resource_path
        azure_mode = self.azure_mode.value

        scope_resource_id = self.scope_resource_id
        subscription_name = self.subscription_name
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        topic_name = self.topic_name
        base_endpoint = self.base_endpoint
        event_type_filters: Union[Unset, List[str]] = UNSET
        if not isinstance(self.event_type_filters, Unset):
            event_type_filters = self.event_type_filters

        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        permissioned_as = self.permissioned_as
        preserve_permissioned_as = self.preserve_permissioned_as
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "azure_resource_path": azure_resource_path,
                "azure_mode": azure_mode,
                "scope_resource_id": scope_resource_id,
                "subscription_name": subscription_name,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
            }
        )
        if topic_name is not UNSET:
            field_dict["topic_name"] = topic_name
        if base_endpoint is not UNSET:
            field_dict["base_endpoint"] = base_endpoint
        if event_type_filters is not UNSET:
            field_dict["event_type_filters"] = event_type_filters
        if mode is not UNSET:
            field_dict["mode"] = mode
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry
        if permissioned_as is not UNSET:
            field_dict["permissioned_as"] = permissioned_as
        if preserve_permissioned_as is not UNSET:
            field_dict["preserve_permissioned_as"] = preserve_permissioned_as
        if labels is not UNSET:
            field_dict["labels"] = labels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_azure_trigger_json_body_error_handler_args import (
            CreateAzureTriggerJsonBodyErrorHandlerArgs,
        )
        from ..models.create_azure_trigger_json_body_retry import CreateAzureTriggerJsonBodyRetry

        d = src_dict.copy()
        azure_resource_path = d.pop("azure_resource_path")

        azure_mode = CreateAzureTriggerJsonBodyAzureMode(d.pop("azure_mode"))

        scope_resource_id = d.pop("scope_resource_id")

        subscription_name = d.pop("subscription_name")

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        topic_name = d.pop("topic_name", UNSET)

        base_endpoint = d.pop("base_endpoint", UNSET)

        event_type_filters = cast(List[str], d.pop("event_type_filters", UNSET))

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, CreateAzureTriggerJsonBodyMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = CreateAzureTriggerJsonBodyMode(_mode)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, CreateAzureTriggerJsonBodyErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = CreateAzureTriggerJsonBodyErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, CreateAzureTriggerJsonBodyRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = CreateAzureTriggerJsonBodyRetry.from_dict(_retry)

        permissioned_as = d.pop("permissioned_as", UNSET)

        preserve_permissioned_as = d.pop("preserve_permissioned_as", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        create_azure_trigger_json_body = cls(
            azure_resource_path=azure_resource_path,
            azure_mode=azure_mode,
            scope_resource_id=scope_resource_id,
            subscription_name=subscription_name,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            topic_name=topic_name,
            base_endpoint=base_endpoint,
            event_type_filters=event_type_filters,
            mode=mode,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            permissioned_as=permissioned_as,
            preserve_permissioned_as=preserve_permissioned_as,
            labels=labels,
        )

        create_azure_trigger_json_body.additional_properties = d
        return create_azure_trigger_json_body

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
