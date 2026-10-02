from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="UpdateAgentSkillDto")



@_attrs_define
class UpdateAgentSkillDto:
    """ Request body to partially update a skill. Slug is immutable.

        Example:
            {'name': 'Excel / spreadsheet helpers', 'description': 'Updated short description for the harness skills
                index.', 'fileId': 'b8c9d0e1-f2a3-4b4c-9d5e-6f708192a3b4'}

        Attributes:
            name (str | Unset): Updated human-readable skill name.
            description (str | Unset): Updated short description for the harness skills index.
            file_id (UUID | Unset): Replacement SKILL.md bundle file id. Mutable by design — editing affects every
                referencing agent on its next turn.
     """

    name: str | Unset = UNSET
    description: str | Unset = UNSET
    file_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        file_id: str | Unset = UNSET
        if not isinstance(self.file_id, Unset):
            file_id = str(self.file_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if file_id is not UNSET:
            field_dict["fileId"] = file_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _file_id = d.pop("fileId", UNSET)
        file_id: UUID | Unset
        if isinstance(_file_id,  Unset):
            file_id = UNSET
        else:
            file_id = UUID(_file_id)




        update_agent_skill_dto = cls(
            name=name,
            description=description,
            file_id=file_id,
        )


        update_agent_skill_dto.additional_properties = d
        return update_agent_skill_dto

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
