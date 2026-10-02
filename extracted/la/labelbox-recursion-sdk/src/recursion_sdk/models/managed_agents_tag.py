from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="ManagedAgentsTag")



@_attrs_define
class ManagedAgentsTag:
    """ An organization-scoped classification definition. Applying or removing it changes only catalog membership: it does
    not update the agent, mint an AgentVersion, or affect running sessions.

        Example:
            {'color': '#14b8a6', 'created_at': '2026-02-18T09:30:00Z', 'description': 'example', 'label': 'example',
                'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tag_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'updated_at': '2026-02-18T09:30:00Z'}

        Attributes:
            color (str): Display color in #RRGGBB form.
            created_at (datetime.datetime): Server-assigned RFC 3339 timestamp of when the tag was created.
            label (str): Display label, trimmed by the service. Unique case-insensitively among live tags in this
                organization.
            organization_id (str): Organization that owns the tag. Server-assigned from the authenticated principal and
                never accepted as authority from the request body.
            tag_id (UUID): Server-assigned tag id (UUID).
            updated_at (datetime.datetime): Server-assigned RFC 3339 timestamp of the most recent definition update.
            description (str | Unset): Optional operator-facing explanation of the classification, up to 280 characters.
     """

    color: str
    created_at: datetime.datetime
    label: str
    organization_id: str
    tag_id: UUID
    updated_at: datetime.datetime
    description: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        color = self.color

        created_at = self.created_at.isoformat()

        label = self.label

        organization_id = self.organization_id

        tag_id = str(self.tag_id)

        updated_at = self.updated_at.isoformat()

        description = self.description


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "color": color,
            "created_at": created_at,
            "label": label,
            "organization_id": organization_id,
            "tag_id": tag_id,
            "updated_at": updated_at,
        })
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        color = d.pop("color")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        label = d.pop("label")

        organization_id = d.pop("organization_id")

        tag_id = UUID(d.pop("tag_id"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        description = d.pop("description", UNSET)

        managed_agents_tag = cls(
            color=color,
            created_at=created_at,
            label=label,
            organization_id=organization_id,
            tag_id=tag_id,
            updated_at=updated_at,
            description=description,
        )


        managed_agents_tag.additional_properties = d
        return managed_agents_tag

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
