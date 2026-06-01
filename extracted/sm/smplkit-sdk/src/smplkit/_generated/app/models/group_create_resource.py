from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.group_create_resource_type import check_group_create_resource_type
from ..models.group_create_resource_type import GroupCreateResourceType

if TYPE_CHECKING:
    from ..models.group import Group


T = TypeVar("T", bound="GroupCreateResource")


@_attrs_define
class GroupCreateResource:
    """JSON:API resource envelope for creating a group (id required).

    Example:
        {'attributes': {'description': 'Senior engineers who may change production.', 'managed_environments':
            ['production'], 'name': 'Production Stewards'}, 'id': 'production_stewards', 'type': 'group'}

    Attributes:
        id (str): Client-supplied resource id.
        type_ (GroupCreateResourceType):
        attributes (Group): An Environment Access Group: a named bundle of standard
            environments its members may manage.

            A user's effective managed-environment set is the union across all
            their groups (or "all" if any of their groups grants ``["*"]``).
            Roles answer *what* a user may do; groups answer *which environments*
            that capability reaches. Example: {'created_at': '2026-05-26T11:02:16.616Z', 'description': 'Senior engineers
            who may change production.', 'managed_environments': ['production'], 'name': 'Production Stewards', 'system':
            False, 'updated_at': '2026-05-26T11:02:16.616Z'}.
    """

    id: str
    type_: GroupCreateResourceType
    attributes: Group
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_: str = self.type_

        attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.group import Group

        d = dict(src_dict)
        id = d.pop("id")

        type_ = check_group_create_resource_type(d.pop("type"))

        attributes = Group.from_dict(d.pop("attributes"))

        group_create_resource = cls(
            id=id,
            type_=type_,
            attributes=attributes,
        )

        group_create_resource.additional_properties = d
        return group_create_resource

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
