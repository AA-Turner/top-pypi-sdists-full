from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserResponse")


@_attrs_define
class UserResponse:
    """
    Attributes:
        date_added (datetime.datetime): datetime with the constraint that the value must have timezone info
        date_updated (datetime.datetime): datetime with the constraint that the value must have timezone info
        email (str): The user's email address
        id (UUID): The unique ID of the entity
        last_organization_id (None | Unset | UUID): The organization the user last operated in, if any
        last_seen (datetime.datetime | None | Unset): When the user's identity was last synced from a request; null if
            never seen
        last_workspace_id (None | Unset | UUID): The workspace the user last operated in, if any
        primary_organization_id (None | Unset | UUID): The user's primary (billing) organization, if any
    """

    date_added: datetime.datetime
    date_updated: datetime.datetime
    email: str
    id: UUID
    last_organization_id: None | Unset | UUID = UNSET
    last_seen: datetime.datetime | None | Unset = UNSET
    last_workspace_id: None | Unset | UUID = UNSET
    primary_organization_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        email = self.email

        id = str(self.id)

        last_organization_id: None | str | Unset
        if isinstance(self.last_organization_id, Unset):
            last_organization_id = UNSET
        elif isinstance(self.last_organization_id, UUID):
            last_organization_id = str(self.last_organization_id)
        else:
            last_organization_id = self.last_organization_id

        last_seen: None | str | Unset
        if isinstance(self.last_seen, Unset):
            last_seen = UNSET
        elif isinstance(self.last_seen, datetime.datetime):
            last_seen = self.last_seen.isoformat()
        else:
            last_seen = self.last_seen

        last_workspace_id: None | str | Unset
        if isinstance(self.last_workspace_id, Unset):
            last_workspace_id = UNSET
        elif isinstance(self.last_workspace_id, UUID):
            last_workspace_id = str(self.last_workspace_id)
        else:
            last_workspace_id = self.last_workspace_id

        primary_organization_id: None | str | Unset
        if isinstance(self.primary_organization_id, Unset):
            primary_organization_id = UNSET
        elif isinstance(self.primary_organization_id, UUID):
            primary_organization_id = str(self.primary_organization_id)
        else:
            primary_organization_id = self.primary_organization_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date_added": date_added,
                "date_updated": date_updated,
                "email": email,
                "id": id,
            }
        )
        if last_organization_id is not UNSET:
            field_dict["last_organization_id"] = last_organization_id
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen
        if last_workspace_id is not UNSET:
            field_dict["last_workspace_id"] = last_workspace_id
        if primary_organization_id is not UNSET:
            field_dict["primary_organization_id"] = primary_organization_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        email = d.pop("email")

        id = UUID(d.pop("id"))

        def _parse_last_organization_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_organization_id_type_0 = UUID(data)

                return last_organization_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        last_organization_id = _parse_last_organization_id(
            d.pop("last_organization_id", UNSET)
        )

        def _parse_last_seen(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_seen_type_0 = isoparse(data)

                return last_seen_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_seen = _parse_last_seen(d.pop("last_seen", UNSET))

        def _parse_last_workspace_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_workspace_id_type_0 = UUID(data)

                return last_workspace_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        last_workspace_id = _parse_last_workspace_id(d.pop("last_workspace_id", UNSET))

        def _parse_primary_organization_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                primary_organization_id_type_0 = UUID(data)

                return primary_organization_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        primary_organization_id = _parse_primary_organization_id(
            d.pop("primary_organization_id", UNSET)
        )

        user_response = cls(
            date_added=date_added,
            date_updated=date_updated,
            email=email,
            id=id,
            last_organization_id=last_organization_id,
            last_seen=last_seen,
            last_workspace_id=last_workspace_id,
            primary_organization_id=primary_organization_id,
        )

        user_response.additional_properties = d
        return user_response

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
