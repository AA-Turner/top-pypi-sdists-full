from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_skill_group import ManagedAgentsSkillGroup





T = TypeVar("T", bound="ManagedAgentsSkillGroupListResponse")



@_attrs_define
class ManagedAgentsSkillGroupListResponse:
    """ Response body of GET /v1/skill-groups. Paged: read to the end by following next_page_token until it is absent. Each
    row carries how many live skills are filed under the group, so a catalog listing can show the size of a folder it
    has not opened.

        Example:
            {'next_page_token': 'example', 'skill_groups': [{'created_at': '2026-02-18T09:30:00Z', 'description': 'example',
                'display_title': 'example', 'metadata': {'key': 'example'}, 'name': 'example-name', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'skill_count': 1, 'skill_group_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at': '2026-02-18T09:30:00Z'}]}

        Attributes:
            skill_groups (list[ManagedAgentsSkillGroup] | None): One page of the caller's skill groups, newest first.
            next_page_token (str | Unset): Present when more groups exist. Pass it as page_token with the same limit to read
                the next page. Absent on the last page.
     """

    skill_groups: list[ManagedAgentsSkillGroup] | None
    next_page_token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_skill_group import ManagedAgentsSkillGroup # noqa: PLC0415
        skill_groups: list[dict[str, Any]] | None
        if isinstance(self.skill_groups, list):
            skill_groups = []
            for skill_groups_type_0_item_data in self.skill_groups:
                skill_groups_type_0_item = skill_groups_type_0_item_data.to_dict()
                skill_groups.append(skill_groups_type_0_item)


        else:
            skill_groups = self.skill_groups

        next_page_token = self.next_page_token


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "skill_groups": skill_groups,
        })
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_skill_group import ManagedAgentsSkillGroup # noqa: PLC0415
        d = dict(src_dict)
        def _parse_skill_groups(data: object) -> list[ManagedAgentsSkillGroup] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                skill_groups_type_0 = []
                _skill_groups_type_0 = data
                for skill_groups_type_0_item_data in (_skill_groups_type_0):
                    skill_groups_type_0_item = ManagedAgentsSkillGroup.from_dict(skill_groups_type_0_item_data)



                    skill_groups_type_0.append(skill_groups_type_0_item)

                return skill_groups_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsSkillGroup] | None, data)

        skill_groups = _parse_skill_groups(d.pop("skill_groups"))


        next_page_token = d.pop("next_page_token", UNSET)

        managed_agents_skill_group_list_response = cls(
            skill_groups=skill_groups,
            next_page_token=next_page_token,
        )


        managed_agents_skill_group_list_response.additional_properties = d
        return managed_agents_skill_group_list_response

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
