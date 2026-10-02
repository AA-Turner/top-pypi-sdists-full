from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedAccessSubnetRequest")


@_attrs_define
class PatchedAccessSubnetRequest:
    """
    Attributes:
        inet (Union[Unset, str]):
        description (Union[Unset, str]):
        applies_to_portal (Union[Unset, bool]): Whether this network may sign in to the portal on behalf of the
            organization. Off by default: any portal-scoped entry restricts sign-in for everyone in the organization.
        offerings (Union[Unset, list[UUID]]): UUIDs of offerings this network may reach. Only offerings the organization
            consumes and that enable access subnets are accepted.
    """

    inet: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    applies_to_portal: Union[Unset, bool] = UNSET
    offerings: Union[Unset, list[UUID]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        inet = self.inet

        description = self.description

        applies_to_portal = self.applies_to_portal

        offerings: Union[Unset, list[str]] = UNSET
        if not isinstance(self.offerings, Unset):
            offerings = []
            for offerings_item_data in self.offerings:
                offerings_item = str(offerings_item_data)
                offerings.append(offerings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if inet is not UNSET:
            field_dict["inet"] = inet
        if description is not UNSET:
            field_dict["description"] = description
        if applies_to_portal is not UNSET:
            field_dict["applies_to_portal"] = applies_to_portal
        if offerings is not UNSET:
            field_dict["offerings"] = offerings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        inet = d.pop("inet", UNSET)

        description = d.pop("description", UNSET)

        applies_to_portal = d.pop("applies_to_portal", UNSET)

        offerings = []
        _offerings = d.pop("offerings", UNSET)
        for offerings_item_data in _offerings or []:
            offerings_item = UUID(offerings_item_data)

            offerings.append(offerings_item)

        patched_access_subnet_request = cls(
            inet=inet,
            description=description,
            applies_to_portal=applies_to_portal,
            offerings=offerings,
        )

        patched_access_subnet_request.additional_properties = d
        return patched_access_subnet_request

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
