from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="OrganizationResponse")


@_attrs_define
class OrganizationResponse:
    """The organization where new workspaces are created by default

    Attributes:
        created_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        dataplane_id (None | str): Data plane id for this org; null until a region is set.
        description (None | str): The description of the organization
        id (UUID): The unique ID of the entity
        name (str): The name of the organization
        updated_at (datetime.datetime): datetime with the constraint that the value must have timezone info
    """

    created_at: datetime.datetime
    dataplane_id: None | str
    description: None | str
    id: UUID
    name: str
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        dataplane_id: None | str
        dataplane_id = self.dataplane_id

        description: None | str
        description = self.description

        id = str(self.id)

        name = self.name

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "dataplane_id": dataplane_id,
                "description": description,
                "id": id,
                "name": name,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))

        def _parse_dataplane_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        dataplane_id = _parse_dataplane_id(d.pop("dataplane_id"))

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        id = UUID(d.pop("id"))

        name = d.pop("name")

        updated_at = isoparse(d.pop("updated_at"))

        organization_response = cls(
            created_at=created_at,
            dataplane_id=dataplane_id,
            description=description,
            id=id,
            name=name,
            updated_at=updated_at,
        )

        organization_response.additional_properties = d
        return organization_response

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
