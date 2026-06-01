from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.group_create_resource import GroupCreateResource


T = TypeVar("T", bound="GroupCreateRequest")


@_attrs_define
class GroupCreateRequest:
    """JSON:API request envelope for creating a group.

    Distinct from :class:`GroupRequest` because create requires
    caller-supplied ``data.id`` while update does not.

        Attributes:
            data (GroupCreateResource): JSON:API resource envelope for creating a group (id required). Example:
                {'attributes': {'description': 'Senior engineers who may change production.', 'managed_environments':
                ['production'], 'name': 'Production Stewards'}, 'id': 'production_stewards', 'type': 'group'}.
    """

    data: GroupCreateResource
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
        from ..models.group_create_resource import GroupCreateResource

        d = dict(src_dict)
        data = GroupCreateResource.from_dict(d.pop("data"))

        group_create_request = cls(
            data=data,
        )

        group_create_request.additional_properties = d
        return group_create_request

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
