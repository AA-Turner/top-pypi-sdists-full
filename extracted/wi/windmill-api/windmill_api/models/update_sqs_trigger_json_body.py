from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_sqs_trigger_json_body_aws_auth_resource_type import UpdateSqsTriggerJsonBodyAwsAuthResourceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_sqs_trigger_json_body_error_handler_args import UpdateSqsTriggerJsonBodyErrorHandlerArgs
    from ..models.update_sqs_trigger_json_body_retry import UpdateSqsTriggerJsonBodyRetry


T = TypeVar("T", bound="UpdateSqsTriggerJsonBody")


@_attrs_define
class UpdateSqsTriggerJsonBody:
    """
    Attributes:
        queue_url (str):
        aws_auth_resource_type (UpdateSqsTriggerJsonBodyAwsAuthResourceType):
        aws_resource_path (str):
        path (str):
        script_path (str):
        is_flow (bool):
        enabled (bool):
        message_attributes (Union[Unset, List[str]]):
        error_handler_path (Union[Unset, str]):
        error_handler_args (Union[Unset, UpdateSqsTriggerJsonBodyErrorHandlerArgs]): The arguments to pass to the script
            or flow
        retry (Union[Unset, UpdateSqsTriggerJsonBodyRetry]):
    """

    queue_url: str
    aws_auth_resource_type: UpdateSqsTriggerJsonBodyAwsAuthResourceType
    aws_resource_path: str
    path: str
    script_path: str
    is_flow: bool
    enabled: bool
    message_attributes: Union[Unset, List[str]] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "UpdateSqsTriggerJsonBodyErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "UpdateSqsTriggerJsonBodyRetry"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        queue_url = self.queue_url
        aws_auth_resource_type = self.aws_auth_resource_type.value

        aws_resource_path = self.aws_resource_path
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        enabled = self.enabled
        message_attributes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.message_attributes, Unset):
            message_attributes = self.message_attributes

        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "queue_url": queue_url,
                "aws_auth_resource_type": aws_auth_resource_type,
                "aws_resource_path": aws_resource_path,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
                "enabled": enabled,
            }
        )
        if message_attributes is not UNSET:
            field_dict["message_attributes"] = message_attributes
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_sqs_trigger_json_body_error_handler_args import UpdateSqsTriggerJsonBodyErrorHandlerArgs
        from ..models.update_sqs_trigger_json_body_retry import UpdateSqsTriggerJsonBodyRetry

        d = src_dict.copy()
        queue_url = d.pop("queue_url")

        aws_auth_resource_type = UpdateSqsTriggerJsonBodyAwsAuthResourceType(d.pop("aws_auth_resource_type"))

        aws_resource_path = d.pop("aws_resource_path")

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        enabled = d.pop("enabled")

        message_attributes = cast(List[str], d.pop("message_attributes", UNSET))

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, UpdateSqsTriggerJsonBodyErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = UpdateSqsTriggerJsonBodyErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, UpdateSqsTriggerJsonBodyRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = UpdateSqsTriggerJsonBodyRetry.from_dict(_retry)

        update_sqs_trigger_json_body = cls(
            queue_url=queue_url,
            aws_auth_resource_type=aws_auth_resource_type,
            aws_resource_path=aws_resource_path,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            enabled=enabled,
            message_attributes=message_attributes,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
        )

        update_sqs_trigger_json_body.additional_properties = d
        return update_sqs_trigger_json_body

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
