from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.group_membership_resource import GroupMembershipResource


T = TypeVar("T", bound="GroupMembershipRequest")


@_attrs_define
class GroupMembershipRequest:
    """JSON:API request envelope for creating a group membership.

    Memberships have no mutable attributes, so this envelope is used
    only on POST. There is no PUT/PATCH on the membership resource.

        Attributes:
            data (GroupMembershipResource): JSON:API resource envelope for a group membership.

                `id` is server-assigned and must not be specified on create. Example: {'attributes': {'created_at':
                '2026-05-26T11:02:16.616Z', 'group': 'production_stewards', 'updated_at': '2026-05-26T11:02:16.616Z', 'user':
                'd290f1ee-6c54-4b01-90e6-d701748f0851'}, 'id': 'f7c1d2e3-4b5a-6789-0123-456789abcdef', 'type':
                'group_membership'}.
    """

    data: GroupMembershipResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.group_membership_resource import GroupMembershipResource

        d = dict(src_dict)
        data = GroupMembershipResource.from_dict(d.pop("data"))

        group_membership_request = cls(
            data=data,
        )

        group_membership_request.additional_properties = d
        return group_membership_request

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
