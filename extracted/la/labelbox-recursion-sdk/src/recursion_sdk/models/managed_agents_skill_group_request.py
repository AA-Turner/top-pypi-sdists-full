from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_skill_group_request_metadata import ManagedAgentsSkillGroupRequestMetadata





T = TypeVar("T", bound="ManagedAgentsSkillGroupRequest")



@_attrs_define
class ManagedAgentsSkillGroupRequest:
    """ Request body for creating a skill group.

        Example:
            {'description': 'example', 'display_title': 'example', 'metadata': {'key': 'example'}, 'name': 'example-name'}

        Attributes:
            name (str): The group's addressable name, lowercase letters, digits, and single hyphens, e.g. document-ops. Held
                to the same shape as a skill name so the two never disagree in a listing that shows them together.
            description (str | Unset): What this group collects, for operators browsing the catalog. Never disclosed to the
                model, so it does not need to read as a routing signal the way a skill's description does.
            display_title (str | Unset): Human-readable title for listings. Defaults to the name.
            metadata (ManagedAgentsSkillGroupRequestMetadata | Unset): Caller-owned key/value data stored with the group and
                returned unchanged.
     """

    name: str
    description: str | Unset = UNSET
    display_title: str | Unset = UNSET
    metadata: ManagedAgentsSkillGroupRequestMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_skill_group_request_metadata import ManagedAgentsSkillGroupRequestMetadata # noqa: PLC0415
        name = self.name

        description = self.description

        display_title = self.display_title

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if display_title is not UNSET:
            field_dict["display_title"] = display_title
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_skill_group_request_metadata import ManagedAgentsSkillGroupRequestMetadata # noqa: PLC0415
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        display_title = d.pop("display_title", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsSkillGroupRequestMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsSkillGroupRequestMetadata.from_dict(_metadata)




        managed_agents_skill_group_request = cls(
            name=name,
            description=description,
            display_title=display_title,
            metadata=metadata,
        )


        managed_agents_skill_group_request.additional_properties = d
        return managed_agents_skill_group_request

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
