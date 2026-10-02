import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Tag")


@_attrs_define
class Tag:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        offering_count (int): Return offering count filtered by user permissions.
            Staff sees all offerings.
            Service providers see their own + active/paused/archived public offerings.
        created (datetime.datetime):
        created_by_username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_
            characters
        created_by_full_name (str):
        description (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    name: str
    offering_count: int
    created: datetime.datetime
    created_by_username: str
    created_by_full_name: str
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        offering_count = self.offering_count

        created = self.created.isoformat()

        created_by_username = self.created_by_username

        created_by_full_name = self.created_by_full_name

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "offering_count": offering_count,
                "created": created,
                "created_by_username": created_by_username,
                "created_by_full_name": created_by_full_name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        offering_count = d.pop("offering_count")

        created = isoparse(d.pop("created"))

        created_by_username = d.pop("created_by_username")

        created_by_full_name = d.pop("created_by_full_name")

        description = d.pop("description", UNSET)

        tag = cls(
            url=url,
            uuid=uuid,
            name=name,
            offering_count=offering_count,
            created=created,
            created_by_username=created_by_username,
            created_by_full_name=created_by_full_name,
            description=description,
        )

        tag.additional_properties = d
        return tag

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
