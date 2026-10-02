from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EventConsumerScopeOutput")


@_attrs_define
class EventConsumerScopeOutput:
    """
    Attributes:
        type_ (Union[None, str]):
        uuid (Union[None, str]):
    """

    type_: Union[None, str]
    uuid: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: Union[None, str]
        type_ = self.type_

        uuid: Union[None, str]
        uuid = self.uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "uuid": uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_type_(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        type_ = _parse_type_(d.pop("type"))

        def _parse_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        uuid = _parse_uuid(d.pop("uuid"))

        event_consumer_scope_output = cls(
            type_=type_,
            uuid=uuid,
        )

        event_consumer_scope_output.additional_properties = d
        return event_consumer_scope_output

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
