from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CancelRequestResponse")


@_attrs_define
class CancelRequestResponse:
    """
    Attributes:
        uuid (str): UUID of the canceled permission request
        scope_name (str): Name of the invitation scope
        scope_uuid (str): UUID of the invitation scope
    """

    uuid: str
    scope_name: str
    scope_uuid: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        scope_name = self.scope_name

        scope_uuid = self.scope_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "scope_name": scope_name,
                "scope_uuid": scope_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        scope_name = d.pop("scope_name")

        scope_uuid = d.pop("scope_uuid")

        cancel_request_response = cls(
            uuid=uuid,
            scope_name=scope_name,
            scope_uuid=scope_uuid,
        )

        cancel_request_response.additional_properties = d
        return cancel_request_response

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
