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
  from ..models.managed_agents_skill_bundle import ManagedAgentsSkillBundle
  from ..models.managed_agents_skill_version_frontmatter import ManagedAgentsSkillVersionFrontmatter
  from ..models.managed_agents_skill_version_metadata import ManagedAgentsSkillVersionMetadata





T = TypeVar("T", bound="ManagedAgentsSkillVersion")



@_attrs_define
class ManagedAgentsSkillVersion:
    """ An immutable snapshot of a skill's document and metadata, minted on every update. An agent may pin one, so that what
    a session runs cannot change under it.

        Example:
            {'artifact_sha256': 'example', 'bundle': {'bytes': 1, 'entries': [{'bytes': 1, 'mode': 1, 'path': 'example',
                'sha256': 'example'}], 'sha256': 'example'}, 'created_at': '2026-02-18T09:30:00Z', 'created_by': 'example',
                'description': 'example', 'entrypoint_path': 'example', 'file_manifest': ['example'], 'frontmatter': {'key':
                'example'}, 'instructions': 'example', 'metadata': {'key': 'example'}, 'name': 'example-name',
                'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'skill_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'skill_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'version_number': 1}

        Attributes:
            created_at (datetime.datetime): Server-assigned RFC 3339 timestamp of when this version was minted.
            description (str): The skill's routing description as it stood at this version.
            name (str): The skill's addressable name as it stood at this version.
            organization_id (str): Organization that owns this record. Resolved from the API key; never accepted from the
                caller.
            skill_id (str): Skill this version belongs to.
            skill_version_id (str): Identifier for this skill version. Server-assigned. Pass it when attaching a skill that
                must stay pinned to a specific revision.
            version_number (int): Monotonically increasing version counter within the skill, starting at 1. Server-assigned.
            artifact_sha256 (str | Unset): SHA-256 of the stored document, which is also its content address.
            bundle (ManagedAgentsSkillBundle | Unset): The files bundled with one skill version, stored as a single
                canonical archive and extracted into the session sandbox so the agent can read references and run scripts.
                Example: {'bytes': 1, 'entries': [{'bytes': 1, 'mode': 1, 'path': 'example', 'sha256': 'example'}], 'sha256':
                'example'}.
            created_by (str | Unset): Identifier of the caller that minted this version.
            entrypoint_path (str | Unset): Path of the document within the bundle. SKILL.md unless the author moved it.
            file_manifest (list[str] | Unset): Relative paths of files bundled with the skill. Listed to the model at
                activation; read only if it uses them.
            frontmatter (ManagedAgentsSkillVersionFrontmatter | Unset): The parsed SKILL.md frontmatter as authored,
                including fields this platform does not interpret.
            instructions (str | Unset): The skill's full Markdown instructions. Returned only when reading a single version,
                since a listing has no use for it.
            metadata (ManagedAgentsSkillVersionMetadata | Unset): Caller-owned key/value data stored with this version and
                returned unchanged.
     """

    created_at: datetime.datetime
    description: str
    name: str
    organization_id: str
    skill_id: str
    skill_version_id: str
    version_number: int
    artifact_sha256: str | Unset = UNSET
    bundle: ManagedAgentsSkillBundle | Unset = UNSET
    created_by: str | Unset = UNSET
    entrypoint_path: str | Unset = UNSET
    file_manifest: list[str] | Unset = UNSET
    frontmatter: ManagedAgentsSkillVersionFrontmatter | Unset = UNSET
    instructions: str | Unset = UNSET
    metadata: ManagedAgentsSkillVersionMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_skill_bundle import ManagedAgentsSkillBundle # noqa: PLC0415
        from ..models.managed_agents_skill_version_frontmatter import ManagedAgentsSkillVersionFrontmatter # noqa: PLC0415
        from ..models.managed_agents_skill_version_metadata import ManagedAgentsSkillVersionMetadata # noqa: PLC0415
        created_at = self.created_at.isoformat()

        description = self.description

        name = self.name

        organization_id = self.organization_id

        skill_id = self.skill_id

        skill_version_id = self.skill_version_id

        version_number = self.version_number

        artifact_sha256 = self.artifact_sha256

        bundle: dict[str, Any] | Unset = UNSET
        if not isinstance(self.bundle, Unset):
            bundle = self.bundle.to_dict()

        created_by = self.created_by

        entrypoint_path = self.entrypoint_path

        file_manifest: list[str] | Unset = UNSET
        if not isinstance(self.file_manifest, Unset):
            file_manifest = self.file_manifest



        frontmatter: dict[str, Any] | Unset = UNSET
        if not isinstance(self.frontmatter, Unset):
            frontmatter = self.frontmatter.to_dict()

        instructions = self.instructions

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "description": description,
            "name": name,
            "organization_id": organization_id,
            "skill_id": skill_id,
            "skill_version_id": skill_version_id,
            "version_number": version_number,
        })
        if artifact_sha256 is not UNSET:
            field_dict["artifact_sha256"] = artifact_sha256
        if bundle is not UNSET:
            field_dict["bundle"] = bundle
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if entrypoint_path is not UNSET:
            field_dict["entrypoint_path"] = entrypoint_path
        if file_manifest is not UNSET:
            field_dict["file_manifest"] = file_manifest
        if frontmatter is not UNSET:
            field_dict["frontmatter"] = frontmatter
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_skill_bundle import ManagedAgentsSkillBundle # noqa: PLC0415
        from ..models.managed_agents_skill_version_frontmatter import ManagedAgentsSkillVersionFrontmatter # noqa: PLC0415
        from ..models.managed_agents_skill_version_metadata import ManagedAgentsSkillVersionMetadata # noqa: PLC0415
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        description = d.pop("description")

        name = d.pop("name")

        organization_id = d.pop("organization_id")

        skill_id = d.pop("skill_id")

        skill_version_id = d.pop("skill_version_id")

        version_number = d.pop("version_number")

        artifact_sha256 = d.pop("artifact_sha256", UNSET)

        _bundle = d.pop("bundle", UNSET)
        bundle: ManagedAgentsSkillBundle | Unset
        if isinstance(_bundle,  Unset):
            bundle = UNSET
        else:
            bundle = ManagedAgentsSkillBundle.from_dict(_bundle)




        created_by = d.pop("created_by", UNSET)

        entrypoint_path = d.pop("entrypoint_path", UNSET)

        file_manifest = cast(list[str], d.pop("file_manifest", UNSET))


        _frontmatter = d.pop("frontmatter", UNSET)
        frontmatter: ManagedAgentsSkillVersionFrontmatter | Unset
        if isinstance(_frontmatter,  Unset):
            frontmatter = UNSET
        else:
            frontmatter = ManagedAgentsSkillVersionFrontmatter.from_dict(_frontmatter)




        instructions = d.pop("instructions", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsSkillVersionMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsSkillVersionMetadata.from_dict(_metadata)




        managed_agents_skill_version = cls(
            created_at=created_at,
            description=description,
            name=name,
            organization_id=organization_id,
            skill_id=skill_id,
            skill_version_id=skill_version_id,
            version_number=version_number,
            artifact_sha256=artifact_sha256,
            bundle=bundle,
            created_by=created_by,
            entrypoint_path=entrypoint_path,
            file_manifest=file_manifest,
            frontmatter=frontmatter,
            instructions=instructions,
            metadata=metadata,
        )


        managed_agents_skill_version.additional_properties = d
        return managed_agents_skill_version

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
