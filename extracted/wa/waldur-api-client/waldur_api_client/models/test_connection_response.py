from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TestConnectionResponse")


@_attrs_define
class TestConnectionResponse:
    """
    Attributes:
        status (str):
        groups_count (int):
        groups (list[str]):
    """

    status: str
    groups_count: int
    groups: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        groups_count = self.groups_count

        groups = self.groups

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "groups_count": groups_count,
                "groups": groups,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = d.pop("status")

        groups_count = d.pop("groups_count")

        groups = cast(list[str], d.pop("groups"))

        test_connection_response = cls(
            status=status,
            groups_count=groups_count,
            groups=groups,
        )

        test_connection_response.additional_properties = d
        return test_connection_response

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
