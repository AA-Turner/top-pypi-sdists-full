from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="VncCredential")


@_attrs_define
class VncCredential:
    """
    Attributes:
        id (str):
        display_name (str):
        locator (str):
        created_by_user_id (str):
        created_at (datetime.datetime):
        last_used_at (datetime.datetime | None | Unset):
        revoked_at (datetime.datetime | None | Unset):
    """

    id: str
    display_name: str
    locator: str
    created_by_user_id: str
    created_at: datetime.datetime
    last_used_at: datetime.datetime | None | Unset = UNSET
    revoked_at: datetime.datetime | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        display_name = self.display_name

        locator = self.locator

        created_by_user_id = self.created_by_user_id

        created_at = self.created_at.isoformat()

        last_used_at: None | str | Unset
        if isinstance(self.last_used_at, Unset):
            last_used_at = UNSET
        elif isinstance(self.last_used_at, datetime.datetime):
            last_used_at = self.last_used_at.isoformat()
        else:
            last_used_at = self.last_used_at

        revoked_at: None | str | Unset
        if isinstance(self.revoked_at, Unset):
            revoked_at = UNSET
        elif isinstance(self.revoked_at, datetime.datetime):
            revoked_at = self.revoked_at.isoformat()
        else:
            revoked_at = self.revoked_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "display_name": display_name,
                "locator": locator,
                "created_by_user_id": created_by_user_id,
                "created_at": created_at,
            }
        )
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at
        if revoked_at is not UNSET:
            field_dict["revoked_at"] = revoked_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        display_name = d.pop("display_name")

        locator = d.pop("locator")

        created_by_user_id = d.pop("created_by_user_id")

        created_at = datetime.datetime.fromisoformat(
            d.pop("created_at").replace("Z", "+00:00")
        )

        def _parse_last_used_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_used_at_type_0 = datetime.datetime.fromisoformat(
                    data.replace("Z", "+00:00")
                )

                return last_used_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at", UNSET))

        def _parse_revoked_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                revoked_at_type_0 = datetime.datetime.fromisoformat(
                    data.replace("Z", "+00:00")
                )

                return revoked_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        revoked_at = _parse_revoked_at(d.pop("revoked_at", UNSET))

        vnc_credential = cls(
            id=id,
            display_name=display_name,
            locator=locator,
            created_by_user_id=created_by_user_id,
            created_at=created_at,
            last_used_at=last_used_at,
            revoked_at=revoked_at,
        )

        return vnc_credential
