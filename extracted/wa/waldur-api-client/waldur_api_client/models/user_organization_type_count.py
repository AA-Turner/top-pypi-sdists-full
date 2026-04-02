from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UserOrganizationTypeCount")


@_attrs_define
class UserOrganizationTypeCount:
    """
    Attributes:
        organization_type (Union[None, str]): Organization type (SCHAC URN)
        count (int): Number of users
    """

    organization_type: Union[None, str]
    count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        organization_type: Union[None, str]
        organization_type = self.organization_type

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organization_type": organization_type,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_organization_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        organization_type = _parse_organization_type(d.pop("organization_type"))

        count = d.pop("count")

        user_organization_type_count = cls(
            organization_type=organization_type,
            count=count,
        )

        user_organization_type_count.additional_properties = d
        return user_organization_type_count

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
