from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="CreateUserApiKeyResponse")


@_attrs_define
class CreateUserApiKeyResponse:
    """
    Attributes:
        date_added (datetime.datetime): datetime with the constraint that the value must have timezone info
        date_updated (datetime.datetime): datetime with the constraint that the value must have timezone info
        expires_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        id (UUID): The unique ID of the entity
        key (str): The plaintext API key. Shown once at creation, never stored.
        key_prefix (str): The first 8 characters of the key for identification
        name (str): The label for the API key
    """

    date_added: datetime.datetime
    date_updated: datetime.datetime
    expires_at: datetime.datetime
    id: UUID
    key: str
    key_prefix: str
    name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        expires_at = self.expires_at.isoformat()

        id = str(self.id)

        key = self.key

        key_prefix = self.key_prefix

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date_added": date_added,
                "date_updated": date_updated,
                "expires_at": expires_at,
                "id": id,
                "key": key,
                "key_prefix": key_prefix,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        expires_at = isoparse(d.pop("expires_at"))

        id = UUID(d.pop("id"))

        key = d.pop("key")

        key_prefix = d.pop("key_prefix")

        name = d.pop("name")

        create_user_api_key_response = cls(
            date_added=date_added,
            date_updated=date_updated,
            expires_at=expires_at,
            id=id,
            key=key,
            key_prefix=key_prefix,
            name=name,
        )

        create_user_api_key_response.additional_properties = d
        return create_user_api_key_response

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
