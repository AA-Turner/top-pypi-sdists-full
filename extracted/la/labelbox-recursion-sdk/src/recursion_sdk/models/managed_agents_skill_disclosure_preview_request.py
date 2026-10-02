from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_skill_disclosure_preview_request_skills_type_0_item import ManagedAgentsSkillDisclosurePreviewRequestSkillsType0Item





T = TypeVar("T", bound="ManagedAgentsSkillDisclosurePreviewRequest")



@_attrs_define
class ManagedAgentsSkillDisclosurePreviewRequest:
    """ Request body for previewing tier-1 skill disclosure. Read-only: nothing is stored, and the attachments do not have
    to belong to any agent yet.

        Example:
            {'context_window_tokens': 1, 'skills': [{'key': 'example'}]}

        Attributes:
            skills (list[ManagedAgentsSkillDisclosurePreviewRequestSkillsType0Item] | None): The attachment list exactly as
                it would be saved on the agent, including group entries, which are expanded here the same way a session start
                expands them. Capped at the 100 skills a session can carry.
            context_window_tokens (int | Unset): The context window of the model the agent will run on. Omit to be answered
                against the conservative floor this service uses when a window is unknown.
     """

    skills: list[ManagedAgentsSkillDisclosurePreviewRequestSkillsType0Item] | None
    context_window_tokens: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_skill_disclosure_preview_request_skills_type_0_item import ManagedAgentsSkillDisclosurePreviewRequestSkillsType0Item # noqa: PLC0415
        skills: list[dict[str, Any]] | None
        if isinstance(self.skills, list):
            skills = []
            for skills_type_0_item_data in self.skills:
                skills_type_0_item = skills_type_0_item_data.to_dict()
                skills.append(skills_type_0_item)


        else:
            skills = self.skills

        context_window_tokens = self.context_window_tokens


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "skills": skills,
        })
        if context_window_tokens is not UNSET:
            field_dict["context_window_tokens"] = context_window_tokens

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_skill_disclosure_preview_request_skills_type_0_item import ManagedAgentsSkillDisclosurePreviewRequestSkillsType0Item # noqa: PLC0415
        d = dict(src_dict)
        def _parse_skills(data: object) -> list[ManagedAgentsSkillDisclosurePreviewRequestSkillsType0Item] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                skills_type_0 = []
                _skills_type_0 = data
                for skills_type_0_item_data in (_skills_type_0):
                    skills_type_0_item = ManagedAgentsSkillDisclosurePreviewRequestSkillsType0Item.from_dict(skills_type_0_item_data)



                    skills_type_0.append(skills_type_0_item)

                return skills_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsSkillDisclosurePreviewRequestSkillsType0Item] | None, data)

        skills = _parse_skills(d.pop("skills"))


        context_window_tokens = d.pop("context_window_tokens", UNSET)

        managed_agents_skill_disclosure_preview_request = cls(
            skills=skills,
            context_window_tokens=context_window_tokens,
        )


        managed_agents_skill_disclosure_preview_request.additional_properties = d
        return managed_agents_skill_disclosure_preview_request

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
