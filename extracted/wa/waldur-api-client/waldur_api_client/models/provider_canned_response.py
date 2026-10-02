import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProviderCannedResponse")


@_attrs_define
class ProviderCannedResponse:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        provider_helpdesk (UUID):
        text (str): Template text. Supports Django template syntax.
        usage_count (int):
        created (datetime.datetime):
        modified (datetime.datetime):
        category (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    name: str
    provider_helpdesk: UUID
    text: str
    usage_count: int
    created: datetime.datetime
    modified: datetime.datetime
    category: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        provider_helpdesk = str(self.provider_helpdesk)

        text = self.text

        usage_count = self.usage_count

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "provider_helpdesk": provider_helpdesk,
                "text": text,
                "usage_count": usage_count,
                "created": created,
                "modified": modified,
            }
        )
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        provider_helpdesk = UUID(d.pop("provider_helpdesk"))

        text = d.pop("text")

        usage_count = d.pop("usage_count")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        category = d.pop("category", UNSET)

        provider_canned_response = cls(
            url=url,
            uuid=uuid,
            name=name,
            provider_helpdesk=provider_helpdesk,
            text=text,
            usage_count=usage_count,
            created=created,
            modified=modified,
            category=category,
        )

        provider_canned_response.additional_properties = d
        return provider_canned_response

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
