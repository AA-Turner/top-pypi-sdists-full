from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="APIToken")



@_attrs_define
class APIToken:
    """ A personal API token's own metadata — never the token value
    itself, which only ever appears once, in
    APITokenCreateResponse's own response body at creation time.

        Attributes:
            id (str):
            label (str): The name given at creation time, so a list of several is tellable apart.
            created_at (datetime.datetime):
            expires_at (datetime.datetime): When this token stops authenticating requests —
                always set, mandatory at creation, no "never expires"
                option. A token whose expiration has passed is rejected the
                same way an invalid one is.
            last_used_at (datetime.datetime | Unset): Omitted if this token has never authenticated a request yet.
     """

    id: str
    label: str
    created_at: datetime.datetime
    expires_at: datetime.datetime
    last_used_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        label = self.label

        created_at = self.created_at.isoformat()

        expires_at = self.expires_at.isoformat()

        last_used_at: str | Unset = UNSET
        if not isinstance(self.last_used_at, Unset):
            last_used_at = self.last_used_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "label": label,
            "createdAt": created_at,
            "expiresAt": expires_at,
        })
        if last_used_at is not UNSET:
            field_dict["lastUsedAt"] = last_used_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        label = d.pop("label")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        expires_at = datetime.datetime.fromisoformat(d.pop("expiresAt"))




        _last_used_at = d.pop("lastUsedAt", UNSET)
        last_used_at: datetime.datetime | Unset
        if isinstance(_last_used_at,  Unset):
            last_used_at = UNSET
        else:
            last_used_at = datetime.datetime.fromisoformat(_last_used_at)




        api_token = cls(
            id=id,
            label=label,
            created_at=created_at,
            expires_at=expires_at,
            last_used_at=last_used_at,
        )


        api_token.additional_properties = d
        return api_token

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
