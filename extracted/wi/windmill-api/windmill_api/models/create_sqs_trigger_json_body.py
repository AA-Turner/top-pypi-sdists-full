from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_sqs_trigger_json_body_aws_auth_resource_type import CreateSqsTriggerJsonBodyAwsAuthResourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateSqsTriggerJsonBody")


@_attrs_define
class CreateSqsTriggerJsonBody:
    """
    Attributes:
        queue_url (str):
        aws_auth_resource_type (CreateSqsTriggerJsonBodyAwsAuthResourceType):
        aws_resource_path (str):
        path (str):
        script_path (str):
        is_flow (bool):
        message_attributes (Union[Unset, List[str]]):
        enabled (Union[Unset, bool]):
    """

    queue_url: str
    aws_auth_resource_type: CreateSqsTriggerJsonBodyAwsAuthResourceType
    aws_resource_path: str
    path: str
    script_path: str
    is_flow: bool
    message_attributes: Union[Unset, List[str]] = UNSET
    enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        queue_url = self.queue_url
        aws_auth_resource_type = self.aws_auth_resource_type.value

        aws_resource_path = self.aws_resource_path
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        message_attributes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.message_attributes, Unset):
            message_attributes = self.message_attributes

        enabled = self.enabled

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
            }
        )
        if message_attributes is not UNSET:
            field_dict["message_attributes"] = message_attributes
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        queue_url = d.pop("queue_url")

        aws_auth_resource_type = CreateSqsTriggerJsonBodyAwsAuthResourceType(d.pop("aws_auth_resource_type"))

        aws_resource_path = d.pop("aws_resource_path")

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        message_attributes = cast(List[str], d.pop("message_attributes", UNSET))

        enabled = d.pop("enabled", UNSET)

        create_sqs_trigger_json_body = cls(
            queue_url=queue_url,
            aws_auth_resource_type=aws_auth_resource_type,
            aws_resource_path=aws_resource_path,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            message_attributes=message_attributes,
            enabled=enabled,
        )

        create_sqs_trigger_json_body.additional_properties = d
        return create_sqs_trigger_json_body

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
