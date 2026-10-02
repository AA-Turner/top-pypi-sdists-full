from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_skill_group_patch_request_metadata import ManagedAgentsSkillGroupPatchRequestMetadata





T = TypeVar("T", bound="ManagedAgentsSkillGroupPatchRequest")



@_attrs_define
class ManagedAgentsSkillGroupPatchRequest:
    """ Request body for updating a skill group. An omitted field is left unchanged.

        Example:
            {'description': 'example', 'display_title': 'example', 'metadata': {'key': 'example'}, 'name': 'example-name'}

        Attributes:
            description (str | Unset): What this group collects, for operators browsing the catalog. Omit to leave
                unchanged.
            display_title (str | Unset): Human-readable title for listings. Omit to leave unchanged.
            metadata (ManagedAgentsSkillGroupPatchRequestMetadata | Unset): Caller-owned key/value data stored with the
                group. Omit to leave unchanged.
            name (str | Unset): The group's addressable name, lowercase letters, digits, and single hyphens. Omit to leave
                unchanged.
     """

    description: str | Unset = UNSET
    display_title: str | Unset = UNSET
    metadata: ManagedAgentsSkillGroupPatchRequestMetadata | Unset = UNSET
    name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_skill_group_patch_request_metadata import ManagedAgentsSkillGroupPatchRequestMetadata # noqa: PLC0415
        description = self.description

        display_title = self.display_title

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        name = self.name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if description is not UNSET:
            field_dict["description"] = description
        if display_title is not UNSET:
            field_dict["display_title"] = display_title
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_skill_group_patch_request_metadata import ManagedAgentsSkillGroupPatchRequestMetadata # noqa: PLC0415
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        display_title = d.pop("display_title", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsSkillGroupPatchRequestMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsSkillGroupPatchRequestMetadata.from_dict(_metadata)




        name = d.pop("name", UNSET)

        managed_agents_skill_group_patch_request = cls(
            description=description,
            display_title=display_title,
            metadata=metadata,
            name=name,
        )


        managed_agents_skill_group_patch_request.additional_properties = d
        return managed_agents_skill_group_patch_request

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
