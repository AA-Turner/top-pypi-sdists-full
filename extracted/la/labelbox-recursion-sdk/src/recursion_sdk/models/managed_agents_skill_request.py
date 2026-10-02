from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_skill_request_metadata import ManagedAgentsSkillRequestMetadata





T = TypeVar("T", bound="ManagedAgentsSkillRequest")



@_attrs_define
class ManagedAgentsSkillRequest:
    """ Request body for creating or updating a skill. The document is the source of truth: the skill's name and description
    come from its frontmatter. Publishing a new version of an existing skill goes through createSkillVersion, which
    mints one rather than editing the last.

        Example:
            {'display_title': 'example', 'document': 'example', 'manifest': ['example'], 'metadata': {'key': 'example'},
                'skill_group_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            document (str): The complete SKILL.md: YAML frontmatter delimited by --- on the very first line, then Markdown
                instructions. name and description are required in the frontmatter and are read from it.
            display_title (str | Unset): Human-readable title for listings. Defaults to the frontmatter name.
            manifest (list[str] | Unset): Relative paths of files bundled with the skill, listed to the model when it
                activates the skill. Paths must stay inside the skill directory.
            metadata (ManagedAgentsSkillRequestMetadata | Unset): Caller-owned key/value data stored with the skill and
                returned unchanged.
            skill_group_id (None | str | Unset): Catalog group to file this skill under. Send an empty string to remove it
                from its group; omit to leave the group unchanged. Grouping is for browsing and bulk attachment only and is
                never disclosed to the model.
     """

    document: str
    display_title: str | Unset = UNSET
    manifest: list[str] | Unset = UNSET
    metadata: ManagedAgentsSkillRequestMetadata | Unset = UNSET
    skill_group_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_skill_request_metadata import ManagedAgentsSkillRequestMetadata # noqa: PLC0415
        document = self.document

        display_title = self.display_title

        manifest: list[str] | Unset = UNSET
        if not isinstance(self.manifest, Unset):
            manifest = self.manifest



        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        skill_group_id: None | str | Unset
        if isinstance(self.skill_group_id, Unset):
            skill_group_id = UNSET
        else:
            skill_group_id = self.skill_group_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "document": document,
        })
        if display_title is not UNSET:
            field_dict["display_title"] = display_title
        if manifest is not UNSET:
            field_dict["manifest"] = manifest
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if skill_group_id is not UNSET:
            field_dict["skill_group_id"] = skill_group_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_skill_request_metadata import ManagedAgentsSkillRequestMetadata # noqa: PLC0415
        d = dict(src_dict)
        document = d.pop("document")

        display_title = d.pop("display_title", UNSET)

        manifest = cast(list[str], d.pop("manifest", UNSET))


        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsSkillRequestMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsSkillRequestMetadata.from_dict(_metadata)




        def _parse_skill_group_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        skill_group_id = _parse_skill_group_id(d.pop("skill_group_id", UNSET))


        managed_agents_skill_request = cls(
            document=document,
            display_title=display_title,
            manifest=manifest,
            metadata=metadata,
            skill_group_id=skill_group_id,
        )


        managed_agents_skill_request.additional_properties = d
        return managed_agents_skill_request

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
