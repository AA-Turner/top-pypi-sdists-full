from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="UserApiKeyResponse")


@_attrs_define
class UserApiKeyResponse:
    """
    Attributes:
        date_added (datetime.datetime): datetime with the constraint that the value must have timezone info
        date_updated (datetime.datetime): datetime with the constraint that the value must have timezone info
        expires_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        id (UUID): The unique ID of the entity
        key_prefix (str): The first 8 characters of the key for identification
        last_used_at (datetime.datetime | None): When the key was last used for authentication
        name (str): The label for the API key
        revoked_at (datetime.datetime | None): When the key was revoked, null if active
    """

    date_added: datetime.datetime
    date_updated: datetime.datetime
    expires_at: datetime.datetime
    id: UUID
    key_prefix: str
    last_used_at: datetime.datetime | None
    name: str
    revoked_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        expires_at = self.expires_at.isoformat()

        id = str(self.id)

        key_prefix = self.key_prefix

        last_used_at: None | str
        if isinstance(self.last_used_at, datetime.datetime):
            last_used_at = self.last_used_at.isoformat()
        else:
            last_used_at = self.last_used_at

        name = self.name

        revoked_at: None | str
        if isinstance(self.revoked_at, datetime.datetime):
            revoked_at = self.revoked_at.isoformat()
        else:
            revoked_at = self.revoked_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date_added": date_added,
                "date_updated": date_updated,
                "expires_at": expires_at,
                "id": id,
                "key_prefix": key_prefix,
                "last_used_at": last_used_at,
                "name": name,
                "revoked_at": revoked_at,
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

        key_prefix = d.pop("key_prefix")

        def _parse_last_used_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_used_at_type_0 = isoparse(data)

                return last_used_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at"))

        name = d.pop("name")

        def _parse_revoked_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                revoked_at_type_0 = isoparse(data)

                return revoked_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        revoked_at = _parse_revoked_at(d.pop("revoked_at"))

        user_api_key_response = cls(
            date_added=date_added,
            date_updated=date_updated,
            expires_at=expires_at,
            id=id,
            key_prefix=key_prefix,
            last_used_at=last_used_at,
            name=name,
            revoked_at=revoked_at,
        )

        user_api_key_response.additional_properties = d
        return user_api_key_response

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
