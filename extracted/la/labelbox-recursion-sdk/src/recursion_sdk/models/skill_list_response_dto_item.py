from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SkillListResponseDtoItem")



@_attrs_define
class SkillListResponseDtoItem:
    """ 
        Attributes:
            name (str): Skill name (filename stem) — pass it to the install command, e.g. "recursion".
            description (str): One-line summary taken from the skill's frontmatter (may be empty).
     """

    name: str
    description: str





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
            "description": description,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        skill_list_response_dto_item = cls(
            name=name,
            description=description,
        )

        return skill_list_response_dto_item

