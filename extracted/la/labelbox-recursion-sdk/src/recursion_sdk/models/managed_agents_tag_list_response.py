from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_tag import ManagedAgentsTag





T = TypeVar("T", bound="ManagedAgentsTagListResponse")



@_attrs_define
class ManagedAgentsTagListResponse:
    """ A complete set of organization-scoped tag definitions. GET /v1/tags returns the organization catalog; agent tag PUT
    routes return the agent's resulting exact set.

        Example:
            {'tags': [{'color': '#14b8a6', 'created_at': '2026-02-18T09:30:00Z', 'description': 'example', 'label':
                'example', 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tag_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at': '2026-02-18T09:30:00Z'}]}

        Attributes:
            tags (list[ManagedAgentsTag]): The complete live tag set for this response. Always an array; an empty array
                means no definitions exist or the agent has no classifications.
     """

    tags: list[ManagedAgentsTag]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_tag import ManagedAgentsTag # noqa: PLC0415
        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "tags": tags,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_tag import ManagedAgentsTag # noqa: PLC0415
        d = dict(src_dict)
        tags = []
        _tags = d.pop("tags")
        for tags_item_data in (_tags):
            tags_item = ManagedAgentsTag.from_dict(tags_item_data)



            tags.append(tags_item)


        managed_agents_tag_list_response = cls(
            tags=tags,
        )


        managed_agents_tag_list_response.additional_properties = d
        return managed_agents_tag_list_response

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
