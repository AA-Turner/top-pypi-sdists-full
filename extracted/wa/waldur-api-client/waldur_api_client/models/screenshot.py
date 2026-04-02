import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Screenshot")


@_attrs_define
class Screenshot:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        created (datetime.datetime):
        image (str):
        thumbnail (Union[None, str]):
        offering (str):
        customer_uuid (UUID):
        description (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    name: str
    created: datetime.datetime
    image: str
    thumbnail: Union[None, str]
    offering: str
    customer_uuid: UUID
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        created = self.created.isoformat()

        image = self.image

        thumbnail: Union[None, str]
        thumbnail = self.thumbnail

        offering = self.offering

        customer_uuid = str(self.customer_uuid)

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "created": created,
                "image": image,
                "thumbnail": thumbnail,
                "offering": offering,
                "customer_uuid": customer_uuid,
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

        created = isoparse(d.pop("created"))

        image = d.pop("image")

        def _parse_thumbnail(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        thumbnail = _parse_thumbnail(d.pop("thumbnail"))

        offering = d.pop("offering")

        customer_uuid = UUID(d.pop("customer_uuid"))

        description = d.pop("description", UNSET)

        screenshot = cls(
            url=url,
            uuid=uuid,
            name=name,
            created=created,
            image=image,
            thumbnail=thumbnail,
            offering=offering,
            customer_uuid=customer_uuid,
            description=description,
        )

        screenshot.additional_properties = d
        return screenshot

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
