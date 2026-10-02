from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="CreateAgentSkillDto")



@_attrs_define
class CreateAgentSkillDto:
    """ Request body to create an org skill (or a platform skill when platform=true).

        Example:
            {'slug': 'xlsx', 'name': 'Excel / spreadsheet helpers', 'description': 'Read and write .xlsx workbooks from the
                agent workspace.', 'fileId': 'b8c9d0e1-f2a3-4b4c-9d5e-6f708192a3b4'}

        Attributes:
            slug (str): URL-safe skill slug unique within the owning org (or among platform skills). Lowercase alphanumeric
                with hyphens.
            name (str): Human-readable skill name.
            description (str): Short description for the harness skills index.
            file_id (UUID): Previously uploaded SKILL.md bundle file id (via POST …/skills/upload or the signed-upload +
                finalize path).
            platform (bool | Unset): When true, create a platform skill (organization_id NULL). Staff-admin only;
                ignored/rejected for non-admins.
     """

    slug: str
    name: str
    description: str
    file_id: UUID
    platform: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        slug = self.slug

        name = self.name

        description = self.description

        file_id = str(self.file_id)

        platform = self.platform


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "slug": slug,
            "name": name,
            "description": description,
            "fileId": file_id,
        })
        if platform is not UNSET:
            field_dict["platform"] = platform

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        slug = d.pop("slug")

        name = d.pop("name")

        description = d.pop("description")

        file_id = UUID(d.pop("fileId"))




        platform = d.pop("platform", UNSET)

        create_agent_skill_dto = cls(
            slug=slug,
            name=name,
            description=description,
            file_id=file_id,
            platform=platform,
        )


        create_agent_skill_dto.additional_properties = d
        return create_agent_skill_dto

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
