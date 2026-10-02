from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MessageStateCacheFilter")


@_attrs_define
class MessageStateCacheFilter:
    """
    Attributes:
        resource_uuid (Union[None, str]): Filter by resource UUID
        message_type (Union[None, str]): Filter by message type
    """

    resource_uuid: Union[None, str]
    message_type: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_uuid: Union[None, str]
        resource_uuid = self.resource_uuid

        message_type: Union[None, str]
        message_type = self.message_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_uuid": resource_uuid,
                "message_type": message_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_resource_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resource_uuid = _parse_resource_uuid(d.pop("resource_uuid"))

        def _parse_message_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        message_type = _parse_message_type(d.pop("message_type"))

        message_state_cache_filter = cls(
            resource_uuid=resource_uuid,
            message_type=message_type,
        )

        message_state_cache_filter.additional_properties = d
        return message_state_cache_filter

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
