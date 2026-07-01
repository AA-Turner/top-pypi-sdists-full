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
        dataplane_id (str): Data plane id for this org.
        date_added (datetime.datetime): datetime with the constraint that the value must have timezone info
        date_updated (datetime.datetime): datetime with the constraint that the value must have timezone info
        description (None | str): The description of the organization
        id (UUID): The unique ID of the entity
        name (str): The name of the organization
    """

    dataplane_id: str
    date_added: datetime.datetime
    date_updated: datetime.datetime
    description: None | str
    id: UUID
    name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dataplane_id = self.dataplane_id

        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        description: None | str
        description = self.description

        id = str(self.id)

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataplane_id": dataplane_id,
                "date_added": date_added,
                "date_updated": date_updated,
                "description": description,
                "id": id,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dataplane_id = d.pop("dataplane_id")

        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        id = UUID(d.pop("id"))

        name = d.pop("name")

        organization_response = cls(
            dataplane_id=dataplane_id,
            date_added=date_added,
            date_updated=date_updated,
            description=description,
            id=id,
            name=name,
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
