from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="AgentSkillPageDtoItemsItem")



@_attrs_define
class AgentSkillPageDtoItemsItem:
    """ An unversioned, mutable skill catalog entry — org-scoped or platform-wide — whose SKILL.md bundle is mounted into an
    agent workspace.

        Attributes:
            id (UUID): Stable skill identifier (UUID). Org-uploaded or platform-curated skill bundle mounted into an agent
                workspace.
            organization_id (None | UUID): Owning organization, or null for a platform skill visible to every org.
            slug (str): URL-safe skill slug unique within the owning org (or among platform skills). Lowercase alphanumeric
                with hyphens.
            name (str): Human-readable skill name shown in the harness skills index.
            description (str): Short description surfaced in the harness skills index.
            file_id (UUID): Current SKILL.md bundle file id. Replacing this file_id is how a skill is updated.
            created_at (datetime.datetime): Timestamp when the skill was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the skill was last updated (ISO-8601, UTC).
     """

    id: UUID
    organization_id: None | UUID
    slug: str
    name: str
    description: str
    file_id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        organization_id: None | str
        if isinstance(self.organization_id, UUID):
            organization_id = str(self.organization_id)
        else:
            organization_id = self.organization_id

        slug = self.slug

        name = self.name

        description = self.description

        file_id = str(self.file_id)

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "organizationId": organization_id,
            "slug": slug,
            "name": name,
            "description": description,
            "fileId": file_id,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_organization_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                organization_id_type_0 = UUID(data)



                return organization_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        organization_id = _parse_organization_id(d.pop("organizationId"))


        slug = d.pop("slug")

        name = d.pop("name")

        description = d.pop("description")

        file_id = UUID(d.pop("fileId"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        agent_skill_page_dto_items_item = cls(
            id=id,
            organization_id=organization_id,
            slug=slug,
            name=name,
            description=description,
            file_id=file_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        return agent_skill_page_dto_items_item

