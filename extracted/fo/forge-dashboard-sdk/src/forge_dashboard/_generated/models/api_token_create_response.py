from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="APITokenCreateResponse")



@_attrs_define
class APITokenCreateResponse:
    """ The one and only response that ever carries the raw token value
    — shown to the user once, at creation time; only its hash is
    stored, so it can't be recovered from here again. Losing it
    means generating a new one.

        Attributes:
            id (str):
            label (str):
            created_at (datetime.datetime):
            expires_at (datetime.datetime):
            token (str): The raw Bearer credential: `Authorization: Bearer <token>`.
     """

    id: str
    label: str
    created_at: datetime.datetime
    expires_at: datetime.datetime
    token: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        label = self.label

        created_at = self.created_at.isoformat()

        expires_at = self.expires_at.isoformat()

        token = self.token


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "label": label,
            "createdAt": created_at,
            "expiresAt": expires_at,
            "token": token,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        label = d.pop("label")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        expires_at = datetime.datetime.fromisoformat(d.pop("expiresAt"))




        token = d.pop("token")

        api_token_create_response = cls(
            id=id,
            label=label,
            created_at=created_at,
            expires_at=expires_at,
            token=token,
        )


        api_token_create_response.additional_properties = d
        return api_token_create_response

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
