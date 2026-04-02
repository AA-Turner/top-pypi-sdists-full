from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OpenStackInstanceSecurityGroupsUpdateRequest")


@_attrs_define
class OpenStackInstanceSecurityGroupsUpdateRequest:
    """
    Attributes:
        security_groups (list[str]): List of security groups to be assigned to the instance.
    """

    security_groups: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        security_groups = self.security_groups

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "security_groups": security_groups,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        security_groups = cast(list[str], d.pop("security_groups"))

        open_stack_instance_security_groups_update_request = cls(
            security_groups=security_groups,
        )

        open_stack_instance_security_groups_update_request.additional_properties = d
        return open_stack_instance_security_groups_update_request

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
