from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_skill_version import ManagedAgentsSkillVersion





T = TypeVar("T", bound="ManagedAgentsSkillVersionListResponse")



@_attrs_define
class ManagedAgentsSkillVersionListResponse:
    """ Response body of GET /v1/skills/{skill_id}/versions. Versions are immutable snapshots of the document: pin one on an
    agent to keep what its sessions run under fixed. Instructions are omitted here and returned when reading a single
    version.

        Example:
            {'skill_versions': [{'artifact_sha256': 'example', 'bundle': {'bytes': 1, 'entries': [{'bytes': 1, 'mode': 1,
                'path': 'example', 'sha256': 'example'}], 'sha256': 'example'}, 'created_at': '2026-02-18T09:30:00Z',
                'created_by': 'example', 'description': 'example', 'entrypoint_path': 'example', 'file_manifest': ['example'],
                'frontmatter': {'key': 'example'}, 'instructions': 'example', 'metadata': {'key': 'example'}, 'name': 'example-
                name', 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'skill_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'skill_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'version_number': 1}]}

        Attributes:
            skill_versions (list[ManagedAgentsSkillVersion] | None): Every published version of the requested skill, newest
                first.
     """

    skill_versions: list[ManagedAgentsSkillVersion] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_skill_version import ManagedAgentsSkillVersion # noqa: PLC0415
        skill_versions: list[dict[str, Any]] | None
        if isinstance(self.skill_versions, list):
            skill_versions = []
            for skill_versions_type_0_item_data in self.skill_versions:
                skill_versions_type_0_item = skill_versions_type_0_item_data.to_dict()
                skill_versions.append(skill_versions_type_0_item)


        else:
            skill_versions = self.skill_versions


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "skill_versions": skill_versions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_skill_version import ManagedAgentsSkillVersion # noqa: PLC0415
        d = dict(src_dict)
        def _parse_skill_versions(data: object) -> list[ManagedAgentsSkillVersion] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                skill_versions_type_0 = []
                _skill_versions_type_0 = data
                for skill_versions_type_0_item_data in (_skill_versions_type_0):
                    skill_versions_type_0_item = ManagedAgentsSkillVersion.from_dict(skill_versions_type_0_item_data)



                    skill_versions_type_0.append(skill_versions_type_0_item)

                return skill_versions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsSkillVersion] | None, data)

        skill_versions = _parse_skill_versions(d.pop("skill_versions"))


        managed_agents_skill_version_list_response = cls(
            skill_versions=skill_versions,
        )


        managed_agents_skill_version_list_response.additional_properties = d
        return managed_agents_skill_version_list_response

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
