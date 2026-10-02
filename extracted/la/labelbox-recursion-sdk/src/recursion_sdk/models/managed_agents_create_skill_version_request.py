from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.managed_agents_create_skill_version_request_metadata import ManagedAgentsCreateSkillVersionRequestMetadata





T = TypeVar("T", bound="ManagedAgentsCreateSkillVersionRequest")



@_attrs_define
class ManagedAgentsCreateSkillVersionRequest:
    """ Request body for creating a new immutable skill version. Every field means what it means on createSkill -- full
    content is always required, there is no partial update. base_skill_version_id must be the skill's current version or
    the request is rejected with revision_conflict so the caller can re-read and retry.

        Example:
            {'base_skill_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'display_title': 'example', 'document':
                'example', 'manifest': ['example'], 'metadata': {'key': 'example'}}

        Attributes:
            base_skill_version_id (UUID): The skill's current latest_skill_version_id, as returned by getSkill. Rejected
                with 409 revision_conflict if the skill has moved past this version.
            document (str): The complete SKILL.md: YAML frontmatter delimited by --- on the very first line, then Markdown
                instructions. name and description are required in the frontmatter and are read from it.
            display_title (str | Unset): Human-readable title for listings. Defaults to the frontmatter name.
            manifest (list[str] | Unset): Relative paths of files bundled with the skill, listed to the model when it
                activates the skill. Paths must stay inside the skill directory.
            metadata (ManagedAgentsCreateSkillVersionRequestMetadata | Unset): Caller-owned key/value data stored with the
                skill and returned unchanged.
     """

    base_skill_version_id: UUID
    document: str
    display_title: str | Unset = UNSET
    manifest: list[str] | Unset = UNSET
    metadata: ManagedAgentsCreateSkillVersionRequestMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_create_skill_version_request_metadata import ManagedAgentsCreateSkillVersionRequestMetadata # noqa: PLC0415
        base_skill_version_id = str(self.base_skill_version_id)

        document = self.document

        display_title = self.display_title

        manifest: list[str] | Unset = UNSET
        if not isinstance(self.manifest, Unset):
            manifest = self.manifest



        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "base_skill_version_id": base_skill_version_id,
            "document": document,
        })
        if display_title is not UNSET:
            field_dict["display_title"] = display_title
        if manifest is not UNSET:
            field_dict["manifest"] = manifest
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_create_skill_version_request_metadata import ManagedAgentsCreateSkillVersionRequestMetadata # noqa: PLC0415
        d = dict(src_dict)
        base_skill_version_id = UUID(d.pop("base_skill_version_id"))




        document = d.pop("document")

        display_title = d.pop("display_title", UNSET)

        manifest = cast(list[str], d.pop("manifest", UNSET))


        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsCreateSkillVersionRequestMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsCreateSkillVersionRequestMetadata.from_dict(_metadata)




        managed_agents_create_skill_version_request = cls(
            base_skill_version_id=base_skill_version_id,
            document=document,
            display_title=display_title,
            manifest=manifest,
            metadata=metadata,
        )


        managed_agents_create_skill_version_request.additional_properties = d
        return managed_agents_create_skill_version_request

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
