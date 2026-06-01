from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.group_resource_type import check_group_resource_type
from ..models.group_resource_type import GroupResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.group import Group


T = TypeVar("T", bound="GroupResource")


@_attrs_define
class GroupResource:
    """JSON:API resource envelope for a group.

    Example:
        {'attributes': {'created_at': '2026-05-26T11:02:16.616Z', 'description': 'Senior engineers who may change
            production.', 'managed_environments': ['production'], 'name': 'Production Stewards', 'system': False,
            'updated_at': '2026-05-26T11:02:16.616Z'}, 'id': 'production_stewards', 'type': 'group'}

    Attributes:
        type_ (GroupResourceType):
        attributes (Group): An Environment Access Group: a named bundle of standard
            environments its members may manage.

            A user's effective managed-environment set is the union across all
            their groups (or "all" if any of their groups grants ``["*"]``).
            Roles answer *what* a user may do; groups answer *which environments*
            that capability reaches. Example: {'created_at': '2026-05-26T11:02:16.616Z', 'description': 'Senior engineers
            who may change production.', 'managed_environments': ['production'], 'name': 'Production Stewards', 'system':
            False, 'updated_at': '2026-05-26T11:02:16.616Z'}.
        id (None | str | Unset):
    """

    type_: GroupResourceType
    attributes: Group
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.group import Group

        d = dict(src_dict)
        type_ = check_group_resource_type(d.pop("type"))

        attributes = Group.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        group_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        group_resource.additional_properties = d
        return group_resource

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
