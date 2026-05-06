from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectAffiliatedOrganizationsUpdateRequest")


@_attrs_define
class ProjectAffiliatedOrganizationsUpdateRequest:
    """
    Attributes:
        affiliated_organizations (Union[Unset, list[UUID]]):
    """

    affiliated_organizations: Union[Unset, list[UUID]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        affiliated_organizations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.affiliated_organizations, Unset):
            affiliated_organizations = []
            for affiliated_organizations_item_data in self.affiliated_organizations:
                affiliated_organizations_item = str(affiliated_organizations_item_data)
                affiliated_organizations.append(affiliated_organizations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if affiliated_organizations is not UNSET:
            field_dict["affiliated_organizations"] = affiliated_organizations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        affiliated_organizations = []
        _affiliated_organizations = d.pop("affiliated_organizations", UNSET)
        for affiliated_organizations_item_data in _affiliated_organizations or []:
            affiliated_organizations_item = UUID(affiliated_organizations_item_data)

            affiliated_organizations.append(affiliated_organizations_item)

        project_affiliated_organizations_update_request = cls(
            affiliated_organizations=affiliated_organizations,
        )

        project_affiliated_organizations_update_request.additional_properties = d
        return project_affiliated_organizations_update_request

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
