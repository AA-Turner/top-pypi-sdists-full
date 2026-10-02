from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_skill_metadata import ManagedAgentsSkillMetadata





T = TypeVar("T", bound="ManagedAgentsSkill")



@_attrs_define
class ManagedAgentsSkill:
    """ A reusable procedure an agent loads when it judges the procedure relevant. Its name and description are disclosed in
    every turn; the instructions enter the conversation only when the agent activates it. Updating a skill mints a new
    immutable SkillVersion.

        Example:
            {'created_at': '2026-02-18T09:30:00Z', 'description': 'example', 'display_title': 'example',
                'latest_instruction_chars': 1, 'latest_skill_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'latest_version_number': 1, 'metadata': {'key': 'example'}, 'name': 'example-name', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'skill_group_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'skill_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'source': 'example', 'updated_at': '2026-02-18T09:30:00Z'}

        Attributes:
            created_at (datetime.datetime): Server-assigned RFC 3339 timestamp of when the skill was created.
            description (str): When to use this skill. Disclosed to the model in every turn, so it is the whole routing
                signal: write it as the condition under which the skill applies.
            name (str): The skill's addressable name, lowercase with single hyphens, e.g. cut-release. This is what an agent
                passes to the activation tool.
            organization_id (str): Organization that owns the skill. Server-assigned from the caller's credentials; a value
                sent in a request body is ignored.
            skill_id (str): Server-assigned id of the skill, used in the skill and skill-version routes.
            source (str): Where the skill came from: platform, organization, or repository. Decides which skill wins a name
                collision, most specific first.
            updated_at (datetime.datetime): Server-assigned RFC 3339 timestamp of the most recent update to the skill.
            display_title (str | Unset): Human-readable title shown wherever skills are listed. Defaults to the name.
            latest_instruction_chars (int | Unset): Length in characters of the newest version's instructions, the body
                disclosed to the model when it activates the skill. Zero for a skill with no version yet. Instructions are
                truncated at 64000 characters when a session assembles them.
            latest_skill_version_id (str | Unset): Server-maintained id of the newest version of this skill; agents that
                attach it without pinning a version use this one.
            latest_version_number (int | Unset): How many versions this skill has, which is also the number of the newest
                one, since versions are numbered from 1 in creation order. Zero for a skill with no version yet.
            metadata (ManagedAgentsSkillMetadata | Unset): Caller-owned key/value data stored with the skill and returned
                unchanged.
            skill_group_id (str | Unset): Catalog group this skill is filed under, if any. Grouping is for browsing and for
                attaching a set of skills to an agent in one entry; it is never disclosed to the model and does not scope the
                skill's name.
     """

    created_at: datetime.datetime
    description: str
    name: str
    organization_id: str
    skill_id: str
    source: str
    updated_at: datetime.datetime
    display_title: str | Unset = UNSET
    latest_instruction_chars: int | Unset = UNSET
    latest_skill_version_id: str | Unset = UNSET
    latest_version_number: int | Unset = UNSET
    metadata: ManagedAgentsSkillMetadata | Unset = UNSET
    skill_group_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_skill_metadata import ManagedAgentsSkillMetadata # noqa: PLC0415
        created_at = self.created_at.isoformat()

        description = self.description

        name = self.name

        organization_id = self.organization_id

        skill_id = self.skill_id

        source = self.source

        updated_at = self.updated_at.isoformat()

        display_title = self.display_title

        latest_instruction_chars = self.latest_instruction_chars

        latest_skill_version_id = self.latest_skill_version_id

        latest_version_number = self.latest_version_number

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        skill_group_id = self.skill_group_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "description": description,
            "name": name,
            "organization_id": organization_id,
            "skill_id": skill_id,
            "source": source,
            "updated_at": updated_at,
        })
        if display_title is not UNSET:
            field_dict["display_title"] = display_title
        if latest_instruction_chars is not UNSET:
            field_dict["latest_instruction_chars"] = latest_instruction_chars
        if latest_skill_version_id is not UNSET:
            field_dict["latest_skill_version_id"] = latest_skill_version_id
        if latest_version_number is not UNSET:
            field_dict["latest_version_number"] = latest_version_number
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if skill_group_id is not UNSET:
            field_dict["skill_group_id"] = skill_group_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_skill_metadata import ManagedAgentsSkillMetadata # noqa: PLC0415
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        description = d.pop("description")

        name = d.pop("name")

        organization_id = d.pop("organization_id")

        skill_id = d.pop("skill_id")

        source = d.pop("source")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        display_title = d.pop("display_title", UNSET)

        latest_instruction_chars = d.pop("latest_instruction_chars", UNSET)

        latest_skill_version_id = d.pop("latest_skill_version_id", UNSET)

        latest_version_number = d.pop("latest_version_number", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsSkillMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsSkillMetadata.from_dict(_metadata)




        skill_group_id = d.pop("skill_group_id", UNSET)

        managed_agents_skill = cls(
            created_at=created_at,
            description=description,
            name=name,
            organization_id=organization_id,
            skill_id=skill_id,
            source=source,
            updated_at=updated_at,
            display_title=display_title,
            latest_instruction_chars=latest_instruction_chars,
            latest_skill_version_id=latest_skill_version_id,
            latest_version_number=latest_version_number,
            metadata=metadata,
            skill_group_id=skill_group_id,
        )


        managed_agents_skill.additional_properties = d
        return managed_agents_skill

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
