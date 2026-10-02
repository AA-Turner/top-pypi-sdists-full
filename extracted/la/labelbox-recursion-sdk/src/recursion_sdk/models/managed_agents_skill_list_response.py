from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_skill import ManagedAgentsSkill





T = TypeVar("T", bound="ManagedAgentsSkillListResponse")



@_attrs_define
class ManagedAgentsSkillListResponse:
    """ Response body of GET /v1/skills. Paged: read to the end by following next_page_token until it is absent. Each row
    carries the name and description an agent's prompt discloses, but not the instructions, which are read one version
    at a time.

        Example:
            {'next_page_token': 'example', 'skills': [{'created_at': '2026-02-18T09:30:00Z', 'description': 'example',
                'display_title': 'example', 'latest_instruction_chars': 1, 'latest_skill_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'latest_version_number': 1, 'metadata': {'key': 'example'}, 'name':
                'example-name', 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'skill_group_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'skill_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'source': 'example',
                'updated_at': '2026-02-18T09:30:00Z'}]}

        Attributes:
            skills (list[ManagedAgentsSkill] | None): One page of matching skills, newest first. Soft-deleted skills are
                omitted.
            next_page_token (str | Unset): Present when more skills match. Pass it as page_token with the same filters and
                limit to read the next page. Absent on the last page.
     """

    skills: list[ManagedAgentsSkill] | None
    next_page_token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_skill import ManagedAgentsSkill # noqa: PLC0415
        skills: list[dict[str, Any]] | None
        if isinstance(self.skills, list):
            skills = []
            for skills_type_0_item_data in self.skills:
                skills_type_0_item = skills_type_0_item_data.to_dict()
                skills.append(skills_type_0_item)


        else:
            skills = self.skills

        next_page_token = self.next_page_token


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "skills": skills,
        })
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_skill import ManagedAgentsSkill # noqa: PLC0415
        d = dict(src_dict)
        def _parse_skills(data: object) -> list[ManagedAgentsSkill] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                skills_type_0 = []
                _skills_type_0 = data
                for skills_type_0_item_data in (_skills_type_0):
                    skills_type_0_item = ManagedAgentsSkill.from_dict(skills_type_0_item_data)



                    skills_type_0.append(skills_type_0_item)

                return skills_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsSkill] | None, data)

        skills = _parse_skills(d.pop("skills"))


        next_page_token = d.pop("next_page_token", UNSET)

        managed_agents_skill_list_response = cls(
            skills=skills,
            next_page_token=next_page_token,
        )


        managed_agents_skill_list_response.additional_properties = d
        return managed_agents_skill_list_response

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
