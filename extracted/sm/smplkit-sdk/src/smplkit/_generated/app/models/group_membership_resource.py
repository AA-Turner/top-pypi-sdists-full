from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.group_membership_resource_type import check_group_membership_resource_type
from ..models.group_membership_resource_type import GroupMembershipResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.group_membership import GroupMembership


T = TypeVar("T", bound="GroupMembershipResource")


@_attrs_define
class GroupMembershipResource:
    """JSON:API resource envelope for a group membership.

    `id` is server-assigned and must not be specified on create.

        Example:
            {'attributes': {'created_at': '2026-05-26T11:02:16.616Z', 'group': 'production_stewards', 'updated_at':
                '2026-05-26T11:02:16.616Z', 'user': 'd290f1ee-6c54-4b01-90e6-d701748f0851'}, 'id':
                'f7c1d2e3-4b5a-6789-0123-456789abcdef', 'type': 'group_membership'}

        Attributes:
            type_ (GroupMembershipResourceType):
            attributes (GroupMembership): A single (user, group) link inside an account.

                Adding a user to a group creates one membership; removing them
                deletes one. Memberships are create-and-delete only — they expose
                no mutable attributes. The unique constraint on (account, user,
                group) makes a duplicate add a 409. Example: {'created_at': '2026-05-26T11:02:16.616Z', 'group':
                'production_stewards', 'updated_at': '2026-05-26T11:02:16.616Z', 'user':
                'd290f1ee-6c54-4b01-90e6-d701748f0851'}.
            id (None | str | Unset):
    """

    type_: GroupMembershipResourceType
    attributes: GroupMembership
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
        from ..models.group_membership import GroupMembership

        d = dict(src_dict)
        type_ = check_group_membership_resource_type(d.pop("type"))

        attributes = GroupMembership.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        group_membership_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        group_membership_resource.additional_properties = d
        return group_membership_resource

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
