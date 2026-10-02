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
  from ..models.managed_agents_skill_group_metadata import ManagedAgentsSkillGroupMetadata





T = TypeVar("T", bound="ManagedAgentsSkillGroup")



@_attrs_define
class ManagedAgentsSkillGroup:
    """ A folder of skills, for browsing a large catalog and for attaching a whole set to an agent in one entry. Attaching a
    group resolves to its members when a session starts, so adding a skill to the group reaches every agent already
    attached to it. Groups are never disclosed to the model.

        Example:
            {'created_at': '2026-02-18T09:30:00Z', 'description': 'example', 'display_title': 'example', 'metadata': {'key':
                'example'}, 'name': 'example-name', 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'skill_count': 1,
                'skill_group_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at': '2026-02-18T09:30:00Z'}

        Attributes:
            created_at (datetime.datetime): Server-assigned RFC 3339 timestamp of when the group was created.
            name (str): The group's addressable name, lowercase with single hyphens, e.g. document-ops.
            organization_id (str): Organization that owns the group. Server-assigned from the caller's credentials; a value
                sent in a request body is ignored.
            skill_count (int): How many live skills are currently filed under this group. Derived on read.
            skill_group_id (str): Server-assigned id of the group, used in the skill-group routes and when attaching a whole
                group to an agent.
            updated_at (datetime.datetime): Server-assigned RFC 3339 timestamp of the most recent update to the group.
            description (str | Unset): What this group collects, for operators browsing the catalog. Never disclosed to the
                model.
            display_title (str | Unset): Human-readable title shown wherever groups are listed. Defaults to the name.
            metadata (ManagedAgentsSkillGroupMetadata | Unset): Caller-owned key/value data stored with the group and
                returned unchanged.
     """

    created_at: datetime.datetime
    name: str
    organization_id: str
    skill_count: int
    skill_group_id: str
    updated_at: datetime.datetime
    description: str | Unset = UNSET
    display_title: str | Unset = UNSET
    metadata: ManagedAgentsSkillGroupMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_skill_group_metadata import ManagedAgentsSkillGroupMetadata # noqa: PLC0415
        created_at = self.created_at.isoformat()

        name = self.name

        organization_id = self.organization_id

        skill_count = self.skill_count

        skill_group_id = self.skill_group_id

        updated_at = self.updated_at.isoformat()

        description = self.description

        display_title = self.display_title

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "name": name,
            "organization_id": organization_id,
            "skill_count": skill_count,
            "skill_group_id": skill_group_id,
            "updated_at": updated_at,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if display_title is not UNSET:
            field_dict["display_title"] = display_title
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_skill_group_metadata import ManagedAgentsSkillGroupMetadata # noqa: PLC0415
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        name = d.pop("name")

        organization_id = d.pop("organization_id")

        skill_count = d.pop("skill_count")

        skill_group_id = d.pop("skill_group_id")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        description = d.pop("description", UNSET)

        display_title = d.pop("display_title", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsSkillGroupMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsSkillGroupMetadata.from_dict(_metadata)




        managed_agents_skill_group = cls(
            created_at=created_at,
            name=name,
            organization_id=organization_id,
            skill_count=skill_count,
            skill_group_id=skill_group_id,
            updated_at=updated_at,
            description=description,
            display_title=display_title,
            metadata=metadata,
        )


        managed_agents_skill_group.additional_properties = d
        return managed_agents_skill_group

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
