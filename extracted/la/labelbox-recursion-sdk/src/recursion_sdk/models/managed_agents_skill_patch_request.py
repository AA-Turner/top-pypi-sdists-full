from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsSkillPatchRequest")



@_attrs_define
class ManagedAgentsSkillPatchRequest:
    """ Request body for refiling a skill between catalog groups. Filing is not authoring: this leaves the skill's versions
    untouched and mints nothing. Publish new content with createSkillVersion.

        Example:
            {'skill_group_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            skill_group_id (str): Catalog group to file this skill under. Send an empty string to remove it from its group.
                Grouping is for browsing and bulk attachment only and is never disclosed to the model.
     """

    skill_group_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        skill_group_id = self.skill_group_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "skill_group_id": skill_group_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        skill_group_id = d.pop("skill_group_id")

        managed_agents_skill_patch_request = cls(
            skill_group_id=skill_group_id,
        )


        managed_agents_skill_patch_request.additional_properties = d
        return managed_agents_skill_patch_request

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
